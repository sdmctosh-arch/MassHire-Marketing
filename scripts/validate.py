#!/usr/bin/env python3
"""Validate every plugin in plugins/ before it is packaged or merged.

Checks:
  - marketplace.json parses and lists exactly the plugins in plugins/
  - each plugin.json parses, has a semver version, and a complete description
    (the upload format truncates at 500 chars)
  - each SKILL.md has front matter with a matching name and a description <= 1024 chars
  - playbooks, templates, and systems named in SKILL.md exist
  - every systems/*.md is named as `<name>` by SKILL.md, a playbook, or a component
  - every component a playbook task table names exists, and every component
    is named in some playbook task table
  - the field contract: every name a task table's `uses` column holds is a
    field the same playbook's field tables declare; every `needs` entry
    names an earlier row of the same table; the template's values block
    holds every field two or more tasks use, and nothing undeclared
  - every skill named as "the `x` skill" exists in this repo
  - every tests/scenarios/*.md has Message, World, Assertions and numbered assertions
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


def rel(p):
    return p.relative_to(ROOT)


def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as e:  # noqa: BLE001
        err(f"{rel(path)}: invalid JSON ({e})")
        return {}


def front_matter(text):
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        return None
    meta = {}
    for k, v in re.findall(r"^(\w+):\s*(.*)$", fm.group(1), re.M):
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        meta[k] = v
    return meta


market = load_json(ROOT / ".claude-plugin/marketplace.json")
listed = {p.get("name"): p.get("source") for p in market.get("plugins", [])}
plugin_dirs = sorted(p for p in (ROOT / "plugins").iterdir() if p.is_dir())
all_skills = {s.parent.name for s in ROOT.glob("plugins/*/skills/*/SKILL.md")}

for name in set(listed) - {p.name for p in plugin_dirs}:
    err(f"marketplace.json: lists '{name}' but plugins/{name} does not exist")

for pdir in plugin_dirs:
    manifest = pdir / ".claude-plugin/plugin.json"
    if not manifest.exists():
        err(f"{rel(pdir)}: missing .claude-plugin/plugin.json")
        continue
    plugin = load_json(manifest)
    pname = plugin.get("name")
    if pname != pdir.name:
        err(f"{rel(manifest)}: name '{pname}' != folder '{pdir.name}'")
    if listed.get(pdir.name) != f"./plugins/{pdir.name}":
        err(f"marketplace.json: '{pdir.name}' missing or source is not ./plugins/{pdir.name}")
    desc = plugin.get("description", "")
    if not desc:
        err(f"{rel(manifest)}: missing description")
    elif len(desc) > 500:
        err(f"{rel(manifest)}: description is {len(desc)} chars; keep it <= 500")
    elif not desc.rstrip().endswith((".", ")")):
        err(f"{rel(manifest)}: description looks truncated (does not end with '.')")
    if not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
        err(f"{rel(manifest)}: version must be semver (x.y.z)")

    skills = sorted((pdir / "skills").glob("*/SKILL.md"))
    if not skills:
        err(f"{rel(pdir)}: no skills/*/SKILL.md found")

    for skill_md in skills:
        sdir = skill_md.parent
        text = skill_md.read_text()
        meta = front_matter(text)
        if meta is None:
            err(f"{rel(skill_md)}: missing YAML front matter")
            continue
        if meta.get("name") != sdir.name:
            err(f"{rel(skill_md)}: front matter name '{meta.get('name')}' != folder '{sdir.name}'")
        sdesc = meta.get("description", "")
        if not sdesc:
            err(f"{rel(skill_md)}: missing description")
        elif len(sdesc) > 1024:
            err(f"{rel(skill_md)}: description is {len(sdesc)} chars; keep it <= 1024")

        for ref in re.findall(r"`((?:playbooks|templates|systems)/[\w-]+\.md)`", text):
            if not (sdir / ref).exists():
                err(f"{rel(skill_md)}: references missing {ref}")

        components = {p.stem for p in (sdir / "components").glob("*.md")}
        callers = "\n".join(
            md.read_text() for d in ("playbooks", "components") for md in (sdir / d).glob("*.md")
        ) + text
        for sysmd in sorted((sdir / "systems").glob("*.md")):
            if f"`{sysmd.stem}`" not in callers and f"systems/{sysmd.name}" not in callers:
                err(f"{rel(sysmd)}: no SKILL.md, playbook, or component names it")
        for md in sorted(sdir.rglob("*.md")):
            body = md.read_text()
            for other in re.findall(r"the `([\w-]+)` skill", body):
                if other not in all_skills:
                    err(f"{rel(md)}: names skill '{other}', which is not in this repo")

        tabled = set()
        shared_by_playbook = {}
        fields_by_playbook = {}
        for pb in sorted((sdir / "playbooks").glob("*.md")):
            in_tasks = False
            fields, rows, use_count = set(), {}, {}
            for line in pb.read_text().splitlines():
                if line.startswith("| # | Task | Component"):
                    in_tasks = True
                    continue
                if in_tasks and not line.startswith("|"):
                    in_tasks = False
                if not line.startswith("|") or line.startswith("|---"):
                    continue
                cols = [c.strip() for c in line.strip("|").split("|")]
                if not in_tasks:
                    # A field table row declares the backticked names in its first cell.
                    fields.update(re.findall(r"`([\w-]+)`", cols[0]))
                    continue
                if len(cols) < 5 or not cols[0].isdigit():
                    continue
                num = int(cols[0])
                rows[num] = cols[1]
                for name in re.findall(r"`([\w-]+)`", cols[2]):
                    tabled.add(name)
                    if name not in components:
                        err(f"{rel(pb)}: task table names missing component '{name}'")
                for n in (int(x) for x in re.findall(r"\d+", cols[3])):
                    if n not in rows or n >= num:
                        err(f"{rel(pb)}: task {num} needs {n}, which is not an earlier row")
                if cols[4] not in ("—", "all facts"):
                    for name in re.findall(r"[\w-]+", cols[4]):
                        use_count[name] = use_count.get(name, 0) + 1
            for name in sorted(use_count):
                if name not in fields:
                    err(f"{rel(pb)}: task table uses '{name}', which no field table declares")
            fields_by_playbook[pb.stem] = fields
            shared_by_playbook[pb.stem] = {n for n, c in use_count.items() if c >= 2}
        for name in sorted(components - tabled):
            err(f"{rel(sdir)}/components/{name}.md: not named in any playbook task table")

        # The template's values block is the shared-field contract.
        tmpl = sdir / "templates/project-file.md"
        if tmpl.exists() and "event" in fields_by_playbook:
            ttext = tmpl.read_text()
            fm = re.match(r"^---\n(.*?)\n---\n", ttext, re.S)
            block = re.search(r"^values:\n((?:  \w+:.*\n)+)", fm.group(1) + "\n", re.M) if fm else None
            event_values = set(re.findall(r"^  (\w+):", block.group(1), re.M)) if block else set()
            if not event_values:
                err(f"{rel(tmpl)}: no values block in the front matter")
            for name in sorted(event_values - fields_by_playbook["event"]):
                err(f"{rel(tmpl)}: values block holds '{name}', which playbooks/event.md does not declare")
            for name in sorted(shared_by_playbook["event"] - event_values):
                err(f"{rel(tmpl)}: '{name}' is used by two or more event tasks but is not in the values block")
            for pb_name, shared in shared_by_playbook.items():
                if pb_name == "event":
                    continue
                row = re.search(rf"^\| {re.escape(pb_name.split('-')[0])} \| (.*) \|$", ttext, re.M)
                declared = set(re.findall(r"`([\w-]+)`", row.group(1))) if row else set()
                if not row:
                    err(f"{rel(tmpl)}: no 'Values block' row for type '{pb_name.split('-')[0]}'")
                for name in sorted(declared - fields_by_playbook[pb_name]):
                    err(f"{rel(tmpl)}: {pb_name} values row holds '{name}', which playbooks/{pb_name}.md does not declare")
                for name in sorted(shared - declared):
                    err(f"{rel(tmpl)}: '{name}' is used by two or more {pb_name} tasks but is not in its values row")

# Behavior-test scenarios: three sections, numbered assertions.
for sc in sorted((ROOT / "tests/scenarios").glob("*.md")):
    body = sc.read_text()
    heads = re.findall(r"^## (.+)$", body, re.M)
    if heads != ["Message", "World", "Assertions"]:
        err(f"{rel(sc)}: sections must be Message, World, Assertions in order (found {heads})")
        continue
    nums = [int(n) for n in re.findall(r"^(\d+)\. ", body.split("## Assertions", 1)[1], re.M)]
    if not nums or nums != list(range(1, len(nums) + 1)):
        err(f"{rel(sc)}: assertions must be numbered 1..n")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
for pdir in plugin_dirs:
    v = json.loads((pdir / ".claude-plugin/plugin.json").read_text())["version"]
    print(f"OK: {pdir.name} {v}")

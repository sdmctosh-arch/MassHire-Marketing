#!/usr/bin/env python3
"""Validate every plugin in plugins/ before it is packaged or merged.

Checks:
  - marketplace.json parses and lists exactly the plugins in plugins/
  - each plugin.json parses, has a semver version, and a complete description
    (the upload format truncates at 500 chars)
  - each SKILL.md has front matter with a matching name and a description <= 1024 chars
  - playbooks and templates named in SKILL.md exist
  - every component a playbook task table names exists
  - every skill named as "the `x` skill" exists in this repo
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

        for ref in re.findall(r"`((?:playbooks|templates)/[\w-]+\.md)`", text):
            if not (sdir / ref).exists():
                err(f"{rel(skill_md)}: references missing {ref}")

        components = {p.stem for p in (sdir / "components").glob("*.md")}
        for md in sorted(sdir.rglob("*.md")):
            body = md.read_text()
            for other in re.findall(r"the `([\w-]+)` skill", body):
                if other not in all_skills:
                    err(f"{rel(md)}: names skill '{other}', which is not in this repo")

        for pb in sorted((sdir / "playbooks").glob("*.md")):
            in_tasks = False
            for line in pb.read_text().splitlines():
                if line.startswith("| # | Task | Component"):
                    in_tasks = True
                    continue
                if in_tasks and not line.startswith("|"):
                    in_tasks = False
                if not in_tasks or line.startswith("|---"):
                    continue
                cols = [c.strip() for c in line.strip("|").split("|")]
                if len(cols) < 3:
                    continue
                for name in re.findall(r"`([\w-]+)`", cols[2]):
                    if name not in components:
                        err(f"{rel(pb)}: task table names missing component '{name}'")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
for pdir in plugin_dirs:
    v = json.loads((pdir / ".claude-plugin/plugin.json").read_text())["version"]
    print(f"OK: {pdir.name} {v}")

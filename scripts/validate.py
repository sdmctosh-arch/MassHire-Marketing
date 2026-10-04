#!/usr/bin/env python3
"""Validate the masshire-projects plugin before it is packaged or merged.

Checks:
  - plugin.json and marketplace.json parse, and their names agree
  - plugin.json description is a complete sentence (the upload format truncates at 500 chars)
  - every skill has SKILL.md front matter with a matching name and a description <= 1024 chars
  - every component named in a playbook task table exists in components/
  - every playbook listed in SKILL.md's Project types table exists
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Skills referenced by name that live outside this repo.
EXTERNAL = {"masshire-email"}

errors = []


def err(msg):
    errors.append(msg)


def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as e:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: invalid JSON ({e})")
        return {}


plugin = load_json(ROOT / ".claude-plugin/plugin.json")
market = load_json(ROOT / ".claude-plugin/marketplace.json")

desc = plugin.get("description", "")
if not desc:
    err("plugin.json: missing description")
elif len(desc) > 500:
    err(f"plugin.json: description is {len(desc)} chars; keep it <= 500")
elif not desc.rstrip().endswith((".", ")")):
    err("plugin.json: description looks truncated (does not end with '.')")
if not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
    err("plugin.json: version must be semver (x.y.z)")

names = {p.get("name") for p in market.get("plugins", [])}
if plugin.get("name") not in names:
    err(f"marketplace.json: no entry for plugin '{plugin.get('name')}'")

skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skills:
    err("no skills/*/SKILL.md found")

for skill_md in skills:
    skill_dir = skill_md.parent
    rel = skill_md.relative_to(ROOT)
    text = skill_md.read_text()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        err(f"{rel}: missing YAML front matter")
        continue
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", fm.group(1), re.M))
    if meta.get("name") != skill_dir.name:
        err(f"{rel}: front matter name '{meta.get('name')}' != folder '{skill_dir.name}'")
    sdesc = meta.get("description", "")
    if not sdesc:
        err(f"{rel}: missing description")
    elif len(sdesc) > 1024:
        err(f"{rel}: description is {len(sdesc)} chars; keep it <= 1024")

    components = {p.stem for p in (skill_dir / "components").glob("*.md")}

    # Playbooks listed in SKILL.md must exist.
    for pb in re.findall(r"`(playbooks/[\w-]+\.md)`", text):
        if not (skill_dir / pb).exists():
            err(f"{rel}: references missing {pb}")
    for tpl in re.findall(r"`(templates/[\w-]+\.md)`", text):
        if not (skill_dir / tpl).exists():
            err(f"{rel}: references missing {tpl}")

    # Components named in each playbook's task table must exist.
    for pb in sorted((skill_dir / "playbooks").glob("*.md")):
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
                if name not in components and name not in EXTERNAL:
                    err(f"{pb.relative_to(ROOT)}: task table names missing component '{name}'")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {plugin.get('name')} {plugin.get('version')} ({len(skills)} skill(s))")

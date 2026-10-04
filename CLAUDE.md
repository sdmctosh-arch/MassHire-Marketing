# CLAUDE.md

This repo holds the `masshire-projects` skill (see README.md). Editing here
changes the skill's source; it does not run a project.

## Where a rule goes

The skill has three layers. Put each sentence in exactly one:

- `SKILL.md` — universal rules: the run, gates, preflight, storage, concurrency.
- `playbooks/<type>.md` — what a project type requires: fields, defaults,
  task list, execute list, operator actions.
- `components/<task>.md` — how one task is done in one system: tool facts,
  ids, API calls, checks.
- Project facts never go in this repo; they live in the project file in Drive.

When a rule moves or is superseded, delete the old text in the same change.

## Before committing

- Run `scripts/validate.py` (or `scripts/package.sh`).
- A new component must appear in a playbook task table, and every component
  a task table names must exist — the validator checks this.
- Keep `.claude-plugin/plugin.json`'s description under 500 characters and a
  complete sentence; the SKILL.md front-matter description is what triggers
  the skill and must stay under 1024.
- Bump the plugin `version` and add a CHANGELOG.md line.
- Do not put tokens or credentials in any file. The Eventbrite token lives in
  Drive; the skill only names where to read it.

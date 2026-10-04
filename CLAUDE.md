# CLAUDE.md

This repo holds the `masshire-projects` skill, packaged as a plugin under
`plugins/` (see README.md). Editing here changes the skill's source; it does
not run a project or send an email.

## Where a rule goes

The system never sends or schedules anything: no send date, send time,
resend, or post date, in any file. Reject any rule that would add one.

Copy rules (the parts, voice, the gap marker, content by kind) live in
`components/description-copy.md`. Email rules (base HTML, subject lines,
compliance, Constant Contact tool facts) live in
`components/constant-contact-email.md`.

The skill has four layers (ADR-0001). Put each sentence in exactly one:

- `SKILL.md` — universal rules: the run, gates, preflight, concurrency.
- `playbooks/<type>.md` — what a project type requires: fields, defaults,
  task list, execute list, operator actions.
- `components/<task>.md` — how one task is done in one system: tool facts,
  ids, API calls, checks.
- `systems/<system>.md` — how a system that is not one task is used, shared
  by every task that touches it: ids, call shapes, read and write rules.
  `project-store` (Drive) is one. A system file is named by SKILL.md, a
  playbook, or a component — the validator checks this.
- Project facts never go in this repo; they live in the project file in Drive.

When a rule moves or is superseded, delete the old text in the same change.

## Before committing

- Run `scripts/validate.py` (or `scripts/package.sh`).
- If the change alters behavior (a rule, default, task list, or execute
  step), run the behavior tests (`/test-skill`, see `tests/README.md`) and
  add or update a scenario that covers it.
- A new component must appear in a playbook task table, and every component
  a task table names must exist — the validator checks this.
- A value is declared once, in the playbook's field table. Every name in a
  task table's `uses` column must be a declared field, every `needs` entry
  an earlier row, and the template's values block must hold every field two
  or more tasks use — the validator checks this too. Components never list
  the values they read; they point at `uses`.
- Keep each `plugin.json` description under 500 characters and a
  complete sentence; the SKILL.md front-matter description is what triggers
  the skill and must stay under 1024.
- Bump the changed plugin's `version` and add a CHANGELOG.md line.
- Do not put tokens or credentials in any file. The Eventbrite token lives in
  Drive; the skill only names where to read it.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `sdmctosh-arch/MassHire-Marketing`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

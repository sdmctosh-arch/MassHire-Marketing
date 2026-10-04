# MassHire Marketing — skills

Source of truth for the MassHire Central Career Centers Claude skill,
`masshire-projects`. It runs marketing projects (job fairs, recruitment and
hiring events, webinars, workshops, training promotions) from request to
finished deliverables, with one review gate. Email is part of it: the
`constant-contact-email` component holds the brand voice, base HTML, subject
lines, and compliance rules. The system drafts; it never sends or schedules.

## Layout

```
.claude-plugin/marketplace.json     lists the plugin for Claude Code
plugins/
  masshire-projects/
    .claude-plugin/plugin.json      name, version, description
    skills/masshire-projects/
      SKILL.md                      orchestration: the run, gates, preflight, storage, universal rules
      playbooks/                    one file per project type
      components/                   one file per task
      templates/                    project-file.md, the per-project state file
scripts/
  validate.py                       structural checks (run before every commit)
  package.sh                        validates, then builds dist/<plugin>-v<version>.zip
```

The zip from `package.sh` has the same layout as the original upload, so it
can be uploaded to claude.ai / Cowork as-is.

## Workflow

1. Branch, edit the markdown.
2. Bump `version` in that plugin's `.claude-plugin/plugin.json` (patch:
   wording fixes; minor: a new rule, component, or playbook; major: a change
   in how project files or stored templates are structured).
3. Add a line to `CHANGELOG.md`.
4. `scripts/package.sh` validates and builds the zip.
5. Open a PR. CI runs the same validation and attaches the zip as a build
   artifact.
6. After merge, upload the zip to replace the installed skill.

## Installing in Claude Code

```
/plugin marketplace add sdmctosh-arch/MassHire-Marketing
/plugin install masshire-projects@masshire-marketing
```

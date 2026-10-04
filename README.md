# MassHire Marketing — skills

Source of truth for the MassHire Central Career Centers Claude skill,
`masshire-projects`. It runs marketing projects (job fairs, recruitment and
hiring events, webinars, workshops, training promotions) from request to
finished deliverables, with one review gate. The copy every channel takes
from, and its voice, live in the `description-copy` component; the
`constant-contact-email` component holds the base HTML, subject lines, and
compliance rules. The system drafts; it never sends or schedules.

## Layout

```
.claude-plugin/marketplace.json     lists the plugin for Claude Code
plugins/
  masshire-projects/
    .claude-plugin/plugin.json      name, version, description
    skills/masshire-projects/
      SKILL.md                      orchestration: the run, gates, preflight, universal rules
      playbooks/                    one file per project type
      components/                   one file per task
      systems/                      one file per system shared by many tasks (the Drive project store)
      templates/                    project-file.md, the per-project state file
tests/
  scenarios/                        behavior tests: message, simulated world, assertions
.claude/skills/test-skill/          runs the behavior tests ("run the tests" or /test-skill)
.claude/skills/<other>/             engineering skills copied from mattpocock/skills (not part of the plugin)
docs/agents/                        issue tracker, triage labels, and domain-doc settings for those skills
docs/adr/                           architecture decisions; GLOSSARY.md at the root holds the domain terms
.github/workflows/validate.yml      CI: validate and build the zip on every PR
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
4. `scripts/package.sh` validates and builds the zip. If the change alters
   behavior, run the behavior tests too (see `tests/README.md`).
5. Open a PR. CI runs the same validation and attaches the zip as a build
   artifact.
6. After merge, upload the zip to replace the installed skill.

## Installing in Claude Code

```
/plugin marketplace add sdmctosh-arch/MassHire-Marketing
/plugin install masshire-projects@masshire-marketing
```

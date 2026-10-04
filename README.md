# MassHire Marketing — skills

Source of truth for the **masshire-projects** skill, which runs MassHire Central
Career Centers marketing projects (job fairs, recruitment and hiring events,
webinars, workshops, training promotions) from request to finished
deliverables with one review gate.

## Layout

```
.claude-plugin/
  plugin.json          plugin manifest (name, version, description)
  marketplace.json     lets Claude Code install the plugin from this repo
skills/masshire-projects/
  SKILL.md             orchestration: the run, gates, preflight, storage, universal rules
  playbooks/           one file per project type: fields, defaults, task list, execute list
  components/          one file per task: how it is done in a given system
  templates/           project-file.md, the per-project state file
scripts/
  validate.py          structural checks (run before every commit)
  package.sh           validates, then builds dist/masshire-projects-v<version>.zip
```

The zip from `package.sh` has the same layout as the original upload, so it
can be uploaded to claude.ai / Cowork as-is.

## Workflow

1. Branch, edit the markdown.
2. Bump `version` in `.claude-plugin/plugin.json` (patch: wording fixes;
   minor: new rule, component, or playbook; major: a change in how project
   files are structured).
3. Add a line to `CHANGELOG.md`.
4. `scripts/package.sh` — validates and builds the zip.
5. Open a PR. CI runs the same validation and attaches the zip as a build
   artifact.
6. After merge, upload `dist/masshire-projects-v<version>.zip` to replace the
   installed skill.

## Installing in Claude Code

```
/plugin marketplace add sdmctosh-arch/MassHire-Marketing
/plugin install masshire-projects@masshire-marketing
```

## Related

The skill depends on the separate `masshire-email` skill for the email
component; it is not in this repo.

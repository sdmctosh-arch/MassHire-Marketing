# Changelog

## Repo — 2026-10-04

- Behavior tests: six scenarios in `tests/scenarios/` and the `test-skill`
  project skill that plays each one with a fresh subagent and grades it with
  another. The validator checks scenario format. Plugin unchanged.

## masshire-projects 1.1.0 — 2026-10-04

- Merged the masshire-email skill into masshire-projects; the separate
  plugin is gone. Its rules now live in `components/constant-contact-email.md`,
  rewritten to the project model:
  - Removed send windows, resend spacing, the daily cap, SEND/RESEND dates in
    the build sheet, and the separate pre-build approval (the review packet
    is the approval).
  - Removed the browser fallback (a failed connector blocks the task) and
    the ask-about-audience stop (the operator attaches the list).
  - Email skeletons map to the playbook roles (announce, reminder, last
    call); correction emails are drafted only on request.
- SKILL.md: triggers on any MassHire email request; email requests route to
  their project; employer emails listed as not written yet; the base HTML
  is in the Drive storage tree.
- Training execute list gains the email destination check.

## masshire-email 1.0.0 — 2026-10-04

- Imported masshire-email v1.
- Fixed `plugin.json`: the description was truncated mid-sentence at 500
  characters; replaced with a complete one and added `version` and `author`.
- Repo restructured: each skill is now a plugin under `plugins/`.

## masshire-projects 1.0.0 — 2026-10-04

- Imported masshire-projects v1 (event and training-promotion playbooks,
  10 components, project-file template).
- Fixed `plugin.json`: the description was truncated mid-sentence at 500
  characters; replaced with a complete one and added `version` and `author`.

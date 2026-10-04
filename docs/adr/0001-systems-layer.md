---
status: accepted
---

# A fourth layer, `systems/`, for what is not one task

The skill had three layers: SKILL.md for universal rules, a playbook per
project type, a component per task. The rules for the Drive project store
(ids, write mechanics, checkpoints, staleness, index) fit none of them, so
they accumulated in SKILL.md and in the template body and were re-read on
every run. We added `systems/<system>.md`: how a system that is not one task
is used, shared by every task that touches it. A system file is named by
SKILL.md, a playbook, or a component, and the validator enforces that.

## Considered options

- Keep storage in SKILL.md (the status quo): a third of the universal file
  was Drive mechanics most steps never need.
- Make the store a component: a component is one task with a row in a task
  table; the store has no task, and the validator's task-table rule would
  have needed an exemption.

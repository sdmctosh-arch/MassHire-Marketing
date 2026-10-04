---
project:      YYYY-MM-DD-name
type:         event
event_kind:   job-fair
status:       intake
event_date:   YYYY-MM-DD
created:      YYYY-MM-DD
updated:      YYYY-MM-DD
values:
  event_name:
  event_date:
  start_time:
  end_time:
  venue:
  address:
  jobseeker_slug:
  jobseeker_link:
  jobseeker_short_link:
  employer_slug:
  employer_link:
  employer_short_link:
tasks:
  - id: existing-check
    status: todo
    needs: []
    uses: [event_date, event_name]
open_questions: []
---

# TASK SCHEMA

Every task carries these fields. Omit a field only where marked optional.

| Field | Holds |
|---|---|
| `id` | The task name from the playbook's task list. |
| `status` | todo, blocked, draft, approved, done, skipped, stale. |
| `needs` | Task ids that finish first. Conditional entries are resolved at intake; a task not in this file is never named here. |
| `uses` | Value names. A change to any of them marks this task stale. |
| `blocked_by` | Required when status is blocked: the missing fact or the failing check. |
| `output` | Optional. The file path, url, or external id this task produced. |

For a training project, the values block holds `training_link`, `path`, and
`public_link` instead of the event values.

# STATUS

What is waiting on whom, in three lines or fewer. During handoff: the
operator's remaining work as a numbered list.

# SOURCE REQUEST

The original request, unedited.

# FACTS

| Field | Value | Source |
|---|---|---|

Source is one of: request, default, derived, lookup, generated, written.
Facts one task uses go here; shared facts go in the values block.

# LOG

| Date | Event |
|---|---|

One line per completed task, per value change, one `Approved: review packet`
line, and one `Executed: <task> <action>` line per execute action.

# DECISIONS AND FAILURES

| # | Decision or failure | Kind | Rule |
|---|---|---|---|

Kind: project fact, project-type rule, tool fact, universal rule, or
constraint rule. At close, everything except project facts moves to its home
and is deleted here.

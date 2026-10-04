---
project:      YYYY-MM-DD-name
type:         event
event_kind:   job-fair
status:       intake
event_date:   YYYY-MM-DD
created:      YYYY-MM-DD
updated:      YYYY-MM-DD
values:
  copy:
  event_name:
  event_date:
  start_time:
  end_time:
  online_platform:
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

# STATUS

# SOURCE REQUEST

# FACTS

| Field | Value | Source |
|---|---|---|

# LOG

| Date | Event |
|---|---|

# DECISIONS AND FAILURES

| # | Decision or failure | Kind | Rule |
|---|---|---|---|

<!-- Schema, statuses, checkpoints, and staleness: systems/project-store.md.
     The values block holds every field two or more tasks list in `uses`.

| Type | Values block |
|---|---|
| event | The keys in the front matter above. |
| training | `copy`, `training_link`, `path`, `public_link` |
-->

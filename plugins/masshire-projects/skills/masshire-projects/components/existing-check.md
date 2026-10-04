# Component — existing-check

Access: read-only, in every live system the playbook creates in. Runs at
intake, after Preflight and before the project folder is created, so a date,
venue, or slug that disagrees with a live system is caught before anything
is made from it.

This is the one place the skill searches before it creates. A creating
component never searches on its own: it reads this task's record and either
updates the object recorded here or creates a new one where the record says
`none`. Two nearby events with similar names is exactly the case that
matters: a second object makes a second link and splits the registrations.

## Targets by playbook

| Playbook | Target | Search |
|---|---|---|
| event | Eventbrite event | `GET /organizations/<org_id>/events/?status=draft,live&order_by=start_desc` (org id from `eventbrite-event`); a similar name or the same date. |
| event | WordPress `event` post | The `wordpress` find by title, type `event` (drafts count); read the `date` field of any match. |
| event, job fairs | Zoho `Job_Fairs` record | Search on `Name` and on `Event_Date` (`zoho-job-fair` tool facts). |
| event | Redirect path(s) | For each slug the field table derives (`jobseeker_slug`, then `employer_slug`), the path check in `vanity-redirect`; a taken path moves to the next candidate by its slug rules. |
| training | WordPress `training` post | The `wordpress` find by title, type `training` (path B). |
| training | Directorist `at_biz_dir` listing | The `wordpress` find by title, type `at_biz_dir`. |

## Process

1. Search every target in the table for the chosen playbook.
2. For each match, compare date, start and end time, and venue (or title,
   for a training) with the request.
3. Record the result on this task, per target: `matched: <id>` or `none`;
   for redirects, the free slug and every rejected candidate.

## Result

- `none`: the creating component creates.
- A match that agrees with the request: the creating component updates that
  object instead of creating one, and builds only what it lacks.
- A match that disagrees: the live system is what exists. Use its value,
  record the conflict in FACTS, and list it first under Assumptions in the
  review packet, naming both values ("Assumed: 2026-11-20, the date already
  in Eventbrite; the request said 2026-11-19"). "Approve" accepts it;
  "approve, but use the 19th" overrides it, and the override updates the
  matched object at execute.
- A taken redirect path: the next candidate, automatically; the chosen slug
  and the rejected candidates go in the review packet. Never repoint an
  existing redirect without the operator saying so.

## Checks

- [script] Every target in the table for this playbook was searched; the
  result per target is recorded in the task.
- [script] No creating task in the file runs a search of its own.

# Component — existing-check

Access: read-only. Runs first, at intake, so a date or venue that disagrees
with a live system is caught before anything is drafted.

## Process

1. Eventbrite: list the organization's events
   (`GET /organizations/1772914159203/events/?status=draft,live&order_by=start_desc`)
   and look for one with a similar name or the same date.
2. WordPress (`novamira/execute-php`, `get_posts` with `post_status` any, so
   drafts count): search posts of type `event` for a similar title, and read
   the `date` field of any match.
3. Zoho (job fairs only): search `Job_Fairs` on name and on `Event_Date`.
4. For each match, compare date, start and end time, and venue with the
   request.

## Result

- No match: continue.
- A match that agrees with the request: record its id in the task; the
  component that would create that object uses it instead of creating a new
  one ("search before you create").
- A match that disagrees: the live system is what exists. Use its value,
  record the conflict in FACTS, and put it at the top of the review packet as
  an assumption to confirm.

## Checks

- [script] Each system was searched; the result per system is recorded in the
  task.

# Component — zoho-job-fair

Access: reads and writes Zoho CRM through the connectors. Creating the record
is Level 1 and runs in the draft pass: it notifies no one and lists nothing
publicly (tested). The link it produces goes public only when the redirect,
the WordPress event, or staff share it.

## Tool facts

- Module `Job_Fairs` (CustomModule8). Three writable fields only: `Name`,
  `Event_Date` (YYYY-MM-DD), and `Registration_Link`, which an automation
  fills on create. The module makes the link; it does not hold event details.
- The link is one shared Zoho form. The `jfid` query parameter carries the
  record id. Copy `Registration_Link` exactly. Never build or edit the link.
- Registrations land in `Job_Fair_Registrations`, linked by the `Job_Fair`
  lookup. This skill never reads them.

## Process

1. Search the module first, matching on name AND event date. Two nearby
   events with similar names is exactly the case that matters. A duplicate
   record makes a second link and splits the employer registrations.
2. If no record exists: create one with `Name` = `event_name` and
   `Event_Date` = `event_date`.
3. Read back `Registration_Link`. If it is still empty, recheck up to three
   times, a short wait apart. Still empty: leave `employer_link` empty, draft
   the other tasks, flag it in the review packet, and read it again at the
   start of the execute pass (the fill marks the WordPress event and the
   employer redirect stale; update both before publishing).
4. Record the link as the `employer_link` value. Confirm its `jfid` equals
   this record's id.

## Checks

- [script] Exactly one record for this event after the run.
- [script] The link's `jfid` matches the record id.

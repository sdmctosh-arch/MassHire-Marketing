# Component — eventbrite-event

Access: calls the Eventbrite API v3 directly (`eventbriteapi.com` is
allowlisted for network egress in this Cowork session). The draft is built in
the draft pass. Publication is Level 2: it runs in the execute pass, after
the review packet is approved.

## Inputs

From the values block: event_date, start_time, end_time, venue, address. From
the project file:
`event_kind`, the copy in `descriptions/<project>.html`, the scope
fields (time slots and slot range, walk-ins), the derived tag list,
capacity (default 2000), max tickets per order (default 10). An Eventbrite API
token, read from Google Drive (see step 1) — never write it into the project
file or any file in the workspace.

## Process

1. Read the Eventbrite API token from the Drive file `eventbrite-token.txt`
   (id `1Te4ym9f1Io-HFtQ53MzcWJpWZR35owha`, in the `masshire-projects` Drive
   folder under `MassHire Projects`) using `download_file_content`. Fall back
   to `search_files` for `title = 'eventbrite-token.txt'` if the id ever
   changes. If the file is missing or empty, stop the run and report it — don't guess or reuse an old value. Authenticate requests with
   `Authorization: Bearer <token>`.
2. Look up the organization ID (`GET /users/me/organizations/`; MassHire
   Central Career Centers is `1772914159203`). For an in-person event, check
   existing saved venues (`GET /organizations/<org_id>/venues/`) for one
   matching the values-block venue; create it
   (`POST /organizations/<org_id>/venues/`) only if not found. For an online
   event, set `online_event: true` and no venue.
3. Create the draft event (`POST /organizations/<org_id>/events/`) with
   `status: draft`, the values-block date/time, the matched venue ID, and
   the copy from `descriptions/<project>.html` as the HTML
   description.
4. Build the ticket classes and order-form questions from the settings
   stored below. Never invent a field value from general API knowledge.
   If a setting in this file is marked "not recorded", or the API refuses to
   create a question or a setting, use the fallback in "When the API cannot
   build it".
5. Set the order confirmation (see below).
6. Record the event id in the task, and the draft's public URL (the `url`
   field of the create response) as the `jobseeker_link` value. The URL does
   not change on publish (tested). Put the edit URL and the tag list in the
   review packet; the operator adds the tags to the draft before approving.

## Execute

1. Publish: `POST /events/<event_id>/publish/`.
2. Confirm `jobseeker_link` opens the live event page.
3. Read the tags back (see Tags). Missing tags are reported, not blocking.

## Ticket patterns

Common to every pattern:

- `hide_sale_dates` true on every ticket class, or the checkout looks faulty.
- Capacity 2000 per ticket class unless the project says otherwise.

**General registration** (the default). Reference: Milford Job Fair,
event `1999112756068`.

- `Registration`: sales start at creation, end at event start.
- `Admission` (walk-in, when walk-ins are in scope): sales start at event
  start, end at event end, `auto_hide` true.

**Time slots** (any event kind, only when the operator requests them).
Reference: Worcester Job Fair, event `2000642954934`.

- One labeled ticket class per slot, named `<time> Admission` in the form
  `10:00am Admission`, `10:30am Admission`. Default slot length 30 minutes.
- Slot tickets replace the `Registration` ticket. Each slot ticket's sales
  start at creation and end at event start, `auto_hide` true.
- Never use Eventbrite's built-in time slots (timed entry / series).
- The walk-in `Admission` ticket, when in scope, is the same as in general
  registration.

## Order-form questions

Six questions, a fixed set with fixed option lists. Create them with
`POST /events/<event_id>/questions/`. Never delete a question; scope it to a
ticket class. Only the Job Seeker ID question shows on the walk-in
`Admission` ticket. The questions scoped to `Registration` in the general
pattern are scoped to every slot ticket in the slot pattern. Question 6
measures the marketing channels; its options never change between events.

| # | Question text | Type | Required | Options | Ticket classes |
|---|---|---|---|---|---|
| 1 | not recorded | | | | Registration (slot tickets) |
| 2 | not recorded | | | | Registration (slot tickets) |
| 3 | not recorded | | | | Registration (slot tickets) |
| 4 | not recorded | | | | Registration (slot tickets) |
| 5 | Job Seeker ID (exact wording not recorded) | | | | Registration (slot tickets), Admission |
| 6 | How did you hear... (exact wording and options not recorded) | | | | Registration (slot tickets) |

While a row reads "not recorded", copy that question from the reference
event (`GET /events/<ref_event_id>/questions/`). Show the exact text, type,
required flag, and options in the review packet under "Order-form questions
(copied from the reference event)", as information the operator can store
in this table. It is not a question and asks for no reply.

## When the API cannot build it

If the API refuses a ticket setting or a question, copy the reference event
for the pattern (`POST /events/<ref_event_id>/copy/`) instead of building
from scratch. The copy carries the ticket classes, the questions, and their
scoping. Then update the copy to this project: name, dates and times,
venue, description, each ticket class's sales window, and status `draft`.
Run every check below on the copy; a copy that keeps the reference event's
dates or name is a failed check. Record in the task that the event was
copied, and from which reference event.

## Order confirmation

Set both fields to exactly this text, on every event:

> Thanks for registering! Don't forget to keep your ticket handy, either in the Eventbrite app or print it out and bring it with you!

`POST /events/<event_id>/ticket_buyer_settings/` with body

```json
{"ticket_buyer_settings": {
  "confirmation_message": {"html": "<the text>"},
  "instructions": {"html": "<the text>"}
}}
```

Eventbrite fills the `text` form from `html`. Verified on a draft event,
2026-09-11. Older events carry an extra job-fair-prep line in
`instructions`; do not copy it.

## Tags

Default tags by kind:

| Kind | Default tags |
|---|---|
| Job fair, recruitment, hiring | `employment`, `jobs`, `jobfair`, `hiring` |
| Webinar | `employment`, `careers`, `webinar`, `online` |
| Workshop | `employment`, `careers`, `workshop`, `jobseekers` |

Eventbrite allows 10 tags. Add up to 6 more for this event from its topic,
sectors, and town (for example `resume`, `manufacturing`, `southbridge`),
skipping any that repeat a default. The tag list goes in the review packet.

- [constraint: no API write] The public API v3 has no endpoint that writes
  tags (`event.tags` is rejected; `/events/<id>/tags/` does not exist —
  tested 2026-09-11). The operator adds the tags to the draft in the
  Eventbrite UI before approving the review packet. Review this rule if Eventbrite adds a write endpoint.
- Read back at execute:
  `GET /destination/events/?event_ids=<event_id>&expand=tags`. The tags are
  the entries with `prefix` `OrganizerTag`. The destination endpoint does not
  return drafts, so this runs after publishing.

## Checks

- [api] The ticket classes match the chosen pattern with the correct sales
  windows — confirm by reading them back
  (`GET /events/<event_id>/ticket_classes/`), not just from the create
  response.
- [api] Six questions present; only the Job Seeker ID question on the walk-in
  `Admission` ticket.
- [api] `confirmation_message` and `instructions` both equal the standard
  text (`GET /events/<event_id>/ticket_buyer_settings/`).
- [api] Date, time, and venue (or `online_event`) match the values block.
- [api] After publish: the `OrganizerTag` entries match the tag list.
- [judgement] The description matches the copy in `descriptions/` and makes no promise
  a third party controls.

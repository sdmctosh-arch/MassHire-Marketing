# Component — eventbrite-event

Access: calls the Eventbrite API v3 directly (`eventbriteapi.com` is
allowlisted for network egress in this Cowork session). The draft is built in
the draft pass. Publication is Level 2: it runs in the execute pass, after
the review packet is approved.

## Inputs

The values this task lists in `uses` (the playbook task table). From the
project file: `event_kind`, the copy in `descriptions/<project>.html`, the
scope fields (time slots and slot range, walk-ins), the derived tag list,
capacity (default under Ticket patterns), max tickets per order (default 10).
An Eventbrite API token, read from Google Drive (see step 1) — never write it
into the project file or any file in the workspace.

## Process

1. Read the Eventbrite API token from the Drive file `eventbrite-token.txt`
   (id `1Te4ym9f1Io-HFtQ53MzcWJpWZR35owha`, in the `masshire-projects` Drive
   folder under `MassHire Projects`) using `download_file_content`. Fall back
   to `search_files` for `title = 'eventbrite-token.txt'` if the id ever
   changes. If the file is missing or empty, don't guess or reuse an old value
   (Preflight stops the run). Preflight reads it once per session; every
   later call reuses that value and never reads the file again.
   Authenticate requests with `Authorization: Bearer <token>`.
2. Look up the organization ID (`GET /users/me/organizations/`; MassHire
   Central Career Centers is `1772914159203`). For an in-person event, check
   existing saved venues (`GET /organizations/<org_id>/venues/`) for one
   matching the values-block venue; create it
   (`POST /organizations/<org_id>/venues/`) only if not found. For an online
   event, set `online_event: true` and no venue.
3. If existing-check recorded a matching Eventbrite event, use that event:
   update it (`POST /events/<event_id>/`) with the values below instead of
   creating one, and build only the ticket classes and questions it lacks.
   Otherwise create the draft event (`POST /organizations/<org_id>/events/`) with
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
   review packet.

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

Seven questions, a fixed set. Every question except question 7 is required.
Every question is shown on the `Registration` ticket (in the slot pattern,
on every slot ticket). The walk-in `Admission` ticket gets none. Never delete
a question. Question 6 measures the marketing channels; its options never
change between events.

| # | Question text | Type | Options |
|---|---|---|---|
| 1 | Cell phone | Eventbrite's built-in contact field, not a custom question: turn it on and make it required | — |
| 2 | What city or town do you live in? | Short text | — |
| 3 | Have you served in the military? | Single choice | Yes; No |
| 4 | Are you looking for full-time or part-time work? | Single choice | Full time; Part time; Either |
| 5 | What industries or fields of work are you interested in? | Multiple choice (check all that apply) | Not recorded yet: copy from the reference event |
| 6 | How did you hear about this event? | Not recorded yet: copy from the reference event | Not recorded yet: copy from the reference event |
| 7 | MassHire Job Seeker ID number | Short text, optional | — |

Create questions 2–7 with `POST /events/<event_id>/questions/`. Set
question 1 the way the reference event has it: read the reference event's
built-in fields (`GET /events/<ref_event_id>/canned_questions/`) and match
it.

Where a cell reads "not recorded yet", copy it from the reference event
(`GET /events/<ref_event_id>/questions/`), keeping the options and their
order exactly. Show what was copied in the review packet under "Order-form
details copied from the reference event", as information the operator can
store in this table. It is not a question and asks for no reply.

## When the API cannot build it

If the API refuses a ticket setting or a question, copy the reference event
for the pattern (`POST /events/<ref_event_id>/copy/`) instead of building
from scratch. The copy carries the ticket classes, the questions, and their
scoping. Then update the copy to this project: name, dates and times,
venue, description, each ticket class's sales window, and status `draft`.
Then bring its tickets and questions in line with this file: delete any
ticket class this event's pattern does not have (the walk-in `Admission`
ticket when walk-ins are out of scope or the event is online); scope
questions 2–7 to `Registration` (or every slot ticket) and off `Admission`;
make 2–6 required and 7 optional.
Run every check below on the copy; a copy that keeps the reference event's
dates or name is a failed check. Record in the task that the event was
copied, and from which reference event.

If this run created a draft event before the refusal, delete that draft
(`DELETE /events/<event_id>/`) once the copy passes its checks, so only one
draft remains, and record its id as deleted in the task. Never delete an
event this run did not create, such as one existing-check matched.

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
  tested 2026-09-11); they are added in the Eventbrite UI. Review this rule
  if Eventbrite adds a write endpoint.
- Read back at execute:
  `GET /destination/events/?event_ids=<event_id>&expand=tags`. The tags are
  the entries with `prefix` `OrganizerTag`. The destination endpoint does not
  return drafts, so this runs after publishing.

## Checks

- [api] The ticket classes match the chosen pattern with the correct sales
  windows — confirm by reading them back
  (`GET /events/<event_id>/ticket_classes/`), not just from the create
  response.
- [api] Questions 2–7 present on `Registration` (or every slot ticket) and
  not on `Admission`; 2–6 required and 7 optional; the cell phone field is
  on, required, and scoped like questions 2–7 (read back from
  `GET /events/<event_id>/canned_questions/`); the options of questions
  3–6 match this file or the reference event exactly.
- [api] `confirmation_message` and `instructions` both equal the standard
  text (`GET /events/<event_id>/ticket_buyer_settings/`).
- [api] Date, time, and venue (or `online_event`) match the values block.
- [api] After publish: the `OrganizerTag` entries match the tag list.
- [script] The description contains no `awaiting your answer`.
- [judgement] The description matches the copy in `descriptions/`.

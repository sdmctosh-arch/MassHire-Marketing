# Playbook — Event

Any event MassHire hosts or co-hosts where jobseekers register on Eventbrite:
job fairs, recruitment events, hiring events, webinars, workshops. The event
kind (`event_kind` in the project file header) sets the defaults below.

## Fields

Source key: **Required** (request; the only kind that may produce a
question), **Request** (from the request, else the fallback shown),
**Default**, **Derived**, **Lookup**, **Generated**, **Written**.

### Facts

| Field | Source and rule |
|---|---|
| `event_kind` | **Derived** from the request wording: "job fair" → job-fair; one employer hiring → recruitment (or hiring, if the request says hiring event); "webinar" → webinar; "workshop" → workshop. None matches: the closest kind, stated as an assumption. |
| `event_date` | **Required**. |
| `start_time` | **Required**. |
| `end_time` | **Required**. No default duration. |
| `format` | **Request** (in person or online: "online", "virtual", "Zoom", "Teams" mean online). Request silent: the kind default below. |
| `venue` | **Required** when in person. |
| `address` | **Lookup**: match `venue` against Eventbrite saved venues; else **Request**; else **Required**. |
| `online_platform` | **Request**; else **Default** "Link sent after registration". Online events only. |
| `audience` | **Default** "Open to all jobseekers"; **Request** overrides. |
| `cost` | **Default** free. |
| `cohost` | **Request** only; no default; omitted if not given. |
| `venue_rules` | **Request** only (parking, ID, entrance); omitted if not given. |
| `what_to_bring` | Job fair and recruitment/hiring: **Default** "Bring several copies of your resume and dress as you would for an interview." Webinar and workshop: **Written** from the topic. |
| `hiring_employer` | **Required** for recruitment and hiring events. |
| `job_name` | **Derived** from the positions in the request: the category of work, not a single job title. |
| `positions` | **Request**, up to 3 (title, location, pay). Never asked. |
| `sectors` | **Request**; else **Default** "employers from many industries". |
| `partner_logo` | **Lookup** in Canva assets by company name; not found: the frame stays empty and is flagged in the review packet. |

### Scope

| Field | Source and rule |
|---|---|
| `time_slots` | **Default** no; **Request** turns them on. |
| `slot_length` | **Default** 30 minutes. |
| `slot_range` | **Default** first slot at `start_time`, last slot 30 minutes before `end_time`. |
| `walk_ins` | **Default** yes (the `Registration` + `Admission` two-ticket structure); no for online events. |
| `employer_registration` | **Default** by kind: job fairs only. |
| `flyer` | **Default** yes for every kind that has a template (table below). |
| `social` | **Default** yes. |

### Names and links

| Field | Source and rule |
|---|---|
| `event_name` | **Derived**. Recruitment/hiring: `Event Type: Company (Job Name)`, e.g. `Recruitment Event: NFI Industries (Truck Drivers)`. Job fair: the name in the request, else `<Town> Job Fair`. Webinar/workshop: the request's title. |
| project slug | **Derived**: `YYYY-MM-DD-kebab-event-name`. |
| `jobseeker_slug` | **Derived** by the slug rules in `vanity-redirect`. Taken: the next candidate, automatically. |
| `employer_slug` | **Derived**: `jobseeker_slug` + `employer`. |
| `jobseeker_link` | **Generated** when the Eventbrite draft is created (the draft's public URL; it does not change on publish). |
| `jobseeker_short_link` | **Derived**: `https://masshirecentralcc.com/<jobseeker_slug>`. The redirect is created at execute. |
| `employer_link` | **Generated** by the Zoho automation in the draft pass. |
| `employer_short_link` | **Derived**: `https://masshirecentralcc.com/<employer_slug>`. |
| Tags | **Derived**: 4 fixed + 2-3 from kind, sector, town. See `eventbrite-event`. |
| Campaign names | **Derived**: `<Event Name> - YYYY-MM-DD - Email <n>` / `- Facebook <n>`. |
| Flyer design name | **Derived**: `<Event Name> Flyer - YYYY-MM-DD`. |

## Defaults by kind

| Setting | Job fair | Recruitment / hiring | Webinar | Workshop |
|---|---|---|---|---|
| Default `format` | In person | In person | Online | In person |
| Employer registration (Zoho) | Yes | No | No | No |
| Vanity redirects | 2: jobseeker, employer | 1: jobseeker | 1: jobseeker | 1: jobseeker |
| Email drafts | 3: announce, reminder, last call | 2: announce, last call | 2: announce, last call | 2: announce, last call |
| Social post drafts | 1 | 1 | 1 | 1 |
| Flyer template | MH Event - Job Fair | MH Event - Job Listings | None: no flyer | None: no flyer |
| WordPress `event-category` | Job Fair (684); add Employer Registration (1016) when employer registration is in scope | Recruitment Event (973) | Online: Virtual Workshop (688) | Online: Virtual Workshop (688). In person: Worcester (685), Southbridge (1009). Elsewhere: flagged in the review packet. |

Email and social counts are fixed. They set how many drafts are created and
nothing else: no draft carries a date, time, or resend setting.

## Task list

| # | Task | Component | needs | uses |
|---|---|---|---|---|
| 1 | existing-check | `existing-check` | — | event_date, event_name |
| 2 | description-copy | Copy rules in SKILL.md | 1 | all facts |
| 3 | eventbrite | `eventbrite-event` | 2 | event_date, start_time, end_time, venue, address |
| 4 | zoho-job-fair (if employer registration) | `zoho-job-fair` | 1 | event_name, event_date |
| 5 | short-links | `vanity-redirect` | 3; 4 if in scope | jobseeker_link, employer_link |
| 6 | flyer-qr (if flyer) | `flyer-from-template`, QR section | 5 | jobseeker_short_link |
| 7 | flyer (if flyer) | `flyer-from-template` | 2, 6 | event_date, start_time, end_time, venue, address, jobseeker_short_link |
| 8 | flyer-export (if flyer) | `flyer-from-template`, export section | 7 | — |
| 9 | wordpress-event | `wordpress-event` | 3; 4 if in scope; 8 if flyer | event_date, start_time, end_time, venue, address, jobseeker_link, employer_link |
| 10 | jobseeker-emails | `constant-contact-email` | 2, 3 | event_date, start_time, end_time, venue, jobseeker_link |
| 11 | facebook-posts | `facebook-post-draft` | 2, 5; 8 if flyer | event_date, start_time, venue, jobseeker_short_link |
| 12 | review-packet | SKILL.md | all above | — |
| 13 | execute | Execute list below | 12 approved | — |

Leave out-of-scope tasks out of the project file. Do not add them as
`skipped`.

## Execute list

In this order, after the review packet is approved:

1. Publish the Eventbrite event. Confirm `jobseeker_link` opens the live
   page. Read back the tags the operator added; report any missing (see
   `eventbrite-event`, Tags). Do not block on it.
2. Create the redirect(s). Confirm each short link resolves to its
   destination.
3. Publish the WordPress event.
4. Confirm every email draft's REGISTER buttons point at the live
   `jobseeker_link` (the destination check in `constant-contact-email`).
5. Report, and write the handoff list to STATUS.

## Rules for this project type

- **Time slots on request, for any kind.** The default is general
  registration. When slots are on, follow the slot pattern in
  `eventbrite-event`.
- **Announce without the employer list.** The system never reads or waits for
  the employer registrations. Job fair emails and the flyer name sectors, not
  employers. Recruitment and hiring events name `hiring_employer`.
- **Short links on print and social, full links elsewhere.** The flyer and
  the social posts carry the short link only. The emails and the website
  event page keep the full links: a click there costs nothing, and a full
  link survives a deleted redirect.

## Operator actions

Before approving the review packet:

- Add the tags to the Eventbrite draft (the API cannot write them).

After the execute pass (the handoff list in STATUS):

- In Constant Contact: attach the "Email List" segment to each email draft,
  set any resend, and schedule each one.
- In Constant Contact: schedule the social draft.
- Print the flyer from the PDF, if needed.
- Fix the font on any flyer text the connector added (it cannot set fonts).

# Changelog

## masshire-projects 1.7.0 — 2026-10-04

The project store gets its own file; a fourth layer, `systems/`.

- New `systems/project-store.md` (ADR-0001): where state lives, `index.md`,
  Drive tool loading, opening and creating a project, writing and renaming
  files, the project-file schema (header, values, tasks, statuses, body
  sections), checkpoints, values and staleness, and the repair of old
  project files. Every sentence of it left SKILL.md or the template.
- SKILL.md keeps the run; a six-line "Project state" section points at the
  store. Starting and resuming a project open the store in one step.
- The template is a skeleton again: front matter and empty sections. The
  schema prose, the second status list, and the time-format rule are in
  the store. Every project file created from it is shorter.
- Repo: CLAUDE.md and README list the fourth layer; the validator requires
  every `systems/*.md` to be named by SKILL.md, a playbook, or a
  component. `GLOSSARY.md` is in the prescribed format and gains "project
  store" and "system". Behavior is unchanged; no scenario changes.

## masshire-projects 1.6.0 — 2026-10-04

The field contract is declared once and checked.

- `copy` is declared in both playbooks' field tables (**Generated** by
  `description-copy`).
- The template states the values-block rule (every field two or more tasks
  use) and lists the training values in a table the validator reads.
- Component Inputs sections no longer repeat the value names; they point
  at the task's `uses`.
- `validate.py` checks the contract: every `uses` name is a field the same
  playbook declares, every `needs` entry is an earlier row, the template's
  values block holds every shared field and nothing undeclared, for both
  types. A renamed or missing value is now a validation error instead of a
  silent staleness hole.

## masshire-projects 1.5.0 — 2026-10-04

The copy gets its own component.

- New `components/description-copy.md`: the copy's six parts (`headline`,
  `summary`, `details`, `audience`, `bring`, `body`, each a `data-part`
  block), the content by kind, the voice, the gap marker and its redraft,
  the subagent handoff, and the copy checks. Both task tables name it.
- Voice rules leave `constant-contact-email`; its "Details by project type"
  table and the per-kind body column go. Each channel now names the part it
  takes: email `{{BODY}}`, flyer `body`, the WordPress content line, and the
  social text take `summary`; the details box is `details` then `audience`;
  `{{CTA_LINE}}` is `bring`; the training post is every part but
  `headline`; the listing excerpt is `summary` plus `body`.
- "No promise a third party controls" lives only in `description-copy`;
  the Eventbrite, flyer, and email checks become "matches the copy", and
  every publishing component checks for `awaiting your answer`.
- `copy` is a value: `description-copy` fills it with the file's Drive id,
  and every taker lists `copy` in `uses`, so a redraft marks them stale.
  The playbooks' sectors rule and "eligibility is public" move into the
  content-by-kind table; the template's values block gains `copy`.
- Repo: `GLOSSARY.md` created with copy, part, and gap marker. Tests:
  `job-fair-complete` asserts the parts and who takes which;
  `missing-required-fact` asserts the exact marker and the `copy` uses.

## masshire-projects 1.4.1 — 2026-10-04

Fixes from the whole-repo standards review. Each rule now lives in one layer.

- Frozen-draft stop: only in `constant-contact-email`.
- "Updated as employers confirm": the event playbook's copy rule; the email
  details box stays in `constant-contact-email`; the flyer takes its body
  from the copy.
- Campaign name formats: only in the email and Facebook components.
- Eventbrite token missing: the run-stop rule is only in Preflight.
- Operator adds the Eventbrite tags: the playbook's operator actions; the
  component keeps the API fact.
- WordPress category ids move from the event playbook to `wordpress-event`;
  training post type, Directorist type and example ids leave the training
  playbook.
- Redirect count and which kinds get a flyer: only in the playbooks.
- A preflight failure goes at the top of the review packet, not under item 9.
- existing-check takes the Eventbrite org id from `eventbrite-event`.
- Repo: README layout lists the copied skills, `docs/agents/` and CI;
  `mp-code-review` display name updated after the rename.

## masshire-projects 1.4.0 — 2026-10-04

Fixes from the whole-repo spec review.

- An existing-check conflict is an assumption, listed first under
  Assumptions with both values: "approve" accepts the live value, "approve,
  but …" overrides it. It no longer blocks publishing.
- existing-check runs at intake, before the project folder is created, so
  the slug and folder use the live value. The Eventbrite and WordPress
  components update a matched object instead of creating a second one.
- The copy-the-reference fallback also deletes ticket classes the pattern
  lacks (the walk-in ticket for online events), scopes questions 2–7 to
  Registration, and makes question 7 optional. A draft the run created
  before the refusal is deleted once the copy passes its checks.
- `wordpress-event` is created as soon as its needs are done; the draft
  pass is not reordered to run the flyer first.
- `create_email_campaign` is called with the campaign `name`.
- The Facebook profile id no longer points to an `index.md` section that
  does not exist.
- Repo: `validate.py` fails on a component no playbook task table names.
  Tests: new `eventbrite-copy-fallback` scenario; assertions for the
  exact-path slug check, the project-file checkpoints, the `index.md` row,
  copied questions shown as information, the campaign name, the conflict as
  an assumption, and unaffected actions running past a major block.

## masshire-projects 1.3.4 — 2026-10-04

- Order-form question 7: MassHire Job Seeker ID number, short text,
  optional, on Registration only.

## masshire-projects 1.3.3 — 2026-10-04

- Eventbrite order-form questions stored: cell phone (built-in), city or
  town, military service, full-time or part-time, industries, how they
  heard. All required, on Registration only; the walk-in Admission ticket
  gets none (the Job Seeker ID question is gone). The industry options and
  the "how did you hear" type and options are still copied from the
  reference event until recorded.

## masshire-projects 1.3.2 — 2026-10-04

- Order-form questions copied from the reference event are shown in the
  review packet as information, not as a request to confirm.

## masshire-projects 1.3.1 — 2026-10-04

- Choices the operator might change are written as assumptions, never as
  "tell me if…" requests; the only review-packet questions are for missing
  Required facts.
- Test wording: missing-required-fact assertion 4 exempts description-copy.

## masshire-projects 1.3.0 — 2026-10-04

Fixes from the second behavior-test run.

- A missing Required fact no longer stops the copy: description-copy is
  drafted with a marked gap (`[end time — awaiting your answer]`), and a gap
  in a published item or email draft fails its checks.
- `index.md` columns defined: slug, type, event_date, status, folder_id,
  notes; status mirrors the project file.
- Constant Contact tool names match the connector (`create_email_campaign`,
  `update_email_campaign_activity`, `rename_email_campaign`,
  `get_physical_address`, `retrieve_email_addresses`, `create_social_post`,
  `update_social_post`).
- `project.md` is written at four checkpoints (intake, end of draft pass,
  each execute action, handoff) instead of after every task.
- Training listings: no location term when no source gives one.
- Eventbrite default tags by kind; webinars and workshops no longer get
  `jobfair` and `hiring`.
- short-links (slug choice) needs only existing-check; unused Job Listings
  position rows are sent empty and checked; the WordPress existing-check
  names its tool; times are stored as 24-hour HH:MM, America/New_York;
  `online_platform` is in the values block.
- Tests: missing-required-fact and training-path-b cover the new rules.

## masshire-projects 1.2.0 — 2026-10-04

Fixes from the first behavior-test run.

- Approve publishes unless something major is missing (a Required fact, an
  unconfirmed existing-check conflict, an item that failed its own checks,
  or a link to nothing). Only the affected actions are skipped; the rest
  run, and blocked drafts go in the handoff.
- Eventbrite order-form questions get a stored table in `eventbrite-event`
  (to be filled; until then they are copied from the reference event). If
  the API refuses a setting, the reference event is copied and updated.
  Questions endpoint corrected to `/questions/`.
- The flyer QR encodes the Eventbrite link; the printed address stays the
  short link. flyer-qr no longer waits on short-links.
- The WordPress event no longer waits on the flyer; the flyer is added when
  it exists, or listed in the handoff. Facebook posts are text-only.
- Job fair emails and flyer say the registration page will be updated as
  employers confirm.
- Eventbrite tags: up to 10 (4 defaults + up to 6).
- Short-link availability check matches the exact path, not any slug that
  contains it.
- Tests: job-fair-complete covers the new rules; new scenarios
  approve-with-minor-block and approve-with-major-block.

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

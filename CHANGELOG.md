# Changelog

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

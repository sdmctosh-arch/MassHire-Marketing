# Scenario — approve-with-schedule

The operator approves and asks the system to schedule. The system never
schedules: it must run the execute pass and leave scheduling to the operator.

## Message

> approve the Grafton job fair. Also go ahead and schedule email 1 for
> Tuesday at 10am and set the resend to non-openers for Friday.

## World

- Drive `index.md` has the row `2026-11-05-grafton-job-fair`, status
  `review`, with its folder id. All writes succeed.
- Its `project.md`: type event, event_kind job-fair, status review.
  Values: event_name "Grafton Job Fair", event_date 2026-11-05, 10:00–13:00,
  venue "Grafton Public Library", jobseeker_slug `graftonfair`,
  employer_slug `graftonfairemployer`, jobseeker_link
  https://www.eventbrite.com/e/grafton-job-fair-tickets-111, employer_link
  set. Tasks existing-check, description-copy, zoho-job-fair, flyer-qr,
  flyer, flyer-export, wordpress-event, jobseeker-emails (3 drafts),
  facebook-posts are `draft` or `done`; short-links is `draft` (slugs
  checked); eventbrite is `draft`; review-packet is done.
- Preflight: every connector check passes.
- Eventbrite publish succeeds and the live page opens. The operator added
  the tags.
- Redirect creation succeeds and both short links resolve.
- WordPress publish succeeds.
- All three email drafts' REGISTER buttons point at the jobseeker_link.

## Assertions

1. The execute pass runs in the playbook order: Eventbrite publish, then
   redirects, then WordPress publish, then the email destination check, then
   the report.
2. No email is scheduled: no send date or time is set, no resend is set, and
   no scheduling tool (including `check_campaign_schedule_readiness`) is
   called.
3. The reply tells the operator plainly that the system does not schedule or
   set resends, without asking a separate question or stopping the execute
   pass.
4. The handoff list tells the operator to schedule email 1 and set its
   resend in Constant Contact (their requested Tuesday 10am / Friday may be
   echoed as their plan, but the system sets neither).
5. The LOG gets one `Approved: review packet` line and one `Executed: …` line
   per execute action.
6. No second review packet is shown (the requested change alters nothing
   the operator has not seen).
7. No message is written to anyone other than the operator.
8. At handoff, the flyer, email, and social tasks are `done`, the
   review-packet and execute tasks are `done`, and the project status is
   `handoff`.

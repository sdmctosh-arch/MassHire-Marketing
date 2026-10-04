# Scenario — approve-with-minor-block

The operator approves while the flyer is blocked. A blocked flyer is not
major, so execute publishes everything else.

## Message

> approve the Grafton job fair

## World

- Drive `index.md` has the row `2026-11-05-grafton-job-fair`, status
  `review`, with its folder id. All writes succeed.
- Its `project.md`: type event, event_kind job-fair, status review.
  Values: event_name "Grafton Job Fair", event_date 2026-11-05, 10:00–13:00,
  venue "Grafton Public Library", jobseeker_slug `graftonfair`,
  employer_slug `graftonfairemployer`, jobseeker_link
  https://www.eventbrite.com/e/grafton-job-fair-tickets-111, employer_link
  set. Tasks: existing-check, description-copy and zoho-job-fair `done`;
  eventbrite, short-links, wordpress-event (created without the flyer),
  jobseeker-emails (3 drafts) and facebook-posts `draft`, all checks passed;
  flyer-qr done; flyer and flyer-export `blocked`, blocked_by
  "Canva preflight" (canva.com upload refused); review-packet done.
- Preflight: every connector check passes except Canva, which still fails.
- Eventbrite publish succeeds and the live page opens. The operator added
  the tags.
- Redirect creation succeeds and both short links resolve.
- WordPress publish succeeds.
- All three email drafts' REGISTER buttons point at the jobseeker_link.

## Assertions

1. The execute pass runs: the Eventbrite event is published, both redirects
   are created, and the WordPress event is published.
2. The blocked flyer does not stop or delay execute, and no question is
   asked before publishing.
3. The WordPress event is published without the flyer, and the handoff list
   says to add the flyer to the website event once it exists.
4. The report names the flyer as blocked (Canva) and still unfinished.
5. The email destination check runs and passes.
6. No send date, send time, resend date, post date, or `SCHEDULED` status is
   set anywhere, and no scheduling tool is called.

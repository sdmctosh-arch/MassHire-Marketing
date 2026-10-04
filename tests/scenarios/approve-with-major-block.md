# Scenario — approve-with-major-block

The operator approves while the Eventbrite draft has failed its own checks.
That is major: the event must not be published broken, and what depends on
it waits.

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
  https://forms.zohopublic.com/masshire/form/EmployerRegistration?jfid=555.
  Zoho record id 555. Tasks: existing-check, description-copy, zoho-job-fair,
  flyer-qr, flyer, flyer-export `done`; short-links, wordpress-event,
  jobseeker-emails (3 drafts), facebook-posts `draft`, checks passed;
  eventbrite `draft` but its check failed: the order-form questions were
  refused by the API and the copy fallback also failed, so the draft has no
  questions. The review packet reported this; review-packet done.
- Preflight: every connector check passes.
- Re-reading the Eventbrite draft confirms it still has no questions.
- Every other call succeeds.

## Assertions

1. The Eventbrite event is not published.
2. The jobseeker redirect (`graftonfair`) is not created, because its
   destination is the unpublished Eventbrite event.
3. The WordPress event is not published, because its registration link
   would lead to an unpublished event.
4. The report names each skipped action and the reason (the Eventbrite
   draft is missing its order-form questions).
5. The run does not invent or hand-write the missing questions.
6. The employer redirect `graftonfairemployer` is still created and confirmed
   to resolve to the Zoho form, because it does not depend on the Eventbrite
   event.
7. No send date, send time, resend date, post date, or `SCHEDULED` status is
   set anywhere, and no scheduling tool is called.

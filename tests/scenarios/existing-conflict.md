# Scenario — existing-conflict

The request's date disagrees with an event that already exists in
Eventbrite. The live system wins, and the conflict is surfaced.

## Message

> New job fair: Worcester Fall Job Fair, November 19, 2026, 10am–2pm at the
> DCU Center.

## World

- Drive: `index.md` exists and has no row for this event. All writes succeed.
- Preflight: every connector check passes.
- Eventbrite events: a draft "Worcester Fall Job Fair", id 9001, on
  2026-11-20, 10:00–14:00, venue DCU Center.
- Eventbrite saved venues: "DCU Center", 50 Foster Street, Worcester, MA
  01608.
- WordPress: no matching event post.
- Zoho `Job_Fairs`: no matching record.
- Redirection: `worcesterfair` is free.
- Every create call returns success with a new id.

## Assertions

1. existing-check finds Eventbrite event 9001 and records the date conflict
   (request 2026-11-19, live 2026-11-20) in FACTS.
2. The live value, 2026-11-20, is used as `event_date`, and the project slug
   uses it: `2026-11-20-worcester-fall-job-fair`.
3. The conflict is at the top of the review packet as an assumption to
   confirm, not silently resolved.
4. No second Eventbrite event is created; event 9001 is used.
5. No send date, send time, resend date, post date, or `SCHEDULED` status is
   set or planned anywhere.

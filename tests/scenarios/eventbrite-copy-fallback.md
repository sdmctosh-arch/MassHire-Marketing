# Scenario — eventbrite-copy-fallback

The Eventbrite API refuses the order-form questions, so the event is built
by copying the reference event. The copy carries the reference event's walk-in
ticket and its question scoping, which this online event must not keep.

## Message

> New webinar: Resume Basics, Tuesday December 8, 2026, 1pm to 2pm, on Zoom.

## World

- Drive: `index.md` exists and has no row for this event. All writes succeed.
- Preflight: every connector check passes.
- Eventbrite events: none with a similar name or the date 2026-12-08.
- WordPress: no matching event post.
- Redirection: `resumebasics` is free.
- Canva: both brand templates are found.
- Eventbrite: creating the event succeeds (id 7001), but every
  `POST /events/7001/questions/` call is refused with an error.
- Eventbrite: `POST /events/1999112756068/copy/` succeeds and returns event
  7002. The copy has a `Registration` ticket and a walk-in `Admission`
  ticket. Questions 2–6 are on `Registration`; question 7 (MassHire Job
  Seeker ID number) is required and on both `Registration` and `Admission`.
- Every other call succeeds.

## Assertions

1. The event is built by copying reference event 1999112756068, and the task
   records that it was copied and from which event.
2. The copy is updated to this project: name "Resume Basics", date
   2026-12-08, 13:00–14:00, online with no venue, status `draft`.
3. The walk-in `Admission` ticket is deleted from the copy, because the
   event is online.
4. Questions 2–7 are on `Registration` only, 2–6 required and 7 optional.
5. The Eventbrite task's checks are run on the copy and pass; the copy is not
   reported as a major block.
6. No question is asked in the review packet.
7. The unused draft 7001 is deleted after the copy passes its checks, and
   the task records it as deleted; only event 7002 remains.
8. No send date, send time, resend date, post date, or `SCHEDULED` status is
   set or planned anywhere.

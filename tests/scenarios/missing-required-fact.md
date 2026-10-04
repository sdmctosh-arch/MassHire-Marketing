# Scenario — missing-required-fact

A webinar request with no end time. `end_time` is Required and has no
default, so the run must ask exactly one question and keep going.

## Message

> Can we promote a webinar? "Resume Tips for Career Changers", Tuesday
> November 17, 2026 at 2pm, on Zoom.

## World

- Drive: `index.md` exists and has no row for this event. All writes succeed.
- Preflight: every connector check passes.
- Eventbrite events: none matching.
- WordPress: no matching event post.
- Redirection: `resumetips` is free.
- Every create call returns success with a new id.

## Assertions

1. `event_kind` is webinar and `format` is online; `online_platform` is Zoom.
2. The review packet opens with exactly one question, and it asks for the end
   time. No other question appears.
3. No end time or duration is invented or defaulted anywhere (no "3pm", no
   "one hour").
4. Every task that uses `end_time` is marked `blocked` with
   `blocked_by: end_time` (or equivalent naming the end time).
5. The run does not stop at the missing fact: description-copy is drafted,
   with a marked gap for the end time (e.g. `[end time — awaiting your
   answer]`) rather than a guessed time.
6. No venue or address is asked for.
7. There is no flyer task (webinars have no template) and no Zoho task.
8. The WordPress event category is Virtual Workshop (688).
9. Exactly 2 email drafts are planned: announce and last call.
10. No send date, send time, resend date, post date, or `SCHEDULED` status is
    set or planned anywhere.
11. The Eventbrite tag list uses the webinar defaults (`employment`,
    `careers`, `webinar`, `online`) and contains neither `jobfair` nor
    `hiring`.
12. No published item or created email draft contains the gap text.

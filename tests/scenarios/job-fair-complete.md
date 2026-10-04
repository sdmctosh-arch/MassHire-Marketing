# Scenario — job-fair-complete

A complete job fair request. Nothing is missing, so nothing may be asked.

## Message

> New job fair. Southbridge Job Fair, Thursday November 12, 2026, 10am to
> 1pm, at the Southbridge Community Center. We expect employers from
> manufacturing, healthcare and retail. Thanks!

## World

- Drive: `index.md` exists and has no row for this event. All writes succeed.
- Preflight: every connector check passes.
- Eventbrite events: none with a similar name or the date 2026-11-12.
- Eventbrite saved venues: "Southbridge Community Center", 99 Main Street,
  Southbridge, MA 01550.
- WordPress: no event post with a similar title.
- Zoho `Job_Fairs`: no record with a similar name or date.
- Redirection: `southbridgefair` has an existing redirect (from 2025).
  `southbridgejobfair` and `southbridgejobfairemployer` are free.
- Canva: both brand templates are found.
- Every create call returns success with a new id.

## Assertions

1. `event_kind` is job-fair and `format` is in person.
2. No question is asked anywhere in the review packet.
3. The project slug is `2026-11-12-southbridge-job-fair`.
4. The address is filled from the Eventbrite saved venue (source: lookup).
5. `jobseeker_slug` is `southbridgejobfair`, and `southbridgefair` is listed
   as a rejected candidate. `employer_slug` is `southbridgejobfairemployer`.
6. The task list contains zoho-job-fair, flyer-qr, flyer, and flyer-export.
7. Exactly 3 email drafts are created: announce, reminder, last call. Each
   has a subject and a different resend subject.
8. Exactly 1 social draft is created, with `status: DRAFT`.
9. The flyer uses the template "MH Event - Job Fair".
10. The WordPress event categories are Job Fair (684) and Employer
    Registration (1016).
11. The email and flyer copy names sectors (manufacturing, healthcare,
    retail), not individual employers, and says the registration page will
    be updated as employers confirm.
12. No send date, send time, resend date, post date, or `SCHEDULED` status is
    set or planned anywhere, and no scheduling tool is called.
13. No redirect is created in the draft pass; redirects appear only in the
    execute list, after the Eventbrite publish.
14. The review packet lists "add the tags to the Eventbrite draft" as an
    operator action before approving.
15. No message is written to anyone other than the operator.
16. The QR code encodes the Eventbrite `jobseeker_link`, and the flyer's
    printed address (`cta_url`) is the short link
    `https://masshirecentralcc.com/southbridgejobfair`.
17. The Eventbrite tag list has at most 10 tags: the 4 defaults plus
    manufacturing, healthcare, retail, and southbridge.
18. The social draft carries no image.
19. The WordPress event draft is created in the draft pass; it does not wait
    on the flyer.
20. The Eventbrite draft gets the stored order-form questions: cell phone
    (built-in, required), city or town, military service (Yes/No), full-time
    or part-time (Full time/Part time/Either), industries, and how they heard,
    all required, on Registration only; none on the walk-in Admission ticket.

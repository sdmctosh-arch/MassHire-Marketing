# Scenario — recruitment-event

One employer hiring. Checks the naming rule, the single redirect, and the
Job Listings flyer.

## Message

> NFI Industries wants a recruitment event at our Worcester office,
> Wednesday November 18, 2026, 9am to noon. They're hiring CDL-A Truck
> Drivers (Leicester, $28/hr) and Yard Jockeys (Leicester, $22/hr).

## World

- Drive: `index.md` exists and has no row for this event. All writes succeed.
- Preflight: every connector check passes.
- Eventbrite events: none matching.
- Eventbrite saved venues: "MassHire Worcester Career Center", 340 Main
  Street, Suite 400, Worcester, MA 01608.
- WordPress: no matching event post.
- Redirection: `nfi` is free.
- Canva: both brand templates are found; an asset named "NFI Industries logo"
  exists.
- Every create call returns success with a new id.

## Assertions

1. `event_kind` is recruitment and `hiring_employer` is NFI Industries.
2. `event_name` has the form `Recruitment Event: NFI Industries (<Job Name>)`,
   where the job name is a category of work (e.g. Truck Drivers, Drivers,
   Transportation), not a single job title copied verbatim.
3. No question is asked.
4. The venue is matched to the saved venue "MassHire Worcester Career
   Center" and the address comes from it.
5. There is no zoho-job-fair task and no employer redirect; exactly one
   redirect (`nfi`) is planned.
6. Exactly 2 email drafts are created: announce and last call.
7. The flyer uses the template "MH Event - Job Listings", and the NFI logo
   asset is used for `partner_logo`.
8. The WordPress event category is Recruitment Event (973).
9. The email copy names NFI Industries.
10. No send date, send time, resend date, post date, or `SCHEDULED` status is
    set or planned anywhere, and no scheduling tool is called.
11. The emails contain no registration mechanics (no slot lengths, no ticket
    class names).
12. No task lists `employer_link` or `employer_short_link` in `uses`, and
    description-copy's `uses` names fields rather than "all facts".

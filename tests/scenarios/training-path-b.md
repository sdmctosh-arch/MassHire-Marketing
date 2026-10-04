# Scenario — training-path-b

A training link that is only an application form. Checks the path decision,
the build order, and that cost is not invented.

## Message

> Please promote this CNA training: https://example.org/qcc/cna-apply

## World

- Drive: `index.md` exists and has no row for this training. All writes
  succeed.
- Preflight: every connector the training playbook needs passes.
- https://example.org/qcc/cna-apply is a form titled "CNA Training
  Application — QCC Workforce Development" with fields for name, phone,
  email, and "Why are you interested?". The page has no program description,
  schedule, location, or cost.
- WordPress: `training-category` terms include "Healthcare". Directorist
  categories include "Healthcare Training"; locations include "Worcester".
- Creating a `training` draft returns sample permalink
  https://masshirecentralcc.com/training/cna-training/.
- Every create call returns success with a new id.

## Assertions

1. `path` is B, and the reason (an application form with no program
   information) is stated as an assumption.
2. The task list contains training-post and directorist-listing, and no
   Eventbrite, Zoho, redirect, or flyer task.
3. `public_link` is the training post's sample permalink, not the submitted
   form link.
4. The Directorist listing's `_website` is the training post permalink.
5. Exactly 2 email drafts (announce, last call) and 1 social draft are
   planned, all linking to `public_link`.
6. Cost is not written as "no cost" or "free" anywhere.
7. The execute list publishes the training post before the Directorist
   listing, and includes confirming the email REGISTER buttons point at the
   live `public_link`.
8. No send date, send time, resend date, post date, or `SCHEDULED` status is
   set or planned anywhere.
9. No question is asked (the form link is the only Required fact, and it was
   given).
10. The Directorist listing has a category term and no location term (no
    source gives a location), and this does not block publishing it.

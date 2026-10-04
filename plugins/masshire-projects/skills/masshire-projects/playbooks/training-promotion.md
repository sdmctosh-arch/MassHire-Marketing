# Playbook — Training Promotion

A training program that MassHire promotes. The deliverables are WordPress
entries, Constant Contact email drafts, and a social post draft.

## Fields

Source key as in `playbooks/event.md`.

| Field | Source and rule |
|---|---|
| `training_link` | **Required**: the submitted link. |
| `path` | **Derived**: open the submitted link. A page with a full program description AND a way to apply → **A**. An application form with no program information → **B**. State the result and the reason as an assumption. |
| `training_title` | **Request**; else **Lookup** from the linked page. |
| `organization` | **Request**; else **Lookup** from the linked page. |
| `eligibility` | **Request** or **Lookup**; omitted if neither. |
| `format`, `location`, `schedule` | **Request** or **Lookup**; omitted if neither. |
| `cost` | **Request** or **Lookup**. Written as "no cost" only when a source says it is free. |
| `application_deadline` | **Request** or **Lookup**; used in copy only. |
| `training_start` | **Request** or **Lookup**; used in copy only. |
| `public_link` | **Derived**. Path A: `training_link`. Path B: the training post's permalink, read from the draft's sample permalink in the draft pass and confirmed after publish. |
| `copy` | **Generated** by `description-copy`: the Drive id of `descriptions/<project>.html`. Every task that takes from the copy lists it in `uses`. |
| `training-category` term | **Derived** by the `wordpress` match-or-propose term policy. |
| Directorist category and location terms | **Derived**, the same way. |
| Listing search text, excerpt | **Written**. |

## Defaults

| Setting | Default |
|---|---|
| Eventbrite, Zoho, redirects | None. |
| Email drafts | 2: announce, last call |
| Social post drafts | 1 |
| Flyer | None. No training template exists. |

## The two paths

| Path | The link points to | Build |
|---|---|---|
| A | A landing page with a full description AND an application | Directorist listing only. Its `_website` is the submitted link. |
| B | An application form only, with no program information | A `training` post, then a Directorist listing whose `_website` is the training post permalink. |


## Task list

| # | Task | Component | needs | uses |
|---|---|---|---|---|
| 1 | existing-check | `existing-check` | — | training_title |
| 2 | description-copy | `description-copy` | — | all facts |
| 3 | training-post (path B only) | `training-post` | 1, 2 | copy, training_link, organization |
| 4 | directorist-listing | `directorist-listing` | 1; 3 on path B; 2 on path A | copy, public_link |
| 5 | training-emails | `constant-contact-email` | 2; 3 on path B | copy, public_link |
| 6 | facebook-post | `facebook-post-draft` | 2; 3 on path B | copy, public_link |
| 7 | review-packet | SKILL.md | all above | — |
| 8 | execute | Execute list below | 7 approved | — |

## Execute list

1. Create any new taxonomy term listed in the review packet.
2. Path B: publish the training post. Confirm its permalink equals
   `public_link`; if not, update `public_link` (staleness marks the listing,
   emails, and social post stale — correct each before step 3).
3. Publish the Directorist listing.
4. Confirm every email draft's REGISTER buttons point at the live
   `public_link` (the destination check in `constant-contact-email`).
5. Report, and write the handoff list to STATUS.

## Rules for this project type

- **The listing is never the destination.** Directorist is for site search and
  browsing. The emails and the social post use `public_link`.
- **Path B order is fixed at execute.** The training post publishes before
  the listing.

## Operator actions

After the execute pass: attach the "Email List" segment and schedule each
email draft in Constant Contact; schedule the social draft.

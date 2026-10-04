# Component — training-post

Access: the `wordpress` system (Novamira). The post is created as a draft in
the draft pass; publication is Level 2 and runs in the execute pass.

Used on path B only: the submitted link is an application form with no program
information, so the site must carry the description.

## Fields to set

| Field | Value |
|---|---|
| post type | `training` |
| post_title | The training title |
| post_name | A slug from the title |
| post_content | The copy, every part except `headline`, in order (`description-copy`). Eligibility is in the copy when a source states it. |
| `training-category` | Match-or-propose term policy, exactly one term |
| link | The submitted application link or email address |
| button_text | `Apply`, for both a link and an email address |

Also fill each of these when the request or the linked page provides it;
leave it empty otherwise: organization_name, application_deadline,
training_starts, summary, email, phone_number, contact_name, format,
location_name, location_address, audience, eligibility_requirements, schedule,
recurring. Leave `flyer` empty (trainings have no flyer).

## Process

1. Run the `wordpress` draft-post procedure with the fields above: update
   the post `existing-check` matched, else create.
2. Read the draft's sample permalink (the procedure, step 5) and write it to
   the values block as `public_link`. Read the preview link for the review
   packet.

## Execute

Publish by the `wordpress` procedure. Confirm the live permalink equals
`public_link`; if it differs, update the value (the playbook's execute list
handles the stale tasks).

## Checks

- [script] Exactly one `training` post with this title after the run.
- [script] `button_text` is `Apply`.
- [script] `training-category` is set to exactly one term.
- [script] No `awaiting your answer` in any field.
- [judgement] The description matches the copy.

# Component — training-post

Access: writes to the live site through the Novamira connector. The post is
created as a WordPress draft in the draft pass; publication is Level 2 and
runs in the execute pass.

Used on path B only: the submitted link is an application form with no program
information, so the site must carry the description.

## Tool facts

Custom post type `training`. Taxonomies `training-category` and
`training-audience`. Fields are post meta, written like ACF fields.

## Fields to set

| Field | Value |
|---|---|
| post_title | The training title |
| post_content | The copy, every part except `headline`, in order (`description-copy`). Eligibility is in the copy when a source states it. |
| training_category | An existing term matched on meaning. A new term is listed in the review packet and created at execute. |
| link | The submitted application link or email address |
| button_text | `Apply`, for both a link and an email address |

Also fill each of these when the request or the linked page provides it;
leave it empty otherwise: organization_name, application_deadline,
training_starts, summary, email, phone_number, contact_name, format,
location_name, location_address, audience, eligibility_requirements, schedule,
recurring. Leave `flyer` empty (trainings have no flyer).

## Process

1. If `existing-check` recorded a matching `training` post, update it with
   the fields below. Otherwise create the post as a draft with a `post_name`
   slug from the title; set the fields and the category term.
2. Read the draft's sample permalink (`get_sample_permalink`) and write it
   to the values block as `public_link`. Read the preview link for the
   review packet.

## Execute

Publish the post. Confirm the live permalink equals `public_link`; if it
differs, update the value (the playbook's execute list handles the stale
tasks).

## Checks

- [script] Exactly one `training` post with this title after the run.
- [script] `button_text` is `Apply`.
- [script] `training_category` is set to exactly one term.
- [script] No `awaiting your answer` in any field.
- [judgement] The description matches the copy.

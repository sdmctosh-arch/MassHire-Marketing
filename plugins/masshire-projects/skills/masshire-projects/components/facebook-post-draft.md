# Component — facebook-post-draft

Access: drafts only. The system never publishes or schedules to Facebook. The
Drive file is the source of the copy; the Constant Contact social draft is
the delivery, created in the draft pass (Level 1: a DRAFT is not public).

## Inputs

The copy in `descriptions/`, the social post count from the playbook, and
jobseeker_short_link (event) or public_link (training). Posts carry no image:
the flyer is a print design, not a social one.

## Process

1. Write each post to `social/post-<n>.txt` in the project folder. Text
   derives from the copy's `summary` part; do not write new event facts. Short, one link,
   plain language. No hashtags.
2. Create the Constant Contact social draft:
   `create_social_post`, `status: DRAFT`, one `profile_posts` entry:

   ```
   name:          <Event Name> - YYYY-MM-DD - Facebook <n>
   status:        DRAFT
   profile_posts: [{ profiles: [{ profile_id: 9a50cd21-94e0-4e4e-8896-eb4079f2cb96 }],
                     text: <post text> }]
   ```

   The profile id is MassHire's Facebook page. No `images`: the post is
   text-only.
3. Verify from the response, not by re-reading: `status` is `DRAFT`,
   `profile_name` is the MassHire page, the text came back with the link
   intact. Record `campaign_id` and the profile's
   `campaign_activity_id` on the task.

## Tool facts

- The connector exposes no `/social/profiles` list. Profile ids cannot be
  discovered through it.
- `images`, when a future post uses one, must be a list of objects with a
  `url` key, not a list of strings, and each url must be publicly reachable.
- A `DRAFT` carries no date. The system never sets `SCHEDULED`.
- `update_social_post` edits an existing campaign by `campaign_id`.
  Revise in place rather than creating a second campaign.

## Checks

- [script] The link equals this project's short link (event) or public_link
  (training).
- [script] The profile id is the one above.
- [script] No `awaiting your answer` in the text.
- [judgement] The text reads well on its own, with no image.

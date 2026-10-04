# Component — facebook-post-draft

Access: drafts only. The system never publishes or schedules to Facebook. The
Drive file is the source of the copy; the Constant Contact social draft is
the delivery, created in the draft pass (Level 1: a DRAFT is not public).

## Inputs

The copy in `descriptions/`, the social post count from the playbook, the
flyer PNG export when the flyer is in scope, and jobseeker_short_link (event)
or public_link (training).

## Process

1. Write each post to `social/post-<n>.txt` in the project folder. Text
   derives from the copy; do not write new event facts. Short, one link,
   plain language. No hashtags.
2. Create the Constant Contact social draft:
   `createSocialPostUsingPOST`, `status: DRAFT`, one `profile_posts` entry:

   ```
   name:          <Event Name> - YYYY-MM-DD - Facebook <n>
   status:        DRAFT
   profile_posts: [{ profiles: [{ profile_id: 9a50cd21-94e0-4e4e-8896-eb4079f2cb96 }],
                     text: <post text>,
                     images: [{ url: <flyer PNG url> }] }]
   ```

   The profile id is MassHire's Facebook page, also listed in `index.md`
   under Shared assets. When the flyer is out of scope, omit `images`: the
   post is text-only by design.
3. Verify from the response, not by re-reading: `status` is `DRAFT`,
   `profile_name` is the MassHire page, the text came back with the link
   intact, the image is attached. Record `campaign_id` and the profile's
   `campaign_activity_id` on the task.

## Tool facts

- The connector exposes no `/social/profiles` list. Profile ids cannot be
  discovered through it.
- `images` must be a list of objects with a `url` key, not a list of strings,
  and each url must be publicly reachable. The Canva export URL works when
  used right after export (tested); it expires, so create the social draft in
  the same session as the export. If an image ever fails to render, upload
  the PNG to MyLibrary (`upload_my_library_file`) and use that URL.
- A `DRAFT` carries no date. The system never sets `SCHEDULED`.
- `updateSocialPostUsingPUT` edits an existing campaign by `campaign_id`.
  Revise in place rather than creating a second campaign.

## Checks

- [script] The link equals this project's short link (event) or public_link
  (training).
- [script] The profile id is the one above.
- [judgement] The text stands alone without the image.

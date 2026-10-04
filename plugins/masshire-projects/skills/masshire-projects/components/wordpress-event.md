# Component — wordpress-event

Access: writes to the live site through the Novamira connector. The event is
created as a WordPress draft in the draft pass; publication is Level 2 and
runs in the execute pass.

## Tool facts

- The Events Calendar plugin is inactive. Events are a custom post type
  `event` with ACF fields and an `event-category` taxonomy.
- The post type has `rewrite` false, so event URLs are query strings,
  site-wide. Do not treat that as a fault.

## Inputs

From the values block: event_date, start_time, end_time, venue, address,
jobseeker_link, employer_link (may be empty; see `zoho-job-fair` step 3). One
short line of post content, written from the copy. The exported flyer PNG,
if `flyer-export` is done; the event never waits for it.

## Process

1. If existing-check recorded a matching WordPress event post, use it:
   update that post with the fields below instead of creating one.
   Otherwise create the post: type `event`, the short content line, status
   `draft`.
2. Write the ACF fields: `date` and `date_formatted` (Ymd), `start_time` and
   `end_time` (H:i:s), `all_day` 0, `location`, `address`, `registration_url`,
   `registration_label` "Register".
3. When employer registration is in scope, set
   `employer_registration_required` 1,
   `employer_registration_url`, `employer_registration_label`
   "Register as an Employer". If the employer link value is still empty,
   create the event anyway; the value fill marks this task stale and the
   fields are added then.
4. Set the `event-category` term(s) from the playbook's kind table. Never
   create a term; a case the table does not cover is flagged in the review
   packet.
5. For an online event, `location` is `Online` and `address` is empty.
6. If the flyer PNG exists: upload it to the media library and set the
   `flyer` field to it (tested). If the flyer is not exported yet, create the
   event without it. When `flyer-export` finishes later in the draft pass,
   add the flyer to this draft in place. If the flyer is still missing at
   execute, publish without it and list "add the flyer to the website event"
   in the handoff.
7. Read the preview link for the review packet.

## Execute

Publish the post (status `publish`). Read back its URL.

## Checks

- [script] All date and time fields match the values block, correct formats.
- [script] The registration URLs match this project's values, not another
  project's (concurrency rule).
- [script] The category term is set and no duplicate post exists.
- [judgement] The page reads correctly in preview.

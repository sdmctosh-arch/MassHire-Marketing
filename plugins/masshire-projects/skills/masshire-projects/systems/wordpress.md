# System — wordpress

Access: the live masshirecentralcc.com site, through the Novamira connector.
`discover-abilities` lists what it exposes; everything below runs PHP on the
site through `novamira/execute-php`, which returns what the PHP returns.
Preflight checks Novamira once (SKILL.md).

A caller does five things through it: find a post by title, create or update
a draft post of a type, set its terms by a term policy, read its preview or
sample permalink, and publish it. The Redirection plugin is reached the same
way but is not a post: `vanity-redirect` holds its own PHP.

## Site facts

- The Events Calendar plugin is inactive. Events are a custom post type
  `event` with ACF fields and an `event-category` taxonomy. The post type has
  `rewrite` false, so event URLs are query strings, site-wide. Do not treat
  that as a fault.
- Trainings are a custom post type `training` with taxonomies
  `training-category` and `training-audience`. Fields are post meta, written
  like ACF fields.
- Directorist listings are post type `at_biz_dir` with taxonomies
  `at_biz_dir-category`, `at_biz_dir-location`, `at_biz_dir-tags`, and
  `atbdp_listing_types`. Meta keys carry a leading underscore. Real example:
  listing 56577, whose `_website` points at training post 56574.
- Redirects are the Redirection plugin's `Red_Item` rows, group 1 (see
  `vanity-redirect`).

## Before the first write

Read the tool before you write input for it (SKILL.md): once per session,
run one read through `execute-php` (`get_post(<known id>)`) to confirm the
ability runs PHP and returns arrays. Never assume a post type, taxonomy, or
plugin is active: `post_type_exists('<type>')`, `taxonomy_exists('<tax>')`,
`function_exists('update_field')` for ACF.

## The draft-post procedure

1. **Find.** `get_posts(['post_type' => T, 'post_status' => 'any',
   's' => '<title>', 'numberposts' => 5])`, then compare titles.
   `existing-check` runs this at intake; a component reads its record and
   never searches again.
2. **Create or update.** `wp_insert_post([...], true)` with `post_type`,
   `post_title`, `post_name`, `post_content`, `post_excerpt`, and
   `post_status => 'draft'`; for the post `existing-check` matched,
   `wp_update_post` with its `ID`. Check `is_wp_error` on the result.
3. **Fields.** ACF fields with `update_field('<name>', <value>, <id>)`, so
   the field-key reference is stored and the admin shows the value; plain
   meta with `update_post_meta(<id>, '<key>', <value>)`. Formats are the
   component's field table.
4. **Terms.** By the term policy below.
5. **Preview and permalink.** `get_preview_post_link(<id>)` for the review
   packet. `get_sample_permalink(<id>)` returns `[<template>, <slug>]`;
   substitute `%postname%` (or `%pagename%`) with the slug for the public
   link the draft will have.
6. **Publish.** Level 2, execute pass only:
   `wp_update_post(['ID' => <id>, 'post_status' => 'publish'])`, then read
   back `get_permalink(<id>)` and `get_post_status(<id>)`.
7. **A file into the media library.** `wp_upload_bits(<name>, null,
   <bytes>)`, `wp_insert_attachment` with the returned file path,
   `wp_generate_attachment_metadata` and `wp_update_attachment_metadata`;
   then set the field to the attachment id.

## Term policies

| Policy | Used by | Rule |
|---|---|---|
| fixed | `wordpress-event` | The component names the term ids. `wp_set_object_terms(<id>, [<ids>], '<tax>')`. Never create a term; a case the component's table does not cover is flagged in the review packet. |
| match or propose | `training-post`, `directorist-listing` | `get_terms(['taxonomy' => '<tax>', 'hide_empty' => false])`; match an existing term on meaning, not on spelling (a near-duplicate splits browsing). None fits: propose the new term in the review packet, create it at execute with `wp_insert_term`, then set it (the playbook's execute list, step 1). Nothing is created in the draft pass. |

## Checks

For every post this procedure creates, in addition to the component's own:

- [script] `get_post_status` is `draft` until the execute pass, then
  `publish`.
- [script] Exactly one post of the type with this title.
- [script] Every field read back (`get_field` or `get_post_meta`) equals
  what was sent.

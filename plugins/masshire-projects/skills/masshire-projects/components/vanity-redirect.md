# Component — vanity-redirect

A short masshirecentralcc.com path that forwards to a long registration URL,
so a flyer, a social post, or a spoken announcement carries one readable link.

Access: the Redirection plugin has no Novamira ability. Create and read
redirects by running PHP through the Novamira connector
(`novamira/execute-php`), which loads the plugin's own `Red_Item` class.
The slug is chosen and checked in the draft pass and shown in the review
packet, because it goes on printed material. The redirect is created in the
execute pass (Level 2). Deleting one is reversible and needs no approval.

## Inputs

A destination URL and a slug. Two redirects per job
fair:

| Redirect | Destination | Value it fills |
|---|---|---|
| Jobseeker | the Eventbrite public URL (`jobseeker_link`), published in execute step 1 | `jobseeker_short_link` |
| Employer | the Zoho `Registration_Link` (`employer_link`) | `employer_short_link` |

Never create a redirect before its Eventbrite event is published, and never
point one at a link built by hand.
Read the destination from this project's values block, which the
`eventbrite-event` and `zoho-job-fair` components filled from the live system.

## The slug

- One word, lowercase, letters and digits only. No hyphens, no dates, no year.
- Name the thing the audience already knows: the town, the employer, or the
  format. `southbridgefair`, `vulcanforms`, `nfi`, `virtualjobfair`.
- The employer slug is the jobseeker slug plus `employer`:
  `graftonemployer`. It is never announced publicly; the BSR sends it.
- Short enough to say out loud and to read on a flyer at arm's length.
- A slug is reused across years only if the old redirect is repointed, never
  duplicated. Check first.

## Process

1. Check the plugin is active and the path is free, in one read:

   ```php
   global $wpdb;
   return [
     'plugin_active' => class_exists('Red_Item'),
     'existing'      => $wpdb->get_results($wpdb->prepare(
         "SELECT id, url, action_data, status FROM {$wpdb->prefix}redirection_items WHERE url IN (%s, %s)",
         '/<slug>', '/<slug>/'), ARRAY_A),
     'post_at_path'  => url_to_postid(home_url('/<slug>')),
   ];
   ```

   The match is exact (the path with and without a trailing slash; the
   table's collation ignores case). Never match with `LIKE '%<slug>%'`: it
   also hits every longer slug that contains this one, so `graftonfair`
   would be rejected because `graftonfairemployer` exists.
   A row in `existing`, or a non-zero `post_at_path` (a real page owns the
   path), means the slug is not usable. Take the next candidate by the slug
   rules (add the format word, e.g. `southbridgefair` → `southbridgejobfair`)
   and check again. Never repoint an existing redirect without the operator
   saying so. Record the chosen slug as a value; it goes in the review packet
   with any rejected candidates. This is the end of the draft pass for this
   task.

2. Execute pass: run the step 1 check again (the path may have changed since
   the review), then create it:

   ```php
   $result = Red_Item::create([
     'url'         => '/<slug>',
     'action_data' => ['url' => '<destination>'],
     'match_type'  => 'url',
     'action_type' => 'url',
     'action_code' => 301,
     'group_id'    => 1,
     'title'       => '<event name> — <jobseeker|employer>',
     'match_data'  => ['source' => [
        'flag_case'     => true,
        'flag_trailing' => true,
        'flag_regex'    => false,
        'flag_query'    => 'exact',
     ]],
   ]);
   return is_wp_error($result) ? ['error' => $result->get_error_message()]
                               : ['created' => $result->to_json()];
   ```

   `flag_case` and `flag_trailing` are always set: a slug printed on a flyer
   gets typed back with capitals and a trailing slash. Group 1 is the only
   redirect group on the site. 301 is the default; it is cached by browsers,
   which is why repointing a reused slug needs a cache-clear warning to the
   operator.

3. Record the redirect id in the task, so it can be repointed or deleted
   later, and write the LOG line with the id. (The short URL value was
   filled in the draft pass, when the slug was chosen.)

## Rollback

```php
$item = Red_Item::get_by_id(<id>);
return $item ? $item->delete() : 'not found';
```

## Checks

- [script] `Red_Item::get_for_url()` returns this redirect for four spellings
  of the path: plain, capitalized, trailing slash, capitalized with trailing
  slash. Test them; do not assume the flags took.
- [script] The stored `action_data` equals the values-block link character for
  character, and for the employer redirect the `jfid` in it matches this
  project's Zoho record id.
- [script] Fetch the short URL and confirm the final location is the
  destination.
- [judgement] The operator opens the short URL in a browser and lands on the
  right event. If the path was ever visited before the redirect existed,
  LiteSpeed may have cached the 404 — purge from the LiteSpeed Cache toolbar
  in wp-admin and retest.
- [judgement] The slug is not already printed on another live event's
  material.

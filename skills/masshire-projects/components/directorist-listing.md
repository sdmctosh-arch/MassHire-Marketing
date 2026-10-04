# Component — directorist-listing

Access: writes to the live site through the Novamira connector. The listing
is created as a draft in the draft pass; publication is Level 2 and runs in
the execute pass, after the training post on path B.

Every training gets a listing, on both paths. The listing makes the training
findable in site search and browsing. It is not the destination.

## Tool facts

Post type `at_biz_dir`. Taxonomies: `at_biz_dir-category`,
`at_biz_dir-location`, `at_biz_dir-tags`, `atbdp_listing_types`.
Meta keys carry a leading underscore.

Real example: listing 56577, whose `_website` points at training post 56574.

## Fields to set

| Field | Value |
|---|---|
| `_directory_type` | `390` |
| post_title | The training title, matching the training post when there is one |
| post_content | **Search text, not display text.** Not shown anywhere on the site. Include all text about the training, plus search terms a jobseeker would type: the trade, the job titles it leads to, related skills, common misspellings, and plain words for the field. |
| post_excerpt and `_excerpt` | A short public description, two or three sentences |
| `_website` | Path A: the submitted link. Path B: the training post permalink. Always read it from `public_link` in the values block. |
| `at_biz_dir-location` | An existing term matched on meaning; a new term is listed in the review packet and created at execute |
| `at_biz_dir-category` | Same as location |

## Process

1. Search `at_biz_dir` for the same title first.
2. On path B, confirm the training post draft exists and its sample
   permalink is in `public_link` before creating the listing.
3. Create as a draft, set the meta and both excerpt places, assign the terms.
4. Before proposing a new taxonomy term, list the existing terms and match on
   meaning, not on exact spelling. A near-duplicate term splits browsing.

## Execute

Publish the listing. Confirm `_website` still equals `public_link`.

## Checks

- [script] `_directory_type` is 390.
- [script] `_website` equals `public_link` exactly and is not empty.
- [script] `_excerpt` and post_excerpt hold the same text.
- [script] One category term and one location term are set.
- [judgement] The description holds real search terms, not a copy of the
  excerpt.

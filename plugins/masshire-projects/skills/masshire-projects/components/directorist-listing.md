# Component — directorist-listing

Access: the `wordpress` system (Novamira). The listing is created as a draft
in the draft pass; publication is Level 2 and runs in the execute pass,
after the training post on path B.

Every training gets a listing, on both paths. The listing makes the training
findable in site search and browsing. It is not the destination.

## Fields to set

| Field | Value |
|---|---|
| post type | `at_biz_dir` |
| `_directory_type` | `390` |
| post_title | The training title, matching the training post when there is one |
| post_content | **Search text, not display text.** Not shown anywhere on the site. Include all text about the training, plus search terms a jobseeker would type: the trade, the job titles it leads to, related skills, common misspellings, and plain words for the field. |
| post_excerpt and `_excerpt` | The copy's `summary`, then up to two sentences from its `body` |
| `_website` | Path A: the submitted link. Path B: the training post permalink. Always read it from `public_link` in the values block. |
| `at_biz_dir-category` | Match-or-propose term policy, exactly one term |
| `at_biz_dir-location` | Match-or-propose term policy, at most one term, only when a source gives a location. No location in any source: no term. |

## Process

1. On path B, confirm the training post draft exists and its sample
   permalink is in `public_link` before creating the listing.
2. Run the `wordpress` draft-post procedure with the fields above: update
   the listing `existing-check` matched, else create.

## Execute

Publish by the `wordpress` procedure. Confirm `_website` still equals
`public_link`.

## Checks

- [script] `_directory_type` is 390.
- [script] `_website` equals `public_link` exactly and is not empty.
- [script] `_excerpt` and post_excerpt hold the same text.
- [script] One category term is set, and at most one location term (none
  when no source gives a location).
- [script] No `awaiting your answer` in any field.
- [judgement] The description holds real search terms, not a copy of the
  excerpt.

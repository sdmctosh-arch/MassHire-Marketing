# Component — wordpress-event

Access: the `wordpress` system (Novamira). The event is created as a draft
in the draft pass; publication is Level 2 and runs in the execute pass.

## Inputs

The values this task lists in `uses` (the playbook task table);
employer_link may be empty (see `zoho-job-fair` step 3). The copy's
`summary` part as the post content. The exported flyer PNG, if
`flyer-export` is done; the event never waits for it.

## Fields to set

| Field | Value |
|---|---|
| post type | `event` |
| post_content | The copy's `summary` part |
| `date`, `date_formatted` | event_date, format `Ymd` |
| `start_time`, `end_time` | start_time, end_time, format `H:i:s` |
| `all_day` | 0 |
| `location`, `address` | venue, address. Online event: `Online` and empty |
| `registration_url`, `registration_label` | jobseeker_link, "Register" |
| `employer_registration_required`, `employer_registration_url`, `employer_registration_label` | When employer registration is in scope: 1, employer_link, "Register as an Employer". If the link is still empty, create the event anyway; the value fill marks this task stale and the fields are added then |
| `flyer` | The exported PNG as a media-library attachment (tested), when `flyer-export` is done; otherwise empty |
| `event-category` | Fixed term policy. Ids: Job Fair 684, Employer Registration 1016, Recruitment Event 973, Virtual Workshop 688, Worcester 685, Southbridge 1009. The playbook's kind table says which apply; a case it does not cover is flagged in the review packet |

## Process

1. Run the `wordpress` draft-post procedure with the fields above: update
   the post `existing-check` matched, else create.
2. Create the event as soon as this task's `needs` are done. Do not run the
   flyer tasks first to have the PNG ready. When `flyer-export` finishes
   later in the draft pass, add the flyer to this draft in place. If the
   flyer is still missing at execute, publish without it and list "add the
   flyer to the website event" in the handoff.
3. Read the preview link for the review packet.

## Execute

Publish by the `wordpress` procedure. Read back the URL.

## Checks

- [script] All date and time fields match the values block, correct formats.
- [script] The registration URLs match this project's values, not another
  project's (concurrency rule).
- [script] The category term is set and no duplicate post exists.
- [script] No `awaiting your answer` in any field.
- [judgement] The page reads correctly in preview.

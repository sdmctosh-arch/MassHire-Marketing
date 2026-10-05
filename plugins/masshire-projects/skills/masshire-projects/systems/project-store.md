# System — project-store

All project state lives in Google Drive, in one file per project. The Cowork
filesystem resets between sessions and holds nothing. This file says how
that state is found, read, written, and kept current. Read it before the
first Drive call of a session.

A caller does six things through it: open a project, create one, write a
checkpoint, fill a value, rename a slug, and update the index row. Every
other Drive detail is inside.

## Where state lives

```
MassHire Projects/                 id 1AczGC82kIJlLGGUHy59hgJ9Emm74Nkr-
  index.md                         registry of every project — read this first
  masshire-projects/               id 1SdRqj_wUMgolxLq-RMuFBUQpa7OgD590
    eventbrite-token.txt           shared credentials, not project state
    templates/jobseeker-email.html the email base HTML (see `constant-contact-email`)
  <slug>/                          one folder per project
    project.md                     the project file, single source of truth
    descriptions/                  the approved copy, one .html per project
    campaigns/                     email draft copies
    social/                        social post drafts
    flyer/                         QR files and flyer exports
    drafts/                        subagent output
```

Slug format: `YYYY-MM-DD-kebab-case-name`. The date is the event date (for a
training: the date the project starts).

## index.md

One table, one row per project, newest first:

```
| slug | type | event_date | status | folder_id | notes |
```

Every column is filled on every row; `notes` may be empty. A new project's
row, as appended:

```
| 2026-11-12-southbridge-job-fair | event/job-fair | 2026-11-12 | intake | 1AbCfolderid | |
```

`type` is the playbook and, for events, the kind (`event/job-fair`,
`training`). `event_date` is the slug's date. `status` mirrors the project
file's status. `notes` holds an old slug after a rename, and nothing else
routine.

`index.md` is written only at a checkpoint, in the same checkpoint as the
project file, and only when a row is added or its status changes. A new
project's first turn writes it twice, by design: the row at creation
(`intake`), then `review` at the end of the draft pass.

## Tool loading

Load the Drive tools in one `tool_search` call covering `search_files`,
`download_file_content`, `create_file`, `update_file`, and `trash_file`.

## Opening a project

1. Read `index.md` and take the `folder_id` from the project's row.
2. List that folder: `parentId = '<folder_id>'`, with
   `excludeContentSnippets: true`.
3. Read `project.md`. Once per session: if you already have a file's
   content, do not re-download it in another format.

If the project is not in `index.md`, search by title, never by content:
`title contains '<slug>' and mimeType = 'application/vnd.google-apps.folder'`.
Then add the missing row to `index.md` before going further.

**Never run `find` or `ls` looking for project files, and never full-text
search Drive for a project.** `fullText contains` returns every past project
with a multi-kilobyte snippet attached to each. It is never the right call.

## Creating a project

Create the Drive folder `<slug>/` under `MassHire Projects`, write
`templates/project-file.md` into it as `project.md`, and append the
project's row to `index.md`.

## Writing a file

Always pass both of these on `create_file`:

```
contentMimeType: "text/markdown"          (or "text/html" for descriptions/)
disableConversionToGoogleType: true
```

Without both, Drive converts the file to a Google Doc and the next read loses
the YAML front matter, the headers, and the table pipes. If you open a
`project.md` whose `mimeType` is `application/vnd.google-apps.document`, fix it
silently before doing anything else: rewrite it as `text/markdown`, verify the
new file reads back correctly, then trash the Doc.

The Drive connector has no tool that rewrites a file's contents — `update_file`
changes metadata only. To edit a stored file: `create_file` the full new
version at the same path, verify it reads back, then `trash_file` the old id.
Never leave both in place. When many small edits have accumulated, rewrite
the file in full.

## Renaming a slug

When the event date turns out to be wrong, the slug is wrong with it. Rename
the folder with `update_file`, correct the `project:` and `event_date:` header,
and fix the `index.md` row in the same pass. Note the old slug in `index.md`.

## The project file

`templates/project-file.md` is the skeleton. Its front matter holds the
header fields, the `values` block, the task list, and `open_questions`; its
body holds STATUS, SOURCE REQUEST, FACTS, LOG, and DECISIONS AND FAILURES.

### Header and values

Times are stored as 24-hour `HH:MM` in the America/New_York time zone
(`10:00`, `13:30`). `online_platform` is filled for online events only.

The `values` block holds every field two or more tasks list in `uses`; the
template says which keys each project type has. Facts one task uses go in
FACTS, each with its source: request, default, derived, lookup, generated,
or written.

### Tasks

Every task carries these fields. Omit a field only where marked optional.

| Field | Holds |
|---|---|
| `id` | The task name from the playbook's task list. |
| `status` | `todo`, `blocked`, `draft`, `approved`, `done`, `skipped`, `stale`. |
| `needs` | Task ids that finish first. Conditional entries are resolved at intake; a task not in this file is never named here. |
| `uses` | Value names. A change to any of them marks this task stale. |
| `blocked_by` | Required when status is `blocked`: the missing fact or the failing check. |
| `output` | Optional. The file path, url, or external id this task produced. |

**Resolve the task table at intake.** The project file holds concrete names
only:

- Drop every `needs` entry whose task is out of scope for this project, and
  leave out-of-scope tasks out of the file entirely (not as `skipped`). A
  `needs` pointing at a task that is not in the file blocks that task
  forever.
- Drop every `uses` entry for a value this project never has: one whose
  producing task is out of scope (`employer_link` and `employer_short_link`
  without employer registration), or one the field table scopes away
  (`online_platform` for an in-person event; `venue` and `address` for an
  online one).
- Expand `all facts` to the name of every field in the playbook's Facts
  table (training: every field in its field table except `public_link`),
  whether or not it has a value yet. Filling an empty one later is a value
  change, so the copy goes stale.

**Status through the run.**

- `todo` until drafted; `blocked` while a missing fact or a failed
  connector holds it; `draft` once its draft exists and passes its checks.
  A task with no private draft (`short-links`) is `draft` once its output
  is recorded.
- The review packet sets `review-packet` to `done`. Approval sets every
  `draft` task to `approved`.
- Each execute action sets its task to `done` once verified. At handoff,
  every `approved` task with no execute action (the flyer, the emails, the
  social post) becomes `done`: its draft is the deliverable. `execute` is
  `done` at handoff, whether or not actions were skipped; a skipped action
  leaves its task `approved` or `blocked`, and is named in STATUS.

Project statuses: `intake`, `review`, `executing`, `handoff`, `closed`. The
`index.md` row mirrors the project status (see index.md).

### Body sections

- **STATUS**: what is waiting on whom, in three lines or fewer. During
  handoff: the operator's remaining work as a numbered list.
- **SOURCE REQUEST**: the original request, unedited.
- **FACTS**: `| Field | Value | Source |`, for facts one task uses.
- **LOG**: `| Date | Event |`. One line per completed task, per value
  change, one `Approved: review packet` line, and one
  `Executed: <task> <action>` line per execute action.
- **DECISIONS AND FAILURES**: `| # | Decision or failure | Kind | Rule |`.
  Kind: project fact, project-type rule, tool fact, universal rule, or
  constraint rule. At close, everything except project facts moves to its
  home and is deleted here.

## Checkpoints

Only the main thread writes the project file. Every write costs three Drive
calls (create, verify, trash), so it is written at checkpoints, not after
every task:

1. after intake (fields, task list, preflight);
2. once after the draft pass, with every task's status and output, just
   before the review packet;
3. after each execute action, so a failure part-way is on record;
4. at handoff, and whenever the operator's message changes a value.

Between checkpoints, keep the changes in the turn. If a session ends
between checkpoints, the next one finds the drafts already made by the
"search before you create" rule, so nothing is created twice.

## Values and staleness

Each task lists the values it uses in `uses`. When a value changes or an
empty value is filled: update the block, write a LOG line, and mark every
task that uses it `stale` if it was `draft`, `approved`, or `done`. Redraft
stale drafts before the review packet. A stale published item is corrected
only with the operator's approval. `needs` means only "which tasks finish
first"; staleness comes from `uses`.

There are no due dates and no scheduled wakes. The project moves only when
the operator sends a message.

## Old project files

A project file with `type: job-fair` is an `event` with `event_kind:
job-fair`; fix its header when it is next opened. A project file with
`campaigns`, `notice_days`, `send_weekday`, `wake`, or `due` fields, a
`marketing-plan` task, or a `freeze-read` task was made by the old version of
this skill: delete those fields and tasks when it is next opened.

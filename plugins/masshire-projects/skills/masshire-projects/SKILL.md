---
name: masshire-projects
description: Orchestrate MassHire multi-step marketing projects (events — job fairs, recruitment and hiring events, webinars, workshops — and trainings) from an incoming request to finished deliverables, with one review gate. Use this skill whenever Steven starts a new event or marketing project, pastes a request email, says "new job fair", "new recruitment event", "new hiring event", "new webinar", or "new workshop", approves or corrects a review packet, resumes a project, asks for project status, or says "close" a project. Also use it for any MassHire email request — drafting, a reminder, a resend, a correction, building a Constant Contact draft — even if Constant Contact is not named; this skill drafts email and never sends or schedules it. Playbooks define each project type; components define each task; a per-project markdown file holds all state.
---

# MassHire Project Orchestration

You run multi-step marketing projects for MassHire Central Career Centers.
A **playbook** says what a project type requires. A **component** says how one
task is done. The **project file** says what is true right now. A sentence that
does not fit one of those three definitions is in the wrong layer.

## The run

Every project runs in four phases. The operator sends one message, approves
once, and the work is done.

1. **Intake.** Extract every fact from the request. Fill every other value
   from its source in the playbook's field table: a default, a derivation, or
   a lookup. Never ask a question at intake.
2. **Draft pass.** Build every deliverable as a draft, in one pass, with no
   approvals. Drafts are private: an unpublished Eventbrite event, a WordPress
   draft, Constant Contact drafts, a committed Canva design, Drive files.
3. **Review packet.** One message (below). The run stops here.
4. **Execute pass.** After the operator approves, run every public action in
   order, verify each, and report once. The execute pass is the end of the
   run.

There is no marketing schedule. The system never decides send dates, send
times, resends, or post dates. The playbook's counts set how many drafts are
created; the operator schedules everything by hand.

### Required facts and missing facts

Only facts the playbook marks **Required** may ever produce a question. When a
Required fact is missing, do not stop: draft every task that does not use it,
mark the others `blocked` with `blocked_by: <fact>`, and put one question at
the top of the review packet. When the answer arrives, fill the value, draft
the blocked tasks, and send an updated review packet.

The copy is the exception: `description-copy` uses every fact, but it is
drafted anyway, with a marked gap where the missing fact goes (the marker
and its redraft are in `description-copy`). Everything that takes from the
copy without using the missing fact can then be drafted. A gap never
reaches a public item: every publishing component checks for it.

Never invent a fact. A default is not an invention: it is a stated rule, and
every default and derived value used is listed in the review packet as an
assumption.

Every choice the operator might want to change is written as an assumption
("Assumed: the Zoom link is sent after registration"), never as a request
("tell me if…", "let me know whether…"). The only questions in a review
packet are for missing Required facts.

### The review packet

One message, in this order:

1. Any question about a missing Required fact.
2. Facts table: each value, and its source (request, default, derived,
   lookup, generated).
3. Assumptions: every default and derivation used, so the operator can
   override any of them.
4. Names and slugs: event name, redirect slug(s).
5. Copy: the description from `descriptions/`.
6. Draft links: Eventbrite edit URL, WordPress preview link(s).
7. Flyer: design link and thumbnail.
8. Email and social drafts: subject, resend subject, preheader, headline,
   body, CTA line, per draft; social text.
9. The `judgement` checks from every drafted component, and any flags (text
   overflow, empty logo frame). A preflight failure goes at the top of the
   packet instead (see Preflight).
10. Operator actions before approving: the playbook's list.
11. What execute will do: the list of public actions, in order.

The operator replies "approve", or "approve, but change X". Apply the changes
to the drafts, then run the execute pass without a second review. Show a
second review only if a change alters something the operator has not seen
(a new slug, a new flyer design).

### The execute pass

"Approve" publishes. Blocked or unfinished drafts do not hold it back unless
something major is missing. Major means a public action would put out
something wrong or broken:

- a Required fact is still missing;
- the item about to be published failed its own checks (for example, the
  Eventbrite event is missing its tickets or order-form questions);
- a link would point at nothing (a redirect whose destination is empty).

Skip only the actions that a major item touches, and the actions that
depend on them; run the rest. Everything else that is blocked or unfinished
(flyer, emails, social draft, a partner logo, the flyer on the website
event) stays as it is and goes in the handoff list. Name every skipped action
and the reason in the report.

Run the playbook's execute list in order. Each action gets one LOG line:
`Executed: <task> <action>` (the review approval is logged once, as
`Approved: review packet`). Verify each action with its component's checks
before the next one. If an action fails, finish the ones that do not depend
on it, then report. Finish with one message: what was done, the links, and
the operator's remaining work (the playbook's handoff list).

## Gates

| Level | Meaning | Approval |
|---|---|---|
| 1 | Private and reversible: a draft, a file, a committed Canva design, a Zoho record | None |
| 2 | Public: publishing, creating a live redirect | The single review packet |

Separate stops exist only where a playbook or component names one.

## Preflight

Check connectors once, at intake, after the playbook is chosen. Check only
the connectors that playbook's in-scope tasks need.

| Connector | Needed for | Check |
|---|---|---|
| Google Drive | every project — all state, plus `eventbrite-token.txt` | reading `index.md` (intake step 1) |
| Novamira | `wordpress-event`, `directorist-listing`, `training-post`, `vanity-redirect`, `existing-check` | `discover-abilities` |
| Eventbrite API v3 | `eventbrite-event`, `existing-check` | Read the token from Drive (`eventbrite-event`, Process step 1), then `GET https://www.eventbriteapi.com/v3/users/me/` with it |
| Constant Contact | `constant-contact-email`, `facebook-post-draft` | `retrieve_email_addresses` |
| Canva | `flyer-from-template` | `search-brand-templates` — the template the flyer needs is in the result |
| Zoho CRM | `zoho-job-fair`, `existing-check` — job fairs only | `getModules` |

Every check is read-only. Report one line per connector:

```
Preflight — Drive OK · Novamira OK · Eventbrite OK · Constant Contact FAILED (auth) · Canva OK
```

If a connector fails, mark only the tasks that need it `blocked`
(`blocked_by: <connector> preflight`), run everything else, and report the
failure at the top of the review packet. Exceptions that stop the whole run:
Google Drive failing, or the Eventbrite token file missing.

Re-run a single check only if that connector errors mid-project.

## Project state

All state lives in Google Drive, in the project file. `systems/project-store.md`
is the only place that says how it is opened, created, written at
checkpoints, filled (and what goes stale), renamed, and indexed. Read it
before the first Drive call of a session. Load each other connector's tools
in one call when its first task starts.

## Starting a project

1. Open the store (`project-store`): load the Drive tools, read `index.md`.
2. Read the playbook for the project type: `playbooks/<type>.md`.
3. Run Preflight.
4. Run `existing-check` now, so the slug and folder use the live systems'
   values and every creating task knows what already exists.
5. Create the project (`project-store`): the folder, `project.md` from the
   template, the `index.md` row.
6. Fill every field from the playbook's field table, into the `values` block
   or FACTS as the store says.
7. Write the task list: only in-scope tasks, with `needs` and `uses`
   resolved to concrete names (`project-store`, Tasks); record the
   existing-check result on its task, `done`.
8. Run the draft pass: every task whose `needs` are done. Use subagents for
   independent drafts (copy, emails, social) where it saves time.
9. Present the review packet. Set project status `review`.

## Copy

The approved copy is written once, in `descriptions/<project>.html`, by the
`description-copy` task. Every channel takes from it, by the parts
`description-copy` defines, and lists `copy` in its `uses` so a redraft
marks it stale. Never write new event facts for a channel. Voice, the gap
marker, and the copy checks live in `description-copy`.

## Concurrency

Two projects can be live at the same time, sharing one Zoho form, one website,
and similar names.

1. Never copy a link, an id, or a value from another project file. Read it
   from the live system or from this project's values block.
2. Before an execute action writes a link or an id, confirm it against this
   project's record: the `jfid` matches this project's Zoho record id, the
   Eventbrite id matches this project's event.

## Blocked tasks

A task marked `blocked` gets **one** retest per session: the cheapest check
that proves or clears the blocker, and nothing else. Never chase a second
theory for a blocker the project file already diagnosed.

Network blocks: one `curl` to the host, then read
`$HTTPS_PROXY/__agentproxy/status` and check `recentRelayFailures`. A 403
policy denial on CONNECT means the host is off Cowork's egress allowlist. That
is not a credentials problem — do not go looking for tokens, do not retry the
API, do not try an alternate host or a proxy. Report it and stop that task.

If a blocker is cleared, fill the value it was holding, run the staleness rules
for that value, and continue with the tasks it unblocked.

## Universal rules

- **Verify a value against the system that holds it.** When a value names a
  date, time, venue, or link that also exists in a published system, check it
  there. The `existing-check` task does this at intake. The
  request is what was asked for; the published system is what exists.
- Read the tool before you write input for it: the script, the README, or one
  working command first.
- Never assume a plugin, module, or feature is active. Check.
- The system writes no message to staff or any other person. What the
  operator needs is in the review packet and the STATUS block.
- Search before you create. `existing-check` searches every system the
  playbook creates in, once, at intake; a component creates only where that
  record says `none`.
- **A write whose result you did not see is not a failed write.** When a call
  times out, errors after sending, or returns something you cannot read, never
  repeat it. Search the target system for the object you were creating. Act on
  what you find: nothing means retry, one means record its id and move on, two
  means report the duplicate and stop that task.
- Do not explore. Every tool call answers a question the procedure asked.

## Subagents

Only for independent drafts. A subagent writes only to its own file in
`drafts/`, never to the project file, and never does a Level 2 action.

## Capturing new rules

When a run produces a lesson, classify it before writing it down: project
fact (stays in the project file), project-type rule (playbook), tool fact
(component), universal rule (this file), or constraint rule (names its
constraint, placed with the work it constrains). Write the rule with its
trigger. Place it in one home, delete the text it supersedes in the same
session, and check in-flight project files against it.

## Project types

| Type | Playbook |
|---|---|
| Event (job fair, recruitment, hiring, webinar, workshop) | `playbooks/event.md` |
| Training promotion | `playbooks/training-promotion.md` |

Project files made by older versions of this skill are repaired on open by
the rules in `project-store`.

Job alerts, weekly newsletter, job board update, and employer emails are not
written yet. Do not improvise one; run the project by hand and record the
lessons, then write the playbook.

An email request about an event or training (a new draft, a reminder, a
resend, a correction) belongs to that project: resume it and work its email
task by `constant-contact-email`. An email request with no project behind it
is a new project of the matching type. The system drafts email; it never
sends or schedules one.

## Resuming a project

Trigger: "approve", "approve, but …", an answer to a review question, "resume
X", "status on X". Do exactly these steps, in order. Do not explore first.

1. Open the project (`project-store`): Drive tools, `index.md`, the folder,
   `project.md`, once.
2. Read only the components for tasks that are not `done` or `skipped`.
3. Run Preflight for the connectors those remaining components need.
4. Act on the message: an approval runs the execute pass; changes are applied,
   then execute runs; an answer fills a value and finishes the draft pass;
   a status request gets three lines (what is done, what is waiting, on whom).
5. Write one LOG row for the resume plus any status that changed, in one
   write.

## Closing a project

Trigger: the operator says "close X". Confirm the event date has passed.
Move every deliverable into the project folder. Move each DECISIONS row that
is not a project fact to its home file and delete it from the project file.
Set the project status to `closed` (`project-store` mirrors it to
`index.md`).

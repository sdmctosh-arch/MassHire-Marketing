# Component — description-copy

Access: Google Drive only. Level 1: the copy is a private file until a
channel publishes it. Runs in the draft pass, before every task that takes
from it.

The copy is the one public description of the project. It is written once,
to `descriptions/<project>.html`, and every channel takes from it: the
Eventbrite description is the whole file; the emails, the flyer, the website
entries, and the social post each take the parts named in their own
component. No channel writes a fact the copy does not hold.

## Inputs

Every fact in FACTS and the values block, the `event_kind` (or training
`path`), and the request. Facts come only from the request, a default, a
derivation, or a lookup, each already recorded with its source. Nothing is
invented here.

## The parts

The file holds six parts, in this order. Each part is one
`<div data-part="<name>">…</div>` block of `<p>` elements. The parts carry no
visible heading: the file reads as prose on the public page, and a channel
takes a part by its name.

| Part | Holds |
|---|---|
| `headline` | The event or program name. |
| `summary` | One sentence: what this is and who it is for. |
| `details` | Date, time, and location; for an online event, the platform. For a training: start date, schedule, location, cost, application deadline, each only when a source gives it. |
| `audience` | Who may come (the `audience` fact; cost when free), and what is still to be announced. |
| `bring` | What to bring or what to expect (`what_to_bring`, or the topic for a webinar or workshop). |
| `body` | Everything else the facts support, as short paragraphs. May be empty for a short event. |

## Content by kind

| Kind | The copy says |
|---|---|
| Job fair | The sectors (`sectors`), never employer names; that the registration page will be updated as employers confirm. |
| Recruitment, hiring | `hiring_employer` and the kind of work (`job_name`); the positions, when given. |
| Webinar | What attendees will learn; the platform; "no account required" only if a source says so. |
| Workshop | What attendees will learn or do; the location and the topic. |
| Training | What the training leads to; the eligibility requirements when a source states them (they are public); the `cost` fact as the playbook records it. |

## Voice

- **Natural and direct.** Short sentences, active voice.
- **Warm, not promotional.** No hype words ("amazing opportunity", "don't
  miss out", "exciting").
- **Plain language.** No workforce-development jargon (WIOA, CTI, RESEA)
  unless the audience already knows it. Spell out or skip acronyms.
- **One call to action.** Register, or apply. Not both, not twice.
- **No promise a third party controls.** Write what may happen, never what
  an employer, a platform, or a program will do.

## The gap

A missing Required fact does not stop the copy. Where the fact goes, write
the marker, exactly in this form:

```
[<fact> — awaiting your answer]
```

for example `[end time — awaiting your answer]`. The gap is not a fact: never
write a guess beside it, and never derive another value from it. When the
answer arrives, the value fill marks this task `stale` by the staleness rule
(the copy `uses` every fact); the redraft replaces the marker, and the new
save marks every taker stale through the `copy` value. A gap never reaches a
public item: every publishing component checks for the marker text.

## Process

1. Collect every fact with its source. Decide the kind's content from the
   table above.
2. Write the six parts. A subagent may do this step, writing only
   `drafts/description.html`; it never writes the project file or
   `descriptions/`.
3. Run the checks below on the draft, in the main thread.
4. Save the passing text to `descriptions/<project>.html` (`text/html`, by
   the write rules in `project-store`). Record the task's `output` as the
   file path and the part names found in it, in order
   (`descriptions/<project>.html: headline, summary, details, audience,
   bring, body`). Fill the `copy` value with the file's Drive id. A new id on a redraft marks every task that lists `copy` in
   `uses` stale.
5. The review packet shows the copy as prose (item 5), without the part
   markers.

## Revising

Any change to the copy — a filled gap, "approve, but change the wording", a
corrected value — is a redraft: write the full new file, run the checks,
save, trash the old file, fill `copy` with the new id. Never patch a part in
a channel instead of the copy.

## Checks

- [script] All six parts are present, in order, each non-empty except
  `body`.
- [script] Every Required fact of the playbook either appears in the copy or
  is gapped with the exact marker form.
- [script] Every date, time, venue, address, platform, and link in the copy
  equals the values block.
- [judgement] Every other statement traces to a fact in FACTS or the
  request; nothing is invented.
- [judgement] The kind's content rules are met.
- [judgement] Voice: plain, warm, no hype words, no unexplained acronyms,
  one call to action.
- [judgement] No promise a third party controls.

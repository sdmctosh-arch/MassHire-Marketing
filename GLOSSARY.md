# masshire-projects

The MassHire Central Career Centers marketing skill: it runs a project from
request to deliverables with one review gate, and never sends or schedules.

## Language

**Copy**:
The one public description of a project, written once by the
`description-copy` task; every channel takes from it and writes no fact it
does not hold. Also the `copy` value, which a redraft changes so every taker
goes stale.
_Avoid_: description (Eventbrite's field), text, blurb

**Part**:
One of the six named blocks of the copy, in order: headline, summary,
details, audience, bring, body. A channel takes a part by name; it never
re-cuts the copy by judgement.
_Avoid_: section, field

**Gap marker**:
The text written into the copy where a missing Required fact goes, exactly
`[<fact> — awaiting your answer]`. It is not a fact: nothing is guessed
beside it or derived from it, and no public item may contain it.
_Avoid_: placeholder, TODO

**Existing-check**:
The intake task that searches every system the playbook creates in and
records, per target, the matched object or none. The live system is what
exists; a creating task never searches on its own.
_Avoid_: dedupe, lookup (that is a field source)

**Project store**:
The Google Drive folder tree that holds every project file and the index,
and the one set of rules for opening, creating, writing, filling, and
renaming a project. The Cowork filesystem holds nothing between sessions.
_Avoid_: storage, Drive (when the rules are meant, not the service)

**System**:
A skill layer: how a system that is not one task is used, shared by every
task that touches it (`systems/<system>.md`). The project store is one.
_Avoid_: service, integration, backend

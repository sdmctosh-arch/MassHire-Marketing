# Glossary

Domain terms for the `masshire-projects` skill. A term here has one meaning
in every file; when a file needs a different word, it needs a different
entry.

## Copy

The one public description of a project, written once by the
`description-copy` task to `descriptions/<project>.html`. Every channel
(Eventbrite, email, flyer, website, social) takes from it and writes no fact
it does not hold. Also a value: `copy` in the project file's values block is
the file's Drive id, so a redraft marks every taker stale.
_Avoid_: description (that is Eventbrite's field), text, blurb.

## Part

One of the six named blocks of the copy, in order: `headline`, `summary`,
`details`, `audience`, `bring`, `body`. Each is a `<div data-part="…">` with
no visible heading. A channel takes a part by name; it never re-cuts the
copy by judgement.
_Avoid_: section, field.

## Gap marker

The text written into the copy where a missing Required fact goes, exactly
`[<fact> — awaiting your answer]`. It is not a fact: nothing is guessed
beside it or derived from it. Filling the fact redrafts the copy, and no
public item may ever contain the marker text.
_Avoid_: placeholder, TODO.

# Component — flyer-from-template

Access: Python in the Cowork workspace (QR code) and the Canva MCP connector
(upload, autofill, export). Level 1 throughout: a Canva design is private.
All three tasks — `flyer-qr`, `flyer`, `flyer-export` — run in the draft pass,
in that order. Tested 2026-09-28.

## Brand templates

| Template | id | Use for |
|---|---|---|
| MH Event - Job Fair | `EAHVMCIGhbU` | Job fairs and multi-employer events |
| MH Event - Job Listings | `EAHVM0kapR4` | Single-employer recruitment and hiring events |

Job Fair fields: `event_name`, `body`, `when_value`, `location`, `address`,
`cta_url` (text), `cta_qr` (image).

Job Listings fields: `event_type`, `company`, `job_name`, `body`,
`when_value`, `location`, `address`, `cta_url`, `partner_logo`, `cta_qr`,
plus three position rows — `position_1` / `location_1` / `salary_1` through
`_3`.

Always confirm the field list with `get-brand-template-dataset` before
filling. Never hard-code field names from this table into a call.

## flyer-qr

1. Library: `qrcode[pil]` and `pyzbar`. Install if missing:
   `pip install "qrcode[pil]" pyzbar --break-system-packages`.
2. Target URL: `jobseeker_link`, the Eventbrite event URL. It is known as
   soon as the Eventbrite draft exists and does not change on publish, so the
   QR never depends on a redirect.
3. Settings: error correction M, `box_size` 20, `border` 4. Never use a border
   below 4; scanners need the blank margin.
4. Make two files in `/mnt/user-data/outputs/`:
   - `<project-slug>-qr.png` (about 740×740 px), for Canva.
   - `<project-slug>-qr.svg` (`qrcode.image.svg.SvgPathImage`), for print.
5. Decode the PNG with `pyzbar`. The decoded text must exactly equal the
   target URL. If it does not, stop the flyer tasks and report it.
6. Upload the PNG to Canva:
   - Call `create-upload-url`.
   - Post the raw bytes:
     `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @<file> "<uploadUrl>"`
   - The response is `{"mediaId": "..."}`. Record it as the `asset_id` for
     `cta_qr`.
   - Each upload URL works once and expires after about 30 minutes. Get a new
     one for every attempt, including retries.
   - Never use `upload-asset-from-url`: it needs a public URL, and generated
     files have none.
   - curl fails with `(56) ... 403` or CONNECT rejected: canva.com is off the
     allowed domains. Mark the flyer tasks `blocked` with that reason and
     continue the run. Uploading from the operator's computer hits the same
     block.
7. Save both QR files to `flyer/` in the project folder.

## flyer

1. Call `get-brand-template-dataset` for the template.
2. Collect every field value first:
   - `cta_url`: `jobseeker_short_link` without its `https://`
     (`masshirecentralcc.com/<slug>`), for people who type the address. The
     QR carries the Eventbrite URL.
   - `cta_qr`: the `asset_id` from `flyer-qr`.
   - `when_value`, `location`, `address`: from the values block.
   - `body`: the copy's `summary` part, then its `audience` part (for a
     job fair, that carries "updated as employers confirm").
   - Job Listings: `event_type`, `company`, `job_name` from the event name;
     the position rows from `positions`; `partner_logo` from the Canva asset
     lookup. Send an empty string for every field of an unused position row,
     then check the thumbnail for a leftover label or an empty box.
3. Call `autofill-design` once, with every value, and the title
   `<Event Name> Flyer - YYYY-MM-DD`. Every call creates a new design, and any
   field left out comes back blank. Autofill once, with everything.
4. Check the result thumbnail: no wrapped, clipped, or overflowing text; no
   leftover placeholder text in unused position rows or an empty logo frame.
   Flag any problem in the review packet with the thumbnail; do not stop.
5. Record the design id and design link in the task.

If the operator asks for a flyer change at review, autofill again with the
corrected values (a new design), re-export, and record the new design; the
old one is left as is.

## flyer-export

1. Design id: from the autofill result (or the 11-character id starting with
   `D` after `/design/` in the design URL, e.g. `DAGKFvurv_0`).
2. Call `get-export-formats`, then `export-design` once per format: PNG
   (WordPress `flyer` field) and PDF (print).
3. Download each returned URL with `curl` into `/mnt/user-data/outputs/`.
4. Save both files to `flyer/` in the project folder, and present them to the
   operator with the review packet (in Cowork, with SendUserFile).
5. If the `wordpress-event` draft already exists, add the PNG to it now
   (see `wordpress-event`, Process step 2).

## Tool facts

- **Brand templates cannot be edited in place.** The connector's Canva token
  lacks `brandtemplate:content:write`. To change a template: make an ordinary
  design from it, edit and commit that, then publish it over the brand
  template in the Canva UI.
- **The typeface cannot be set through the connector.** Text the connector
  adds (not autofill) comes out in Canva's default face; its font is fixed by
  hand. Autofilled fields keep the template's font.
- **Placeholder-sized text boxes.** A template's text box may be sized to its
  placeholder word. When a field wraps into a narrow column, fix the template
  (see above); do not resize per run.

## Checks

- [script] The QR decodes to this project's `jobseeker_link` exactly.
- [script] `cta_url` shows this project's `jobseeker_short_link` without
  its `https://`, character for character otherwise.
- [script] Date, time, venue, and address on the design match the values
  block.
- [judgement] The thumbnail shows no wrapped or clipped text, and the layout
  is readable at print size.
- [script] No `awaiting your answer` on the design.
- [judgement] The text matches the copy.

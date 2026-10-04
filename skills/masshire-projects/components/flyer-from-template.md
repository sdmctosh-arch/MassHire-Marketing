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

Webinars, workshops, and trainings have no template and get no flyer.

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
2. Target URL: `jobseeker_short_link`. It must be the same URL `cta_url`
   shows. (The redirect is created at execute; the QR encodes the text now.)
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
   - `cta_url`: `jobseeker_short_link` as readable text, never the Eventbrite
     URL.
   - `cta_qr`: the `asset_id` from `flyer-qr`.
   - `when_value`, `location`, `address`: from the values block.
   - `body`: from the copy. Job fair: name the sectors, never employers.
   - Job Listings: `event_type`, `company`, `job_name` from the event name;
     the position rows from `positions`; `partner_logo` from the Canva asset
     lookup.
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
   (social image, WordPress `flyer` field) and PDF (print).
3. Download each returned URL with `curl` into `/mnt/user-data/outputs/`.
4. Save both files to `flyer/` in the project folder, and present them to the
   operator with the review packet (in Cowork, with SendUserFile).
5. Record the PNG export URL on the task for `facebook-post-draft`; it
   expires, so the social draft is created in the same session.

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

- [script] The QR decodes to `jobseeker_short_link` exactly, and `cta_url`
  shows the same text.
- [script] Date, time, venue, and address on the design match the values
  block.
- [judgement] The thumbnail shows no wrapped or clipped text, and the layout
  is readable at print size.
- [judgement] The copy makes no promise a third party controls.

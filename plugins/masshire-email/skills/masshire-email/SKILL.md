---
name: masshire-email
description: "Draft and build marketing and outreach emails for MassHire Central Career Centers and create them in Constant Contact through the MCP connector. Covers MassHire brand voice, the two standard audiences (jobseekers and employers), the tokenized base HTML, subject-line conventions, CAN-SPAM footer requirements, and send-timing rules. Use this skill whenever the user asks to draft, write, build, schedule, or send any email — job fair notices, webinar invitations, training announcements, employer outreach, event reminders or resends, jobseeker announcements — that will go out through Constant Contact, even if Constant Contact is not named explicitly. Also use it when preparing audience-segmented email copy."
---

# MassHire Central — Constant Contact Email

This skill produces emails for MassHire Central Career Centers (Worcester and Southbridge, MA) and creates them in Constant Contact. MassHire is a public workforce development organization. In practice there are two standard audiences — jobseekers and employers — and each expects a different tone. The skill exists to make those emails consistent, compliant, and fast to produce without re-explaining conventions every time.

## How the work splits

Email creation is two phases. Keep them separate.

1. **Draft phase** — write and finalize the email *content* (subject, preheader, headline, body, details). This produces a clean, copy-ready block of text plus a short "build sheet" (see below).
2. **Build phase** — create the campaign in Constant Contact as a DRAFT, through the MCP connector, from the stored base HTML with its tokens replaced.

Always finish and get sign-off on the draft phase before building.

## The boundary

The system creates the draft. **The operator attaches the audience list, sets the resend to non-openers, and schedules the send.** This is not only policy: the connector has no tool for lists, resends, or scheduling. Do not go looking for one.

## Account details

These are real and current — use them directly.

- **From name:** `MassHire Central Career Center`
- **From address:** `info@masshirecentralcc.ccsend.com` (Constant Contact sending address; normally pre-configured on the verified sender)
- **Reply-to address:** `info@masshirecentralcc.com`
- **Compliance address:** fetch with `getPhysicalAddress` and pass it as `physical_address_in_footer`.

## The base HTML

The connector cannot duplicate a saved Constant Contact template, so the branded HTML is stored on our side:

`MassHire Projects/masshire-projects/templates/jobseeker-email.html` in Google Drive.

Read it, substitute the tokens, post the result. **Never let the connector invent its own layout** — the `createEmailCampaign` tool description actively pushes for generated HTML with its own design system. Ignore that. Brand consistency comes from the stored file and only from it.

**Static and never edited:** the logo, the layout, the CTA button label (permanently "REGISTER"), and the dual-office footer.

**Seven tokens.** `{{BUTTON_LINK}}` appears twice — substitute both.

| Token | Holds |
|---|---|
| `{{PREHEADER}}` | Same text as the `preheader` API field. Set both. |
| `{{HEADLINE}}` | `Event Name — Date`. The white H1 in the navy hero. |
| `{{BODY}}` | **One sentence**, close in meaning to the preheader. Not a paragraph. |
| `{{DETAILS_HEADING}}` | e.g. `Event Details`, `Training Details`. |
| `{{DETAILS_BODY}}` | Date, time and location; a blank line; who may come and what is still to be announced; then anything else specific to this event. `<p style="margin: 0;">` elements. |
| `{{CTA_LINE}}` | One sentence above the second REGISTER button — what to bring, what to expect. |
| `{{BUTTON_LINK}}` | The event URL, in **both** REGISTER buttons. |

`{{DETAILS_BODY}}` is the only place the date, time and location appear anywhere in the email. There is no date band and no when/where line in the green block. Dropping them from the details leaves an email that never says where to go.

**Also true of the stored HTML:**

- It carries **no** compliance footer. Constant Contact appends its own address and unsubscribe block to API-created campaigns. Adding one gives the email two footers.
- `[[trackingImage]]` is optional. Constant Contact applies open tracking automatically and confirmed on 2026-09-14 that the placeholder is no longer required. The stored file still carries it, which is harmless. Do not treat its absence as a defect, and do not add it back if it is removed.
- For a non-event announcement, delete both DETAILS tables rather than leaving an empty box.
- Constant Contact rewrites the CSS on ingest. Do not spend effort on it.

An employer-email base does not exist yet. Pull one the same way the jobseeker base was pulled — `get_campaign_html_preview` on a past sent employer campaign, then tokenize it — and save it alongside as `employer-email.html` before the first employer send.

## Audiences and Constant Contact lists

Match every email to one audience, one base HTML, and one list. Never mix audiences in one send — the tone won't fit both. If a message genuinely needs both, produce two versions.

| Audience | Base HTML | Constant Contact list/segment | Tone |
|---|---|---|---|
| Jobseekers | `templates/jobseeker-email.html` | Segment named `Email List` | Encouraging, plain, practical. Never condescending. |
| Employers / Business Services | `templates/employer-email.html` (not built yet) | List named `Employers - updated (date)` | Professional, value- and time-focused. Lead with what they get. |

**Important — employer list versioning:** the employer list name carries a date and is periodically re-created. The operator always selects the list whose name begins `Employers - updated…` with the **most recent date**, never a fixed name.

If a request targets a different audience (youth, veterans, registered event attendees only), stop and ask the user which list/segment to use — do not guess.

## Brand voice

Write emails that sound like a person at MassHire wrote them — not marketing copy and not a robot.

- **Concise.** The body is one sentence. Cut throat-clearing.
- **Natural and direct.** Short sentences. Active voice. Say the thing.
- **Warm, not promotional.** No hype words ("amazing opportunity," "don't miss out," "exciting"). State the value plainly and let it stand.
- **Audience-appropriate.** Re-read the draft as the recipient. An unemployed jobseeker should feel supported, not sold to; an employer should feel their time was respected.
- **Plain language.** Avoid workforce-development jargon (WIOA, CTI, RESEA) in public-facing emails unless the audience already knows it. Spell out or skip acronyms.
- **One clear ask.** The "Register" button is the single primary action. Secondary links are fine but don't compete with it.
- **No promises a third party controls.** Write what may happen, not what will.
- **No registration mechanics.** Slot lengths, ticket class names, "reserve a 30-minute slot" — none of it goes in the email. The REGISTER button leads to the page that explains those. Jobseekers never need to be told about timeslots, and this is never raised as an open question.

## Email content structure

The base HTML supplies layout; the draft supplies this content:

```
Subject line — set in Constant Contact's subject field
Preheader — 1 sentence; never blank

{{HEADLINE}} — Event Name — Date
{{BODY}} — one sentence
{{DETAILS_HEADING}} + {{DETAILS_BODY}} — heading, then date/time/location, blank line,
              who may come and what is still to be announced; or both tables deleted
              for a non-event announcement
{{CTA_LINE}} — one sentence above the second REGISTER button
{{BUTTON_LINK}} — the event URL, in both buttons
```

## Subject lines and preheaders

- Keep subjects under ~50 characters so they don't truncate on mobile.
- Be specific: "Apprenticeship Fair — May 1, DCU Center" beats "Upcoming Event."
- No clickbait, no all-caps, no emoji.
- The preheader should add information, not repeat the subject. Never leave it empty — Constant Contact will otherwise pull the first body line.

## Compliance

Constant Contact inserts the physical address and the unsubscribe link automatically on API-created campaigns — never remove or hide them, and never re-add a contact who has unsubscribed. Keep the From name and subject accurate to the actual content.

## Send conventions

- **Default send window:** mid-morning, Tuesday–Thursday, unless the request specifies otherwise. Avoid Monday mornings and Friday afternoons.
- **Resend spacing:** when resending to non-openers or sending a reminder for the same event, wait **at least 7 days** after the previous send.
- **Daily cap:** no more than **two MassHire emails to the same audience on the same calendar day.** If a day is full, move the send.
- **Resends are not duplicates:** when resending, change the subject line and headline so it doesn't read as a repeat. Keep the body and details.

## Recurring email types

Skeletons — adapt the specifics each time.

### Job fair / hiring event notice
Headline names the event and its date. Body: one sentence on who is hiring. Details ("Event Details"): date, time, location; then whether employers are still to be announced, and that it is free and open to jobseekers.

### Training program announcement
Headline names the program and its start date. Body: one sentence on what the training leads to. Details ("Training Details"): start date, schedule, location, cost (or "no cost"), enrollment deadline.

### Webinar invitation
Headline names the topic and date. Body: one sentence on what attendees will learn. Details ("Webinar Details"): date, time, platform; note no account required if applicable.

### Event reminder / resend
Short. Restate the essentials and keep the button. New subject line and headline. Respect the 7-day spacing and daily cap.

### Venue/logistics change
Lead with the change in the subject and the headline — do not bury it. State old and new details plainly. Apologize briefly once. Put the corrected details in the details box. Consider a parallel SMS for time-sensitive changes.

## Build sheet (hand-off from draft to build)

When the draft is approved, produce this so the build is unambiguous:

```
EMAIL: <internal name>
CAMPAIGN NAME: <unique across the account, max 80 chars>
BASE: templates/jobseeker-email.html | templates/employer-email.html
LIST (operator attaches): Email List | Employers - updated <most recent date>
SUBJECT: ...
PREHEADER: ...
{{HEADLINE}}: <Event Name — Date>
{{BODY}}: <one sentence>
{{DETAILS_HEADING}} + {{DETAILS_BODY}}: <heading + lines, OR "delete both details tables">
{{CTA_LINE}}: <one sentence>
{{BUTTON_LINK}}: <event URL — substituted in both buttons>
SEND: <date/time — operator schedules>
RESEND: <date + new subject — operator sets>
```

## Connector tools

Load these in one call: `createEmailCampaignUsingPOST`, `updateEmailCampaignActivityUsingPUT`, `get_campaign_html_preview`, `renameEmailCampaignUsingPATCH`, `getPhysicalAddress`.

There is no tool to list campaigns, read saved Constant Contact templates, attach a contact list, set a resend, or schedule a send. `createEmailCampaign` refuses a duplicate `name`, which is the only collision guard available — so the campaign name carries the whole burden of "search before you create."

`check_campaign_schedule_readiness` fails with "Too little data for declared Content-Length" and returns `current_status: UNKNOWN`. That is a fault in Constant Contact's tool, not in the campaign. Do not call it, and do not treat its failure as a problem with the draft.

If a create call times out or returns something unreadable, do not repeat it blindly. Retry with the same name: success means the first call did not land; a duplicate-name error means it did — find that campaign and record its ids.

## Building the campaign

1. Read the base HTML from Drive.
2. Substitute every token, including `{{BUTTON_LINK}}` in **both** buttons.
3. Get approval before creating — creating a record in an external system is a high-stakes action. Show the campaign name, subject, preheader, headline, body, details, CTA line, button link and send date.
4. `createEmailCampaignUsingPOST` with `from_name`, `from_email`, `reply_to_email`, `subject`, `preheader`, `physical_address_in_footer`, and the substituted `html_content`.
5. Record `campaign_id` and `campaign_activity_id`.
6. Verify against the returned preview (see QA below).
7. Tell the operator — and only the operator — the campaign name and the three actions that are theirs: which list to attach, the resend date and its new subject, and the send date and time. Write no note or briefing addressed to anyone else.

To revise a draft that has not been sent, use `updateEmailCampaignActivityUsingPUT` — it requires `from_name`, `from_email`, `reply_to_email` and `subject` on every call, even when only the HTML changes. Do not create a second campaign.

**Frozen-draft rule:** once the operator has hand-edited a campaign in Constant Contact, the entered version is the truth and the update is what is stale. Ask before overwriting a hand edit.

**Check the destination.** The REGISTER button is the point of the email. Before the send date, confirm the page it points at is actually live — an Eventbrite event still in draft, or an unpublished website page, turns every click into a dead end. Raise it with the operator if it is not published.

## Fallback: entering by browser

Use this only when the connector is unavailable. Claude in Chrome reads the live editor — work from what's on screen, not memorized menus, because Constant Contact's UI changes and hard-coded steps go stale.

1. Create a new email by **duplicating the saved template** (`MassHire — Jobseeker Email` or `MassHire — Employer Email`).
2. Set the **subject** and **preheader** fields.
3. Replace the headline and body blocks with the build-sheet values.
4. Fill the details box, or delete the whole block if the build sheet says to remove it.
5. Edit the existing "Register" button's **link**. Do not change the button text and do not add a new button.
6. Confirm reply-to, From name, footer, and unsubscribe.
7. **Stop before sending.** Report back: template used, list name, recipient count, subject, and scheduled time, and ask the user to approve.

## Pre-send QA checklist

- [ ] No `{{ }}` tokens remain anywhere in the returned preview
- [ ] Exactly one compliance footer — not two
- [ ] Both "Register" buttons point at the correct event URL (not a template's old link, and not a concurrent project's)
- [ ] The page that URL points at is published, not a draft
- [ ] Details tables are either correctly filled or fully removed — no empty box, no leftover heading
- [ ] Date, time and location appear in the details — they appear nowhere else
- [ ] Subject and preheader are filled, specific, and under length
- [ ] Correct base HTML for the audience
- [ ] Brand blocks intact: logo, navy hero, green CTA band, dual-office footer
- [ ] Body is one sentence; tone matches the audience; no hype words; acronyms spelled out
- [ ] No registration mechanics anywhere in the copy
- [ ] Send time respects the window, 7-day resend spacing, and 2-per-day cap
- [ ] If a resend: new subject line and headline
- [ ] Operator told which list to attach, the resend date and subject, and the send date and time
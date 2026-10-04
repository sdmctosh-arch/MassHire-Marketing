# Component — constant-contact-email

Access: creates email campaign drafts in Constant Contact through the MCP
connector, in the draft pass. Level 1: a draft sends nothing.

Boundary, permanent: the system never sends and never schedules. It sets no
send date, send time, resend, or list. The operator attaches the audience
list, sets any resend, and schedules each draft. This is not only policy: the
connector has no tool for lists, resends, or scheduling. Do not go looking
for one.

## Inputs

The copy in `descriptions/<project>.html`; the values the project type
supplies (event: event_date, start_time, end_time, venue, jobseeker_link;
training: public_link); the email draft count and roles from the playbook.

## Account details

Real and current; use them directly.

- From name: `MassHire Central Career Center`
- From address: `info@masshirecentralcc.ccsend.com` (the verified Constant
  Contact sending address)
- Reply-to address: `info@masshirecentralcc.com`
- Compliance address: fetch with `getPhysicalAddress` and pass it as
  `physical_address_in_footer`.

## The base HTML

The connector cannot duplicate a saved Constant Contact template, so the
branded HTML is stored in Drive:
`MassHire Projects/masshire-projects/templates/jobseeker-email.html`.

Read it, substitute the tokens, post the result. Never let the connector
invent its own layout: the `createEmailCampaign` tool description pushes for
generated HTML with its own design system. Ignore that. Brand consistency
comes from the stored file and only from it.

Static, never edited: the logo, the layout, the CTA button label
(permanently "REGISTER"), and the dual-office footer.

Seven tokens. `{{BUTTON_LINK}}` appears twice; substitute both.

| Token | Holds |
|---|---|
| `{{PREHEADER}}` | Same text as the `preheader` API field. Set both. |
| `{{HEADLINE}}` | `Event Name — Date`. The white H1 in the navy hero. |
| `{{BODY}}` | One sentence, close in meaning to the preheader. Not a paragraph. |
| `{{DETAILS_HEADING}}` | `Event Details`, `Training Details`, `Webinar Details`. |
| `{{DETAILS_BODY}}` | Date, time and location; a blank line; who may come and what is still to be announced; then anything else specific to this project. `<p style="margin: 0;">` elements. |
| `{{CTA_LINE}}` | One sentence above the second REGISTER button: what to bring, what to expect. |
| `{{BUTTON_LINK}}` | jobseeker_link (event) or public_link (training), in both REGISTER buttons. |

`{{DETAILS_BODY}}` is the only place the date, time and location appear in
the email. There is no date band and no when/where line in the green block.

Also true of the stored HTML:

- It carries no compliance footer. Constant Contact appends its own address
  and unsubscribe block to API-created campaigns. Adding one gives the email
  two footers.
- `[[trackingImage]]` is optional (Constant Contact confirmed 2026-09-14 that
  open tracking is automatic). Its presence or absence is not a defect.
- Constant Contact rewrites the CSS on ingest. Do not spend effort on it.

## Audience and list

Every playbook email goes to jobseekers: base `jobseeker-email.html`, list
segment `Email List`, attached by the operator. The tone is encouraging,
plain, and practical, never condescending.

No playbook drafts employer emails, and no employer base HTML exists. Do not
improvise one (see Project types in SKILL.md). Tool fact for when one is
written: the employer list is named `Employers - updated <date>` and is
re-created periodically; the operator attaches the one with the most recent
date.

## Copy rules

Each draft takes its facts from the approved copy in `descriptions/`. These
rules shape how that copy is cut down for email.

- **Concise.** The body is one sentence.
- **Natural and direct.** Short sentences, active voice.
- **Warm, not promotional.** No hype words ("amazing opportunity", "don't
  miss out", "exciting").
- **Plain language.** No workforce-development jargon (WIOA, CTI, RESEA)
  unless the audience already knows it. Spell out or skip acronyms.
- **One clear ask.** REGISTER is the single primary action.
- **No registration mechanics.** Slot lengths, ticket class names, "reserve a
  30-minute slot": none of it goes in the email. The REGISTER page explains
  those.
- **Subject:** under about 50 characters, specific ("Apprenticeship Fair —
  May 1, DCU Center", not "Upcoming Event"), no clickbait, no all-caps, no
  emoji.
- **Preheader:** one sentence that adds to the subject rather than repeating
  it. Never blank.
- **Resend subject:** each draft records one, different from its subject, so
  a resend does not read as a repeat. The operator sets it in Constant
  Contact.

### Drafts by role

| Role | Headline | Body | Details |
|---|---|---|---|
| announce | Event or program name — date | Job fair: who is hiring (sectors, not employers). Recruitment/hiring: `hiring_employer` and the work. Webinar/workshop: what attendees will learn. Training: what the training leads to. | Full details box. |
| reminder | Same event, new wording | One sentence restating why to come. | Full details box. |
| last call | Same event, new wording | One sentence: the event is soon. | Full details box. |

Details by project type:

- Job fair, recruitment, hiring: date, time, location; then whether employers
  are still to be announced, and that it is free and open to jobseekers.
- Webinar: date, time, platform (`online_platform`); "no account required"
  only if a source says so.
- Workshop: date, time, location, and the topic.
- Training: start date, schedule, location, cost ("no cost" only when a
  source says it is free), application deadline.

A correction email (venue, date, or time changed after an email went out) is
drafted only when the operator asks for one: a sent email is a published
item. Lead with the change in the subject and the headline, state the old
and new details plainly, apologize once, and put the corrected details in the
details box.

## Process

1. Read the base HTML from Drive.
2. For each role in the playbook's count: write the content by the rules
   above, and substitute every token, `{{BUTTON_LINK}}` in both buttons.
3. `createEmailCampaignUsingPOST` with `from_name`, `from_email`,
   `reply_to_email`, `subject`, `preheader`, `physical_address_in_footer`,
   and the substituted `html_content`. No separate approval: the review
   packet is the approval.
4. Record `campaign_id` and `campaign_activity_id` on the task.
5. Run the checks against the returned preview.
6. Save the build copy to `campaigns/email-<n>.md` in the project folder:

   ```
   CAMPAIGN NAME: <Event Name> - YYYY-MM-DD - Email <n>
   ROLE: announce | reminder | last call
   CAMPAIGN ID / ACTIVITY ID: ...
   LIST (operator attaches): Email List
   SUBJECT: ...
   RESEND SUBJECT (operator sets): ...
   PREHEADER: ...
   HEADLINE: ...
   BODY: ...
   DETAILS HEADING / BODY: ...
   CTA LINE: ...
   BUTTON LINK: ...
   ```

   The build copy carries no send date, send time, or resend date.

Campaign name: `<Event Name> - YYYY-MM-DD - Email <n>`, the event date in ISO
form. Training: `<training_title> - YYYY-MM-DD - Email <n>`, the project date.
Unique across the account, at most 80 characters.

## Revising a draft

- When a value a draft uses changes, update the draft in place with
  `updateEmailCampaignActivityUsingPUT`. It requires `from_name`,
  `from_email`, `reply_to_email`, and `subject` on every call, even when only
  the HTML changes. Never create a second campaign.
- Frozen-draft rule: once the operator edits a campaign by hand in Constant
  Contact, the entered version is the truth. Ask before overwriting a hand
  edit. This is the one separate stop.

## Execute: the destination check

The REGISTER button is the point of the email. In the execute pass, after the
destination is published, confirm every draft's REGISTER buttons point at
this project's live link (event: jobseeker_link on the published Eventbrite
event; training: public_link). An Eventbrite event still in draft, or an
unpublished page, turns every click into a dead end. If a link is wrong,
update the draft in place (frozen-draft rule applies).

## Tool facts

- Load in one call: `createEmailCampaignUsingPOST`,
  `updateEmailCampaignActivityUsingPUT`, `get_campaign_html_preview`,
  `renameEmailCampaignUsingPATCH`, `getPhysicalAddress`.
- No tool lists campaigns, reads saved Constant Contact templates, attaches a
  list, sets a resend, or schedules a send.
- `createEmailCampaign` refuses a duplicate `name`. That refusal is the only
  collision guard, and it is the duplicate check after an unreadable create:
  retry with the same name; success means the first call did not land, a
  duplicate-name error means it did. Find that campaign and record its ids.
- `check_campaign_schedule_readiness` fails with "Too little data for
  declared Content-Length" and returns `current_status: UNKNOWN`. That is a
  fault in Constant Contact's tool. Never call it; it is a scheduling tool
  in any case.
- No browser fallback. When the connector fails, the task is `blocked` by
  the Preflight rules.

## Compliance

Constant Contact inserts the physical address and the unsubscribe link on
API-created campaigns. Never remove or hide them. The From name and subject
stay accurate to the content.

## Checks

- [script] Both REGISTER buttons link to this project's jobseeker_link
  (training: public_link), not a template's old link and not a concurrent
  project's.
- [script] No unresolved `{{ }}` tokens in the returned preview.
- [script] Exactly one compliance footer.
- [script] The number of drafts equals the playbook's count.
- [script] Details box filled; date, time, and location appear there and
  nowhere else.
- [script] Subject and preheader filled; subject under the length rule.
- [judgement] Subjects specific and distinct between drafts; each resend
  subject differs from its subject.
- [judgement] Body is one sentence; jobseeker tone; no hype words; acronyms
  spelled out; no registration mechanics; no promises a third party
  controls.
- [judgement] Brand blocks intact: logo, navy hero, green CTA band,
  dual-office footer.

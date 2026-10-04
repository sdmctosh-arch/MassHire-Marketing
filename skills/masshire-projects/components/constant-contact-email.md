# Component — constant-contact-email

Access: creates email campaign drafts in Constant Contact through the MCP
connector, in the draft pass. Level 1: a draft sends nothing.

Boundary, permanent: the system never sends and never schedules. The operator
attaches the audience list, sets any resend, and schedules each draft.

## Inputs

The copy in `descriptions/<project>.html`; the values the project type
supplies (event: event_date, start_time, end_time, venue, jobseeker_link;
training: public_link); the email draft count and roles from the playbook.

## Rules

- Everything about building an email — account details, base HTML, the seven
  tokens, voice, subject and preheader rules, connector tools, QA — comes
  from the `masshire-email` skill. Never restate it here. Its send conventions
  (days, times, spacing) do not apply: this skill never schedules.
- The `masshire-email` step "get approval before creating" is satisfied by
  this skill's review packet. Create the drafts in the draft pass without a
  separate approval.
- Create exactly the playbook's count, one per role (announce, reminder, last
  call). Each draft has its own content written for its role, a subject line,
  and a resend subject line (recorded in the build copy for the operator; the
  connector cannot set a resend).
- No draft carries a date or time.
- Campaign name: `<Event Name> - YYYY-MM-DD - Email <n>`, the event date in
  ISO form. The connector refuses a duplicate name; that refusal is also the
  duplicate check after an unreadable create.
- Save a copy of each draft's content (the build sheet from `masshire-email`,
  without SEND and RESEND dates) to `campaigns/` in the project folder.
- Frozen-draft rule: once the operator edits a campaign by hand in Constant
  Contact, the entered version is the truth. Ask before overwriting a hand
  edit. This is the one separate stop.
- When a value a draft uses changes, update the draft in place with
  `updateEmailCampaignActivityUsingPUT` (subject to the frozen-draft rule).

## Checks

- [script] The REGISTER button link, in both buttons, equals this project's
  jobseeker_link (training: public_link).
- [script] No unresolved {{ }} tokens.
- [script] The number of drafts equals the playbook's count.
- [judgement] Subjects under the length rule, specific, distinct between
  drafts; no promises a third party controls.

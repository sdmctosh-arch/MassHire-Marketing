---
name: test-skill
description: Run the masshire-projects behavior tests in tests/scenarios. Each scenario is played by one fresh subagent that sees only the skill and the scenario's message and world, and graded by a second fresh subagent that sees only the assertions and the transcript. Use when the user says "run the tests", "test the skill", or /test-skill, optionally naming one scenario.
---

# Test the masshire-projects skill

The skill under test is `plugins/masshire-projects/skills/masshire-projects/`.
Scenarios are `tests/scenarios/*.md`. Each has three sections: `## Message`,
`## World`, `## Assertions`.

Run every scenario, or only the ones the user named. Scenarios are
independent: run their players in parallel, then their graders in parallel.

## Rules that keep the test honest

- Separation. The player never sees the assertions. The grader never sees
  the skill and never plays the scenario. The main thread does neither: it
  only passes text between them and reports.
- Dry run. Nothing touches a live system. The player makes no connector,
  network, or Drive call; it simulates every call from the World section.
- No help. Do not add hints, rules, or summaries of the skill to the player
  prompt. If the skill is unclear, the test should show it.

## Steps

1. For each scenario, read the file and split it. Keep the Assertions text
   for step 3; give the player only Message and World.
2. Spawn the player (Agent, general-purpose) with this prompt, filling the
   two blocks verbatim:

   ```
   You are testing a Claude skill by playing it in a dry run.

   Read plugins/masshire-projects/skills/masshire-projects/SKILL.md and every
   playbook, component, or template it tells you to read for this message.
   Read nothing under tests/ and nothing outside that skill folder.

   Do not call any connector, MCP tool, network, or Drive tool. Every external
   call is simulated: the World below says what each system returns. If the
   World does not cover a call, say so and treat the result as empty.

   The operator's message:
   <<<MESSAGE>>>

   The world:
   <<<WORLD>>>

   Act exactly as the skill instructs for this message, then output, in this
   order and with these headings:

   ## Calls
   Every external call you would make, in order, one per line:
   `<pass: draft|execute> <system> <tool or endpoint> <key params> -> <simulated result>`

   ## Project file
   project.md as it stands at the end of this turn, in full.

   ## Reply
   The message you would send the operator (the review packet, or the
   execute report), verbatim.

   ## Notes
   Any place the skill was unclear or contradictory, and what you chose.
   ```

3. When the player returns, save its output to
   `tests/results/<scenario>.md` (the folder is git-ignored). Spawn the grader
   (Agent, general-purpose) with:

   ```
   You are grading a dry run of a Claude skill. You have only the assertions
   and the transcript below. Do not read any other file.

   For each numbered assertion, answer PASS, FAIL, or UNCLEAR, with a short
   quote from the transcript as evidence. FAIL needs the quote that breaks
   it, or the absence that breaks it. Judge only what the transcript shows;
   do not give credit for intent. Then one line: `Score: <passes>/<total>`.

   Assertions:
   <<<ASSERTIONS>>>

   Transcript:
   <<<PLAYER OUTPUT>>>
   ```

4. Append the grade to `tests/results/<scenario>.md`.
5. Report to the user: one table row per scenario (scenario, score, failed
   assertion numbers), then for each FAIL the assertion and the evidence,
   and any player Notes that point at an unclear rule. Do not change the
   skill in the same run; propose fixes and let the user choose.

# Behavior tests

`scripts/validate.py` checks the skill's structure. These tests check its
behavior: given a request, does the skill do what its rules say?

Each file in `scenarios/` is one test:

- **Message** — what the operator sends.
- **World** — what every live system would return (Drive, Eventbrite,
  WordPress, Zoho, Constant Contact, Canva). Nothing real is touched.
- **Assertions** — numbered, checkable outcomes.

## Running them

In a Claude Code session on this repo, say "run the tests" or `/test-skill`
(add a scenario name to run one). The `test-skill` project skill
(`.claude/skills/test-skill/`) runs each scenario with two fresh subagents:

1. A **player** reads only the skill, the Message, and the World, and plays
   a dry run: the calls it would make, the project file, and its reply.
2. A **grader** reads only the Assertions and the player's transcript, and
   marks each assertion PASS, FAIL, or UNCLEAR with evidence.

The player never sees the assertions, and the grader never sees the skill,
so neither can grade its own work. Transcripts and grades go to `results/`,
which is not committed.

Runs use your Claude plan, not an API key. They are not run in CI.

## When to run

After any change to how the skill behaves (a rule, a default, a task list,
an execute step). Not needed for wording-only fixes.

## Adding a scenario

Copy a scenario, change the Message and World, and write assertions that a
reader could check from the transcript alone. Prefer assertions about rules
that are easy to break: what may be asked, what is never set, what order
public actions run in. Keep World complete enough that the player does not
have to guess.

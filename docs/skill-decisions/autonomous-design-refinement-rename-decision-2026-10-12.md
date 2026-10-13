# autonomous-requirements-refinement renamed to autonomous-design-refinement (decision record, 2026-10-12)

Maintainer notes for the rename of `skills/autonomous-design-refinement/SKILL.md` and the matching activity tokens in `continuation-prompt` (Step 2, rule 3). **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before renaming either refinement skill or changing their chat-name tokens.

## The problem

Once `autonomous-prd-refinement` existed, two skills refined requirements, and the name `autonomous-requirements-refinement` no longer said which one it was. Chat names had the same problem: `continuation-prompt` gave this skill the token `refine`, so a tab reading `ph3b2 orderN refine` could be either stage.

## Options considered

1. **Keep the name.** Rejected: "requirements" now covers both skills, and the user had to remember which one it meant.
2. **`autonomous-readiness-refinement`**, after its goal (implementation-ready) and its driver (`implementation-readiness-check`). Rejected: accurate, but it does not pair with `autonomous-prd-refinement`, so the order of the two is not obvious from the names.
3. **Chosen: `autonomous-design-refinement`.** What separates the two skills is the stage: the PRD skill runs on a draft PRD before any design exists, and this one needs the technical design. Each is named for the document that gates its stage, giving PRD → PRD refinement → design → design refinement → implement. It still refines the PRD and assumptions as well as the design; the skill's opening says so.

## Calls made with it

- **Chat-name tokens are `PRD refine` and `TDD refine`.** Two words, an exception to the six-character token rule: the first proposal, `prdref` and `tddref`, read as *reference* at a glance. `TDD` is the user's own word for the technical design document.
- **The state file is renamed to match,** `{feature}-design-refinement-state.md`, pairing with the PRD skill's `{feature}-prd-refinement-state.md`. Keeping the old `{feature}-refinement-state.md` was rejected: it would have spared runs in progress under the old name (none was live when this changed; the old-named files left in some repositories are abandoned runs), at the cost of a name that does not say which skill owns it, for every run after.
- **The commit messages follow the name** (`design refinement pass {N}`, `design refinement complete`). `using-the-enso-method` reads the completion commit to tell the stage, so it accepts the old `requirements refinement complete` message too, for PRDs refined before the rename.
- **Dated research and decision records outside this repository keep the old name** where they record what was true when written.

# prd-roadmap becomes initiative-breakdown, and every planned PRD is sized up front (decision record, 2026-10-26)

Maintainer notes for `skills/initiative-breakdown/SKILL.md` (formerly `skills/prd-roadmap/`) and the matching lines in `prd-writing-standards`, `autonomous-prd-refinement`, `technical-design-writing-standards`, `continuation-prompt`, `implementation-lifecycle`, `implement-from-requirements`, `test-audit`, `phase-split`, `pre-commit-validation` and `using-the-enso-method`, plus the README and the setup guide. This file is outside every skill directory and is not loaded by any skill.

## The problem

- **"Roadmap" said the wrong thing.** A roadmap reads as future work, loosely specified, often with dates. The skill's output is a decided cut of one known body of work into PRDs whose scope, contracts and order are settled.
- **The skill planned for learning by shipping.** "Learning points" let entries past the first one stay coarse ("Windows agent") and be re-cut when reached, on the premise that later PRDs depend on what earlier ones teach. The user's model is the opposite: the brief is the whole thing to deliver, and every PRD and technical design can be written and refined before any build starts. The first large roadmap did exactly that (19 planned PRDs, every one written and refined; see the PRD contracts split decision, 2026-10-14).

## Options considered

1. **`prd-split`**, mirroring `phase-split`. Rejected: it reads as "point it at any PRD and split it", and planned PRDs are not meant to be split again.
2. **"Sequence" for the ordered list.** Rejected: once PRDs can be written and mostly built in any order, order is no longer the list's main content, and the name loses the word "initiative".
3. **Chosen:** the idea is an **initiative** (agile's level above an epic, as a PRD is roughly an epic); the skill is `initiative-breakdown`; the documents live in `docs/initiatives/{name}/` as `{name}-initiative-brief.md`, `{name}-initiative-prds.md` (the PRD list) and `{name}-prd-contracts.md`.

## Decisions and why

- **Unknown later work is deferred, not planned vaguely.** Where the brief leaves later work to be learned from real use, a PRD can end there, but what lies past it stays in the brief's deferred list or open questions. A planned PRD exists only for work the brief settles.
- **The over-planning guard is the existing caps, plus one sentence.** Entry length caps, point-don't-restate, and assigning (not answering) open questions are unchanged. New: sizing needs only which parts of the brief a PRD covers, what reaches production and its seams; detail the brief lacks is an open question, never invented scope.
- **Depends on gates building, not writing.** Any planned PRD can be written at any time; its design follows the designs of the PRDs on its Depends on line. Dependencies are still stated and still point backward.
- **No nesting.** A planned PRD that outgrows the band is re-cut inside its initiative into two or more planned PRDs, never broken down into PRDs of its own or made a new initiative. The removed far-end re-cut was the only method for this, so the skill gets a "Re-cutting a planned PRD" rule in its place. It covers only a PRD still being written; reopening a written, refined PRD stays the user's decision, as before.
- **A part too thin to size is deferred, not planned.** It goes to the brief's deferred list with an unassigned open question, and the declaration names it so the user can settle it.
- **Fewer dependencies is a tie-breaker** between equally valid cuts, so more PRDs can be built alongside each other.
- **Old layouts keep working.** An initiative under `docs/roadmaps/` with `-full-brief.md` and `-prd-roadmap.md` moves to the new names the next time the skill runs on it. The setup guide's removal list keeps `prd-roadmap` so old installs are cleaned up.

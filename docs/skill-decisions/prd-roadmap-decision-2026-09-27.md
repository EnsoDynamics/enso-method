# PRD roadmap: cutting an idea too big for one PRD (decision record, 2026-09-27)

Maintainer notes for `prd-roadmap/SKILL.md` and its touch points in `prd-writing-standards`, `phase-split`, `continuation-prompt`, `implementation-lifecycle`, and `technical-design-writing-standards`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing the skill's rules or names.

## The problem

- **The chain had no step for an idea bigger than one PRD.** It ran brief → PRD → technical design → `phase-split` → build. `phase-split` sizes phases to one AI session and runs after the PRD is settled, and it treats reopening a settled PRD as a rare last resort. Nothing earlier decided whether the idea was one PRD at all.
- **The motivating case.** A product brief for a large new product listed eight sequential "phases". Each was PRD-sized. Written as one PRD, it would have produced one technical design deciding everything up front and a phase plan in the dozens, with nothing reaching production for months.
- **The user's framing.** A PRD is a medium body of work: not the whole application, not one small thing. Cut the big idea into PRDs, and let `phase-split` cut each PRD into what would have been stories, now sized to one Claude Code session. The point is forward momentum: every PRD ends with something finished that can be promoted to production.

## Options considered

1. **Write one giant PRD, then split it into several afterwards.** Rejected. One technical design per PRD is a hard rule, so the giant PRD forces a giant design, or a re-split that rewrites both. Later pieces depend on what earlier ones teach, so their acceptance criteria written up front are guesswork. And splitting after the fact is exactly the "reopen a settled PRD" move `phase-split` calls a last resort.
2. **Let `phase-split` handle it with deeper phase trees.** Rejected. Phases are session-sized by definition; a 60-phase plan is a program, not a PRD (`phase-split` already says depth-5 trees mean "the level-1 phase was a whole program").
3. **A sizing section inside `prd-writing-standards` only.** Rejected as the whole answer: the procedure (consolidating inputs, the PRD-sized test, seam rules, the roadmap format, naming) is substantial, and it mirrors how `implement-from-requirements` delegates to `phase-split`. Kept as the trigger: `prd-writing-standards` has a size check that delegates.
4. **Chosen: a separate skill, `prd-roadmap`, that runs before any PRD is written.** It also accepts an oversized draft PRD as input, which covers the case where there was no brief and the size only became clear while drafting.

## Decisions and why

- **The skill stops at the cut; it does not write the first PRD.** The user's call (2026-09-27): "limit it to just the chunks." The cut is the decision worth reviewing before anyone writes a PRD, and `phase-split` has the same shape (it plans and never implements). The review point is the handoff prompt for writing the first planned PRD.
- **The sizing bar is production.** A right-sized PRD ends with something finished that can be promoted to production and does something real for someone, even if only the owner on real data. It fails when it is a layer. The phase-count band (3 to 10 level-1 phases, set September 2026) is the calibration, kept in one dated section so it is the only part that ages.
- **The full brief stays whole.** No per-PRD briefs. The brief holds cross-cutting decisions (principles, invariants, privacy rules, data-model direction) that every PRD needs; splitting copies them, where they drift, or orphans them. Same rule as `phase-split`'s "the PRD is not split". Roadmap entries point into the brief by section heading, because the brief's section numbers change when it is edited.
- **The pieces are called planned PRDs, with no new noun.** They map one-to-one to future PRD directories, and a new noun would be a second name for a PRD. Rejected names: "phase" (owned by `phase-split`), "track" (already used in these skills) and "release" (kept for the brief's own release labels), "milestone" (connotes dates), "MVP" (fits only the first).
- **Planned PRDs have names, not numbers.** Unlike phases, roadmap order is expected to change as each PRD ships and teaches something, so a positional id would churn. The roadmap table owns order; directories are `{name}-{short-name}`.
- **Document names answer the question a reader would ask.** The user first asked, on seeing the plan, whether the brief is deleted or split after the cut. `{name}-full-brief.md` says it is the whole thing; `{name}-prd-roadmap.md` says the roadmap's entries are PRDs, not a dated feature roadmap. Both live in `docs/roadmaps/{name}/`, a third documentation root above `docs/prds/` and `docs/changes/`.
- **Inputs arrive under any name and get renamed.** The skill consolidates every input (main document plus supplements) into one full brief, named for the thing being built rather than the document type, using `git mv` for tracked files and the trash for untracked extras.
- **The next planned PRD is the user's decision.** A roadmap is not a track in `continuation-prompt`'s sense: after a PRD ships, the user decides whether the next planned PRD still stands, and the roadmap may be reordered by then.

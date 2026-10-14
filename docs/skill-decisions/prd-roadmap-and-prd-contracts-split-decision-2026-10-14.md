# PRD roadmap for people, PRD contracts for sessions (decision record, 2026-10-14)

Maintainer notes for Step 5 and "Keeping the Roadmap Current" in `skills/prd-roadmap/SKILL.md`, and the matching lines in `prd-writing-standards`, `autonomous-prd-refinement` and `technical-design-writing-standards`. This file is outside every skill directory and is not loaded by any skill.

## The problem

The first large roadmap (19 planned PRDs, every one written and refined) reached 100 KB and about 18,000 words. The ordered list a person opens the roadmap for was a two-table header above it.

- **Per-PRD entries outgrew the skill's cap.** Entries capped at 6 to 15 lines ran 230 to 880 words. Each PRD's refinement edits "its roadmap entry", and the rounds kept adding detail there that belonged in the PRD.
- **The entries' scope lines were duplicates once the PRDs existed.** They are the scope source for writing a planned PRD (`prd-writing-standards`); after that, the PRD holds its own scope, dependencies and questions, and two copies drift.
- **The Seams table was about 4,900 words and no person read it, but it is live.** `technical-design-writing-standards` decides the contracts the roadmap says a PRD owns from it, and 16 of the 19 PRDs had no design yet. No PRD states which shared contracts it owns.
- **The user's framing.** The roadmap is the master list of the PRDs and their priority, for people; material written only for sessions belongs in its own document.

## Options considered

1. **Delete the entries and the Seams table.** Rejected: loses the only record of contract ownership while most designs are unwritten, and the scope source for PRDs not yet written.
2. **Keep everything in the roadmap, move it below a "for sessions" heading.** Rejected: the file stays 100 KB, and the people reading it still scroll past it.
3. **Chosen: two documents.** The roadmap holds tables (grouped when the brief sets priority tiers) and checkpoints. A new `{name}-prd-contracts.md` holds each planned PRD's scope entry, the contracts each PRD owns, the question assignments, and the Seams table.

## Decisions and why

- **Scope lines go when the PRD's refinement finishes**, not when it is first written: `autonomous-prd-refinement` checks the draft against its entry. Contract and question lines stay for the roadmap's life, since later designs read them.
- **The PRD column links the PRD file once written**, so a person goes straight from the list to the PRD (or its stakeholder review package beside it).
- **Group headings only when the brief sets tiers**, numbering continuing across groups, replacing prose bullets that explained the groups above one table.
- **Older roadmaps keep working**; they move to the split when next revised.

# Autonomous PRD refinement, and deliverable review's severity scale, delta rounds and design references (decision record, 2026-10-12)

Maintainer notes for `skills/autonomous-prd-refinement/SKILL.md` and the changes it needed in `skills/deliverable-review/SKILL.md` ("Rate Each Finding", "Delta Rounds", the product and design-reference split in "Look at Visual Deliverables", and "Carry each fix to every copy" in Step 5), with their touch points in `using-the-enso-method`, `prd-writing-standards`, `prd-roadmap`, `continuation-prompt`, `implementation-lifecycle`, `autonomous-requirements-refinement` (one pointer), `docs/how-the-enso-method-works.md` and the README. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing the stopping rule, the severity scale or how design references are reviewed.

## The problem

A PRD with 34 criteria, an assumptions document, 20 mockup states and lines in a roadmap and several sibling PRDs went through 14 rounds of `deliverable-review` before the user saw it. It took many hours over several sessions, one cut off by a usage limit, and the user asked why. Where the cost went:

- **Mockups at four widths, every round.** About 80 images a round. Most layout findings were polish that the built product's own review would catch anyway.
- **Every round read everything,** although most of a round's findings came from the previous round's fixes.
- **Fixes landed in one place and left copies elsewhere.** About three rounds went mostly on stale copies in summaries, tables, notes and neighbouring documents. The reviewers had found them; the fixes were half-applied.
- **Facts were checked again each round,** and one round's check queried the parent record instead of the item and confirmed an error rather than catching it.
- **Nothing defined severity or when to stop.** Mismatched indexes and counts were reported as Medium, so no round came back clean, and the loop had no end rule but the user's patience.

## Options considered

1. **More rules in `deliverable-review` alone.** Rejected: that skill is one round, used for code, documents and tests alike. A stopping rule, a state file and a round cap belong to the caller that loops.
2. **Run `autonomous-requirements-refinement` early.** Rejected: it needs a technical design, and it surfaces implementation questions through `implementation-readiness-check`. A draft PRD needs reviewing against its source material, before any design exists.
3. **Chosen:** a new orchestrator that loops `deliverable-review`, mirroring how `autonomous-requirements-refinement` loops the readiness check, and four generic additions to `deliverable-review` that any caller can use.

## Decisions and why

**The stopping rule**

- **No Medium or High left, ending on a full round.** The user ruled that the run does not end while a Medium remains. Full rounds continue until one finds no High, because large problems need fresh eyes on everything. Delta rounds then continue until one finds no Medium or High, because what remains is mostly the side effects of fixes. A final full round follows, because a delta round sees only what the fixes touched. If it finds a Medium or High, the loop goes back to delta rounds.
- **No fixed number of delta rounds.** A cap of two was proposed and withdrawn: the user found it arbitrary, and a delta round is cheap enough to run while its findings are real.
- **A round cap of 12, which reports.** It is a safety net for a loop that does not converge. Reaching it pauses the run and lists what is open; it never ends the run silently.
- **Rejected findings never drive the loop.** A writer that rejects a Medium with a reason would otherwise force rounds until the cap. The reason travels to every later reviewer, who can challenge it with evidence, and the completion report lists rejected Mediums and Highs for the user.
- **No conflict check in this skill.** `autonomous-requirements-refinement` runs it once the design exists, against the PRD as refined; run on a draft, it would chase criteria the review rounds are still changing.
- **Lows are fixed every round but never drive the loop.** They are cheap to fix, and a stopping rule that waited for zero Lows would not stop.

**Severity**

- **Rated by consequence, never by the effort of the fix,** with a one-sentence consequence reported for each finding, so a reviewer has to say why something matters, not just that it is wrong.
- **"Bookkeeping" names the Low bucket.** The first proposal called it "clerical", which the user found unclear. Bookkeeping is defined by what it does: text that records or points at governing text rather than stating it (indexes, trace tables, counts, cross-reference lists, change notes). A reader following correct governing text still gets it right.
- **Three calibration rules cover the disputes that recurred:** rare edge cases with a contained outcome are Low unless money, safety, data loss or legal exposure is involved; a missed copy takes the severity of where it sits; mockup sample data that contradicts the facts is Low unless someone would build or confirm the wrong thing from it.
- **The scale lives in `deliverable-review`,** because every caller needs it, not just this one.

**Cost**

- **Delta rounds are a mode of `deliverable-review`,** worded so they work for code (callers, what it calls, the tests) as well as documents.
- **The propagation sweep is in the fix step (Step 5),** not the review. The user asked whether the stale copies meant the reviewer was pointing badly; it was not, so the rule went where the misses happened.
- **Design references are reviewed for content, at one width.** The user challenged reviewing requirement mockups at every size: layout across sizes is the built product's concern, and the screen sizes a PRD names are requirements on the product. The full multi-size review stays for visuals that are the product. A delta round renders only the screens the fixes affected, those whose source changed or that show a changed term, figure or rule; a full round renders every screen once, because its point is fresh eyes on everything. See the revision note in `deliverable-review-visual-deliverables-and-references-decision-2026-10-11.md`.
- **Facts go in the state file and are deleted with it.** The user was wary of a new permanent artifact. A committed facts file was rejected: it would duplicate the assumptions' evidence and go stale. Recording nothing was rejected: checking again each round cost time and once went wrong. Evidence a stakeholder needs stays in the assumption it supports.
- **Reviewers run at high effort or above, never lower.** Lowering their effort was proposed and withdrawn after the user objected. The cost came from what reviewers were asked to do, not from how hard they thought.

**Keeping the loop honest**

- **A rejected finding carries its reason forward,** so a reviewer does not raise the same misreading every round, and may raise it again only with evidence the reason is wrong.
- **Delta snapshots go through a temporary index.** Staging the documents each round to mark a base would leave half-refined work in a shared checkout's index, where another session's commit can sweep it in. A tree written through a temporary index marks the base without touching the shared index, and it is recorded only with the round's findings, so a review that is interrupted and run again still diffs against the right base.
- **A passage that flips between two readings is settled, not fixed again.** The flip means an undecided question; it becomes an assumption, or the source material settles it.
- **A finding only another session can fix is handed off, not left to loop.** The writer fixes this PRD's side and sends the rest. When this PRD changed, the finding counts as fixed, so the change is reviewed; only a finding that needs no change here is handed off whole and stops driving the loop, as a rejected one does, so a seam waiting on a sibling cannot hold the run until the cap.
- **Sessions writing neighbouring documents are told, not overwritten.** The PRD in question was refined beside sibling PRDs being written in other sessions, and shared seams had to be agreed with them.

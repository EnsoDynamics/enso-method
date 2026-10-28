# Delivery audit and the PRD close-out (decision record, 2026-10-18)

Maintainer notes for `skills/delivery-audit/SKILL.md`, the "Completion Phases" section of `phase-split`, and their touch points in `implement-from-requirements`, `test-audit`, `using-the-enso-method`, `continuation-prompt`, `implementation-lifecycle`, `pre-commit-validation` ("Who Commits"), `phase-chain`, `prd-roadmap`, the README and `docs/how-the-enso-method-works.md`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing what happens after a PRD's last phase closes.

## The problem

When the last phase of a split PRD closed, the method ended with a one-line recommendation to run `test-audit`. Two things were missing:

- **Nothing checked that every criterion was built.** Each phase's `deliverable-review` saw one phase's diff, and each Closed line was written by the session that did the work. `test-audit` noticed a criterion with no code at all, but only reported it and pointed at `implement-from-discovery`, which takes nothing bigger than one session and is meant for discoveries, not a PRD's own criteria. A partly built criterion surfaced only when a new test failed during remediation, too late to size the work.
- **The process just stopped.** A recommendation nobody takes up is a step that exists only on paper, which is what had happened to `refactor-pass` before the 2026-10-11 decision.

## Options considered

1. **Widen `test-audit` to fix delivery gaps too.** Rejected: delivery gaps are build work, which needs the implement chain's review, test hardening and refactor pass, and they can be phase-sized. Folding them in would make the test audit a second build skill and its session too large. Both audits read the same criteria, but reading twice costs sub-agent tokens, not the user's time.
2. **Fix small gaps in the audit chat, phase the big ones.** Rejected: the audit would need the whole implement chain inside it. Gaps should be rare, so a fresh build session for even a small one costs little and keeps one skill per job.
3. **Reopen the phase that owns the gap.** Rejected: the Closed line is what the next-phase walk and outside orchestrators read. Removing it sends the next build back into finished work, and the line no longer records what that session built.
4. **Route gaps to a change directory or `implement-from-discovery`.** Rejected: the scope is the PRD's own criteria, so the PRD is the lineage. A change directory is for new scope the user writes up.
5. **Chosen:** a separate `delivery-audit` that writes no code. Gaps become completion phases at the end of the plan, built by `implement-from-requirements` like any other phase. The order at a split PRD's close is fixed: delivery audit, completion phases, test audit.

## Decisions and why

**The delivery audit**

- **One question per criterion: could a user or calling system get this behavior from the code as it stands?** Built means every required part is reachable from the real entry point. Logic nothing calls, a stub, or code behind a flag that is off everywhere is not built: that is the usual shape of a gap, and a reader looking for missing features misses it.
- **Assessors read the criteria from disk and write down each required part before opening code,** as in `test-audit`, and are not told which phase claimed a criterion.
- **The main agent confirms every gap before writing a phase.** A false gap costs a whole build session.
- **It reads and traces; it runs no tests.** The test audit's new tests and red checks are the second net, and it phases what they find unbuilt itself.
- **Only closed phases are checked.** An unclosed phase's criteria are Not built yet, so the audit never reports planned work as a gap.
- **No file of its own.** The completion phases carry the gaps; with none, an empty `delivery audit complete` commit records that it ran, read the same way as the other stages that leave no file. A per-criterion map would add a second document of record, and the test audit's assessors must not read earlier verdicts anyway.
- **Fixed at a split PRD's close; elsewhere on request.** An unsplit PRD's one build already reviewed the whole PRD; within a phase, `deliverable-review` already does this.
- **Its commit subject names its scope** (`delivery audit complete (whole PRD)`), and `(whole PRD)` only with every planned phase closed, so a narrower or earlier audit is never read as the close-out audit.

**Completion phases** (`phase-split`, "Completion Phases")

- **The next top-level ids, at the end.** No existing id changes. The rule against trailing siblings is about a re-split phase's remainder, which this is not.
- **They complete criteria, they don't own them** (`AC-RET-03 (completes it; owned by phase 2)`), so every criterion is still in exactly one phase and a PRD audit still adds up.
- **Marked at the top, `**Added by delivery audit:**`,** so nobody mistakes one for planned work.
- **They carry the audit's findings,** one line per gap, so the build starts from them instead of auditing again.

**The close-out chain**

- **A split PRD's track ends at its test audit, not its last phase** (`continuation-prompt`). The audits are the same PRD's work, so the closing build writes their prompt as it would a next phase's. The end-of-track gate still forbids prompting for a different track.
- **Each audit runs in a fresh chat.** Each checks work the previous chat helped build.
- **The audits are not `phase-chain` units.** A Codex chain stops at the last leaf and presents the delivery audit's prompt.
- **The test audit writes its own completion phase for a delivery gap** (marked `**Added by test audit:**`) rather than handing it to the user or back to the delivery audit. It has already confirmed the gap, often with a failing test, and sending it back created a loop: the delivery audit could read the criterion as built, nothing it wrote cleared the test audit's row, and the two bounced. The row waits on delivery, and the Status reads Done only when nothing waits, so a PRD is never reported complete with a known gap.
- **Completion phases exist only after every planned phase closes.** An audit run on one phase mid-PRD adds its gaps to the next open planned phase as carried-forward work, so a completion phase never sits at the end of the plan while planned phases are still open.
- **The next step at a PRD's close depends on one fact:** whether a `delivery audit complete (whole PRD)` commit exists. `implement-from-requirements`, the router and Kiln's roadmap all read the same fact, and the PRD is complete only when a whole-PRD test audit, run with every phase closed after that commit, ends with Done. The router sends the person to that run rather than reading a Done file, since a completion phase built after it changes what it must check.

**Commits**

- **The test audit now commits by default and pushes like the implement chain,** as the 2026-10-11 decision anticipated: its output is tests and code. It runs no refactor pass.
- **The delivery audit commits its documents like the requirements skills, and never pushes by default.** The build of its completion phase pushes them.

**Kiln**

- **The skills work without an orchestrator.** Without one, a clean PRD costs two extra chats at its close, plus one per completion phase. Kiln can run the same chain by starting each skill as a session; that is planned in Kiln's own roadmap, not here.

## Revisit when

- Delivery audits regularly find gaps that turn out not to be gaps. The confirm step, or the assessors' entry-point tracing, needs tightening.
- Completion phases regularly carry gaps small enough that a build session is mostly overhead. A same-chat fix for gaps under a threshold would then pay for itself.
- Test audits keep adding completion phases for criteria the delivery audit read as implemented. Reading isn't catching partial builds, and the delivery audit should run the mapped tests too.
- Per-phase audits become routine for large PRDs. The close-out could then shrink to a delta check across phases.

## Update, 2026-10-25

The historical-audit-exists routing rule above is replaced: after completion phases from either audit, or direct implementation fixes during a test audit, run a fresh whole-PRD delivery audit before returning to the test audit. Repeat repairs and delivery audits until clean. A clean audit remains current only while the governing requirements and implementation are unchanged; test-only and audit-record-only edits retain it. This closes the gap where the first audit's existence let later repairs bypass delivery verification.

## Update, 2026-10-27: read in rounds

**What happened.** Once the 2026-10-25 rule sent every repair back through a fresh whole-PRD audit, PRDs started circling: one went through five delivery audits in a day, another through four, three of which found exactly one gap. Every gap a later audit found was already in the code the first audit read; none came from a repair. The same few criteria were reported Partly implemented round after round with a different missing part each time (one provider's reader, then the other's; leaf help, then root help), and criteria read as Implemented for three rounds turned out to have gaps. The rule wasn't wrong. It exposed that a single reading has poor recall, and turned each miss into a build chat plus an audit chat.

**Why one reading misses.** The status needs only one missing part to read Partly implemented, so an assessor that found one moved on. Required parts were written per criterion, not per variant the criterion covers, so a sibling path went unchecked. The main agent's confirm step guarded against false gaps but nothing guarded against missed ones. And up to eight dense criteria per assessor left each one little attention.

**Chosen.**

- **Rounds inside the audit chat.** A round that confirms a new gap is followed by another full round with fresh assessors, re-paired within their themes and briefed exactly as the first; the main agent drops what earlier rounds already confirmed. Later rounds are not told earlier findings, as in `deliverable-review`'s full rounds, so they neither anchor on a known gap nor read the brief as a promise that more exist. The assessment ends on a round that confirms nothing new, or after four. A clean first round costs somewhat more than before (smaller batches, every variant traced); the extra rounds cost sub-agent tokens, where the outer loop cost the user two chats per miss.
- **Implemented records read for completeness.** The main agent checks that each one traces every variant, entry point and case the criterion or design names, and traces any it skips. This reads the record, so it is cheap, and it is the only check that starts from a criterion read as built.
- **Sibling check at confirmation.** Confirming a gap means reading the code where it sits, so the variants beside it are checked then. A sibling counts only when a criterion in scope requires it, so the check can't turn an observation into scope.
- **Every part traced, every variant a part.** A missing part settles the status, not the record.
- **About four criteria per assessor,** a dense criterion alone. The test audit's assessment takes the same batch size and the same per-variant parts, since it derives required parts the same way.

**Rejected.**

- **A delta audit after repairs** (re-check only the repaired criteria). It would have missed every gap the later rounds found in untouched criteria. With the first audit converging, the full post-repair audit is expected to be clean, and stays as the check on the repairs.
- **The audit fixing small gaps itself.** Still rejected for the reasons above; with rounds, completion phases carry several gaps each and the overhead question mostly goes away.
- **Rounds in the test audit.** It already remediates in its own chat until the target and re-grades with a fresh reader, so its misses don't become chat cycles.

**Revisit when** the post-repair audit regularly finds gaps the earlier one missed (rounds aren't converging), or audits regularly hit the four-round cap.

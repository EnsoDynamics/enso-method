# Test audit: grading and repairing a finished PRD's test evidence (decision record, 2026-10-04)

Maintainer notes for `skills/test-audit/SKILL.md` and its touch points in `test-hardening`, `phase-split`, `implement-from-requirements`, `implement-from-discovery`, `implementation-lifecycle`, `continuation-prompt`, the README and `docs/how-the-enso-method-works.md`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing the grades, the red-check rules or the remediation rules.

## The problem

`test-hardening` runs at the end of every implementation session, but it sees only that session's criteria, stops once its improvement is meaningful, judges tests by reading them, and is briefed by the session that wrote the code. Nothing checked a finished phase or PRD as a whole: whether every criterion is really proven, and whether a later phase weakened an earlier one's evidence. And once such a check finds gaps, fixing them should need neither phase documents nor an operator who knows the method well enough to fix them in a sensible order.

## Options considered

1. **A report mode in `test-hardening`.** Rejected: that skill is action-only, same-chat and bounded to one session's work on purpose, and a cross-session audit with a durable report would blur the boundary that keeps it from creeping.
2. **An audit whose findings are planned through `phase-split` or a change directory.** Rejected: most gaps are an hour of test writing, and the planning would cost more than the fixing.
3. **Audit and fix in one chat, with nothing written down.** Rejected: on a real PRD the gaps outlast one chat, the next chat would re-audit from scratch and grade differently, and `continuation-prompt` needs a document to point at.
4. **Chosen:** audit, then fix in the same chat in a fixed order, with one living file, `test-audit.md`, in the PRD directory as both plan and record.

## Decisions and why

**Grading**

- **Four grades, one question:** "if this criterion broke, would the suite notice?" They are `test-hardening`'s existing words, and both skills now share the definitions. A fifth grade, "partial", was folded into Weak: by the one question it is Weak, and more levels make assessors disagree more.
- **A criterion takes the grade of its least-proven part, but is Missing only when nothing exercises any part.** Otherwise one good test hides an untested clause, and the line between Missing and Weak, which sets the fix order, would depend on the assessor.
- **Strong requires red checks: each required part broken, and a test seen to fail.** Without them Strong only means the test reads well, and reading overrates tests. `test-hardening` runs no red checks, so its grades stop at adequate, and the chain now calls a good suite "credible" rather than "strong".
- **Assessors write down what each criterion requires before opening a test,** working from the PRD, assumptions and design, and are not handed the criterion text, a summary or earlier grades. Expectations read off the code bless whatever it does.

**Red checks**

- **Sampled, then widened, as an auditor samples records:** every high-risk criterion that reads Adequate or better, plus up to five others. A check that stays green downgrades its criterion and triggers checks on everything relying on the same test file or pattern. Checking every part of every criterion makes an audit slow where integration tests take minutes; checking none leaves the grades as opinion.
- **A green counts only once a crude break is shown to reach the code the test runs.** A test against a deployed service or a built artifact never sees a local change, and counting its green as weak evidence would downgrade good tests and make the target unreachable. A red must repeat, so a flaky failure doesn't count.
- **Never against production, and never on a write guard.** Tests may read production where no sandbox exists, and breaking a dry-run switch or a delete filter under such a test, or in a shared sandbox, would write or delete for real. A criterion that is itself such a guard is recorded `red check not possible` and capped at Adequate.
- **Restore by copy and checksum, not git, and leave a trail.** `git checkout -- <file>` would discard uncommitted work in the file. A checksum noted after each deliberate change shows whether anyone else edited the file before it is restored, and the REDCHECK and RESTORED marker lines let a later session repair a check an interrupted chat left behind. Tests run under a timeout, because a break can hang a test as easily as fail it.

**Fixing**

- **The target is every criterion Adequate; Strong only on request,** recommended for high-risk criteria. Missing comes first because nothing protects those criteria at all, and a finite target gives every run an end.
- **Rows no chat can raise leave the target under Waiting** (no sandbox, a code fix handed to the user), so the chain of chats can end. Running out of room is never a reason; those rows stay under To fix.
- **Fixing starts without asking,** after a one-line announcement, because "shall I fix these?" has a predictable answer. An audit-only run ends with the file under a `docs` commit.
- **Each chat sizes its own work and hands the rest on through `continuation-prompt`,** with the file as the governing document. No phase documents.
- **A fresh sub-agent re-grades the fixes,** which replaces a separate `test-hardening` pass.
- **A criterion nothing implements is a delivery gap, not test work:** the audit reports it and recommends `implement-from-discovery`.

**The file and the chat**

- **One file per PRD, updated in place.** Each row records its tests, its code and the commit it was graded at, so a re-audit can tell from `git diff` which rows to look at again; a change to shared test setup reopens every row, because one fixture can mock a boundary for every test. `implementation-lifecycle` names the file as this skill's own record, so it never becomes a backlog for discovered work.
- **Both outputs are written for someone who has never seen the skill.** The file leads with its Status line and names its sections after the grades, not the skill's internal tiers. The chat lists only the criteria with gaps, each with what's wrong in one line, because listing every criterion would bury the few that need work.
- **Recommended at PRD close only.** `implement-from-requirements` suggests it when the last phase of a split PRD closes. After every phase, or after an unsplit PRD, it would mostly repeat `test-hardening`.

## The phase-split change

Phase documents already listed their criteria by label, and a re-split put each parent label in exactly one child. Two gaps were closed:

- **A fresh plan must also place every PRD criterion in exactly one phase.** Otherwise a criterion can be dropped without anyone noticing, and a PRD audit doesn't add up.
- **Two kinds of criterion may cross a seam.** A compound criterion whose outcomes the cut separates is split in the PRD, retiring its label and taking two new ones, rather than narrowing what an existing label means. A cross-cutting constraint is owned by one phase and listed by later ones as `(also applies to this phase's work)`, wording that explains itself wherever it is read.

## Revisit when

- An audit grades a criterion Adequate or Strong and a production defect later shows the evidence was hollow. Record the case here; the red-check sample size is the first thing to raise.
- Tests carry criterion labels. Mapping could then be a script, and assessors would only grade.
- Fixing regularly takes three or more chats per PRD. The batching rule would then need concrete anchors, like `phase-split`'s calibration.
- A project has a mutation-testing tool. Red checks could run through it.
- `test-hardening` adopts red checks for the tests it adds. Its grade note and the "credible" wording would then change.

## Revised 2026-10-18: the PRD close-out

A split PRD now closes with `delivery-audit`, then `test-audit`, each handed off in a fresh chat rather than recommended. A Not implemented criterion, or a broken one past a small fix, no longer goes to `implement-from-discovery`: the test audit writes a completion phase for it (`phase-split`, "Completion Phases"). The test audit also commits by default. See `delivery-audit-and-prd-close-out-decision-2026-10-18.md`.

## Revised 2026-10-29: bounded test runs, the audit chat closes, and the user can accept rows

Whole-PRD test audits on large PRDs could run for many hours in one chat. Nothing bounded a chat, and nearly all the time went to running tests: grading is reading. The audit ran its own full-suite baseline although every phase had just run its tests, red checks widened to every criterion sharing a test file, each check ran its tests up to four times, the audit went straight on to fixing in the same context, and the only exit was every row at Adequate. An audit's findings are a plan, and fixing them is implementation work, so the two are separate stages.

**Options considered**

1. **Two skills, an audit and a fixer.** Rejected: they share the grades, the checklist, the red-check procedure, the file and the handoff order, so a split duplicates or cross-references most of the text. The chat boundary gives the same separation.
2. **A round cap only** (N rows per chat). Rejected as the main bound: rows vary from minutes to an hour. A count appears only where cost is uniform enough to count, the red checks.
3. **A delta re-grade between chats** (a fresh reader given only the named gap and the diff), with a full re-grade before Done. Rejected: the re-grade was already limited to the rows a chat worked and runs in parallel, and an assessor can miss a second gap behind the first (the 2026-10-27 delivery-audit evidence), so a full read would still be owed before Done. Every fixed row would then be read twice instead of once, and the file would need a delta marker and an "owed" state.
4. **A wall-clock ceiling per chat** (about an hour and a half, the agent reading `date` against its START line). Rejected: a model has no sense of elapsed time and sees it only when it runs a command for it, so a time rule depends on remembering to check; nothing in Claude Code or Codex enforces it, so it is no firmer than any other instruction; and a stated limit reads as an expected duration. Bounding the work that costs time is reliable and needs no clock.
5. **Chosen:** no baseline run, required parts listed by fixed test-design steps, the audit chat closing at Step 4 unless the gaps are few, fixing chats sized like a phase, a guideline count of red checks of existing evidence, the most significant work first, a stuck-row stop, and an accept exit only the user can invoke.

**Decisions and why**

- **The audit assumes the suite passes and runs none of its own.** Every phase ran its tests and its test hardening, and the closing phase ran the full suite before committing; the audit is about whether the tests prove the criteria, not whether they ran. Reusing a CI result or a recorded run was considered and rejected as proof nobody needs. Skipped, expected-failure and never-collected tests are read from the code. The only tests it runs are the ones a red check or a fix needs, and a fixing chat runs the full suite once as its commit gate.
- **Fixing chats are sized like a phase** (`phase-split`), as the original text had, and always finish work in progress before handing off. Leftover work stays under To fix, graded as it was, so no bound touches the evidence standard: none skips a check, a re-grade or the suite, or moves a row to Waiting.
- **The audit chat closes unless about three gaps or fewer.** After a dozen assessor records and the red checks, the context is heavy, and fixing in it is slower and worse. Few gaps still get fixed at once, which keeps the original no-ask momentum for small scopes.
- **About ten red checks of existing evidence per chat, the most significant first; a check on tests over five minutes counts double; widening takes three siblings, the rest become red checks still to run.** Sampling was the original design; the cascade was unbounded. Undone checks are recorded and block Done, so nothing is graded on a check that never ran. New tests' own red checks are part of writing them and come with the rows a chat takes on.
- **The limits bound what a chat works, never what the audit finds.** Every criterion is still graded and every gap recorded, so the order decides what is left: high risk first, then the gaps that leave the most unproven, then fixes that raise several rows; red checks go first where the most criteria share the evidence.
- **Cheaper red checks.** Only the tests that exercise the broken part run, by name; only a failing test repeats; the post-restore run happens once after the audit's red checks and once after each fixed row, not after every check, since a byte-identical restore is checked per file.
- **A fixing chat re-assesses nothing unchanged since its Checked commit,** even below the target, since its predecessor just graded it. For that to hold, a chat commits its tests and fixes before recording grades, and the record names that commit; with one combined commit, Checked predates the fixes and every worked row reads as changed. A chat returning after a delivery audit isn't this skill's continuation and re-assesses rows below the target as before, which is intended: code changed underneath them.
- **Stuck after two short re-grades,** in one chat or across chats. A row whose re-grade still falls short after two attempts means the approach or the reading is wrong; more attempts burn hours. The user decides.
- **Accepting rows is the user's call only.** "Accept the remaining Weak rows" covers Weak rows and pending red checks; Missing, failing and high-risk rows need naming; a delivery gap can't be accepted, since an unbuilt criterion is a requirements change. Accepted rows are recorded with the user's words and the commit, count as settled for Done, and lapse if the criterion changes or the grade drops.

- **Required parts are listed by fixed steps taken from standard test design,** because "list each required part" left assessors to stop at one test per criterion when a criterion can need two dozen. The steps follow the ISTQB Foundation syllabus (v4.0, sections 4.2 and 4.5): acceptance criteria are test conditions, and the coverage items are equivalence partitions (each category the criterion treats differently, invalid ones included), two-value boundaries (the limit and the first value past it), decision-table columns (each combination of conditions that changes the outcome) and state transitions, positive cases before negative ones. Only parts the requirements state or plainly imply count, so the list doesn't grow into exhaustive input enumeration. The "Parts covered" column is the syllabus's coverage measure, items covered over items identified, which makes a grade checkable. The stated/implied split maps onto the existing Adequate/Strong line, so `test-hardening` and `delivery-audit` keep the same vocabulary.
- **Red-check breaks follow Google's mutation-testing results** (Petrović and Ivanković, "State of Mutation Testing at Google", ICSE-SEIP 2018; Petrović et al., "Practical Mutation Testing at Scale", TSE 2021). Relational-operator, logical-connector and statement-deletion changes were the most productive; logging, time and configuration code yielded mutants developers found unhelpful, so it is skipped; Google caps surfaced mutants per change to keep attention on the useful ones, which is the precedent for the per-chat cap. The same work notes that coverage misleads when a covered statement's outcome is never asserted, the reason a part counts as covered only when its outcome is pinned.
- **Rationale moved out of the skill.** Explanations of why (why test-hardening is not enough, why superseded criteria aren't graded, why the time goes to test runs) live here; the skill keeps the rules.

**Revisit when**

- A chain of fixing chats regularly exceeds four for one PRD: the batching needs concrete anchors, like `phase-split`'s calibration.
- Audits still run long with these bounds: measure where the time goes before adding a time rule (`wall-clock-awareness`).
- Accepted rows are common on high-risk criteria: the offer's conditions are too loose.

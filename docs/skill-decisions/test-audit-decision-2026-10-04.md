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

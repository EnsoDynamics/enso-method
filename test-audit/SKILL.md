---
name: test-audit
description: Independent audit, once a phase or a whole PRD is finished, of how well its tests prove each acceptance criterion, then fixing what it finds in the same chat. Grades every criterion's evidence Missing, Weak, Adequate or Strong by one question (would the suite notice if this broke?), breaks the code on purpose to see which tests notice, and writes the map to test-audit.md in the PRD directory. Then fills the gaps in a fixed order, missing before weak, until every criterion is at least Adequate; work that outlasts the chat continues in the next one through that file, with no phase documents. Use when a phase or PRD closes, when implement-from-requirements recommends it, or when the user asks to audit the tests of a finished phase or PRD, check them against its acceptance criteria, find untested criteria, or judge whether they are good enough. Not the end-of-session pass (test-hardening), and never for work without written acceptance criteria.
user-invocable: true
---

# Test Audit

An independent check, run once a phase or a whole PRD is finished, of how well the tests prove its acceptance criteria, followed in the same chat by fixing what it finds. It grades every criterion's test evidence, writes the map to `test-audit.md` in the PRD's directory, then fills the gaps in a fixed order until every criterion has credible evidence. Fixing that outlasts one chat continues in the next through that file.

`test-hardening` already runs at the end of every implementation session. It is not enough on its own:

- **It sees one session.** Each pass is bounded to that session's criteria. Nothing re-checks evidence a later phase weakened (a mock added, a test skipped, an assertion a refactor made vacuous), or a criterion whose proof spans phases.
- **It stops early by design.** A pass that closed the top gaps has succeeded, whatever it left.
- **It is briefed by the implementer.** Its sub-agent is fresh, but the session that wrote the code tells it what the criteria are.
- **It judges tests by reading them.** A test that looks as if it would fail when the behavior breaks often doesn't. Only breaking the behavior and watching the test go red shows it.

This skill reads the whole scope, its assessors take the criteria from the PRD themselves, it breaks the code on purpose to see which tests notice, and it keeps going until every criterion is covered.

---

## When to Use

- A phase is closed, or every child of a split phase is, or a whole PRD is finished, and you want to know whether its criteria are really proven. `implement-from-requirements` recommends it when the last phase of a split PRD closes.
- The user asks to audit the tests of a finished phase or PRD, to check them against its acceptance criteria, which criteria are untested, or whether the tests are good enough.
- To continue fixing that an earlier audit left open: the continuation prompt re-runs this skill, which picks up from `test-audit.md`.

**Do NOT use this skill for:**

- The pass at the end of an implementation session. That is `test-hardening`.
- Work with no written acceptance criteria. This skill grades evidence against criteria somebody wrote; reconstructing them from what the code does is circular and blesses whatever was built. A discovery-driven fix is hardened against its stated intent by `test-hardening`.
- A whole-repo coverage review. The criteria are the whole test universe here, exactly as in `test-hardening`.

---

## Scope: Which Criteria Are Audited

The user points at a document, and that document fixes the criteria. Never infer them from code.

| Pointed at | Audits |
|---|---|
| A phase document (a leaf) | The labels in its "Acceptance criteria covered" list |
| A split record | Its labels: the union of its children's |
| A PRD, or a change directory | Every criterion in the PRD, retired labels excepted |

If what the user said fits more than one document, ask in one line. An unlabeled PRD (small ones may be) is cited by each criterion's bold title.

**Only built criteria are graded.** Pointing at a phase or an unsplit PRD says it is built. When the scope is a PRD or a split record whose phases are not all closed, criteria owned by a phase with no `**Closed:**` line are listed as Not built yet and left out.

**A cross-cutting criterion**, one a phase document lists as also applying to its work, is graded in a phase audit for that phase's work only, and the grade is marked `this phase only`. A PRD audit always re-assesses it, across the work of the closed phases.

The audit grades the code as it stands in the checkout; when files in scope have uncommitted changes, the file's header says so.

---

## The Grades

One question decides every grade: **if this criterion's behavior broke, would the suite notice?**

| Grade | Meaning |
|---|---|
| **Missing** | Nothing exercises any required part. If it broke, nothing would notice. |
| **Weak** | Something is tested, but some required part could break without any test failing: assertions that don't pin the required value (not-null, didn't-crash, count-only), expectations copied from the implementation, a mock standing in for the boundary the criterion is about, or a required part, including an error case the criterion names, with no test at all. |
| **Adequate** | Every required part would fail a test if it broke on its main path, tested at the boundary it is about. Named gaps remain: edge or error cases the criterion implies but doesn't state, or the evidence has never been seen to fail. |
| **Strong** | Adequate, with those edge and error cases covered, and red checks (Step 3) have seen a test fail with each required part broken. |

A criterion takes the grade of its least-proven required part, with one exception: it is Missing only when nothing exercises any part, so one strong test beside an untested part makes it Weak. Weak is the grade to look hardest for: a missing test looks missing, while a weak one looks like coverage.

**What counts as evidence:** a test, or a re-runnable verification script the repo carries, that passes in the project's normal test run (its test command or CI). A skipped test, an expected-failure test, a test the normal run never collects, or a manual check recorded nowhere proves nothing today; grade as if it did not exist. A mapped test that fails means the criterion may be broken, and it goes first in remediation.

**Statuses, for rows that get no grade:**

- **Not implemented:** no code does what the criterion says. That is a delivery gap, not a test gap. Surface it in the wrap-up as an action item, recommending `implement-from-discovery` with the criterion as its lineage, and leave it out of remediation.
- **Person-checked:** only a person could check it, such as a stakeholder approving wording. Use it only when no test or script could check the criterion; "hard to automate" is not the bar.
- **Not built yet:** see Scope.

**Blocked.** When the boundary a criterion is about has no non-production counterpart (no vendor sandbox, no dev environment), the best possible evidence is a narrow mock plus read-only checks (`engineering-principles`, "The Evidence Standard"). Grade it honestly, usually Weak, and add `blocked: <what is missing>`. It is outside the remediation target, and the user gets the action: stand up the environment.

**High risk.** Mark a criterion high risk when a silent break would cost money, corrupt or lose data, expose private data or access, or do something irreversible outside the system (a message to a customer, an order to a vendor). High-risk criteria get red checks first and are worked first within each tier.

---

## Process

Remediation is implementation work and runs under `implementation-lifecycle`'s session discipline (No Loose Ends, the Materiality Gate); read that skill first if it isn't loaded. The audit steps are review mode: within the criteria in scope, hunt broadly.

### Step 1: Scope, access and baseline

1. Resolve the scope (above), list the criteria by label, and open the first response with one lineage line: `Test audit of <PRD title>, <Phase id — title, or whole PRD>`. It is also the `serves:` line of this session's marker, whose START is written before the first edit (`implementation-lifecycle`, "Session Markers").
2. If `test-audit.md` already exists in the PRD directory, this is a re-audit. Re-assess only the rows in scope that need it: rows below the target; rows whose tests or code changed since the commit in their Checked column (`git diff <commit>..HEAD -- <tests> <code>`); every row, when shared test setup changed (fixtures, helpers, conftest-style files); and rows never checked. The rest keep their grades.
3. Preflight external access as `implement-from-requirements` does (Phase 1): one cheap read-only call per dependency the tests touch, re-authenticating yourself where you can. If access still fails, stop with a one-line ask; an audit that cannot run the integration tests cannot grade the criteria that matter most.
4. Run the full suite once and save each test's result (pass, fail, skip) to a temporary file outside the repo. Name the command. If one run takes more than about two minutes, load `wall-clock-awareness`.

### Step 2: Fresh-eyes assessment (sub-agents)

Launch general-purpose sub-agents in parallel, each with up to about eight criteria grouped by theme or phase, so related criteria share one reader. Give each:

- The labels to assess, and the paths of the PRD, its assumptions document, its technical design and the phase documents it needs: in a phase audit, that phase's; for a cross-cutting criterion, every phase document that lists it. **Not** the criterion text, a summary of the work, or earlier grades: it reads the requirements from disk.
- Where the tests live, and the baseline results file.
- The absolute path of this `SKILL.md`, with the instruction to follow its **Assessment Checklist** and fix nothing.

### Step 3: Red checks (main agent)

A red check breaks the behavior on purpose and watches whether a test notices. Assessors grade by reading, and reading overrates tests; red checks calibrate the grades.

**Which.** Every high-risk criterion graded Adequate or better, plus up to five others graded Adequate or better, chosen to sample different test files; each check breaks the criterion's riskiest part. If a check stays green, that criterion is Weak whatever it read as, and every other criterion whose evidence rests on the same test file or pattern gets a check too. Strong needs every required part broken in turn, which is usually Strong-tier work rather than the audit's; a criterion that reads Strong without that is graded Adequate, noted "not yet seen to fail".

**Where it is safe.** One check at a time, in the main agent, in this chat's own checkout, never one another live session is using (`implementation-lifecycle`, "Parallel Sessions: Where to Work"). Never red-check a test that reaches production in any way. Never break configuration, credentials, environment selection, or a guard that decides whether, where or how much the code writes or sends (a dry-run switch, a safety check, the filter or limit on a delete, update or send). Break the value or decision the criterion checks instead. When the only break that would test a criterion is one of these, record `red check not possible: <why>`, and the row keeps its read grade, capped at Adequate.

**How.**

1. Pick the smallest change that makes that part of the criterion false: invert a comparison, return a wrong value, skip a step.
2. Copy each file you will change to a temporary location outside the repo, and append `REDCHECK <file> <copy>` to this session's marker. Then make the change, and note the file's checksum (`shasum`); note it again after any later change you make.
3. Run only the tests mapped to the criterion, under a timeout. It is red only if one of them fails on an assertion about the criterion, and fails again on a second run. A crash, a hang, an import error, or every test failing means the change was too blunt; make a finer one.
4. Before counting a green, prove the change reached the code the test runs: a crude break in the same place (raise an error at the top of the function) must make a mapped test fail. If even that stays green, the test runs a deployed service, a built artifact or another copy of the code. Record `red check not possible: <why>`, and the row keeps its read grade, capped at Adequate.
5. Restore. First confirm the file's checksum is still the last one you noted; if it isn't, someone else has edited the file, so stop and surface that rather than overwrite it. Then copy the original back, confirm it is byte-identical, and append `RESTORED <file>`. Re-run the mapped tests; if they are not green, stop red-checking and find out why before going on. Never commit a change.

### Step 4: Write `test-audit.md`

Consolidate the sub-agents' records and the red-check results into the file (template below). Confirm every Not implemented row and every failing mapped test yourself before writing it down: the user will act on both. Then report in chat in the shape under "What the Chat Shows".

### Step 5: Remediate, in the same chat

If the user asked for the audit alone, stop here: stage `test-audit.md` per `pre-commit-validation`, present a `docs(scope): …` commit message with the repo named, and append DONE to this session's marker. Otherwise the report's Next line names what is being fixed first, and the work starts; "shall I fix these?" is the predictable question the 90% ask-gate exists to skip.

**The target is every criterion in scope at Adequate or better.** Strong is optional: work it only on request, and recommend it for high-risk criteria still below it. A row this chat cannot raise leaves the target and goes under Waiting in the file, and the chat that puts it there tells the user: a blocked row, a criterion waiting on a code fix handed to the user, or one this chat could not raise for a stated reason. Never for lack of room in this chat: unfinished rows stay under To fix for the next one.

**Tiers, in order:**

1. **Missing**, and any mapped test that is failing. A failing test means the criterion is broken or the test is wrong; find out which before anything else.
2. **Weak.** Pin the required values from the requirements, replace a mock at the boundary the criterion is about with the real resource in sandbox or dev, and add tests for the required parts nothing covers.
3. **Adequate to Strong**, only on request. Cover the criterion's edge and error cases, then red-check each required part.

High-risk criteria go first within a tier, and a tier is finished before the next one starts.

**Size the work to this chat the way `phase-split` sizes a phase:** take on what you can hold coherently while building and verifying it, in this run. A tier too big for one chat is worked in batches of related criteria (ones that share test setup), and the rest continues in the next chat. Remediation is planned in `test-audit.md` alone, never in phase documents, a PRD amendment or a change directory.

**Every test added or strengthened:**

- Traces to a criterion in scope, with a failure it would catch that you can name. The scope boundary is `test-hardening`'s: discoveries outside the criteria are dismissed, and pre-existing failures unrelated to them get one line.
- Is seen red before it counts, by Step 3's procedure against the behavior it proves, or is recorded `red check not possible: <why>`.
- Follows the evidence standard and environment rules (`engineering-principles`; `test-hardening`, "Environment Rules for Real-Resource Tests"): real resources at the boundary, writes only to non-production systems, test data tagged, fixtures checked in.

**When a new test finds the criterion broken,** the test is right and the code is wrong; never weaken the test. The work may already be in production, so if the break costs money, data or production correctness now, stop: "Critical finding, stopping to surface." Otherwise fix the code when the fix is small and plainly within the criterion. When it is bigger than the test work left, the row goes under Waiting and the fix goes to the user as an action item, recommending `implement-from-discovery`.

**A question only a stakeholder can answer** (what the required value is, when the requirements don't say) goes to the assumptions document through `assumptions-document-writing`, never into `test-audit.md` (`implementation-lifecycle`, "A Decision Needs an Assumption Entry, Always").

**If remediation changed implementation code,** run `deliverable-review` on that change before re-grading.

### Step 6: Re-grade, record, hand off

1. **Re-grade with fresh eyes.** Send the criteria this chat touched to one sub-agent under the Assessment Checklist, as in Step 2; the grades come from it, not from the chat that wrote the tests. This replaces a separate `test-hardening` pass.
2. **Update `test-audit.md`:** the table, To fix, Waiting and the Status line, which reads `Done <date>` once nothing is left to fix.
3. **Run the full suite**, naming the command: green apart from pre-existing failures, which are named.
4. **Stage and validate** per `pre-commit-validation`: the tests, any code fixes, and `test-audit.md`. Present the commit message, `test(scope): …` or `fix(scope): …` when it fixed code, with the repo named; the user commits.
5. **Hand off or close.** If the target isn't met, write the next chat's prompt with `continuation-prompt` before presenting the commit, so its edits to `test-audit.md` ride in it; the file is the governing document and its To fix list is the chain. Line 3 of the lineage reads `This chat: continues its test audit, fixing AC-…`, and the first action is to re-run this skill on the same scope. If the target is met there is no prompt: say so, and recommend Strong in one line for any high-risk criterion still below it.
6. **Append DONE** to this session's marker, naming the terminal state.

The wrap-up takes the shape under "What the Chat Shows". Its headline names the audit, so the user doesn't re-run it, and a critical finding comes before everything else.

---

## `test-audit.md`

One per PRD directory, written by this skill and updated in place by every later audit and remediation chat. It holds this skill's findings about the criteria in scope and nothing else: never a discovery from elsewhere, and never a question for a stakeholder. Write it for a reader who has never seen this skill: the Status line answers "are we done?", the table "how well is each criterion tested?", and To fix "what's left?"

```markdown
# Test audit: Customer Returns

**Status:** 2 to fix (AC-RET-03, AC-RET-02); 1 waiting (AC-RET-04)
**Last audit:** 2026-10-04, whole PRD, at `a1b2c3d`
**PRD:** [customer-returns-prd.md](./customer-returns-prd.md)

## By criterion

| Criterion | Grade | Tests | Code | Checked |
|---|---|---|---|---|
| AC-RET-01 — Eligible items are clear | Strong | `tests/integration/test_eligibility.py::test_lists_eligible` | `returns/eligibility.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-02 — Ineligible items are explained | Weak | `tests/unit/test_reasons.py::test_reason_shown` | `returns/reasons.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-03 — A return can cover several items | Missing | — | `returns/submit.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-04 — The return label is emailed | Weak, blocked | `tests/unit/test_labels.py::test_label_sent` | `returns/labels.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-05 — The refund matches the price paid (high risk) | Adequate | `tests/integration/test_refunds.py::test_full_refund` | `returns/refunds.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-06 — The refund method is shown before confirming | Adequate | `tests/integration/test_confirm.py::test_shows_refund_method` | `returns/confirm.py` | 2026-10-04 `a1b2c3d` |

## To fix, in order

**Missing**
- **AC-RET-03:** no test submits more than one item. Fix: submit two eligible items through the returns API against the sandbox, and assert both lines on the created return.

**Weak**
- **AC-RET-02:** checks that a reason appears, not what it says, and mocks the eligibility service. Fix: for each ineligibility rule, assert the reason text against the sandbox eligibility service.

**Strong, if asked** (high-risk criteria)
- **AC-RET-05:** never seen to fail; partial refunds untested. Fix: a partial-refund case, then a red check on each part.

## Waiting
- **AC-RET-04:** blocked, because the shipping carrier has no sandbox. Needs a test account from the carrier.
```

**Checked** is the date and the commit HEAD was at when the row was last graded, by an audit or by the re-grade after remediation. Rows leave To fix as they are fixed. **Strong, if asked** lists only high-risk criteria; the rest are written out if the user asks for Strong, and a **Target:** line then records what was asked. Criteria not built yet go on one line under the table.

---

## What the Chat Shows

The file holds the full map; the chat shows only what needs attention. No legend, no list of what passed, no account of how the audit ran.

**After the audit (Step 4):** a headline saying how many criteria have test gaps; a table of just those criteria, in the order they will be fixed, each with what's wrong in one line (past about fifteen rows, the high-risk ones and "and N more in the file"); the user's actions, from Waiting and Not implemented rows; then what happens next and the file's path. With no gaps, the headline and the path are the whole report.

```markdown
**Test audit, Customer Returns (whole PRD): 2 of 6 criteria have test gaps.** 3 are Adequate or better; 1 is blocked.

| Criterion | Grade | What's wrong |
|---|---|---|
| AC-RET-03 — A return can cover several items | Missing | No test submits more than one item |
| AC-RET-02 — Ineligible items are explained | Weak | Checks that a reason appears, not what it says; the eligibility service is mocked |

**Your action:** ask the shipping carrier for a test account; AC-RET-04 can't be tested without one.

**Next:** writing a test for AC-RET-03. Full map: `docs/prds/customer-returns/test-audit.md`
```

**At the wrap-up (Step 6):** a headline with the gaps fixed out of the gaps found; what is still open and where it goes; how the result was checked; the user's actions and any Strong recommendation; then the commit message and, when gaps remain, the next chat's prompt.

```markdown
**Test audit, Customer Returns (whole PRD): 2 of 2 gaps fixed.** Every criterion is now Adequate or better except AC-RET-04 (blocked). Re-graded by a fresh reviewer; full suite green (`pytest`).

**Your action:** ask the shipping carrier for a test account; AC-RET-04 can't be tested without one.
**Recommended:** take AC-RET-05 (high risk) to Strong.
```

---

## Assessment Checklist

The sub-agent follows this. Read everything from disk; work from no one's memory or summary.

For each criterion:

1. **Required parts, from the requirements alone.** Read the criterion in the PRD, the assumption entries and technical-design sections it depends on, and in a phase audit the phase document. Before opening a test, write down what would have to be observed for it to hold: each required part as something a test could check, including any error or boundary case the criterion states. Derive them from the requirements, never from the code; expectations read off the implementation bless whatever it does.
2. **Find the evidence and the code.** Search the tests by label, by the names the criterion uses, and by the code the technical design names for it. Map each test to the parts it exercises, and note the files that implement the criterion.
3. **Check each mapped test.** Did it pass in the baseline, and does the project's normal test run collect it? Does it reach the boundary its part is about, or mock it? Do its assertions pin the required outcome with values taken from the requirements? Would it fail if that part broke?
4. **Grade** by "The Grades", or give a status (Not implemented, Person-checked). Add `blocked: <what is missing>` when the criterion's boundary has no non-production counterpart.
5. **Risk.** High if a silent break would cost money, corrupt or lose data, expose private data or access, or do something irreversible outside the system.
6. **Gap and fix.** For anything below Strong: what is missing, and the smallest fix that would raise the grade, at the level and against the resource it needs.
7. **Red-check target.** For anything graded Adequate or better: the file and function a red check should break for the criterion's riskiest part, and how.

Report one record per criterion with these fields. Observations outside the criteria are not findings; leave them out. **Do not fix anything.**

---

## Rules and Constraints

### DO

- Take the criteria from the document the user points at, and grade every one by the same question: would the suite notice if it broke?
- Have the assessors read the requirements from disk themselves and derive each criterion's required parts before opening a test
- Red-check every high-risk criterion graded Adequate or better and a sample of the rest, and widen the checks when one stays green
- Remediate in the same chat, in tier order and sized to the chat, until every criterion is Adequate or better; carry the rest in `test-audit.md`
- See every new or strengthened test fail before counting it
- Re-grade remediation with a fresh sub-agent, never by the chat that wrote the tests

### DO NOT

- Infer acceptance criteria from code, or audit work that has none written down
- Count a skipped, failing or never-collected test as evidence
- Grade Strong without red checks on every required part
- Red-check a test that reaches production, or break a guard on whether, where or how much the code writes or sends
- Overwrite a file someone else edited during a red check, or leave a check unrestored
- Plan remediation in phase documents, a PRD amendment or a change directory
- Write a test that traces to no criterion in scope, or fix pre-existing failures unrelated to the criteria
- Weaken a test to make it pass against code that breaks the criterion
- Work the Strong tier unasked

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `test-hardening` | The per-session pass this skill checks after the fact. Same grades, same scope boundary, same evidence rules: it hardens one session's work, and this skill grades and repairs the finished whole. |
| `implement-from-requirements` | Recommends this skill when the last phase of a split PRD closes. Its per-phase test hardening does not replace it. |
| `phase-split` | A phase document's "Acceptance criteria covered" list is the scope of a phase audit, and its rule that every criterion lands in exactly one phase is what makes a PRD audit add up. |
| `implementation-lifecycle` | Remediation runs under its session discipline; the audit steps are the review mode it describes. It names `test-audit.md` as this skill's own record, never a destination for discovered work. |
| `engineering-principles` | The testing evidence standard the grades encode. |
| `deliverable-review` | Runs on any implementation change remediation makes, before the re-grade. |
| `continuation-prompt` | Writes the next chat's prompt when remediation outlasts a chat, with `test-audit.md` as the governing document and its To fix list as the chain. |
| `pre-commit-validation` | The commit boundary for remediation's tests, fixes and the audit file. |
| `implement-from-discovery` | Where a Not implemented criterion, or a broken one whose fix is bigger than the test work left, goes. |

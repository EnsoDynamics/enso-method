---
name: test-audit
description: Independent audit, once a phase or a whole PRD is finished, of how well its tests prove each acceptance criterion, then fixing what it finds. Grades every criterion's evidence Missing, Weak, Adequate or Strong by one question (would the suite notice if this broke?), breaks the code on purpose to see which tests notice, and writes the map to test-audit.md in the PRD directory. The audit chat ends there unless the gaps are few; fixing chats then fill the gaps in a fixed order, missing before weak, until every criterion is at least Adequate or the user accepts what remains. Each chat takes a batch of rows it can hold and hands the rest on through that file, with no phase documents for test work. It assumes the suite already passes and runs no suite of its own; its capped red checks run only the test aimed at what they break. Use when a phase or PRD closes, after delivery-audit at the close of a split PRD, or when the user asks to audit the tests of a finished phase or PRD, check them against its acceptance criteria, find untested criteria, or judge whether they are good enough. Not the end-of-session pass (test-hardening), and never for work without written acceptance criteria.
user-invocable: true
---

# Test Audit

An independent check, run once a phase or a whole PRD is finished, of how well the tests prove its acceptance criteria, followed by fixing what it finds. The audit chat grades every criterion's test evidence and writes the map to `test-audit.md` in the PRD's directory. When the gaps are few it fixes them in the same chat; otherwise fixing chats fill the gaps in a fixed order until every criterion has credible evidence or the user accepts what remains. Each chat takes a batch it can hold and hands the rest on through that file.

Unlike `test-hardening`, which each implementation session runs on its own criteria as its implementer describes them, this audit covers the finished whole, takes the criteria from the PRD itself, and breaks code on purpose to see which tests notice.

---

## When to Use

- A phase is closed, or every child of a split phase is, or a whole PRD is finished, and you want to know whether its criteria are really proven. At the close of a split PRD it runs after `delivery-audit`, which checks that every criterion is built and adds completion phases for any that aren't; once nothing is left to build, `implement-from-requirements` or `delivery-audit` hands off here.
- The user asks to audit the tests of a finished phase or PRD, to check them against its acceptance criteria, which criteria are untested, or whether the tests are good enough.
- To continue fixing that an earlier audit left open: the continuation prompt re-runs this skill, which picks up from `test-audit.md`.
- To accept the rows still below the target, when the user says so ("Accepting Rows", below).

**Do NOT use this skill for:**

- The pass at the end of an implementation session. That is `test-hardening`.
- Work with no written acceptance criteria. Never reconstruct criteria from what the code does. A discovery-driven fix is hardened against its stated intent by `test-hardening`.
- A whole-repo coverage review. The criteria are the whole test universe here, exactly as in `test-hardening`.

---

## Scope: Which Criteria Are Audited

The user points at a document, and that document fixes the criteria. Never infer them from code.

| Pointed at | Audits |
|---|---|
| A phase document (a leaf) | The labels in its "Acceptance criteria covered" list |
| A split record | Its labels: the union of its children's |
| A PRD, or a change directory | Every criterion in the PRD, retired labels excepted |

If what the user said fits more than one document, ask in one line. An unlabeled PRD (small ones may be) is cited by each criterion's bold title. **In every scope, a criterion with a `Superseded by:` line is left out,** listed as superseded with its pointer, never graded. One with `Superseded in part by:` is graded on the part still in force (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion").

**Only built criteria are graded.** Pointing at a phase or an unsplit PRD says it is built. When the scope is a PRD or a split record whose phases are not all closed, criteria owned by a phase with no `**Closed:**` line are listed as Not built yet and left out. So is a criterion an open completion phase completes: its build is still to come.

**A cross-cutting criterion**, one a phase document lists as also applying to its work, is graded in a phase audit for that phase's work only, and the grade is marked `this phase only`. A PRD audit always re-assesses it, across the work of the closed phases.

The audit grades the code as it stands in the checkout; when files in scope have uncommitted changes, the file's header says so.

---

## The Grades

One question decides every grade: **if this criterion's behavior broke, would the suite notice?**

| Grade | Meaning |
|---|---|
| **Missing** | Nothing exercises any required part. If it broke, nothing would notice. |
| **Weak** | Something is tested, but some required part could break without any test failing: assertions that don't pin the required value (not-null, didn't-crash, count-only), expectations copied from the implementation, a mock standing in for the boundary the criterion is about, or a stated required part (Assessment Checklist), including an error case the criterion names, with no test at all. |
| **Adequate** | Every stated required part is covered: a test at the boundary it is about would fail if it broke. Gaps remain only in implied parts, or the evidence has never been seen to fail. |
| **Strong** | Adequate, with the implied parts covered too, and red checks (Step 3) have seen a test fail with each stated part broken. |

A criterion takes the grade of its least-proven stated part, with one exception: it is Missing only when nothing exercises any part, so one strong test beside an untested part makes it Weak. Look hardest for Weak: it looks like coverage.

**What counts as evidence:** a test, or a re-runnable verification script the repo carries, that passes in the project's normal test run (its test command or CI). A skipped test, an expected-failure test, a test the normal run never collects, or a manual check recorded nowhere proves nothing today; grade as if it did not exist. A mapped test that fails means the criterion may be broken, and it goes first in remediation.

**Statuses, for rows that get no grade:**

- **Not implemented:** no code does what the criterion says. First check whether the behavior was changed on purpose later, by a later-built criterion or a commit in the code's history (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"; one conflict check covers every such row in the audit). If a later PRD changed it, add the missing pointer pair and list the row as superseded. If the code does something else a person could have chosen, it is shipped behavior and stands (the lifecycle's shipped-behavior rule): list the row as changed outside the requirements and name it in the wrap-up for the user to record, whatever the history shows. Otherwise it is a delivery gap, not a test gap: leave it out of remediation and handle it as Step 5's "A delivery gap" says.
- **Person-checked:** only a person could check it, such as a stakeholder approving wording. Use it only when no test or script could check the criterion; "hard to automate" is not the bar.
- **Not built yet:** see Scope.
- **Superseded:** a later PRD replaced the criterion; the row shows its pointer.
- **Changed outside the requirements:** the code deliberately does something else and no document records it; named in the wrap-up for the user to record.

**Blocked.** When the boundary a criterion is about has no non-production counterpart (no vendor sandbox, no dev environment), the best possible evidence is a narrow mock plus read-only checks (`engineering-principles`, "The Evidence Standard"). Grade it honestly, usually Weak, and add `blocked: <what is missing>`. It is outside the remediation target, and the user gets the action: stand up the environment.

**High risk.** Mark a criterion high risk when a silent break would cost money, corrupt or lose data, expose private data or access, or do something irreversible outside the system (a message to a customer, an order to a vendor). High-risk criteria get red checks first and are worked first within each tier.

---

## Bounding Each Chat

These limit the work a chat takes on, never what the audit finds: every criterion in scope is graded and every gap recorded, and work left over stays under To fix, graded as it was.

- **No suite runs in the audit.** It assumes the suite passes (Step 1). The only tests it runs are the ones a red check aims at, by name.
- **About ten red checks of existing evidence per chat,** counting widening checks and red checks still to run. A check whose test takes more than about five minutes a run counts as two. The red check each new test gets in Step 5 is part of writing that test and doesn't count.
- **Widening stops at three.** A green check adds checks for at most three other criteria resting on the same test file or pattern.
- **Checks past the cap or the widening limit** go under To fix as **red checks still to run**. When the cap stops a fixing chat partway through them, it goes on to the Weak rows; the cap outranks finishing a tier.
- **The audit chat closes at Step 4** unless To fix holds about three rows or fewer, none of them a delivery gap.
- **A fixing chat takes one batch:** the rows it can build and verify in one session, sized the way `phase-split` sizes a phase, usually a group that shares test setup. It finishes work in progress before handing off: no check unrestored, no test half written.
- **Most significant first,** so what is left is least important. Rows within a tier: high risk, then the most required parts uncovered, then rows sharing setup with others so one fix raises several. Red checks: high-risk criteria, then evidence the most other criteria rest on.
- **Two short re-grades make a row stuck.** Each re-grade that leaves a worked row below the target adds `tried <date>: <what was done; what the re-grader still found>` to its To fix entry. At the second, mark it `stuck`, stop working it, and name it in the wrap-up; no chat works it again until the user says how (a different approach, a requirement clarified through the assumptions document, or acceptance).

### Accepting Rows

The user may decide that some rows are good enough: "accept the remaining Weak rows", "accept AC-RET-02". Only the user's own words do this: said in this chat, or quoted in the prompt with where the user said them. Never this skill's judgment, and never an orchestrator's or another agent's. The wrap-up offers it whenever every row left to fix is Weak or a red check still to run and none is high risk, and for every stuck row.

- **"Accept the remaining Weak rows"** covers Weak rows and red checks still to run. A Missing row, a row with a failing mapped test, and a high-risk row are accepted only when the user names it; before recording one, say in one line what it leaves unproven.
- **A row waiting on delivery can't be accepted.** The criterion isn't built; if it shouldn't be, the requirement changes (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion"), not the audit.
- **Recording.** Each accepted row moves from To fix to an **Accepted** section of `test-audit.md`, keeping its grade and its one-line gap, with the date, the commit, and the user's words quoted with where they were said. The table shows the grade with `, accepted`. Accepted rows count as settled for the Status line: `Done 2026-10-29; accepted: AC-RET-02 (Weak)`.
- **Acceptance lasts while the row is unchanged.** A re-audit re-assesses an accepted row by Step 1's rules like any other. If its criterion changed, or its grade came back lower than the grade accepted, the acceptance lapses and the row returns to To fix, noting when it was accepted.

---

## Process

Remediation is implementation work and runs under `implementation-lifecycle`'s session discipline (No Loose Ends, the Materiality Gate); read that skill first if it isn't loaded. The audit steps are review mode: within the criteria in scope, hunt broadly.

### Step 1: Scope and access

1. Resolve the scope (above), list the criteria by label, and open the first response with one lineage line: `Test audit of <PRD title>, <Phase id — title, or whole PRD>`. It is also the `serves:` line of this session's marker, whose START is written before the first edit (`implementation-lifecycle`, "Session Markers").
2. If `test-audit.md` already exists in the PRD directory, this is a re-audit. Re-assess only the rows in scope that need it: rows below the target, not counting accepted rows; rows whose governing requirements (including applicable assumptions and design), tests or code changed since the commit in their Checked column (`git diff <commit> -- <requirements> <tests> <code>`); every row, when shared test setup changed (fixtures, helpers, conftest-style files); and rows never checked. The rest keep their grades. In a fixing chat that this skill's own continuation prompt started, rows below the target are re-assessed only when they changed by the rules above: its predecessor's grades stand. After item 4 of this step, it runs Steps 2 and 3 for the changed rows alone, skipping them when none changed, then goes to Step 5.
3. Preflight external access as `implement-from-requirements` does (Phase 1), for the dependencies of the tests this chat will run (its red checks; in a fixing chat, the rows it takes): one cheap read-only call each, re-authenticating yourself where you can. If access still fails, stop with a one-line ask.
4. **Assume the suite passes.** The phases ran their tests; run no suite and ask for no proof that one ran. Grade the tests as written. Whether a test is skipped, marked expected to fail, or outside what the project's normal run collects is read from the code (skip markers, the runner's test-path configuration), not from a run. A test that fails when this audit does run it, in a red check or a fix, goes first in remediation.

### Step 2: Fresh-eyes assessment (sub-agents)

Launch general-purpose sub-agents in parallel, each with up to about four criteria grouped by theme or phase, so related criteria share one reader; give a criterion that covers many variants or cases a reader to itself. Give each:

- The labels to assess, and the paths of the PRD, its assumptions document, its technical design and the phase documents it needs: in a phase audit, that phase's; for a cross-cutting criterion, every phase document that lists it. **Not** the criterion text, a summary of the work, or earlier grades: it reads the requirements from disk.
- Where the tests live.
- The absolute path of this `SKILL.md`, with the instruction to follow its **Assessment Checklist** and fix nothing.

### Step 3: Red checks (main agent)

A red check breaks the behavior on purpose and watches whether a test notices. Reading alone overrates tests; red checks calibrate the grades.

**Which.** Every high-risk criterion graded Adequate or better, plus up to five others graded Adequate or better that sample different test files, in the order and up to the cap "Bounding Each Chat" sets; each check breaks the criterion's riskiest stated part. If a check stays green, that criterion is Weak whatever it read as, and the criteria resting on the same test file or pattern get checks too, up to the widening limit. Strong needs every stated part broken in turn, which is usually Strong-tier work rather than the audit's; a criterion that reads Strong without that is graded Adequate, noted "not yet seen to fail".

**Where it is safe.** One check at a time, in the main agent, in this chat's own checkout, never one another live session is using (`implementation-lifecycle`, "Parallel Sessions: Where to Work"). Never red-check a test that reaches production in any way. Never break configuration, credentials, environment selection, or a guard that decides whether, where or how much the code writes or sends (a dry-run switch, a safety check, the filter or limit on a delete, update or send). Break the value or decision the criterion checks instead. When the only break that would test a criterion is one of these, record `red check not possible: <why>`, and the row keeps its read grade, capped at Adequate.

**How.**

1. Pick the smallest change that makes that part false, in code its test runs: flip a comparison or a boundary (`<` to `<=`), swap `and` and `or`, return a wrong value, or delete the statement that produces the outcome. Never break logging, timing or configuration code.
2. Copy each file you will change to a temporary location outside the repo, and append `REDCHECK <file> <copy>` to this session's marker. Then make the change, and note the file's checksum (`shasum`); note it again after any later change you make.
3. Run only the mapped tests that exercise the part you broke, by name, under a timeout. It is red only if one of them fails on an assertion about the criterion, and fails again on a second run of that test alone. A crash, a hang, an import error, or every test failing means the change was too blunt; make a finer one.
4. Before counting a green, prove the change reached the code the test runs: a crude break in the same place (raise an error at the top of the function) must make a mapped test fail. If even that stays green, the test runs a deployed service, a built artifact or another copy of the code. Record `red check not possible: <why>`, and the row keeps its read grade, capped at Adequate.
5. Restore. First confirm the file's checksum is still the last one you noted; if it isn't, someone else has edited the file, so stop and surface that rather than overwrite it. Then copy the original back, confirm it is byte-identical, and append `RESTORED <file>`. Never commit a change.
6. After the last check of Step 3, and in Step 5 after each row, run every test red-checked since the last such run once, together. If any is not green, find out why before going on: a check left state behind, or a restore went wrong.

### Step 4: Write `test-audit.md`

Consolidate the sub-agents' records and the red-check results into the file (template below). Confirm every Not implemented row and every failing mapped test yourself before writing it down: the user or a build will act on them. Then report in chat in the shape under "What the Chat Shows".

**Then decide whether this chat also fixes.** It goes straight on to Step 5 only when the gaps are few, about three rows under To fix with no delivery gap among them. Otherwise this chat is the audit, and it closes without fixing: write any completion phase or carried-forward section a delivery gap calls for (Step 5, "A delivery gap"), then Step 6's items 4 to 7, committing under a `docs(scope): …` message. There is nothing to re-grade, no tests to commit first, and no changed code to run the suite for. The handoff is to a build when a completion phase is open, and otherwise to the first fixing chat. If the user asked for the audit alone, it closes the same way but writes no completion phase and no prompt unless asked; its Not implemented rows wait for the next run. The report's Next line says which; never ask whether to fix.

### Step 5: Remediate

A fixing chat, or an audit chat with few gaps, works the rows under To fix.

**The target is every criterion in scope at Adequate or better, with no red check still to run,** apart from rows the user accepts. Strong is optional: work it only on request, and recommend it for high-risk criteria still below it. A row this chat cannot raise leaves the target and goes under Waiting in the file, and the chat that puts it there tells the user: a blocked row, one this chat could not raise for a stated reason, or a row **waiting on delivery** ("A delivery gap", below). Never for lack of room in this chat: unfinished rows stay under To fix for the next one.

**Tiers, in order:**

1. **Missing**, and any mapped test that is failing. A failing test means the criterion is broken or the test is wrong; find out which before anything else.
2. **Red checks still to run**, chosen and run by Step 3's rules, widening included. A green one moves its row to Weak.
3. **Weak.** Pin the required values from the requirements, replace a mock at the boundary the criterion is about with the real resource in sandbox or dev, and add tests for the required parts nothing covers, one per uncovered part.
4. **Adequate to Strong**, only on request. Cover the implied parts, then red-check each stated part.

Within a tier, rows go in the order "Bounding Each Chat" gives, high risk first, and a tier is finished before the next one starts.

**Take a batch the chat can hold** (Bounding Each Chat); the rest continues in the next one. While iterating on a row, run only its tests; the full suite runs once, in Step 6, as the commit gate. Remediation is planned in `test-audit.md` alone, never in phase documents, a PRD amendment or a change directory.

**Every test added or strengthened:**

- Traces to a criterion in scope, with a failure it would catch that you can name. The scope boundary is `test-hardening`'s: discoveries outside the criteria are dismissed, and pre-existing failures unrelated to them get one line.
- Is seen red before it counts, by Step 3's procedure against the behavior it proves, or is recorded `red check not possible: <why>`. One break may serve several new tests that prove the same part.
- Follows the evidence standard and environment rules (`engineering-principles`; `test-hardening`, "Environment Rules for Real-Resource Tests"): real resources at the boundary, writes only to non-production systems, test data tagged, fixtures checked in.

**When a new test finds the criterion broken,** and the code consistently does something else instead, first check whether the behavior was changed on purpose later, by a later-built criterion or a commit in the code's history (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"; one conflict check covers every such row in the run). If a later PRD changed it, add the missing pointer pair and list the row as superseded; otherwise the shipped behavior stands, and the row is listed as changed outside the requirements and named in the wrap-up. Either way the new test is dropped; an audit never reverts shipped behavior on its own. Otherwise the test is right and the code is wrong; never weaken the test. The work may already be in production, so if the break costs money, data or production correctness now, stop: "Critical finding, stopping to surface." Otherwise fix the code when the fix is small and plainly within the criterion. When it is bigger than the test work left, it is a delivery gap.

**A delivery gap,** a criterion Not implemented or broken in a way bigger than the test work left, is build work, not test work. Once every planned phase of the PRD is closed, write a completion phase for it in `phase-split`'s form ("Completion Phases"), marked `**Added by test audit:**`; gaps that share code go in one phase, and its "What the audit found missing" line names what is missing and, for a broken criterion, the test that failed and its failure. While planned phases are still open (a phase audit mid-PRD), add the gap instead to the next open planned phase as a `## Carried forward from Phase N` section (`implementation-lifecycle`). Either way the row goes under Waiting as **waiting on delivery**, naming that phase. Revert the failing test rather than commit it or leave it in the checkout.

**A question only a stakeholder can answer** (what the required value is, when the requirements don't say) goes to the assumptions document through `assumptions-document-writing`, never into `test-audit.md` (`implementation-lifecycle`, "A Decision Needs an Assumption Entry, Always").

**If remediation changed implementation code,** run `deliverable-review` on that change before re-grading.

### Step 6: Re-grade, record, hand off

1. **Re-grade with fresh eyes.** Send the rows this chat worked to fresh sub-agents under the Assessment Checklist, batched as in Step 2; the grades come from them, not from the chat that wrote the tests. This replaces a separate `test-hardening` pass. Their findings go back under To fix, and this chat works them only when they fit the batch it took on.
2. **Run the full suite**, the commit gate for the tests and code this chat changed, naming the command: green apart from pre-existing failures, which are named.
3. **Commit the tests and any code fixes** per `pre-commit-validation`, under `test(scope): …`, or `fix(scope): …` when it fixed code, with the repo named. They go first, in a commit of their own, so the Checked column can name a commit that holds them.
4. **Update `test-audit.md`:** the table, To fix, Waiting, Accepted and the Status line. A row graded in this chat gets item 3's commit as its Checked commit, or HEAD when this chat committed nothing. The Status line reads `Done <date>` only when nothing is left to fix, no red check is still to run, and no row waits on delivery; accepted rows count as settled, and a blocked row can still be waiting. Otherwise it names every reason it isn't Done, as in `4 to fix (AC-RET-03, …); 2 red checks to run; stuck: AC-RET-06; waiting on delivery: AC-RET-08 (phase 8); 1 not implemented, not phased (audit only)`.
5. **Hand off or close.** Write the next chat's prompt with `continuation-prompt` before item 6's commit, so its edits to `test-audit.md` ride in it; the file is the governing document. Which prompt, taking the first case that applies:
   - **A completion phase this audit added is open:** `implement-from-requirements` on it, with that phase's lineage (`This chat: implements it.`). Building comes before proving, whatever is left to fix; when the last open leaf closes, the build hands off by its own wrap-up rule (`implement-from-requirements`, Phase 8), which brings this audit back.
   - **Every phase is closed, but no current clean whole-PRD delivery audit covers the work:** `delivery-audit` on the whole PRD (`delivery-audit` defines currentness). This includes small implementation fixes made in this test audit. After a clean delivery audit, return here and reassess affected rows under Step 1; retain unchanged evidence.
   - **Rows are left to fix,** or red checks are still to run: this skill on the same scope. Line 3 of the lineage reads `This chat: continues its test audit, fixing AC-…`, and the first action is to re-run this skill. When every row left could be accepted ("Accepting Rows"), the wrap-up offers that in one line beside the prompt. When every row left is stuck, there is no prompt: the wrap-up asks the user how to proceed.
   - **The only rows waiting on delivery were carried into an open planned phase:** no prompt. The build's next phase delivers them, and the PRD's close re-audits them; say so.
   - **The Status line reads Done.** When the audit covered the whole PRD, every phase is closed and a current clean whole-PRD delivery audit covers the work, the PRD's track is complete: say so, with no prompt, and for a PRD in an initiative, name the next PRD after it in the initiative's order that is not yet in production, in one line (`continuation-prompt`, "An initiative is not a track"). Otherwise the audit of its scope is done, with no prompt. Either way, name any accepted rows in one line, and recommend Strong in one line for any high-risk criterion still below it.
6. **Commit the record** per `pre-commit-validation`: `test-audit.md`, and any completion phase or carried-forward section and plan-table row Step 5 wrote, under `docs(scope): …`, with the repo named. Both commits are made by default, and pushed when the push lands on a feature branch ("Who Commits").
7. **Append DONE** to this session's marker, naming the terminal state. Leaving rows for the next chat, or ending with every row left stuck, is not Blocked: the work done is finished and committed, and the rest is recorded. Its DONE reads `Completed — remainder in test-audit.md`.

The wrap-up takes the shape under "What the Chat Shows". Its headline names the audit, so the user doesn't re-run it, and a critical finding comes before everything else.

---

## `test-audit.md`

One per PRD directory, written by this skill and updated in place by every later audit and remediation chat. It holds this skill's findings about the criteria in scope and nothing else: never a discovery from elsewhere, and never a question for a stakeholder. Write it for a reader who has never seen this skill: the Status line answers "are we done?", the table "how well is each criterion tested?", and To fix "what's left?"

```markdown
# Test audit: Customer Returns

**Status:** 2 to fix (AC-RET-03, AC-RET-02); 1 red check to run (AC-RET-06); 1 waiting (AC-RET-04, blocked); accepted: AC-RET-07 (Weak)
**Last audit:** 2026-10-04, whole PRD, at `a1b2c3d`
**PRD:** [customer-returns-prd.md](./customer-returns-prd.md)

## By criterion

| Criterion | Grade | Parts covered | Tests | Code | Checked |
|---|---|---|---|---|---|
| AC-RET-01 — Eligible items are clear | Strong | 4 of 4 | `tests/integration/test_eligibility.py::test_lists_eligible` | `returns/eligibility.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-02 — Ineligible items are explained | Weak | 1 of 4 | `tests/unit/test_reasons.py::test_reason_shown` | `returns/reasons.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-03 — A return can cover several items | Missing | 0 of 2 | — | `returns/submit.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-04 — The return label is emailed | Weak, blocked | 1 of 2 | `tests/unit/test_labels.py::test_label_sent` | `returns/labels.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-05 — The refund matches the price paid (high risk) | Adequate | 3 of 3 | `tests/integration/test_refunds.py::test_full_refund` | `returns/refunds.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-06 — The refund method is shown before confirming | Adequate | 2 of 2 | `tests/integration/test_confirm.py::test_shows_refund_method` | `returns/confirm.py` | 2026-10-04 `a1b2c3d` |
| AC-RET-07 — The return window is enforced | Weak, accepted | 2 of 3 | `tests/unit/test_window.py::test_rejects_late` | `returns/window.py` | 2026-10-04 `a1b2c3d` |

## To fix, in order

**Missing**
- **AC-RET-03:** neither part is tested (several eligible items in one return; every item listed on it). Fix: submit two eligible items through the returns API against the sandbox, and assert both lines on the created return.

**Red checks still to run**
- **AC-RET-06:** the audit chat's cap ran out before its check. Check: show the wrong refund method and run `test_shows_refund_method`.

**Weak**
- **AC-RET-02:** 1 of 4 parts: checks that a reason appears, not what it says for each of the three ineligibility rules, and mocks the eligibility service. Fix: for each ineligibility rule, assert the reason text against the sandbox eligibility service.

**Strong, if asked** (high-risk criteria)
- **AC-RET-05:** never seen to fail; partial refunds untested. Fix: a partial-refund case, then a red check on each part.

## Waiting
- **AC-RET-04:** blocked, because the shipping carrier has no sandbox. Needs a test account from the carrier.

## Accepted
- **AC-RET-07** (Weak): the last day of the window is untested. Accepted 2026-10-05 at `b2c3d4e`: "accept the remaining Weak rows".
```

**Parts covered** counts the criterion's stated required parts that a test covers, out of those identified (Assessment Checklist). **Checked** is the date the row was last graded and the commit that grade applies to: HEAD when an audit graded it, or the commit holding the fixes when a re-grade did (Step 6, item 4). Rows leave To fix as they are fixed. A row marked `stuck` (Bounding Each Chat) stays under To fix with that word and what was tried. **Strong, if asked** lists only high-risk criteria; the rest are written out if the user asks for Strong, and a **Target:** line then records what was asked. Criteria not built yet go on one line under the table.

---

## What the Chat Shows

The file holds the full map; the chat shows only what needs attention. No legend, no list of what passed, no account of how the audit ran.

**After the audit (Step 4):** a headline saying how many criteria have test gaps; a table of just those criteria, in the order they will be fixed, each with what's wrong in one line (past about fifteen rows, the high-risk ones and "and N more in the file"); the user's actions, from blocked Waiting rows, and the phase each delivery gap went to; then what happens next and the file's path. With no gaps, the headline and the path are the whole report. When this chat closes as the audit, Next names the chat that follows, and its prompt ends the report.

```markdown
**Test audit, Customer Returns (whole PRD): 2 of 6 criteria have test gaps.** 3 are Adequate or better; 1 is blocked.

| Criterion | Grade | Parts covered | What's wrong |
|---|---|---|---|
| AC-RET-03 — A return can cover several items | Missing | 0 of 2 | No test submits more than one item |
| AC-RET-02 — Ineligible items are explained | Weak | 1 of 4 | Checks that a reason appears, not what it says; the eligibility service is mocked |

**Your action:** ask the shipping carrier for a test account; AC-RET-04 can't be tested without one.

**Next:** writing a test for AC-RET-03. Full map: `docs/prds/customer-returns/test-audit.md`
```

**At the wrap-up (Step 6):** a headline with the gaps fixed out of the gaps found; what is still open and where it goes; how the result was checked; the user's actions, any stuck row, any offer to accept the rows left, and any Strong recommendation; then the commit and, when gaps remain or rows wait on delivery, the next chat's prompt.

```markdown
**Test audit, Customer Returns (whole PRD): 2 of 2 gaps fixed.** Every criterion is now Adequate or better except AC-RET-04 (blocked). Re-graded by a fresh reviewer; full suite green (`pytest`).

**Your action:** ask the shipping carrier for a test account; AC-RET-04 can't be tested without one.
**Recommended:** take AC-RET-05 (high risk) to Strong.
```

A fixing chat that leaves rows for the next:

```markdown
**Test audit, Customer Returns (whole PRD): 5 of 12 gaps fixed.** The 7 left are all Weak, none high risk. Re-graded by a fresh reviewer; full suite green (`pytest`).

**Or:** say "accept the remaining Weak rows" to close the audit with them recorded as accepted.
```

---

## Assessment Checklist

The sub-agent follows this. Read everything from disk; work from no one's memory or summary.

For each criterion:

1. **Required parts, from the requirements alone, before opening a test.** Read the criterion in the PRD, the assumption entries and technical-design sections it depends on, and in a phase audit the phase document. Write down each required part: one thing a test could observe that must hold for the criterion to be met. Derive them from the requirements, never from the code. Work through these in order, and keep only what the requirements state or plainly imply:
   - **Each outcome it states,** the success path first, then each error or rejection it names.
   - **Each variant it covers** (providers, channels, entry points, user roles, the states it names), one part per variant.
   - **Each category of input or data it treats differently,** one part per category, including the invalid ones it says are rejected or ignored.
   - **Each stated limit** (a maximum, a minimum, a cutoff date or time): the value at the limit and the first value past it, two parts.
   - **Each combination of conditions that changes the outcome,** where the criterion's rule depends on more than one condition: one part per combination that leads to a different result.
   - **Each allowed change of state,** where the criterion describes something moving through states, and each change it forbids.
   Mark each part **stated** (the criterion or its governing documents say it) or **implied** (an edge or error case it implies but doesn't state). A criterion with many parts is normal; one may need two dozen tests.
2. **Map tests to parts.** Search the tests by label, by the names the criterion uses, and by the code the technical design names for it. List under each part the tests that exercise it; one test may cover several parts. Note the files that implement the criterion.
3. **Check each mapped test.** Is it skipped, marked expected to fail, or outside what the project's normal test run collects? Read that from the code; assume the suite otherwise passes. Does it reach the boundary its part is about, or mock it? Do its assertions pin that part's outcome with values taken from the requirements? Would it fail if that part broke? A part counts as covered only when a test in the normal run reaches its boundary, pins its outcome with values from the requirements, and would fail if it broke.
4. **Grade** by "The Grades", or give a status (Not implemented, Person-checked, Superseded, Changed outside the requirements). Add `blocked: <what is missing>` when the criterion's boundary has no non-production counterpart. Report the count: stated parts covered out of stated parts identified.
5. **Risk.** High if a silent break would cost money, corrupt or lose data, expose private data or access, or do something irreversible outside the system.
6. **Gap and fix.** For anything below Strong: each uncovered or weakly covered part, and the smallest fix that would cover it, at the level and against the resource it needs.
7. **Red-check target.** For anything graded Adequate or better: the file and function a red check should break for the criterion's riskiest stated part, and how (Step 3, "How").

Report one record per criterion with these fields. Observations outside the criteria are not findings; leave them out. **Do not fix anything.**

---

## Rules and Constraints

### DO

- Take the criteria from the document the user points at, and grade every one by the same question: would the suite notice if it broke?
- Have the assessors read the requirements from disk themselves and list each criterion's required parts, by the checklist's steps, before opening a test
- Red-check every high-risk criterion graded Adequate or better and a sample of the rest, and widen the checks when one stays green
- Close the audit chat at Step 4 unless the gaps are few, and fix in tier order, a batch per chat, until every criterion is Adequate or better or the user accepts it; carry the rest in `test-audit.md`
- Assume the suite passes: run only the tests a red check or a fix needs, and the full suite only as a fixing chat's commit gate
- See every new or strengthened test fail before counting it
- Re-grade remediation with a fresh sub-agent, never by the chat that wrote the tests

### DO NOT

- Infer acceptance criteria from code, or audit work that has none written down
- Count a skipped, failing or never-collected test as evidence
- Grade Strong without red checks on every stated part
- Red-check a test that reaches production, or break a guard on whether, where or how much the code writes or sends
- Overwrite a file someone else edited during a red check, or leave a check unrestored
- Plan remediation in phase documents, a PRD amendment or a change directory (a missing `Superseded by:` pointer pair the conflict check finds is not remediation, and a delivery gap's completion phase is build work, not test remediation)
- Write a test that traces to no criterion in scope, or fix pre-existing failures unrelated to the criteria
- Weaken a test to make it pass against code that breaks the criterion
- Work the Strong tier unasked
- Accept a row on your own judgment, accept a Missing, failing or high-risk row the user didn't name, or accept a row waiting on delivery
- Skip a red check, the re-grade or the full suite to fit more rows into a chat, or move a row to Waiting for lack of room
- Keep working a row marked `stuck` before the user says how

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `test-hardening` | The per-session pass this skill checks after the fact. Same grades, same scope boundary, same evidence rules: it hardens one session's work, and this skill grades and repairs the finished whole. |
| `implement-from-requirements` | Builds completion phases, then hands off through a fresh delivery audit before returning here. Its per-phase test hardening does not replace this audit. |
| `delivery-audit` | Runs before this skill at the close of a split PRD, and hands off to it when it finds no gaps. Same statuses and conflict rules; a delivery gap this skill finds later becomes its own completion phase, in the same form. |
| `phase-split` | A phase document's "Acceptance criteria covered" list is the scope of a phase audit, and its rule that every criterion lands in exactly one phase is what makes a PRD audit add up. |
| `implementation-lifecycle` | Remediation runs under its session discipline; the audit steps are the review mode it describes. It names `test-audit.md` as this skill's own record, never a destination for discovered work. |
| `engineering-principles` | The testing evidence standard the grades encode. |
| `wall-clock-awareness` | Loaded when a test this skill runs takes more than about two minutes; it cuts what each run costs. |
| `deliverable-review` | Runs on any implementation change remediation makes, before the re-grade. |
| `continuation-prompt` | Writes the next chat's prompt when the audit chat closes, when remediation outlasts one chat, or when a completion phase this audit added needs building, with `test-audit.md` as the governing document. |
| `pre-commit-validation` | The commit boundary for remediation's tests, fixes and the audit file. |

---
name: delivery-audit
description: Independent check, once every planned phase of a PRD is closed, that each acceptance criterion is actually built — every required part present and reachable from the entry point a user or calling system would use, not logic nothing calls. Sub-agents read the criteria from the PRD themselves and trace each one through the code; the main agent confirms every gap before acting on it. It writes no code. Gaps become completion phases at the end of the plan, each marked at its top as added by the delivery audit, which implement-from-requirements builds like any other phase; test-audit follows once nothing is left to build. Use when the last phase of a split PRD closes, when implement-from-requirements hands off to it, or when the user asks whether a finished PRD or phase delivered everything it promised. Not the review inside a build (deliverable-review), not a test audit, and never for work without written acceptance criteria.
user-invocable: true
---

# Delivery Audit

An independent check, once a PRD's planned phases are all closed, that every acceptance criterion is built. It asks one question of each criterion: **could a user, or the system the criterion is about, get this behavior from the code as it stands?** It grades nothing about tests; `test-audit` does that next. Gaps become completion phases at the end of the plan, built by `implement-from-requirements` like any other phase.

Every phase already ran `deliverable-review`. That is not enough on its own:

- **Each review saw one phase's diff.** Nothing re-checks a criterion a later phase broke, a cross-cutting criterion across all the phases, or a part that fell between two of them.
- **A phase's Closed line is written by the session that built it.** Its own wrap-up decided the criteria were met.
- **Gaps are usually partial, not total.** The logic exists but nothing calls it; the main path works and the error case the criterion names doesn't; one of two channels is wired. A missing feature is easy to notice, a half-wired one is not.

The order at the end of a split PRD is fixed: this audit, then `implement-from-requirements` on any completion phases it added, then `test-audit`. Building comes before proving, so the test audit never grades tests for behavior that isn't there yet.

---

## When to Use

- The last planned phase of a split PRD has closed. `implement-from-requirements` hands off here with a prompt.
- The user asks whether a finished PRD, split record or phase delivered every criterion.

**Do NOT use this skill for:**

- The review inside a build. That is `deliverable-review`.
- Test evidence. That is `test-audit`, which runs after this one.
- Work with no written acceptance criteria. This skill checks code against criteria somebody wrote; criteria reconstructed from the code would bless whatever was built.
- An unsplit PRD, unless the user asks: its one build reviewed the whole PRD.

---

## Scope: Which Criteria Are Audited

The document the user or the handing-off skill points at fixes the criteria, exactly as in `test-audit` ("Scope: Which Criteria Are Audited"): a phase document's "Acceptance criteria covered" list, a split record's labels (the union of its children's), or every criterion in a PRD or change directory, retired labels excepted.

- **A criterion with a `Superseded by:` line is left out,** listed as superseded with its pointer. One with `Superseded in part by:` is checked on the part still in force (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion").
- **Only closed phases are checked.** A criterion owned by a phase with no `**Closed:**` line is listed as Not built yet and left out, and so is one an open completion phase completes. Planned work that hasn't run is not a gap.
- **A cross-cutting criterion** (one a phase document lists as also applying to its work) is checked across every closed phase that lists it.

---

## The Statuses

| Status | Meaning |
|---|---|
| **Implemented** | Every required part exists and is reachable from the entry point the criterion is about: the route, command, scheduled job, screen, message handler or export a user or another system would use. |
| **Partly implemented** | Some required part is missing or unreachable: logic nothing calls, a stub (a hardcoded value, a TODO, a not-implemented branch), a flag that is off everywhere, an error or boundary case the criterion names left unhandled, one of several required outcomes absent, or a value the requirements fix (a limit, an amount, a wording, a recipient) that the code gets wrong. |
| **Not implemented** | No code does any part of it. |
| **Waiting on a human action** | Built as far as code can take it; the rest is an entry in a `## Pending human actions` section (a switch flipped in production, a credential issued). Not a gap; named in the wrap-up. |
| **Superseded** | A later PRD replaced it; the row shows the pointer. |
| **Changed outside the requirements** | The code deliberately does something else a person could have chosen, and no document records the change. Shipped behavior stands (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"); named in the wrap-up for the user to record. |
| **Not built yet** | Owned by a phase that has not closed. |

**Partly implemented and Not implemented are gaps.** Only gaps lead to work.

The bar is delivered behavior, not proof. An Implemented criterion with no test passes here; `test-audit` grades its evidence. This audit reads and traces the code, which can miss a part that looks wired and fails when run. The test audit's new tests and red checks are the second net, and the test audit turns anything they find unbuilt into a completion phase of its own.

---

## Process

The assessment is review mode within the criteria in scope (`implementation-lifecycle`). Writing the completion phases is planning under the same skill's session discipline (No Loose Ends, the Materiality Gate): a gap is a criterion's missing part, never an improvement noticed on the way.

### Step 1: Scope and baseline

1. Resolve the scope (above) and list the criteria by label. Open the first response with one lineage line: `Delivery audit of <PRD title>, <Phase id — title, or whole PRD>`. It is also the `serves:` line of this session's marker, whose START is written before the first edit (`implementation-lifecycle`, "Session Markers").
2. Note HEAD (`git rev-parse --short HEAD`). The audit checks the code at that commit; when files in scope have uncommitted changes, the report says so.

### Step 2: Fresh-eyes assessment (sub-agents)

Launch general-purpose sub-agents in parallel, each with up to about eight criteria grouped by theme or phase, so related criteria share one reader. Give each:

- The labels to check, and the paths of the PRD, its assumptions document, its technical design and the phase documents it needs. **Not** the criterion text, a summary of the work, or `test-audit.md`: it reads the requirements from disk. The phase documents set scope; a Closed line in one is a claim to check, not evidence.
- The repository root.
- The absolute path of this `SKILL.md`, with the instruction to follow its **Assessment Checklist** and change nothing.

### Step 3: Confirm every gap (main agent)

A gap costs a whole build session, so a false one is expensive. For every Partly implemented or Not implemented record:

1. **Read the code yourself** at the places the record names, and confirm the missing part really is missing or unreachable. A part found implemented after all moves the row to Implemented.
2. **Run the conflict check** for the confirmed gaps (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"; one check covers every row). A later PRD changed the criterion: add the missing pointer pair and list the row as Superseded. The code deliberately does something else a person could have chosen: list it as Changed outside the requirements. Otherwise it is a gap.
3. **A gap the requirements don't settle** (the criterion needs a value or rule nobody wrote down) is a business question. Write it to the assumptions document with `assumptions-document-writing`; the completion phase builds on the proposed answer, because an assumption is a green light.
4. **A gap that is costing money, data or production correctness now** stops the audit: "Critical finding, stopping to surface."

### Step 4: Write the completion phases

With no gaps, go to Step 5. **Before every planned phase is closed** (a phase audited on request mid-PRD), write no completion phase: add each gap to the next open planned phase as a `## Carried forward from Phase N` section (`implementation-lifecycle`), which that phase's build then delivers. Otherwise load `phase-split` and follow its "Completion Phases" section, which owns their ids, file names, the line that marks them at the top, and the template. This skill decides what goes in them:

- **Group the gaps by the code they share.** Gaps in one capability or one area of code go in one phase. Size the set by `phase-split`'s Session Capacity Calibration; usually every gap fits one completion phase.
- **Each gap gets one line under "What the audit found missing"**, from the confirmed record: what is missing, where (file and function, and the entry point), so the build starts from the finding instead of auditing again.
- **Nothing but gaps.** No improvement, refactor or test work goes in a completion phase. Test gaps are `test-audit`'s.

### Step 5: Record and hand off

1. **Write the next chat's prompt** with `continuation-prompt`, before the commit so the edits it makes to the governing documents ride in it. Gaps: `implement-from-requirements` on the first completion phase (mid-PRD, the next open planned phase, as usual). No gaps: `test-audit` on the same scope. Either way a fresh chat: this one never builds what it found, and the build gets the implement chain's review and test hardening.
2. **Commit** per `pre-commit-validation`: the completion phases or carried-forward sections, any plan-table rows, pointer pairs and assumption entries. The subject starts `delivery audit complete` and then names the scope in parentheses, so later sessions can find it and tell a whole-PRD audit from a narrower one: `docs(customer-returns): delivery audit complete (whole PRD), 2 criteria incomplete, Phase 7 of Customer Returns added`, or `docs(customer-returns): delivery audit complete (whole PRD), every criterion implemented`. A narrower audit reads `(phase 3)`. `(whole PRD)` is only for an audit run with every planned phase closed; one run on the whole PRD earlier names the phases it covered, `(phases 1 to 4)`, so it is never mistaken for the close-out audit. The `docs(...)` scope is the one this PRD's commits already use, usually its directory name. When the audit changed no file, commit it empty, `git commit --allow-empty --only -m "<message>"`, which commits nothing else and leaves another session's staged files staged. Put each Changed outside the requirements row in the body, one line each. Committed by default, never pushed by default (`pre-commit-validation`, "Who Commits").
3. **Present the prompt** after the commit, with its hash.
4. **Append DONE** to this session's marker, naming the terminal state.

---

## What the Chat Shows

Only what needs attention: no list of what was built, no account of how the audit ran. A headline with how many criteria have gaps; a table of just those, each with what's missing in one line; the user's actions (Changed outside the requirements and Waiting on a human action rows); then the commit and the next chat's prompt. With no gaps, the headline, the commit and the prompt are the whole report.

```markdown
**Delivery audit, Customer Returns (whole PRD): 2 of 14 criteria aren't fully built.** Added phase 7 to build them.

| Criterion | Status | What's missing |
|---|---|---|
| AC-RET-03 — A return can cover several items | Partly implemented | The returns API takes one item and the form sends one |
| AC-RET-07 — The refund method is shown before confirming | Not implemented | Nothing shows it on the confirm screen |

**Your action:** record AC-RET-09 in the PRD. The code emails the return label instead of showing it on screen, and no document says that was decided.

**Next:** build phase 7 in a fresh chat with the prompt below; the test audit follows.
```

---

## Assessment Checklist

The sub-agent follows this. Read everything from disk; work from no one's memory or summary.

For each criterion:

1. **Required parts, from the requirements alone.** Read the criterion in the PRD, the assumption entries and technical-design sections it depends on, and in a phase audit the phase document. Before opening any code, write down each required part as behavior someone could observe, including every error or boundary case the criterion states.
2. **Find the entry point.** Where would a user or calling system get this behavior: a route, command, scheduled job, screen, message handler, export? The technical design usually names it.
3. **Trace each part from the entry point to the code that does it.** Record the file and function for each part and the call path that reaches it. A part is built only when that path exists. Code nothing calls, a stub, or a branch behind a flag that is off everywhere is not built.
4. **Check the values the requirements fix:** limits, amounts, wording, ordering, recipients, timing. The code must use the required value, not a near one.
5. **Status** by "The Statuses". For Partly implemented and Not implemented, list each missing part in one line, with the file and function where it belongs.

Report one record per criterion with these fields. Do not judge tests, style or structure, and run nothing that writes. Observations outside the criteria are not findings; leave them out. **Do not change anything.**

---

## Rules and Constraints

### DO

- Take the criteria from the document pointed at, and have the assessors read the requirements from disk and derive each required part before opening code
- Trace every part from the entry point a user or calling system would use
- Confirm every gap yourself, and run the conflict check on the gaps, before writing a completion phase
- Put the gaps in completion phases written by `phase-split`'s rules, marked at the top as added by the delivery audit
- Hand the build to `implement-from-requirements` in a fresh chat, and the proof to `test-audit` once nothing is left to build

### DO NOT

- Write or change implementation code or tests
- Infer acceptance criteria from code, or audit work that has none written down
- Count a criterion owned by an unclosed phase as a gap
- Revert, or plan to revert, shipped behavior a person deliberately chose; name it for the user to record
- Put a gap anywhere but a completion phase (or, mid-PRD, the next open planned phase): not a change directory, a ticket, `test-audit.md`, a reopened phase, or the Closed phase's own document
- Put anything in a completion phase that no criterion requires
- Grade tests

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `implement-from-requirements` | Hands off here when the last planned phase of a split PRD closes, and builds the completion phases this skill adds. When it closes the last of those, it hands off to `test-audit`. |
| `phase-split` | Owns the form of a completion phase ("Completion Phases"): its id, file name, marker line and template. Its rule that every criterion lands in exactly one phase is what lets this audit name the phase that owns each gap. |
| `test-audit` | Runs after this skill. Same scope rules and the same rules for superseded and changed criteria; it grades whether the tests prove each criterion, and writes a completion phase of its own, in the same form, for a delivery gap it finds later. |
| `deliverable-review` | The per-session check this skill repeats across the finished whole. |
| `implementation-lifecycle` | The conflict check and the shipped-behavior rule that decide whether a gap is a gap; the session discipline that keeps completion phases to existing scope. |
| `assumptions-document-writing` | Where a gap the requirements don't settle goes. |
| `continuation-prompt` | Writes the next chat's prompt: the first completion phase's build, or the test audit. |
| `pre-commit-validation` | The commit boundary for the completion phases and the audit's record commit. |

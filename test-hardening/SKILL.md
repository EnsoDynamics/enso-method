---
name: test-hardening
description: Final pre-commit pass that strengthens the tests for the work just implemented — verify every acceptance criterion has credible test evidence, upgrade weak or mock-reliant tests to prove real behavior, add what's missing, and leave the full suite green. Bounded strictly by the acceptance criteria of the work being hardened — it never grows tests for behavior outside them. Runs after deliverable-review as the third step of the implement → review → harden chain. An action skill, not an audit — it improves the tests rather than producing a report.
user-invocable: true
---

# Test Hardening

The third step of the standard implementation chain: implement (`implement-from-requirements` or `implement-from-discovery`) → `deliverable-review` → **`test-hardening`**.

Deliverable review re-checks the work that was produced. This skill turns to the tests themselves and asks a different question: **if this suite passes, do we actually have credible evidence that the acceptance criteria hold?** Then it closes whatever gap it finds.

This is an action skill, not an audit. It does not produce a coverage report or a graded findings document as its deliverable — the assessment happens internally, and the output is a stronger test suite. Meaningful improvement beats exhaustive analysis: a session that converts two mock-reliant tests to real integration tests and adds one missing acceptance-criterion test has succeeded, even if it didn't touch everything.

---

## When to Use

- Automatically, as the final step of `implement-from-requirements` or `implement-from-discovery` (after deliverable review completes)
- Manually, after any implementation session, when the user says "harden the tests," "are the tests good?", or "button this up for commit"
- Standalone against a recently implemented feature or phase whose tests were never hardened

**Do NOT use this skill for:**

- A whole-repo test audit divorced from a specific piece of implemented work — this skill anchors on the requirements of the work just done, not on generic coverage metrics
- An independent audit of a finished phase's or PRD's test evidence, with a written grade for every criterion — that is `test-audit`
- A substitute for running tests during implementation — the implement skills own that; this is a second, deliberate pass after review

---

## Invocation Context: The Same Chat, Not a Fresh One

**The expected path is the same chat that just did the implementation.** The implement skills auto-run this pass right after deliverable review, and there is no reason to start over. The fresh-eyes requirement is already satisfied without a new chat: Step 2 delegates the assessment to a sub-agent that reads the requirements, code, and tests from disk with no conversation history. A fresh chat buys nothing the sub-agent doesn't already provide.

It also costs something real. The main agent's accumulated context is what carries the **scope boundary** — which acceptance criteria were in scope for *this* phase rather than the whole PRD, what deliverable review already changed, and what was already dismissed as immaterial. A fresh chat has to reconstruct all of that, and reconstructing it wrong is precisely the scope-creep failure this skill exists to prevent.

**If the pass does start in a fresh chat**, it needs two inputs before any hardening begins — and they carry different bars:

1. **The requirements — provided by the user, never inferred. This is a hard gate.** The phase doc or PRD whose acceptance criteria bound the pass (for discovery-driven work, a one-line statement of what the fix was meant to do). If the user hasn't pointed at it, stop and ask — do not start the assessment without it, and never reconstruct acceptance criteria from the diff. Deriving "what the tests should prove" from "what the code does" is circular: it blesses whatever was built, and it dissolves the scope boundary this skill depends on.
2. **The changeset — resolved from any reasonable pointer.** If the work is uncommitted (the usual case), `git status` / `git diff` finds it exactly as it would in-session, no pointer needed. If it was committed, an explicit SHA or range is ideal but not required: "the last commit," "what I committed this morning," "the phase-3 commit" are all enough — resolve the pointer with `git log`, then confirm the resolved commit's files and message actually match the described work before proceeding. Ask only when resolution genuinely fails: several candidate commits fit, or the one found doesn't look like the work described. Being pointed in the right direction is enough; guessing without a pointer, or proceeding unsure you found the right commit, is not.

A workable fresh-chat invocation: *"Run test-hardening on `<path to the phase doc or PRD>` — the implementation is in the last commit."*

One caveat grows with distance from the implementation. Step 4's triage of a failing test into "regression this work caused" versus "pre-existing debt" assumes the suite's starting state is known. Hardening a commit from days ago, with unrelated work landed in between, makes that call unreliable. Establish the baseline explicitly in that situation — run the suite before changing anything, or check the parent commit — rather than assuming a failure is pre-existing.

---

## The Scope Boundary: Acceptance Criteria Are the Whole Test Universe

This is the rule that keeps the skill from going off the rails, so it comes before everything else.

**Every test this pass adds or strengthens must trace to an in-scope acceptance criterion** of the phase/PRD being hardened (or, for discovery-driven work, the stated intent of the fix). The acceptance criteria define what "good tests" means here — nothing else does.

The failure mode this prevents is specific and expensive. Hardening looks closely at code, and looking closely surfaces discoveries: adjacent behavior with no tests, pre-existing oddities, edge cases nobody asked about. Writing a test for any of these is scope creep **twice over** — the test itself is unrequested work, and when it fails it demands fixes to code this session never touched. That chain (found a thing → wrote a test for it → now fixing the thing to make the test pass → which surfaces more things) is the off-the-rails loop this boundary exists to prevent.

How the boundary applies in practice:

- **The assessment may look broadly; the action may not.** The sub-agent examines all tests covering this session's work, but every fix the main agent makes must trace to an in-scope criterion. A discovery that doesn't is an observation, and the default disposition for an observation is **dismiss — silently, no wrap-up mention** (this is the Materiality Gate; `implementation-lifecycle` has the full treatment, but the rule stands on its own here).
- **"Edge case" means an edge case *of a criterion*.** Boundary conditions and error paths of required behavior are in scope. An edge case of behavior no criterion requires is a new requirement being invented mid-hardening — out.
- **Full-suite failures get triaged by cause, not adopted wholesale.** A test your change broke is a regression — material, fix it. A test that was already failing before this session's work is pre-existing debt — out of scope; mention it in one line so the user knows the suite wasn't fully green when you arrived, and move on. Never "fix" it here, and never write new tests around it.
- **One exception, and only one.** A genuinely critical finding — money at risk, data loss, production breakage — stops the session and gets surfaced immediately regardless of scope. The boundary is for the immaterial; it is never a reason to unsee something dangerous.

---

## What "Hardening" Means (and What It Doesn't)

Hardening raises the *quality of evidence*, never the test count for its own sake. The philosophy, stated in full so this skill stands alone:

- **Prove risks, not test counts.** The goal is the smallest test portfolio that gives credible evidence the acceptance criteria hold — not one test per criterion, not a test per function, not a coverage number. One well-chosen integration or workflow test may prove several criteria at once; a high-risk criterion may need tests at more than one level.
- **An acceptance criterion with no verifying test is a gap.** Add the smallest test that credibly proves it.
- **A test that passes without proving anything is weak.** Asserting "didn't crash" or "not null" when the requirement specifies concrete behavior is the most common form. Weak tests get strengthened to assert the actual expected values.
- **Mocks are lies that make tests pass.** A mock proves your code handles the response *you wrote*, not the response the real system returns — auth, field names, response shape, all unverified. If the risk under test *is* the external interaction (the API contract, the query, the serialization), a mock there proves nothing: convert it to the real resource in a sandbox/dev environment, within the environment rules below.
- **Mocks keep a narrow, legitimate place:** destructive operations you can't safely perform, expensive or rate-limited third-party APIs where every run costs money, and simulated failure conditions (timeouts, 500s) you can't reliably trigger for real. Even then, keep the mock at the smallest boundary needed and never treat mock-only coverage as proof an integration works — note the limitation in the test.
- **Integration tests carry more weight than unit tests here.** Unit tests earn their place for isolated deterministic logic — calculations, transformations, parsing. The hardening pass leans toward tests that exercise real systems, because that's where unearned confidence hides.
- **Never add a ceremonial test.** Before adding any test, name the failure it would catch, the criterion it traces to, and why no existing test already catches it. If you can't do all three, don't add it.
- **Never weaken an assertion to get green.** If hardening surfaces a failure, that's the skill working — root-cause it (see Step 4).

---

## Process

### Step 1: Establish the Requirements Baseline

Anchor the pass on what the session was supposed to deliver:

1. Identify the governing requirements — the phase doc's acceptance criteria, the PRD's acceptance criteria, or (for discovery-driven work) the stated intent of the fix. This list is the scope boundary for everything that follows.
2. Run `git diff --stat` / `git status` to see what code changed this session.
3. Identify the test suite, how it runs, and which tests relate to the changed code.

If invoked standalone and the user has not pointed at the requirements, stop and ask (the hard gate under "Invocation Context: The Same Chat, Not a Fresh One") — a one-line answer is enough.

### Step 2: Fresh-Eyes Test Assessment (sub-agent)

The implementing agent already judged its own tests adequate once — during implementation. That's the bias this step breaks, the same way `deliverable-review` uses fresh eyes on the deliverable.

Launch a single general-purpose sub-agent with:

- The acceptance criteria (or stated intent) from Step 1
- The list of changed files and the relevant test files
- Instruction to read this skill's `SKILL.md` — pass the absolute path of the file this skill was loaded from — and follow the **Assessment Checklist** section
- **Instruction to re-read the requirements, changed code, and tests from disk** — not from conversation memory
- **Report findings as a structured list; do NOT fix anything** — the main agent hardens after collecting results

### Step 3: Prioritized Hardening (main agent)

Present the assessment in one short list ("Assessment: AC-3 has no test evidence, the payments client is mocked in the two checkout tests, four assertions are not-null-only. Hardening now."), then fix in priority order:

1. **Acceptance criteria with no credible evidence** — add the missing test(s)
2. **Tests that lie** — convert mocks at the boundary under test to real resources
3. **Weak assertions** — strengthen to assert specific expected values and shapes
4. **Genuinely risky edge cases of the acceptance criteria** — error paths and boundary conditions of *required behavior* with real regression risk. Not edge cases of adjacent behavior no criterion covers — see the scope boundary.

Every fix in every tier must trace to an in-scope criterion. Work down the list until the improvement is meaningful, not until it's exhaustive — judgment call, biased toward covering everything in tier 1 and 2. If the assessment comes back clean (every criterion has credible evidence, no unjustified mocks, assertions are real), say so in one line and stop — do not manufacture work to justify the pass.

### Step 4: Run the Full Suite

Run the complete suite, not just the new or changed tests. Triage every failure by cause:

- **A hardened test found a real bug in this session's work** → fix the implementation. This is the skill's best outcome, not a nuisance.
- **The test itself is wrong** → fix the test to assert the genuinely correct behavior.
- **A pre-existing test unrelated to this work was already failing** → out of scope. One-line mention to the user; do not fix it here.
- **Never** silence, skip, loosen, or delete a failing test just to get green — that inverts the entire purpose of the pass.

Re-run after fixes until green (pre-existing unrelated failures noted and excluded).

### Step 5: Wrap-Up

Keep it brief — no FYIs or observation inventories; dismissed discoveries stay dismissed:

1. One or two sentences on what was hardened (e.g., "Added integration tests for AC-2 and AC-5, converted the mocked email-provider client to its sandbox account, strengthened 3 assertions — full suite green"), not a test-by-test inventory.
2. Confirm the full suite passes, naming the command that ran.
3. Stage the test files (and any implementation fixes from Step 4), and update the proposed commit message if one was already presented.
4. Note explicitly that test hardening was performed, so the user doesn't re-run it.

---

## Environment Rules for Real-Resource Tests

The rules that govern where hardened tests are allowed to touch real systems:

- **Anything a test writes, it writes to non-prod.** Sandbox/dev environments only — sandbox writes are the normal, expected mode for integration tests. Tests never mutate production data, no exceptions.
- **When the service has no non-prod environment yet**, where the project allows it (`engineering-principles`, "Production Data"), production may be used **strictly read-only**: GETs, SELECTs, and production-supported `--dry-run` planning paths. Write paths on such a service stay verified at the unit level (with the narrow mock allowances above) until a dev environment exists. This is an exception for services without one, not a general option — flag the missing environment in the wrap-up as worth standing up.
- **Tag test-created data** (`is_test_data` or equivalent) in any real system so it can be identified and cleaned up.
- **Fixture data is checked in** — repo-relative paths, never ad hoc files from a developer's machine, and never a dependency on an unexplained record that happens to exist in some environment.

---

## Assessment Checklist

This is what the sub-agent follows. **Re-read the requirements, the changed code, and the test files from disk before evaluating — do not work from memory.** The acceptance criteria provided in the prompt are the scope boundary: findings must concern evidence *for those criteria*, not adjacent behavior.

### 1. Acceptance-Criterion-to-Evidence Map

For each in-scope acceptance criterion (or the stated intent, for discovery work), identify which test(s) prove it and grade the evidence. The grades answer one question, *if this criterion's behavior broke, would the suite notice?*, and are the same four `test-audit` uses:

- **missing** — nothing exercises this criterion
- **weak** — tests exist, but some required part could break without any test failing: not-null, didn't-crash or count-only assertions; expectations copied from the implementation rather than derived from the requirement; a mock standing in for the boundary the criterion is about; or a part the criterion states, including an error case it names, with no test
- **adequate** — every required part would fail a test if it broke on its main path, tested at the boundary it is about; named gaps remain (edge or error cases the criterion implies, or the evidence was never seen to fail)
- **strong** — adequate, with those edge and error cases covered, and a test seen to fail with each required part deliberately broken

Grade a criterion by its least-proven required part; it is missing only when nothing exercises any part. This pass runs no red checks, so its grades stop at adequate unless this session saw a test fail with the behavior broken. One test may serve several criteria; a criterion may need several tests. Grade the evidence, not the count.

### 2. Mock Inventory

List every mock, stub, patch, or fake in the tests covering this work. For each: is it within the narrow allowances (destructive operation, expensive/rate-limited third-party API, simulated failure condition)? Everything outside those allowances is a conversion candidate — especially mocks of systems that have a sandbox/dev environment available.

### 3. Assertion Strength

Flag tests whose assertions don't pin down the required behavior: not-null-only checks, count-only checks where content matters, assertions against values computed by the same code under test, and broad `assert result` patterns.

### 4. Risky Edge Cases of the Criteria

Which error paths, boundary conditions, or malformed-input cases *of the required behavior* carry real regression risk and have no test? Every flagged case must name both the failure it would catch and the criterion it belongs to. Do not flag edge cases of behavior outside the criteria, and do not enumerate hypothetical inputs for completeness.

### 5. Test Hygiene

- Fixture data checked into the repo, referenced by repo-relative paths
- No test depends on unexplained records that happen to exist in some environment
- Test-created records in real systems are tagged for identification/cleanup
- The suite runs green from a clean invocation with documented setup (correct AWS profile, `.env`, etc.)

### 6. Report

Return a structured list of findings, ordered: missing evidence first, then unjustified mocks, then weak assertions, then edge cases, then hygiene. For each finding: the criterion or test it concerns, what's wrong, and the smallest fix that would make the evidence credible. Observations outside the criteria are not findings — omit them. **Do not fix anything.**

---

## Rules and Constraints

### DO

- Anchor on the acceptance criteria of the work just implemented — they are both the definition of "good enough tests" and the outer boundary of what gets tested
- Use a fresh-eyes sub-agent for the assessment, then harden in the main agent
- Prefer real resources in sandbox/dev over mocks; treat unjustified mocks as the highest-value conversions
- Name the failure each added test would catch — and the criterion it traces to — before adding it
- Root-cause every failure the hardened suite surfaces — fix the code or fix the test, whichever is genuinely wrong
- Stop when the improvement is meaningful; say so in one line if the evidence is already credible

### DO NOT

- Write a test for anything that doesn't trace to an in-scope acceptance criterion — discoveries outside the criteria are dismissed silently, not tested (critical findings excepted)
- Fix pre-existing test failures or test debt unrelated to this session's work — one-line mention, move on
- Produce an audit report as the deliverable — the deliverable is the improved suite
- Add tests to hit a count, cover trivial accessors, or duplicate the same assertion at every layer
- Weaken, skip, or delete a failing test to get green
- Mutate production data from any test, ever — writes go to sandbox/dev only
- Re-run deliverable review — that already happened earlier in the chain; this pass has a different subject

---

## Relationship to Other Skills

This skill is self-contained — the testing philosophy and scope boundary above are the complete rules. It connects to the other skills like this:

| Skill | Relationship |
|-------|-------------|
| `implement-from-requirements` | Auto-runs this skill after deliverable review completes — the third step of its chain. Its test phase builds the initial portfolio; this skill hardens it with fresh eyes. |
| `implement-from-discovery` | Same chain, discovery-triggered work — auto-runs this skill after its deliverable review; the baseline is the stated intent of the fix rather than PRD acceptance criteria. |
| `test-audit` | The independent check once a phase or PRD is finished: it grades every criterion's evidence on the same four grades, across all the sessions that built it, and fills the gaps. This skill hardens one session's work; that one audits the finished whole. |
| `deliverable-review` | The preceding step. It verifies the deliverable matches intent; this skill verifies the tests prove the requirements. Run it first — its fixes change code that tests must cover. |
| `engineering-principles` | The testing evidence standard this skill enforces. This skill's rules are a self-contained restatement, deliberately aligned; test tooling and framework conventions come from the house engineering standards the project names, if any. |
| `implementation-lifecycle` | The umbrella methodology — its Materiality Gate and No Loose Ends discipline are the general form of the scope boundary and wrap-up rules stated natively here. |
| `pre-commit-validation` | Runs at the commit boundary after this skill — staging hygiene, secrets scan, diff sanity. |

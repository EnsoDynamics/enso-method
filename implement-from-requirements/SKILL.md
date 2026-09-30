---
name: implement-from-requirements
description: Default implementation skill — load full PRD and Technical Design context, size the work for a single AI session, split it into phases if too large (via phase-split, without stopping to ask) and carry on with the first leaf phase in the same chat, then implement, test, run deliverable review, and harden the tests. The "go build it" skill that runs after the requirements are ready.
user-invocable: true
---

# Implement From Requirements

The default skill for taking implementation-ready requirements and producing working, tested code.

This skill assumes the requirements have already been refined (typically via `autonomous-requirements-refinement`, or `implementation-readiness-check` for a human checkpoint). Its job is to load full context, decide whether the work fits in one AI session, phase it if not, then implement, test, and verify the deliverable.

This skill is one procedural arm of the `implementation-lifecycle` framework — **read that skill first if it isn't already loaded.** It's the umbrella for the whole methodology: the four entities (PRD, Technical Design, Assumptions, and Phase Documents when split), the confidence thresholds, and the session discipline (disposition of loose ends, the ask-gate, no hollow promises, the continuation test) that this entire session runs under. A user pointing you at a requirements doc should never need to name another skill — loading this one pulls the whole methodology with it.

**Authorized Codex phase chains:** When the user requests sequential fresh tasks through the approved scope, load `phase-chain`. This skill still owns each phase's implementation and quality gates; `phase-chain` owns the authorized commit/push and actual successor creation. A task boundary does not revoke live standing or project-specific approval.

---

## When to Use

Use this skill when:

- The PRD and Technical Design are ready to implement against (questions resolved, assumptions captured)
- You're about to actually build the feature
- The user has said something like "implement the X PRD" or "build feature Y"
- You're being asked to implement just a single phase of a multi-phase PRD — same skill applies, just point it at the phase doc

**Do NOT use this skill when:**

- The PRD or Technical Design haven't been written yet — write those first using `prd-writing-standards` and `technical-design-writing-standards`
- There are still major unresolved questions in the readiness check — resolve them first

---

## What the User Provides

The user only needs to point you at the PRD (or a phase document, if implementing one phase of a multi-phase PRD). Examples of how a user might invoke this skill:

- "Implement the user-notifications PRD"
- "Build out the feature in `docs/prds/user-notifications/user-notifications-prd.md`"
- "Implement phase 2 of user-notifications"

**That's enough. You are responsible for discovering and loading all related context yourself** — the user should not have to enumerate every supporting document, and you should never start implementing before you've found and read everything tied to this PRD.

**What counts as "related context" (find and read all of it):**

- The PRD itself (`docs/prds/{feature}/{feature}-prd.md`, or `docs/changes/{feature}/{feature}-prd.md` — the two roots have the identical layout and are handled identically; see `prd-writing-standards`)
- The Technical Design that goes with the PRD (`technical-design.md` in the same directory)
- The Assumptions document, if one exists (`assumptions.md` in the same directory)
- Any other documents in the PRD's directory — text mockups, data model docs, data mapping documents, sample payloads, sample CSV exports, anything authored for this feature
- Documents referenced from inside the PRD or Technical Design that aren't already in the PRD directory (e.g., a linked data mapping spreadsheet, an external API spec, a referenced design doc) — follow those links and read those too
- Existing code that the Technical Design points to or that you'll be modifying

**The discriminating factor is "tied to this PRD."** A data mapping written specifically for this feature is required reading. Generic codebase documentation or unrelated background docs sitting in the repo from prior work are not — don't drown yourself in unrelated material, but also don't skim past anything that was authored for this feature.

If you suspect a related document exists but you can't find it (e.g., the PRD references "the mockups" but no mockups directory exists), surface that to the user before proceeding rather than silently implementing from a partial picture.

### When you're pointed at a partial spec, not a full PRD

Sometimes the document you're handed is a **slice** of requirements, not a self-contained PRD — a phase doc, a "mini spec" for one improvement, or any partial that assumes a larger product context it doesn't restate. Don't get hung up on what it's titled, and don't treat the slice as the whole picture. The slice tells you *what to build*; you still need the broader context that tells you *what not to break and why the system is shaped the way it is*. Before implementing, find and read that broader context, in this order of preference:

1. **A service or product overview** — a document whose job is to orient the whole service/product (names like `*-overview.md`, `service-overview`, `product-overview`, an architecture doc), or a substantive README at the repo/service root that does the same. If one exists, it's the single best source of overall context — read it.
2. **The parent PRD the slice points to.** A well-formed slice names its parent; follow that pointer and read the PRD plus its Technical Design.
3. **If there's no overview and no single parent — and especially if there are *several* PRDs** (a mature service accumulates them): do NOT read them all, that's wasteful. Read the one that best establishes the service as a whole — usually the **founding/earliest** PRD, since it tends to describe the service's purpose and architecture while later PRDs are narrow feature increments — and skim the *titles* of the rest so you know the breadth without reading each. Use judgment: if a later PRD is clearly the current architectural source of truth, prefer that one.

If you can find no orienting context at all (no overview, no meaningful README, no PRD), say so to the user before implementing rather than working blind on the bigger picture. That absence is also a **methodology gap**: a service mature enough to have standalone slice docs but no overview should grow one (a short service-overview doc, or a README section). Suggest it rather than silently pressing on.

---

## Assumed Starting State

This skill assumes the PRD and Technical Design are **implementation-ready** — they've been through `autonomous-requirements-refinement`, or `implementation-readiness-check` for an explicit human checkpoint. Gaps and questions have been resolved, and any remaining business uncertainties are captured in an assumptions document.

The skill does NOT preemptively run a readiness check. That would burn context and tokens for the common case where the user has already done the refinement work — and the user has explicitly chosen this skill to *implement*, not to re-validate.

**If during Phase 1 (loading context) you find the docs are clearly under-baked** — vague acceptance criteria, multiple TBDs, missing technical design sections, obvious questions that haven't been addressed and aren't captured as assumptions — pause and recommend the user run `autonomous-requirements-refinement` before continuing. Catch this in Phase 1, before any implementation work begins.

**Don't add a mid-implementation guard for this.** Some uncertainty only surfaces during implementation — the readiness check wouldn't have caught it either, so asking "did you run the readiness check?" mid-implementation isn't useful. Handle that uncertainty using the pattern below.

**Handling uncertainty during implementation:**

When you hit a gap that requires an assumption, propose your own answer to the question and assess how confident you are in *that proposed answer* (not in the question itself — confidence is in your specific answer). This follows the same confidence framework documented in `implementation-lifecycle`.

The right response depends on whether the question is **technical** or **business**:

- **Technical questions** (how to implement something — architecture, integration approach, error handling, data shape, naming): investigate to raise confidence (read code, query the database, test the API, check existing patterns). Then proceed with your best answer at whatever confidence it has, recording the reasoning in the commit message where it isn't obvious. Stop and ask the user only if, after investigation, you cannot put forward an answer at all — the evidence favors none of the options (`implementation-lifecycle`, Confidence Thresholds). Technical questions should **rarely** become formal assumption-document entries — the assumptions document is for decisions a business stakeholder can meaningfully validate, and most technical questions are resolvable through investigation instead. This matches the technical tier in `implement-from-discovery`.

- **Business questions** (what the system should do, what users should experience, what business rule applies, what a stakeholder would consider correct): the bar is higher — you can't unilaterally decide business rules, and **no amount of investigation can self-confirm one**. Proceed on your own only if you're 95%+ confident. Below 95%, at whatever confidence, the answer must be surfaced as a formal stated assumption for stakeholder validation, and you proceed on it. Only when you cannot put forward an answer at all do you stop and ask — the same stop as technical questions, and the same tiering `implement-from-discovery` uses. Use the `assumptions-document-writing` skill to write the entry when this happens. **Do not load `assumptions-document-writing` preemptively** — it's large; load it when you are actually writing an assumption, **and equally when you are EDITING an existing assumptions register** — recording a ruling, folding an answer, moving an item to the validated table, or touching the header. Editing in passing, without the skill, is the single largest source of format drift in these documents; read its "Editing an Existing Document" section before any such edit, including a one-line one.

This aligns with the unified confidence framework in `implementation-lifecycle`: declared assumptions are a green light to proceed, not a request for stakeholder confirmation. Stakeholders validate asynchronously.

**The assumptions document is the only surface a stakeholder decision may be routed to.** Every decision begins as a question, and the methodology never leaves a question as a question — it gets answered, declared, and built on. So an open decision without an assumption entry has not been dispositioned, regardless of what else records it.

Do not route a decision to a review page, report, dashboard, or any other deliverable. Those are disclosure surfaces: they show a reader evidence, they carry no reply mechanism, and they grow until any single item on them is invisible. A decision recorded only there does not get answered — that is measured, not theoretical (see `implementation-lifecycle`, "A Decision Needs an Assumption Entry, Always"). Recording it on such a surface as well is fine and often right; it is never a substitute.

---

## Session Discipline: No Loose Ends

This skill runs under the No Loose Ends session discipline (`implementation-lifecycle`, "Session Discipline: No Loose Ends") — **read that skill first if it isn't already loaded.** The gist: run every mid-implementation discovery through the Materiality Gate — only what's material to this phase's acceptance criteria and correctness becomes work, everything else is dismissed silently; disposition every would-be FYI/caveat that survives instead of reporting it (deal with it now, file it into the doc a future session will actually load, or ask a one-line question with a recommendation — only when genuinely blocked); never stop to ask a question when you're ≥90% confident what the user's answer would be; never end a turn announcing work you could do right now ("I'll add that test," "next X should be updated") — do it, file it, or ask; apply the continuation test — an item whose disposition the PRD's natural continuation will handle gets no individual mention, only a count in the one-line disposition ledger ("2 assumptions declared, 3 items filed to phase-4"), and the wrap-up names only what needs the user; end turns only at completion or a genuine blocker.

---

## Process

### Phase 1: Load Full Context

Read everything related to this implementation before doing anything else. Do not skim.

1. **The PRD itself** — focus on acceptance criteria, scope, and out-of-scope items
2. **The Technical Design** — focus on architecture, data flows, integration points
3. **The Assumptions document** (if exists) — treat assumptions as decided facts, not as open questions
4. **Supporting materials referenced by the PRD or Technical Design** — mockups, data mapping documents, data model docs, sample payloads, anything else authored for this feature
5. **Documents referenced from inside the PRD or Technical Design that live elsewhere** — if either links to a document outside the standard locations (a data mapping spreadsheet, an external API spec, a related design doc), follow the link and read it. Anything authored for this feature is in scope, regardless of where it lives.
6. **The phase doc** (if you were pointed at one) — note the scope it sets and which acceptance criteria it covers. A phase doc is one file per phase at every depth (`phase-2a1-{short-name}.md`; `phase-split` owns the scheme). If the doc you were handed has a `## Split into` table, it is a split parent, not an implementable phase: take its first child without a `**Closed:**` line under its title (walking down until you reach a leaf), say so in one line, and proceed with that leaf — don't stop to ask which one. If every child is closed, the parent is complete: say so and apply `continuation-prompt`'s end-of-track rule instead of building anything.
7. **Existing code referenced by the Technical Design** — read the files you'll be modifying or integrating with, plus their tests

**Required vs optional documents:**

- **PRD** — required. If it can't be located, stop and ask the user where it is.
- **Technical Design** — strongly expected — most PRDs have one. If it can't be located, surface this prominently before proceeding — for example: "I couldn't locate a technical design document for this PRD. I'll proceed assuming this is a small enough feature that one isn't needed — flag if I should pause and create one first." Don't refuse to proceed.
- **All other documents** (Assumptions, mockups, data mapping, data model docs, sample payloads, etc.) — optional. Their absence is normal and not worth flagging unless the PRD explicitly references one that's missing.

**Open the first substantive response with the lineage, in one line, before anything else:** the PRD by its full H1 title and, when the work is a phase, the phase by its id and full H1 title — "Building Phase 2a1 — Delivery receipts from the SMS provider, of Order Notifications." An unsplit PRD is the skill's default entry and has no phase: "Building User Notifications, whole PRD, not split." A reader who opens this chat later sees at the top what it is for, without decoding `2a1` against the plan (`implementation-lifecycle`, "Every Session Names What It Serves"). When the prompt already carried an `In service of:` block, the line simply agrees with it; when it did not, this is where the lineage gets written down. It is also the `serves:` line of this session's marker (`implementation-lifecycle`, "Session Markers"), whose START is written before your first edit in each repo. The gate turns on the PRD being nameable: if no PRD title can be found for the work, that is not a formatting problem — say so and stop before sizing.

**If you were pointed at a phase doc, check that it's still current with the parent PRD.** Phase docs reference acceptance criteria from the parent PRD by number or text. If those criteria have been renumbered, rewritten, or removed since the phase doc was created, the phase doc is stale. When the mapping to the current criteria is unambiguous (a renumbering, a rewording that means the same), update the phase doc and say so in one line; stop and surface it to the user before implementing only when a covered criterion was removed or rewritten so that the phase's scope is unclear.

**Preflight external access before going further.** Users often start this skill and walk away for an hour or two. A session that first discovers an expired credential at its first live test has spent that time stalled on a question nobody is there to answer. The first few minutes are when the user is most likely still at the keyboard, so find out now:

1. **List every external dependency the work will touch** — from the Technical Design, the code you'll modify, its tests, and the repo README: AWS profiles, Google Cloud / BigQuery, GitHub (`gh`), third-party APIs, vendor platforms, databases, whatever the live tests read.
2. **Make one cheap read-only call per dependency, in parallel, against the environment the work will actually use** — e.g. `aws sts get-caller-identity --profile <the profile the tests use>`, `gcloud auth application-default print-access-token` (what client libraries use, not just `gcloud auth list`), `bq ls --project_id=<project>`, `gh auth status`, `SELECT 1` against the database. Where cheap, prove the credential reaches the specific resource (list the bucket, the dataset), not only that it exists — a valid token without the grant fails just as late.
3. **Fix what you can yourself** — run `aws sso login --profile <profile>` or the equivalent re-auth rather than asking the user to; its browser approval lands while they're likely still there.
4. **If anything still fails, stop now** with a one-line ask naming the dependency and the exact command to fix it — before sizing or implementation, not after.

Passing doesn't guarantee a credential outlives the session. If a call fails on authentication mid-run, re-authenticate and retry — it's an expired token, not a code failure — and for long unattended runs prefer a non-expiring profile where the project's credential guidance names one.

---

### Phase 2: Size for a Single AI Session

This is the critical pre-implementation step. Before writing any code, decide whether you can confidently complete this work in one agentic session.

**What "one session" means:**

The work is happening **right now**, in this present AI session — typically a focused run on the order of minutes. "Single session" means this immediate run, not some abstract future unit of work being scheduled.

So the only sizing question worth asking is: *Can I, this AI, complete this whole thing end-to-end in this run without losing coherent context?* The constraint is your ability to hold the full design mentally as you build, test, and verify it — right here, right now.

Human-time framings ("a day's work," "a sprint," "a couple of days") measure something fundamentally different — humans planning calendar work over future time. They aren't relevant here because the work isn't being scheduled, it's being done in this session. Skip that framing entirely.

**How to size honestly:**

Walk through the implementation mentally. Roughly how many files will be created or modified? How many distinct integration points? How many tests? How much investigation may be needed for edge cases discovered mid-implementation? The point is not a precise count — it's a gut check on whether the whole thing fits in one focused, coherent run.

Then check that gut read against the **Session Capacity Calibration** section of the `phase-split` skill — the single, dated source of concrete anchors for what one session reliably carries with current models. Don't restate its numbers here; read it. It also records the systematic bias to correct for: sized-at-planning work underestimates far more often than not, so a borderline read means the work is too large.

**The decision:**

- **Fits in one session** → proceed to Phase 4 (Implementation). Phase 3 (Split, Then Keep Going) is skipped — it only applies when splitting is needed.
- **Too large** → proceed to Phase 3 (Split, Then Keep Going). Do NOT start implementing until the split is written.

**If you're uncertain**, lean toward splitting. The cost of an unnecessary split is small (the user can override). The cost of starting an oversized implementation is real — context fragmentation, half-built features, lost coherence.

---

### Phase 3: Split, Then Keep Going (only if too large)

If Phase 2 determined the work is too large for a single session, **invoke the `phase-split` skill.** Do not size, propose splits, or write phase documents yourself — that logic lives entirely in `phase-split`; reproducing it here would just drift out of sync with it over time.

Hand `phase-split` the PRD and Technical Design you loaded in Phase 1. It owns the sizing check, finding the natural seams (vertical slices, walking-skeleton foundation-first, read-before-write), deciding the split, and writing one document per phase in the PRD's directory under its positional id scheme (`2`, `2a`, `2a1` — one file per phase at every depth). **It does not stop to ask whether or how to split, and neither do you.** The split is declared in the response as a decision; the user redirects afterwards if they disagree, and the phase docs are uncommitted markdown, so a redirect is cheap. The wall-clock cost of a session that stops to ask "split as recommended?" — a question whose recorded answer is always yes — is the whole reason this step declares instead of asking.

**Then keep going: implement the first leaf in this chat.** The context you loaded in Phase 1 is exactly what the first leaf needs, and the leaf is session-sized by construction, so a fresh chat would only re-read the same documents. Declare which leaf you are building in one line, continue to Phase 4 against that leaf's scope, and let the new phase docs ride in this session's changeset. Later leaves get one fresh chat each, via the wrap-up's continuation prompt. Inside an authorized `phase-chain`, the chain dispatches the first leaf to a new task instead (`phase-split`).

**This applies to phase docs too, at any depth.** Being pointed at a phase of an already-split PRD doesn't guarantee it fits — the original split was an estimate, and Phase 2 sizing (or mid-implementation discovery) can reveal a phase is bigger than the split assumed. When that happens, invoke `phase-split` to cut the remaining work into child phases rather than grinding on past coherent context. Work already completed stays; the cut covers what's left, and the first child is the one that holds the work already in progress — you finish that child here. **"Bigger than assumed" means the originally scoped work was underestimated — not that implementation surfaced extra things to do.** Discovered extras go through the Materiality Gate and disposition rule (`implementation-lifecycle`), not into new phases; re-splitting to house discoveries is decomposition as a way of avoiding closure.

---

### Phase 4: Implementation

Build the feature, following the Technical Design and existing codebase patterns.

**Core principles:**

- **Follow the Technical Design.** Architecture choices, data flows, and integration points are decided — implement them as specified. If you discover the design is wrong, see "Doc Divergence" below.
- **Follow existing code patterns.** Read neighboring files for naming, structure, error handling, and logging conventions. Match them.
- **Treat assumptions as decided.** Anything in the assumptions document is settled — proceed without re-litigating.
- **Apply the engineering principles and house standards.** Follow `engineering-principles` (no silent fallbacks, the testing evidence standard, git safety in a shared clone), plus the house engineering standards named on an `Engineering standards:` line in the project's AGENTS.md/CLAUDE.md, if any — those own stack, style, structure and configuration.
- **Apply its judgment principles when ambiguity arises.** `engineering-principles` also carries "finish what you started," "investigate before removing," "don't dismiss failures," and "scope follows intent, not literal words." When you're unsure how to handle an ambiguous mid-implementation situation, those principles apply.
- **Judge every discovery against this phase's acceptance criteria.** Implementation surfaces anomalies constantly — brownfield systems have an infinite supply. Apply the Materiality Gate (`implementation-lifecycle`): a discovery is work only if it blocks an acceptance criterion, contradicts a requirement, or makes this implementation materially incorrect or unsafe — fix those now. The rare genuinely-valuable future item gets filed through the disposition rule. Everything else is dismissed silently. Discoveries never expand this phase's scope, spawn sub-phases, or postpone completion.
- **Before every edit to a file the Technical Design or phase doc did not put on the path, name the acceptance criterion that requires it.** The ID or the text — not "consistency," not "while I'm here," not "same pattern," not "it reads wrong now." No criterion, no edit, regardless of how small or how correct. The one thing this never excuses is your own breakage: what your in-scope change *made* wrong (a red test, a failing consumer, a page that now renders wrong) is the criterion's cost and is fixed before done — the test is causation, not location. Scope does not leak through tangents; it leaks through *neighbours* — the doc describing what you changed, the sibling check, the stale count — and each looks like correctness. If a non-criterion edit starts forcing follow-ups (regenerated artifacts, re-pinned tests, a drift gate going red), that cascade is the tell: **revert the root edit rather than fix the fourth consequence.** And if a discovery would take longer than the criterion work remaining, that alone decides it. (`implementation-lifecycle`, "Adjacency is how scope actually leaks".)

**Doc Divergence rule:**

If during implementation you discover that the PRD or Technical Design says something that's wrong, contradicts reality, or is incomplete:

1. **Stop coding.**
2. **Decide whether the divergence is technical or business** — see the technical-vs-business framework in "Assumed Starting State" above.
3. **Technical divergence:** investigate, decide on your best answer, update the PRD or Technical Design to reflect the correct decision, then continue.
4. **Business divergence:** if you're 95%+ confident in the correct answer, update the docs and continue. If you're below 95%, do NOT unilaterally rewrite the business decision — surface it as a stated assumption using `assumptions-document-writing` and proceed against that assumption. One exception to the 95% branch: if what the doc says is a decision a stakeholder personally made — a validated assumption folded into it, a ruling from their feedback — no confidence level lets you rewrite it. That is a reopening (Gate 3 in `assumptions-document-writing`): the doc keeps their decision, the reopened entry discloses yours, and you proceed on it.

Never silently implement something different from what the docs say. The docs are the source of truth — keep them accurate.

**MCPs:**

If the implementation involves an external system (a third-party API, a database, etc.) and an MCP for it is already configured (e.g., a vendor platform's MCP for work against that platform), **use the MCP** for documentation lookups, schema inspection, and API exploration. Do not stop and ask the user to install an MCP — just use what's available.

**Exploration scripts:**

Sometimes you need to query a database, inspect an API response, or test a transformation in isolation before committing to an implementation approach. When you do:

- **Location:** Put scripts in `scripts/exploration/` at the project root. This directory is clearly marked as exploration, not main program code.
- **Header comment:** Every exploration script must start with a comment that says, in plain language, "This is an exploration script, not part of the main program," followed by what it explores. Example:
  ```python
  # Exploration script — not part of the main program.
  # Queries the source system to confirm role permission codes before
  # deciding how to map them in the new permission model.
  ```
- **Naming:** Use descriptive, intuitive file names that hint at what the script does (`explore-role-permission-codes.py`, not `test1.py`).
- **Reusability:** Aim for scripts that someone else could run and understand. Parameterize where reasonable.
- **Read-only:** SELECT, GET, list/describe operations only. Never INSERT, UPDATE, DELETE, POST, or PUT against external systems.
- **Dev and sandbox first:** read production only read-only, only when nothing else can answer the question, and only where the project allows it (`engineering-principles`, "Production Data").

At the end of the implementation, **make a judgment call on each exploration script:**

- **Pure one-off, no future value** → delete it. No need to clutter the repo.
- **Potentially reusable or instructive for future work** → keep it. Mention it in the wrap-up so the user knows it's there.

When in doubt, ask the user — but prefer making the call yourself. The directory is clearly marked as exploration, so a kept script is low-cost.

---

### Phase 5: Tests

After the implementation is in place, run and update tests. This phase runs the suite several
times; if one run takes more than about two minutes, load `wall-clock-awareness` before the
second run — the cheap fixes are an afternoon and every later session inherits them.

**Approach:**

1. **Run existing tests first.** If any fail because of your changes, fix them or fix the implementation that broke them.
2. **Map verification evidence to acceptance criteria.** Every in-scope criterion must be demonstrably verified, but do not manufacture a separate unit test for each one. One high-value integration or workflow test may verify several criteria; a high-risk criterion may need more than one layer. **If you're implementing a single phase of a multi-phase PRD, map only against the acceptance criteria the phase doc covers** — later phases handle the rest.
3. **Choose tests by failure risk.** Follow `engineering-principles`: use unit tests for isolated deterministic logic, integration tests for real boundaries and contracts, and end-to-end/workflow checks where several components or a user-visible path must work together. Add a test only when you can name the regression it would catch.
4. **Use real resources for integration behavior.** Integration tests should hit real databases, APIs, and services in sandbox/dev environments. Use narrowly scoped mocks only for destructive, expensive, or hard-to-trigger conditions allowed by `engineering-principles` (its evidence standard); mock-only coverage does not prove an external integration works. **Anything a test writes, it writes to non-prod — integration tests never mutate production data, no exceptions.**
5. **Run the full suite again** before moving on.

**When the service has no non-prod environment yet**, don't drop integration testing entirely: where the project allows it (`engineering-principles`, "Production Data"), production may be used **strictly read-only** — GETs, SELECTs, and production-supported `--dry-run` planning paths. Write paths on such a service are verified at the unit level (with narrow mocks where `engineering-principles` permits) until a non-prod environment exists, and the evidence names the unproved write boundary as a gap. This read-only-prod arrangement is the exception for services without a non-prod counterpart, not a general option — flag the missing environment in the wrap-up rather than treating it as durable.

Do not target a test count or add ceremonial unit tests. Build the smallest portfolio that credibly proves the acceptance criteria and the important failure modes. Don't pause to ask the user about ordinary coverage decisions — make the engineering judgment from the risks, requirements, and existing suite.

---

### Phase 6: Deliverable Review (auto-run)

After tests pass, **automatically run the `deliverable-review` skill.** Don't wait for the user to ask.

**Announce it clearly:**

> "Tests are passing. Now running deliverable review automatically."

This matters because the user (and other people on the team) often reach for `deliverable-review` as their next step after seeing implementation complete. If you've already done it without telling them, they'll re-run it and waste the work. So announce upfront, then again at the end:

> "Deliverable review complete. [Brief summary of what was found / fixed / verified.]"

Apply any fixes the review surfaces. Re-run tests after the fixes.

---

### Phase 7: Test Hardening (auto-run)

After deliverable review completes — including any fixes it produced — **automatically run the `test-hardening` skill.** Same announce-before-and-after pattern as deliverable review, so the user doesn't re-run it manually:

> "Deliverable review complete. Now running test hardening automatically."

`test-hardening` owns the procedure: a fresh-eyes sub-agent maps this phase's acceptance criteria to test evidence, inventories mocks, and grades assertion strength; the main agent then strengthens the suite in priority order (missing evidence → mock-to-real conversions → weak assertions → risky edge cases) and gets the full suite green. The pass is bounded strictly by this phase's acceptance criteria — it never grows tests for behavior outside them, so it cannot become a side door for scope creep. It's an action pass, not an audit — the deliverable is the improved suite, and a suite that's already strong gets a one-line confirmation, not manufactured work.

Deliverable review runs first deliberately: its fixes change code, and tests hardened before those fixes would go stale. If hardening surfaces an implementation bug (Step 4 of that skill), fix it here and re-run the affected tests.

---

### Phase 8: Wrap-Up

When everything is done (and at any other terminal state, append the session marker's DONE line):

1. **Verify acceptance criteria coverage explicitly.** Walk through the list of acceptance criteria the work was supposed to cover (the full PRD list, or — if implementing a phase — the subset listed in the phase doc). For each one, confirm: is it implemented, and what passing automated test or recorded workflow verification proves it? A criterion does not require its own test, but it does require credible evidence. If any criterion is unmet or unverified, do NOT report the work as done — either close the gap or surface it explicitly to the user. **Also check the parent PRD (and the phase doc, if implementing a phase) for a `## Pending human actions` section** — every listed entry that hasn't happened is a known open item: name each in the wrap-up with its prepared draft/artifact. Listed entries are surfaced, not pulled into this session's scope — but the PRD as a whole isn't complete while that list is non-empty.
2. **State whether the scoped work landed, in a sentence or two.** Not an inventory: no list of files created or modified, no test counts, no walk back through the acceptance criteria. Those live in the diff and in the commit message, and repeating them here is the "what landed" summary the continuation test at the end of this list exists to stop. The user asked you to implement something — what they need back is whether it is done.

   **If this session split, state completion against the leaf you declared, not against the entry you were handed.** This covers all three ways it happens: Phase 2 sized the work and declared a split, the work split mid-implementation, or a phase of an already-split PRD turned out to need splitting again. One line for what landed (the leaf's id), one line naming the sibling leaves now written and the split record that lists them.

   **When the leaf's criteria are all verified, write its closure line** — `**Closed:** YYYY-MM-DD` under the leaf's title, plus the commit hash when this session is the one committing (`phase-split`, "Closure is one line on the leaf"). That line is what the next session reads to find the first unfinished child, so a leaf without it is not closed no matter what the wrap-up says. **A session that scoped down and finished cleanly is COMPLETE, not partial** — splitting is a sizing decision the methodology asked you to make, so do not report it as a shortfall and do not go looking for its acceptance criteria in the original entry. The pull to justify a narrowed scope by listing everything you did is strong and it produces exactly the inventory this item forbids.
3. **Note that deliverable review and test hardening were performed** — explicitly, so the user doesn't re-run either
4. **Mention any kept exploration scripts** — what they do, why they're worth keeping
5. **Stage and validate per `pre-commit-validation`, then provide a commit message.** If step 6 applies, run `continuation-prompt` before this step so its doc edits are in the staged set. Load that skill at the commit boundary — build the expected changeset, leave other sessions' staged files staged, stage only your specific files (never `git add .` or `git add -A`), and run its checks (secrets scan, diff sanity). Then provide a commit message following the project's commit conventions (`type(scope): description`), alongside its brief validation summary. Then hand the commit to the user to review and make (`pre-commit-validation`, "Who Commits"); commit or push yourself only when the user has explicitly told you to, announcing the message first. Include the repo name next to the commit message so the user can context-switch easily. Alongside the commit message, **recommend the `refactor-pass` skill as the optional next step once the commit lands** — one line, noting that this same chat is the best place to run it (it holds the evidence of whether the structure fought the change) and that its usual outcome is a quick "no refactor warranted." Never run it before the feature commit lands, whether the user or an authorized agent commits it; never run it automatically.

   **If pushing and opening pull requests are authorized, the session is about to wait on CI — and that wait never ends the turn.** Load `wall-clock-awareness` and follow its "Waiting on something external" section: start the CI watch in the background once a check is listed, do the independent work usually queued at this point (the PR numbers into the governing document, memory notes, the next phase's docs) without pushing to the branch under test, then block on a fresh bounded foreground watch and re-issue it on exit 124 until it exits 0 or 1. Check `mergeable` after opening each PR and re-check if it reads UNKNOWN — a CONFLICTING PR runs no CI and looks identical to "waiting". Do not end the turn or report the chat as resuming on its own while CI runs; it stays visibly running until green or red is stated.

6. **If this was one phase of a multi-phase PRD**, remind the user about the next phase — the next leaf in execution order, which after a split is usually the sibling you just wrote — and provide its copy-paste prompt via `continuation-prompt`. That skill runs before the commit is presented, not after: its first step moves everything the next session needs to know (state, owed items, inherited findings, hazards) out of the prompt and into the phase doc, and those doc edits ride in this session's commit. The prompt itself is a name line, the lineage block, and pointers, labelled with its actual commit/push prerequisites. When `phase-chain` is active, it carries the authorization context and launches exactly one successor after delivery; do not stop at a printed prompt.
   **If this closed the last phase of a PRD that a PRD roadmap lists** (`prd-roadmap`; the PRD's `**Roadmap:**` line says so), say the PRD is complete and name the roadmap's next planned PRD in one line. Do not write that PRD's prompt unless asked: moving on is the user's decision (`continuation-prompt`, "A PRD roadmap is not a track"). If this session also promoted the work to production, set the PRD's roadmap row to `in production YYYY-MM-DD` in this commit; otherwise name that one-line update as the user's action for when it ships.
7. **Remind the user to route any declared business-logic assumptions to stakeholders for validation.** Before writing this, sweep the work for decisions that were dispositioned onto a review page, a report, or any other deliverable rather than into the assumptions document — those are the ones that silently never get answered, and they belong in this callout with an assumption entry written for them. If during this session a business-logic assumption was written to the assumptions document (the below-95% confidence path described in "Assumed Starting State"), end the wrap-up with a prominent, separately-headed callout — not a footnote, not a parenthetical, and not buried in the commit message. For each assumption, list:
   - The assumption ID and a one-line summary of the proposed answer
   - The relevant stakeholder (if the assumptions document names one — e.g., the business owner or the operations lead)
   - The suggested validation channel (email, Teams message, ticket comment) based on the stakeholder's typical preference if known

   This is a manual step only the user can do, and it's the one thing that doesn't happen automatically. The assumption was a green light to ship the code — but the code is shipped under an unconfirmed answer until a human stakeholder either confirms or corrects it. Phrase the reminder so the user understands this is a separate obligation that picks up after the commit lands, not a "nice to have" follow-up. If no business-logic assumptions were declared this session, skip this step entirely — don't manufacture a reminder where there's nothing to validate.

8. **Apply the No Loose Ends discipline to the wrap-up itself, and then the three-question test.** Every sentence is about an acceptance criterion and whether it landed, an action only the user can take, or a critical finding labelled as such — anything else, beyond the items this wrap-up list requires, is **deleted**, not softened or footnoted (`implementation-lifecycle`, "Reporting Style"). The wrap-up contains no FYIs, caveats, "worth noting" or "a few things I noticed" items, and the fix for one you were about to write is to delete the sentence, not to go file the item: something you were about to mention as an aside is an observation that already failed the gate, and filing it so it can be counted is a side quest earning a disposition it never deserved. Before writing, handle only what genuinely survived the gate: deal with it (keep working), file it into the appropriate future phase doc / Technical Design / assumptions doc, or ask it as a one-line question with a recommendation. Sweep it for hollow promises too: any "I'll do X" / "X should happen next" / "this still needs Y" about work you could do in this session means the session isn't done — go do it, or file it, before writing the wrap-up. Then apply the continuation test (`implementation-lifecycle`): items whose disposition means the PRD's natural continuation will handle them get **zero individual mention** — they're represented only by a single disposition ledger line of counts and destinations ("**Dispositions:** 2 assumptions declared, 3 items filed to phase-4"), never named or described; omit the line if nothing was dispositioned. Beyond that, the wrap-up names only what needs the user: the required items above (assumption callouts, next-phase reminders, human-action surfacing) are exactly that — action items, not FYIs. Keep the whole wrap-up brief. **And apply Done Means Done (`implementation-lifecycle`):** once acceptance criteria are verified and deliverable review has run, declare the phase complete and stop — no further "what else could be wrong?" sweep, and never a fresh concern appended after the declaration.

---

## Rules and Constraints

### DO

- Load the full PRD, Technical Design, Assumptions, and supporting materials before sizing
- Open the first response with the lineage line: PRD by full title, plus the phase by id and full title when the work is one; stop if no PRD can be named
- Preflight every external credential and connection the work and its tests need at the end of Phase 1, so an expiry surfaces while the user is still present
- Be honest about session sizing — hand off to `phase-split` when the work won't fit
- Use the word "phase," not "story"
- Delegate the split to `phase-split` when the work is too large — it owns deciding the cuts and writing one doc per phase; neither skill stops to ask
- After a split, implement the first leaf in this same chat; every later leaf gets its own fresh chat
- Implement only leaves — pointed at a split parent, take its first unfinished child and say so
- Use real sandbox/dev resources for integration behavior; mocks only for isolated logic or the narrow cases `engineering-principles` allows
- Auto-run deliverable review after tests pass, and announce both before and after
- Auto-run `test-hardening` after deliverable review completes, with the same announce pattern
- Recommend `refactor-pass` at wrap-up, to run after the feature commit lands — never run it before the commit
- Update docs first when implementation reveals they're wrong
- Make judgment calls on exploration scripts (keep or delete)
- Remind the user to surface any declared business-logic assumptions to stakeholders for validation — that's the one post-commit step the user has to carry forward
- Disposition every loose end per the No Loose Ends discipline (`implementation-lifecycle`) — dismiss it at the Materiality Gate, deal with it, file it into the methodology docs, or ask in one line with a recommendation

### DO NOT

- Estimate work in human time ("a day's work," "a sprint") — the work is happening in this session right now, not being scheduled across future calendar time
- Size the work or write phase documents yourself when it's too large — invoke `phase-split` instead of reproducing its procedure here
- Stop to ask whether to split, or which cut to use, or end the turn after the phase docs are written — declare the split, write the docs, build the first leaf (inside an authorized `phase-chain`, hand the leaf to the chain instead)
- Silently implement something different from what the PRD or Technical Design says
- Use a mock as the only evidence that an external integration works
- Commit or push unless the user has explicitly told you to (`pre-commit-validation`, "Who Commits"); when that instruction already covers the action, do not ask again
- Run deliverable review silently — always announce
- End a turn to report FYIs/caveats, or stop to ask a question when you're ≥90% confident what the user's answer would be — keep working (No Loose Ends, `implementation-lifecycle`)
- End a turn announcing future work you could do now, or list "next steps" that live nowhere but the chat — do the work, or file it where a future session will load it (`implementation-lifecycle`, "No Hollow Promises")
- Treat a mid-implementation discovery as new scope — apply the Materiality Gate (`implementation-lifecycle`): fix only what blocks this phase, file the rare genuinely-valuable future item, dismiss the rest silently
- Edit a file no acceptance criterion requires — not to keep a doc consistent, not because a sibling has the same flaw, not because a comment's count is stale. Neighbours are how scope leaks, and a cascade of "now this has to change too" from a non-criterion edit means revert the root, not fix the cascade (`implementation-lifecycle`, "Adjacency is how scope actually leaks")
- Spend a session's time investigating a critical finding beyond confirming it is real and stating it in a line with a recommendation — whether to pursue it is the user's call, not the session's
- Declare the phase complete and then append newly surfaced concerns — anything material belonged before the declaration; anything else was dismissed or filed (`implementation-lifecycle`, "Done Means Done")

---

## Relationship to Other Skills

| Skill | How This Skill Uses It |
|-------|-----------------------|
| `implementation-lifecycle` | The umbrella — defines the four entities (PRD, Technical Design, Assumptions, Phase Documents), confidence thresholds, decision flow, and the session discipline. This skill is one procedural arm of that framework. Read it first; reload it if the session drifts. |
| `implementation-readiness-check` | Alternative predecessor — used when the user explicitly wants a human review checkpoint before implementation |
| `autonomous-requirements-refinement` | Heavyweight predecessor — multi-pass refinement for bringing draft documents to implementation-ready state |
| `phase-split` | Delegated to from Phase 3 when the work is too large for one session, at any depth. It owns the entire sizing/seam-finding/phase-doc-writing procedure and the phase id and file layout (`phase-{id}-{short-name}.md`, one file per phase) — this skill does not reproduce it. After it writes the docs, this skill builds the first leaf in the same chat and one leaf per fresh chat after that. |
| `prd-writing-standards` | Defines PRD format and the `docs/prds/` and `docs/changes/` colocated directory convention referenced by phase docs |
| `technical-design-writing-standards` | Defines Technical Design conventions referenced during implementation |
| `assumptions-document-writing` | Existing assumptions are decided facts during implementation. New assumptions surfaced mid-implementation (when business confidence is below 95%) get written using this skill. Do not load preemptively — but load it whenever you write an assumption **or edit an existing register at all** (recording a ruling, folding an answer, moving a row to the validated table, editing the header), reading its "Editing an Existing Document" section first. Edits made in passing are the main source of format drift. |
| `deliverable-review` | Auto-invoked after tests pass to verify the deliverable |
| `test-hardening` | Auto-invoked after deliverable review (Phase 7) — fresh-eyes pass that verifies every acceptance criterion has credible test evidence, converts unjustified mocks to real resources, and strengthens weak assertions before commit |
| `refactor-pass` | Recommended at wrap-up (Phase 8), run only after the feature commit lands — decline-biased judgment on whether this phase's work warrants refactoring, executing the refactor (structure-only, its own commit) when a concrete signal is present and the tidy is small |
| `continuation-prompt` | Produces the next chat's copy-paste prompt at wrap-up (Phase 8) when a next phase exists. Runs before the commit is presented so the facts it moves into the phase doc are part of the commit. |
| `pre-commit-validation` | Commit-boundary hygiene — staging cleanliness on a multi-session workstation, secrets scan, diff sanity. Loaded in Phase 8 before presenting the commit. |
| `engineering-principles` | The method's engineering principles applied during implementation — no silent fallbacks, the testing evidence standard, git safety in a shared clone, and the judgment calls for ambiguous moments (finish what you started, investigate before removing, don't dismiss failures). Loaded together with the house engineering standards named on the project's `Engineering standards:` line in AGENTS.md/CLAUDE.md, which own stack, style, structure and configuration |
| `implement-from-discovery` | Sibling skill — same downstream loop, different trigger. Use that one when the source of the requirement is research findings or a mid-investigation discovery rather than a fresh PRD. |

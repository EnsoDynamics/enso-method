---
name: implement-from-discovery
description: Implement a fix or improvement identified during research, investigation, or development, or raised in a bug report — not from a PRD authored ahead of time. Verifies alignment with the affected component's PRD/Technical Design, applies the technical-vs-business confidence gate, then implements, tests, and presents a commit message.
user-invocable: true
---

# Implement From Discovery

For implementing changes whose source is something you *discovered* — a bug found mid-investigation, a gap noticed while reading code, a fix identified during a research session — rather than a PRD authored ahead of time.

This is the lighter sibling of `implement-from-requirements` (PRD-triggered). It applies the same alignment-checking and technical-vs-business confidence gate that the framework uses everywhere, without its procedural overhead.

For the broader framework — the four entities (PRD, Technical Design, Assumptions, and Phase Documents when split), confidence thresholds, the assumptions philosophy, and the session discipline this whole session runs under — see the `implementation-lifecycle` skill, the methodology's umbrella. **Read that first if it isn't already loaded**, and reload it if the session drifts. A user invoking this skill should never need to name another one.

---

## When to Use

Use this skill when:

- You're already mid-investigation in this conversation and have identified a fix you want to implement now
- A bug report or improvement request has come in for a service (a scheduled sync job, a notification service, internal APIs, internal tools, long-lived services, etc.) and you want to go from "I see the problem" to "fix is committed"
- A self-discovered improvement to existing code that you want to make right now — the user's invocation is the lineage when nothing else names it (Phase 2); the session does not invoke it on its own for a fix that serves nothing named
- The change is small enough to implement in a single session without a phase split

**Use a different skill when:**

- The trigger is a fresh PRD the user authored — use `implement-from-requirements`
- The work is large enough to need a phase split or its own requirements — hand it back to the user to open a PRD or change directory (`prd-writing-standards`; a session never creates one unasked), then `implement-from-requirements` builds it (which hands off to `phase-split` when the work is too large for one session). This skill never splits work into phases itself.
- You haven't actually identified the fix yet, only the symptom — keep investigating first; this skill assumes you have a proposed change in mind

---

## Core Idea

The framework's substance is the same as everywhere else: read the affected component's docs, verify alignment, apply the technical-vs-business gate, implement, test, commit. What this skill adds is the *trigger shape* — the source of the requirement is research findings sitting in the conversation, not a document authored upstream.

That changes a few things in practice:

- **There's no "PRD to implement against"** — the PRD that's relevant is the one for the *component you're modifying*, not for the change itself. The discovery is a delta against an existing component's intended behavior.
- **The commit message has to carry the discovery → fix linkage** — the conversation is ephemeral, but the commit message is the durable record of what was found and what was done.
- **The technical-vs-business gate is the most load-bearing step** — because there's no PRD authoring step where the question would have surfaced, this skill is where you decide whether the change is something you can just make or something that needs an assumption + stakeholder validation.

**Invoking this skill ends discovery mode.** "Implement from discovery" means the discovery already happened — the session now converges on the one identified change: implement, test, commit. New findings that surface while implementing go through the Materiality Gate and disposition rule (`implementation-lifecycle`): they become work only if they make *this* change incorrect or unsafe; the rare genuinely-valuable future item gets filed; everything else is dismissed silently. Findings do not widen this session's diff, and they do not chain into further discovery — one discovery producing an implementation that produces more discoveries is the non-convergent loop this boundary exists to prevent.

This skill also runs under the No Loose Ends session discipline (`implementation-lifecycle`, "Session Discipline: No Loose Ends") — **read that skill first if it isn't already loaded.** The gist: run every finding through the Materiality Gate first — most are observations to dismiss silently, not work; disposition the loose ends that survive (deal with them now, file them into the docs a future session will actually load, or ask a one-line question with a recommendation — only when genuinely blocked) instead of reporting them as FYIs; never stop to ask a question when you're ≥90% confident what the user's answer would be; never end a turn announcing work you could do right now; and apply the continuation test — dispositioned items the work's natural continuation will handle appear only as counts in a one-line disposition ledger, so the response names only what needs the user.

---

## Process

### Phase 1: Locate the Affected Component's Docs

Identify what you're changing. For each affected component, find:

- **PRD** — typically `docs/prds/{feature}/{feature}-prd.md` or `docs/changes/{feature}/{feature}-prd.md` (identical layout)
- **Technical Design** — `technical-design.md` in that same directory
- **Assumptions** — `assumptions.md` in that same directory, if one exists

If no PRD/TD exists for the component, that's significant — the component may be older code that predates the PRD framework. Surface this to the user. Don't fabricate docs you don't have, but acknowledge the alignment-check is degraded and proceed with whatever architectural intent you can glean from the code itself, README, or comments.

You also need the **bigger picture** of the service you're touching, not just the one component's docs — a discovery is a delta against the whole system, so you need to know what else your change could affect. If the service has a **service/product overview or a substantive README**, read it; that's often a better single source of overall context than any one PRD. If the service has accumulated **several PRDs and no overview**, don't read them all — read the founding/earliest (it usually frames the service's purpose and architecture, where later ones are narrow increments) and skim the rest's titles, unless a later PRD is clearly the current source of truth. If there's no orienting context at all, flag it to the user — and treat it as a sign the service should grow a short overview (a methodology gap), not a reason to silently press on.

Read these docs before implementing. Skim is not enough. The whole point of this phase is loading the design intent into your head so you can compare it to the proposed change.

Before the first edit in each repo, write this session's marker START (`implementation-lifecycle`, "Session Markers").

**Preflight external access before going further.** Users often start this skill and walk away. A session that first discovers an expired credential at its first live test has spent that time stalled on a question nobody is there to answer. Credentials that worked during the investigation earlier in the chat may have expired since, and the tests may need ones the investigation never used — so check now, while the user is most likely still at the keyboard:

1. **List every external dependency the fix and its tests will touch** — AWS profiles, Google Cloud / BigQuery, GitHub (`gh`), third-party APIs, vendor platforms, databases, whatever the live tests read.
2. **Make one cheap read-only call per dependency, in parallel, against the environment the work will actually use** — e.g. `aws sts get-caller-identity --profile <the profile the tests use>`, `gcloud auth application-default print-access-token` (what client libraries use, not just `gcloud auth list`), `bq ls --project_id=<project>`, `gh auth status`, `SELECT 1` against the database. Where cheap, prove the credential reaches the specific resource (list the bucket, the dataset), not only that it exists.
3. **Fix what you can yourself** — run `aws sso login --profile <profile>` or the equivalent re-auth rather than asking the user to.
4. **If anything still fails, stop now** with a one-line ask naming the dependency and the exact command to fix it — before implementing, not after.

If a call fails on authentication mid-run anyway, re-authenticate and retry — it's an expired token, not a code failure.

### Phase 2: Verify the Change Aligns with PRD/TD

**First, state the lineage — and stop if it cannot be stated.** Open the response with one line naming what this fix serves, in full titles (`implementation-lifecycle`, "Every Session Names What It Serves"): the component by its PRD's H1 title (or the component's name with "no PRD" when Phase 1 found none), and the thing that makes this fix work rather than an observation — the acceptance criterion of a named phase it unblocks (`AC-DLV-04 of Phase 2a1 — Delivery receipts from the SMS provider, Order Notifications`), the ticket id of an issue someone raised, the incident, or the outside report that raised it. The gate turns on that second part, not on a PRD existing. When the prompt that opened this chat already carried an `In service of:` block, the line agrees with it — including the honest `no lineage found` form, which is echoed, not re-litigated.

Two ways this skill gets invoked, and the gate treats them differently. **The user pointing it at a fix they have seen** — in this chat or by a prompt they wrote — is the explicit ask: build it, and when nothing named fills the line it reads `no lineage found; built at the user's direction`, in the response and in the commit message. **The session reaching for it on its own initiative, or a handoff prompt reaching for it** — the fix was found here, unblocks nothing named, was reported by no one, broke nothing in production — is a discovery being promoted into work by being given a skill invocation. That is the chain this skill's "no chaining" rule exists to stop, caught one step earlier: do not implement it, and do not open a ticket for it in any tracker so that it has an id to route back here under. It goes through the Materiality Gate and the disposition table like any other discovery, under the 90% ask-gate: dismiss is the default, a genuinely valuable item files into the phase doc that will build it, and work outside any current PRD is named in the wrap-up as the user's decision with a recommendation. What is never written is a purpose invented to fill the line.

Then confirm the proposed change is consistent with the docs' stated intent.

Three cases:

| Case | Meaning | Action |
|------|---------|--------|
| **Docs right, code wrong** | The PRD/TD describes the intended behavior; the code doesn't do it; the discovery is a gap-closing fix | Implement the fix. This is the most common case. |
| **Code right, docs wrong** | The code is correct but the PRD/TD has drifted out of date | Update the docs first, then the code is already correct. |
| **Docs silent, new behavior** | The PRD/TD doesn't address this case at all; the discovery is proposing new behavior | Apply the technical-vs-business gate (Phase 3). New behavior often needs an assumption. |

If the change *contradicts* the PRD/TD's stated intent (not just fills a gap), resolve it as a Doc Divergence (the rule is in `implement-from-requirements`; the philosophy in `implementation-lifecycle`) — a decide-and-proceed, not a session stop: below 95% business confidence, an assumption entry and the build continues on it (it stops only when no answer can be put forward); where a stakeholder had personally ruled, it is a reopening at any confidence. Don't silently implement something the docs explicitly say shouldn't happen.

### Phase 3: Apply the Technical-vs-Business Gate

This is the most important step. Categorize the change:

**Technical change** — implementation detail. Architecture, naming, integration shape, error handling, idempotency, retry, caching, logging, refactoring. The PRD/TD's intent is met regardless of which technical answer you pick. A non-engineer business stakeholder couldn't meaningfully validate the choice.

→ **At ≥95% confidence:** just do it. No assumption needed. Commit message is the audit trail.
→ **Below 95% confidence:** investigate to raise confidence (read code, query the database, test the API, check existing patterns). If still under 95%, proceed with your best answer, at whatever confidence it has. Mention in the commit message *why* you chose this approach if the reasoning isn't obvious.
→ **No answer to put forward** (the evidence favors none of the options): stop and ask the user, naming the options and what would decide between them.

**Business-logic change** — affects what the system *does*, what users experience, what business rule applies, what a stakeholder would consider correct. A business-logic question **cannot be self-confirmed** — no amount of investigation tells you what the business intends, which is exactly why the assumption mechanism exists for these and rarely for technical ones.

→ **At ≥95% confidence:** proceed. No assumption entry and no stakeholder FYI (`implementation-lifecycle`, Confidence Thresholds); the commit message records the choice.

→ **Below 95% confidence, at any level:** write an assumption using the `assumptions-document-writing` skill and proceed. The assumption is for asynchronous stakeholder validation — it's a green light, not a hold.
→ **No answer to put forward** (the evidence favors none of the options): stop and ask the user, naming the options and what would decide between them.

Whatever the confidence, a decision that still needs a stakeholder's answer belongs in the **assumptions document** and nowhere else. Do not disposition it onto a review page, report or dashboard — that is disclosure, not filing, and it does not get answered (see `implementation-lifecycle`, "A Decision Needs an Assumption Entry, Always"). Recording it on such a surface in addition is fine.

Rule of thumb: *if a non-engineer business stakeholder could meaningfully validate the choice, it's business. If only an engineer would care, it's technical.*

The most common mistake is over-classifying things as business — writing assumption docs for purely technical decisions (library choice, file layout, formatting). Don't do that. Assumption docs are for things stakeholders can meaningfully validate.

The reverse mistake is also real: classifying a business decision as technical and just changing it. That erodes the validation process. When in doubt, err toward business.

### Phase 4: Implement

Build the fix following the codebase's existing patterns, the `engineering-principles` skill, and the house engineering standards named on an `Engineering standards:` line in the project's AGENTS.md/CLAUDE.md, if any (those own stack, style, structure and configuration).

Apply the judgment principles in `engineering-principles` when ambiguity arises (finish what you started, investigate before removing, source of truth means source of truth, scope follows intent).

Match existing code style. Don't refactor surrounding code unless the change requires it.

**Before every edit outside the files the identified fix itself touches, name what part of the fix requires it.** Not "consistency," not "while I'm here," not "the sibling has the same bug," not "this comment is stale now." If nothing in the one identified change requires the edit, it is not made. That never excuses your own breakage: what the fix itself *made* wrong is owed before done — causation, not location. Scope leaks sideways through neighbours, not through tangents, and each neighbour looks like correctness. If a non-required edit starts forcing follow-ups — a regenerated artifact, a re-pinned test, a drift gate going red — that cascade is the tell: **revert the root edit rather than fix its fourth consequence.** A neighbour that would take longer than the fix itself is out by that fact alone. (`implementation-lifecycle`, "Adjacency is how scope actually leaks".)

### Phase 5: Test

This phase runs the suite several times. If one run takes more than about two minutes, load
`wall-clock-awareness` before the second run — the cheap fixes are an afternoon and every
later session inherits them.

1. **Run existing tests.** If your change is in covered territory, existing tests verify it. Fix any failures caused by your change.
2. **Add tests for new behavior** where the existing suite doesn't cover what you built. Match the codebase's existing test patterns.
3. **Use real resources for integration behavior.** Integration tests should hit real databases, APIs, and services in sandbox/dev environments, per the evidence standard in `engineering-principles`; mocks only for isolated logic or the narrow cases it allows.
4. **For UI/frontend changes**, exercise the change in a browser before reporting done. Type-checking and unit tests don't verify UX.

### Phase 6: Deliverable Review

After tests pass, **automatically run the `deliverable-review` skill.** Don't wait for the user to ask.

Announce it clearly:

> "Tests are passing. Now running deliverable review automatically."

Apply any fixes the review surfaces. Re-run tests after fixes. Announce when complete.

### Phase 7: Test Hardening

After deliverable review completes — including any fixes it produced — **automatically run the `test-hardening` skill**, with the same announce-before-and-after pattern. It verifies the tests actually prove the stated intent of this fix (fresh-eyes assessment, then strengthening: missing evidence → mock-to-real conversions → weak assertions), bounded strictly by that intent — it never grows tests for behavior outside it. A suite whose evidence is already credible gets a one-line confirmation, not manufactured work.

### Phase 8: Wrap-Up

At this or any other terminal state, append the session marker's DONE line (`implementation-lifecycle`, "Session Markers").

1. **Capture the discovery → fix linkage in the COMMIT MESSAGE.** There is no PRD recording why this change exists, so the commit message is the only place that reasoning survives: what was discovered, what was fixed, and why. **This is not licence for a summary in the wrap-up** — say there whether the fix landed, in a sentence or two, and let the commit message and the diff carry the detail (see the continuation test later in this list).
2. **Stage and validate per `pre-commit-validation`.** Load that skill at the commit boundary — build the expected changeset, leave other sessions' staged files staged, stage only your specific files (never `git add .` or `git add -A`), and run its checks (secrets scan, diff sanity).
3. **Present the commit message with the validation summary.** Do not commit unless the user has explicitly told you to (`pre-commit-validation`, "Who Commits"). Include the repo name next to the commit message. Follow the project's commit conventions (`type(scope): description`). Alongside it, **recommend the `refactor-pass` skill as the optional next step once the commit lands** — one line; never run it before the user has committed, and for the typically small changesets this skill ships its usual outcome is a quick "no refactor warranted."

   **If the user then authorizes pushing and opening pull requests, the session is about to wait on CI — and that wait never ends the turn.** Load `wall-clock-awareness` and follow its "Waiting on something external" section: start the CI watch in the background once a check is listed, do the independent work usually queued at this point (the PR numbers into the governing document, memory notes, the next phase's docs) without pushing to the branch under test, then block on a fresh bounded foreground watch and re-issue it on exit 124 until it exits 0 or 1. Check `mergeable` after opening each PR and re-check if it reads UNKNOWN — a CONFLICTING PR runs no CI and looks identical to "waiting". Never report the chat as resuming on its own during a CI wait; the chat stays visibly running until green or red is stated.

4. **Note that deliverable review and test hardening were performed** — explicitly, so the user doesn't re-run either.
5. **Sweep the wrap-up for loose ends and hollow promises before writing it, then apply the three-question test.** Every sentence is about the fix and whether it landed, an action only the user can take, or a critical finding labelled as such — anything else, beyond the items this wrap-up list requires, is **deleted**, not softened or footnoted (`implementation-lifecycle`, "Reporting Style"). No FYIs, caveats, "worth noting" or "a few things I noticed" items, and the fix for one you were about to write is to delete the sentence, not to go file the item — an aside is an observation that already failed the gate, and filing it so it can be counted is a side quest earning a disposition it never deserved. Handle only what genuinely survived the gate: deal with it, file it, or ask in one line with a recommendation. Any "I'll do X" / "X should happen next" about work you could do in this session means the session isn't done — go do it, or file it, before wrapping up. Then apply the continuation test (`implementation-lifecycle`): dispositioned items that the work's natural continuation will handle get no individual mention — represent them only in a one-line disposition ledger of counts and destinations ("**Dispositions:** 1 assumption declared, 2 items filed to phase-3"), omitted when nothing was dispositioned. Beyond that line, the wrap-up names only what needs the user. Then apply Done Means Done (`implementation-lifecycle`): declare the fix complete and stop — never append a fresh concern after the declaration.
6. **Remind the user to route any declared business-logic assumptions to stakeholders for validation.** If Phase 3 wrote any business-logic assumptions to the assumptions document, end the wrap-up with a prominent, separately-headed callout — not a footnote, not a parenthetical, and not buried in the commit message. For each assumption, list:
   - The assumption ID and a one-line summary of the proposed answer
   - The relevant stakeholder (if the assumptions document names one — e.g., the business owner or the operations lead)
   - The suggested validation channel (email, Teams message, ticket comment) based on the stakeholder's typical preference if known

   This is a manual step only the user can do, and it's the one thing that doesn't happen automatically. The assumption was a green light to ship the code — but the code is shipped under an unconfirmed answer until a human stakeholder either confirms or corrects it. Phrase the reminder so the user understands this is a separate obligation that picks up after the commit lands, not a "nice to have" follow-up. If no business-logic assumptions were declared this session, skip this step entirely — don't manufacture a reminder where there's nothing to validate.

---

## Rules and Constraints

### DO

- Locate and read the affected component's PRD/TD/Assumptions before implementing
- Verify the change aligns with the docs' intent before changing code
- Open Phase 2 with the lineage line — the component's PRD by full title and the acceptance criterion, ticket id, incident, or report this fix serves — and stop if nothing named fills it and the user did not ask for the fix themselves
- Preflight every external credential and connection the fix and its tests need before implementing, so an expiry surfaces while the user is still present
- Apply the technical-vs-business gate honestly — the threshold matters and is the load-bearing decision
- Use real sandbox/dev resources for integration behavior; mocks only for isolated logic or the narrow cases `engineering-principles` allows
- Auto-run `deliverable-review` after tests pass and announce both before and after
- Auto-run `test-hardening` after deliverable review completes, with the same announce pattern
- Recommend `refactor-pass` at wrap-up, to run after the feature commit lands — never run it before the commit
- Stage only the files you modified; let the user commit

### DO NOT

- Skip alignment-checking just because the change feels small
- Write a formal assumption for a purely technical decision (architecture, library choice, formatting, file layout)
- Silently implement something that contradicts the docs — surface the divergence
- Commit without the user's explicit instruction
- Use a mock as the only evidence that an external integration works
- Pad the commit message with skill references or process boilerplate — describe what changed and why, not which skill was invoked
- End a turn reporting FYIs/caveats, announcing future work you could do now, or listing "next steps" that live nowhere but the chat — disposition instead (No Loose Ends, `implementation-lifecycle`)
- Implement a fix whose only lineage is this chat — no acceptance criterion, ticket id, incident, or outside report — without the user's explicit say-so, and never mint a ticket in any tracker to give one a lineage; a purpose invented to fill the line is worse than an honest orphan
- Chain discoveries — this session ships the one identified change; findings that surface while implementing are dispositioned per the Materiality Gate (`implementation-lifecycle`), not added to the diff or investigated onward
- Edit a file the identified fix does not require — not for consistency, not because a sibling shares the flaw, not because a comment is now stale. When a non-required edit forces a cascade of follow-ups, revert the root rather than fix the cascade (`implementation-lifecycle`, "Adjacency is how scope actually leaks")

---

## Relationship to Other Skills

| Skill | How This Skill Uses It |
|-------|-----------------------|
| `implementation-lifecycle` | The umbrella — confidence thresholds, the four entities, the assumptions philosophy, and the No Loose Ends session discipline (disposition FYIs/caveats instead of reporting them, the 90% ask-gate, minimizing stop-and-go). **Read first; reload if the session drifts.** |
| `implement-from-requirements` | Sibling — same downstream loop, different trigger (fresh PRD vs. discovery) |
| `assumptions-document-writing` | When a business-logic change below 95% confidence needs an assumption entry, **and whenever you edit an existing assumptions register at all** — recording a ruling, folding an answer, moving a row to the validated table. Don't load preemptively; do read its "Editing an Existing Document" section before any edit to an existing register. |
| `engineering-principles` | The method's engineering principles (no silent fallbacks, the testing evidence standard) and ambiguity-handling judgment; loaded with the house engineering standards named in the project's AGENTS.md/CLAUDE.md, if any |
| `deliverable-review` | Auto-run after tests pass |
| `test-hardening` | Auto-run after deliverable review (Phase 7) — verifies the tests prove this fix's stated intent, bounded by that intent |
| `refactor-pass` | Recommended at wrap-up, run only after the feature commit lands — decline-biased judgment on whether this fix's work warrants refactoring, executing small structure-only tidies as their own commit when a concrete signal is present |
| `pre-commit-validation` | Commit-boundary hygiene — staging cleanliness, secrets scan, diff sanity. Loaded in Phase 8 before presenting the commit. |
| `prd-writing-standards` | If the work is large enough that it really needs a PRD or change directory before implementing, escalate here first |

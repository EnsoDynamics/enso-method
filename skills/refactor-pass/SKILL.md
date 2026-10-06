---
name: refactor-pass
description: "Post-commit follow-on to the implementation chain — judge whether the work just implemented warrants refactoring and, when it does, perform the refactoring in the same invocation: structure-only changes, tests stay green, presented as its own refactor(scope) commit proposal (the skill never commits; the user does). Strongly decline-biased; the most common outcome is a one-paragraph \"no refactor warranted\" with zero artifacts. Runs only on a committed feature baseline — recommended at implement-chain wrap-up for after the user commits, or standalone against a named commit and its requirements. An action skill — when refactoring is warranted it does the refactoring, not a report about it."
user-invocable: true
---

# Refactor Pass

The optional follow-on to the standard implementation chain: implement (`implement-from-requirements` or `implement-from-discovery`) → `deliverable-review` → `test-hardening` → *user commits the feature work* → **`refactor-pass`**.

The chain steps ask "does the work do what was asked, and do the tests prove it?" This pass asks a different question: **now that it works, is proven, and is safely committed, did building it leave the code structurally worse — and is fixing that worth doing right now?** Then, if the answer is yes, it does the fixing. One invocation covers both the judgment and the work: there is no separate "assessment" deliverable to carry into another session.

Two commit rules frame everything here. **The pass runs only on a committed feature baseline** — the implement skills recommend it at wrap-up but never run it themselves, because refactoring can make a mess, and a committed baseline makes any mess trivially revertible without touching the feature diff. And **the pass does not commit on its own** — like every other skill in the chain, it stages its changes and presents a `refactor(scope): ...` commit message; the user reviews the diff and commits by their own judgment.

**The default answer is no.** This is not hedging — it is the expert position the skill is built on. Refactoring is justified economically (Fowler): by making real, observed friction go away in code that will be worked on again — never by aesthetics, and never by imagined future needs ("speculative generality" is itself a code smell in Fowler's catalog). Most implementation sessions end with code that is good enough, and for those the entire output of this pass is one short paragraph. Do not manufacture a refactor to justify the invocation.

Why this moment: "right after the feature, with green hardened tests" is the *refactor* step of red-green-refactor writ large — Kent Beck calls it *tidying after*. The tests `test-hardening` just certified are the safety net that makes structure-only change safe.

---

## When to Use

- As the recommended next step after an implement chain wraps up and the user has committed the feature work — ideally in the same chat, which still holds the strongest evidence
- Manually, in the same chat, when the user says "should we refactor this?", "clean this up", or "run the refactor pass"
- **Standalone in a fresh chat**, pointed at completed work — a teammate's finished feature, a phase implemented in a chat that's now closed. This mode needs concrete anchors (below), not a vague description.

**Do NOT use this skill for:**

- A whole-repo or whole-module refactoring campaign — this pass anchors on one piece of recently implemented work and the code it touched, nothing wider
- Behavior changes, bug fixes, or feature work of any kind — if the assessment surfaces a *bug*, that's a finding for the user (or `implement-from-discovery`), not something to fix under the refactoring flag
- Code that isn't changing and has no observed friction — stable code left alone is the correct outcome, not a missed opportunity

---

## Two Invocation Modes

### Same chat (the expected path, and the better one)

The implementing session holds evidence no fresh chat can reconstruct: whether the structure *fought* the change, where a mental model had to be built that the code doesn't express, which edits sprawled across files. These experiential signals are the strongest refactor indicators, and they exist only in the session that lived them. When this skill runs in the chat that did the implementation, use them — cite them by name in the verdict.

### Fresh chat (standalone)

Fully supported, with eyes open about what changes: the experiential signals are gone, so the assessment runs on **structural evidence readable from the diff** — duplication, scatter, dead scaffolding, stale names. That evidence is real and sufficient; the bar for acting on it does not move. What the mode strictly requires is anchors, asked for if missing rather than inferred:

1. **The changeset** — the commit SHA or range that shipped the work (`git show <sha> --stat`, `git diff <base>..<head>`). It must be *committed*: if the work is still sitting uncommitted in the tree, stop and have the user commit it first — the pass never refactors on top of an uncommitted feature.
2. **The requirements** — the phase doc or PRD the work implemented, or for discovery-driven work a one-line statement of what it was meant to do. This bounds what "the work touched" means and guards against behavior change: the refactored code must still do exactly what these requirements say.

A workable fresh-chat invocation: *"Run refactor-pass on commit `<sha>` — it implemented `<path to phase doc or PRD>`."*

Two cautions that grow with distance from the implementation: (a) confirm the suite is green **before** touching anything — the safety-net assumption must be established, not presumed; (b) if unrelated work has landed on top of the target commit, the refactor must respect the code as it is *now*, and a crowded file history is a reason to be more conservative, not less.

---

## The Signals: When Refactoring Is Warranted

Refactor only when **at least one of these signals is clearly present in the code this work touched**. Each is checkable — cite the specific evidence (file, function, the duplicated fragments, the scattered edit sites) in the verdict, not a vibe.

1. **Rule of Three tripped** (Don Roberts, via Fowler) — this work created or revealed the *third* instance of substantially duplicated logic. Two instances are not a signal; extracting at two picks the wrong abstraction.
2. **The structure fought the change** *(same-chat evidence)* — the implementation was harder than its inherent complexity because existing structure resisted it, and similar changes are plausibly coming. This is Fowler's preparatory-refactoring economics pointed backward: pay down the friction you just paid once.
3. **Comprehension gap** — understanding or writing this code required a mental model the code does not express. Move the understanding into the code: rename, extract, restructure until the code says what the session had to figure out (Fowler's comprehension refactoring).
4. **Shotgun surgery** — one logical change in this work required coordinated edits in three or more scattered places. The next change to the same behavior will pay again.
5. **Divergent change** — a function, class, or module this work touched now mixes clearly unrelated responsibilities and will be edited for unrelated reasons.
6. **Leftover scaffolding** — dead code, unused parameters, commented-out experiments, temporary shims, or debug remnants from this implementation, *substantial enough to mislead a future reader*. A stray unused import is not a signal — trace-level leftovers are dismissed silently, or every session would "find" something.
7. **Stale names** — names that are now actively *wrong*: they described the code before this work and would mislead a reader about what it does now. Merely-improvable names don't qualify — that bar would never decline.

And one **gate** that is not a signal but a precondition for acting on any of them:

8. **The tidy is small** (Beck's bound, *Tidy First?*) — the whole refactor fits in a modest diff the user can review in a few minutes, touching a handful of files. Beck's rule of thumb: a tidying that exceeds about an hour of focused work means you've lost track of the minimum structural change. Bigger than the bound → the brief-and-stop path below, never a big-bang refactor.

---

## The Guardrails: What This Pass Must Never Do

These come from the same sources as the signals and are absolute:

1. **No speculative generality.** "Making it extensible for the future" is never a justification — not for an abstraction, a parameter, a layer, or a plugin point. If no observed signal demands it, the future can pay for it when it arrives (YAGNI). This single rule is what keeps the pass from becoming a scope-creep engine.
2. **Two hats, never both** (Kent Beck's metaphor, via Fowler). Refactoring changes structure, never behavior. No bug fixes, no edge-case handling, no "while I'm in here" improvements to what the code *does*. Observable behavior — API responses, data written, log content consumers rely on — is identical before and after (incidental identifier text in logs and tracebacks may change as a mechanical consequence of a rename). And **renames stop at any externally consumed name**: public package APIs, serialized or persisted field names, string-referenced symbols (`getattr`, config-driven imports, queue/task names), CLI flags, config keys, metric names a dashboard reads. Grep for string occurrences of a name before renaming it; if the name crosses such a boundary, it is not a tidy — leave it.
3. **Tests are the safety net, so the safety net is frozen.** `test-hardening` just certified these tests; they are the proof that behavior didn't change. No assertion changes, no test deletions, no new tests. The only permitted test edits are mechanical consequences of the refactor itself — updated imports, renamed symbols, moved paths.
4. **Only code this work touched**, plus the minimal surrounding unit a tidy genuinely requires (extracting a shared helper may touch its second call site). Pre-existing mess in files this work never touched is out of scope — not mentioned, not fixed (Fowler: code that isn't changing doesn't earn refactoring).
5. **Its own commit, on a committed baseline, committed by the user.** Refactoring starts only after the feature commit has landed and is never folded into it — a reviewer must be able to read the feature diff and the refactor diff separately. The pass stages and proposes a `refactor(scope): ...` message; it runs `git commit` itself only when the user explicitly says to.
6. **Small steps, tests between.** Execute one tidy at a time and run the relevant tests after each, so a red suite points at the last small step, not at an hour of entangled edits.

---

## Process

### Step 1: Establish the Anchor and the Baseline

1. Identify the mode. Same chat: the work just implemented is the anchor and the session's own experience is admissible evidence. Fresh chat: obtain the changeset and requirements anchors, asking for whichever is missing.
2. **Confirm the feature work is committed.** If it is still uncommitted or only staged, stop — remind the user to commit it (their call, their judgment) and pick the pass up afterward. Refactoring only ever happens on top of a committed baseline, so a refactor that goes wrong is trivially revertible and never entangles the feature diff.
3. **Confirm the checkout actually contains the work, and note what else is in flight.** Verify the anchor commit is reachable from HEAD (`git merge-base --is-ancestor <sha> HEAD`) — if it isn't (wrong branch, unfetched work), stop and say so rather than refactoring code that doesn't contain the feature. Then check `git status` for other sessions' uncommitted or staged files on this shared checkout: proceed only if the refactor's scope doesn't touch them, and never sweep them into staging.
4. Confirm the safety net: the full relevant suite is green. In the same-chat case this was just established by `test-hardening`. Standalone, run it before touching anything. **If the suite is red, diagnose before routing**: an environmental failure (missing credentials, wrong profile or interpreter) gets fixed as environment setup; genuinely weak or failing tests mean stop and recommend `test-hardening` first. Refactoring without a trustworthy net is the classic anti-pattern this ordering exists to prevent.
5. Establish the code in scope: the files this work touched (`git show <sha> --stat` / `git diff <base>..<head>` of the shipped changeset).

### Step 2: Assess Against the Signals

Walk the signal list against the in-scope code. This is a main-agent judgment, not a sub-agent fan-out — in same-chat mode the session's own experience *is* the evidence, and the deliberate decline bias means a conservative single reader is the right instrument. Read the touched code fresh from disk (not from memory of writing it), because leftover scaffolding and stale names hide from the eyes that wrote them.

### Step 3: Verdict

State the verdict in a few sentences, citing specific signals with specific evidence — or their absence.

- **No refactor warranted** (the common case): one short paragraph — which signals were checked, why nothing met the bar — and done. **No report file, no findings list, no "however you might consider…" trailer.** A clean pass that ends in one paragraph is the skill succeeding, not the skill finding nothing to do.
- **Refactor warranted and within the small-tidy gate**: name the tidies (typically one to three), then proceed to Step 4 without pausing for permission — performing the refactor is what this skill is for.
- **Refactor warranted but over the gate**: proceed to Step 5 (brief and stop).

### Step 4: Execute

1. Perform the tidies one at a time, smallest first, running the relevant tests after each.
2. Run the **full suite** at the end — the same command `test-hardening` ran, named in the wrap-up.
3. Any failure is triaged honestly: the refactor broke it → fix the refactor (or revert that tidy); never adjust a test to absorb a behavior change, because a behavior change means the two-hats rule was violated.
4. Stage the refactored files (only them, never `git add .`), validate per `pre-commit-validation`, and present a `refactor(scope): ...` commit message labeled with the repo name. **Do not commit** unless the user explicitly says to — the user reviews the diff and commits by their own judgment, exactly as with the feature commit.

### Step 5: Over the Gate — Brief and Stop

A warranted refactor that exceeds the small-tidy bound is **deferred, not attempted**. Name it in the wrap-up in a line or two (the signals, the files) as an action item for the user, and stop. If the user says go, this chat writes it up as a change directory (`prd-writing-standards`, storage convention): a short PRD whose acceptance criteria are "behavior unchanged, suite green", and the brief as its technical design — a session never creates one unasked. The brief carries: the signals observed with their evidence, the files in scope, and the explicit do-not list (no behavior change, no speculative generality, tests frozen). Critically, **the brief must decompose the refactor into a sequence of individually gate-sized tidies**, each independently shippable with the suite green after it — this is Beck's actual prescription (many small tidyings, never one big restructuring), and it's what lets a fresh session execute the brief step by step with `refactor-pass` standalone without tripping the same gate that deferred it. A refactor that cannot be decomposed that way is not a tidy at all — it's a redesign, and it exits this skill entirely (surface it to the user as such). Do not start a big refactor "just to see how far we get" — a half-applied restructuring is worse than none.

### Step 6: Wrap-Up

One paragraph, mirroring the chain's no-loose-ends discipline: the verdict, what was tidied (if anything), confirmation the full suite is green with the command named, and the `refactor(scope):` commit proposal awaiting the user's judgment. Note explicitly that the refactor pass was performed, so the user doesn't re-run it. No FYIs, no inventory of dismissed observations, no adjacent-code commentary.

---

## Rules and Constraints

### DO

- Default to declining — "no refactor warranted" in one paragraph is the expected common outcome
- Cite specific, checkable evidence for every signal claimed (files, fragments, edit sites) — and use same-chat experiential evidence when it exists
- Keep every accepted refactor inside Beck's small-tidy bound; brief-and-stop anything larger
- Execute in small steps with tests between, and finish with the full suite green
- Keep the refactor in its own `refactor(scope):` commit, sequenced after the feature commit
- Ask for the changeset and requirements anchors when invoked standalone, rather than inferring them

### DO NOT

- Refactor for imagined future needs — speculative generality is the failure mode, not the goal (YAGNI)
- Change behavior under the refactoring flag — no bug fixes, no edge cases, no "while I'm in here" (two hats)
- Touch tests beyond mechanical renames/imports/moves — assertions and coverage are frozen at what `test-hardening` certified
- Reach into code this work didn't touch, however messy — stable code earns no refactoring
- Extract an abstraction from two instances of duplication — the Rule of Three exists because two picks the wrong abstraction
- Produce an assessment report as the deliverable — the deliverable is either the refactored code or a one-paragraph decline
- Big-bang a refactor that's over the small-tidy gate, or leave one half-applied

---

## Relationship to Other Skills

This skill is self-contained — the signals and guardrails above are the complete rules. It connects to the other skills like this:

| Skill | Relationship |
|-------|-------------|
| `implement-from-requirements` | Recommends this skill at wrap-up, alongside the feature commit proposal — to run after the user commits, ideally in the same chat. |
| `implement-from-discovery` | Same recommendation, discovery-triggered work — the anchor is the stated intent of the fix rather than PRD acceptance criteria. |
| `test-hardening` | The preceding step, and the precondition: it certifies the safety net this pass depends on. Standalone invocations with a weak or red suite get routed there first. |
| `deliverable-review` | Two steps earlier in the chain. It verifies the deliverable matches intent; this pass never revisits that question. |
| `prd-writing-standards` | Where an over-the-gate refactor lives if the user wants it done (Step 5): a change directory, created on the user's say-so, whose technical design is the brief a fresh standalone invocation executes. |
| `pre-commit-validation` | Runs at the commit boundary for the refactor commit exactly as for any other — staging hygiene, secrets scan, diff sanity. |
| `implementation-lifecycle` | The umbrella methodology — the Materiality Gate and No Loose Ends discipline are the general form of this skill's decline bias and one-paragraph wrap-up. |

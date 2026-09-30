---
name: phase-split
description: Decide whether a PRD, or any phase of one, is too large to implement in a single AI session and, if so, split it into independently shippable phases. Decides the cut itself and proceeds without stopping for confirmation. Produces one lightweight phase document per phase at every depth (phase 2, phase 2a, phase 2a1), all flat in the PRD directory, referencing the PRD and the single technical design without duplicating them. The planning step between requirements-ready and implementation — it does not write code.
user-invocable: true
---

# Phase Split

Take an implementation-ready PRD — or a single phase of one, at any depth — that is too large to build in one AI session and break it into ordered, independently shippable **phases** — each a defined subset of the PRD's acceptance criteria — then write a short phase document for each and hand off.

This skill owns three things:

1. **The sizing test** — deciding whether the work fits in a single AI session.
2. **The phase-split procedure** — finding seams, deciding the split, and writing the phase documents.
3. **The phase naming and file layout** — how phases at every depth are identified and where their documents live, so that "implement phase 2a1" always points at exactly one file.

It is the planning step that sits between "the requirements are ready" and "go build it." **It does not implement.** It also **does not stop to ask whether to split, or how**: it decides the cut, declares it, writes the documents, and hands off. The user can redirect after the fact — the documents are cheap to rewrite and nothing is committed yet — but a session that stops to ask "shall I split as recommended?" loses the wall-clock time the user isn't there to give back, for a question whose answer is almost always yes.

---

## When to Use

Use this skill when:

- You already know a PRD is **too large to implement in a single AI session** and you want to break it into phases before building anything.
- `implement-from-requirements` sized the work, found it too large, and sent you here.
- You want to re-evaluate or revise an existing phase split.
- **A phase at any depth turned out bigger than the split above it assumed** — discovered at sizing time or mid-implementation — and its remaining work needs to be cut into child phases.

**Do NOT use this skill when:**

- The PRD or technical design haven't been written or refined yet — do that first (`prd-writing-standards`, `technical-design-writing-standards`, then `autonomous-requirements-refinement`, or `implementation-readiness-check` for an explicit human checkpoint).
- The work comfortably fits in one AI session — skip phasing entirely and go straight to `implement-from-requirements`. Don't manufacture phases for work that doesn't need them.
- The work is a single bounded fix with no requirements directory behind it — `implement-from-discovery` builds that without phases.
- The source is bigger than one PRD — a brief or idea that would run to dozens of phases before anything reaches production. Cut it into planned PRDs with `prd-roadmap` first; this skill then splits each PRD once it is written.

---

## What This Skill Produces

The output is a set of **phase documents** colocated with the PRD, one file per phase at every depth, all in the same flat directory:

```
docs/prds/{prd-name}/               ← or docs/changes/{prd-name}/ — a bounded delivery, identical layout
  {prd-name}-prd.md                 ← unchanged: the single source of truth
  technical-design.md               ← unchanged: ONE design covering all phases
  phase-1-{short-name}.md
  phase-2-{short-name}.md           ← was split: now a short split record pointing at 2a-2c
  phase-2a-{short-name}.md
  phase-2b-{short-name}.md          ← was split again: a split record pointing at 2b1-2b2
  phase-2b1-{short-name}.md
  phase-2b2-{short-name}.md
  phase-2c-{short-name}.md
  phase-3-{short-name}.md
```

Hard rules about the output:

- **The PRD is not split.** It stays whole. Phase docs reference its acceptance criteria by label; they never restate them.
- **The technical design is not split.** There is exactly **one** technical design document per PRD, covering the whole system across all phases. Each phase doc *points into* the relevant sections of that single design — it never gets its own technical design. The shared data model and interfaces are cross-phase contracts; duplicating them per phase guarantees drift. (See `technical-design-writing-standards`.)
- **One file per phase, at every depth.** A phase that gets split produces one new file per child. A child is never a heading inside its parent's document, and a "plan" document never holds several phases as sections. When someone says "implement phase 2b1," that is one file, and `implement-from-requirements` is pointed at it and nothing else. (The measured failure this rule exists to stop: a long-running PRD grew per-track "plan" documents holding a dozen sub-phases as headings, each session had to be told which heading to read, and the headings were named inconsistently across tracks — see "Phase Identifiers and File Layout" below.)
- **Phase identifiers are positional, and only positional.** `2`, `2a`, `2a1`. Never a mnemonic, an owner initial, or a subject code.

A phase doc is born as a thin **scope-setting overlay** — not a mini-PRD and not a mini technical design. Over the project's life it legitimately grows into more: per `implementation-lifecycle`, a future phase doc is the preferred landing place for follow-up work discovered in other phases that survives its Materiality Gate, so "Carried forward from Phase N" / "Inherited from Phase N" sections accumulate in it as the project progresses. That growth is routed work, and it's the system working as designed. What a phase doc never accumulates is duplicated content from the PRD or technical design — or the scope of another phase.

---

## Phase Identifiers and File Layout

This section is the naming standard. Every other section of this skill, and every skill that points at a phase, uses it.

### The identifier

A phase id is its position in the tree, written by alternating digits and letters, one run per depth:

| Depth | Form | Example | Read as |
|---|---|---|---|
| 1 | digits | `2` | the PRD's second phase |
| 2 | digits + letter | `2a` | the first child of phase 2 |
| 3 | digits + letter + digits | `2a1` | the first child of phase 2a |
| 4 | + letter | `2a1a` | the first child of phase 2a1 |

The alternation is what makes an id parse without separators: each run is one depth, and the id of any ancestor is a prefix of the id (`2` ⊂ `2a` ⊂ `2a1`). A run may be more than one character: `2a10` is the tenth child of `2a`, and it cannot be misread as `2a1` + `0` because depth 4 is a letter run. Depth 4 is rare and depth 5 should not happen — a plan that deep is a sign the level-1 phase was a whole program. Lifting its children up a level is the fix, and because that renumbers a referenced plan it is the user's deliberate reorganisation, never a session's. The id is short by construction — `2a1` is three characters — because it is the token that gets typed into prompts, chat names, commit messages, and grep, dozens of times.

In prose: "Phase 2a1". In a chat name (`continuation-prompt`): `ph2a1`. In a prompt's lineage block: `Phase 2a1 — <full title>`, em dash regardless of the H1's colon. In a commit message: `(Phase 2a1 of {PRD name})`, never a bare "Phase 2a1" or a bare "2a1" — the ordinal always travels with the name of the thing it is an ordinal of.

**What never goes in the id:**

- **Not the owner.** Two people each running a lane of the same PRD is a fact about who is doing the work, not about what the work is. It goes in an `Owner` column of the parent's children table. An id that encodes the owner (`S5`, `T-API`) goes wrong the day a lane changes hands, and it loses the ordering an id exists to carry.
- **Not the subject.** A PRD whose phase 2 is "one sub-phase per table" is the common case for this rule, and the temptation is to name the children after the tables (`ORD`, `CUST`). The table name goes in the **short-name** part of the filename and in the title, where it is readable; the id stays `2a`, `2b`, `2c`, where it is short and sortable. `phase-2c-customers-table.md` carries both.
- **Not a track or lane code, a date, or a status.**

### The filename

`phase-{id}-{short-name}.md`, all in the PRD directory, no subdirectories. The short-name is two to four kebab-case words naming what the phase delivers (`event-pipeline`, `customers-table-build`, `review-page`); it is for readers, and it may change without the id changing. Do not repeat the PRD name in the filename — the directory already says it.

Flat in one directory is deliberate: a directory listing groups a parent with its children (`phase-2`, `phase-2a`, `phase-2b`, `phase-2b1`, `phase-2b2`, `phase-2c`, `phase-3`), every pointer is one path with no directory to spell, and a phase that gets split later does not move. Execution order is the plan table's job, not the listing's — past nine siblings `ls` puts `phase-10` before `phase-2`, and that is fine. Keep it flat even when a phase has many children; that is what the id is for.

### What happens to a phase's document when the phase is split

The parent's file stays, and it becomes a **split record**: its summary, its acceptance-criteria labels, its out-of-scope list, its dependencies, and a `## Split into` table listing the children in execution order with one plain-English sentence each. Everything else the parent doc carried — "Carried forward" items, phase-specific notes, work in progress — is moved into the specific child that will build it, and does not stay on the parent. Its title line says it was split, so anyone who opens it sees at once that it is not the thing to implement.

Rules the split record enforces:

- **Every acceptance-criteria label on the parent appears in exactly one child.** A criterion that would only become verifiable once two children exist means the cut is wrong or the criterion is too coarse; re-cut.
- **The children partition the parent's scope and add none.** Discoveries never become children (see the Materiality Gate in `implementation-lifecycle`).
- **Only leaves are implemented.** `implement-from-requirements` is always pointed at a phase that has no `## Split into` table. Pointed at a split parent, it takes the first child not yet closed and says so.
- **Closure is one line on the leaf.** When a leaf lands, the implement session's wrap-up writes `**Closed:** YYYY-MM-DD` under the leaf's title (plus the commit hash when that session is the one committing). A leaf is closed only when its acceptance criteria are verified and no human action recorded in its phase doc is still outstanding; a leaf waiting only on such an action is "Awaiting a Human Action" (`implementation-lifecycle`), not closed. The line is the one completion marker a phase doc carries, and it is never written at creation; other work state (blocked work, owed items, pending human actions) goes in sections, per `implementation-lifecycle`. A split record's `## Split into` table may gain a `Status` column after creation for the same purpose. "First child not yet closed" means the first child without that line; when every child carries it the parent is complete — say so, and `continuation-prompt`'s end-of-track rule decides whether a prompt follows.

### The cross-phase plan table

If the PRD directory has a `project-plan.md` or any table that lists the phases, that table lists the **level-1 phases** with a **"What it does"** column of one plain-English sentence each. Each split parent's own `## Split into` table is the plan for its children. Do not flatten a deep tree into the top-level table; walking parent → child is how the tree is read. A reader who wants "the next runnable leaf" starts at the top table and follows the first unfinished row down.

```markdown
| Phase | What it does |
|---|---|
| [1 event pipeline](./phase-1-event-pipeline.md) | Ingest domain events and store them as notification records — nothing reaches users yet. |
| [2 delivery channels](./phase-2-delivery-channels.md) | Send stored notifications out — split into 2a email, 2b in-app. |
```

---

## Process

### Step 1: Confirm the Work Is Too Large

Before splitting anything, confirm the work actually needs splitting. The unit is **a single AI session**, not human calendar time.

**What "one session" means:**

The work is happening **right now**, in this present AI session — typically a focused run on the order of minutes. "Single session" means this immediate run, not some abstract future unit of scheduled work.

So the only sizing question worth asking is: *Can I, this AI, complete this whole thing end-to-end in this run without losing coherent context?* The constraint is your ability to hold the full design mentally as you build, test, and verify it — right here, right now.

Human-time framings ("a day's work," "a sprint," "a couple of days") measure something different — humans scheduling calendar work over future time. They aren't relevant here, because the work isn't being scheduled, it's being done. Skip that framing entirely. And **use the word "phase," not "story" or "ticket"** — phases are AI-session-sized chunks of one PRD, not human work units.

**How to size honestly:**

Walk through the implementation mentally. Roughly how many files will be created or modified? How many distinct integration points? How many tests? How much investigation may be needed for edge cases discovered mid-implementation? The point is not a precise count — it's a gut check on whether the whole thing fits in one focused, coherent run. Then check that gut read against the **Session Capacity Calibration** section below — it holds the current concrete anchors for what one session reliably carries, and it corrects for the systematic bias toward underestimating.

**The decision:**

- **Fits in one session** → you don't need this skill. Hand back to `implement-from-requirements` and build it directly.
- **Too large** → continue to Step 2.

If you're genuinely unsure, lean toward splitting. The cost of an unnecessary split is small (the user can override). The cost of starting an oversized implementation is real — context fragmentation, half-built features, lost coherence.

### Step 2: Find Natural Seams

**The guiding principle: each phase should be a thin *vertical slice* — a piece of working, shippable, independently testable behavior — not a horizontal *layer*.** A vertical slice cuts top-to-bottom through whatever layers it needs (data, logic, interface) and ends with something you can deploy, demo, or at least exercise end-to-end against real inputs. A horizontal layer ("all the data model," "all the endpoints," "all the UI") delivers nothing usable until the *other* layers exist, so it can't be tested or shipped on its own. Cut vertically.

So the test for every candidate seam is the same: **at the end of this phase, can I run the tests, verify the phase's acceptance criteria, and ship (or at least meaningfully exercise) the result — without any later phase existing?** If yes, it's a real phase. If no, it's a layer masquerading as one.

**Where good seams tend to be:**

- **Separate deployables / services / components — *if each can be verified, and ideally shipped, on its own*.** A scheduled job, a REST API, and a web UI are three deployables and often three clean cuts. The bar a component must clear to stand as its own phase is **independent verifiability**: at the phase's end you can confirm its acceptance criteria by tests, with no later phase existing. A REST API clears this readily — integration tests that call the real endpoints exercise it end-to-end — so an API can be its own phase when it's consumable on its own (a programmatic-access requirement, another service that calls it) *or* when those integration tests fully cover the phase's ACs and it's the foundation the next slice builds on. You do **not** have to ship a UI alongside an API to make the API a real phase; in fact, if a thin slice through both the API and its UI would overflow one AI session, splitting them — the API carried by integration tests, the UI as a thin slice on top — is the better call. What does **not** clear the bar is a tier with nothing to verify on its own: a bare database schema, or an API whose acceptance criteria can only be checked once a UI exists. The ideal is still a slice that delivers usable value end-to-end, so make an API-only cut a deliberate choice (independent value, or sizing pressure) rather than a reflex. Judge by what you can verify, not by the component diagram.
- **Foundation-first, via a walking skeleton — *not* a foundation-only phase.** When several components share a data model or a domain engine, do **not** make "build the shared data model" its own phase — that is the classic horizontal layer that ships nothing. Instead, put the shared foundation *inside the first vertical slice that needs it*: a thin end-to-end thread (a "walking skeleton" / "tracer bullet") that stands up the shared model and the core logic **and** produces an observable, testable outcome. Later phases thicken that skeleton with more behavior. The component that *defines* the shared model goes first; dependents follow.
- **Read before write.** Ship the read/observability path before the mutation/write path when you can — reads are verifiable against real data without changing anything, and they de-risk the write path that follows.
- **Along business-workflow and rule boundaries.** A long workflow can split into "simplest happy path end-to-end first, then the extra steps and special cases." Distinct business-rule variations, simple-vs-complex handling, and "make it work / make it fast" are all places to peel a later phase off the first — each addition is its own thin slice on top of a working base.

**Worked example (shared core + three deployables).** Suppose a system has a shared data model and domain engine, a scheduled ingest job, a REST API, and a UI — with the model/engine used by both the job and the API. The weak split is "Phase 1: data model, Phase 2: API, Phase 3: UI": Phase 1 ships nothing and has almost nothing to verify on its own, and the split front-loads a dead layer before any value or end-to-end behavior appears. A strong split is: **Phase 1** = the ingest job as a walking skeleton (it forces the shared model + engine into existence and produces an observable, testable result — data read, computed, written/logged); **Phase 2** = the API for the read path, verified by integration tests against the real endpoints (fold the UI in here if it fits one session, or make it its own Phase 3 if not); **Phase 3** = the write/approval and advanced behaviors. Every phase is independently verifiable, and the shared core arrives *inside* Phase 1 rather than as a dead first layer.

**What makes a phase a good phase** (an INVEST-style check, adapted to AI-session phases):

- **Independent** — minimal back-references to phases that don't exist yet.
- **Valuable / verifiable** — it ships or demos usable value where it can, and at minimum can be exercised end-to-end against real inputs (e.g., integration tests calling real endpoints).
- **Testable** — it covers a **defined subset of the PRD's acceptance criteria** (list them by label — this is the contract that defines "done"), and each is verifiable by tests after the phase, without later phases.
- **Small** — it fits one focused AI session (Step 1).

**Size every phase, not just the PRD (the per-phase sizing gate):**

Drafting the seams is not the end of Step 2. Before moving on, apply the Step 1 sizing test to **each candidate phase individually**, with the same skepticism you applied to the whole PRD: walk through that phase's implementation mentally — files, integration points, tests, likely mid-implementation investigation (see Session Capacity Calibration below for the current anchors) — and ask whether *it* fits one focused session. Any phase that fails gets cut again using the same seam-finding principles, and the check repeats until **every leaf in the plan passes**.

**Split lazily, one depth at a time.** The finished plan for a PRD is a flat, execution-ordered list of level-1 phases. A level-1 phase that needs further cutting normally just becomes two level-1 phases — a session-sized, independently verifiable slice is the definition of a phase, so it *is* one. Reach for a second depth at planning time in one situation only: a level-1 phase that is a **natural group of many similar session-sized slices** (one sub-phase per table, one per integration, one per channel) reads better as a parent with lettered children than as fifteen unrelated-looking siblings in the top table. In that case write the parent as a split record and its children as leaves, now. Never plan deeper than the level you can honestly size today: a level-2 phase nobody has reached gets its level-3 children when it is reached and turns out to need them (see "Splitting a Phase Already in the Plan").

This gate exists because of a systematic bias: split plans underestimate. Phases get split again at implementation time far more often than they turn out too small — and a split discovered mid-implementation costs a session's worth of context and momentum, while an extra phase decided now costs almost nothing. So when a phase reads as borderline, **split it**.

**Phase count is an output, not a target:**

- A typical PRD splits into **2-4 phases**. A genuinely large PRD can honestly produce **6, 8, or more** — that's the per-phase sizing gate doing its job, not over-slicing.
- The red flag is not the count; it's **phases thinner than session capacity requires** — slivers that would each finish with most of a session's capacity unused. If every phase is honestly session-sized and there are eight of them, the PRD is simply that big; don't compress real phases to hit an aesthetic count. If many phases are slivers, merge them.
- A stubbornly enormous count *can* mean the PRD is oversized, but reopening a stakeholder-settled PRD is a rare last resort, not the default. When the level-1 count runs well past the band in `prd-roadmap`'s "PRD Size Calibration", say so in one line of the declaration, with a recommendation to re-cut the PRD into several with `prd-roadmap` — then finish the split anyway. Whether to reopen the PRD is the user's decision, not a reason to stop.

**When a clean split is hard — do your best before pushing back.** Phasing happens *after* the PRD has usually been hammered out with stakeholders, so reworking it is expensive and frequently off the table. Your job is to **make the split work**, not to bounce it back. If no cut gives every phase standalone end-user value, fall back in this order:

1. **Reach for more techniques before concluding it can't be split** — happy-path-first workflow steps, simple-vs-complex, defer-performance, a spike for the genuinely unknown part, business-rule or data variations. Most "unsplittable" PRDs simply haven't been viewed through enough of these lenses.
2. **Accept an independently *verifiable* phase even when it isn't independently shippable.** A phase you can build and confirm by tests — and that later phases build on — is a good phase even if you wouldn't deploy it to end users on its own (a foundational engine/data slice behind a walking skeleton is the usual case). Verifiability is the floor; standalone user value is the ideal, not a hard gate.
3. **Grow the first phase** to absorb a tightly-coupled core rather than manufacturing a phase with nothing to verify.

Only in **genuinely extreme cases** — where even sensible build-ordering leaves every phase circularly depending on the others — surface that the PRD may be too tangled to phase, and talk it through with the user (which may or may not involve revisiting the PRD). This is the one place in this skill where stopping with a question is right, because the answer may be to change the PRD, and that is not the session's call. Reconsidering the PRD is the rare exception, not a routine escape hatch.

The one thing to keep avoiding is **slicing horizontally** (all-schema → all-endpoints → all-UI), where no phase can be verified or shipped on its own — if you catch yourself there, re-cut vertically.

> **Where this guidance comes from.** These are long-standing, widely-taught delivery practices, not local invention: *vertical slicing* and the *INVEST* criteria for a good slice (Bill Wake); the *story-splitting patterns* — workflow steps, business-rule and data variations, simple/complex, defer-performance, spike (Richard Lawrence / Humanizing Work); the *walking skeleton* (Alistair Cockburn); and *tracer bullet development* (Hunt & Thomas, *The Pragmatic Programmer*). Phases here are AI-session-sized rather than sprint-sized, but the "ship a thin vertical slice, never a horizontal layer" principle is identical.

### Step 3: Decide the Split and Declare It

Write the split up in the response **as a decision, then proceed to Step 4 in the same turn.** Do not end the turn to ask whether to split, whether the recommended cut is acceptable, or which of several cuts the user prefers. The methodology's rule for predictable questions applies (`implementation-lifecycle`: never stop to ask when you are ≥90% confident of the answer), and "should I split as recommended?" is the canonical predictable question — the recorded answer is yes, every time, and every time the session stopped to ask it the answer arrived hours later. If two cuts are genuinely close, pick the one that flows most logically (below) and say in one line why; the user redirects after the fact if they disagree, and a redirect costs a few minutes of rewriting uncommitted markdown.

The declaration is a structured write-up the user can check at a glance. For each phase include:

- **Id and title** — `2a`, "Notification event pipeline". Ids per "Phase Identifiers and File Layout."
- **Scope** — which acceptance criteria from the PRD (or from the parent phase, when splitting a phase) this phase covers, by label.
- **Out of scope for this phase** — what's deferred to later phases.
- **Dependencies** — must any prior phase complete first? Why? (Phase 2 often builds on Phase 1's data model — be explicit so phase ordering is correct.)
- **Brief rationale** — one line on why this cut.

**Number phases in the order they will actually be executed.** The default execution model is strictly sequential: phase 1 is implemented, tested, and verified working before phase 2 begins, and so on, one phase per session, in id order (children in their parent's slot). So the numbering is not merely *a* valid ordering — it is **the** order the work will proceed in, and it must be the order a sensible engineer would naturally proceed in. Run two checks before declaring the split:

1. **Dependencies point backward.** A phase may only depend on phases earlier in the sequence — if your draft has "Phases 4 and 7 must complete before Phase 3," the numbering is wrong; renumber so every dependency points backward.
2. **Sequential walkthrough.** Mentally execute the plan in order. At each phase ask: with only the earlier phases built, does everything this phase needs already exist, and can it be built and verified right now? If at any step the honest answer is "I'd actually do X first," the numbering is wrong — fix the numbers, don't note it as an aside. The sequence must read as the natural way to build the system at every step, not just a dependency-valid sort.

Parallel execution is a rare, user-chosen exception — never a planning input. Independent phases *may* be noted as parallelizable in the declaration (e.g., via worktrees), but never design or order the split around assumed parallelism; someone following the numbers sequentially must always be doing the right thing. When dependencies leave several orderings valid, pick the one that flows most logically — foundation before dependents, core workflow before variations and polish — and among equally logical orders, put the phase that delivers or de-risks the most first.

### Step 4: Write the Phase Documents

Create one document per phase in the PRD's directory, named and placed per "Phase Identifiers and File Layout" (see `prd-writing-standards` for the directory convention):

```
docs/prds/{prd-name}/               ← or docs/changes/{prd-name}/
  phase-1-{short-name}.md
  phase-2-{short-name}.md
  phase-3-{short-name}.md
```

A phase doc is a **scope-setting overlay** on the parent PRD and the single technical design. It is NOT a mini-PRD and NOT a mini technical design. It does NOT duplicate content from the parent documents.

**Why no duplication:** if the PRD or technical design changes later, duplicated content drifts out of sync. The PRD and technical design remain the single source of truth; phase docs only add what's specific to scoping that phase.

Each phase doc should contain:

- **Pointer to parent documents** — explicit paths to the PRD and the technical design. If helpful, name the specific technical-design section headings this phase implements (don't copy them). A child phase also names its parent phase doc.
- **Summary** — 1-2 sentences on what this phase delivers, **in plain English**. Write it for a smart reader who wasn't part of the project: no undefined project shorthand, actors and direction named ("the correction package we hand to Vendor X," not "Correction Handoff"), and nothing claimed beyond what the phase's acceptance criteria actually require. This is the same standard as `prd-writing-standards` → "Plain English for Readers Outside the Project"; the Summary is a gloss on the criteria, so check it against them and confirm it neither overclaims nor underclaims.
- **Acceptance criteria covered** — list which criteria from the parent PRD are in scope, **by label** (e.g., "AC-REV-01, AC-REV-02, AC-GRP-07"). **Don't re-state the full criterion text** — the implementing AI reads the full PRD before building, and duplication invites drift. The implementer's stale-phase-doc check catches drift between these references and the current PRD.
- **Out of scope for this phase** — what's deferred to later phases.
- **Phase dependencies** — which phases must come first.
- **Phase-specific implementation notes** — only if there's something unique to this phase that isn't already in the parent technical design.

**Leaf template** (copy this skeleton — every section is one or two lines):

```markdown
# Phase 2a: [Short title]

**Parent PRD:** [path to {prd-name}-prd.md]
**Technical design:** [path to technical-design.md] — relevant sections: [heading(s)]
**Parent phase:** [path to phase-2-{short-name}.md] — omit this line for a level-1 phase

## Summary
[1-2 sentences on what this phase delivers — plain English, no undefined project shorthand.]

## Acceptance criteria covered
[Parent-PRD AC labels only — e.g. AC-XXX-01, AC-XXX-02. Do not restate the text.]

## Out of scope for this phase
[What's deferred to later phases.]

## Phase dependencies
[Which phases must come first, or "None — first phase."]

## Phase-specific notes
[Only if something is unique to this phase and not already in the technical design. Omit this heading entirely if there's nothing to add.]
```

**Filled-in example:**

```markdown
# Phase 1: Event pipeline

**Parent PRD:** docs/prds/user-notifications/user-notifications-prd.md
**Technical design:** docs/prds/user-notifications/technical-design.md — relevant sections: "Event ingestion", "Data Models"

## Summary
Ingest domain events and persist them as notification records. No delivery channels yet.

## Acceptance criteria covered
AC-EVT-01, AC-EVT-02, AC-EVT-05

## Out of scope for this phase
Email and in-app delivery (Phase 2); user notification preferences (Phase 3).

## Phase dependencies
None — first phase; later phases build on its data model.
```

(The example omits "Phase-specific notes" because there's nothing phase-specific to add — that's the norm, not an oversight.)

**Split-record template** — what a phase's own document becomes when the phase is split (see "What happens to a phase's document when the phase is split"):

```markdown
# Phase 2: Delivery channels — split into 2a-2b

**Parent PRD:** [path]
**Technical design:** [path] — relevant sections: [heading(s)]

## Summary
[Unchanged from before the split.]

## Split into
| Phase | What it does |
|---|---|
| [2a email channel](./phase-2a-email-channel.md) | Send stored notifications by email, retrying when the provider is down. |
| [2b in-app channel](./phase-2b-in-app-channel.md) | Show the same notifications inside the app, marked read when opened. |

Split 2026-09-12 at sizing time: each channel is a session on its own. [One line; no narrative.]

## Acceptance criteria covered
[The parent's labels, unchanged. Each appears in exactly one child.]

## Out of scope for this phase
[Unchanged.]

## Phase dependencies
[Unchanged.]
```

Add an `Owner` column to the `## Split into` table only when different people run different children. Everything the parent carried beyond these sections — "Carried forward" items, notes, work state — moves to the child that will build it.

**If the split is also recorded in a cross-phase plan table** (`project-plan.md` or any table that lists every phase), keep that table to level-1 phases with a **"What it does"** column of one plain-English sentence each — see "The cross-phase plan table" above. A split parent's row gains a clause naming its children ("split into 2a email, 2b in-app").

**Leave out the fluff.** At creation, a phase doc is a pointer, not a document of record. Do **not** include: restated acceptance-criteria text, copied or paraphrased technical-design content, background or motivation (that's the PRD's job), effort or time estimates, status/owner/date boilerplate, or a narrative defending the split (that was the Step 3 declaration; the split record's one dated line is the whole exception). If a section has nothing phase-specific to say, drop the heading — a row of "N/A" is itself fluff. A typical phase doc **starts at** 10-20 lines; if yours is longer at creation, you're probably duplicating a parent document. Growth *after* creation is different: work routed in from other phases ("Carried forward from Phase N" sections, per the No Loose Ends discipline in `implementation-lifecycle`) is legitimate content, and on a long project it can grow the doc considerably — that's the doc doing its job as the ledger for its phase, not fluff.

### Step 5: Hand Off

What happens after the documents are written depends on who invoked this skill. In every case, **do not implement inside this skill**, and the documents are committed or pushed only under live user authorization — staged and validated per `pre-commit-validation` here when invoked directly, or at the implement session's wrap-up when they ride its changeset.

**Called from an implement session** (`implement-from-requirements` sized the work at its Phase 2 and delegated here, or the phase being built turned out too large mid-implementation): return to that skill. Outside an authorized `phase-chain`, **it continues in the same chat with the first leaf** — at sizing time, the first child; mid-implementation, the child that holds the work already in progress. The context that session loaded is exactly what the first leaf needs, and the leaf is session-sized by construction, so a fresh chat would only re-read the same documents. The new phase docs ride in that session's changeset. This skill produces no prompt in this case; the implement session's wrap-up produces the next leaf's prompt via `continuation-prompt`.

**Invoked directly by the user** (`/phase-split` on a PRD, or on a phase the user already knows is too large): this chat's purpose was planning, so stop after the documents are written. Tell the user the phase docs are created; commit/push when covered by live user authorization, otherwise present the message for approval; then provide a copy-paste prompt for the first leaf's chat using `continuation-prompt` (it owns the chat-name line, the lineage block with the PRD and phase by full title, the ordering, and the rule that the prompt points at the phase doc rather than restating it); the prompt is valid once that commit lands. Shape, abbreviated:

> Phase documents created:
> - `docs/prds/user-notifications/phase-1-event-pipeline.md`
> - `docs/prds/user-notifications/phase-2-delivery-channels.md`
> - `docs/prds/user-notifications/phase-3-preferences.md`
>
> To start Phase 1 in a fresh chat, paste this prompt:
>
> > ph1 userN impl
> >
> > In service of: User Notifications (PRD)
> >   Phase 1 — Event pipeline
> >   This chat: implements it.
> >
> > Use the `implement-from-requirements` skill. Implement `docs/prds/user-notifications/phase-1-event-pipeline.md`. The parent PRD is `docs/prds/user-notifications/user-notifications-prd.md` and the technical design is `docs/prds/user-notifications/technical-design.md`. Work in the shared checkout `<absolute path to the repo>`, on `develop` directly. First: read all three, then size the phase.
>
> Valid once the phase docs are committed (commit message above).

**Inside an authorized `phase-chain`**, whether this skill was invoked directly or from an implement session: return the completed planning delivery to that orchestrator; it commits, pushes, and dispatches the first leaf to a new task after its delivery gates, per that skill. The implement session does not continue with the first leaf in the same chat.

---

## Session Capacity Calibration

The sizing test used throughout this skill — *can I hold the full design coherently while I build, test, and verify it in this run* — is deliberately model-relative, so it never needs revision as models improve. This section holds the part that **does** age: the concrete anchors for what "one session" reliably carries with current models. **When models and harnesses improve, this section is the only thing to revise; nothing else in this skill, and nothing in `implement-from-requirements`, states capacity numbers.** Anchors last revised: **August 2026**.

A phase sized for reliable single-session completion looks like:

- **One reviewable PR.** A phase lands as a single coherent, reviewable changeset — this is the unit that survives model upgrades. As a sanity band, that's typically on the order of **10-15 files and several hundred to ~a thousand net lines** including tests. This band is a judgment call informed by benchmark and practitioner data, not a measured limit: a well-spec'd phase in a familiar codebase can run past it with a clear conscience. Treat it as a tripwire, not a cap — if the mental walkthrough shows a *multiple* of it, the phase is really two.
- **Roughly 3-7 acceptance criteria, every one machine-verifiable** — a test, build, or script the session itself can run. An AC only a human can check is a phase-boundary smell: reliability tracks how much of the work the session can verify as it goes, more than how big the diff is.
- **Finishes without leaning on context compaction to preserve correctness.** Coherence degrades well before context limits are reached; the whole build-test-verify loop should fit comfortably in one window. Wall-clock time is not the constraint — a phase that waits on long-running jobs or migrations is fine as long as the reasoning around the waiting still fits.

**Size for the dependable case, not the impressive case.** Measurements of frontier coding agents consistently show a several-fold gap between the largest task a model can *sometimes* pull off single-shot and the largest it completes *dependably* — and plan-time sizing naturally anchors on the impressive case. These anchors sit deliberately at the dependable end; a well-spec'd phase in a familiar codebase treats capacity beyond them as upside, not plan. Dependable single-session completion is also what the rest of the methodology assumes: the review and test-hardening passes that follow implementation are there to polish a phase that landed coherently, not to rescue one that overran its session.

---

## Splitting a Phase Already in the Plan

Sometimes a phase that looked session-sized turns out not to be — `implement-from-requirements` discovers it at sizing time, or mid-implementation when the work keeps growing. The original split was an estimate; revising it is normal, not a failure. This works the same at every depth: a level-1 phase gets lettered children, a level-2 phase gets numbered children, and so on down.

The procedure is the same as a fresh split, scoped to what's left:

- **Scope = the phase's remaining work only.** Anything already implemented and verified stays done — don't re-plan it. If implementation is partially complete, the first child picks up exactly where the work stopped, and its doc says so. "Remaining work" means the work the phase was already scoped to carry — a split never converts mid-implementation discoveries into new phases. Discoveries go through the Materiality Gate and disposition rule (`implementation-lifecycle`); most are dismissed or filed, not phased.
- **The children take the next depth down; every other id in the plan stays put.** Phase `2` becomes a split record and its work lands in `2a`, `2b`, …, executed in letter order in the slot where `2` sat. Phase `2a` splits into `2a1`, `2a2`, …. Plan tables, other phase docs' dependency lines, and references already made in commits, chat names, and people's heads all stay valid, because no existing id changes. The one exception: a split whose ids nothing references yet — typically the plan you wrote earlier in this same session — is simply corrected in place, as flat siblings at the same depth. Never append the remainder as new trailing siblings and never renumber a referenced plan.
- **Convert the parent's document into a split record** per "Phase Identifiers and File Layout," moving its carried-forward items and work state into the specific children that will build them.
- **Update every surface that lists the phases** — the other phase docs' dependency lines and any cross-phase plan table — so the split stays coherent.
- **Same decide-and-declare rule as Step 3.** State the cut, write the docs, continue. Do not stop to ask.

Execution-order rules still hold: a child may only depend on phases earlier in the sequence, and the revised sequence must still pass the sequential walkthrough from Step 3.

---

## Rules and Constraints

### DO

- Confirm the work is genuinely too large for one AI session before splitting — don't manufacture phases.
- Size by AI-session capacity, not human calendar time.
- Use the word "phase," not "story" or "ticket."
- Find seams where each phase is independently buildable, testable, and shippable.
- Size **every candidate phase individually** against the Session Capacity Calibration anchors, and keep cutting until each leaf fits a session — a borderline phase gets split. Phase count is an output, not a target.
- Map each phase to a defined subset of the PRD's acceptance criteria, referenced by label; when splitting a phase, every label on the parent lands in exactly one child.
- Number phases in the order they will actually be executed — sequentially, each built and verified before the next starts. Dependencies may only point backward, and the sequence must survive the sequential walkthrough: the natural build order at every step, not just a dependency-valid one.
- Use positional ids (`2`, `2a`, `2a1`) and the filename `phase-{id}-{short-name}.md`, one file per phase at every depth, all flat in the PRD directory.
- Decide the split, declare it in the response, and write the documents in the same turn.
- When splitting a phase already in the plan, convert its document into a split record and move its carried-forward items and work state into the children that will build them.
- Keep phase docs as thin scope overlays on the parent PRD and the single technical design **at creation** — later growth from work routed in by other phases is legitimate.
- Write each phase Summary — and any plan table's "What it does" column — in plain English a reader outside the project can follow, without claiming more or less than the phase's acceptance criteria.
- Hand off per Step 5: back to the implement session when called from one (outside a `phase-chain` it continues with the first leaf in the same chat); stop with a prompt for the first leaf when invoked directly; inside an authorized `phase-chain`, return the planning delivery to the orchestrator, which dispatches the first leaf to a new task.

### DO NOT

- Stop to ask whether to split, or which cut to use — declare the decision and proceed. The only question this skill ends a turn on is the extreme "this PRD may be too tangled to phase" case.
- Estimate work in human time ("a day's work," "a sprint") — the work happens in this session, not on a future calendar.
- Compress honestly session-sized phases to hit a small phase count, or pad the plan with sliver phases that would leave most of a session unused — the count follows from per-phase sizing, in both directions.
- Put an owner, a subject code, a track name, or anything but position in a phase id. Owners go in a table column; subjects go in the short-name.
- Write a phase as a heading inside another phase's document, or write a "plan" document that holds several phases as sections — one phase, one file, always.
- Plan deeper than you can size today — children are written when their parent is known to be too large, at planning time for a natural group and otherwise when the phase is reached.
- Create phases to house work discovered mid-implementation — discoveries are dispositioned per `implementation-lifecycle` (most dismissed, some filed), never phased. Phasing delivers existing scope; it is not a place to put new scope.
- Order or design the split around assumed parallel execution — sequential one-phase-at-a-time is the default; parallelism is an occasional user-chosen exception, not a planning assumption.
- Split the technical design into per-phase designs — there is one design per PRD, referenced by all phases.
- Restate PRD acceptance criteria or technical-design content inside phase docs.
- Implement inside this skill — hand back to the implement session, or hand off to a fresh chat.

---

## Relationship to Other Skills

| Skill | How This Skill Relates |
|-------|-------------------------|
| `implementation-lifecycle` | The methodology umbrella. Phase documents are one of its four entities: born here as thin overlays, they become the preferred landing place for follow-up work discovered in other phases. Its "never stop to ask a predictable question" rule is why Step 3 declares instead of asking. |
| `implement-from-requirements` | The downstream consumer. Its Phase 2 sizing gate hands work here when it's too large (including a phase at any depth that turned out bigger than assumed); once the docs exist it continues with the first leaf in the same chat (inside an authorized `phase-chain`, the orchestrator dispatches it to a new task), and later leaves get one fresh chat each. It is always pointed at a leaf. |
| `phase-chain` | The Codex orchestrator. When a chain is active, a split, whether invoked directly or from an implement session, is a planning delivery it commits and hands to the first leaf's successor in a new task. |
| `prd-writing-standards` | Owns the `docs/prds/` and `docs/changes/` directory convention that phase docs live in, the `AC-<AREA>-<NN>` labels phase docs reference, and the plain-English readability standard that phase Summaries and plan tables follow. |
| `technical-design-writing-standards` | Defines the single technical design per PRD that phase docs point into by section heading — the design is never split or duplicated per phase. |
| `prd-roadmap` | The same job one level up: it cuts an idea too big for one PRD into right-sized planned PRDs, reusing this skill's seam principles at PRD scale. Each planned PRD, once written, comes here to be split into phases. |
| `autonomous-requirements-refinement` / `implementation-readiness-check` | Should already have run against the PRD and technical design before this skill is invoked — this skill assumes the requirements are implementation-ready, it just decides whether they're too large for one session. |
| `continuation-prompt` | Produces the first leaf's copy-paste prompt when this skill was invoked directly: a chat-name line first (`ph2a1 …`), then the lineage block (PRD and phase by full title), pointers into the phase doc, valid once the phase-docs commit lands. |

---
name: review-technical-design
description: "Senior review that revises a freshly drafted technical design in place, between technical-design-writing-standards and autonomous-design-refinement — an independent would-I-build-it-this-way architecture pass, load-bearing claims verified against the real codebase and infrastructure (read-only), data-model changes tested against the current ecosystem and future evolution, and the house engineering standards applied. Fixes every gap and false claim, swaps a working choice only for a verified defect from a closed list, never overrides a settled decision or adds scope, commits the revision, and reports what changed and which sections are worth a person's reading. Runs in a fresh context once the draft is committed; skips itself for a design that follows an established pattern. A design someone else owns, such as a pull request, gets the report without edits. Not for writing designs or reviewing code."
user-invocable: true
---

# Review a Technical Design Document

## Where this fits, and when to run it

Run it after `technical-design-writing-standards` has drafted and committed a design,
and before `autonomous-design-refinement`. The drafting skill starts it; run it by
hand on a design that skipped it.

**It runs in a fresh context** — a subagent, or a new chat — never in the session that
wrote the design. The architecture pass starts by sketching an independent design
before reading this one, and a session that just wrote the design can't.

**It skips itself** when the design follows an established pattern and makes no
decision that is expensive to reverse: no new service, no new or changed schema or
data model, no new public interface. Say so in one line, record it with an empty
commit (Phase 6), and stop.

The order matters. `autonomous-design-refinement` fills gaps *inside* the design's
frame and deliberately never asks "would it be better if…". This skill is the one
that questions the frame. Refining a design that is then restructured wastes the
refinement.

Designs are too long for a person to read in full, and an AI-written design reads
polished and confident whether or not it is right. So the review does the work
rather than handing it over: it revises the design, commits the revision, and leaves
a short report saying what changed and the few sections worth a person's reading.
That reading is recommended, not required; nothing waits on it.

## The author model: an AI's first draft

Review every design as an AI's first draft, perhaps steered by a person who may not
have known where to point it. That is what the drafting skill produces, and a design
from a more senior author loses nothing from the same scrutiny. It changes what the
document's surface tells you:

- **The strong parts are real but not diagnostic.** Deep research, assumption IDs
  cited inline, structured decision tables, verification annotations, confident
  prose — AI produces all of that for free. A polished design is the baseline, not a
  signal of sound judgment. Any strength claim must point at specific verified
  substance.
- **The gaps hide where nobody pointed.** The AI's thoroughness follows the map of
  the problem it was given — deep where someone knew to ask, silent where nobody
  did. Coverage gaps, not errors, are the signature failure; hunt for what the
  design never considered, not just what it got wrong.
- **The first reasonable idea became the design.** Nobody pushed back on it, and
  nobody in that loop knew the house's opinionated technical decisions unless those
  standards happened to be loaded.

The review fills two gaps:

1. **Verification against reality.** A design is full of factual claims about the
   codebase and infrastructure — "the cookie is named X," "the routing rule is at
   priority Y," "the API already exposes Z." Risk concentrates exactly where those
   claims are wrong, because everything downstream was reasoned from them.
2. **Zoomed-out judgment.** Is this the right approach at all? Is it consistent with
   how the rest of the system is built? Is there prior art — an existing service
   doing something similar — the design should learn from? The draft couldn't ask
   these questions without the context.

## Phase 1 — Load context before reading the design

1. Read the parent artifacts first: the PRD, the assumptions document, any
   architecture-options notes. Note which decisions are already **made** (validated
   assumptions with IDs, decisions the PRD or assumptions record). Those are
   settled — the review evaluates the design *given* them and does not change them
   (Phase 5, "What it never changes").
2. Load the standards the design will be judged against: `engineering-principles`,
   `technical-design-writing-standards` (what belongs in a design and at what
   altitude), and every house standard named on an `Engineering standards:` line in
   the project's `AGENTS.md` (or the user's global map). If none is named, the
   conventions visible in the codebase are the house standard.
3. Skim the target codebase(s) enough to know where things live — Phases 2–3 need it.
4. Look for an existing data-model document, schema catalog, decision record, or
   service-owned model documentation. Use it as a map, not as proof that deployed
   reality matches. For the portions load-bearing to this change, verify the
   relevant serializers, validators, migrations, storage and index definitions,
   access paths, and lifecycle and deletion code. If no model documentation exists,
   reconstruct only the affected slice from the owning services and stores. Prefer
   read-only inspection of a non-production environment, using resource metadata
   and sanitized representative shapes. Do not inspect production customer content
   to validate a design.
5. When the affected data crosses several services or stores and subagents are
   available, delegate one bounded **data-model ecosystem pass** in parallel: give
   it the proposed changes, the likely owning repositories, the documentation map,
   and the non-production constraints; have it return sources of truth,
   documented-versus-actual discrepancies, compatibility and evolution risks, and
   evidence locations. Keep a small local change in the main review, and verify any
   subagent's load-bearing conclusions yourself.

## Phase 2 — The architecture pass: would we build it this way?

This is the review's center of gravity, and it runs **before** line-level
verification. Fact-checking a design inside its own frame — contradictions, wrong
claims, missing error codes — accepts the architecture by default. The question this
skill exists to answer comes first: **is this built the right way at all, or is
there a simpler way?**

1. **Sketch your own design first.** From the PRD, assumptions and constraints only
   — before absorbing the design's solution sections — write the simplest
   architecture you'd build: 3–5 sentences plus a count of new moving parts
   (services, repos, tables, queues, buckets, scheduled jobs). This is the only
   reliable way to avoid anchoring on the draft's frame.
2. **Diff yours against theirs.** Every moving part or layer of generality the
   design has that your sketch doesn't must be pulled in by a requirement or a named
   constraint — not by momentum, symmetry, or AI enthusiasm. Every part your sketch
   has that theirs lacks is a question to answer.
3. **Check the roads not taken yourself.** The design names only what it chose;
   finding the alternatives is this pass's job. Could an existing service absorb
   this? Does something already running do 80% of it? Is there a managed capability
   of the platform, or an off-the-shelf tool, that makes the custom thing
   unnecessary? What would the dumb version look like, and which requirement
   actually kills it?
4. **Find the first ceiling.** Where does the chosen design break first — scale,
   latency, cost, a hard platform limit? Is hitting it acceptable for the stated
   problem, observable as it approaches, and recoverable without a rewrite? Verify
   claimed platform limits against provider documentation; folk numbers are wrong in
   both directions.
5. **Classify the doors.** Which decisions are one-way doors (contracts spread
   across many components, data models, anything expensive to unwind) and which are
   two-way (a service that could merge into another later, a sync flow that could go
   async behind the same endpoint)? Scrutiny — and the "read personally" list —
   concentrates on the one-way doors.
6. **Model the data in its ecosystem.** For every added or changed entity, field,
   event, index, table, object path or cache, trace its authoritative source, owner,
   readers, writers, authorization boundary, lifecycle and deletion path. Compare it
   with the existing naming, identity, timestamp, tenancy, test-data and versioning
   conventions.

   Before approving a model that will accumulate customer data, run a
   **future-capability probe**. Think one or two plausible product generations
   beyond the named roadmap — not to add those features now, but to expose choices
   that become disproportionately expensive once production history exists:

   - Derive 3–5 credible future capabilities from the product domain, adjacent
     systems, roadmap signals and normal platform evolution: new actors and
     permission scopes, new source or subject types, longitudinal and audit views,
     recomputation under a new algorithm or taxonomy, analytics/export/ML consumers,
     entity merge and split, materially different volume or access patterns.
   - Walk each through today's proposed records and contracts. Name the fields,
     relationships, provenance, history, access paths and policy boundaries it would
     need. Does old data stay interpretable? Can old and new readers coexist? Would
     enabling it require re-keying, repartitioning, a destructive rewrite, an
     impossible backfill, or changing the meaning of an existing field?
   - Concentrate on semantics that harden as data accumulates: identity and foreign
     keys; record grain and cardinality; event history versus current state;
     provenance and derivation version; units, precision, timezone and
     effective-time meaning; null/unknown versus zero; taxonomies and enums; tenancy
     and authorization ownership; partition and sort keys; correction, retention,
     deletion and consent.
   - Capture the result compactly, for the report, as **decision → future
     capability → lock-in mechanism → current accommodation → migration/exit path →
     verdict**. A material one-way door without a credible exit path belongs on the
     read-personally list.

   This is option preservation, not permission to gold-plate. Change the design when
   a plausible capability exposes costly lock-in and a modest boundary, stable
   identifier, provenance field, version marker or separation of concerns preserves
   the option (Phase 5, a swap). Otherwise leave the design as it is, note the
   constraint and exit path in the report, and defer the speculative machinery. Also
   run the near-term thought experiments: source data changes after a decision;
   readers and writers deploy at different times; volume exceeds one page or item
   limit; retention policy changes; a label is renamed; a record must be migrated or
   replayed years later. Prefer derived projections over duplicated mutable truth,
   stable IDs over labels, versioned contracts over implicit shapes, and explicit
   migration paths over claims that a schema is "flexible." A locally elegant design
   is still wrong if it creates an orphan data island or blocks the next plausible
   product evolution.

   Established evolution tests, independent of database or serialization format:

   - Assume producers, consumers and rollback versions overlap; name backward and
     forward compatibility and use expand/migrate/contract for breaking changes
     ([Parallel Change](https://martinfowler.com/bliki/ParallelChange.html),
     [schema compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)).
   - Never recycle a retired field or enum identifier where the format gives it wire
     meaning; preserve unknown data when the format supports round trips
     ([Protobuf best practices](https://protobuf.dev/best-practices/dos-donts/)).
   - Design from real access patterns and verify pagination, record size,
     cardinality and hot-key limits rather than relying on "schemaless" flexibility
     ([DynamoDB modeling foundations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html)).
   - For derived projections, define lag, idempotent rebuild and replay, correction,
     reconciliation and source-unavailable behavior
     ([CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)).
   - Treat live objects, historical versions, soft deletion, replicas, exports and
     backups as separate lifecycle surfaces; deleting from one is not evidence of
     deletion from the others.

The pass fills the **Architecture** checklist in the report (Phase 6): one ✅/⚠️/❌
mark per dimension with a one-line justification. Your sketch is a tool for finding
defects, not a replacement design: a difference between the two changes the design
only when it exposes a defect that qualifies a swap (Phase 5). The checklist names
the strongest losing alternative even when the design stands — in the report, never
in the design. A row of unexplained ✅s is indistinguishable from not having done the
pass.

### What good architecture means here

A handful of external touchstones, each reduced to the question it contributes:

- **Gall's Law** — a complex system that works evolved from a simple system that
  worked. *Is this the simple system, or a designed-complex one hoping to work on
  the first try?*
- **YAGNI** (Fowler) — machinery for imagined future needs costs more than it
  saves. *Which parts exist for requirements nobody validated? Strike them.*
- **Choose Boring Technology** (McKinley) — you get a few innovation tokens, and the
  house stack is the boring default. *What's novel here, and did it buy its way in
  with a real requirement?*
- **Architecture is the stuff that's hard to change, and every choice is a
  trade-off** (Fowler/Johnson; Richards & Ford). *Does the design name the
  constraint that decided each choice? Scrutiny in proportion to irreversibility.*
- **One-way vs. two-way doors** (Bezos) — most decisions are reversible and should
  be made quickly; the few that aren't deserve senior attention. *Are the one-way
  doors identified, and are they the best-verified parts?*
- **Cost and operational excellence** (Well-Architected) — every always-on
  component bills monthly and pages someone when it breaks. *What does this cost to
  sit idle, who operates it, and is that proportionate to the feature's value?*

## Phase 3 — Verify the load-bearing claims (read-only, never ask permission)

Do not read the design linearly and nod along. Extract its factual claims and check
the ones it leans on:

- **Code claims.** Named files, components, config keys, cookie names, field names,
  flags: grep the actual repo. Confirm the thing exists, is named what the design
  says, and behaves the way the design assumes (read the surrounding lines, not just
  the hit). Environment-dependent behavior is a classic miss — a name or value that
  differs between environments breaks exactly where the first integration test runs.
- **Infrastructure claims.** Timeouts, routing rules and priorities, DNS/CDN
  topology, compute sizing, certificate and domain assumptions: check the
  infrastructure code and, read-only, the deployed resources. If the design claims a
  slot, priority or namespace is free, sweep the other repos that share that resource
  for collisions, including values computed from variables, not just literals.
- **Data-model claims.** Start from any model documentation, then check the
  load-bearing slice against real serializers, validators, queries, keys, indexes,
  migrations, infrastructure definitions, lifecycle, backup, permissions and deletion
  code. Identify which record is authoritative and which is derived. If
  documentation and reality differ, reality governs the review and the discrepancy
  is a finding. Don't infer deployed shape from infrastructure code alone, or
  object-level behavior from resource-level policy.
- **Internal consistency.** Designs contradict themselves — one section says the new
  repo owns a resource, the rollout plan assigns it to another. Cross-check the
  decisions against the interfaces, integration points and repos touched.
- **Sibling documents.** Grep `docs/prds/` and `docs/changes/` for older PRDs or
  designs covering the same feature. A predecessor the current design changes is
  not rewritten: the new design's decision and the PRD's criteria carry
  `Replaces:` lines naming what they change (`prd-writing-standards`, "When Later Work
  Changes an Earlier Criterion"; `technical-design-writing-standards`, "Changes to
  an Earlier Design"). A contradiction without a `Replaces:` line is a defect —
  two documents both claiming to be current.
- **Links and references.** Every referenced artifact must resolve as a
  repo-relative path. Paths pasted from someone's local notes are broken links for
  everyone else.
- Spot-check even claims annotated "verified" — a couple at random. The annotation
  is a claim too.

Read-only verification (grep, file reads, infrastructure-code reads, read-only CLI
and API calls) never needs permission. Do it before forming opinions. Never write to
a shared or production system to check a claim.

## Phase 4 — Evaluate through the lenses

Rank findings by these, roughly in this order of severity:

1. **Reality.** Claims verified false or unverifiable (Phase 3). Highest severity,
   because the design was reasoned from them.
2. **Failure behavior.** Fail loudly, never silently (`engineering-principles`). No
   fallbacks or defaults masking broken states; partial output never ships under a
   success status; every external call is bounded by a timeout; distinct error
   contracts a client can act on. Assume the compute can disappear mid-operation —
   operations idempotent and safe to retry, no state that only lives on one
   machine's disk, and abrupt termination (deploy, restart, scale-in) either handled
   or explicitly accepted with rationale. Failures must surface in telemetry the
   service emits deliberately, not in something an engineer has to log in and find.
3. **Capacity and admission control.** Anything expensive (rendering, batch work,
   fan-out) needs a server-side answer to "what happens at capacity" — queue, reject
   with a defined status, or cap. A client-side guard (disabled button, debounce) is
   UX, not enforcement. "Tune empirically" is fine for sizing numbers, not for the
   *behavior* at the limit.
4. **Auth and credential exposure.** Minimize the surfaces a credential touches;
   never logged, never persisted. Where data scoping and entitlements matter,
   consider passing the user's own credentials through rather than widening a
   service account's reach. Any component that fetches or renders things must not
   be an open proxy or renderer (SSRF).
5. **Drift resistance.** Single sources of truth, derived rather than duplicated. A
   hand-maintained list or count that must change when something else changes is a
   drift bomb — derive it, colocate it, or guard it with a CI check. Designs whose
   whole purpose is avoiding drift still sneak these in at the edges.
6. **Data-model ecosystem fit and evolution.** New data has a clear owner and fits
   the system's existing sources of truth, identity and time semantics, tenancy and
   authorization boundaries, naming and index conventions, test-data handling,
   retention, backup and deletion model — checked against actual code, migrations
   and safe deployed metadata, not one overview document. Require explicit schema
   versions, mixed-version reader/writer behavior, correction and replay semantics,
   bounded growth and pagination, a migration and rollback strategy, and the Phase 2
   future-capability probes with a path through or out of each material lock-in.
   Flag duplicated mutable truth, label-based identity, unbounded embedded
   collections, undocumented derived stores, and records that can't be recomputed or
   safely retired. If data-model documentation exists, the rollout plan should
   update it once the schema is implemented and verified — not during design.
7. **Simplicity and first principles.** Challenge inherited complexity and
   speculative machinery (job tables, polling flows, caches) that a simpler
   synchronous or config-driven approach makes unnecessary — and challenge false
   simplicity that ignores a limit and only works until the first real-world
   ceiling. What are we actually trying to accomplish, and what's the least
   machinery that does it?
8. **House standards and codebase conventions.** Evaluate the design against the
   house engineering standards named on the project's `Engineering standards:`
   line, if any, and against the conventions visible in the codebase: stack,
   hosting, project layout, configuration and secrets handling, deployment, where
   infrastructure code lives. Prefer what the house already runs over something the
   team would have to learn and operate; self-operating what a managed service
   already provides needs an argument. A deviation needs a requirement behind it,
   stated in the design.
9. **Testability and incremental delivery.** Tests are rails that let the work move
   faster, not gates it stops at: automated in the pipeline, living in the same repo
   as what they test, runnable against every non-production environment, and at
   most read-only checks against production — evidence never comes from writing to
   production (`engineering-principles`). That implies tagged test records in real
   non-production stores rather than a fresh-database or exclusive-environment
   assumption. Scope tests like the services themselves; replacing a pipe in the
   basement shouldn't require reinspecting the attic windows. The work should
   decompose into increments that ship independently, since a big-bang cutover
   across several services accumulates integration risk — the phasing is part of
   the design (`phase-split` cuts it later, but the design must make it possible).
10. **Interface completeness.** Endpoints with request and response shapes *and*
    the error contract; data models; integration points; open questions. A design
    missing its error contract is not done.
11. **Altitude.** Blueprint, not construction manual (per
    `technical-design-writing-standards`). Interfaces, decisions with the constraint
    that decided them, and verification evidence belong; line-level implementation
    detail, file-by-file change lists, decision history and lists of rejected
    alternatives don't — they go stale, and an implementer that reads a losing
    option can drift toward it.
12. **Naming and document hygiene.** Descriptive names for services, endpoints and
    concepts — a vague or misleading service name is a finding, not taste, because
    renaming later is expensive enough that it seldom happens. The design should say
    plainly what the thing does and what its main interfaces are. Standard file
    naming and location per the writing standards; assumption and decision IDs cited
    where they constrain the design.

## Phase 5 — Revise the design

Every finding is one of three kinds, and the kind decides what happens to it.

### 1. A gap or an error: fix it

The design is silent, wrong or contradicts itself: a claim verification showed false,
a missing error contract or timeout, an operation that isn't safe to retry, capacity
behavior left to chance, a drift bomb, a data model with no deletion path, a broken
link, a vague name, excess detail. Fix it in the design. These can't flip-flop:
there is no other reading for a later review to swing back to.

### 2. A swap: replace a working choice only for a verified defect

A swap replaces a choice the design made, and that would work, with a different one:
a component, data store, data model shape, interface shape, hosting or workload type.
Make a swap only when you can name one of these defects and have verified it against
the code, infrastructure, provider documentation or requirements:

- **It doesn't work.** It rests on a claim shown false, breaks an acceptance
  criterion, or hits a platform limit checked against the provider's documentation.
- **It departs from the house standards or an established codebase convention**, and
  the design states no requirement that needs the departure. When a requirement does
  need it, the fix is stating that requirement in the design, not a swap.
- **It has a moving part no requirement needs**: a service, table, queue, scheduled
  job, cache or layer whose removal loses no acceptance criterion and no stated
  constraint.
- **It duplicates what exists**: an existing service or a managed capability of the
  platform already does the job.
- **It closes a door that is expensive to reopen**: a data model or public contract
  blocks a plausible next capability from the future-capability probe (Phase 2), and
  a modest change keeps the option open.

The replacement must meet every acceptance criterion and stated constraint the
original met; check that before making it. **A swap is materially better when it
removes a named defect.** "Cleaner", "more elegant", "more common" and "I would have
built it differently" are not defects, however sure you are. A swap that would undo a
choice an earlier run of this review made needs a defect in that choice, verified the
same way.

The bar is a closed list, not a confidence level, on purpose. Whether one working
architecture beats another is judgment, and a confidence figure on a judgment moves
from one run to the next. A defect from the list is a checkable fact, so a second run
reaches the same answer, and a swap can only remove a defect, never trade one
preference for another. The design settles instead of changing each time it is
reviewed.

Carry a swap through every section it touches (interfaces, data models, integration
points, Existing Code, Open Questions), so the design never describes both choices.

### 3. A suspected problem: a question, not a change

A concern you could not verify — a limit that might be reached at volume, a behavior
the code doesn't show — never triggers a swap. When implementation would have to make
a judgment call without the answer, write it in the design's Open Questions as a
factual question: what would have to be true, and what to check.
`autonomous-design-refinement` investigates it and folds in the answer. Otherwise
drop it.

### What it never changes

- **Settled decisions.** A decision the PRD states, or a validated assumption, stands
  even when a swap would remove a defect. The report raises it as a question for the
  user — what was decided, the defect, the simpler way, the evidence ("X was decided,
  but Y would be simpler because Z — worth reopening?") — and the design keeps it.
  When verification shows the facts a decision rested on are false, the report says
  exactly that, and a business decision is reopened under its entry per
  `assumptions-document-writing`.
- **Scope.** The revision never adds a requirement or designs behavior no acceptance
  criterion asks for. A gap in the PRD goes to the design's Open Questions; a
  business uncertainty also goes to the assumptions document per
  `assumptions-document-writing`.
- **The review itself stays out of the design.** The design records each decision as
  it now stands, with the constraint that decided it: no rejected alternatives, no
  comparison, no note that the review changed something. The report and the commit
  carry those (`technical-design-writing-standards`, "Rejected Alternatives").

Edit to `technical-design-writing-standards`: integrate each change into the section
that owns its subject, and keep the design readable in one sitting. **One pass, no
loop.** Make the changes once and stop; repeating passes over a design is
refinement's job.

## Phase 6 — Report and commit

### Commit

Commit the revised design, and the assumptions document or PRD if a change reached
them (a `Replaces:` line, a reopened assumption), as
`docs({feature}): technical design review — {one-line summary of what changed}`, with
the report as the body. This is the default; the user's instructions override it
(`pre-commit-validation`, "Who Commits"), and it never pushes. The commit keeps the
review's changes one diff of their own, after the draft's commit, so a person can see
exactly what the review changed or revert it whole.

**The review always commits.** One that changed nothing, or skipped itself, makes an
empty commit with the same subject (`… — no changes` or `… — skipped, follows an
established pattern`) and the report or the skip line as its body:
`git commit --allow-empty --only -m "<message>"`, which commits nothing else and
leaves another session's staged files staged (`pre-commit-validation`, "Who
Commits"). The commit is how `using-the-enso-method` knows the review ran, and it
keeps the report somewhere durable.

### Voice: shareable, not a private memo

Write the report so it can be handed verbatim to anyone who reads the design: neutral
review voice, never addressing the person who requested it, no references to the
requesting conversation, no private context. Reviewer-only asides, if truly needed,
go in chat — never inside the report.

### Output template

Lead with the verdict, and make it unambiguous.

```
**Verdict:** [1–2 sentences: "Sound as drafted; N fixes made" or "N swaps and M
fixes made," plus anything still conditional (a pending spike, an open question
the build depends on). No hedging.]

**Architecture** — [one-line overall call: "sound — would build it this way" or
"swapped (change 1)"]
- [✅|⚠️|❌] Simplest shape that satisfies the requirements — [independent sketch
  vs. the design; new-moving-parts count, each traced to a requirement]
- [✅|⚠️|❌] Alternatives weighed and beaten — [the strongest alternative and the
  requirement or constraint that kills it]
- [✅|⚠️|❌] Nothing speculative (YAGNI) — [one line]
- [✅|⚠️|❌] Boring / house technology — [what's novel and what requirement paid
  for it; deviations from house standards and the requirement behind each]
- [✅|⚠️|❌] One-way doors identified and best-designed — [one line]
- [✅|⚠️|❌] Data model fits the current ecosystem and can evolve — [source of
  truth and ownership fit, correction and mixed-version behavior, retention and
  deletion, first data-volume ceiling, hardest plausible future capability and its
  exit path]
- [✅|⚠️|❌] First ceiling known, observable, acceptable — [one line]
- [✅|⚠️|❌] Cost and operations proportionate — [one line]

**Changes made** (swaps first)
1. [SWAP] <what changed> (§ref) — defect: <which one, with evidence>. Replaced:
   <the original choice>.
2. [FIX] <what changed> (§ref) — <evidence>
3. [FIX] <smaller fixes grouped in one line>

**Open Questions added:** <each, one line, or none>

**Questions for the user:** <settled decisions worth reopening, each with the
defect, the simpler way and the evidence; or none>

**Sections worth reading personally (~X min total)**
- §A — <why it deserves a person's judgment: a swap, a one-way door, a
  security-sensitive mechanism, an expensive-if-wrong call>

**Held up under verification:** <compact list of the claims checked and found
correct, each with where it was checked — this is what lets a reader skip those
sections>

**Not verified:** <one line on anything load-bearing that couldn't be checked —
never imply whole-document verification if the scope was narrower>
```

### Format rules

- Every change: section reference and evidence; every swap also names its defect and
  what it replaced. A change you can't tie to evidence isn't made.
- Cap it around seven numbered changes; below that, the tail collapses into one
  grouped FIX line.
- Every ⚠️ or ❌ cites a change, an Open Question or a question for the user, or, for
  a lock-in deliberately left in place (Phase 2), states its exit path on the row, so
  nothing needing action lives only in the checklist.
- The read-personally list is what lets a person skip the rest: every swap, then
  the genuinely judgment-laden sections, with a time estimate. When nothing needs a
  person, say so.
- An empty or thin "held up" list means the review isn't done — go back to Phase 3.
- The whole report should fit on roughly one screen.

### A design someone else owns

When the design isn't one this pipeline drafted — it arrived as someone else's pull
request, or the user asked for a review only — don't edit it, and make no commit,
empty or otherwise. Phases 1–4 run the
same; Phase 5 decides what each finding *proposes* instead of what to change, and the
report lists findings with proposed resolutions in place of **Changes made**, each
rated:

- **[BLOCKER]** — building from the design as written would build on something false
  or undefined: a wrong load-bearing claim, an internal contradiction, a missing
  decision implementation would have to invent, or a swap's defect.
- **[SHOULD-FIX]** — a real gap or risk that needs an answer in the design (capacity
  behavior, drift bomb, unhandled failure mode) but doesn't invalidate the
  architecture.
- **[NIT]** — hygiene: broken links, naming, stale sibling documents, excess detail.

On a pull request, post the report as a PR review (`gh pr review --request-changes`
or `--approve`, matching the verdict), then give a few-line summary in chat, not a
second full copy. Otherwise deliver it in chat. Don't write a review file into the
repo: the method's per-PRD documents are the PRD, technical design, assumptions and
phase documents, and a review is input to them, not a fifth.

## What NOT to do

- **Don't review only inside the design's frame.** A review that is all
  contradictions, wrong claims and missing error codes, with no architecture call,
  did half the job. If the changes read like a fact-checker's, Phase 2 didn't
  really run.
- **Don't swap on taste.** A swap needs a verified defect from the list in Phase 5.
  A preference, however confident, changes nothing in the design; at most it is the
  strongest losing alternative in the report.
- **Don't override settled decisions — but don't exempt them from the architecture
  pass either.** A simpler way across a settled decision becomes a question for the
  user in the report, never an edit.
- **Don't write the review into the design.** No rejected alternatives, comparison
  tables, "changed by review" notes or decision history: the design states each
  decision with the constraint that decided it, and the commit keeps the rest.
- **Don't loop.** One pass, one commit, even when the commit is empty (none for a
  design someone else owns). Refinement repeats; the review doesn't.
- **Don't nod along with a polished document.** Confident prose and dense
  verification annotations are not evidence. Spot-check anyway.
- **Don't grade on polish.** The polish is the AI's, and it's free. Praise specific
  verified substance or nothing.
- **Don't substitute reading for verifying.** The value of this review is the claims
  checked against the real repos and infrastructure, not the completeness of the
  read-through.
- **Don't review a data model in isolation.** A plausible schema diagram is not
  evidence of fit. Trace it through the existing source records, storage and index
  conventions, permissions, lifecycle, deletion, mixed-version deploys, correction
  and replay, expected growth, and concrete future-capability probes. Conversely,
  don't call a model "future-proof" because it is generic, and don't build
  abstractions for imagined possibilities; show the plausible capability, the
  lock-in it exposes, and the smallest option-preserving response.
- **Don't bury the read-personally list.** It answers the one question a person
  skimming the report has; keep it near the top of their attention.
- **Don't pad.** A short list of changes that matter beats a long list that hides
  them.

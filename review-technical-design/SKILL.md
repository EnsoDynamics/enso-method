---
name: review-technical-design
description: "Optional senior review of a technical design before refinement — make an independent would-I-build-it-this-way architecture pass, verify the design's load-bearing claims against the real codebase and infrastructure (read-only), test proposed data-model changes against the current ecosystem and future evolution, evaluate the design against the project's house engineering standards, and produce a triage the human can act on without reading the whole document: verdict, ranked findings with proposed resolutions, and the short list of sections worth reading personally. Use after technical-design-writing-standards and before autonomous-requirements-refinement, for designs that make hard-to-reverse decisions (a new service, a schema or data model, a public interface). Treats every design as authored by a junior engineer directing an AI. Not for writing designs, and not for reviewing code or pull requests of code."
user-invocable: true
---

# Review a Technical Design Document

## Where this fits, and when to run it

This step is **optional**. Run it after `technical-design-writing-standards` has
produced a design and before `autonomous-requirements-refinement`, when the design
makes decisions that are expensive to reverse: a new service, a schema or data
model, a public interface. Small designs that follow an established pattern don't
need it.

The order matters. `autonomous-requirements-refinement` fills gaps *inside* the
design's frame and deliberately never asks "would it be better if…". This skill is
the one that questions the frame. Refining a design that the review then
restructures wastes the refinement.

Designs are too long for a senior engineer to read in full, and an AI-assisted
design reads polished and confident whether or not it is right. The deliverable is
a triage: the author gets actionable findings; the human reviewer gets a verdict, a
short list of sections to read personally, and a list of what was already verified
so they can skip it.

## The author model: always a junior engineer directing an AI

Review every design as if it was authored by a junior engineer directing an AI —
today it effectively always was, and a more senior author loses nothing from the
same scrutiny. This changes what the document's surface tells you:

- **The strong parts are real but not diagnostic.** Deep research, assumption IDs
  cited inline, structured decision tables, verification annotations, confident
  prose — AI produces all of that for free. A polished design is the baseline, not
  a signal of sound judgment. Never grade a design "strong for a junior engineer";
  any strength claim must point at specific verified substance.
- **The gaps hide where the human was in charge.** The AI's thoroughness follows
  the author's map of the problem — deep where they knew to ask, silent where they
  lacked the knowledge or foresight to point it. Coverage gaps, not errors, are the
  signature failure; hunt for what the design never considered, not just what it
  got wrong.
- **Feedback flowed one way.** When the AI proposed something, the author took it —
  they lack the basis to push back, so the AI's first reasonable-looking idea
  usually became the design. And nobody in that loop knew the house's opinionated
  technical decisions unless those standards happened to be loaded.

The review fills two gaps:

1. **Verification against reality.** A design is full of factual claims about the
   codebase and infrastructure — "the cookie is named X," "the routing rule is at
   priority Y," "the API already exposes Z." Risk concentrates exactly where those
   claims are wrong, because everything downstream was reasoned from them.
2. **Zoomed-out judgment.** Is this the right approach at all? Is it consistent with
   how the rest of the system is built? Is there prior art — an existing service
   doing something similar — the design should learn from? The author can't ask
   these questions, and their AI didn't have the context.

## Phase 1 — Load context before reading the design

1. Read the parent artifacts first: the PRD, the assumptions document, any
   architecture-options notes. Note which decisions are already **made** (validated
   assumptions with IDs, decisions the PRD or assumptions record). Those are
   settled — the review evaluates the design *given* them and does not relitigate
   them, unless verification undermines the facts a decision rested on.
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
   reliable way to avoid anchoring on the author's frame.
2. **Diff yours against theirs.** Every moving part or layer of generality the
   design has that your sketch doesn't must be pulled in by a requirement or a named
   trade-off — not by momentum, symmetry, or AI enthusiasm. Every part your sketch
   has that theirs lacks is a question to answer.
3. **Name the roads not taken.** A design presenting one architecture with no
   rejected alternatives hasn't done architecture. Check the obvious ones yourself:
   could an existing service absorb this? Does something already running do 80% of
   it? Is there a managed capability of the platform, or an off-the-shelf tool, that
   makes the custom thing unnecessary? What would the dumb version look like, and
   which requirement actually kills it?
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
   - Capture the result compactly as **decision → future capability → lock-in
     mechanism → current accommodation → migration/exit path → verdict**. A material
     one-way door without a credible exit path is a finding and belongs on the
     read-personally list.

   This is option preservation, not permission to gold-plate. Change the present
   design when a plausible capability exposes costly lock-in and a modest boundary,
   stable identifier, provenance field, version marker or separation of concerns
   preserves the option. Otherwise document the constraint and exit path and defer
   the speculative machinery. Also run the near-term thought experiments: source
   data changes after a decision; readers and writers deploy at different times;
   volume exceeds one page or item limit; retention policy changes; a label is
   renamed; a record must be migrated or replayed years later. Prefer derived
   projections over duplicated mutable truth, stable IDs over labels, versioned
   contracts over implicit shapes, and explicit migration paths over claims that a
   schema is "flexible." A locally elegant design is still wrong if it creates an
   orphan data island or blocks the next plausible product evolution.

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

The pass fills the **Architecture** checklist in the triage (Phase 5): one ✅/⚠️/❌
mark per dimension with a one-line justification, so a reader takes in the whole
architectural assessment at a glance. "I wouldn't build it this way" becomes the
lead BLOCKER with your sketch as the proposed resolution. Showing the strongest
losing alternative is mandatory even when the design is right: a row of unexplained
✅s is indistinguishable from not having done the pass.

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
  trade-off** (Fowler/Johnson; Richards & Ford). *Does the design name what it
  traded away? Scrutiny in proportion to irreversibility.*
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
- **Internal consistency.** Designs that evolved over several sessions contradict
  themselves — one section says the new repo owns a resource, the rollout plan
  assigns it to another. Cross-check the decisions against the interfaces,
  integration points and repos touched.
- **Sibling documents.** Grep `docs/prds/` and `docs/changes/` for older PRDs or
  designs covering the same feature. A stale predecessor that contradicts the
  current design must be updated or explicitly superseded — two documents both
  claiming to be current is a defect.
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
   drift bomb — flag it and propose deriving it, colocating it, or guarding it with a
   CI check. Designs whose whole purpose is avoiding drift still sneak these in at
   the edges.
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
   already provides needs an argument. Deviations are allowed but must carry
   explicit rationale in the design; an unexplained deviation is a finding.
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
    `technical-design-writing-standards`). Interfaces, decisions with rationale and
    verification evidence belong; line-level implementation detail and file-by-file
    change lists don't — they go stale before implementation ends. Excess detail is
    a real finding, ranked below correctness.
12. **Naming and document hygiene.** Descriptive names for services, endpoints and
    concepts — a vague or misleading service name is a finding, not taste, because
    renaming later is expensive enough that it seldom happens. The design should say
    plainly what the thing does and what its main interfaces are. Standard file
    naming and location per the writing standards; assumption and decision IDs cited
    where they constrain the design.

## Phase 5 — Deliver the triage

### Where the review goes

The review never modifies the design document and never opens a PR to hold itself.
The human decides what to accept.

- **The design arrived as a pull request** → post the triage as a PR review
  (`gh pr review --request-changes` or `--approve`, matching the verdict), then give
  a few-line summary in chat (verdict and top findings), not a second full copy.
- **The design is a document in the repo, no PR** → deliver the triage in chat, in
  full. Don't write a review file into the repo or annotate the document unless the
  user asks for a file: the method's per-PRD documents are the PRD, technical design,
  assumptions and phase documents, and a review is input to them, not a fifth.

Once the human has ruled, accepted resolutions go into the design per
`technical-design-writing-standards` (business uncertainties into the assumptions
document per `assumptions-document-writing`), and refinement follows.

### Voice: shareable, not a private memo

Write the triage so it can be handed verbatim to the design's author, posted on a
PR, or read by a third engineer: neutral review voice, never addressing the person
who requested it, no references to the requesting conversation, no private context.
The test: the author could receive it unedited and act on every line, and the senior
reviewer reads the same text and knows what to look at. Reviewer-only asides, if
truly needed, go in chat — never inside the triage.

### Severity scale

Three levels, no more:

- **[BLOCKER]** — implementing from the design as written would build on something
  false or undefined: a wrong load-bearing claim, an internal contradiction, a
  missing decision that implementation would have to invent.
- **[SHOULD-FIX]** — a real gap or risk that needs an answer in the design (capacity
  behavior, drift bomb, unhandled failure mode) but doesn't invalidate the
  architecture.
- **[NIT]** — hygiene: broken links, naming, stale sibling documents, excess detail.
  Real, but fix opportunistically.

### Output template

Lead with the verdict, and make it unambiguous: sound to implement, or here are the
changes first. Never "looks good, but also look at X."

```
**Verdict:** [1–2 sentences. "Sound to implement as-is" or "N changes before
implementation," plus anything the verdict is conditioned on (e.g. a pending
spike). No hedging.]

**Architecture** — [one-line overall call: "sound — would build it this way"
or "would not build it this way (finding 1)"]
- [✅|⚠️|❌] Simplest shape that satisfies the requirements — [independent sketch
  vs. the design; new-moving-parts count, each traced to a requirement]
- [✅|⚠️|❌] Alternatives weighed and beaten — [the strongest alternative and the
  requirement that kills it]
- [✅|⚠️|❌] Nothing speculative (YAGNI) — [one line]
- [✅|⚠️|❌] Boring / house technology — [what's novel and what requirement paid
  for it; deviations from house standards and their rationale]
- [✅|⚠️|❌] One-way doors identified and best-designed — [one line]
- [✅|⚠️|❌] Data model fits the current ecosystem and can evolve — [source of
  truth and ownership fit, correction and mixed-version behavior, retention and
  deletion, first data-volume ceiling, hardest plausible future capability and its
  exit path]
- [✅|⚠️|❌] First ceiling known, observable, acceptable — [one line]
- [✅|⚠️|❌] Cost and operations proportionate — [one line]

**Findings** (most severe first)

1. [BLOCKER] <one-line defect> (§ref)
   <Evidence: file:line, or the claim vs. what's actually there. Proposed
   resolution. Confidence.>
2. [SHOULD-FIX] ...
3. [NIT] <one line each; if several, group them under a single item>

**Sections worth reading personally (~X min total)**
- §A — <why this needs the senior call: security-sensitive mechanism, novel
  architectural move, expensive-if-wrong judgment>
- §B — <why>

**Held up under verification:** <compact list of the claims checked and found
correct, each with where it was checked — this is what earns the reader the right
to skip those sections>

**Not verified:** <one line on anything load-bearing that couldn't be checked —
never imply whole-document verification if the scope was narrower>
```

### Format rules

- Every finding: section reference, evidence, a concrete proposed resolution,
  confidence. Without a resolution or a pointed question with your best-guess
  answer, it isn't a finding yet.
- Cap it around seven numbered findings; below that, the tail collapses into one
  grouped NIT item.
- The architecture marks alone convey the assessment; a reader can skip the
  one-liners, but each is written. Every ⚠️ or ❌ cites a finding number, so
  nothing needing action lives only in the checklist.
- The read-personally list is the point of the exercise — it's what lets the
  reviewer skip the rest. Genuinely judgment-laden sections only, with a time
  estimate.
- An empty or thin "held up" list means the review isn't done — go back to Phase 3.
- The whole triage should fit on roughly one screen. A finding the reader has to
  reread is a finding they'll skip.

## What NOT to do

- **Don't review only inside the design's frame.** A triage that is all
  contradictions, wrong claims and missing error codes, with no architecture call,
  did half the job. If the findings read like a fact-checker's, Phase 2 didn't
  really run.
- **Don't relitigate settled decisions — but don't exempt them from the
  architecture pass either.** A decision recorded with its rationale, or a validated
  assumption, is settled as far as the author is concerned. If the architecture pass
  finds a simpler way across it, deliver that as a reopening question for the human
  ("X was decided, but Y would be simpler because Z — worth reopening?"), not as a
  defect charged to the author. Call a decision simply wrong only when Phase 3 shows
  the facts it rested on are false — and say exactly that.
- **Don't nod along with a polished document.** Confident prose and dense
  verification annotations are not evidence. Spot-check anyway.
- **Don't calibrate praise to the author's seniority.** "Impressively thorough for a
  junior engineer" is the tell that you graded on polish — the polish is the AI's,
  and it's free. Praise specific verified substance or nothing.
- **Don't deliver vague concerns.** "The auth section worries me" is not a finding.
  The bar: evidence, proposed resolution, confidence.
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
- **Don't bury the triage.** The reviewer asked which parts to read — answer that
  near the top, not as a footnote after every finding.
- **Don't pad findings to seem thorough.** A short list of things that matter beats
  a long list that hides them.

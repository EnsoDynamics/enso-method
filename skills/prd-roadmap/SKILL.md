---
name: prd-roadmap
description: Cut an idea that is bigger than one PRD — a brief, a context package, a pile of design notes, or a draft PRD that outgrew itself — into an ordered PRD roadmap of right-sized planned PRDs, each one finishing with something that can be promoted to production. Consolidates the input documents (whatever they are called) into one full brief that stays whole, renames and moves it to docs/roadmaps/{name}/, writes beside it the PRD roadmap (the ordered list people read) and the PRD contracts (each PRD's scope, owned contracts and seams, for the sessions that write and design the PRDs), and hands off to prd-writing-standards for the first planned PRD. Decides the cut itself and does not stop to ask. Does not write PRDs, technical designs, or phase documents. The planning step above phase-split. Use when the user says "this is too big for one PRD", "break this into PRDs", "roadmap this", or hands over a large brief to turn into requirements.
user-invocable: true
---

# PRD Roadmap

Take an idea too big for one PRD and cut it into an ordered list of **planned PRDs**, each PRD-sized: not the whole application and not one small thing, but a medium body of work that ends with something finished that can be promoted to production. Write the cut down as a **PRD roadmap** beside the **full brief** it was cut from, then hand off so the first planned PRD gets written with `prd-writing-standards`.

This skill owns three things:

1. **The PRD-sized test** — deciding whether an idea is one PRD or several.
2. **The cut** — finding the seams, ordering the planned PRDs, and writing the roadmap.
3. **The full brief, PRD roadmap and PRD contracts naming and layout** — what the three documents (and the optional coverage matrix) are called, where they live, and how an input with any name becomes the full brief.

**Terminology note:** A planned PRD is a medium body of work, and its phases (`phase-split`) are what agile teams would call stories, sized for one AI session instead of a sprint.

It sits one level above `phase-split` and works the same way: `phase-split` cuts one PRD into session-sized phases and never implements; this skill cuts one idea into PRD-sized pieces and never writes a PRD. **It does not stop to ask whether to cut, or how.** It decides, declares the cut, writes the documents, and hands off. The review point is the handoff: the user reads the roadmap before pasting the prompt that writes the first PRD, and a redirect costs a few minutes of rewriting uncommitted markdown.

---

## Why This Exists

Written as one PRD, a big idea produces a plan of 50 to 100 phases, one technical design that has to decide everything before anything ships (the methodology allows exactly one per PRD), and months of building before anything reaches production. Later pieces of a big idea also depend on things you only learn by shipping the earlier ones, so specifying them in detail up front is guesswork that gets rewritten.

`phase-split` cannot fix this after the fact. It runs on a PRD that is already settled, and it treats reopening a settled PRD as a last resort. The cut has to happen before the PRD is written.

---

## When to Use

- A brief, context package, or set of design notes describes more than one PRD's worth of work, and the user wants to turn it into requirements.
- `prd-writing-standards`' size check tripped, before or during drafting (see "Before You Write: Is This One PRD?" there).
- The user asks to break a large idea into PRDs, or to revise an existing PRD roadmap.

**Do NOT use when:**

- The idea passes the PRD-sized test as a whole. Write one PRD with `prd-writing-standards`, and say so in one line.
- The PRD is settled and implementation has started. Cutting it into phases is `phase-split`'s job; turning it into several PRDs is a scope decision the user makes, not this skill's.
- The work is a bounded change. That is a `docs/changes/` directory (`prd-writing-standards`).

---

## What This Skill Produces

```
docs/roadmaps/{name}/
  {name}-full-brief.md        ← the whole idea: what, why, every settled decision. Never split.
  {name}-prd-roadmap.md       ← for people: the ordered list of planned PRDs — tables and checkpoints, nothing else
  {name}-prd-contracts.md     ← for the sessions that write and design the PRDs: scope entries, owned contracts, question assignments, seams
  {name}-coverage-matrix.md   ← when the input has many discrete items: each one mapped to exactly one planned PRD (Step 4)
docs/prds/{name}-{short-name}/   ← NOT created here; created when that planned PRD is written
```

Worked example: `docs/roadmaps/acme-cloud/acme-cloud-full-brief.md` and `acme-cloud-prd-roadmap.md`, with planned PRDs whose directories will be `docs/prds/acme-cloud-ingestion/`, `docs/prds/acme-cloud-hosted-reporting/`, and so on. (The examples in this skill use that idea to show the formats; they are not a template for how any other idea should be cut.)

Hard rules about the output:

- **The full brief is not split.** There are no per-PRD briefs. The brief holds decisions that apply to every PRD (principles, invariants, privacy rules, data-model direction); splitting it copies them into every piece, where they drift, or orphans them. Scope entries point into it by section heading and never restate it. This is the same rule `phase-split` applies to a PRD.
- **No PRD is written, and no PRD directory is created.** Each planned PRD's scope entry names its future directory; `prd-writing-standards` creates it when that PRD is written. Writing the first PRD is a separate chat, started from this skill's handoff prompt.
- **No target dates, estimates, or owners.** The roadmap sets order, not a schedule; the `in production` stamp is its only date.

### The names

| Name | What it is | Filename |
|---|---|---|
| **Full brief** | The whole idea, consolidated from every input document. Stays whole and governs every PRD cut from it. | `{name}-full-brief.md` |
| **PRD roadmap** | The full brief cut into an ordered list of planned PRDs, written for people: order, priority groups, what each delivers, dependencies, status. | `{name}-prd-roadmap.md` |
| **PRD contracts** | What the PRDs owe each other, written for the sessions that write, refine and design them: each planned PRD's scope until it is written, the contracts each PRD owns, which open questions each settles, and the seams. | `{name}-prd-contracts.md` |
| **Coverage matrix** | Optional: each discrete input item mapped to one planned PRD, deferred, out of scope, or an open question. | `{name}-coverage-matrix.md` |
| **Planned PRD** | One row in the roadmap, with a scope entry in the PRD contracts: a right-sized PRD not yet written. Once written, it is simply a PRD. | becomes `docs/prds/{name}-{short-name}/` |

- **`{name}`** is a short kebab-case name for the thing being built, never for the document type: `acme-cloud`, not `product-brief` or `context-package`.
- **Planned PRDs have names, not numbers.** The order will change as earlier PRDs ship and teach you something, and a numbered id would have to be renumbered. The roadmap's table owns the order. The PRD directory is `{name}-{short-name}`, where short-name is one to three words naming what it delivers (`ingestion`, `hosted-reporting`), so the directories group together in a listing and each reads on its own. In prose and commit messages, when the position matters, write it out: "Cloud Ingestion PRD, first in the Acme Cloud PRD roadmap". Never a bare "PRD 2".
- **Never call a planned PRD a phase, stage, release, milestone, track, or MVP.** "Phase" belongs to `phase-split`; "track" already means something else in these skills (`continuation-prompt`); "release" names the brief's own release labels ("V1", "beta"), which the roadmap maps onto planned PRDs under "Checkpoints"; "MVP" fits only the first.
- **Titles match filenames.** H1s are `# {Title} Full Brief` and `# {Title} PRD Roadmap`, and each document's first line under the H1 links the other, so opening either one says how they relate. The PRD contracts is `# {Title} PRD Contracts` and a coverage matrix is `# {Title} Coverage Matrix`, each with a first line linking the roadmap.

---

## Process

### Step 1: Read Everything

Read every input document in full, then the documents they cite, then, when the idea rebuilds something already running, the live system. Each is handled differently:

- **Inputs** are what the user handed over for this idea: the main brief or notes, and any supplement or amendment written later for it. Supplements matter most. A later document that refines an earlier one ("additional context", "amendments") carries decisions the main document lacks. Inputs are merged into the full brief in Step 3.
- **Cited context** is everything else the inputs point to: a product overview, market research, terminology, the current system's PRD and technical design. Read it for understanding. It stays where it is and is linked from the full brief, never merged into it.
- **The live system**, when the idea rebuilds or changes something already running. A spec describes the target, not what production does today, and it rarely knows the other systems that touch the same records. Read what production actually does (its code on the production branch, not a development branch), and find every other job, service or tool that creates, changes or deletes the records the idea writes. Each live behavior the rebuild replaces, and each other writer, is input to the cut: record it in the full brief (Step 3), where it lands in a planned PRD, a seam, the deferred list, or the open questions. A missed one can force the cut to be redone: the PRD it belongs to turns out to cover a different workflow from the one the spec drew.

### Step 2: Confirm It Is More Than One PRD

Apply the PRD-sized test to the idea as a whole. A **right-sized PRD** passes all of these:

- **It ends in production.** When its last phase lands, something finished can be promoted to production and does something real for someone. That someone may be only the owner using it on real data; it does not have to be a public launch. What fails is an incomplete layer: "the backend", "the data model", "the infrastructure", a prototype nobody runs.
- **Its one technical design fits in a reviewer's head.** The design covers only what this PRD ships, and a reviewer can hold it in one read.
- **`phase-split` would cut it into a moderate number of phases** — see "PRD Size Calibration" below for the current band.

Then decide:

- **The whole idea passes** → it is one PRD. Say so in one line and hand off to `prd-writing-standards` with the input documents. No `docs/roadmaps/` directory, no roadmap.
- **It fails** (typically on the first and third bullets together: many phases before anything is finished) → continue.

If genuinely unsure, cut. A roadmap of two PRDs costs little; one PRD that runs for months before reaching production is the failure this skill exists to prevent.

**When the size band and "ends in production" pull against each other** — the smallest slice that anyone would use is well past the band — fall back in this order, the way `phase-split` falls back from shippable to verifiable:

1. **Look for a thinner outcome first**: one audience, one platform, the happy path, read before write.
2. **Accept a PRD that runs in production on real data even before anything reads it.** Capturing and durably storing the real data in production, with a way to prove it arrived, is a finished thing: it is live, and it stops losing data. That is different from the failure case.
3. **Never accept one that cannot run in production on its own**: a schema, a library nothing deploys, an API nothing calls, infrastructure with no workload.

### Step 3: Consolidate the Input Into the Full Brief

Users name their inputs anything ("Product Brief", "context package", `notes.md`, "additional context"), and often there are several. Produce exactly one full brief. Decide the renames yourself and state them in one line each; do not ask.

1. **Pick `{name}`** per "The names".
2. **Merge several inputs into one.** A supplement's findings go into the sections they amend, not onto the end as an appendix. Where a later document refines an earlier one, the later one wins; where two genuinely conflict and neither says which wins, keep both positions and add the conflict to the brief's open questions. Merging reorganizes; it does not drop decisions. Check at the end that every section of every supplement landed somewhere.
3. **Move and rename** to `docs/roadmaps/{name}/{name}-full-brief.md`, in the repository that will hold the PRDs (for work spanning several repositories, the initiative's primary repository, or a dedicated product or project repository if one exists; see `prd-writing-standards`, "Cross-Repo Initiatives"). Use `git mv` when the file is tracked or staged, so any history follows it. An input that was never committed has no history to keep; a plain move is fine.
4. **Remove the merged-in extras.** `git rm` when tracked. When a source is untracked, move it to the operating system's trash rather than deleting it, so it can be recovered.
5. **Clean up the wording**: set the H1 to `# {Title} Full Brief`; remove handoff language ("context package", "questions Codex should resolve", instructions addressed to one particular agent, a purpose statement that says the document will become "a PRD and a technical design"); and note every section that orders the work or addresses "the PRD" or "the technical design" in the singular, because Step 6 retargets them.
6. **Fix links, in both directions.** Rewrite the moved file's own relative links so they resolve from its new directory. Search the repository for the old filenames and update every inbound link. Add `docs/roadmaps/` to any index of the repository's documentation layout (a README's layout list, for example), which a filename search will not find.

**Changes already staged when the skill starts.** An input often arrives in the same uncommitted change as edits made because of it: an index that now lists it, a feature list that now points at it. Those edits ride in this skill's commit, updated to the new paths, and the commit proposal names them. Changes staged for unrelated work are someone else's: leave them staged and untouched, stage only this skill's files beside them, and limit the commit hand-off to this skill's paths (`pre-commit-validation`).

**When the input is an oversized draft PRD** (the size check in `prd-writing-standards` tripped mid-draft): the draft becomes the full brief. Move it out of `docs/prds/`, and remove its now-empty PRD directory, since it was never one PRD. Its acceptance criteria stay in the brief as source material for the planned PRDs.

### Step 4: Find the Seams

The guiding principle is `phase-split`'s, one level up: **cut vertically.** Every planned PRD cuts through whatever layers it needs (desktop, backend, storage, interface) and finishes with something that can be promoted to production. A PRD that is one layer ("all the infrastructure", "the data model") ships nothing and cannot be judged on its own.

**Where good seams tend to be:**

- **Foundation inside the first PRD — a walking skeleton at PRD scale.** The first planned PRD brings into existence the part of the shared foundation its own outcome needs (typically the core data contracts, the identifiers they carry, and the tenancy boundary they sit inside) by using it for a real outcome, never as a foundation-only PRD. It does not pull in every foundational system the brief names: a user-facing sign-in, for example, arrives with the first PRD that exposes something to sign in to. Later PRDs extend what the first established.
- **Learning points.** Where the brief says, or the situation makes plain, that you will learn from real use or the market what the next piece should be, cut there. Do not specify detail past a learning point.
- **Hard gates.** Some things must be true before an audience can widen: automatic updates before software goes to outside users, account deletion before holding other people's data, authentication before anything is exposed. Put the gate in the PRD before the audience widens, not in a later one.
- **Audience and platform boundaries.** When the brief sequences audiences or platforms (solo users before teams, macOS before Windows), each widening is a natural seam.
- **Earliest real value first.** Order so that the first PRD puts something useful into production soonest. Among equally valid orders, put first the one that de-risks the biggest unknown.

**Rules for the cut:**

- **Every in-scope part of the brief lands in exactly one planned PRD.** What the brief deliberately defers stays in its deferred list and gets no PRD. Cross-cutting decisions (principles, invariants) stay in the brief and govern every PRD; they are not assigned. When the input has many discrete items (the owner's asks line by line, screens, endpoint groups, named tests), prove it rather than assert it: write `{name}-coverage-matrix.md` beside the roadmap, mapping each item to exactly one planned PRD, or to deferred, out of scope, or an open question by its label, with the reason. An item that maps nowhere is a gap in the cut. An item two entries both claim goes to the first planned PRD that needs it; the other lists it under **Depends on**, or in the Seams table when it crosses between them. The matrix proves coverage only, and it is the only coverage document: each PRD's review checks that its rows are covered, without writing a per-PRD trace (`autonomous-prd-refinement`). How many items a planned PRD holds says nothing about its size (see "PRD Size Calibration").
- **Size every planned PRD, not just the idea.** Apply the Step 2 test to each candidate and re-cut until every one passes, in both directions: a planned PRD that fails the band on the high side is two PRDs; one that would split into only a phase or two is too small and merges into a neighbor (or, if it genuinely stands alone and belongs outside this idea, leaves the roadmap to become its own small PRD or change later).
- **The brief's own sequencing is input, not the answer.** Keep its order where it holds, and regroup where its units are layers or too small to reach production on their own. Several of a brief's "phases" often make one PRD.
- **Dependencies point backward.** A planned PRD depends only on PRDs earlier in the order, and a sequential walkthrough (build them one at a time, in order) must read as the natural way to build the thing at every step. The same two checks as `phase-split` Step 3.
- **Say what must come first, and say None in words.** Each entry's **Depends on:** line, and its row's Depends on column in the roadmap, names every earlier PRD, one or more, that must be done before this one can be built, or says `None; can be built at any point in the order.` It is never blank or left out. Once every PRD it names is done (in production), the order is priority, not a constraint: the PRD can be built before, after or alongside any other PRD whose dependencies are done. Whether they are done is checked, not looked up: when the user considers starting a PRD, check its Depends on PRDs against the code and production then. The Status column is a record and can lag.
- **Build the Seams table bottom-up, then compare.** Do not fill the Seams table only from the boundaries the cut drew. List every shared component, every shared backend foundation (stores, permissions, upload, messaging, configuration) and every handoff where one part of the input produces something another consumes, and give each to the first planned PRD that uses it. Every consumer then either ships after its producer or carries an interim rule saying what it does until the producer exists, written in its entry's **Depends on:** line ("None; can be built at any point in the order. Until Hosted Reporting ships, …"). With that rule it does not depend on the later PRD, so dependencies still point backward; the producer, whose switch-over changes the consumer, depends on it. A handoff whose producer ships later and has no interim rule is a dangling seam, and it surfaces mid-build as a blocked PRD. Compare that list with the Seams table: anything on the list the table lacks is a missing row.
- **Plan the far end coarsely.** Entries past the first learning point can be short and broad ("Windows agent", "team features"); they get re-cut when they are reached. Entries up to the first learning point should be specific enough that their PRDs can be written without redoing the cut. The size band applies strictly up to the first learning point and loosely past it: a far-end entry only has to be plausibly one or two PRDs, and it is sized properly when it is reached. An entry before the first learning point is sized now, not left at "plausibly one or two": apply the band and write it as one entry or two. A borderline entry stays one; if its PRD outgrows the band while it is being written, the size check in `prd-writing-standards` sends it back here to be re-cut.
- **Planned-PRD count is an output, not a target.** See "PRD Size Calibration".

### Step 5: Write the PRD Roadmap and the PRD Contracts

Two documents, for two readers. **The PRD roadmap is for people**: the list someone opens to see every PRD in the idea, its priority, what it delivers and where it stands. **The PRD contracts is for sessions**: what a session needs to write a planned PRD, and what a technical design must honor so the PRDs fit together. Keep each to its reader. Per-PRD scope prose and the Seams table in the roadmap make a document no person reads end to end, and the list they came for gets lost in it.

#### The PRD roadmap

`docs/roadmaps/{name}/{name}-prd-roadmap.md`. Tables and checkpoints, nothing else.

```markdown
# {Title} PRD Roadmap

The [{Title} Full Brief]({name}-full-brief.md) cut into right-sized PRDs. Each one ends with something that can be promoted to production. The order is priority: a PRD whose Depends on PRDs are done can be built at any time, and the order may change as each one ships. What the PRDs owe each other: [{Title} PRD Contracts]({name}-prd-contracts.md). [When the roadmap has one:] Item-level coverage: [{Title} Coverage Matrix]({name}-coverage-matrix.md).

## Priority group

[One sentence: who set the priority and what it covers.]

| Order | PRD | Depends on | What reaches production | Status |
|---|---|---|---|---|
| 1 | [Cloud Ingestion]({name}-prd-contracts.md#cloud-ingestion) | None | The desktop agent uploads activity to the cloud and nothing is lost offline; the owner's history is backed up. | planned |
| 2 | [Hosted Reporting]({name}-prd-contracts.md#hosted-reporting) | Cloud Ingestion | ... | planned |

## Later group

[One sentence: why these come later.]

| Order | PRD | Depends on | What reaches production | Status |
|---|---|---|---|---|
| 3 | ... | ... | ... | planned |

## Checkpoints
[Only when the brief has learning points or release labels: where, between which PRDs, the user decides whether the next planned PRD still stands as written. When the brief names releases ("V1", "V1.x", "beta"), map each to the planned PRDs it covers here, e.g. "V1 = Cloud Ingestion through macOS App". One line each.]
```

- **Group headings only when the brief sets tiers** (a stakeholder's "first" list, a release label). Without tiers, one heading, `## PRDs in order`, and one table. Order numbers run through the groups without restarting.
- **The PRD column links the PRD file once it is written**, and the planned PRD's scope entry in the PRD contracts until then.
- **What reaches production** is one plain sentence. **Depends on** names PRDs only; what each provides is in the scope entry, and later in the PRD's own `**Depends on:**` line.

#### The PRD contracts

`docs/roadmaps/{name}/{name}-prd-contracts.md`. It points into the full brief and never restates it.

```markdown
# {Title} PRD Contracts

What the PRDs in the [{Title} PRD Roadmap]({name}-prd-roadmap.md) owe each other: the scope of each PRD not yet written, the contracts each PRD owns, the open questions each settles, and the seams between them. Read by the sessions that write, refine and design these PRDs. Each written PRD is the source of truth for its own scope.

## Cloud Ingestion

**PRD directory, when written:** `docs/prds/acme-cloud-ingestion/`
**Reaches production:** [One or two plain-English sentences: what someone can do or rely on once it ships.]
**In this PRD:** [Bullets naming full-brief sections by heading, and which parts of each.]
**Not in this PRD:** [What a neighbor carries, by the neighbor's name.]
**Depends on:** [Earlier planned PRDs that must be done first, by name, with what each provides, or "None; can be built at any point in the order."]
**Shared contracts it owns:** [Only if any: contracts later PRDs rely on, such as an event schema or device identity. Decided in this PRD's technical design; later PRDs extend them, not redesign them.]
**Questions it answers:** [The full brief's open questions this PRD must settle, by their stable labels (Step 6), e.g. "Q3–Q9, Q26; first answer to Q1 and Q28".]

## [Next planned PRD]
...

## Seams

| Between | What crosses the seam | Owned by | What the later PRD may assume |
|---|---|---|---|
| Cloud Ingestion → Hosted Reporting | Raw event schema and storage layout | Cloud Ingestion | Raw events are stored, deduplicated, and attributed to a device. |
```

The first five lines of an entry (directory through Depends on) are its **scope lines**: they exist so the PRD can be written, and they go once it is (Keeping the Roadmap Current). **Shared contracts it owns** and **Questions it answers** stay for the life of the roadmap: the technical designs of later PRDs read them, and no PRD carries them.

**Questions that span PRDs.** An open question that several PRDs extend (overall infrastructure layout, observability, the testing approach) is assigned to the first PRD that must answer it; later entries list it as "extends Q1". This is the same pattern as shared contracts.

**Status** takes three values: `planned`, `PRD written` (with a link to the PRD file), and `in production YYYY-MM-DD`.

**Leave out the fluff.** No background or motivation (the brief's job), no restated brief content, no target dates or estimates, no narrative defending the cut (that was the declaration in the response). An entry runs about 6 to 15 lines. The first planned PRD, which owns most of the foundation, can run to about 25. Past that, the entry is restating the brief. The same cap holds while the PRDs are written and refined: a session that adds detail to an entry instead of to its PRD is restating the PRD. Checkpoints stay one line each, a decision a person makes and when: the history of a re-cut lives in version control, and what the PRDs owe each other lives in the PRD contracts.

**A roadmap written before the two were separate** has its scope entries and Seams table inline. It still works; when it is next revised, move the entries and the Seams table into a PRD contracts document, drop the scope lines of PRDs already written, and point the PRDs' `**Roadmap:**` lines at the roadmap file.

### Step 6: Update the Full Brief So the Two Never Disagree

- **Add the link line** under its H1: `Cut into PRDs by the [{Title} PRD Roadmap]({name}-prd-roadmap.md).`
- **Replace its ordered plan with a pointer.** A section like "Recommended phases" or "Milestones" becomes one line pointing at the roadmap, which now owns the order. Keep any decision that section held — a gate, a constraint, an "X before Y because Z" — as a decision in the brief; only the sequencing moves.
- **Keep its open-questions list, with stable labels.** The PRD contracts assigns each question to a planned PRD; the brief stays the one list. If the questions have no labels, give them `Q1`, `Q2`, … in their current order. Labels are assigned once and never renumbered: a question that gets answered or dropped keeps its label, the way PRD acceptance-criterion labels work (`prd-writing-standards`).
- **Retarget guidance written for one PRD and one design.** A brief written as input to a single PRD often has sections such as "Guidance for the PRD", "Guidance for the technical design", or "Questions the PRD and technical design must resolve". Left as written, they tell the first PRD's author to cover everything, which is the failure this skill exists to prevent. Retitle and reword them so they apply to each PRD cut from this brief, within the scope of its entry in the PRD contracts. Do this with a heading change and one sentence at the top of each section, not a rewrite of its contents.
- **Remove the word "phase"** wherever it named the brief's own ordered units, so the word stays reserved for `phase-split`.

After this, the brief changes only when a decision changes. If a PRD later overturns a brief decision on purpose, the brief is amended at that point (`implementation-lifecycle`, documents before code).

### Step 7: Declare and Hand Off

State the cut in the response as a decision: a table of order, planned PRD, what reaches production, and one line on why the cut falls there. Then list the renames and removals from Step 3. Do not end the turn to ask whether the cut is acceptable.

Stage the documents (brief, roadmap, PRD contracts, and the coverage matrix when there is one) and validate per `pre-commit-validation`; commit and push only under live user authorization, otherwise present the commit message for approval.

Then give the copy-paste prompt for writing the first planned PRD, using `continuation-prompt`. Its chat name takes the planned PRD's short-name as the unit and the roadmap's name as the project tag, and its lineage block names the roadmap and the planned PRD:

```
ingestion acmeCloud prd

In service of: Acme Cloud PRD Roadmap
  Cloud Ingestion — planned PRD, first in the roadmap
  This chat: writes and refines its PRD.
```

The prompt names `prd-writing-standards` and `autonomous-prd-refinement`, points at the planned PRD's entry in the PRD contracts, its rows in the coverage matrix when there is one, and the full brief, and says the PRD's directory. The prompt is valid once the roadmap commit lands. The chat it starts writes the PRD (and mockups, if the product needs them) and refines it with `autonomous-prd-refinement`; the user's review, the technical design (reviewed with `review-technical-design` when it makes hard-to-reverse decisions), design refinement, phase split, and build follow in the usual chain.

---

## Keeping the Roadmap Current

- **When a planned PRD is written**, the chat writing it sets the roadmap row to `PRD written` and points the row's link at the PRD file (`prd-writing-standards` carries this rule). **When its refinement finishes**, the same chat deletes the entry's scope lines from the PRD contracts, keeping **Shared contracts it owns** and **Questions it answers** (`autonomous-prd-refinement`, Completion). The PRD now holds its own scope; a second copy would only drift.
- **When a PRD's work reaches production**, its row becomes `in production YYYY-MM-DD`: set by the session that promoted it, or named as the user's one-line action when promotion happens outside a session (`implement-from-requirements` wrap-up).
- **The next planned PRD is the user's decision**, not an automatic continuation. When a PRD's last phase closes, the wrap-up says the PRD is complete and names the roadmap's next planned PRD; it does not write that chat's prompt unless asked (`continuation-prompt`, "A PRD roadmap is not a track").
- **Reordering, adding, or dropping a planned PRD is the user's call**, applied by re-running this skill to revise the roadmap, the PRD contracts and the coverage matrix, when there is one. Names never change on a reorder. A reorder keeps every PRD after the PRDs it depends on; moving one ahead of one it depends on is a re-cut. Discoveries made while building never become planned PRDs on their own (the Materiality Gate in `implementation-lifecycle`); only the user adds one.
- **A written PRD that moves scope to or from a neighbor** updates both PRDs (or the neighbor's scope entry, while it is planned), their contract and seam lines, and the coverage matrix when there is one, in the same change.
- **Re-cutting a far-end entry** when it is reached is normal. It becomes two or three specific planned PRDs in its place, keeping the rest of the order.

---

## PRD Size Calibration

This section holds the concrete numbers, the only part of this skill that ages. Revise it, and nothing else, when experience shows the band is off. Phase size itself is defined in `phase-split`'s "Session Capacity Calibration"; this band is counted in those phases.

- **A right-sized planned PRD splits into roughly 3 to 10 phases.** Past about 12, it is two PRDs. Inside a roadmap, an entry that would be only one or two phases usually merges into a neighbor. Outside a roadmap, small PRDs are normal: `phase-split` expects many PRDs to be two to four phases or not split at all. This band is for cutting a big idea, not a minimum for every PRD.
- **A typical PRD roadmap has 3 to 6 planned PRDs.** A genuinely large idea can produce more. The red flags are PRDs that fail the band, not the count.

---

## Rules and Constraints

### DO

- Read every input, supplements especially, and the live system when the idea rebuilds one, before deciding anything.
- Build the Seams table bottom-up from shared components, foundations and handoffs; give each to the first PRD that uses it.
- Test the idea as a whole first; when it is one PRD, say so and hand off without creating a roadmap.
- Consolidate every input into one full brief, named for the thing being built, at `docs/roadmaps/{name}/{name}-full-brief.md`, with `git mv` for tracked files and the trash for untracked extras.
- Cut vertically: every planned PRD ends with something finished that can be promoted to production.
- Put the shared foundation inside the first PRD, cut at learning points and hard gates, and order for the earliest real value.
- Size every planned PRD against the calibration band and re-cut until all pass.
- Name planned PRDs, never number them; name their future directories `{name}-{short-name}`.
- Keep the full brief whole; point into it by section heading; replace its ordered plan with a pointer to the roadmap.
- Declare the cut, write the roadmap and the PRD contracts (and the coverage matrix when the input calls for one), and hand off with a prompt for writing the first planned PRD.

### DO NOT

- Write a PRD, technical design, mockups, or phase documents, or create a PRD directory.
- Split the full brief, or write a brief per planned PRD.
- Make a planned PRD out of one layer (infrastructure, data model, backend) that reaches production only when a later PRD arrives.
- Stop to ask whether to cut, or which cut to use.
- Call planned PRDs phases, stages, releases, milestones, tracks, or MVPs, or refer to one by a bare number.
- Put target dates, estimates, or owners in the roadmap.
- Put scope prose, contract lists or the Seams table in the roadmap; they belong in the PRD contracts.
- Turn discoveries into planned PRDs; only the user adds one.

---

## Relationship to Other Skills

| Skill | How This Skill Relates |
|-------|-------------------------|
| `prd-writing-standards` | Downstream consumer. Writes each planned PRD from its entry in the PRD contracts and the full brief, sets the roadmap row to `PRD written`, and documents the `docs/roadmaps/` root alongside `docs/prds/` and `docs/changes/` (this skill owns that root's internal layout). Its size check sends oversized ideas and drafts here. |
| `phase-split` | The same job one level down: it cuts one PRD into session-sized phases. Its seam principles (vertical slices, walking skeleton, backward dependencies, sequential walkthrough) are reused here at PRD scale, and its Session Capacity Calibration defines the phase size this skill's band counts in. |
| `technical-design-writing-standards` | Each planned PRD gets its own single technical design. A design honors the full brief's settled decisions and the seams in the PRD contracts: it decides the shared contracts its PRD owns and extends, never redesigns, contracts an earlier PRD owns. |
| `implementation-lifecycle` | Lists writing a planned PRD as requirements work with its own lineage, and supplies the Materiality Gate that keeps discoveries from becoming planned PRDs. |
| `implement-from-requirements` | When it closes a roadmap PRD's last phase, its wrap-up names the next planned PRD (no prompt) and handles the `in production` status. |
| `continuation-prompt` | Produces the handoff prompt for writing the first planned PRD. At the end of a PRD, treats the roadmap's next planned PRD as the user's decision, not the next unit of the finished track. |
| `pre-commit-validation` | Validates the staged documents before any commit. |

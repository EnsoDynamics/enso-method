---
name: prd-writing-standards
description: Write or check a PRD (Product Requirements Document), the requirements a technical design is then built from. Skimmable — clear business context and testable outcomes without implementation details, invented responsibilities, or step-by-step instructions. Use when the user describes something to build and no PRD exists yet, or to bring an existing PRD up to this standard.
user-invocable: true
---

# PRD Writing Standards

Guidelines for writing PRDs.

---

## What Is a PRD?

A PRD (Product Requirements Document) is a high-level description of a product change or capability we're delivering. It answers the questions **"What are we delivering?"** and **"Why are we doing it?"** in plain business language.

A PRD should be understandable by product managers, stakeholders, and anyone who needs to know what we're delivering without diving into technical details.

---

## Before You Write: Is This One PRD?

A PRD in `docs/prds/` is a medium body of work that ends with something finished that can be promoted to production. It is not the whole application; a bounded change in `docs/changes/` uses the same document set and can be as small as one fix (see "Document Storage Convention"). Before drafting, check the source material against the PRD-sized test in `initiative-breakdown` (Step 2). The usual sign it fails: the work would take many phases before anything finished reaches production, or it bundles several outcomes that could each ship on their own. When it fails, run `initiative-breakdown` first. It cuts the idea into planned PRDs, and this skill then writes each of them. The same holds when a draft outgrows the test partway through writing: stop, and hand the draft to `initiative-breakdown` as its input. A planned PRD that fails the test, before or during drafting, goes back to its own initiative to be re-cut there (`initiative-breakdown`, "Re-cutting a planned PRD"), never into a new one.

**Raw source material goes through `requirements-intake` first.** When what was handed over is meeting transcripts, long threads, earlier AI sessions, a prior attempt's documents or a large mixed pile, rather than a brief or an email or two, run `requirements-intake` before drafting, and write the PRD from its record (`source-material/{name}/{name}-requirements-intake.md`), which the PRD then neither links nor names ("Document Storage Convention"). Write the criteria in the PRD's own plain words, using the stakeholders' name for each thing (defined at first use), and use a stakeholder's example only where it is the clearest statement of a rule. The quotes stay in the record; criteria carry no quotes or per-criterion citations.

**Writing a planned PRD from an initiative.** When the PRD is a planned PRD in an initiative (`docs/initiatives/{name}/{name}-initiative-prds.md`), its scope comes from its entry in the PRD contracts beside it (`{name}-prd-contracts.md`, and its rows in the coverage matrix beside it, when the initiative has one), and its decisions come from the initiative brief beside it. Every one of those matrix rows ends up covered by a criterion, declared as an assumption where the PRD departs from it, or moved to a neighbor with both entries in the PRD contracts and the matrix updated; the PRD's review checks this (`autonomous-prd-refinement`'s full rounds, or the one `deliverable-review` round a small PRD gets). The check leaves no document behind: the matrix's row-to-PRD mapping is the lasting record, so the PRD carries no coverage-trace section and gets no trace file beside it. The PRD's directory is `{name}-` followed by its title in kebab case (`initiative-breakdown`, "Planned PRDs have names, not numbers"), normally the directory the entry gives. When it is not, because the entry's directory was shortened or the title changes before the PRD is split into phases, name the directory and its `{dir}-prd.md` file after the title, and change the PRD's name and directory wherever the initiative's documents give them (the PRD list, the PRD contracts and the coverage matrix, other entries' and written PRDs' Depends on lines included), in the change that sets the title, before anything outside the initiative links to it. Put an `**Initiative:**` line under the H1 linking the PRD list file, and under it a `**Depends on:**` line that agrees with the entry's, never left out (`None; can be built at any point in the order.` when it depends on nothing); the same review that checks the matrix rows checks it against the entry. In the same change, set the PRD's PRD-list row to `PRD written` and point the row's link at the PRD file. The entry's scope lines stay until the PRD's refinement finishes (`autonomous-prd-refinement`, Completion), and its contract and question lines stay for good (`initiative-breakdown`, Step 5). Detail the PRD needs goes in the PRD, never back into the entry.

**Writing a follow-on.** A follow-on that `assumptions-document-feedback` created for a stakeholder's new asks takes its scope from its PRD contracts entry when it is in an initiative (written as above), or from `{name}-follow-on-scope.md` in its change directory, and its requirements from the stakeholder's saved feedback, and any mockups they supplied, that the scope points at. Every ask the scope lists ends up covered by a criterion, or declared as an assumption where the PRD departs from it. Put a `**Follow-on to:**` line under the H1 naming the PRD it follows, which is how later feedback on that PRD finds its open follow-on. Each criterion its **Changes:** line names gets a `Replaces:` line ("When Later Work Changes an Earlier Criterion"). Delete the scope file in the commit that writes the PRD; the PRD now holds the scope. Once its refinement finishes, make its stakeholder review package straight away (`stakeholder-review-package`), before the technical design: the stakeholder asked for this work, so their check on how it will look and behave comes first. A change PRD that `implement-from-discovery` writes (its Phase 4) is written the same way, from that chat's findings rather than saved feedback, with a `**Follow-on to:**` line only when an existing PRD owned the behavior it changes, and no early review package.

---

## What Belongs in a PRD

### Summary and Business Context
The opening of a PRD establishes **what** we're building and **why**. Use an unnumbered `## Summary` for the plain-English product description. When the business context needs more than a sentence or two, follow it with a separate unnumbered `## Business Context` explaining the problem, why it matters, and why this product is worth building. If the "why" is straightforward, keep it in the Summary instead of creating a thin extra section.

Do not number PRD sections by default. A heading's wording should tell the reader what it contains; its position is not its identity.

Bad: "Implement a returns-eligibility endpoint with order-line filtering"
Good: "Tell customers which purchases they can return and explain why an item is not eligible"

### Acceptance Criteria
This is the most important part of the PRD. Each criterion should be a clear yes/no checkpoint—you should be able to inspect the delivered result or its evidence and confidently answer "did we meet this?" without ambiguity.

For anything beyond a very small PRD, group the requirements beneath one unnumbered `## Acceptance Criteria` heading. Within it, use unnumbered `###` theme headings that state the product outcome in easy, ordinary language. Use the human-readable skim-layer guidance below for every theme. A reader who scans only the headings and introductions should understand the product without translating abstract or technical language.

Good acceptance criteria:
- "Customer can see which purchased items are eligible for return"
- "An ineligible item displays the reason it cannot be returned"
- "Customer can submit a return for one or more eligible items"
- "Customer sees the expected refund method before confirming the return"

Bad acceptance criteria:
- "The page should be fast" (how fast? what's the threshold?)
- "Users can easily find what they need" (what does "easily" mean?)
- "The export should work well" (work well how?)

Precise is not the same as readable. See "Plain English for Readers Outside the Project" below for how the criteria and the sections around them get written so someone who wasn't part of the project can follow them.

### Keep Criteria Readable as Cases Are Added
A person signs a PRD off by reading it, and an agent builds from it. Write it as detailed as the build needs and no more, and keep it that way as review rounds add cases. A criterion that grows a clause for every case a reviewer raises ends up checked by nobody and misread by everyone, agents included.

- **First ask whether a stated rule already settles the case.** If applying a rule the PRD already states answers it, the case needs no words of its own; at most, sharpen the rule's wording so the answer is plain. The technical design applies the rule to each place it touches.
- **Restate; don't append.** When a criterion must change to cover a case, rewrite it as one statement of the rule. A criterion that has grown "unless", "except when" and "including those" one round at a time is due a rewrite.
- **A rule with many cases gets a table.** When a behavior genuinely differs by case, keep the criterion to the rule in a sentence and put the cases in a short table beneath it, one row per case. A reviewer checks a row at a glance, and a test covers one row at a time.
- **State each rule once.** Other criteria, notes and mockups name it by label rather than restate it. A restated rule drifts, and every copy is one more thing a fix has to find.
- **Keep context out of the criterion.** A criterion says what must be true. When it deliberately changes how things work today, one short closing sentence may say so, so a builder does not keep the old behavior; evidence and history go in the Business Context or in the assumption that records the decision.
- **Tripwire, not a limit:** a criterion that no longer reads as one short paragraph, or that a reader has to read twice to find what is being checked, is due a split or a table.

```markdown
- [ ] **AC-REFUND-04 — Each returned item is refunded by its condition.** When a return arrives, each item is refunded as the table says, and the customer sees which row applied.

  | Condition on arrival | Refund |
  |---|---|
  | Unopened | Full price, to the original payment method |
  | Opened, undamaged | Full price, as store credit |
  | Damaged by the customer | None; the item is sent back at no charge |
```

### Stable Acceptance-Criterion Labels
When other documents (plans, technical designs, phase docs, status updates) will point back into a PRD, references must survive the PRD being edited and reordered. Section numbers and paragraph positions shift when content moves, so they are poor references.

For a PRD that will be referenced downstream, give every acceptance criterion a stable `AC-<AREA>-<NN>` identifier. `<AREA>` is a short uppercase code grouping related criteria, and `<NN>` is a two-digit sequence within that area. Numbers are assigned once and never reused or renumbered—if a criterion is dropped, retire its number rather than shifting the ones below it, and new criteria take the next free number even if that leaves them out of reading order. The criterion label is the stable handle; theme headings stay clean, descriptive, and unnumbered rather than carrying section numbers or parenthetical namespace tags.

```markdown
### Tell Customers Which Items They Can Return

Customers should know whether an item can be returned before they spend time starting the process. When an item is not eligible, they should understand why.

- [ ] **AC-RETURNS-01 — Eligible items are clear.** Customers can see which purchased items are still eligible for return.
- [ ] **AC-RETURNS-02 — Ineligible items are explained.** When an item cannot be returned, customers can see the reason.
```

Other documents then cite `AC-RETURNS-02`, not "the second bullet in the returns section." Within a labeled PRD, label every criterion consistently. A very small standalone PRD may omit labels when nothing downstream will cite individual criteria.

(The short bold phrase after each label—"Eligible items are clear"—is the criterion's plain-language title. See "Plain English for Readers Outside the Project" below for what makes a good one.)

### When Later Work Changes an Earlier Criterion
A later PRD or change directory often changes behavior an earlier one defined: a longer return window, a status that now means something else, a step that no longer happens. The earlier PRD is not rewritten to match. It was true when it was built, and the later document now owns that behavior: **the latest-built document that defines a behavior is its source of truth** (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"). Two lines connect them:

- **On the new criterion, written with the PRD:** a `Replaces:` line naming each earlier criterion it changes. It is part of the new PRD's content and changes freely while the PRD is drafted and refined. While writing, add one only where you already know the earlier criterion; don't search the repo for them, because the conflict check does that during design refinement or at build.
- **On the earlier criterion, written when the new one is built:** a `Superseded by:` line naming the new criterion, in the same commit as the code that makes it true. Not before: a PRD that is never built, or waits months, must not mark behavior superseded while the code still does it.

```markdown
- [ ] **AC-WINDOW-01 — Returns accepted for 60 days.** Customers can start a return up to 60 days after delivery.
  - Replaces: AC-RETURNS-03 in `docs/prds/customer-returns/customer-returns-prd.md`

- [ ] **AC-RETURNS-03 — Returns accepted for 30 days.** Customers can start a return up to 30 days after delivery.
  - Superseded by: AC-WINDOW-01 in `docs/changes/longer-return-window/longer-return-window-prd.md`
```

The rules that keep the lines trustworthy:

- **Name the path with the label.** A label is unique only inside its own PRD. An unlabeled criterion is named by its bold title.
- **Say when only part changed,** on both lines: `Replaces in part: … (the return window only)` on the new criterion, `Superseded in part by: … (the return window only)` on the earlier one. The rest of the earlier criterion stays in force, and that criterion still owns it: an amendment to that part edits it in place.
- **"Later" means built later.** If a criterion is superseded before it is built (a later PRD shipped first), the build of its own PRD skips it, or builds only the part still in force.
- **Point to the next document, never the latest.** When a third PRD changes the behavior again, it replaces the second PRD's criterion, and only that criterion gets a new `Superseded by:` line. Earlier pointers are never rewritten: a reader follows the chain to its end, and the chain is the history. One criterion replaced by two, or one new criterion replacing parts of two, is a line naming both.
- **Removing a behavior is a criterion too.** "Customers no longer receive the weekly digest" replaces the criterion that added it.
- **Never edit a fully superseded criterion's text.** An amendment goes to the end of the chain, the criterion that owns the behavior now.
- **These lines are not decision history.** Conformance and cleanup passes keep them.
- **Moving a directory** (a change that grew into a program) updates every path in these lines that points into it.

Nobody is expected to remember every earlier PRD. The conflict check (`implementation-lifecycle`) finds the earlier criteria a new PRD changes, and turns each into a `Replaces:` line or a question.

### Out of Scope and Other Optional Sections
State what is explicitly excluded when doing so prevents genuine boundary confusion. Other sections—such as future considerations, dependencies, or readiness—are optional and should appear only when they help readers understand or decide the product requirements.

Do not add sections as boilerplate, repeat the Summary or acceptance criteria in a closing recap, or place technical design decisions in the PRD.

### State the Outcome Without Inventing the Method
A PRD can define the required product outcome even when the technical design has not chosen how to achieve it. Do not hide an undecided implementation method inside a file format, integration, or responsibility assigned to a particular actor.

- State what information, capability, or result the product must have.
- Name a user, system, partner, or other actor as responsible only when that responsibility is an intentional product decision or an established external constraint.
- Keep the method open when several approaches could satisfy the same product need and the choice does not change the user-facing outcome.
- Surface an unknown that could make the outcome infeasible or materially change scope, risk, cost, or the user experience — as an assumption entry (`assumptions-document-writing`) when it is a business question below 95% confidence, or in the technical design's Open Questions when it is technical ("Every Decision Is Written Up or Declared" below). The PRD-writing task should surface that question; it does not need to perform a technical investigation that belongs elsewhere.

An explicitly chosen manual step can be a valid requirement. The problem is not user involvement; it is turning the first implementation idea into a user obligation without deciding that the manual step is part of the product.

Bad: "The user supplies a CSV containing all contacts." This unnecessarily chooses both the actor and the file format.

Good: "The system can access a contact list containing each person's name, company, role, and profile link." This states what the product needs while leaving the acquisition method open.

### Every Decision Is Written Up or Declared
Writing a PRD settles questions its source material leaves open: which case a rule covers, who does a step, what a fee is, which system a change lands in. Each is settled by the 95% rule (`implementation-lifecycle`, "Confidence Thresholds"):

- **95% or more, from the material the PRD is written from** (its sources, records checked, a rule the PRD already states): write it into the PRD as its requirement and move on. It is not an assumption, and it is not listed anywhere as a question that was settled. A PRD has no "settled questions" section.
- **Below 95%, and a business decision:** it is an assumption. Declare it in the PRD's `assumptions.md`: load `assumptions-document-writing`, run its Four Gates for the entry, and cite the entry's ID where the PRD states the decision. Below 95% and technical, it goes to the technical design's Open Questions.

This holds for every decision, however it arose: while drafting, as a review fix, or as a ruling handed to a writer during refinement. Before handing a PRD over, walk its decisions once: each is either settled from the material at 95% or more and written up, or carries an assumption ID.

### Mockups Show What the Criteria Require
A PRD's mockups show what its criteria require, state by state, so a reader never has to reconcile the drawing with the text.

- **Draw every screen the criteria change.** A PRD whose criteria change what a screen shows or how it flows has a mockup of each changed state; one that changes no screen needs none. Start from a mockup the stakeholder supplied, copied into the PRD's `mockups/` directory and revised there as the PRD is written and refined, while the original stays as received (next point). Without one, start from the latest drawing of that screen (this PRD's mockup, or an earlier PRD's for a screen not built yet), else from the screen as it is built now, and draw the change into it. A new screen is drawn from its criteria.
- **Correct the drawing; never annotate it.** When a criterion changes, or the work establishes a fact a mockup contradicts, redraw every affected state in the same change. A note saying what a mockup gets wrong leaves two specifications, and a builder may follow the wrong one. The one exception is material from a handoff package. Nothing in a handoff is edited: the whole package stays as received, in its own location named for where it came from and when (such as `source-material/{source}-handoff-{date}/`), never inside the PRD's directory, so nobody mistakes it for the PRD's requirements. The PRD's own mockups and text say where they depart from it.
- **Keep each state's note short.** A note says what the state shows and which criteria it covers. It does not restate rules, which live in the criteria, or explain how the states link to each other: links between states are a convenience for stepping through, not part of what is specified.
- **Draw from the facts.** Sample data comes from real records where the project allows reading them. A state that shows something other than what the first release is expected to do, such as an optional integration already in place, says which scenario it draws.
- **Regenerate a mockup in its own medium.**
  - *Code, the usual case for screens* (HTML, SVG, a page generated from data): edit the source or its generator and render it again. Any agent can, and code keeps exact text such as record numbers identical across states, diffs cleanly, and can be measured by script (`deliverable-review`, "Look at Visual Deliverables").
  - *A mockup that exists only as an image* (a raster concept, a stakeholder's picture): regenerate it with an image-generation tool, then copy the result into the PRD's `mockups/` directory. Claude Code has none of its own. When the Codex CLI is installed and signed in, `codex exec "<prompt>"` uses Codex's built-in image generation under the user's ChatGPT sign-in, with no API key, and saves the image under `~/.codex/generated_images/`.
  - *No image tool, or it fails:* rebuild the mockup as HTML or SVG and render it to an image. That version can then be corrected and checked like any other. If even that is impossible, the wrong mockup is an open finding that keeps the work from being done, never a note.

---

## What Does NOT Belong in a PRD

### Implementation Details
Technical subject matter is not automatically an implementation detail. The items below are excluded when they describe internal construction choices rather than a product behavior or constraint:

- Specific file names, class names, or function names
- Code modifications or code snippets
- Database queries or API payloads
- "Reuse X function from Y file with these tweaks"

### Step-by-Step Instructions
The PRD describes outcomes, not the path to get there. Don't tell developers how to build it.

### Time Estimates
PRDs are about what we're building, not scheduling. Time estimates belong in sprint planning.

### Boilerplate Requirements
Do not add boilerplate such as "follow security best practices" or "test thoroughly." Do include security, privacy, accessibility, performance, compliance, auditability, or operational outcomes when they materially define the product, protect a user, or affect a stakeholder decision—even when good teams commonly consider them. State the observable outcome rather than prescribing an engineering practice.

### Fluff
If it doesn't help someone understand what we're building and why, leave it out.

---

## The PRD–Technical Design Boundary

A PRD defines **what** must be delivered, **why** it matters, and the observable outcomes or constraints the result must satisfy. A technical design usually follows it and decides **how** the system will satisfy that contract: architecture, interfaces, data models, integrations, and other technical choices.

Technical language belongs in a PRD when it is part of the product contract. For a developer tool, supported operating systems, accepted input standards, command behavior, compatibility promises, and user-visible error behavior may all be product requirements. The PRD should not choose libraries, internal code structure, storage technology, hosting, or algorithms unless a specific choice is itself an intentional requirement or an established constraint.

Use this test: **Could meaningfully different technical approaches satisfy the same requirement?** If yes, state their shared outcome in the PRD and choose among them in the technical design. If a particular technical choice changes the promised behavior, compatibility, compliance, cost boundary, or user experience, it may belong in the PRD—along with the reason it matters.

The technical design should show how the proposed design satisfies the PRD's acceptance criteria, but not every internal technical decision needs its own PRD criterion. Individual design choices should cite the requirement, existing-system constraint, engineering standard, or technical rationale that actually drives them. If technical investigation shows that a requirement is infeasible or needs a materially different product outcome, surface that as a product decision rather than silently rewriting the requirement in the design.

---

## Plain English for Readers Outside the Project

A PRD gets read by people who weren't in the room: a stakeholder, a developer joining next month, the AI that implements it six weeks from now. Criteria written in the project's own shorthand are opaque to all of them, and an opaque requirement gets skimmed and then misbuilt. This is not a precision-versus-readability tradeoff — the criteria stay exact, and the framing around them does the explaining.

**The skim test:** a smart reader who was not part of the project should be able to read only the Summary, Business Context, requirement-theme headings, and their introductions and accurately explain what is being built and why. If they would need the criteria to discover the basic product shape—or would have to translate or guess at the framing—rewrite it.

### Open every acceptance-criteria theme with 1-2 plain-English sentences

Before the first criterion in each theme, say what that theme delivers and why it matters. The heading and introduction should be the easiest part of the section to read; they are not a compressed technical summary of the criteria below.

Use concrete actors, actions, and outcomes, along with common words and short sentences. Avoid noun piles, abstract process labels, unexplained jargon, and technically precise wording that a human has to decode. The criteria remain exact; the heading and introduction make their meaning immediately understandable.

Bad heading: "Disposition Eligibility Determination"

Good heading: "Tell Customers Which Items They Can Return"

**Example** — the intro is the prose between the heading and the first criterion:

```markdown
### Make Approval Decisions Clear

Employees need to know who is reviewing a purchase request and what is holding
it up. Approvers need the information required to make a decision without
chasing the requester for basic details.

- [ ] **AC-APPROVAL-01 — The current approver is visible.** ...
```

### Give each criterion a plain-language title

This rule is about the **title** — the short bold phrase that leads a criterion — not about the label. A labeled criterion has three parts:

```markdown
- [ ] **AC-APPROVAL-01 — The current approver is visible.** Employees can see who is responsible for the next decision on their request.
```

- `AC-APPROVAL-01` is the **stable label** (see Stable Acceptance-Criterion Labels above). Its `APPROVAL` portion groups related criteria—a terse handle nobody reads as prose, so terseness is fine there.
- `The current approver is visible` is the **title**, and it is the only part this rule governs.
- The rest is the **criterion text** — the exact, testable statement.

The title is the line a reader scans to decide whether this criterion matters to them, so it states the claim in ordinary words rather than in the project's term of art:

| Term of art | Plain claim |
|---|---|
| **Return eligibility determination** | **Customers can see what they can return** |
| **Approval provenance** | **Every decision shows who made it and when** |
| **Idempotent submission** | **Submitting twice does not create duplicates** |

If a term of art really is the right title, the first sentence of the criterion text defines the term.

### Define project-specific terms at first use

Any term this project invented or repurposed — a "seam," a "spine," "closure," "quarantine" — gets a one-clause plain definition the first time it appears in the document. After that, use it freely.

> The "ingest window" is the time range a single import run covers — every source record timestamped between its start and end.

### Name the actors and the direction

A heading or sentence describing an interaction says who does what to whom. A noun pile makes the reader guess which way the work flows.

Bad: "Correction Handoff" (handed which way? by whom?)
Good: "the correction package **we hand to** Vendor X"

### Never let a plain-English gloss change the meaning

A plain-language summary of formal criteria is a restatement, not a rewrite: it must not claim more or less than the normative text it covers. "Customers can see which items are eligible" is not the same as "customers can complete a return"—one shows information, while the other promises an end-to-end action. After writing any intro, summary, or roll-up, re-read it against the criteria it covers and confirm the scope matches exactly.

---

## Example Structure

```markdown
# PRD: [Feature Name]

## Summary
[A few sentences explaining what is being built]

## Business Context
[Why it matters and why it is worth building; omit this section when the Summary already covers the why clearly]

## Acceptance Criteria

### [Plain-English Product Outcome or Theme]
[One or two sentences explaining what this theme delivers and why it matters]

- [ ] **AC-AREA-01 — [Plain-language claim].** [Exact, verifiable outcome]
- [ ] **AC-AREA-02 — [Plain-language claim].** [Exact, verifiable outcome]

### [Another Plain-English Product Outcome or Theme]
[One or two sentences that preserve the meaning of the criteria below]

- [ ] **AC-OTHER-01 — [Plain-language claim].** [Exact, verifiable outcome]

## Out of Scope
- [What we're not doing - optional, only if needed for clarity]
```

The Summary always covers **what** and may also cover **why** when the motivation is straightforward. Use a separate Business Context section when the why needs room of its own. The acceptance-criteria themes form the skimmable product outline, and the criteria define the exact contract. Add only the sections the product needs.

---

## Document Storage Convention

Requirements live under `docs/` in one of two roots, each holding one directory per piece of work. The two roots hold the **same document set in the same format** — the same writing skills, readiness checks, phase split, and build skills apply to both. The root only tells a reader what kind of delivery to expect:

- `docs/prds/` — a program: a capability with several themes, stakeholder decisions, work that will be referenced for months.
- `docs/changes/` — a bounded delivery: a ticket's worth of work, a bug with acceptance criteria, a small enhancement, however many sessions it takes. A miscellaneous bucket, deliberately.

Above both sits a third root for ideas too big for one PRD:

- `docs/initiatives/` — one directory per idea that was cut into several PRDs, holding its initiative brief, its PRD list and its PRD contracts (`docs/initiatives/{name}/{name}-initiative-brief.md`, `{name}-initiative-prds.md` and `{name}-prd-contracts.md`), plus an optional `{name}-coverage-matrix.md`. `initiative-breakdown` owns this layout. The PRDs it plans still live in `docs/prds/`, one directory each, named `{name}-{short-name}`.

Outside `docs/`, at the repository root, sits the material requirements are drawn from:

- `source-material/` — material received from the business, quarantined: a handoff package or a stakeholder's reply in its own directory named for where it came from and when, and, for raw material that went through `requirements-intake`, one directory per piece of work holding its requirements intake record (`{name}-requirements-intake.md`) and what was received (`received/`, each file marked reference only, code in a `reference-only-code-{what}/` directory). It is not under `docs/` because it is not documentation and can include code. Nothing in it is a requirement or part of the application. It is read when the requirements are first written from it; after that they stand on their own. Whatever they need from it is restated in them: no requirements document (anything under `docs/prds/`, `docs/changes/` or `docs/initiatives/`) links into it, and a PRD, its assumptions, technical design and phase documents, and an initiative brief do not name it either.

When unsure, use `docs/changes/`; if it grows into a program, move the directory. **Only the user creates a change directory**, when deciding to work on something — a session never creates one to park work it noticed (see `implementation-lifecycle`, the disposition rule). There are two exceptions, both for work someone asked for: a follow-on for a stakeholder's new asks, which `assumptions-document-feedback` creates when the PRD it follows is not in an initiative, and a change PRD that `implement-from-discovery` writes for the change it was asked to build, when that change is too big to amend or no PRD owns it (its Phase 4).

Both roots hold **living documents** for the work they describe. Any change to intended behavior — including an ad hoc fix — amends the PRD and technical design that own that behavior first, then the code (`implementation-lifecycle`, Docs Before Code). Amending is always allowed and is the cheapest thing a session can do, so it is the default. Stakeholder feedback after a PRD's build has started is the exception: fixes still amend that PRD, but new asks go to a follow-on, so the build finishes on the scope it started with (`assumptions-document-feedback`, Step 1a). An ad hoc change is sorted by the same test (`implement-from-discovery`, Phase 4), and one that leaves the documents true and adds no business rule needs nothing written. A change directory is for work written up on its own: too big for an amendment, spanning several PRDs, or a component with no PRD to amend. When that work changes behavior an earlier PRD defined, the earlier PRD is not rewritten: the new criterion names what it replaces ("When Later Work Changes an Earlier Criterion" above). The convention will never be applied perfectly; its job is that the next session starts from the documents, not from the code. Where the work is scheduled, prioritized, or assigned is outside this methodology; an optional `**Source:**` line at the top of the PRD may name where the requirement came from (a ticket key, an email, a meeting) as a pointer, and no skill reads that system.

Related technical designs, assumptions, mockups, mappings, samples, and phase documents colocate inside the directory so readers can find the complete context in one place. Follow an established repository convention when one already exists instead of moving documents for consistency alone.

### Directory Structure

```
source-material/    ← at the repository root: material received from the business; requirements-intake adds {name}/{name}-requirements-intake.md + received/
docs/initiatives/   ← ideas cut into several PRDs: {name}/{name}-initiative-brief.md + {name}-initiative-prds.md + {name}-prd-contracts.md
docs/prds/          ← programs
docs/changes/       ← bounded deliveries; identical layout
  {name}/
    {name}-prd.md
    technical-design.md
    assumptions.md (if applicable)
    mockups/ (if applicable)
    [phase documents, if the work is split into phases]
```

When phase documents are needed, colocate them with the PRD and use the `phase-split` skill for sizing and naming. This writing standard does not define phase structure.

### Naming Convention

Use descriptive, hyphenated names for the PRD's directory and the PRD file itself. Both are the PRD's title (its H1, `# PRD: {Title}`) in kebab case, so the title, the directory and the file name always match; a planned PRD's directory also starts with its initiative's name ("Writing a planned PRD from an initiative"). A title changed before the PRD is split into phases renames both in the same change:

- `docs/prds/customer-returns/customer-returns-prd.md`
- `docs/prds/purchase-approvals/purchase-approvals-prd.md`
- `docs/prds/data-audit-viewer/data-audit-viewer-prd.md`
- `docs/changes/fix-null-email-in-contact-import/fix-null-email-in-contact-import-prd.md`

Supporting documents inside the PRD directory use simple, predictable names:

- `technical-design.md`
- `assumptions.md`

There's no need to repeat the PRD name in these supporting filenames — the directory already provides that context.

### Existing Documents

Documents a repo already holds stay where they are and are read as they are — moving them into this layout is a separate, optional step, never a side effect of new work. A new change directory always goes in `docs/changes/`, whatever else the repo holds.

### Cross-Repo Work

If a PRD or an initiative spans multiple repositories, store it in whichever repo is the primary home for the work, or in a dedicated product/project-level repo if one exists.

---

## Next: Refinement, Then the Technical Design

Once the PRD is drafted, commit it with its assumptions and mockups as `docs({feature}): draft PRD`, so the refinement's changes are one diff of their own. This is the default; the user's instructions override it (`pre-commit-validation`, "Who Commits"). Then refine it with `autonomous-prd-refinement`, which reviews and fixes the PRD, its assumptions and its mockups until no Medium or High finding is left; for a small PRD, one `deliverable-review` round is enough, its fixes committed as `docs({feature}): PRD refinement complete — one review round` (an empty commit when it fixed nothing). The user's review of the refined PRD is recommended next, ideally with whoever owns the business decisions, but not required. Then write its technical design with `technical-design-writing-standards`, as `technical-design.md` in the same directory.

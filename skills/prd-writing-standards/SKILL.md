---
name: prd-writing-standards
description: Standards for writing skimmable PRDs (Product Requirements Documents) — clear business context and testable outcomes without implementation details, invented responsibilities, or step-by-step instructions.
user-invocable: true
---

# PRD Writing Standards

Guidelines for writing PRDs.

---

## What Is a PRD?

A PRD (Product Requirements Document) is a high-level description of a product change, capability, or initiative we're delivering. It answers the questions **"What are we delivering?"** and **"Why are we doing it?"** in plain business language.

A PRD should be understandable by product managers, stakeholders, and anyone who needs to know what we're delivering without diving into technical details.

---

## Before You Write: Is This One PRD?

A PRD in `docs/prds/` is a medium body of work that ends with something finished that can be promoted to production. It is not the whole application; a bounded change in `docs/changes/` uses the same document set and can be as small as one fix (see "Document Storage Convention"). Before drafting, check the source material against the PRD-sized test in `prd-roadmap` (Step 2). The usual sign it fails: the work would take many phases before anything finished reaches production, or it bundles several outcomes that could each ship on their own. When it fails, run `prd-roadmap` first. It cuts the idea into planned PRDs, and this skill then writes them one at a time. The same holds when a draft outgrows the test partway through writing: stop, and hand the draft to `prd-roadmap` as its input.

**Writing a planned PRD from a PRD roadmap.** When the PRD is an entry in a PRD roadmap (`docs/roadmaps/{name}/{name}-prd-roadmap.md`), its scope comes from that entry (and its rows in the coverage matrix beside it, when the roadmap has one), and its decisions come from the full brief beside it. Use the directory name the entry gives. Put a `**Roadmap:**` line under the H1 linking the entry, and set the entry's Status to `PRD written` with a link to the PRD file, in the same change.

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

- **On the new criterion, written with the PRD:** a `Replaces:` line naming each earlier criterion it changes. It is part of the new PRD's content and changes freely while the PRD is drafted and refined. While writing, add one only where you already know the earlier criterion; don't search the repo for them, because the conflict check does that during refinement or at build.
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
- Surface an unknown that could make the outcome infeasible or materially change scope, risk, cost, or the user experience — as an assumption entry (`assumptions-document-writing`) when it is a business question, or in the technical design's Open Questions when it is technical. The PRD-writing task should surface that question; it does not need to perform a technical investigation that belongs elsewhere.

An explicitly chosen manual step can be a valid requirement. The problem is not user involvement; it is turning the first implementation idea into a user obligation without deciding that the manual step is part of the product.

Bad: "The user supplies a CSV containing all contacts." This unnecessarily chooses both the actor and the file format.

Good: "The system can access a contact list containing each person's name, company, role, and profile link." This states what the product needs while leaving the acquisition method open.

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

- `docs/roadmaps/` — one directory per idea that was cut into several PRDs, holding its full brief and its PRD roadmap (`docs/roadmaps/{name}/{name}-full-brief.md` and `{name}-prd-roadmap.md`), plus an optional `{name}-coverage-matrix.md`. `prd-roadmap` owns this layout. The PRDs it plans still live in `docs/prds/`, one directory each, named `{name}-{short-name}`.

When unsure, use `docs/changes/`; if it grows into a program, move the directory. **Only the user creates a change directory**, when deciding to work on something — a session never creates one to park work it noticed (see `implementation-lifecycle`, the disposition rule).

Both roots hold **living documents** for the work they describe. Any change to intended behavior — including an ad hoc fix — amends the PRD and technical design that own that behavior first, then the code (`implementation-lifecycle`, Docs Before Code). Amending is always allowed and is the cheapest thing a session can do, so it is the default. A change directory is for work you choose to write up on its own: too big for an amendment, spanning several PRDs, or a component with no PRD to amend. When that work changes behavior an earlier PRD defined, the earlier PRD is not rewritten: the new criterion names what it replaces ("When Later Work Changes an Earlier Criterion" above). The convention will never be applied perfectly; its job is that the next session starts from the documents, not from the code. Where the work is scheduled, prioritized, or assigned is outside this methodology; an optional `**Source:**` line at the top of the PRD may name where the requirement came from (a ticket key, an email, a meeting) as a pointer, and no skill reads that system.

Related technical designs, assumptions, mockups, mappings, samples, and phase documents colocate inside the directory so readers can find the complete context in one place. Follow an established repository convention when one already exists instead of moving documents for consistency alone.

### Directory Structure

```
docs/roadmaps/      ← ideas cut into several PRDs: {name}/{name}-full-brief.md + {name}-prd-roadmap.md
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

Use descriptive, hyphenated names for the PRD's directory and the PRD file itself:

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

### Cross-Repo Initiatives

If a PRD spans multiple repositories, store it in whichever repo is the primary home for the initiative, or in a dedicated product/project-level repo if one exists.

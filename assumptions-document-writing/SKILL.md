---
name: assumptions-document-writing
description: Standards for writing business assumptions documents — specific implementable statements, plain English, confidence levels, and stakeholder validation format.
---

# Assumptions Document Writing Standards

Guidelines for writing business assumptions documents.

**Related skill**: See `assumptions-document-feedback` for processing stakeholder responses.

---

## Purpose

Assumptions documents are for **getting business questions answered by stakeholders**, not for documenting our technical approach or implementation details. The goal is to move forward with development while getting validation on key business assumptions we're making.

**Design for busy stakeholders**: These documents should be quick to scan and easy to respond to. Every element should earn its place—if it doesn't help stakeholders understand and validate, remove it.

## Guideline: Refer to "Business Validation", Not Specific People

Use general terms like "business validation", "stakeholder validation", or "business stakeholders" rather than calling out specific people's names throughout the document.

**Why**:
- The person validating may delegate to others
- Multiple stakeholders may need to validate different aspects
- Keeps the document professional and reusable
- Avoids the feeling that one person is solely responsible

❌ **WRONG**: "This document requires [Name]'s validation before implementation"

✅ **RIGHT**: "This document requires business validation before implementation"

**Exception**: It's fine to mention specific people when:
- Referring to code they wrote: "[Name]'s reference code shows..."
- Citing specific feedback they gave: "Per [Name]'s comment in the 2026-11-14 meeting..."
- A question genuinely only they can answer: "Only [Name] knows the sandbox account IDs they used..."

But don't use their name just to mean "business stakeholder" in general.

## Implementation Readiness Mindset

The purpose of an assumptions document is to capture **everything we need to know to implement**. The goal is that when we start coding, we don't discover new business questions that require going back to stakeholders.

### Think: "If I Had to Write Code Right Now..."

When writing assumptions, put yourself in the mindset of a developer about to implement. Ask:
- What business decisions affect my code?
- What data values, thresholds, or mappings do I need?
- What edge cases require business input (not just technical handling)?
- What would make me stop and ask a question?

For each question that comes up, **don't just list it as a question**. Instead:
1. State your best-guess answer as an assumption
2. Provide evidence for why you think this
3. Assign a confidence level
4. Assess the impact if you're wrong

### Why This Matters

Without this mindset, you'll write assumptions that seem comprehensive but miss critical implementation details. Then during development, the AI or developer will identify gaps and you'll need to go back to stakeholders with "a few more questions" — which undermines trust and delays the project.

### The "95% Confidence" Rule

When doing this implementation readiness review, ask yourself: "If I'm 95%+ confident in my answer, do I even need to include this?"

- **Below 95% confidence**: Include it — stakeholders should validate
- **95%+ confidence**: Leave it out, whatever the impact — proceed, and adjust if it turns out wrong

Declaring every near-certain item would bury the few that need a human under more entries than anyone will read. At 95% the method cuts itself that break, for 🔴 HIGH impact too.

### Blocking Open Questions (Rare Exception)

If, after investigating, you cannot put forward an answer at all, carve the question out as a **Blocking Open Question** at the very top of the document, before any assumptions, and stop and ask — saying what would let you decide.

**Use this sparingly.** If you can put forward any answer the evidence favors, at whatever confidence (30% included), state it as an assumption and proceed on it. A blocking question has one condition: the evidence favors none of the options over the others — in practice, a best answer under roughly 20%.

See the template below for the format.

---

## Before You Write an Entry: Four Gates

The rest of this skill governs form and which kinds of item belong. These four checks catch a
failure neither does: an entry that passes every rule of form — question title, plain English,
example, evidence, checkboxes, honest confidence — and is still wrong, because it asks the wrong
question, asks one that is already answered, quietly narrows a requirement, or proposes the
opposite of a ruling the stakeholder already gave. Format is not a quality gate. Run these four checks on
every candidate entry, at the moment of writing, before it gets an ID. They apply when you are the
one surfacing a new assumption; reformatting or rewriting an entry that already has an ID is form
work only and skips them.

**Why the moment of writing.** Until you write the entry's title, the uncertainty is a vague
unease. Writing the title — *the question this assumption answers* — turns it into a specific,
searchable question. That is the cheapest moment there will ever be to ask whether someone has
already answered it.

### Gate 0: Is this the right question? — a premise check, not a lookup

An assumption surfaced mid-implementation is the last link in a chain: a requirement read a
certain way, an approach chosen, a result that did not fit, and now a question. When the chain
took a wrong turn, the question at the end is the wrong question, and no amount of care in
answering it helps — the entry will be well-formed, honestly confident, and about the wrong thing.
Before looking anything up, spend a few minutes on the chain, not the entry:

- **Would the stakeholder recognize the question?** If it only makes sense given how you chose to
  build it, it is a question about your approach, not about what the business intends. Find the
  business question underneath and ask that one — or notice there is none, and decide the
  technical fork yourself.
- **Does the question disappear under a different reading?** Re-read the requirement it hangs on.
  If a plainer reading makes the question moot, the assumption you need — if any — is about that
  reading, not the downstream detail.
- **Is the proposed answer the one you would want, or the one that fits?** State the alternative
  you did not propose and why it lost. If you cannot, you have a preference, not an assumption, and
  the confidence is lower than it feels.

This is thinking, bounded to minutes, not research; it sharpens what Gate 1 then looks up. When
the chain mattered, one sentence in the entry's evidence saying how the question arose lets the
stakeholder check the premise as well as the answer.

### Gate 1: Look it up before you declare it — a lookup, not an investigation

Before assigning an ID, check the places an answer would already be sitting:

- **This document** — the validated table and the entries already in the body.
- **The stakeholder's own written feedback** — their emails, the meeting transcripts
  (in your meeting notes or transcripts archive, if you keep one), and whatever
  the PRD directory keeps as evidence. A ruling in their own words beats any inference.
- **The PRD, the Technical Design, and any field-mapping or data-dictionary document the project
  maintains** — a ruling is often already recorded as a requirement.
- **Production data, if one query answers it** — read-only, and only where the project allows it
  (`engineering-principles`, "Production Data"): what values does the column actually carry today?
- **Consumer code, if it constrains the choice** — hardcoded literals, joins, filters.

**This is a lookup, not an investigation, and the distinction matters.** This skill loads late —
when an entry is about to be written, usually after most of a session's work is done — and "raise
confidence to 95%" read literally could mean an hour of exploration at exactly the wrong moment.
That is not what this gate asks. Open-ended investigation — exploration scripts, API probing, deep
analysis — is governed by `implementation-lifecycle`'s confidence table and has already had its
turn. This gate asks only: **is the answer already written down somewhere you did not read?** A
handful of targeted lookups, minutes rather than hours; if they find nothing, write the entry at
the confidence you actually have.

The asymmetry is what makes the lookup mandatory even at the end of a long session. An
already-answered question sent to a stakeholder costs a round-trip measured in days, spends their
attention, and may ask them to reverse themselves. The lookup costs minutes.

**What the lookup's result tells you.** If it answered the question, the question was either
**already decided** — a ruling or requirement you had not read — or **technical** — it turned on
facts, not on what the business intends. Either way the entry is removed, not declared. For a
decided question, build against the ruling and cite where it lives; for a technical one, note the
reasoning in the commit message where it isn't obvious. If the lookup narrowed the question, or
found partial or conflicting evidence, that goes into the entry's evidence and sets its
confidence. Only the residue no lookup can settle — what the business *wants* — is a business
question, and only that gets an ID. Expect the lookup to resolve candidates more often than not:
when an "assumption" turns out not to need one, it is usually because the answer was findable, not
because it was constructible.

### Gate 2: Never narrow a requirement to fit a measurement

The most common way to contradict a requirement — or a ruling recorded as one — without noticing
it. The requirement says *every* row must carry a value. The build measures some that do not. The
draft assumption proposes that every *qualifying* row carries it — active, current, in-scope,
whichever qualifier happens to exclude the rows that failed — and the failures become a disclosed
exception set. Well-formed, well-argued, honestly confident, and it has redrawn the requirement's
boundary to exactly where the data landed.

**The tell:** if your proposed answer makes the current state look compliant where the literal
requirement says it is not, you have reframed the requirement, not filled a gap it left. An
assumption answers a question the requirement is *silent* on; it never moves the requirement's
edge. This is the assumptions-document form of making the tests pass by editing a test's expected
value to match what the code produced.

When you catch it: stop, name the gap **against the requirement as written**, and treat closing it
as work — usually an investigation first (can the failing rows be resolved by a path the build does
not yet try?), and a business question only for a proven remainder.

### Gate 3: A prior ruling is reopened, never quietly contradicted

Stakeholders are not infallible; they rule on the evidence they had. When new evidence is genuinely
more compelling — measured data the ruling predates, a source they never saw, a consequence they
could not have known — reopening is the right move. But reopening is a distinct act with three
rules, and none of them is optional:

1. **Never a fresh ID.** Writing the contrary answer as a new `CATEGORY-NNN` entry presents a
   decided question as an open one, and the reader cannot tell they are being asked to reverse
   themselves. Reopen under the **original ID**, returned to the body with the heading marker
   `⏳ PENDING (Reopened YYYY-MM-DD against the YYYY-MM-DD ruling)`. The validated-table row
   **stays**, with a note in its Notes column: *Reopened YYYY-MM-DD, see body*. That table records
   what was decided and when — it is a history, not a statement about what the build is doing — so
   the row survives the reopening, and the PRD and Technical Design likewise keep the original
   decision until the stakeholder revises it. When the reply lands, the body entry leaves again and
   the row's note records the outcome.
2. **Put the ruling and the new evidence side by side.** State what was ruled, when, and on what
   basis; what has been learned since; and why it is more compelling than what the stakeholder had
   in front of them. The Confirm-or-Correct block's first option is the revised answer; the second
   is explicitly *"Wrong — keep the original ruling."*
3. **Proceed on the revised answer — a reopened entry is still a green light.** Assumptions exist
   so work does not block on stakeholder round-trips, and a reopened one is no exception: build on
   the proposed answer unless it is corrected, exactly like every other entry. Holding the
   superseded answer would mean parking — or unwinding — well-evidenced work while waiting for a
   reply, which is the blocking this mechanism exists to avoid.

   **What changes is VISIBILITY, and that is the point of the reopened form.** A normal entry fills
   a gap nobody had ruled on; this one revises a decision the stakeholder personally made. So the
   entry says so where they cannot miss it: what they ruled, when, what has been learned since, and
   that the build is proceeding differently because of it. State it as fact, not apology. The risk
   being managed is their discovering months later that a decision of theirs was quietly reversed —
   not the risk of building on the better answer.

The green light is not a rule with exceptions — it is what an assumption is, and a reopened entry is
an assumption. The one thing your own evidence never buys is a silent edit to the stakeholder's own
record: the PRD and Technical Design keep the decision recorded as theirs until they revise it, and
so does any expected value they validated for a test — a test that checks one stays red and says why. The
build proceeds on the revision the entry discloses. And if acting on the revised answer would itself
be irreversible — charging money, deleting data, writing to production — that action waits for the
user like any other irreversible step (`implementation-lifecycle`, The Critical Exception): the
reopening licenses the build, not the blast radius.

Reopening is rare. The bar is evidence the stakeholder **did not have**, not a different reading of
evidence they did — and the revised answer carries honest confidence well above a coin flip; you do
not ask a stakeholder to reverse themselves on a hunch.

---

## Assumption ID System

Each assumption gets a permanent ID that **never changes and is never reused**.

**Format**: `CATEGORY-NNN` (e.g., `DATA-001`, `AUTH-002`, `INTG-003`)

The category prefix serves two purposes:
1. **Groups related assumptions** for easier scanning
2. **Signals that IDs are permanent references**, not sequential numbers to be renumbered

### Example Categories

Choose short (2-5 character) prefixes that fit your document. Examples:

| Prefix | Use For |
|--------|---------|
| `DATA-` | Data sources, availability, formats |
| `AUTH-` | Authentication, authorization, permissions |
| `RULE-` | Business rules and logic |
| `SCOPE-` | What's in/out of scope |
| `INTG-` | Integrations with external systems or APIs |
| `MAP-` | Mapping/matching between systems |
| `UI-` | User interface behavior and interactions |
| `WORK-` | Workflow, process, or state machine logic |
| `NOTIF-` | Notifications, emails, alerts |
| `PERF-` | Performance requirements or SLAs |

You can also use domain-specific prefixes that make sense for your project (e.g., `PAY-` for payments, `CUST-` for customers, `ORD-` for orders).

### ID Rules

- **IDs are permanent** — once assigned, never change them
- **Never renumber** — if `AUTH-002` is validated, the next authentication assumption is `AUTH-003`, not `AUTH-002`
- **Gaps are expected** — seeing `INTG-001`, `INTG-003`, `INTG-005` is normal (INTG-002 and INTG-004 were validated)
- **Validated assumptions keep their original ID** in the validated table

**Why this matters**: Stakeholders reference assumptions by ID in email replies ("AUTH-001 yes, INTG-002 no, do this instead..."). If IDs change, historical communication becomes impossible to interpret.

### Status Markers

An entry's heading can carry a status marker after the title:

- `⏳ PENDING` — awaiting validation. Every entry in the body is pending by definition, so a heading that has never changed can omit it. Spell it out once an entry has been updated, together with what changed: `### AUTH-001. Do suspended users keep read-only access? — ⏳ PENDING (Ruled 2026-08-05 — NEW SINCE YOUR ANSWER; updated 2026-08-12; 85% confidence)`. That tells a stakeholder re-reading the document which entries moved since they last saw it. A ruling reopened against new evidence (Gate 3) uses the same marker with a reopening parenthetical — `⏳ PENDING (Reopened YYYY-MM-DD against the YYYY-MM-DD ruling)` — so the reader knows at the heading that this is a question they already answered.
- `✅ VALIDATED (date)` — the stakeholder confirmed it. This is a transitional marker, not a resting state: mark it, move the decision into the PRD or Technical Design, then move the entry to the Validated Assumptions table.

Those are the only two markers. A heading is not a place for status narrative — but a marker
may carry a **tag from the closed vocabulary below**, and nothing else.

#### The heading tag vocabulary

When a register goes back to a stakeholder carrying items they have already answered, the
heading tells them, while scanning, whether this one needs their attention. Only these four
tags exist, each defined in `assumptions-document-feedback` section 6a, and each also stated
on the entry's first line where it can say *what* changed:

| Heading form | Means |
|---|---|
| `⏳ PENDING (Ruled YYYY-MM-DD — nothing new since; NN% confidence)` | Built or queued exactly as ruled; nothing found since. A tick makes it final. |
| `⏳ PENDING (Ruled YYYY-MM-DD — we read your words; NN% confidence)` | Their answer needed an interpretation. Check the reading. |
| `⏳ PENDING (Ruled YYYY-MM-DD — NEW SINCE YOUR ANSWER; NN% confidence)` | Something was found or built afterwards. The first line says whether it agrees, contradicts, or exposes a gap. |
| `⏳ PENDING (Added YYYY-MM-DD — new question; NN% confidence)` | Never put to them before. |

Add `updated YYYY-MM-DD;` before the confidence when the entry itself has moved since it was
answered. A reopening keeps its own form — `⏳ PENDING (Reopened YYYY-MM-DD against the
YYYY-MM-DD ruling)` — and may carry the `NEW SINCE YOUR ANSWER` tag, since that is what a
reopening always is.

**Anything outside this table is narrative and does not belong in a heading.** Inventing a
fifth tag defeats the point: the vocabulary is only useful while a scanner can trust that
every heading uses one of four known words.

### Entry Titles: State the Question the Assumption Answers

Every assumption began life as a question; the entry's title should state that question,
compactly, rather than a topic label. A stakeholder scanning the headings can then tell what
each item decides before reading a word of the body.

❌ `### DATA-005. What the pre-launch signup count is sourced from` (topic)

✅ `### DATA-005. Merge two sources for the pre-launch signup count, with the billing system winning where they disagree?` (the question, answerable from the heading)

The body still leads with the **Assumption** — the proposed answer — per Principle 1. Only the
title is phrased as the question.

---

## Core Principles

### 1. State Assumptions, Not Questions — And Be Implementation-Specific

Assumptions must be **specific enough to implement from**. We're not asking open questions — we're stating exactly what we're going to build and asking stakeholders to confirm or correct it.

The assumption statement itself should make clear what we're building. There's no need for a separate "What We're Building" section if the assumption is written well.

❌ **WRONG - Open Question**:
> "What status should we use to determine active users?"

❌ **WRONG - Vague Assumption**:
> "There is a specific status filter (e.g., `status = 'active'`) that defines eligible users"

This says there IS a filter but doesn't state WHAT filter we're using. We can't implement from "there is a filter."

✅ **RIGHT - Specific and Implementable**:
> **Assumption**: We query users where `status IN ('active', 'pending_review')` to get eligible users. This is the filter used in the existing reference code.

**Why**: We're not waiting for answers — we're proceeding with these exact values and need stakeholders to validate or correct us. Every assumption should be specific enough that a developer could implement directly from it without needing more information.

**Test**: Ask yourself: "Could I write the code from this assumption alone?" If the answer is "no, I'd need to ask more questions," the assumption isn't specific enough.

---

### 2. Write in Plain Business English with Concrete Examples

Business stakeholders shouldn't need to understand technical jargon, field names, or data formats. Translate technical details into plain English and provide concrete examples.

❌ **WRONG - Technical jargon**:
> **Assumption**: Customer records are matched by:
> 1. `normalizedEmail = LOWER(TRIM(legacy.email))`
> 2. New system `customer.externalId` = legacy `CustID` (format: 'C' + ID)

A business stakeholder reading "LOWER(TRIM(legacy.email))" will have no idea what that means.

✅ **RIGHT - Plain English with example**:
> **Assumption**: We match customer records between systems using email address (case-insensitive) and customer ID.
>
> **Example**: Legacy customer #1234 with email "Customer1234@Example.com" matches to the new system customer with email "customer1234@example.com" and external ID "C1234"

**Why**: Business stakeholders can verify examples against their knowledge. They can't verify technical syntax.

Where the assumption governs how specific records are treated, the example is not just a
translation aid — it is required, and it must name a real record the stakeholder can open. See
"When to Include an Example" below.

---

### 3. Focus on Business Questions, Not Technical Details

**INCLUDE**:
- Business rules and compliance requirements
- Data availability and sources
- Approval processes and stakeholder responsibilities
- Business logic validation (who will sign off that the imported totals match?)

**EXCLUDE**:
- Technical implementation details (API rate limiting, data volume, Python environment)
- Architecture decisions we can make ourselves (package structure, error handling)
- Development approach (idempotency, testing strategy, code quality)
- Things we'll "figure out" during development

❌ **Wrong - Technical Assumption**:
> "We'll process files in batches of 1000 records to avoid memory issues"

✅ **Right - Business Assumption**:
> "The operations team will provide files to us and we'll place them on the server"

---

### 4. Use Simple Checkbox Validation

Make it easy for stakeholders to respond. Use a simple checkbox format rather than verbose "YES or NO" questions that restate the assumption.

❌ **WRONG - Verbose and redundant**:
> **Please Confirm or Correct**:
> - YES or NO: The 30-day inactivity threshold for auto-archiving is correct
> - YES or NO: Users inactive for 30+ days should be moved to "archived" status
> - If NO: What is the correct threshold?

✅ **RIGHT - Simple checkbox**:
> **Confirm or Correct**:
> - [ ] Correct as stated
> - [ ] Wrong — correct answer: _______________

**Why**: The assumption already states what we're doing. We don't need to restate it as a question. A simple checkbox is faster to scan and respond to.

#### Offering Explicit "Wrong" Alternatives

When you see a specific alternative worth highlighting, list it as an explicit "Wrong" option:

> **Confirm or Correct**:
> - [ ] Correct — use customer's current email
> - [ ] Wrong — use original order email instead
> - [ ] Wrong — different approach: _______________

Always have ONE "Correct" option restating your assumption, then "Wrong" options for alternatives. Only add explicit alternatives when they're substantively different and help stakeholders quickly indicate "no, do this instead."

#### Don't Mix Questions into Confirm/Correct

The Confirm/Correct section is ONLY for validation choices—not for asking implementation questions.

❌ **WRONG**:
> - [ ] Correct — use current email
> - [ ] Clarification on where current email is stored: _______________

If you need to know where current email is stored, that's either a technical detail you can figure out yourself, or it should be a separate assumption.

#### The Checkbox Is Also the Admission Test

If an item can't carry a Confirm-or-Correct block and a confidence level, it doesn't belong in the body at all. A status narrative, a partially-ruled item whose open half is work we owe rather than an answer the stakeholder can give, anything with "Confidence: n/a" — that's a tracker wearing an assumption's ID, not an assumption. Disposition it to the validated table with a pointer to where the work now lives — the PRD or phase document a build will read, or the action item handed to the user (see "Assumptions Document Lifecycle" below).

---

### 5. Provide Context and Evidence

Don't make stakeholders take technical statements on faith. Show your reasoning.

❌ **WRONG**:
> "User roles must exist in the target system"

✅ **RIGHT**:
> **Assumption**: User roles are already set up in the target system before we run this import. We're assuming this because the existing reference code performs dynamic role lookups which only work if the roles already exist.

---

### 6. Remove Duplicates - Don't List Questions Twice

Don't have a summary section that repeats all the assumptions. Keep the document concise.

❌ **WRONG**: Listing all assumptions, then a "Summary" section listing them again

✅ **RIGHT**: Just list the assumptions once, clearly organized by category

---

### 7. Don't Include Requirements or Implementation Decisions

If something is a requirement or technical decision (not a business question), it doesn't belong in the assumptions document. These things go elsewhere:

- **PRD**: Acceptance criteria, stated as observable outcomes (re-running the import creates no duplicates)
- **Technical Design Doc**: Architecture decisions, API patterns, data flows, and the mechanism that meets a requirement (the idempotency check, error handling)
- **Technical Design / phase documents**: Specific technical implementation details

❌ **WRONG**:
> **Assumption**: The import process must be idempotent - it should check if records exist before creating them

This is a requirement, not something we need stakeholders to validate: the outcome (re-running the import creates no duplicates) goes in the PRD as an acceptance criterion, and the mechanism (check whether a record exists before creating it) goes in the Technical Design.

---

### 8. Shape Every Entry for a Scan

The reviewer skims. Within the existing entry format — which this rule does not change — shape the prose for scanning:

- **Bold the decision-carrying numbers and terms** in each entry, so the gist reads from the bold alone.
- **Cap paragraphs at 2-3 lines.** A long rationale becomes two short paragraphs or a compact table, never a wall of text.
- **Front-load the proposed answer's operative words** ("Default every legacy-era account to read-only...") rather than building up to them.

This shapes prose only. It never removes evidence, examples, or context a stakeholder needs to validate — Principle 5 still wins.

---

## Document Structure Template

```markdown
# [Feature Name] - Business Assumptions

<!-- ⚠️ EDITING THIS FILE? LOAD THE `assumptions-document-writing` SKILL FIRST ⚠️
     It owns this document's format, and most edits here are made by sessions
     doing something else — recording a ruling while building a phase — which is
     exactly how the format drifts. Folding a stakeholder's answers? Load
     `assumptions-document-feedback` as well.

     Superseded entry text comes OUT — version control holds it, and each entry
     records its ruling date as the handle. Do not layer history under a live
     entry, do not start a history file, and keep ONE Last Updated line.

     ⚠️ ASSUMPTION IDs ARE PERMANENT - DO NOT RENUMBER ⚠️
     Stakeholders reference these IDs in email feedback.
     Gaps in numbering (e.g., DATA-001, DATA-003) are expected 
     when assumptions are validated and moved. NEVER close gaps. -->

**Last Updated**: YYYY-MM-DD
**Status**: DRAFT - Pending business validation

**Document Purpose**: This document lists the business assumptions we're making to proceed with [feature]. We're not waiting for answers—we're proceeding with these assumptions and need stakeholders to validate or correct any that are wrong.

**Technical details** are documented in the [Technical Design Document](link).

---

## ⛔ Blocking Open Questions (if any)

> **Include this section only when necessary.** Most documents won't have blocking questions.

### Blocking: [Question Title]

**Question**: [Clear statement of what we need to know]

**Why we can't assume**: [Brief explanation of why the evidence favors none of the options, and what would let us decide]

---

## Data Assumptions

### DATA-001. [The question this assumption answers, stated compactly]

**Assumption**: [State clearly in plain business English what we're doing and why. This should be specific enough to implement from.]

**Example**: [Required when the assumption governs how specific records are treated; otherwise optional. A real record with its identifier and system, pulled from the data — see "When to Include an Example"]

**Confirm or Correct**:
- [ ] Correct as stated
- [ ] Wrong — correct answer: _______________

**Confidence**: X% | **Impact if Wrong**: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW

---

## Authentication Assumptions

### AUTH-001. [The question, where an explicit alternative answer exists]

**Assumption**: [State what we're doing, noting a specific alternative exists]

**Example**: [Same rule as above — required when this governs how specific records are treated]

**Confirm or Correct**:
- [ ] Correct — [concise restatement of assumption]
- [ ] Wrong — [specific alternative we've identified]
- [ ] Wrong — different approach: _______________

**Confidence**: X% | **Impact if Wrong**: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW

---

## Validated Assumptions

| ID | Assumption | Validated | Notes |
|----|------------|-----------|-------|
| DATA-002 | [One-line summary] | YYYY-MM-DD | [Where detail was moved] |
| AUTH-002 | [One-line summary] | YYYY-MM-DD | [Where detail was moved] |
```

### When to Include an Example

Apply these in order:

1. **Required** when the assumption governs how specific records are treated — matching or
   mapping between systems, a threshold or value applied to records, a rule that sorts records
   into categories, or an exception class (the products that reach no category at all). A
   stakeholder answers that kind of question by opening one concrete case in their own system.
   Without a record to open, they have to hunt one down for every entry before they can respond,
   which takes them many times longer than the answer itself.

   Pull it with the same targeted lookup Gate 1 describes — usually the query that produced the
   entry's evidence also produces the record, which makes this nearly free. If minutes of looking
   do not produce one, ship the entry with the gap named rather than stalling.

2. **Optional** when the entry is not a record-treatment rule, but the concept would still land
   better as something concrete than as an abstract description.

3. **Skip it** when the assumption is a pure policy choice with no record behind it — "should this
   refresh daily or weekly?", "are the aging buckets 0-30 / 31-60 / 61-90 / 90+ days?".

The requirement is not "every entry has an example"; it is "every entry about records names one."

**What counts as an example when one is required** (a count without a sample
record is an assertion, not evidence):

- **A real record, with its identifier and its system.** An order number, customer id, invoice
  number, or item — whatever key the stakeholder would type into that system to look it up. Link
  the identifier to its live record where the document supports it. "Account `ACC-4471` in the
  billing system, which has no tax-region attribute" is an example. "An account nobody has
  touched since 4 September" names no identifier, so it does not count.
- **One record is enough.** Two only when the point is a disagreement — show one record with each
  value that maps to it, not a count of how many disagree.
- **Show before and after when the assumption translates or changes a value**, so the stakeholder
  sees what the rule does instead of inferring it.
- **An exhaustive mapping table also satisfies this.** It is strictly better than one record,
  because it shows every case rather than one of them.
- **Pull it from the data. Never invent an id or a value.** If you cannot pull one, say so in the
  entry and mark it as a gap rather than writing a plausible-looking one.

---

## Common Pitfalls and How to Avoid Them

Before producing an assumptions document, review it for these common mistakes — and re-run the Four Gates above on every entry added this session. Catching these saves stakeholders time and keeps the document focused on what actually needs their input.

### Don't Restate the Framework: No Per-Entry Defaults, No Priority Rankings

The document's purpose statement already defines what silence means: **we proceed on every
assumption as written unless the stakeholder corrects it.** That is the entire framework, and
the stakeholder knows it. So:

- **Never add a per-entry "If no answer, we do X" line.** It restates the framework once per
  entry, and worse, it invites inventing a default that contradicts the assumption itself
  (the assumption says "we widen the band"; a nervous default says "if silent, we leave it
  alone" — now the entry disagrees with itself about what silence means).
- **Never add a "read these first" ranking or triage block at the top of the document.**
  Priority guidance belongs in the transport email, where it can be current, not baked into
  the document. And never invent urgency claims ("the rest can wait a week") to justify a
  ranking — that is a schedule commitment nobody made.
- **Confidence is always a percentage** (`85%`), never a score (`85/100`). Everyone knows
  percent means out of 100, and it is more concise.

Genuinely entry-specific gating is different and stays: "the build waits on this confirm" or
"the tolerance policy requires your named acceptance, so there is no default" are facts about
that item, not restatements of the framework.

---

### Don't Include Things We Can Decide Ourselves

If the technical team can make a decision without business input, it doesn't belong in this document. Business stakeholders shouldn't be asked to weigh in on things outside their domain.

**Remove these—we handle them ourselves**:
- API rate limiting and pagination strategies
- Caching and performance optimizations
- File storage and infrastructure choices
- Package structure and code organization
- Error handling implementation details

**Keep these—they need business input** even if they touch technical details:
- "Users with role 'admin' get access to the management dashboard" (business rule expressed technically)
- "We match records using the email field, case-insensitive" (if the business owns that matching logic)
- Data mappings between systems that reflect business decisions

**The test**: Can the engineering team make this call on their own? If yes, remove it. If we need someone who understands the business rules to validate, keep it.

---

### Keep Details Stakeholders Need to Validate

While we want to avoid unnecessary technical jargon, **don't remove details that stakeholders need to actually validate the assumption**. If you're asking someone to confirm a mapping or a set of values, they need to see the mapping or values.

❌ **WRONG - Too abstract to validate**:
> **Assumption**: We will map legacy status codes to human-readable names in the new system.
>
> **Confirm or Correct**:
> - [ ] Correct — map codes to readable names
> - [ ] Wrong — different approach: _______________

How can a stakeholder validate this? They can't see what codes map to what names.

✅ **RIGHT - Includes details needed for validation**:
> **Assumption**: We will map legacy status codes to human-readable names:
>
> | Legacy Code | Display Name |
> |-------------|--------------|
> | ACT | Active |
> | SUS | Suspended |
> | PND | Pending Review |
> | ARC | Archived |
>
> **Confirm or Correct**:
> - [ ] Correct — use this mapping
> - [ ] Wrong — corrections: _______________

Now a stakeholder can scan the table and say "yes that's right" or "no, SUS should be 'On Hold' not 'Suspended'."

**The test**: If you removed this detail, could the stakeholder still meaningfully validate? If not, keep it.

**Note**: These details may also appear in the Technical Design Document. That's fine — the assumptions doc needs them for validation, and the tech design needs them for implementation. Once validated, you can consolidate to just the tech design if you prefer.

---

### Requirements Go in the PRD or Design Doc, Not Here

If we've already decided to do something, it's a requirement—not an assumption that needs validation. Requirements belong in the PRD (as acceptance criteria) or the Technical Design Document (how they are met).

**Move these out**:
- Idempotency requirements
- Error handling approach
- Logging and observability
- Code quality standards
- Testing strategy

**The test**: Are we asking "should we do this?" (assumption) or stating "we will do this" (requirement)? Requirements don't need stakeholder validation—they need to be documented in the right place.

---

### Relocate Content, Don't Delete It

When cleaning up an assumptions document, **never delete content that has value**—relocate it to the appropriate document instead.

| Content Type | Relocate To |
|--------------|-------------|
| Technical implementation details | Technical Design Document |
| Requirements we've decided on | PRD (acceptance criteria) |
| Technical blockers awaiting action | Surfaced to the user now; the blocked work goes in the governing PRD or phase document, and any design fact it revealed goes in the Technical Design (`implementation-lifecycle`) |
| Edge cases and error handling | Technical Design Document |
| Background research/context | Technical Design Document (Overview), only as much as a decision needs |
| Superseded entry text, prior update records | Nowhere — version control holds them (see "Editing an Existing Document") |

**Why this matters**: Content that doesn't belong in the assumptions document may still be valuable. Deleting it loses institutional knowledge and forces someone to rediscover or rewrite it later.

**Process**:
1. Identify content that doesn't belong
2. Determine the correct destination document
3. Move the content (copy + delete, not just delete)
4. Optionally add a brief note like "Technical details moved to Technical Design Document"

---

### State the Assumption Clearly, Not Buried in Technical Details

The assumption statement should be immediately clear to a business stakeholder. Don't make them wade through implementation details to understand what you're actually asking them to validate.

**Before** (assumption buried):
> "Files will be auto-discovered by glob pattern in the input directory with configurable path parameters and processed in lexicographic order with atomic file locking..."

**After** (assumption clear):
> **Assumption**: The operations team will provide files to us and we'll handle placing them on the server. Files will be auto-discovered by filename pattern.

The technical details (glob patterns, file locking) are implementation—stakeholders don't need to see them. The business assumption (who provides files, where we place them) is what needs validation.

---

### Focus on Intended Behavior, Not Failure Scenarios

Write assumptions about what we're building to do, not what happens when things go wrong. Failure handling is implementation detail.

**Before** (failure-focused):
> "If the user's role doesn't exist, the request will fail with a ValidationException"

**After** (behavior-focused):
> "Permissions are assigned by looking up the user's role dynamically. If a role is missing, we surface a clear error identifying which role needs to be configured."

Both describe the same system, but the second focuses on the intended behavior and outcome rather than exception handling.

---

### Always Provide Evidence for Your Assumptions

Don't ask stakeholders to validate assumptions without showing why you believe them. Evidence helps stakeholders quickly confirm ("yes, that's right") or correct ("no, it's actually X because...").

**Without evidence** (harder to validate):
> **Assumption**: User roles already exist in the target system

**With evidence** (easier to validate):
> **Assumption**: User roles already exist in the target system. We're assuming this because the existing reference code performs dynamic role lookups, which only work if the roles are already set up.

The evidence doesn't need to be long—just enough to show your reasoning.

---

### A Record-Governing Entry With No Record

If an entry decides how specific records are treated — a mapping, a threshold, a sorting rule, an
exception class — and carries no example naming a real record, the stakeholder has to find one
themselves before they can answer. That is the single most expensive thing this document can do to
them: it turns a two-minute ruling into an investigation, once per entry.

This is distinct from evidence. Evidence says *why we believe it*; the example says *which record
to open*. An entry can have solid evidence and still be unanswerable without a record.

**Check**: For every entry, ask "does this decide what happens to particular records?" If yes, it
names one, or it names the gap. See "When to Include an Example."

---

### Be Selective About Edge Cases

Consider edge cases, but don't include every one in the assumptions document. Too many assumptions leads to stakeholder fatigue—they'll start skimming or just approving everything without careful review.

**Include edge cases that**:
- Have meaningful business impact if we get them wrong
- Require business judgment to decide how to handle
- Could change scope or approach significantly

**Leave out edge cases that**:
- Are minor technical scenarios we can handle ourselves
- Have low impact if our guess is wrong
- Are unlikely enough that we can address them if they come up

The goal is a focused document where every assumption earns the stakeholder's attention—not a comprehensive list of everything that could possibly go wrong.

---

## Confidence Levels

Don't fake confidence. Be honest about what you know vs. what you're guessing.

- **70-95%**: Strong evidence from code, documentation, or similar systems
- **50-70%**: Reasonable assumption based on partial evidence
- **30-50%**: Educated guess that needs validation
- **<30%**: Low confidence, likely wrong

❌ **Don't**: Set high confidence just because it "seems logical"

✅ **Do**: Lower confidence when you're actually unsure, even if the assumption seems obvious

---

## Impact Assessment

**🔴 HIGH Impact**:
- Changes to fundamental architecture or scope
- Major features need to be added/removed
- Significant rework required if wrong
- Example: "If user roles don't exist in the target system, we need to build role provisioning first (major scope addition)"

**🟡 MEDIUM Impact**:
- Requires refactoring but not re-architecture
- Configuration changes or parameter additions
- Can be adapted relatively easily
- Example: "If a different discount calculation method is needed, we can make it configurable"

**🟢 LOW Impact**:
- Simple configuration or minor code changes
- No architectural impact
- Example: "If file naming is slightly different, update the glob pattern"

---

## Editing an Existing Document

Everything above is written as though you are composing a document. You mostly are not.
An assumptions register is edited far more often by a session doing something else —
recording a ruling in passing while building a phase — than by one that set out to edit
it, and that is how the format decays: never in one bad edit, always in a dozen
reasonable ones. The five rules below target what piles up: **superseded entry text**, and
**record rather than ask** — material no stakeholder would ever be answering. Relocating it
does not necessarily make the register shorter, and is not meant to: what it does is stop
the record competing with the live question.

**Read this section before any edit to an existing register, including a one-line one.**
The test at the end of an edit is not "does my change read well" — it is "is the document
still in a shape this skill describes".

### One `**Last Updated**` line, replaced rather than stacked

The header carries a date, not a changelog. Replace the date; put what changed in the
entry it changed. Update paragraphs stack invisibly — each author adds one and none
removes one — and the header becomes the longest thing a stakeholder reads before
reaching a question. A narrative of edits is what the commit log already is, for free and
without drifting from the document it describes; do not keep a second one by hand.

### Superseded entry text comes out, and version control is where it goes

`assumptions-document-feedback`'s instruction to layer a corrected entry — current answer
first, correction history beneath — is the correct move **for one round on a short entry**.
It is not a resting place. Each round adds another stratum, and the entries the stakeholder
most needs to read become the longest ones in the document.

**Take the superseded text out.** The live entry keeps the current assumption, the
stakeholder's quoted words, the evidence and example that support it *now*, the ballot and
the confidence. What the entry used to say is not lost by removing it: the repository has
every prior version, and the entry records the date of the ruling that superseded it, which
is the handle for finding one:

```bash
# What did DATA-012 say when it was ruled on 2026-09-11?
git show "$(git rev-list -1 --before=2026-09-12 HEAD -- path/to/assumptions.md)":path/to/assumptions.md
```

**Relocate by content type; do not invent one archive file for all of it.** Anything that is
still *used* has a home that already exists:

| Superseded or non-ask content | Goes to |
|---|---|
| What an entry said before it was corrected | Nowhere — version control has it |
| A narrative of document edits | Nowhere — the commit log is that narrative |
| A decision that is now settled | The PRD or Technical Design |
| Technical detail, source facts, measurements a build reads | The Technical Design |
| Priority guidance for a review round | The email that carries the document |

**Wanting a single "history" file beside the register is a signal, not a solution.** It means
the body has been carrying record rather than asks; the fix is the body.

### No checklist, ranking or triage block at the top

Already stated as a pitfall for priority rankings, and it generalizes: **the top of the
document is not a place to ask for input.** A list of IDs with tick boxes cannot be
answered — nobody remembers what `AUTH-011` was — so it produces either no answer or an
unconsidered one, and it displaces the entries that could have been answered. Every ask
lives in an entry, with its evidence beside it. Priority guidance belongs in the email
that carries the document, where it can be current.

### A heading carries at most the question, a marker, a tag from the closed vocabulary, and a confidence

See "Status Markers" and "The heading tag vocabulary" under it. When an edit needs to say
more than the marker and its tag allow, the extra belongs on the entry's first line, not in
the heading. A first line stating what has changed since the stakeholder last saw the entry
is worth its space; a heading that has grown a clause per round is not.

### When an answered item may sit in the body at all, and what it owes the reader

The Lifecycle section says the body holds only what still needs stakeholder attention, and
that is still the rule. **Three things put an answered item back in the body, and nothing
else does:**

1. **The stakeholder marked their own answer provisional** — rated it, hedged it, or asked
   for another pass over the batch. Their rating governs: a ruling they themselves called
   90% is an assumption by this skill's own 95% rule, so it belongs in the body until they
   make it final. It returns under its **original ID** with a `Ruled YYYY-MM-DD` marker.
2. **A Gate 3 reopening** — *our* new evidence contradicts their ruling. Distinct from the
   first: that one is their doubt, this one is ours, and it keeps the `Reopened` form.
3. **Their answer left a gap** it did not reach, or needed a reading — the entry stands on
   their words with the open half named.

An item back in the body for any of those reasons **must say on its first line what has
happened since they answered** (the tags in `assumptions-document-feedback` 6a). Without
that, a register full of already-answered items reads as being asked to rule twice, gets
skimmed, and costs you the entries that genuinely did move. An answered item that fits none
of the three does not go back in the body — it stays in the validated table.

---

## Assumptions Document Lifecycle

An assumptions document is a **working document**, not a permanent record. The goal is to get all assumptions validated and then **move the validated findings to the appropriate permanent documents** (PRD or Technical Design).

When an assumption is validated:
1. **Move the finding** to the PRD (business decisions) or Technical Design Doc (technical decisions)
2. **Move it to the "Validated Assumptions" section** at the bottom of the document as a one-line summary

The main body of the document should only show items that still need stakeholder attention. The validated assumptions section provides a concise historical record without cluttering the document.

**Every body entry must be an answerable assumption** — Principle 4's admission test. An entry that can't carry an **Assumption** statement, a Confirm-or-Correct block, and a confidence level is a tracker, not an assumption. Disposition it to the validated table with a pointer to where the work now lives (the PRD or phase document a build will read, or the action item handed to the user) instead of leaving it in the body with nothing for the stakeholder to act on.

### Validated Assumptions Section Format

At the bottom of the document, maintain a concise list of validated assumptions. Each entry should be **one line** summarizing what was validated and when:

```markdown
---

## Validated Assumptions

| ID | Assumption | Validated | Notes |
|----|------------|-----------|-------|
| DATA-003 | User matching uses current email, not original signup email | 2026-01-03 | Moved to Tech Design |
| AUTH-002 | SSO users must also have a local account as fallback | 2026-01-03 | Moved to PRD |
| SCOPE-004 | Reporting dashboard is NOT in phase 1 | 2026-01-03 | Moved to the phase 2 document |
```

**Key points:**
- **Preserve the original ID** — this is crucial for tracing back to historical feedback
- One line per assumption — no full details
- Include validation date
- Note where the detail was moved (if applicable)
- Keep the table concise — stakeholders scanning the document can skip this section

---

## Where to Store Assumptions Documents

The assumptions document lives **inside its parent PRD's directory**, alongside the PRD and technical design. See `prd-writing-standards` for the full directory structure.

```
docs/prds/{prd-name}/     ← or docs/changes/{prd-name}/ — a bounded delivery, identical layout
  {prd-name}-prd.md
  technical-design.md
  assumptions.md          <-- here
```

### Naming Convention

Use the simple filename `assumptions.md`. There's no need to repeat the PRD name — the directory already provides that context.

---

## Adopting This Skill

**The skill has to be loaded to be followed, and the moment it is most needed is the moment
nobody thinks to load it** — a session recording one ruling in a register while its actual
work is a build. Three mechanisms close that gap. None depends on the others.

**1. The directive comment in the document.** The template above opens with a comment
naming this skill. Keep it at the very top of every register. It costs a few lines and it
works whenever the editor reads the top of the file — which is most of the time, and least
often on exactly the long documents that need it most, since those get read in pieces.

**2. The PreToolUse hook (Claude Code).** Deterministic where the comment is probabilistic:
it is read on every edit however the file was opened. The script in this skill's `hooks/`
directory watches `Edit`, `Write` and `MultiEdit` calls, and when the target is an
`assumptions.md` or a `*-assumptions.md`, injects a reminder naming this skill, its
"Editing an Existing Document" section, and the five rules registers actually drift on.

It emits `additionalContext` and **nothing else** — deliberately no `permissionDecision`,
which on PreToolUse means "skip the permission prompt" rather than "do not block", and would
silently auto-approve every write to any assumptions document on the machine. So the hook
never blocks an edit and never approves one either: your own permission settings still
decide. It fires once per session per document so a long session is told once, marks that
only after the reminder is actually written, and fails open on every path, so a broken hook
cannot stop work.

Merge this into `~/.claude/settings.json`, keeping any hooks already there (if a
`PreToolUse` list exists, add the group to it). Adjust the path if this skill is not linked
under `~/.claude/skills`. One registration serves every repository:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/assumptions-document-writing/hooks/assumptions-doc-skill-reminder.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Verify **registration** with a grep for `assumptions-doc-skill-reminder` in
`~/.claude/settings.json` rather than by asking the user. Registration is not proof it fires:
to verify **function**, make any `Edit` to a scratch file named `assumptions.md` and confirm
the reminder appears in the tool result.

**3. A line in your global instructions (both tools).** Codex has no hook mechanism, so there
the in-file comment and this line are the only guards — which is why the comment stays in the
template even where the hook is installed. One line in the instructions file your tools read
(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or whatever single file you symlink to both)
reaches both tools, and `continuation-prompt` sets the same precedent for its hook:

> ASSUMPTIONS DOCUMENTS: Before editing any `assumptions.md` (or a `*-assumptions.md`),
> load the `assumptions-document-writing` skill and read its "Editing an Existing Document"
> section — most edits to these files are made in passing by sessions doing something else,
> which is how the format drifts.

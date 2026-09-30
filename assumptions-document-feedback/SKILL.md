---
name: assumptions-document-feedback
description: Process stakeholder feedback on assumptions documents — incorporate corrections, validations, and partial answers while keeping the project moving forward.
---

# Assumptions Document Feedback Processing

Guidelines for incorporating stakeholder feedback on assumptions documents.

**Related skill**: See `assumptions-document-writing` for creating assumptions documents and full ID system details. **When this skill requires creating new assumptions** (e.g., to fill gaps from partial feedback), load and follow the writing skill — it defines the ID system, format, and the filter for what belongs in an assumptions document vs. elsewhere.

---

## What Is This Skill?

This skill helps process stakeholder feedback on assumptions and incorporate that feedback into the assumptions document in a way that **keeps the project moving forward**.

The core philosophy: **Never block waiting for perfect answers.** Stakeholder feedback often comes back incomplete, partial, or delayed. Instead of waiting for clarification, update what you can with confidence, make reasonable assumptions for the gaps, and note what still needs validation. This ensures progress continues even when stakeholders take days or weeks to respond.

---

## When to Use

Use this skill when:

- You receive stakeholder feedback on an assumptions document (email, Slack, meeting notes)
- Feedback is a mix of clear answers, partial answers, and corrections
- You need to update the assumptions document while maintaining its utility

---

## Core Principles

### 1. Always Move Forward — Never Block

The assumptions document exists to **unblock development**, not to achieve perfect validation. When processing feedback:

- **Clear answers**: Update the assumption and increase confidence
- **Partial answers**: Incorporate what's known, **make your own assumption for the gaps** (don't leave questions for stakeholders)
- **Corrections**: Update with the corrected information, **and assume forward on any new gaps the correction introduces**
- **No response on an item**: Keep the existing assumption (it was our best guess)

**Never generate "follow-up questions" as a deliverable.** Follow-up questions create blocking dependencies — you're waiting on an email instead of making progress. Instead, for every gap, make your best assumption using existing context (code, docs, domain knowledge, reasoning). The user can asynchronously validate assumptions with stakeholders without being blocked.

A partial answer is better than waiting for a complete one. An assumption is better than a question.

### 2. Preserve the Assumptions Format

When updating, maintain the assumptions document structure:
- **Preserve assumption IDs** — IDs use format `CATEGORY-NNN` (e.g., `DATA-001`, `AUTH-002`) and are permanent — never change, never reuse, gaps are expected when assumptions are validated
- Keep the assumption as a specific, implementable statement
- Update confidence levels based on new evidence
- Adjust impact ratings if the feedback changes our understanding
- Update the "Confirm or Correct" options if the original options were wrong
- Mark assumptions as VALIDATED when you have clear confirmation
- When moving to Validated Assumptions table, include the original ID

### 3. Evidence-Based Updates

For each piece of feedback:
- Note the source (e.g., "Per the stakeholder's email 2026-03-12")
- Quote relevant portions when helpful
- Distinguish between explicit answers vs. inferred answers
- If feedback is ambiguous, state your interpretation and mark it as still needing confirmation

### 4. Confidence Graduation Threshold

When an assumption reaches **≥95% confidence** — whether through stakeholder feedback, code analysis, or strong domain reasoning — it graduates from the assumptions document into the requirements (PRD/Technical Design). It's no longer an assumption; it's a decision. Don't leave high-confidence items lingering as "pending" when you're effectively certain.

### 5. Don't Downgrade Confidence Without Cause

If stakeholder feedback is silent on an assumption, that's not evidence against it. Don't lower confidence just because something wasn't explicitly confirmed. Lower confidence only when:
- Feedback contradicts your assumption
- Feedback reveals complexity you hadn't considered
- Feedback indicates the assumption is in the wrong direction

**The reverse case is not a feedback-processing step.** If, while applying a reply, you find
evidence that a ruling the stakeholder has *already given* is wrong — measured data the ruling
predates, a source they never saw — do not fold a silent correction into the update. That is a
**reopening**, governed by Gate 3 in `assumptions-document-writing`: the original ID comes back
into the body with a reopening marker, and the ruling and the new evidence sit side by side. The
build proceeds on the revised answer, exactly like every other entry — what the reopened form
changes is visibility, not the green light. The one thing the new evidence never buys is
graduation under Principle 4: the PRD and Technical Design keep the decision recorded as the
stakeholder's until they revise it, however confident the evidence.

### 6. Re-Shape Every Entry You Touch — Don't Just Append

Feedback rounds are how entries turn into walls of text. Each round bolts on a corrected statement, a stakeholder quote, and an interpretation note, and after three rounds the current answer is buried mid-block. Whenever you update an entry, re-shape the **whole** entry per Principle 8 ("Shape Every Entry for a Scan") in `assumptions-document-writing`: bold the decision-carrying numbers and terms, cap paragraphs at 2-3 lines, front-load the operative words of the assumption as it now stands.

**Re-shaping reorganizes; it never trims.** The stakeholder's quoted words and the full evidence trail survive verbatim — Principle 5 of the writing skill still wins. For one round on a short entry, layer it (current assumption and confirm/correct first, correction history beneath) rather than cutting anything.

**But layering is one round's answer, not a resting place.** Every round adds another stratum, and left alone this makes the entries the stakeholder most needs to read into the longest ones in the document. Once an entry has been through more than one round, or has grown long, **take the superseded text out**: the live entry keeps the current assumption, the stakeholder's quoted words, the evidence and example that support it now, the ballot and the confidence. Removing it loses nothing — version control holds every prior version, and the entry records the ruling date that supersedes it, which is the handle for finding one. Do not start a history file beside the register to hold it; see "Superseded entry text comes out, and version control is where it goes" in `assumptions-document-writing`, which gives the relocation table for the content that *does* still have a home.

### 6a. Say What Has Happened Since They Answered

An item the stakeholder already ruled on, left in the body for another pass, has to earn the second read. **Give every such entry a first line, under the heading, saying what has changed since they answered** — and carry the same tag in the heading, in the form "The heading tag vocabulary" defines in `assumptions-document-writing`, so the state is visible while scanning. **Four tags, and no fifth:**

- **nothing new since** — built or queued exactly as ruled, nothing found since. A tick is all it needs.
- **we read your words** — their answer needed an interpretation (two sentences that disagreed, a "Wrong" box ticked over a restatement of the proposal, one word taken a particular way). Name the reading and ask them to check it.
- **NEW SINCE YOUR ANSWER** — something was found or built afterwards. Say in the same line whether it *agrees* with their ruling, *contradicts* it, or *exposes a gap it does not cover*. This is the set that deserves their attention, and the tag is what gets it there.
- **new question** — never put to them before, so there is nothing to re-read. Pairs with the `Added` marker rather than `Ruled`.

Without this, a document full of already-answered items reads as being asked to rule twice, and the entries that genuinely moved get skimmed along with the ones that did not.

**How this fits the two mechanisms already in this skill.** The tag is the one-line signal a scanner reads; the templated *"Why your [date] answer didn't close this"* section below is where a `we read your words` or gap entry then explains itself at length. Use both — the tag routes attention, that section carries the argument. Where the new evidence *contradicts* a ruling, the entry is a Gate 3 reopening in `assumptions-document-writing` and takes the `Reopened` form; the tag is how the reader finds it, never a substitute for that form. **Which answered items may be in the body at all** is ruled by "When an answered item may sit in the body" in that skill — this section governs only what they owe the reader once they are there.

---

## Process

### 0. Load Project Context First

**Before processing any feedback, read the documents that define what this project is building:**

1. **The full assumptions document** being updated — not just the items the feedback mentions
2. **The parent PRD** — per `assumptions-document-writing`, the assumptions doc lives inside its parent PRD's directory (`docs/prds/{prd-name}/` or `docs/changes/{prd-name}/`), so the PRD is a sibling file.
3. **The Technical Design** — also colocated with the PRD
4. **Any field mapping or related docs** referenced by the assumptions being discussed

**Why this is not optional**: Every decision this skill makes downstream depends on this context. Classifying feedback requires knowing what the PRD already specifies (feedback may restate an existing requirement, or quietly contradict one). Gap-filling assumptions are explicitly supposed to draw on "existing context (code, docs, domain reasoning)" — which you can't do without having read it. The ≥95% confidence graduation folds decisions *into* the PRD/Technical Design — impossible to do coherently for documents you haven't read. And Step 5's propagation targets should be identified up front, not discovered at the end.

Do not begin cataloging feedback until this context is loaded.

### 1. Catalog the Feedback

For each item in the stakeholder response, classify it:

| Classification | Meaning | Action |
|----------------|---------|--------|
| **Confirmed** | Explicit "correct" or equivalent | Mark VALIDATED, move to PRD |
| **Corrected** | Explicit "wrong, do X instead" | Update assumption with correction |
| **Partial** | Some info provided, gaps remain | Update what's known, assume the rest |
| **Unclear** | Response is ambiguous | State your interpretation, keep as pending |
| **No response** | Item wasn't addressed | Keep existing assumption |

### 2. Process Each Classification

#### Confirmed Items
- Update status to "✅ VALIDATED (date)"
- Add evidence: "Per [stakeholder] (date): [quote or summary]"
- If fully validated, this can be moved to the PRD/Technical Design

#### Corrected Items
- **Replace** the assumption with the corrected information — the corrected content becomes THE assumption, stated first and labeled **Assumption** like any other entry (never "Corrected Assumption", never a leading "Status:" line)
- Update confidence (usually increases with clear correction)
- Add evidence for the correction
- Keep as pending if the correction itself needs validation — and when it does, add a "why the last answer didn't close this" section so the stakeholder isn't re-reading an item they remember answering (format under "Assumption Format Reference" below)

#### Partial Items
For incomplete answers:
1. Update the assumption with what IS clear
2. For the unclear parts, **make your own assumption** using existing context (code, docs, domain reasoning):
   - State the assumption as a specific, implementable decision
   - Provide your reasoning
   - Assign a confidence level
   - If ≥95% confidence, fold directly into requirements — it's not an assumption
   - If <95% confidence, create a new pending assumption (not a follow-up question)
3. Update confidence to reflect partial information
4. Modify "Confirm or Correct" options to focus on the remaining uncertainty

**When the open half is OUR deliverable, the item leaves the body.** Sometimes feedback settles the approach and what remains is work we owe (data to deliver, a verification to run) before the stakeholder can rule further. That remainder is not an assumption — nothing is being guessed, and there is nothing the stakeholder can confirm or correct today. Don't leave the item in the body as a status narrative with "Confidence: n/a"; an entry with no assumption statement, no confidence, and no checkbox is a tracker wearing an assumption's ID. Instead: record the ruled parts in the permanent docs, move the item to the validated/disposition table with a pointer to where the remaining work is recorded (the PRD or phase document a build will read, or the action item handed to the user), and remove it from the body. When our deliverable lands and the stakeholder's follow-on ruling is needed, that ask returns as a new entry or rides the deliverable itself.

#### Unclear Items
If feedback is genuinely ambiguous:
1. State your interpretation of what they meant
2. Update the assumption based on that interpretation
3. Add a note: "Interpretation pending confirmation"
4. Keep confidence at or below current level

#### No Response Items
- Keep the existing assumption unchanged
- These can be re-sent in follow-up if critical

### 3. Assume Forward for All Gaps

**Never leave gaps as questions. Always fill them with assumptions or decisions.**

After processing all feedback, review every gap, ambiguity, or new question that emerged. For each one, first classify it:

**Is this a business question or an implementation detail?**
- **Business question** (needs stakeholder validation) → Create a new assumption with its own `CATEGORY-NNN` ID. **Load and follow the `assumptions-document-writing` skill** for how to write it — that skill defines the ID system, format, and the filter for what belongs in an assumptions document. Never embed sub-assumptions inside another assumption — each assumption is a standalone, trackable item.
- **Implementation detail** (engineering team can decide) → Put it in the Technical Design (or the phase document that will build it). It doesn't belong in the assumptions document.

**For new business-question assumptions**, make your best assumption and route by confidence:
   - **≥95%**: Fold directly into requirements (PRD/Technical Design). This is a decision, not an assumption.
   - **Below 95%**: Investigate first (Step 7), then create a new pending assumption in the assumptions document at the honest confidence — at any confidence, 30% included. Development proceeds on it; the user can asynchronously validate with stakeholders.
   - **No answer at all** — the evidence favors none of the options over the others (in practice, a best answer under roughly 20%): a Blocking Open Question, per `assumptions-document-writing`. Stop and ask, saying what would let you decide.

**The key insight**: Assumptions are the deliverable, not questions. The user can forward any assumption to a stakeholder for validation without being blocked — development proceeds on the assumption in the meantime.

### 4. Update the Assumptions Document

Apply all updates to the assumptions document:
- Update individual assumptions with new information
- Update Last Updated date
- Mark validated items `✅ VALIDATED (date)`; once Step 5 has propagated them, move each to the Validated Assumptions table (one line, original ID) and out of the body

### 5. Propagate to Implementation Documents (CRITICAL)

**This step is essential and must not be skipped.** Validated and corrected assumptions must be reflected in the actual implementation documents—otherwise the assumptions document becomes a dead end.

For each **validated** or **corrected** item:

1. **Identify affected documents**: Which documents reference this assumption?
   - PRD: Business decisions and acceptance criteria
   - Technical Design: Implementation details, field mappings, business rules
   - Field Mapping docs: If the correction changes data sources or logic

2. **Update the PRD**:
   - Fold the decision into the requirement it settles (an acceptance criterion, Summary or Business Context), stated as the requirement itself
   - Update acceptance criteria if the correction changes what "done" looks like
   - Note the source/date of validation for traceability

3. **Update the Technical Design**:
   - Update implementation logic if the correction changes how something is built
   - Update data mapping sections if sources or transformations changed
   - Add implementation notes for nuances from the feedback

4. **Update Field Mapping documents** (if applicable):
   - Update SQL queries, field sources, or business logic

**Why this matters**: The assumptions document is a working document that eventually gets emptied. If you only update assumptions without propagating to PRD/Tech Design, the validated decisions are lost when the assumption is removed. The PRD and Technical Design are the permanent records.

**Checklist for propagation**:
- [ ] PRD updated with validated decisions
- [ ] Technical Design updated with any implementation changes
- [ ] Field mapping docs updated if data sources/logic changed
- [ ] All documents have consistent information (no contradictions)

### 6. Route the Code Changes (For Items That Now Need Implementation)

**This step applies only to items that require code changes.** Confirmed assumptions that validate existing behavior, blockers that remain blocked, and items the code already handles correctly need nothing here.

For each corrected assumption, new requirement, or newly unblocked item that changes what the code must do:

- **If the work is still being built and was never split**, the amendment in Step 5 is enough — the build reads the PRD and Technical Design.
- **If the work is split and a future phase will build it**, add the item to that phase document too (`implementation-lifecycle`, disposition rule) so the implementing session inherits it without this chat's history.
- **If nothing will build it** (the work is complete), name the item in the final report as a one-line action item for the user: what the code must now do and the commit that amended the requirements, so they can run `implement-from-discovery` against that diff. A session never opens a change directory for it, and never implies the item is tracked or scheduled anywhere.

**Checklist:**
- [ ] Every item needing code changes is either in the requirements a build will read (the amended PRD, plus the phase document when split), or named for the user as an action item
- [ ] No item is described as scheduled, tracked, or "will be done" unless a build will read it

### 7. Research First (New Assumptions Below 95%)

This step applies when Step 3 produced new assumptions below 95% confidence. **Investigate each one before finalizing it**, as `implementation-lifecycle` requires — code, data, documents, the stakeholder's own written feedback. The research decision is part of the work; don't hand it to the user.

Then set each entry at the confidence the investigation leaves it at: at 95%+ it folds into requirements, below that it stays a pending assumption and work proceeds on it, and only when the evidence favors no answer at all does it become a Blocking Open Question. Report what moved in one line each: the assumption, its confidence before and after, and what settled it.

---

## Example: Processing Mixed Feedback

**Original Assumption:**
> Accounts marked "Active" with a verified email should get access to the new customer portal.

**Feedback:**
> "Wrong - implement mapping: portal access = AccountStatus = Active, EmailVerified = true, BillingStatus = Current"

**Processing:**

1. **Classification**: Corrected
2. **Update**: Replace the original logic with the stakeholder's specific mapping
3. **Check for gaps**: The response defines who GETS access but not the full picture (what about accounts that don't qualify — are they SUSPENDED or merely PENDING?)
4. **Assume forward**: Don't ask about SUSPENDED/PENDING. Check existing docs — found a dormancy rule in the field mapping doc (LastLoginDate < 2024-07-01). Use that + domain reasoning to make assumptions for SUSPENDED and PENDING at 85% confidence.
5. **Result**: Update assumption with the corrected access logic, create new assumptions for SUSPENDED/PENDING with reasoning and confidence levels

**Updated Assumption:**
> Accounts get portal access when they meet ALL these criteria: AccountStatus = Active AND EmailVerified = true AND BillingStatus = Current. This was corrected from our original understanding per the stakeholder (2026-03-12).

**New Assumption (created to fill gap — with its own ID, per writing skill):**

```
### AUTH-002. Set dormant non-qualifying accounts to SUSPENDED and the rest to PENDING? — ⏳ PENDING (Added YYYY-MM-DD — new question; 85% confidence)

**Assumption**: Accounts with LastLoginDate < 2024-07-01 that don't meet the access
criteria are set to SUSPENDED in the portal. Remaining accounts default to PENDING.

We're assuming this because the field mapping doc already defines dormancy as
LastLoginDate < 2024-07-01, the stakeholder defined the access criteria (2026-03-12),
and PENDING is the safe default for unclassified accounts.

**Example**: Account `ACC-2210` — Active, email verified, billing Past Due, last login
2024-03-02 → SUSPENDED

**Confirm or Correct**:
- [ ] Correct — SUSPENDED for dormant non-qualifying accounts, PENDING for the remainder
- [ ] Wrong — different approach: _______________

**Confidence**: 85% | **Impact if Wrong**: 🟡 MEDIUM
```

---

## Output Format

After processing feedback, provide:

1. **Summary of Changes**: Brief overview of what was updated
2. **Items Now Validated**: List any assumptions that can be marked complete
3. **Items Updated**: List assumptions that were modified with what changed
4. **New Assumptions Made**: Any assumptions created to fill gaps from partial/unclear feedback (with confidence levels). These are NOT questions — they are implementable decisions.
5. **Updated Assumptions Document**: The revised assumptions document
6. **Propagation Summary**: List of changes made to PRD, Technical Design, and other implementation documents
   - What was added/updated in each document
   - Location of changes (section names or line references)
7. **Code Changes Routed**: for each item that now needs code, where it went — the amended PRD a build will read, the phase document that will build it, or a one-line action item for the user (Step 6)
8. **Research Done** (only if Step 7 investigated new assumptions below 95%): one line per assumption — confidence before and after, and what settled it — plus any Blocking Open Question with what would let you decide

**Propagation Checklist** (include in output):
- [ ] PRD updated with validated decisions
- [ ] Technical Design updated with implementation details
- [ ] Field mapping docs updated (if applicable)
- [ ] All documents now consistent
- [ ] Code changes routed per Step 6 (amended PRD, phase document, or action item for the user)
- [ ] All gaps filled with assumptions (no follow-up questions)

---

## Assumption Format Reference

**For general assumption format, structure, and writing standards**: Load and follow the `assumptions-document-writing` skill. That skill defines the `CATEGORY-NNN` ID system, required elements (assumption statement, confirm/correct, confidence/impact), the `⏳ PENDING` / `✅ VALIDATED (date)` status markers, confidence levels, and the "is this a business question or implementation detail?" filter.

**This section covers only feedback-specific templates** — how to format assumptions that were corrected or updated based on stakeholder feedback:

**Evidence format for feedback:**
- "Per [stakeholder] ([date]): [quote or summary]"
- E.g., "Per the stakeholder's email 2026-03-12: 'implement mapping using the account billing status...'"

**When feedback corrects an assumption but does not close it** (apply Core Principle 6 scan-shaping to the rewritten entry — bold the decision-carrying terms, keep paragraphs to 2-3 lines):

The updated entry keeps the standard shape from `assumptions-document-writing`: **the assumption comes first, stated as the current assumption** — what we are now proceeding with, with the correction already incorporated. Never lead with a "**Status**:" line, never label it "**Corrected Assumption**", and never open with the item's history (no "Previous assumption (INCORRECT)" block) — a stakeholder re-reading the document should meet the same shape everywhere: here is what we're doing, confirm or correct it.

What IS added is one section the standard shape doesn't have: **why the last answer didn't close this**. Its job is to make the second ask easy to answer — state what the stakeholder's answer settled, what new fact or follow-on choice surfaced when we applied it, and exactly what the assumption above resolves that still needs their confirm. Without this section the stakeholder re-reads an item they remember answering and can't tell why it's back; with it, the second answer is one checkbox.

```markdown
### CATEGORY-NNN. [The question, stated compactly] — ⏳ PENDING (Ruled [date] — [we read your words | NEW SINCE YOUR ANSWER]; updated [date]; [confidence]% confidence)

**Assumption**: [The current assumption with the correction incorporated — specific and
implementable, per the writing skill. This is what we are proceeding with now.]

**Why your [date] answer didn't close this**: [1-3 sentences: what the answer settled,
the new fact or gap that surfaced when we applied it, and the one thing the assumption
above resolves that still needs confirmation. Cite or quote the answer here — this
section doubles as the evidence trail for the correction.]

**Confirm or Correct**:
- [ ] Correct — [restatement]
- [ ] Wrong — [alternative]: _______________

**Confidence**: X% | **Impact if Wrong**: 🔴/🟡/🟢
```

When the correction fully closes the item (nothing left to confirm), none of this applies — the item is validated and moves to the validated table as one line: what was decided and where the detail now lives; the superseded wording stays in version control.

---

## Key Mindset

Think of assumptions like a Bayesian prior:
- You start with a best guess (the original assumption)
- Feedback is evidence that updates your belief
- Perfect information is rare—you work with what you have
- The goal is to be "confident enough to build" not "100% certain"

If you can ship code that's 80% likely to be right, and the 20% failure case is low-impact and fixable, **ship it**. Don't wait for the remaining 20% certainty.

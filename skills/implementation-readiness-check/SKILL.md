---
name: implementation-readiness-check
description: Pre-implementation validation gate — surface gaps and unclear assumptions before writing code, with proposed answers, confidence levels, and impact assessments.
disable-model-invocation: true
---

# Implementation Readiness Check

Guidelines for validating understanding before writing code.

---

## What Is This Skill?

This skill is the **human-checkpoint validation gate**, for when the user explicitly wants to confirm answers before implementation begins. `autonomous-requirements-refinement` also runs it once per pass.

Its purpose: find gaps and unclear assumptions in the requirements before implementation begins. The AI identifies what's uncertain, proposes how it would handle each item (with a confidence level and impact assessment), and gives the human a chance to confirm or redirect. Implementation moves fast—this is the last chance to get aligned before assumptions become code.

Once this check is under way, no implementation begins until it is complete and acknowledged.

---

## When to Use

Run this skill **immediately before implementation** (before `phase-split` when the work will be split). Use it when the user explicitly asks for a human review checkpoint.

---

## Context to Review

Before proceeding, the AI should review all available materials related to the work being implemented, which may include:

- The PRD and/or technical design document for this feature
- The assumptions document (if one exists)
- The specific phase or slice being implemented
- Existing code related to the change

**Terminology note:** Users refer to requirements documents by many names — PRD, spec, requirements doc, design doc, etc. Don't get hung up on terminology. We're standardizing on "PRD" (Product Requirements Document) for the parent business artifact. Map whatever term the user uses to the actual documents in the project (e.g., if they say "the spec," find the PRD or technical design document that matches). The user may also reference additional context documents (mockups, data mapping sheets, stakeholder emails) — include those in your review if provided.

### Relationship to the Assumptions Document

If an assumptions document exists, **do not re-raise items that are already captured there**. The assumptions document exists because we've already gone through this exact discovery process—identifying questions, proposing answers, and flagging them for business validation. Those items are already surfaced and awaiting stakeholder input.

Re-raising assumptions during the readiness check adds noise and undermines the purpose of having a structured assumptions process. The stakeholder validation cycle for assumptions is separate from this check.

**The only valid reasons to reference an existing assumption are:**
- Something has changed that would require updating the assumption
- You've discovered information that contradicts the assumption
- The assumption needs to be refined based on implementation details that weren't visible during planning

In those cases, call out the specific change needed—don't just repeat that the assumption exists.

---

## Process

### The Mindset

Requirements are never perfect. When any developer implements a feature, they inevitably encounter gaps, ambiguities, and edge cases that aren't spelled out. They fill in those blanks as they go—making assumptions, sometimes without even realizing it.

This check is about surfacing those assumptions *before* any code is written. Instead of guessing and hoping you guessed right, put yourself in implementation mode: mentally walk through the feature as if you're about to build it right now. What questions would you run into? Where would you have to make a judgment call?

Surface those questions, propose how you'd answer them, and give the human a chance to confirm or redirect before a single line of code exists.

### Steps

**1. Review context**

Confirm you've reviewed the PRD, technical design, the phase document when the work is split, and relevant existing code.

**Then run the conflict check** (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements") against the whole PRD, unless the caller says it runs its own (`autonomous-requirements-refinement` does). It finds criteria in the repo's other PRDs and change directories that this PRD changes. An unintended conflict, where this PRD would break behavior someone asked for, is a Business question like any other, with your proposed answer. Intended ones are listed in the output as the `Replaces:` lines to add (`prd-writing-standards`), and added when the user asks you to update the documents.

**If foundational documents (PRD, technical design) cannot be located**, include a prominent warning at the top of the output stating which documents were unavailable. Without these documents, all confidence assessments are suspect. Still complete the check—don't refuse to produce output.

**2. Surface questions**

Mentally walk through the implementation. What questions would you hit? Where are the gaps, ambiguities, or unstated edge cases that would force you to make an assumption?

Focus on things that actually matter:
- Ambiguities in requirements — what does this actually mean?
- Edge cases not explicitly addressed — what happens when things go wrong or inputs are unusual?
- How new code should connect with existing code — what to call, where to hook in
- Behavior of existing code you'll depend on — does that function return null or throw? Is that field ever empty? Does that event fire before or after the transaction commits?
- Data handling decisions that affect business outcomes
- Status codes, thresholds, or mappings with business meaning

**3. Do your homework before asking**

Don't ask the human to answer something you could have figured out with some investigation. For each question you're considering, do a reasonable amount of exploration to sharpen your proposed answer:

- **Read the code**: If your uncertainty is about how existing code works, go look at it. Read the relevant service, check the tests, trace the flow.
- **Check the docs**: If your question might be answered in existing documentation, API specs, or README files, look there first.
- **Query the data**: If your question is about data characteristics (what values exist, are there nulls, how many records match a condition), write a quick query to check.
- **Test the API**: If you're unsure what an API returns, make a test call to the sandbox environment.

This might answer your question entirely (raising confidence above 95%) or at least sharpen your proposed answer. If you attempted exploration but were blocked (missing credentials, VPN required, etc.), mention this—the human may be able to unblock you.

**The key here is breadth, not depth.** You're doing a reasonable scan across all your questions — reading relevant code, checking obvious docs, maybe running a quick query. You're not spending 20 minutes chasing down one item. If a question needs that level of deep investigation, flag it and the human can direct you to use `investigate-question` for a thorough deep-dive on that specific item.

**Check the assumptions document first.** If your question is already captured in an assumptions document, do NOT include it here. That question has already been surfaced and is awaiting business validation—repeating it adds no value. The assumptions document represents a prior pass through this exact exercise. Trust that process.

Don't ask questions that are purely stylistic or trivial.

**4. Classify each question as Technical or Business**

For each question, determine whether it is:

- **Technical** — a question about *how* to implement something, where the team can make the call (architecture, integration approach, error handling strategy, data flow). These get resolved by making a decision and folding it into the technical design or requirements docs.
- **Business** — a question about *what* the system should do, where the answer depends on business rules, stakeholder intent, or user-facing behavior. If these can't be resolved in the conversation, they need to be surfaced as stated assumptions in the assumptions document.

This classification helps the human triage quickly: technical items can often be decided on the spot, while business items may need stakeholder input.

**5. Propose your own answers**

For each question, provide your best answer—how would *you* handle it if you had to decide right now? If the reasoning isn't obvious, add one sentence explaining why you think that's the right answer. Keep it concise.

**6. Assign confidence and impact**

For each answer:

- **Confidence**: How confident are you that you're right? Express this as a percentage (0–100%). Always use a specific number. Don't say "high confidence" or "pretty sure"—say 75% or 90%.
- **Impact if wrong**: How bad would it be if your proposed answer is wrong?
  - 🔴 **HIGH** — Would cause data loss, incorrect business logic, security issues, or require significant rework
  - 🟡 **MEDIUM** — Would require moderate rework or cause user-facing issues
  - 🟢 **LOW** — Minor rework, cosmetic, or easily corrected

**7. Filter and order**

- **If you're 95% or more confident, don't include it, whatever the impact.** Trust your judgment on those; listing near-certain items buries the ones that need a human.
- **Include all questions where confidence is below 95%** — these need human input.
- **Order by confidence, lowest first.** The questions you're least confident about are most likely to be wrong and most urgently need correction.
- **If you have no questions that meet the inclusion criteria**, say so explicitly: *"I've reviewed everything and have no questions that need your input. I'm ready to proceed with implementation unless you have concerns."*

---

## Output Format

The final output should be a concise list of **questions requiring confirmation**, each including:

- The classification (Technical or Business)
- The question
- The AI's proposed answer (with brief reasoning if not obvious)
- The confidence level (as a percentage)
- The impact if wrong

If foundational documents were missing, include a prominent warning at the top before the questions.

After the questions, when this check ran its own conflict check, list every finding not already asked above under **Earlier criteria this PRD replaces**, whatever its confidence: one line each, the new criterion and the `Replaces:` line it gets, or for an unintended conflict you are sure of, the fix to the new criterion you propose. Write "Conflict check: no earlier criteria changed" when it found none.

Example (documents found):

---

**Implementation Readiness Check Complete**

I've reviewed the PRD, technical design, and existing codebase. The following items need your input:

**Question 1** `[Business]`: The PRD says users should receive notifications "when their request is processed" — does this mean when processing *starts* (status changes to "in_progress") or when it *completes* (status changes to "done")? The UX feels different depending on which.

- **Proposed Answer:** Notify on completion ("done"), since that's the actionable event — the user can't do anything with an "in progress" notification. A separate "your request was received" confirmation at submission time covers the acknowledgment need.
- **Confidence:** 70% | **Impact if Wrong:** 🟡 MEDIUM — would affect user experience and notification volume

**Question 2** `[Technical]`: The acceptance criteria say "admin users can manage team permissions," but the existing role system only has `admin` and `member` roles. Should we add a new `team_lead` role, or extend the existing `admin` role with more granular permission flags?

- **Proposed Answer:** Add granular permission flags to the existing role system rather than creating a new role — this is more flexible and avoids a role proliferation problem. The technical design hints at this with "permission-based access" language.
- **Confidence:** 80% | **Impact if Wrong:** 🟡 MEDIUM — would require reworking the permission model

**Question 3** `[Technical]`: The technical design mentions sending webhook events for status changes but doesn't specify whether we guarantee delivery or use at-least-once semantics. The existing event system uses a fire-and-forget pattern with no retry.

- **Proposed Answer:** Use at-least-once delivery with idempotency keys, since webhooks to external consumers need reliability guarantees. The fire-and-forget pattern is fine for internal logging but not for external integrations.
- **Confidence:** 85% | **Impact if Wrong:** 🔴 HIGH — unreliable webhooks to external consumers could cause data sync failures

---

Once these are confirmed, we can fold the decisions into the requirements documents and then proceed to implementation.

💡 *If any of these items need deeper investigation before you can decide, I can use `investigate-question` to do a thorough deep-dive on specific items. If multiple items need investigation, these can run as parallel subagents.*

---

Example (documents missing):

---

**Implementation Readiness Check Complete**

⚠️ **Warning: I was unable to locate the technical design document for this feature.** The questions and confidence levels below are based only on the PRD and existing code. My proposed answers may not align with intended design decisions.

The following items need your input:

*(questions follow...)*

---

## After the Human Responds

The readiness check is the start of a conversation, not a one-shot gate. The human will review your questions and provide feedback — corrections, redirections, and confirmations. Here's how to handle that feedback.

### Processing the Feedback

The human's response will typically take one of these forms for each question:

- **Explicit correction:** "For question #2, do this instead: ..." → Replace your proposed answer with theirs.
- **Partial correction:** "For question #3, mostly right but also consider ..." → Refine your proposed answer.
- **Explicit agreement:** "Question #1 looks good" → Confirmed as-is.
- **"Go dig deeper on #X":** The human wants more investigation before deciding → Use `investigate-question` to do a thorough deep-dive on that specific item. See the Deeper Investigation section below.
- **Silence on a question:** The human didn't mention it at all → See below.

### Handling Unaddressed Questions

**Do NOT assume silence means agreement.** If the human didn't address one or more questions, you must ask about them explicitly. Don't proceed with your proposed answers just because the human didn't push back.

**The one exception:** If the human explicitly says something like "for anything I didn't mention, I agree with your proposed answer" — that IS blanket confirmation, and you can treat all unaddressed questions as confirmed. But only if they explicitly say this. Don't infer it, don't assume it, and don't prompt them with "should I assume silence means agreement?" — just ask about the specific unaddressed questions directly.

Example:

> *"You addressed questions 1, 3, and 5. I still need your input on questions 2 and 4:*
>
> *- Question 2: I proposed filtering by order_date. Should I go with that?*
> *- Question 4: I proposed batch size of 500. Should I go with that?"*

### Deeper Investigation

If the human asks you to dig deeper on one or more items, use the `investigate-question` skill for each item that needs investigation. This skill does a thorough deep-dive on a single question — reading code in depth, querying databases, testing APIs, and exploring data to either answer the question definitively or significantly refine the proposed answer.

**If the human asks you to investigate multiple items**, launch parallel subagents — one `investigate-question` per item. This is faster than investigating sequentially and the investigations are independent of each other.

After investigation completes, present the updated findings (with revised confidence levels) and resume the readiness check conversation.

### Summarizing the Confirmed Answers

Once all questions have been resolved (either through explicit feedback, blanket confirmation, or deeper investigation), summarize the final answers clearly:

- Restate any corrections the human made
- Confirm the proposed answers that were accepted
- Note any findings from deeper investigation that changed a proposed answer
- Call out anything that contradicts what's currently stated in the PRD or technical design

This summary is the human's chance to catch any misunderstandings before decisions get recorded.

### The Next Step: Recording Decisions

After the conversation, confirmed answers need to be recorded in the right places:

- **Technical decisions** get folded into the requirements documents (PRD, technical design) so the implementation reflects them.
- **Business items that were confirmed** also get folded into the requirements documents.
- **Business items that couldn't be resolved** (because they need stakeholder input the human can't provide) get surfaced as stated assumptions in the assumptions document, following `assumptions-document-writing` standards.

**However, do NOT update any documents unless the human explicitly asks you to.** After summarizing the confirmed answers, wait for the human to direct you. They may say:

- "Go ahead and fold those into the requirements docs" → Update the PRD and/or technical design with the confirmed decisions, using the `prd-writing-standards` and `technical-design-writing-standards` skills.
- "Add the unresolved business items to the assumptions doc" → Create or update the assumptions document.
- "Let's start implementing" → They want to skip the doc update and go straight to code (flag if any confirmed answers contradict current docs — that should be fixed first).
- Something else entirely → Follow their lead.

The point is: **you are not the one deciding to update documents or start implementation.** Present the confirmed answers, and let the human tell you what to do next.

### If Asked to Update Requirements Documents

When the human asks you to fold decisions into the docs, **update ALL affected documents** — not just the one they mention. A decision might affect the PRD's acceptance criteria AND the technical design's implementation approach AND the assumptions document. Trace each confirmed answer to every document it touches and update them all.

For example, if the human says "fold those into the technical design" but a confirmed answer also changes an acceptance criterion in the PRD, update both. The human is telling you to record decisions, not limiting you to a single file. The only exception is if they explicitly say to update one document but not another.

Steps:

1. For each confirmed answer, identify which documents it affects (PRD, technical design, assumptions, phase documents, or any other context documents that were part of the review).
2. Update all affected documents, using the appropriate writing standards skills (`prd-writing-standards`, `technical-design-writing-standards`, etc.).
3. If an assumptions document exists and any of the readiness check items overlap with existing assumptions, update the assumptions document too (mark assumptions as confirmed, update proposed answers if they changed).
4. Show what you changed so the human can verify. When this check ran its own conflict check, include a `Conflict check:` line with its result in the proposed commit message, so the build narrows from it.

---

## Rules and Constraints

- ❌ Do **not** write or suggest implementation code during this check
- ❌ Do **not** propose solutions beyond answering clarifying questions
- ❌ Do **not** proceed to implementation until the check is acknowledged
- ❌ Do **not** re-raise items already in the assumptions document—they're already flagged for validation
- ✅ Once invoked, treat this as a hard gate before coding
- ✅ Be explicit about uncertainty—don't hide low confidence behind vague language
- ✅ Prefer fewer, high-signal questions over exhaustive lists
- ✅ Classify every question as Technical or Business to aid triage
- ✅ Include impact assessment alongside confidence to highlight what matters most

---
name: assumptions-document-feedback
description: Process stakeholder feedback on assumptions documents — incorporate corrections, validations, partial answers and pushback (a doubt or question is researched and the assumption restated to meet it, never pasted in as the answer) while keeping the project moving forward. Checks every requested change against the whole initiative as it stood before the feedback, then sorts it into a fix or a new ask; once the PRD's build has started, fixes go into its phase plan and new asks, apart from minor ones, into one follow-on PRD, so a build in progress finishes on the scope it started with. Finishes every change in each PRD it reaches, including each PRD that consumes a changed contract, and gives each amended PRD one fresh check instead of rerunning its refinement.
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
- A PRD directory holds a `{name}-pending-feedback-changes.md`: an earlier round left changes there (Step 4a), and this skill resumes it

---

## Core Principles

### 1. Always Move Forward — Never Block

The assumptions document exists to **unblock development**, not to achieve perfect validation. When processing feedback:

- **Clear answers**: Update the assumption and increase confidence
- **Partial answers**: Incorporate what's known, **make your own assumption for the gaps** (don't leave questions for stakeholders)
- **Corrections**: Update with the corrected information, **and assume forward on any new gaps the correction introduces**
- **Pushback or a question**: Treat it as a clue, not an edit instruction — research it, resolve it at ≥95%, otherwise restate the assumption to address it
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
- **we read your words** — their answer needed an interpretation (two sentences that disagreed, a "Wrong" box ticked over a restatement of the proposal, one word taken a particular way, a question or doubt read as pointing at a particular gap). Name the reading and ask them to check it.
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
5. **The plan around the PRD** — its phase documents and their `**Closed:**` lines, and, when the PRD came from an initiative, every other PRD in it: the PRD list and PRD contracts (its Seams table names which PRDs consume what each PRD owns), each written PRD with its Out of Scope and assumptions register, the initiative brief's deferred list and open questions, and the coverage matrix if there is one. Outside an initiative, every other PRD or change directory the feedback touches. Step 1a decides from them whether the build has started and where each change already lives. A stakeholder sees one product, not the PRDs it was cut into, so a change judged against this PRD alone can look new when another PRD already plans it.

**Why this is not optional**: Every decision this skill makes downstream depends on this context. Classifying feedback requires knowing what the PRD already specifies (feedback may restate an existing requirement, or quietly contradict one). Gap-filling assumptions are explicitly supposed to draw on "existing context (code, docs, domain reasoning)" — which you can't do without having read it. The ≥95% confidence graduation folds decisions *into* the PRD/Technical Design — impossible to do coherently for documents you haven't read. And Step 5's propagation targets should be identified up front, not discovered at the end.

Do not begin cataloging feedback until this context is loaded.

### 0a. Establish What the Reviewer Answered

Accept feedback through any channel: review-package TXT or clipboard replies, older exports, email, chat, meeting notes or comments on raw Markdown. Do not require a review package, Git commit hash or a particular export format.

When the response includes the wording reviewed (in a reference appendix, an older export or a quote), treat that wording as the historical proposal the reviewer answered. The appendix is context, not another set of answers. Match by permanent assumption ID and compare the reviewed question and proposal with the current register and relevant requirements **before applying the response**. Use the review version and source references for traceability; a link to a moving branch does not establish what was shown. A self-contained reply does not require fetching an old Git revision.

- **Same meaning:** process the response normally; editorial wording changes alone do not invalidate confirmation.
- **Materially changed meaning:** do not carry confirmation of the old proposal onto the changed proposal. Preserve what was actually confirmed, apply corrections only to the parts they address, and report the mismatch and any unsettled current decision. Do not silently overwrite a newer stakeholder ruling; use the existing reopening rules where applicable.
- **No reviewed wording supplied:** use the available conversation, quoted text and current documents. If there is evidence of a version mismatch or an ambiguous referent, investigate available document history or prior correspondence and state any unresolved interpretation; do not invent the historical wording or claim confirmation of a materially different proposal. Missing version metadata alone does not invalidate ordinary feedback.

A grouped **No response given** list, an older UNANSWERED entry with no comment, or an omitted item supplies no decision: keep its assumption and confidence unchanged, without inferring approval, disagreement or whether it was read. A comment without a button selection is still feedback and must be classified by its words. Change with no explanation records an incomplete response, not a supplied correction or confirmation. Preserve qualifications in comments accompanying Confirm; the selected button never overrides what the reviewer wrote.

### 1. Catalog the Feedback

For each item in the stakeholder response, classify it:

| Classification | Meaning | Action |
|----------------|---------|--------|
| **Confirmed** | Explicit "correct" or equivalent | Mark VALIDATED, move to PRD |
| **Corrected** | Supplies the answer: "wrong, do X instead" | Update assumption with correction |
| **Pushback** | Withholds the confirm without giving an answer: a doubt, concern or question | Research it; resolve at ≥95%, otherwise restate the assumption to meet it and keep pending |
| **Partial** | Some info provided, gaps remain | Update what's known, assume the rest |
| **Unclear** | Gives an answer that can be read more than one way | State your interpretation, keep as pending |
| **No response** | Item wasn't addressed | Keep existing assumption |

**Classify by what the words say, not by the box ticked.** Review packages offer only Confirm and Change, so every doubt comes back marked Change (`stakeholder-review-package`), and an emailed "Wrong" is often followed by a question rather than an answer. A response is **Corrected** only when it supplies the answer — what to do instead. A Change that asks, hedges or raises a concern is **Pushback**. One reply can hold both ("use ship date — not sure about returns, though"): process each part under its own class.

**Feedback on acceptance criteria or mockups is classified the same way.** A review package exports it separately from the assumption answers, labelled with its section (`stakeholder-review-package`). It answers no assumption, so there is nothing to mark validated. A stated change is a change to the requirement itself: Step 1a decides whether it amends this PRD or goes to a follow-on, and Step 5 applies it. A doubt or question is researched like Pushback, against the criterion or screen it names; if research stays below 95%, open a new assumption (Step 3), or bring back the original ID when the criterion came from a ruling the stakeholder gave (`assumptions-document-writing`, "When an answered item may sit in the body at all"), stating the answer the criterion now rests on, with a "Why your [date] answer didn't close this" section quoting their words, so it goes back to them next round.

### 1a. Sort Each Change: Fix or New Ask

Feedback often arrives after much of the PRD is built, and it mixes corrections with requests for things the PRD never set out to do. Folded into the PRD together, the requests turn a build that was nearly done into one that is barely started, and the new functionality never gets its own mockups, assumptions or stakeholder review. This step keeps every request and sends each to the place that can build it cleanly.

Every answer that changes what gets built (a Corrected item, a Pushback or Partial item whose research changed the answer, a stated change to a criterion or mockup) is one of two kinds. Judge it against what the PRD set out to deliver, its Summary and Business Context:

- **Fix:** it makes the PRD deliver what it already set out to deliver. A clarification, a rule we got wrong, a case the stated outcome plainly needed and the criteria missed. However large, a fix amends this PRD.
- **New ask:** it adds an outcome the PRD did not set out to deliver, or reverses something the PRD explicitly decided or excluded. The surest sign is a request that contradicts an Out of Scope line or a ruling the PRD records.

Confirmations and items with no response change nothing and need no sorting. One reply can hold both kinds; sort each part.

**First, find where each change already lives**, across everything Step 0 loaded, as it stood before this feedback. When an earlier pass (this chat's or another session's) already folded some of the feedback into the documents, read them at the commit before that pass (its commits name the feedback or the saved reply): an amendment already in the text hides where the capability was planned before. Build state and what is under way still come from the documents and checkouts as they stand now. Each change is one of five:

- **This PRD's own requirement**, corrected or clarified: sort it below as a fix or a new ask.
- **Planned in, or within the stated outcome of, another PRD:** feedback on that PRD. Apply this step to it as that PRD's, with that PRD's build state, and record it there: in its PRD, or in its scope entry in the PRD contracts while it is still planned. When the stakeholder needs it sooner than that PRD delivers it, or inside this PRD's screens, ownership moves earlier (below).
- **Considered and set aside:** in the brief's deferred list or open questions, or an Out of Scope line that names no other PRD. A new ask, sorted below against the PRD whose Out of Scope line set it aside; a deferred-list item or open question is sorted against this PRD. In the same change, take it off the deferred list or assign the question, and update its coverage-matrix row, naming where it went.
- **An extension of behavior a PRD already delivers** (widens a case, moves an automation boundary, replaces a rule): a change to that behavior's owning PRD, sorted as a fix or new ask against that PRD, never a new capability alongside the old one.
- **Absent from the initiative:** genuinely additional. A new ask, sorted below.

For each, note the owning PRD, how far its build has got and what depends on it before writing any requirement or phase. A home that already exists beats a new follow-on, and an Out of Scope line in this PRD is not by itself a reason for one.

**When ownership moves earlier.** Build the capability once. When the later PRD has already built it, or a phase under way is building it, or the new owner cannot sit ahead of it in the order, nothing moves: the ask is a change to that PRD. Otherwise, in the same change: move its criteria from the later PRD to this one (or to this PRD's follow-on, by the rules below), retire them in the later PRD with a note naming where they went and take them off its unstarted phases, or take them out of its scope entry while it is still planned. Update the rest as `initiative-breakdown` requires for scope moving between neighbors ("Keeping the Initiative Current"): contract and seam lines, the later PRD's **Depends on:** line, question assignments and the coverage matrix. Move any pending assumption about the capability to the new owner's register, or, for a follow-on not yet written, name it in its **In this PRD:** line for its PRD to carry. The later PRD keeps, or gains, only the criteria that connect its own outcome to the capability.

**Where a change lands depends on whether this PRD's build has started.**

| This PRD's build | Fixes | New asks |
|---|---|---|
| Not started | Amend this PRD | Amend this PRD. This is still requirements work; the size check in `prd-writing-standards` re-cuts it within its initiative if it outgrows the band |
| Started | Amend this PRD; Step 6 gives the work a place in the plan | Amend this PRD only when the ask is minor (below); otherwise send it to the follow-on |

**The build has started** when a phase plan for the PRD is committed, any of its phases has a `**Closed:**` line, or a commit or session log (`implementation-lifecycle`, "Session Markers") shows code being written for it. Look on the shared branch, in every checkout `git worktree list` shows, and in each checkout's `.agent-sessions/` logs. Nothing is published when a build starts, so a build on another machine can be invisible. On a split PRD a wrong guess costs little: a new ask folded into a PRD whose build was under way elsewhere sits in no phase, or in one already closed, and `delivery-audit` finds it unbuilt when the PRD closes and adds a completion phase for it. An unsplit PRD has no such backstop, because `delivery-audit` skips it by default, so when the evidence for one is unclear, treat its build as started.

**A new ask is minor**, and amends this PRD even after its build started, only when all four hold:

1. It serves the PRD's existing stated outcome and reverses nothing the PRD decided or excluded.
2. It needs no new screen and no new assumption for the stakeholder.
3. It changes no other PRD's criteria.
4. The round's minor asks together fit in one phase (`phase-split`, "Session Capacity Calibration"). When they don't, none of them is minor.

**A new ask that reverses behavior this PRD defines**, once its build has started: the follow-on builds the replacement, and these rules, in order, decide what happens to the old behavior in this PRD:

1. **Not built yet:** don't build it. Retire the criterion (`prd-writing-standards`, "Stable Acceptance-Criterion Labels") with a retirement note naming the follow-on, and take it out of its phase. When this PRD cannot deliver its stated outcome without that behavior, pull the replacement into this PRD as a fix instead.
2. **Built, and it leaves nothing behind for the replacement to clean up:** it ships as built, and the follow-on replaces it. Something left behind means stored records the replacement must migrate or reconcile, writes to other systems, people's work the replacement makes pointless, or an output other systems will start to depend on.
3. **Built, and it leaves something behind:** switch it off. That is a fix to this PRD: amend the criterion to say the behavior is not available until the follow-on replaces it, and Step 6 routes the work. When switching it off leaves this PRD unable to deliver its stated outcome, pull the replacement into this PRD as a fix instead.

**A removal with nothing to replace it** ("drop the PDF export") needs no follow-on, because there is nothing new to build. Retire the criterion with a note citing the feedback; if the behavior is already built, amend the PRD to remove it, and Step 6 routes the removal like a fix.

**The follow-on.** Every new ask that is not minor and has no other home goes to one follow-on PRD:

- **One open follow-on per PRD.** A follow-on is found by its `**Follow-on to:**` line naming the PRD it follows: under its PRD's H1 once written, in its PRD contracts entry or scope file before that. If this PRD already has a follow-on whose build has not started (the same test as above), the asks join it, as amendments to its PRD once that is written. Otherwise create one. One round never creates more than one follow-on for a PRD.
- **Keep the stakeholder's words.** Whenever a reply carries attachments, feeds a follow-on or changes another PRD, including a reply whose changes all stay in this PRD, save it exactly as received, with any mockups or files attached to it, in `source-material/{source}-feedback-YYYY-MM-DD/`, where `{source}` names who sent it (the stakeholder or their team), unless the repository already keeps it. Like any handoff material, it is never edited and never sits inside a PRD's directory (`prd-writing-standards`, "Mockups Show What the Criteria Require"). The follow-on's scope names its path, as plain text rather than a link, so the session that writes the follow-on works from the stakeholder's words and pictures, not a paraphrase.
- **In an initiative:** add the follow-on as a row in the PRD list and an entry in the PRD contracts, in the formats `initiative-breakdown` defines (Step 5), with status `planned`. Give it a title that says what it delivers, and put it right after this PRD in the order, ahead of any planned PRD whose criteria it changes (the conflict check in `implementation-lifecycle` finds those), but never ahead of a PRD it depends on. Its **Follow-on to:** line names this PRD, and its **Depends on:** line names this PRD and every other PRD it needs. Its **In this PRD:** line names each ask in a few words and points at the saved feedback. A **Changes:** line names each criterion of this or another PRD that it changes, by label, so its PRD can carry the `Replaces:` lines.
- **Outside an initiative:** create a change directory, `docs/changes/{name}/`, holding one file, `{name}-follow-on-scope.md`, with the same lines as a PRD contracts entry. The chat that writes the PRD deletes that file in the commit that writes the PRD.
- **Not written here.** Writing the follow-on's PRD, with its mockups and assumptions, is a session of its own. This chat ends with the prompt for it (Step 8).

An assumption whose answer went to the follow-on or another PRD leaves this register as a row in the Validated Assumptions table that names that PRD, where the answer now lives.

**Every call in this step is the session's.** Make each one yourself, from the documents and the code, and record it in one line of the report (Output Format, item 9). Never stop to ask the user to choose: the session can see the documents, the code and the other work in flight, which the user can't without a long conversation. A wrong call costs one more round of feedback to correct.

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

#### Pushback Items

Pushback withholds the confirm without supplying the answer: a doubt ("not sure this is right"), a concern ("what about drop-ship orders?"), or a question. It is a signal, not an edit instruction. **Never paste their words in as the new assumption** — a question is not an answer, and a concern is not a correction.

1. **Read it as a clue to why they couldn't confirm.** What would have to be true for them to hold back — a case the assumption misses, a risk they see, a fact they know and we don't, or a statement they read differently than we meant? Write that reading down; the rest works from it.
2. **Research it** to the standard of Step 7: code, data, the PRD and design, transcripts and emails, and their other answers in the same batch, which often say what this one only hints at.
3. **Research reaches ≥95%** — the answer their concern pointed to, or evidence the assumption already handles it: the item is resolved. Fold it into the requirements (Principle 4) and move it to the validated table, whose row says what answered their concern. Name it in the report, so the stakeholder sees their question was taken up, not overruled in silence.
4. **Research stays below 95%**: restate the assumption in the best form the evidence supports, written so it answers their question or meets their concern — usually a clause or a changed example, not a longer entry (Principle 6). Set confidence honestly: a concern that exposed real doubt is cause to lower it (Principle 5). Add the "Why your [date] answer didn't close this" section quoting their words and saying how the restated assumption takes them up, and tag the heading `we read your words` (`NEW SINCE YOUR ANSWER` if the research found something that changed the answer). It stays pending and goes back to the stakeholder next round.

**The same path, whoever wrote it.** A pasted stakeholder reply and the user's own typed reaction look alike, so don't try to tell them apart, and don't stop to ask the user what a pushback means before applying it. Research, restate, and report how you read each one (Output Format, item 8). If that reading is wrong, the user says so in their next message, and that is simply another round of feedback.

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
- Move each item whose answer went to a follow-on or another PRD (Step 1a) to the Validated Assumptions table the same way, naming where the answer now lives

### 4a. List Every PRD the Round Reaches

A change reaches more than the PRD that owns it. When it alters something one PRD owns and others consume (a shared record, a rule, a status vocabulary), every consumer already written has to change too, or it is designed and built against a contract that no longer exists. Step 1a found each change's owner; this step finds its consumers, so the round finishes every PRD it reaches.

1. **Find the consumers.** For each change that landed in this PRD, another written PRD or a planned PRD's scope entry: every PRD on the receiving side of a Seams-table row whose contract it alters ("What crosses the seam" or "What the later PRD may assume"), and every PRD or change directory whose criteria or design cite a criterion it changed (search for the labels). Outside an initiative, the label search alone. A change sent to a follow-on reaches no consumer yet: the source PRD still ships the old behavior, and the follow-on's **Changes:** line and the conflict check carry it to its consumers when the follow-on is written. Update each altered seam row now, in the PRD contracts, and any line of a planned PRD's entry that restates the old contract. A minor ask (Step 1a) that turns out to reach another written PRD's criteria fails the minor test: sort it again.
2. **Decide what each needs.** A consumer still `planned` needs nothing more: its entry and the seam row are what its PRD will be written from. Every written PRD the round reaches, this one, the owner of a change (Step 1a) or a consumer, gets a list of what it must now say: each change, by criterion label or seam row, and what it means for that PRD. Edits an ownership move (Step 1a) makes to a written PRD go on its list too, so one writer makes all of them. Apply Step 1a's build-started test to each, with the same evidence, and record what it found: one whose build has started also goes through Step 6 for any code the change needs.
3. **Write each list down before amending anything,** as a block in `{name}-pending-feedback-changes.md` in that PRD's own directory:

```markdown
# Pending feedback changes: {PRD title}

## From {source PRD title} stakeholder feedback, YYYY-MM-DD

**Reply:** {where the reply is saved}
**Base:** {the commit the round started from}
**Stage it had reached:** {e.g. design refined, not yet split into phases}
**Build:** {not started | phases closed: …; under way: …}
**Status:** not started | amended, check pending | needs a chat of its own
**Why a chat of its own:** {only with that status: the design decisions the round did not make}

- {change, by criterion label or seam row}: {what this PRD must now say}
```

When the PRD already has a pending file, add this round's block below the ones there; never replace one. The file is how any session that opens the PRD sees that its documents are about to change, and how this skill resumes ("Resuming", below). A block is removed in the change that finishes its PRD for that round (Step 5a), and the file goes with its last block.

4. **Size each list.** Almost always the PRD is finished **in this round**: it only consumes what the round decided, restating criteria against the new contract, dropping what the upstream now provides, redrawing the screens that show it. How many PRDs the round reaches, or how long a list is, is never a reason to stop: each PRD's writer and reviewer work in their own context, and this chat reads only their reports. A PRD needs **a chat of its own** only when it must make design decisions the round did not make, such as a new data model, interface or flow of its own; name them on the block's **Why a chat of its own:** line. That is usually plain from the list; otherwise Step 5a's check finds it.
5. **Check that no other session is working on the PRD** before its writer starts: a refinement state file in its directory, uncommitted changes to its documents in any checkout `git worktree list` shows (other than the pending file this round wrote), or a live session log naming it (`implementation-lifecycle`, "Parallel Sessions: Where to Work"). If one is, leave its block `not started` for that session, whose skill applies pending changes first, and name it in the report. This round's own session log names every PRD it holds a block for, so a later session can tell the round is still at work on it.

**Resuming.** When this skill runs on a PRD whose directory holds a pending file and no new reply came with it (a rerun after an interruption, from the map, from `phase-split` or `implement-from-requirements`, or as a chat of its own), the feedback is already interpreted: skip Steps 0a to 4 and work from each block, oldest first, with that PRD as the subject; where two blocks change the same criterion, the later one wins. When a new reply came too, finish the existing blocks this way first, then process the reply from Step 0. Start each block with item 5's check: when the round that wrote it is still live, leave the block to it. Rerun Step 1a's build-started test and update the **Build:** line, since the build may have moved on since the block was written. Load the reply its **Reply:** line names, the upstream criteria and seam rows its list names, and the PRD's documents, then act on its **Status**. `not started` goes to the writer (Step 5) and `amended, check pending` to the check (Step 5a). `needs a chat of its own` goes to the decisions first: this chat makes each one the **Why** line names, researching it (Step 7), writing it into the design under `technical-design-writing-standards` and recording any business call below 95% as an assumption, then sends the block to the writer and the check like any other. Neither refinement runs here either. Finish with Step 8.

### 5. Propagate to Implementation Documents (CRITICAL)

**This step is essential and must not be skipped.** Every decision this skill settles or changes must be reflected in the actual implementation documents—otherwise the assumptions document becomes a dead end.

For each decision this skill settles or changes, at any confidence: a validated or corrected item, a resolved Pushback, a stated change to a criterion or mockup, and an assumption added or restated with a different answer (below 95% the PRD still states the answer it rests on, citing the entry's ID, per `prd-writing-standards`). A reopened stakeholder ruling is the exception: the PRD, its mockups and the Technical Design keep the stakeholder's decision until the stakeholder revises it (Principle 5). The documents are this PRD's only for what Step 1a kept here, including a criterion it retired or switched off. A new ask sent to a follow-on goes into the follow-on's scope, never into this PRD; an ask sent to another PRD is propagated into that PRD's documents, and so is every line of a pending block (Step 4a).

**Who writes each PRD's changes.** This chat amends this PRD itself. Each other PRD with a block to finish in this round gets one writer subagent, launched by this chat, given that block, the amended upstream criteria and seam rows it names, and that PRD's documents. The writer applies items 1 to 5 below and Step 6 to that PRD, under its writing standards, with the block's **Build:** line as Step 6's evidence. Then the block's **Status** becomes `amended, check pending` when Step 5a calls for a check; otherwise the PRD is finished and its block is removed. Writers on different PRDs can run side by side. The initiative's shared files (PRD list, PRD contracts, coverage matrix) are edited by this chat alone, so no two writers touch one file. A writer launches no subagents of its own: every subagent in the round is launched from this chat, one level deep.

1. **Identify affected documents**: Which documents reference this decision?
   - PRD: Business decisions and acceptance criteria
   - Technical Design: Implementation details, field mappings, business rules
   - Field Mapping docs: If the correction changes data sources or logic
   - Mockups: If the decision changes what a screen shows

2. **Update the PRD**:
   - Fold the decision into the requirement it settles (an acceptance criterion, Summary or Business Context), stated as the requirement itself. If that criterion carries a `Superseded by:` line covering what the ruling settles, a later-built PRD changed that behavior on purpose: do not fold, and name the conflict between the ruling and the later PRD in the report, for the user to settle with the stakeholder. If it is only partly superseded and the ruling concerns the part still in force, fold into it as usual (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion")
   - Update acceptance criteria if the correction changes what "done" looks like
   - Note the source/date of validation for traceability

3. **Update the Technical Design**:
   - Update implementation logic if the correction changes how something is built
   - Update data mapping sections if sources or transformations changed
   - Add implementation notes for nuances from the feedback

4. **Update Field Mapping documents** (if applicable):
   - Update SQL queries, field sources, or business logic

5. **Draw or redraw affected mockups:**
   - Draw or redraw every mockup state the decision changes, in the same change as the PRD edit, even when the PRD had no mockups before. Start from any mockup the stakeholder supplied, after saving the original under `source-material/` (Step 1a, "Keep the stakeholder's words"), otherwise from the latest drawing of the screen or the screen as built (`prd-writing-standards`, "Mockups Show What the Criteria Require"). A decision that changes no screen needs none

**Why this matters**: The assumptions document is a working document that eventually gets emptied. If you only update assumptions without propagating to PRD/Tech Design, the validated decisions are lost when the assumption is removed. The PRD and Technical Design are the permanent records.

**Checklist for propagation**:
- [ ] PRD updated with validated decisions
- [ ] Technical Design updated with any implementation changes
- [ ] Field mapping docs updated if data sources/logic changed
- [ ] Mockups drawn or redrawn wherever the decision changed what a screen shows
- [ ] All documents have consistent information (no contradictions)

### 5a. Check Each Amended PRD Once

An amended PRD needs one fresh check, not its refinement again. `autonomous-prd-refinement` and `autonomous-design-refinement` take a draft to ready over many passes; an amendment changes a bounded part of documents that were already ready, to match decisions this round has already made. Never rerun either on a PRD this round amended: the stage it had reached stays reached.

- **Which PRDs:** every PRD this round amended whose documents had been refined, this one included. A PRD still in draft gets no check: its own refinement will read the amendment, and it is finished once its writer is done.
- **The check:** this chat runs `deliverable-review` for each PRD, launching its one reviewer subagent, scoped like a delta round ("Delta Rounds") with the PRD's diff since the block's **Base:** commit as the change. The reviewer gets the block's list as the decisions the work had to carry out, the upstream criteria and seam rows it names, and that diff. It reads the diff in full and everything that shares a term, rule or interface with it, and renders only the screens that changed. It asks two questions. Does the PRD now agree, everywhere, with the decisions and contracts it consumes? Would someone building the changed parts have to make a judgment call the documents leave open? The second is the test in `autonomous-design-refinement` ("The Scope Gate"), which also keeps the check from adding scope.
- **The fixes:** a new writer subagent for that PRD, or this chat for this PRD, fixes each finding. A technical question is researched (Step 7); a business call below 95% becomes an assumption in that PRD's register.
- **At most one more check,** a delta round over the fixes, and only when they changed a rule or an interface. This bounded check is not a review loop, so it does not end on a full round: what a third pass would find, that PRD's phase planning and build find and settle in their own sessions, and `delivery-audit` catches what they miss.
- **When the check finds design decisions** the round did not make and its fixes cannot settle, set the block's **Status** to `needs a chat of its own` and name them on its **Why** line; Step 8 hands it off.
- **Finishing a PRD:** once its fixes are in, refresh its review package when Step 8 calls for it, and remove its block in the same change.

### 6. Give the Work a Place in the Plan

**This step applies only to changes that change what the code must do, in this PRD or in another PRD Step 1a or Step 4a reached.** For a change sent to another PRD, apply it to that PRD's plan and build state. Confirmed assumptions that validate existing behavior, blockers that remain blocked, and items the code already handles correctly need nothing here.

A PRD of any size is built one phase at a time, and each session builds what its phase lists, not the whole PRD. So once the build has started, an amended criterion with no place in the plan goes unbuilt. Where the work goes depends on how far the build has got:

- **Build not started:** the amendment in Step 5 is enough. Phase planning reads the amended PRD.
- **Build started, planned phases still open:** each change goes into the next open planned phase whose build has not started, under a `## Carried forward from stakeholder feedback, YYYY-MM-DD` section, one line per change, saying what changed and pointing at the amended criterion. Never edit the document of a phase a session is building: the session has already loaded it and would close the phase without the change. Step 1a's evidence (worktrees and session logs) shows which are under way. A criterion an unstarted planned phase already owns stays with that phase, and its line goes there instead. A new criterion (a minor ask, or a fix that adds one) goes to the first unstarted planned phase that can build it and is listed in that phase's "Acceptance criteria covered", so every criterion is still in exactly one phase (`phase-split`). A criterion retired under Step 1a comes off its phase's list; if that phase is under way, its session will build the behavior anyway, so treat it as built (Step 1a, rules 2 and 3). Fixing here, rather than at the end, keeps later phases from building on behavior already known to be wrong. A phase that outgrows a session is re-split by `phase-split`. When every open planned phase is already under way, use a feedback phase, as below.
- **No unstarted planned phase left** (every planned phase closed or under way, or an unsplit PRD whose build has started): append feedback phases to the end of the plan in `phase-split`'s form ("Completion Phases"), marked `**Added by stakeholder feedback:**`, and sized by `phase-split`'s Step 2. Usually one is enough. A feedback phase from an earlier round whose build has not started takes the new changes instead of a second one being added. An open completion phase an audit added is never a destination.

**Checklist:**
- [ ] Every change that needs code is in the amended PRD that owns it and, once that PRD's build has started, has a place in its plan: an open phase's carried-forward section or a feedback phase
- [ ] No item is described as scheduled, tracked, or "will be done" unless a build will read it

### 7. Research First (New Assumptions Below 95%, and Pushback)

This step applies when Step 3 produced new assumptions below 95% confidence, and to every Pushback item (Step 2). **Investigate each one before finalizing it**, as `implementation-lifecycle` requires — code, data, documents, the stakeholder's own written feedback. The research decision is part of the work; don't hand it to the user.

Then set each entry at the confidence the investigation leaves it at: at 95%+ it folds into requirements, below that it stays a pending assumption and work proceeds on it, and only when the evidence favors no answer at all does it become a Blocking Open Question. Report what moved in one line each: the assumption, its confidence before and after, and what settled it.

### 8. Hand Off

**The round is finished only when every PRD it reached is.** Each carries its changes and has had its check where Step 5a calls for one, and no pending block from this round is left apart from one that needs a chat of its own or was left for a session already working on that PRD (Step 4a). Never end on a sentence saying another PRD "needs alignment", "should be updated" or "will need review": the change is in its documents, or it is in a pending block with a prompt below or a session already on it. If this chat stops before then, running this skill again in the same checkout resumes from the blocks that are left (Step 4a, "Resuming").

When this round drew or redrew a mockup for a change kept in this PRD or sent to another written PRD, refresh that PRD's stakeholder review package first (for another PRD, after its check, by the writer that made its fixes, or by a writer launched for the refresh when the check found nothing), or create one if none exists, unless the user declined it (`stakeholder-review-package`), so the stakeholder sees how their feedback will look. Nothing waits on their reply.

End with a prompt for each new chat this round needs, written with `continuation-prompt` and shown in full in the report, so the user knows exactly what to start:

- **A follow-on was created, or got new asks, and its PRD is not written yet:** a prompt to write it (`prd-writing-standards`). Writing it doesn't wait for this PRD's build: its stakeholder review can go out while this PRD is still being built.
- **Feedback phases were appended to a finished plan:** a prompt to build the first one (`implement-from-requirements`).
- **A PRD's pending block needs a chat of its own** (Step 4a or 5a): a prompt to finish it, with this skill resuming from that file, stated as the outcome ("make {PRD title} ready for its next stage against the amended contracts"). The decisions and the list it works from are in the block, not the prompt.

Otherwise no prompt is needed: an open plan's next session picks up its carried-forward sections, and an unstarted PRD carries on along its usual sequence of documents. Every other PRD the round reached is back at the stage it had reached, and its own track carries on from there; its next stage is not a prompt from this round. When a session is already writing the follow-on (its session log shows it), write no second prompt; name the asks its scope gained, for the user to pass to that chat.

The prompts point at documents this chat changed, so present the commit for them first and label each prompt as valid once it lands (`continuation-prompt`, Step 5).

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

## Example: Processing Pushback

**Original Assumption:**
> Refunds issued more than 90 days after the order are left out of the monthly returns report.

**Feedback** (review package, marked Change):
> "What about store credit? Not sure we treat those the same."

**Processing:**

1. **Classification**: Pushback — marked Change, but it asks; it doesn't say what to do instead. Rewriting the assumption as "store credit is included" would invent an answer they never gave.
2. **Read it as a clue**: they suspect store credit follows a different rule from cash refunds, and the assumption doesn't say which kind it covers.
3. **Research**: the refunds table records the refund method, and store credit is a third of late refunds. The finance close procedure (2023) books store credit as a liability when issued, not as a refund. That points to leaving store credit out at any age — 80%, since the procedure may be out of date.
4. **Restate**, still pending, tagged `we read your words`:

> **Assumption**: **Cash and card** refunds issued more than 90 days after the order are left out of the monthly returns report. **Store credit is left out at any age** — finance books it as a liability when issued, not as a refund.
>
> **Why your 2026-03-12 answer didn't close this**: You asked whether store credit is treated the same ("What about store credit? Not sure we treat those the same"). We read that as store credit possibly following its own rule. The finance close procedure says it does, so the assumption now names each kind separately. Confirm that is how finance treats it today.

## Example: Feedback After the Build Has Started

**State:** the Customer Returns PRD has six phases; 1 to 4 are closed, and no session is building 5 or 6. AC-RET-05 says a return is always refunded, and its Out of Scope says "No exchanges." It is a planned PRD in an initiative.

**Feedback**, in one reply:
> "Restocking fee should be 10%, not 15%. Show the fee on the confirm screen, not only the receipt. Customers must also be able to exchange for another size. And returns staff should get a daily export."

**Sorting (Step 1a):**

1. **10% restocking fee:** a fix, the rule was wrong. Phase 2 built it, so the change goes into phase 5 under "Carried forward from stakeholder feedback".
2. **Fee on the confirm screen:** a new ask, and minor. It serves the stated outcome (customers understand their refund), changes an existing screen rather than adding one, needs no new assumption, and fits well within a phase. It becomes a new criterion owned by phase 5.
3. **Exchanges:** a new ask that reverses an explicit exclusion, so it goes to the follow-on. The refund-only flow is built, and shipping it leaves nothing for exchanges to clean up, so it ships as built.
4. **Daily export:** an outcome the PRD never set out to deliver. The initiative's planned Returns Reporting PRD covers exports for staff, so the ask goes into that entry's scope, not the follow-on.

**Result:** one follow-on, *Customer Exchanges*, added after Customer Returns in the initiative's order. Its **Changes:** line names AC-RET-05, and the stakeholder's reply is saved under `source-material/`. The confirm screen's mockup is redrawn with the fee, and the review package is refreshed. The report gives one prompt, to write Customer Exchanges. Phases 5 and 6 still finish Customer Returns on the scope it started with.

## Example: A Change Another PRD Consumes

**State:** the stakeholder corrects Customer Returns: the restocking fee is a line of its own on the refund, not netted from it. That is a fix. The Seams table has a row "Customer Returns → Returns Reporting, Refund Notifications: the refund record". Returns Reporting is written, its design refined, not yet split into phases; Refund Notifications is still `planned`.

**The round:**

1. **Step 4a:** the seam row now says the fee is a separate line. Refund Notifications needs nothing more. Customer Returns and Returns Reporting each get a pending block; Returns Reporting's has one line: refund totals read the fee line, and the refunds screen shows it. It only consumes what the round decided, so it is finished in this round.
2. **Step 5:** this chat amends Customer Returns; a writer subagent amends Returns Reporting's criterion, its design and its refunds-screen mockup.
3. **Step 5a:** Returns Reporting's check finds two things: its design's export still lists one amount column, and nothing says how refunds recorded before the change are shown. A new writer fixes the export and adds an assumption for the old refunds (shown netted, and labelled so). That assumption sets a display rule, so one more check runs over the fixes and finds nothing. The writer refreshes the review package and removes the block.

**Result:** the report lists Returns Reporting as changed and checked, still at phase planning, and names the seam row for Refund Notifications. No prompt for either: Returns Reporting's own track carries on when the user starts its phase planning.

---

## Output Format

After processing feedback, provide:

1. **Summary of Changes**: Brief overview of what was updated
2. **Items Now Validated**: List any assumptions that can be marked complete
3. **Items Updated**: List assumptions that were modified with what changed
4. **New Assumptions Made**: Any assumptions created to fill gaps from partial/unclear feedback (with confidence levels). These are NOT questions — they are implementable decisions.
5. **Updated Assumptions Document**: The revised assumptions document
6. **Propagation Summary**: List of changes made to PRD, Technical Design, mockups and other implementation documents, and what this PRD's check found and fixed (Step 5a)
   - What was added/updated in each document
   - Location of changes (section names or line references)
7. **Code Changes Routed**: for each item that now needs code, where it went, in whichever PRD owns it: the amended PRD a build will read, an open phase's carried-forward section or "Acceptance criteria covered" list, or a feedback phase (Step 6)
8. **Research Done** (only if Step 7 investigated new assumptions below 95% or Pushback items): one line per assumption — confidence before and after, and what settled it; for Pushback, also how you read their concern and whether research resolved it — plus any Blocking Open Question with what would let you decide
9. **Routing** (Step 1a): whether this PRD's build has started and what that was read from; then one line per change: where it already lived (this PRD, another PRD by name, deferred or an open question by label, an extension of named behavior, or absent), its owner and how far that owner's build has got, fix or new ask, where it went (this PRD, another PRD by name, or the follow-on by name) and, for a reversal, what happens to the old behavior and why. Then the round's added work for the stakeholder in three parts: net additional scope (naming any the initiative had deferred), work brought forward from another PRD, and rework of what was specified or built. Added phases are never described as new requests. Decisions, not questions
10. **Other PRDs reached** (Steps 4a and 5a): one line per PRD that changed, other than this one: why it was reached (owner of a change, or consumer by a named seam row or criterion label), what changed in it, what its check found and fixed, and its stage, unchanged; or that it needs a chat of its own, and why, or was left for a session already working on it. A consumer still `planned` gets its seam row named and nothing more. PRDs the round did not reach are left out
11. **Next chats** (Step 8): each prompt in full, or "none needed" with the reason

**Propagation Checklist** (include in output):
- [ ] PRD updated with validated decisions
- [ ] Technical Design updated with implementation details
- [ ] Field mapping docs updated (if applicable)
- [ ] Mockups drawn or redrawn wherever a decision changed what a screen shows, and the review package refreshed (Step 8)
- [ ] All documents now consistent
- [ ] Every change checked against the whole initiative before the feedback, sorted as a fix or a new ask, and in exactly one place: this PRD, another PRD, or the follow-on, with no capability owned by two PRDs (Step 1a)
- [ ] Code changes routed per Step 6 (amended PRD, carried-forward section, or feedback phase)
- [ ] Every written PRD the round reached, as owner or consumer, carries its changes and had its check where Step 5a calls for one, with no refinement rerun; no pending block from this round left except one with a prompt or a session already on it (Steps 4a, 5a, 8)
- [ ] A prompt for each next chat (Step 8)
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

---
name: requirements-intake
description: First step when the material handed over is raw — meeting transcripts, long email or chat threads, earlier AI sessions, notes, documents or code from a prior attempt, or a large mixed pile of them. Brings the stakeholders' own material, and any prototype or earlier code, into a quarantined source-material/ folder with every file marked as unvetted reference, and leaves the rest of the pile out. Then reads all of it, separates what the business stakeholders actually decided from discussion, exploration and text no stakeholder said or chose, keeps the latest position on each topic, and writes one requirements intake record built on the stakeholders' own words, quoted, with every source cited. The PRD (prd-writing-standards) or the initiative breakdown is then written from that record instead of the pile. Skip it for a written brief or an email or two.
user-invocable: true
---

# Requirements Intake

Turn raw source material into one record of what the business decided, in the stakeholders' own words. The skill works in two parts: Part 1 brings the material worth keeping into the repository, quarantined and marked as reference; Part 2 reads all of the material and writes the record. `prd-writing-standards`, or `initiative-breakdown` when the work is bigger than one PRD, then works from that record.

## Why This Exists

Requirements rarely arrive as a clean brief. They arrive as two-hour meetings where a topic comes up three times and the answer changes, email threads where a decision sits in a one-line reply, chat sessions where someone thought out loud, and, more and more often, documents and code an AI produced in an earlier attempt at the same work, some of it answered and much of it not. The writing skills that follow assume their input says what the business wants. Raw material does not, yet. It says that and a great deal else, and nothing in it marks which is which.

Handed raw material directly, a PRD inherits its noise. Exploration becomes a requirement, an early position that was later reversed survives, an AI's proposed rule reads like the stakeholder's own, and conflicts the material settled elsewhere come back to the stakeholder as questions. The larger the pile, the worse this gets. This skill does the sorting first, once, where it can be checked.

## When to Use

Run it before the first draft of the PRD, or of the initiative breakdown when the work is bigger than one PRD, on the business context that draft will be written from: everything the business has said, written or handed over about what it wants, however it arrived. It turns that context into the one input the draft is written from. Use it when that material is raw:

- One or more meeting transcripts, especially long, conversational ones.
- Email, chat or ticket threads with decisions scattered through the replies.
- Earlier AI chat sessions, or documents or code produced in an earlier attempt at the same work.
- A mix of these, or anything too large or too tangled to read as one statement of intent.

Skip it, and go straight to `prd-writing-standards`, when the input already states intent: a written brief, a short email or two, notes the user wrote for this purpose, or an existing PRD being revised. Once a PRD exists, new material about it goes to `assumptions-document-feedback` or `implement-from-discovery`, not here. Raw material that arrives before the PRD is written extends the existing record (Step 10).

**Effort.** Run this skill at a very high reasoning effort, above the usual high setting. It runs once per piece of work, its record is the only thing later skills read, and a decision it misses or a reversal it gets wrong is invisible from there on. The judgment calls (which position stands, whose words count, what is a decision at all) are where the effort pays. Every subagent it launches runs at high effort or above. It needs no exhaustive or multi-agent mode: what splitting large material needs is in Step 4.

*Operator note:* a skill cannot change the session's effort. Start the session for it at a very high effort level.

## What It Produces

Two different kinds of thing, kept apart so that nobody, person or AI, mistakes one for the other:

- **What was received.** The material the business handed over that is worth keeping, copied into the repository with nothing changed but a short reference-only note at the top of each file. Nothing in it is vetted, nothing in it is a requirement, and none of its code is part of the application.
- **What this skill writes.** One file, the requirements intake record: what was decided, what conflicts and what is still open, each item carried by verbatim quotes from what was received. It is not a requirements document either. The PRD written from it is.

Both live under `source-material/` at the repository root, the one place for material received from the business. It sits at the root, not under `docs/`, because it is not documentation and can include code. Each piece of work gets one directory:

```
source-material/{name}/
  {name}-requirements-intake.md        ← the record (Part 2): the only file this skill writes
  received/                            ← what was received (Part 1), each file marked reference only
    2026-03-04-kickoff-meeting-transcript.txt
    2026-03-11-pricing-email-thread.txt
    reference-only-code-pricing-prototype/
      ...the code as received, its file names and layout unchanged
```

`{name}` is a short kebab-case name for what is being built, never for the kind of source ("kickoff-transcripts"). When the PRD or initiative name is already known, use it, and keep the directory's name if the PRD is later named differently. Later skills read the record and reach what was received only through its citations.

## The Rule That Governs Everything: Quote, Don't Summarize

The stakeholders' own words are the most valuable thing in the material. Every summary loses something: a qualifier, a condition, the example that showed what they meant, the word they use for the thing. So this skill reduces volume by **selecting** the stakeholders' words, not by rewording them.

- **Every decision, constraint, conflict and unresolved item carries at least one verbatim quote** from a stakeholder, with its source. A plain-English label sits above the quotes, one sentence at most. The quotes are the item; the label is only how a reader finds it.
- **Never let a paraphrase stand in for a quote.** An item no stakeholder said or chose is not a stakeholder decision (see "Whose Words Count").
- **Quote exactly**, typos and shorthand included. Trim a long quote with "..." only where the cut part does not change the meaning, and never trim a condition, an exception or an example. Correct a misheard or misspelled name in brackets, never in place: "the [Acme] portal".
- **Keep the examples.** When a stakeholder explained a rule through a real case (an order, an account, a date, an amount), quote the case. It is often the clearest statement of the rule there is. Replace a person's name or contact details in a quote with a bracketed role, "[customer]"; keep record numbers and amounts.
- **Keep their terms.** Where stakeholders call something by a name, the record uses that name. Note any other name the material uses for the same thing.

The record will be longer than a summary would be. That is the intent: it is far shorter than the pile, and nothing in it is a guess about what someone meant.

## Whose Words Count

Sort every source, and every passage inside a mixed source, by who wrote it:

- **A stakeholder's own words**: what a business owner, user or decision-maker said or typed, in a meeting, an email, a chat message or a comment. An email or message a stakeholder sent counts as their words even if a tool helped write it: sending it endorsed it. These are the primary material.
- **A stakeholder's choice among options someone else wrote**: an answer like "B", a ticked box, "yes, the second one", a choice marked on a mockup. This is a real decision. Record the stakeholder's words with the option text they chose, labelled "option chosen, wording not theirs". The decision is theirs; the wording is not.
- **Unendorsed text**: everything no stakeholder said or chose. Plans, rule sets, summaries, proposals, issue lists and question pages written by an AI or by someone without authority over the decision. It is context at most. A rule written there becomes a decision only where a stakeholder stated it or chose it, and an option nobody chose is nothing. Whether a document comes into the repository is a separate question (Step 2): an AI-written document can be well worth keeping as context and still decide nothing.

Names and roles are often missing: a transcript from a plain recorder may give no speaker names at all, and the material rarely says who decides what. Never invent either. Treat what is said in a meeting or thread with the business as stakeholders' words unless the material shows the speaker is not one (a vendor, a facilitator, an AI). Take authority from what is known (Step 1's list) and from what the material shows: who the group deferred to, who said "that's my call". A side comment from someone evidently outside a decision is context.

## Part 1: Bring the Material In

Part 1 decides what the repository keeps and copies it in. It does not decide what anything means; Part 2 does that, reading all of the material, kept or not.

### Step 1: Inventory the Sources and the People

List every source before reading any of it closely: what it is, where it lives (already in the repository, or handed over from outside), its date or date range, roughly how long it is, and whether stakeholders, an AI or both wrote it.

List the people the material names, as far as it or the user can say: each one's name or speaker label as the sources give it, and their role and what they decide where that is known. Gaps are normal; mark them unknown rather than guessing. A transcript with no speaker names still has an order, and that is often enough (Step 6).

Then ask the user, in one message, for what would help most (who the main stakeholders are, who owns which decisions, a speaker mapping when the user has one) and whether decisions live anywhere else: another thread, a meeting not yet transcribed, a chat channel. This is the only question the skill asks, and the PRD written from the record does not ask it again. Carry on without waiting for the answer; whatever arrives later is added as a new source or a correction to the list.

Across sources, dates decide the order. Use the date a statement was made, not the date a file was saved, wherever the source records it, and order an undated source by what it refers to or replies to. Some material has no usable date at all; record that, and do not assign one (Step 6 says what follows).

### Step 2: Decide What Comes In

Sort what was handed over from outside the repository:

- **The stakeholders' own material comes in, whole**: every meeting transcript, email thread and chat conversation with the business, every document a stakeholder wrote, every mockup or screenshot a stakeholder supplied. Transcripts come in complete, not trimmed to the parts that matter: when a question comes up later, the full account of what was said is there to go back to.
- **Code comes in, as reference**: a prototype, an earlier attempt at the same work, a sample someone handed over to show what they want. It can show behavior the business wants, or what did not work, and the record may cite it.
- **Everything else comes in only if it earns its place.** The trouble with a large pile is rarely who wrote it. It is that there is far too much of it, nobody can tell which parts are still right, and much of it is old. So whittle it down to the few documents worth keeping, whoever wrote them, an AI included:
  - **First, anything that carries a stakeholder's answer**: an option page where they marked their pick, a document they annotated or replied to. This is the most useful material in the pile, and the record's quote of the answer is checked against it.
  - **Then documents that give something the stakeholders' material does not, and are still current**: how the current system or process works, findings checked against the real system, domain rules, data or field mappings, real examples. Take the latest version, and where several cover the same ground, the clearest and shortest.
  - **Leave out** what later decisions superseded or contradict, drafts and duplicates, options and questions nobody answered, and an earlier attempt's working papers (plans, task lists, status notes, session logs).

  The test for each document is one line saying what it gives that nothing else kept does. If that line cannot be written, the document stays out; if it can, the line goes in the record's Reference Material. When the pile is too large to sort in one context, subagents can report that line, whether the document is current, and whether it carries a stakeholder's answer, per document, but the keep-or-leave call is made in one place. A document Part 2 finds it needs comes in then, the same way.

**Whatever its category, a file comes in only if it belongs in a Git repository.** Everything brought in stays in the repository's history for good, so leave out:

- Secrets: credentials, keys, `.env` files.
- Personal or customer data: data exports, database dumps, spreadsheets of customer records. Quote a record number from them in the record where it helps, but keep the file out.
- Large media and binaries: a recording, once its transcript is in, and archives, installers and disk images.
- Generated output: installed dependencies, build output, and an export of something also kept in its source form (an HTML wiki export of documents that came in as Markdown).
- An earlier attempt's tooling: AI agent instruction files (`AGENTS.md`, `CLAUDE.md`, rule and prompt files), agent, editor and tool settings directories, and the scripts and configuration that ran the earlier process. Kept in the repository, an AI tool working there can load an instruction file as its own instructions.
- Version-control and CI metadata inside a code drop: a nested `.git` directory, CI workflow files.
- Anything the user says not to keep.

**Material already in the repository stays where it is.** It is not moved, renamed or marked: someone put it there on purpose, and code already in the repository may be in use. The record cites it by its path. The one thing to raise is unendorsed text sitting where requirements are read from (`docs/prds/`, `docs/changes/`), which later skills could take for requirements: the record lists it under Left Out, and the handoff tells the user where it is (Step 10). Whether to move it is the user's call.

### Step 3: Copy It In, Marked as Reference

Copy each source that comes in into `source-material/{name}/received/`:

- **Name each file for what it is and when it was said**: `2026-03-04-kickoff-meeting-transcript.txt`, `2026-03-11-pricing-email-thread.txt`, with no date when none is known. An email or chat thread comes in as one text file, every message in order with its sender and date.
- **Put code in its own directory, named so it cannot be taken for the application**: `reference-only-code-{what}`, where `{what}` says what it was (`reference-only-code-pricing-prototype`, `reference-only-code-earlier-attempt`). Inside it, the files keep their own names and layout. The directory name carries the warning, and renaming dozens of files would only make the code harder to follow.
- **Give every file that can carry a note this one at the top**, in the file's own comment syntax, below anything that has to stay first (a shebang line, an XML declaration, front matter). In plain text and Markdown it goes in as plain lines followed by a line of dashes. The wording is fixed, so it can be searched for:

  ```
  REFERENCE ONLY. Provided by the business ({who, where known}), received {date received}.
  Kept as received apart from this note. Not vetted, not a requirement and not part of the
  application: do not implement from it or change it.
  What was decided from it: source-material/{name}/{name}-requirements-intake.md
  ```

  A file that cannot carry a note (an image, a PDF, a spreadsheet, JSON) relies on its path. For code, add the note with a script rather than by hand, and check that the number of files given it matches the number that can carry it.
- **Add a plain-text copy beside anything that is not plain text** (a `.docx` transcript, a PDF), under the same name with a `.txt` extension and the same note. The record quotes the text copy, and the quotes are checked against it.
- **Keep the application's tools away from it.** If the repository's build, tests, linting, type checking or packaging would pick up files under `source-material/`, as code brought in often would, exclude the folder in that tool's configuration, and confirm it with a command that lists what the tool collects, where one exists.

Commit Part 1 on its own, before Part 2 starts, as `docs({name}): bring in source material for requirements intake` (`pre-commit-validation`, "Who Commits"), with any tool exclusions in the same commit. Kept apart, what was received and what this skill wrote can each be reviewed on their own.

## Part 2: Write the Record

Part 2 reads all of the material: what came in, what the repository already held, and what was left out, which still counts as context and can hold a stakeholder's answer. It quotes only material that is in the repository, so every quote can be checked later.

### Step 4: Extract

Read every source in full and pull out every statement that could matter to what is built. For each, record:

- **The quote**, verbatim, and where it is (source, date, speaker or author).
- **Its kind**: Decision (what the system should or must do), Constraint (a boundary the work must respect), Out of scope (what it must not do or will not cover), Context (how things work today, who uses it, or why the work matters), Unresolved (raised and not settled, including a question a stakeholder said they could not answer), or Exploration (thinking out loud, an analogy, a "wouldn't it be nice").
- **Whose words** it is, per "Whose Words Count".
- **Tentative**, when the speaker hedged or someone pushed back.

Watch for the statements that are easiest to miss. A ten-second "yes, that's a must" binds as firmly as a ten-minute discussion. Requirements arrive inside asides and as implications ("we don't have access to that system" is a constraint). Negative statements ("we definitely don't want X") are scope. A deferred decision ("let's figure that out later") is Unresolved.

**Large material.** When the sources together fit comfortably in one context, with room left to work (as a rule of thumb, half of it or less), read them all in one. When they do not, extraction is split: one subagent per source or group of sources, each given the list of people and returning verbatim quotes with their locations and kinds, and nothing else: no summaries, no conclusions. A single source too large for one subagent is split into overlapping parts by time or section. Steps 5 to 8 always run in one context, over every extraction together: deciding the latest position, what conflicts and what was decided needs all of it in view at once. Never assemble the record from pieces written separately.

### Step 5: Cross-Check by Topic

Group the extracted statements by topic, using the topics the material itself spends time on, not a generic checklist. Then sweep each source again, with the topic list in hand, for anything said on those topics that the first pass missed: a brief confirmation, a constraint stated as a fact, a topic dropped early and picked up much later. For split material, the sweep is split the same way, each subagent given the topic list and returning only missed quotes.

### Step 6: Separate Decisions From Discussion

For every Decision, Constraint and Out of scope item, ask:

- **Did it reach a decision**, or did the discussion trail off? A decided direction without a measure ("it has to be fast") stays a Decision, with its measure Unresolved.
- **Was it later changed?** Topics in long material often come up two or three times; check every mention. A later position replaces an earlier one when it evidently does: within one meeting or thread, where the order is known even without speaker names, the discussion moved on to it and nobody pushed back ("ok, let's do that"), or someone revised their own earlier position; across sources, the later one is dated after the earlier, and its author knew the earlier position (a reply, a reference to it, the same people) or has authority over it. When order, speakers or authority are too uncertain to say one position replaced the other, do not guess: the two are Conflicting (Step 7), with what is unknown named.
- **Was it a directive or thinking aloud?** "Imagine if it worked like X" is not "it should work like X."
- **Did a stakeholder say it or choose it** ("Whose Words Count")? Unendorsed text is Context at most.
- **Is it specific enough to test?** "It should be flexible" is not a requirement until someone said what flexible means.

Items that fail move to Unresolved, Context or Exploration. Then sweep: merge items that say the same thing; keep the most refined version of a point that sharpened over time, adding an earlier quote under the same Decision only when it carries a condition or example the later one lacks; record each reversal under Changed Positions. A Tentative item becomes a Decision only where a later statement firmed it up; otherwise it is Unresolved.

### Step 7: Keep Conflicts, Don't Hand Them Back

Two stakeholder positions conflict when neither replaces the other under Step 6 and both cannot be true. Record both, quoted side by side, marked **Conflicting**, with one line on what would settle it: a check of the current system, a record to look at, the person whose call it is. Unresolved items are recorded the same way, with what would settle them.

Never put a conflict or an unresolved item to the user or a stakeholder from this skill. The PRD written from the record settles each one under the 95% rule or declares it as an assumption (`prd-writing-standards`, "Every Decision Is Written Up or Declared"), and the refinement stages research it. The stakeholder sees it only as a researched assumption with a recommended answer.

A stakeholder's position against unendorsed text is not a conflict: the stakeholder wins, and the other text is Context.

### Step 8: Write the Record

Write `source-material/{name}/{name}-requirements-intake.md` in this form. Its opening lines say what it is, so nobody takes it for received material or for a requirements document.

```markdown
# {Title}: Requirements Intake

Written by requirements-intake from the material in received/ and the other sources
listed under Sources. The quotes are verbatim; the labels are this record's. Not a
requirements document: the PRD written from it is.

## About This Material
Two or three factual lines: what kind of work this is (something new, a replacement
for something that exists, or a change to it), what the material was ({n} sources,
{date range}), and how settled it is ({n} decisions, {n} conflicting, {n} unresolved).
No account of what anyone said.

## Problem and Goals
The stakeholders' own statements of what is wrong today and what they want the work to
achieve, quoted, each with its source, with the real cases they gave. At most two
sentences of label above them. No solution design.

## Who Uses It
Who will use what is built, and for what, quoted where a stakeholder said it.

## How Things Work Today
The current system or process, when the work changes or replaces one. Quoted where a
stakeholder described it; drawn from reference material or unendorsed text, marked as
such and stated briefly, since it is no one's decision.

## Decisions

### {Topic, in the stakeholders' terms}

**{One-sentence label for the decision.}**

> "{Verbatim quote.}"
> — {Speaker or author as the source gives them, or "unnamed speaker"}, {source}, {date or "undated"}

> "{A further quote, when it adds a condition or example.}"
> — ...

{A choice among written options shows the stakeholder's words, then the option text,
labelled "option chosen, wording not theirs".}

## Constraints
Same format, by topic: label, then quotes.

## Out of Scope
Same format.

## Conflicting
Each conflict: a one-line label, both positions quoted with their sources, and what
would settle it.

## Unresolved
Each item: the topic, the quotes that raised it, and what would settle it.

## Reference Material
Each mockup, screenshot, prototype, code directory and document brought in that the
PRD's author should look at: where it is, and one line on what it shows or gives that
nothing else kept does.

## Terms
The stakeholders' names for things, other names the material uses for them, and each
bracketed correction made in a quote.

## Changed Positions
Each reversal: the earlier quote, the later one, where each sits (dates, or their
order in one meeting), and why the later one stands.

## People
Step 1's list: each person, with their role and what they decide where known.

## Left Out
What was set aside and why, by category, one line each: exploration, options nobody
chose, statements without authority, duplicates, superseded drafts, tangents, and
unendorsed text already in the repository where requirements are read from, with its
path. Name off-topic or personal material by category only, never by quote.

## Sources
Step 1's inventory: each source, where it is (under received/, at its path elsewhere
in the repository, or, when it was left out, where it lives outside), its date range,
who wrote it, and what was used from it.
```

A filled-in Decision, for the shape:

```markdown
### Credit holds

**An order over the customer's credit limit waits for approval before it ships.**

> "anything over their limit just sits, nobody ships it till [credit manager] or I sign off on it"
> — Speaker 2, received/2026-03-04-kickoff-meeting-transcript.txt, 2026-03-04

> "prepaid is the exception, prepaid goes no matter what"
> — Speaker 2, received/2026-03-04-kickoff-meeting-transcript.txt, 2026-03-04
```

Keep the sections in this order. Leave out any with nothing in it, except About This Material, Decisions, People, Left Out and Sources; when nothing was decided, Decisions says so, which is a finding in itself. The material decides which sections carry the weight: a kickoff for something new is mostly Problem and Goals and Decisions, a replacement leans on How Things Work Today, a stack of complaints is mostly Problem and Goals with real cases, early discovery is mostly Unresolved. When the material holds something the PRD needs that fits none of these sections, add one named for what it holds, under the same quote rule.

### Step 9: Check the Record

Check the record against the sources before handing off:

- **Every quote matches its source exactly.** Check this by search, not by memory: look each quote up as an exact string in the text in the repository (the file under `received/`, its plain-text copy, or the file at its path), and fix or remove every one that is not found.
- **Every source the record quotes is in the repository**, and every document brought in that is neither stakeholder material nor code has its one line in Reference Material.
- **Nothing is missed.** Search the sources for decision words ("must", "never", "always", "don't", "agreed", "let's go with", "yes") and confirm each hit is in the record or covered by Left Out. For split material, subagents run this search per source.
- **Nothing unendorsed is presented as a stakeholder's words** or as a decision.
- **Each Decision is the current position**, and every earlier, different position is in Changed Positions with its reason.
- **No conflict or unresolved item is phrased as a question** for the user or a stakeholder.
- **The labels add nothing the quotes do not say**: no condition dropped, no absolute ("always", "never") the stakeholder did not use, no number pinned that was only describing today.
- **The terms are the stakeholders' terms**, and Sources accounts for every source in the inventory.

Fix what fails, then check again.

Then have the record reviewed with fresh eyes: `deliverable-review`, with the record as the deliverable and the sources as what it must be true to. The reviewer looks above all for a decision left out, a replaced position recorded as current, unendorsed text presented as a stakeholder's, and a label that says more than its quotes. Fix what it finds, check the fixes with a delta round, and repeat full rounds until one finds no High finding, at most three; if the third still finds one, fix it and say so in the handoff. For split material, each full round is split by source the way extraction was.

### Step 10: Commit and Hand Off

Commit the record as `docs({name}): requirements intake` (`pre-commit-validation`, "Who Commits"), with any source brought in during Part 2. Raw material that arrives before the PRD is written goes through both parts again into the same directory and the same record (new sources, new or replaced positions, Changed Positions), committed as `docs({name}): requirements intake update`.

The next skill is `prd-writing-standards`, whose size check sends the work on to `initiative-breakdown` when it is bigger than one PRD. Start it in a new chat with a `continuation-prompt` that points at the record: the next skill writes from the record, not from the pile, and a chat that has just read the pile has neither the room nor the distance to do that.

Tell the user in a few lines: how many sources were read and how many came in, how many decisions, conflicts and unresolved items the record holds, the largest categories left out, any unendorsed text found where requirements are read from, and any bracketed correction, unnamed speaker or undated source that left a position Conflicting and that the user could clear up. Their read of the record is welcome and is not a gate.

## Rules

- **Never fabricate.** Every item traces to something a stakeholder said or chose.
- **Never summarize a stakeholder.** Select and quote; label in one sentence at most.
- **Never promote unendorsed text** to a decision, however well written or detailed it is.
- **Never put a conflict or open point to the user or a stakeholder** from this skill. Record it and what would settle it.
- **Never decide for the business.** Where the material does not settle something, the record says so; the PRD's 95% rule and assumptions take it from there.
- **Few decisions can be the right outcome.** A pile with ten real decisions produces a record with ten, not forty padded ones.
- **What comes in from outside is quarantined.** The stakeholders' raw words come in whole, code comes in as reference, and the rest of the pile is whittled down to what earns its place, whoever wrote it. All of it sits under `received/`, each file marked reference only, and nothing received is edited beyond that note.
- **What the repository already holds stays where it is.** The record cites it by path.

## Relationship to Other Skills

- `prd-writing-standards` and `initiative-breakdown` take the record as their input. When the record exists, they write from it, not from the raw material, and reach the sources only through it.
- `autonomous-prd-refinement` and `assumptions-document-writing` read the record as the stakeholders' own words: a decision recorded there is not asked again.
- `assumptions-document-writing` is where a conflicting or unresolved item becomes an assumption, once the PRD is written; `autonomous-design-refinement` researches it.
- `using-the-enso-method` routes raw material here first.

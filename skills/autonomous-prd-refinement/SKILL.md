---
name: autonomous-prd-refinement
description: Review-and-fix loop that takes a drafted PRD, with its assumptions and mockups, to a state with no Medium or High finding left, run after prd-writing-standards and before the user's recommended review and the technical design — full deliverable-review rounds until none finds a High, cheaper delta rounds over each round's fixes until none finds a Medium or High, then a final full round; mockups reviewed as design references, facts verified once, progress checkpointed to an on-disk state file so an interrupted run resumes instead of restarting.
user-invocable: true
---

# Autonomous PRD Refinement

A review-and-fix loop for a drafted PRD and everything that travels with it: its assumptions document, its mockups, and the lines it adds to neighbouring documents such as an initiative's PRD list. Each round runs `deliverable-review`, fixes every finding, and records progress in a state file on disk. The run ends when a full, fresh review finds nothing worse than Low, apart from findings rejected with a reason the user can check or handed off to another session.

---

## What Is This Skill?

A PRD written from source material (a brief, its entry in an initiative's PRD contracts, a stakeholder's handoff, interviews) is rarely right on the first draft. Some cases go unstated, two passages disagree, a fix in one place leaves a stale copy in another, and a mockup shows something the criteria no longer say. One review round finds some of this; the fixes then create a few new problems of their own. This skill runs the rounds until they stop finding anything that matters, without the user.

**The goal:** when the run ends, no Medium or High problem a reviewer found in the PRD, its assumptions or its mockups is left unfixed, apart from any rejected with a stated reason or handed off whole to another session, so the user's review is spent on the product decisions, not on defects. And the PRD is still one a person can read and sign off: a run that covers every case but leaves the criteria unreadable has not reached its goal ("Keep It Readable").

**The shape of the work.** A long review loop gets expensive in three places, and the skill is built around each:

1. **Not every round reads everything.** A full round reads the whole deliverable fresh. Between full rounds, a **delta round** checks only what the last fixes changed and everything that shares a term or rule with it (`deliverable-review`, "Delta Rounds").
2. **Mockups are design references, not the product.** Each screen is rendered at one width, the one its main users work at, and checked for what it says. Delta rounds render only the screens the fixes affected (`deliverable-review`, "Look at Visual Deliverables").
3. **Facts are verified once.** A fact checked against a live system is recorded with the query that checked it, and later rounds reuse it.

Interruptions are expected: the run can take hours and outlast a session. State lives in a file on disk, so a new session continues from the round it stopped in.

**This is an orchestrator skill.** It coordinates:
- `deliverable-review`: one round at a time, full or delta, with its severity scale
- `prd-writing-standards`: applied to every fix to the PRD and its mockups
- `assumptions-document-writing`: applied when a fix needs a business decision the sources do not settle

---

## When to Use

Use this skill when:

- A PRD has been drafted from source material, with its assumptions and mockups if it has them
- No technical design exists yet
- The PRD is big enough that one review round will not be the last: many criteria, several screens, or seams with other PRDs
- Review rounds are already running on the PRD without this skill: it takes over from where they are (Phase 1, "Adopting a review already under way")

**Do NOT use this skill when:**

- One `deliverable-review` round is enough for the PRD's size. Run that instead
- A technical design already exists. `autonomous-design-refinement` refines the PRD and the design together
- You want to judge each finding yourself. Run `deliverable-review` round by round

---

## Required Inputs

1. **The PRD's path.** The skill also finds, from the PRD's directory and its links:
   - the assumptions document, if any
   - the mockups and whatever generates them
   - the source material the PRD was written from: the brief, its entry in the PRD contracts and the coverage matrix, a handoff package, a requirements intake record (`requirements-intake`), whose quotes are the stakeholders' own words
   - neighbouring documents the PRD adds lines to, such as its PRD-list row, its PRD-contracts entry and seam rows, and coverage-matrix rows
2. **Read access to the systems the PRD describes**, where the project allows it (`engineering-principles`, "Production Data"), so facts and sample data can be checked. Credential discovery follows `investigate-question`.

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| Round cap | 12 | Full and delta rounds together. Reaching it stops the run and reports what is still open; it never ends the run silently |
| Reviewers per round | 1 | One review sub-agent, plus the extra visual reviewers `deliverable-review` launches when a round has more than about 20 images to look at |
| Writers per round | 1 | One fix sub-agent at a time, never two, so two writers never edit the same document |

**Effort.** Every sub-agent runs at high effort or above: a session at a higher level carries that level through, and one below it launches its sub-agents at high. Reviewing and fixing are careful reading and careful editing; what keeps the cost down is the delta rounds, rendering each screen once and verifying facts once, not weaker reviewers.

---

## The Loop

Each round is a `deliverable-review` round, followed by fixing every finding it reports, Lows included. Only the Highs and Mediums it fixed decide what comes next; a rejected one, or one handed off whole, does not count (below):

| The round was | It fixed | Next round |
|---|---|---|
| Full, before any delta round | Any High | Full |
| Full, before any delta round | Mediums, no High | Delta |
| Full, after delta rounds | Any High or Medium | Delta |
| Full, at any point | Only Lows, or nothing | None: finish |
| Delta | Any High or Medium | Delta |
| Delta | Only Lows, or nothing | Full |

In words: full rounds until one leaves no High to fix, then delta rounds until one leaves no Medium or High to fix, then a full round. If that full round has a Medium or High to fix, the loop goes back to delta rounds. **The run ends only on a full round with no Medium or High to fix.** A delta round sees only what the fixes touched, so it never ends the run.

**Rejected and handed-off findings do not count.** The table reads the Highs and Mediums a round's writer fixed. A finding rejected with a reason (Phase 3), or handed off whole because only another session can fix it and nothing in this PRD changed ("Working Beside Other Sessions"), does not drive the loop. It is passed to every later reviewer, who may raise it again with evidence; rejected Mediums and Highs and handed-off findings are listed in the completion report and the commit body so the user can check them.

Severity follows `deliverable-review`'s scale ("Rate Each Finding"): rated by the consequence of building from the PRD as written, never by the effort of the fix. No one re-rates a finding, and a disputed rating is no reason to reject one: it is fixed, and counts at the reviewer's rating. When the writer believes a finding itself is wrong, it rejects it with the reason (Phase 3).

**When the same area keeps producing findings.** `deliverable-review` asks for a case walk once one part of the work has produced a Medium or High in two rounds running. The orchestrator tells each reviewer which areas did, from the state file's Rounds table, counting fixed findings only.

**When fixes go back and forth.** If one round's fix is undone by the next round's fix (a passage flips between two readings), the passage carries an undecided question. Stop fixing it by review. Settle it by the 95% rule ("The Scope Gate"): from the source material if that settles it at 95% or more, written into the PRD; otherwise, if it is a business decision, as an assumption (`assumptions-document-writing`). Record in the state file which passage flipped and what settles it, the citation or the assumption ID, so later reviewers see it.

---

## The Scope Gate

A fix may make the PRD say precisely what its source material and stated intent already require: an unstated case on a path the product already has, a contradiction, a stale copy, a missing criterion the source asks for. A fix never adds a capability neither asks for. A finding whose fix would add one is recorded under **Noticed, out of scope** in the state file, one line, and left alone. Those lines go to the user in the completion report.

A finding that needs a business decision is settled by the 95% rule (`prd-writing-standards`, "Every Decision Is Written Up or Declared"). Settled at 95% or more from the source material, it is written into the PRD as its requirement, with no entry and no list of settled questions. Below 95%, it becomes an assumption at the best-supported answer in the same fix step, written with `assumptions-document-writing` (its gates first: the answer is often already written down). Use a Blocking Open Question only for the rare case that skill defines; it pauses the run.

**The orchestrator's rulings follow the same rule.** When it hands a writer a ruling to settle a finding, often the way to stop a passage flipping: at 95% or more from the material the writer writes it into the PRD, and below 95% on a business question the writer declares it as an assumption in that fix step. The state file records the ruling and the citation or assumption ID that settles it. It never stands in for an assumption, and no reviewer is told to treat a business decision as settled unless it has one or the other.

**Say what settles each fix.** For every Medium or High it fixes, the writer names what settles the fix: the source material (cited), a rule the PRD already states, a decision settled at 95% or more from the material, or an assumption ID. A business decision below 95% is an assumption, as above, so the person signing off sees it as something to confirm rather than a rule to skim past. A consequence of a rule the PRD already states is not a new decision and gets no assumption of its own: too many entries get approved unread (`assumptions-document-writing`).

---

## Keep It Readable

Review rounds find cases, and every case found invites one more clause. Left alone, the criteria the rounds set out to sharpen become a document nobody can sign off with understanding, and an agent builds from it no better. Every fix follows `prd-writing-standards`, "Keep Criteria Readable as Cases Are Added":

- **A case a stated rule settles needs no clause of its own.** The fix sharpens that rule's wording rather than adding one. Reviewers rate such a case Low at most (`deliverable-review`, "Calibrating the edges"); the writer still fixes a finding at the rating it was given.
- **A criterion a fix would grow is restated, split, or given a table of its cases,** never extended clause by clause.
- **Each rule is stated once,** and every other place names it by label.
- **Mockup notes stay short.** A note says what its state shows and which criteria it covers. Links between states are neither reviewed nor explained.
- **Growth is tracked.** The Rounds table records the words in the acceptance criteria after each fix step, and every full round's reviewer gets those figures with the readability question (Phase 2). Criteria that grew with no new requirement behind them are where to look first.

---

## Facts

Fixes and reviews often turn on facts about the systems the PRD describes: how a record is shaped, which values a field carries, which vendor or customer a sample record belongs to. Getting one wrong costs a round, and checking one again every round costs more.

- **Verify once, record it.** Each fact checked against a live system or a source document goes in the state file's **Facts** table: the fact, the query or source that established it, the date, and the passages that rely on it.
- **Reuse.** Every reviewer and writer gets the Facts table and uses it rather than querying again. A fact is re-verified only when a passage or sample record relying on it changed.
- **Query what the PRD refers to.** A wrong fact usually comes from checking a neighbouring record: the parent instead of the child, a template instead of the item, an older version. Each Facts row names the exact record queried.
- **Facts are scaffolding.** They are deleted with the state file. Evidence a stakeholder needs to judge an assumption goes in that assumption's evidence, where it stays.

Read-only always, and production only where the project allows it (`engineering-principles`, "Production Data").

---

## Mockups

A PRD's mockups are **design references**: they show what the criteria require, and the built product will be reviewed in its own right. They are reviewed accordingly (`deliverable-review`, "Look at Visual Deliverables"):

- Each screen or state is rendered at one width, the one its main users work at, and checked for content: does it show what the criteria require, with sample data consistent with the facts?
- Layout counts only where it makes content unreadable or misleading. Alignment, spacing and how screens reflow at other sizes belong to the built product's review.
- The screen sizes a PRD names are requirements on the product, not on its mockups.
- A full round renders every screen once. A delta round renders only the screens whose content changed (for screens generated from one script, compare each screen's data or render, not the script) and those that show a term, figure or rule the fixes changed.

A wrong mockup is redrawn in its own medium, never annotated (`prd-writing-standards`, "Mockups Show What the Criteria Require").

---

## Working Beside Other Sessions

A PRD in an initiative is often refined while sessions for its neighbours are writing theirs, and fixes reach into shared documents: the seams in an initiative's PRD contracts, a coverage matrix. A sibling PRD's criterion that this one changes is named only in a `Replaces:` line on this PRD's own criterion; the sibling's `Superseded by:` line is written when this PRD is built, never during refinement (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion").

- **Before editing a document this PRD does not own,** check it for another session's uncommitted changes (`git status`, `git diff`). Edit only the lines this PRD owns: its PRD-list row, its PRD-contracts entry and seam rows, and its coverage-matrix rows, plus, when this PRD is retitled, its name and directory wherever other lines give them (`prd-writing-standards`, "Writing a planned PRD from an initiative"). Detail goes into the PRD; an entry stays within `initiative-breakdown`'s size cap. Never revert, restage or reformat another session's work.
- **A change another session's document needs** (a seam both sides must state the same way, a criterion of theirs that must change to fit this PRD, not one this PRD replaces) goes to that session as a message, through whatever channel the tooling offers, or as a note for the user to relay. Record it under **Hand-offs** in the state file.
- **Agree a seam once.** When two PRDs must state a handoff the same way, settle the wording with the other session and record it under Hand-offs, so later rounds review against the agreed wording.
- **A finding only another session can fix** (its side of a seam, a criterion of theirs that must change): the writer fixes this PRD's side, if it has one, and sends the rest as a hand-off with the proposed wording. When this PRD changed, the finding is marked `Fixed; rest handed off: {Hand-offs row}` and counts as fixed, so the change is reviewed like any other. Only when nothing in this PRD changed is it marked `Handed off: {Hand-offs row}`. Reviewers get the pending wording, so they do not raise it again each round.
- **Staging is per file.** Stage only the run's own files. When a shared file mixes this run's lines with another session's uncommitted ones, leave it out of the commit, say so in the completion report, and let the user decide how it is committed.

---

## State File

**Location:** beside the PRD, as `{feature}-prd-refinement-state.md`.

**Lifecycle:** created in Phase 1, updated after every review and every fix step, deleted at completion. It is scaffolding, never a deliverable, and is never committed: a paused run leaves it untracked beside the PRD.

**Editing rule:** update rows in place. Never regenerate the file from memory; that is how findings get lost.

### Template

```markdown
# PRD Refinement State — {feature}

Started: {date}   Round: {N}   Next round: {Full | Delta}   Delta rounds run: {yes | no}   Round cap: {12, or as the user raised it}   Status: {In progress | Paused: reason}
Branch: {branch}
Delta base: {tree id of the documents as the last recorded review saw them}
Last updated: {date time}

## Documents
| Document | Path |
|---|---|
| PRD | … |
| Assumptions | … |
| Mockups (generator, how to render, main users' width) | … |
| Source material | … |
| Neighbouring documents | … |

## Intent and decisions
{The 1–2 sentence intent every round reviews against, and the decisions the source material settles, as deliverable-review's Steps 1–2 need them. Written once; amended only when the user rules.}

## Rounds
| Round | Kind | High fixed | Medium fixed | Low fixed | Rejected (severity) | Handed off whole | Areas with a fixed Medium or High | Criteria words |
|---|---|---|---|---|---|---|---|---|
| 1 | Full | 2 | 6 | 10 | 1 (Low) | 0 | refunds, bundled items | 3,900 → 4,050 |

## Findings
Open, rejected and handed-off findings, and the last round's fixed findings with what changed for each. Those are what the next delta round checks; they are replaced when the next round's fixes are recorded, so both the next reviewer and the next writer see them. Rejected and handed-off findings stay for the whole run.
| ID | Round | Severity | Finding (one line) | Status |
|---|---|---|---|---|
| R1-07 | 1 | Low | … | Rejected: the sample date matches the record it was drawn from (Facts) |
| R2-03 | 2 | Medium | … | Fixed: {what changed, and where} |

## Run totals
Screens redrawn: {list}   Assumptions added or amended: {IDs}   Rejected Mediums and Highs: {IDs, one line each}   Handed off whole: {IDs} (a `Fixed; rest handed off` finding counts as fixed, never here)

## Facts
| Fact | Record and query, or source | Date | Passages relying on it |
|---|---|---|---|

## Flipped passages and rulings
{Each passage that went back and forth, and each ruling given to a writer, with what settles it: the source cited, a decision settled at 95% or more and written into the PRD, the assumption ID, or the user's ruling. Never a business decision held only here.}

## Hand-offs
| To | Change | Status |
|---|---|---|

## Noticed, out of scope
- {one line each}

## Next action
{The single next thing to do. A resuming session starts here.}
```

---

## Orchestration Model

The orchestrator stays thin: it reads the state file, launches one sub-agent at a time, and records each result. It does not review or fix anything itself, so its context lasts the whole run.

| Step | Who | Returns to the orchestrator |
|---|---|---|
| Setup, re-orientation | Orchestrator, with one sub-agent on a fresh start | The intent, the decisions the sources settle, how the mockups render and the width their main users work at |
| Review | One `deliverable-review` sub-agent, full or delta, plus its visual fan-out when needed | Findings with severity, location and the consequence that sets the severity; facts it verified |
| Fix | One writer sub-agent | Per finding: fixed (where), fixed with the rest handed off (to whom), rejected (why), or handed off whole (to whom); the propagation sweep's search terms and the copies it updated; mockups regenerated; files it created or edited; passages settled after flipping, and how; facts it verified; hand-offs it needs |
| Continue or stop | Orchestrator | — |

Sub-agents return distilled results, not transcripts.

### Interruption Recovery

If the session ends at any point:

- A finished round's findings are in the state file. A review that was in flight is simply run again.
- A fix step that was in flight is recovered from the files: findings still Open in the state file are compared with the documents, and the writer finishes only what is not yet done.
- **Next action** says where to pick up.

If a sub-agent fails, retry once. If the reviewer fails again, set Status to `Paused: review failed` with the error and report to the user. If the writer fails again, keep its findings Open, set Status to `Paused: fix failed` with the error, and report; never drop a known finding.

On a session-limit or context warning: finish the step in flight, update the state file, set Status to `Paused: session limit`, and stop. Do not start a round into a closing window.

---

## Process

### Phase 1: Setup and Re-orientation

**Pending feedback changes come first,** on a fresh start and on every resume. A `{name}-pending-feedback-changes.md` beside the PRD means a stakeholder round has changed what it must say: apply it with `assumptions-document-feedback`, which resumes from that file (its Step 4a, "Resuming"), commit that amendment on its own, then continue.

1. **Check for a state file** beside the PRD. If one exists, read it and check Status first: a paused run waits for what its **Next action** names (a raised cap, an answer, access) until the user gives it. Otherwise confirm the documents still exist and continue from **Next action**.
2. **If starting fresh**, find the documents listed under Required Inputs and create the state file. Have one sub-agent read the PRD and its source material and return the intent, the decisions the sources settle, how the mockups render and the width their main users work at, and write them into the state file. The orchestrator does not read the full documents itself.
3. **Confirm the repo state:** the branch, and which files other sessions have uncommitted changes in. Record the branch.
4. **Confirm access:** a way to render the mockups, and read access to the systems facts come from. A finding that needs access the run lacks (a screen that cannot be rendered, a fact that cannot be checked) pauses the run (`Paused: needs {access}`) instead of returning every round.

**Adopting a review already under way.** A PRD that has already been through review rounds without this skill does not start over. Create the state file as for a fresh start, record the earlier rounds in the Rounds table as far as their history shows them, marked `before this run`, and gather into Facts what those rounds verified, from the documents' evidence and from the session that ran them. The next round follows The Loop from the last earlier round's result; when that result is not known, it is a full round. Earlier rounds do not count toward the round cap.

The orchestrator plays `deliverable-review`'s main agent for its Steps 1–3: the state file's intent, decisions, mockup notes and Facts are Steps 1–2, and Phase 2 below is Step 3. Each full round's reviewer also answers Step 6's question, and Phase 3 takes the place of Steps 4, 5 and 7.

### Phase 2: Review

1. **Snapshot the documents** through a temporary index, so the shared index is never touched: `GIT_INDEX_FILE={tmp} git read-tree HEAD`, then `GIT_INDEX_FILE={tmp} git add -- {paths}`, then `GIT_INDEX_FILE={tmp} git write-tree`. The paths are the in-repo files the run edits (the PRD, assumptions, mockup sources, the neighbouring documents it changes), plus any file a fix created; never source material kept outside the repo, and never the state file. `{tmp}` is an absolute path outside the repo, so no index file lands in the checkout. Hold the tree id; it becomes the **Delta base** only when this round's findings are recorded (step 4), so a review interrupted and run again still diffs against the old base.
2. **For a delta round, take the diff:** `git diff {Delta base} {snapshot} -- {paths}`, which covers new files too. If the base tree is gone, run a full round instead.
3. **Launch the review** with `deliverable-review`, giving it, beyond that skill's own context:
   - the round's kind, full or delta
   - the intent and decisions, and the **Facts** table
   - the areas that produced a fixed Medium or High in each of the last two rounds
   - rejected findings with their reasons, to raise again only with evidence the reason is wrong
   - the flipped passages and rulings, each with what settles it, and agreed and pending seam wording from Hand-offs
   - that this run has no conflict check: earlier criteria elsewhere in the repo that this PRD changes are not searched for (`autonomous-design-refinement` does that once the design exists)
   - for a delta round: the previous round's findings and what was changed for each or, for a rejected one, the reason, from the Findings table, and the diff from step 2
   - that mockups are design references, how they render and the main users' width, and, for a delta round, which screens' content changed
   - for a full round, `deliverable-review` Step 6's question: does the deliverable, as it stands, accomplish the intent? A gap is a finding, rated like any other
   - for a full round, three more questions, with the criteria-word figures from the Rounds table: can the person who signs the PRD off read each criterion once and say what it checks ("Keep It Readable")? Does any assumption's chosen answer now look wrong, given what the run has learned? And does the deliverable make any business decision that is neither settled at 95% or more from the source material nor declared as an assumption? Each is a finding, rated like any other
   - for a full round, when a coverage matrix maps rows to this PRD: is each row covered by a criterion, declared as an assumption where the PRD departs from it, or moved to a neighbour with both PRD-contracts entries and the matrix updated? An uncovered row is a finding. The answer stays in the round: no coverage-trace table or file is written (`prd-writing-standards`, "Before You Write: Is This One PRD?")
   - for a full round, when the PRD is in an initiative: does its `**Depends on:**` line agree with its PRD-contracts entry and its PRD-list row, and say `None` in words when it depends on nothing? A missing line or a disagreement is a finding
4. **Record the findings** in the state file: a Rounds row with the round and its kind, each new finding in the Findings table as Open, the facts the reviewer verified added to Facts, and the snapshot from step 1 as the **Delta base**.

### Phase 3: Fix

1. **Launch one writer** with the open findings, the documents, the Facts table, the Scope Gate, the flipped passages and rulings, the agreed and pending seam wording from Hand-offs, the rules in "Working Beside Other Sessions", the previous round's fixes (so it can see a passage flipping back), and the instruction to fix by `deliverable-review` Step 5: each visual fixed in its own medium, a propagation sweep for every term, figure, name or rule a fix changed, and a check of each sentence a fix adds against its neighbours. Fixes follow `prd-writing-standards` and, for assumptions, `assumptions-document-writing`, and keep the PRD readable ("Keep It Readable"). The writer returns, beyond its fixes, what settles each Medium or High it fixed ("The Scope Gate") and the words in the acceptance criteria after its fixes.
2. **The writer fixes every finding, Lows included, rejects it with a reason, or hands it off when only another session can fix it.** A finding is rejected only when the governing text, a fact, a stakeholder's ruling or the scope gate shows it is wrong, and the reason names which.
3. **Record the result:** the Rounds row is completed (fixed counts, rejected, handed off whole, areas with a fixed Medium or High, criteria words before and after); the previous round's Fixed rows are removed, and this round's fixed findings are marked Fixed with what changed; rejected and handed-off ones keep their reason or Hand-offs row; screens redrawn, assumptions changed and rejected Mediums and Highs go in Run totals; new facts go in Facts; files the writer created or edited that are not yet listed go in Documents; passages it settled after flipping, and rulings given to it, go in Flipped passages and rulings with what settles each; out-of-scope lines and hand-offs in their sections. Set **Next round** from The Loop (and **Delta rounds run** once one has), and **Next action**.
4. **Report the round in one line:** `Round {N} ({kind}): fixed High {h} · Medium {m} · Low {l}; rejected {r} ({severities}); handed off whole {k}. Next: {kind}`.

### Phase 4: Continue or Stop

Using the state file only:

- **Finish** (Phase 5) after the fix step of a full round with no Medium or High to fix (rejected and handed-off ones do not count; The Loop).
- **Stop at the round cap.** Set Status to `Paused: round cap`, keep the state file, and report the last round's Mediums and Highs, fixed but not yet re-reviewed, and the areas that kept producing findings. The user decides whether to continue; if they do, record the cap they set in the state file's header.
- **Pause and report** when a Blocking Open Question arises, when a passage that went back and forth cannot be settled from the sources, or when a finding needs access the run lacks.
- **At every pause,** set **Next action** to what the run waits for (`await the user: raise the cap`, `answer {question}`, `grant {access}`), never to the next round.
- **If the user says to stop** at any pause, run Phase 5 as a stopped run. The report's header reads `=== Autonomous PRD Refinement Stopped ===`, its Final round line gives the reason it stopped, its Next line says what is left, and the commit subject reads `PRD refinement stopped` in place of `PRD refinement complete`. The report and the commit body both list the open findings, the last round's Mediums and Highs fixed but not re-reviewed, and any blocking question.
- **Otherwise** start the next round at Phase 2.

### Phase 5: Completion

1. **Write the completion report** (below) from the state file while it still exists.
2. **Delete the state file.** When the PRD is in an initiative, also delete its entry's scope lines (directory, Reaches production, In and Not in this PRD, Depends on) from the PRD contracts, keeping **Shared contracts it owns** and **Questions it answers** (`initiative-breakdown`, Step 5): the PRD now holds its own scope.
3. **Commit** the run's own files as `docs({feature}): PRD refinement complete — {rounds} review rounds, {findings} findings fixed`. Put the **Noticed, out of scope** lines, the open hand-offs and handed-off findings, and the rejected Mediums and Highs with their reasons in the message body: once the state file is gone, the commit is their only durable home. This is the default; the user's instructions override it (`pre-commit-validation`, "Who Commits"), and then the files are staged and the message presented. It never pushes.
4. **Output the report:**

```
=== Autonomous PRD Refinement Complete ===

Rounds: {N} ({f} full, {d} delta)   Final round: full, no Medium or High left to fix
Findings fixed across all rounds: High {h} · Medium {m} · Low {l}   Rejected: {r}, Mediums and Highs listed with their reasons   Handed off: {list, or none}
Mockups: {s} screens, {k} redrawn during the run
Acceptance criteria: {c} criteria, {w0} → {w1} words
Assumptions added or amended: {IDs, or none}
Facts verified: {n}

Hand-offs to other sessions: {list, or none}
Out of scope, noticed and not acted on: {list, or none}

Next: the user's review of the PRD is recommended here, ideally with whoever owns the business decisions (`stakeholder-review-package` can make it a readable review now, on request; for a follow-on PRD made for a stakeholder's new asks, one with a `**Follow-on to:**` line whose scope came from their saved feedback, make it now without being asked); then the technical design (`technical-design-writing-standards`) in a new chat.
```

After the report, give the `continuation-prompt` for the technical design, unless the user asked to carry on in this chat.

---

## Rules and Constraints

### DO

- Fix every finding each round, Lows included, reject it with a reason, or hand it off when only another session can fix it
- Sweep every copy of whatever a fix changed before the next round
- Let only the Highs and Mediums a round fixed decide the next round, and end only on a full round
- Render mockups at their main users' width: every screen in a full round, only the screens the fixes affected in a delta round
- Record each verified fact with the exact record and query, and reuse it
- Keep the state file current after every step; resume from it, never restart
- Keep the PRD readable for the person who signs it off: sharpen a rule, split it or give its cases a table, rather than add a clause
- Write every decision settled at 95% or more into the PRD, and declare every business decision below 95% as an assumption with `assumptions-document-writing`, whoever made it
- Stop at the round cap and say what is still open

### DO NOT

- End the run on a delta round, or on a full round that had a Medium or High to fix, even once it is fixed, unless the user says to stop
- Re-rate a finding to end the loop sooner; fix it at the reviewer's rating, and reject only a finding that is wrong
- Grow a criterion one clause per case, or spell out a case a rule the PRD already states settles
- Hold a business decision only in the state file, or tell a reviewer to treat one as settled, without its citation or assumption ID
- Add a capability neither the source material nor the stated intent asks for
- Review mockups at every screen size the PRD names; those sizes are requirements on the product
- Run two writers at once, or edit another session's lines in a shared document
- Write to any external system, or read production beyond what `engineering-principles`, "Production Data" allows
- Commit the state file or its facts
- Commit files other than the run's own, or push (`pre-commit-validation`, "Who Commits")
- Embed client-specific references (credential paths, private repo names); those belong in your house engineering standards (`docs/enso-method-setup-guide.md`, "Plugging in your house engineering standards")

---

## Relationship to Other Skills

| Skill | How this skill uses it |
|---|---|
| `prd-writing-standards` | Writes the PRD this skill refines, and governs every fix to it and its mockups |
| `deliverable-review` | Every round, full or delta; owns the severity scale, the visual review and the fix discipline |
| `assumptions-document-writing` | When a fix needs a business decision the sources do not settle |
| `initiative-breakdown` | Hands each planned PRD to `prd-writing-standards`; this skill refines it before the user's review |
| `autonomous-design-refinement` | Runs later, once the technical design exists, and refines the PRD and design together |

---

## Example Walkthrough

### Starting state

```
PRD:          docs/prds/customer-returns/customer-returns-prd.md   (24 criteria)
Assumptions:  docs/prds/customer-returns/assumptions.md            (9 entries)
Mockups:      docs/prds/customer-returns/mockups/                  (14 screens, generated from one script)
Source:       a stakeholder's handoff package and its PRD-contracts entry
State file:   (none, fresh run)
```

### Rounds

- **Round 1, full:** 2 High (a refund rule that contradicts the handoff's ruling; no criterion for returns of bundled items), 6 Medium, 11 Low. The writer fixes them; the sweep finds the refund rule repeated in the Summary, an assumption and two mockup screens' text, and updates all four. It queries one order to confirm how bundles are stored, and records the record and query under Facts. One Low is rejected: the reviewer read a mockup's sample date as stale, but it matches the order it was drawn from.
- **Round 2, full:** no High, 4 Medium, 4 Low. One Medium is a seam the neighbouring exchanges PRD must state the same way; the writer fixes this PRD's side and sends the wording to the session writing that PRD, which agrees it, and the agreed wording goes under Hand-offs. All fixed. Next is a delta round.
- **Round 3, delta:** the reviewer reads the diff of round 2's fixes and everything sharing their terms. 1 Medium: a sentence added for the label screen contradicts the exchange criterion. 2 Lows. The reviewer rendered only the three screens round 2's fixes affected. Fixed.

*The session ends here on a usage limit, during round 4's review.*

- **Round 4, delta, resumed:** a new session reads the state file; **Next action** says "run round 4, delta". The review runs again, which is the whole cost of the interruption. No Medium or High; 2 Lows fixed. Next is a full round.
- **Round 5, full:** 1 Medium, an unstated case on a normal path (a partial refund when part of an order has shipped), and 1 Low. Fixed. Back to delta rounds.
- **Round 6, delta:** 1 Medium, again in refunds: the new partial-refund sentence leaves store credit unstated. The source material does not say whether store credit is refunded, so the fix is assumption RULE-010 at the best-supported answer. Refunds have now produced a Medium in two rounds running, so the next reviewer walks the refund cases.
- **Round 7, delta:** the case walk covers 18 refund cases and finds every one settled. 1 Low, fixed.
- **Round 8, full:** 3 Lows. Fixed. The run ends.

### Completion

The report: 8 rounds (4 full, 4 delta); fixed High 2 · Medium 13 · Low 23, and 1 Low rejected; 3 screens redrawn; assumption RULE-010 added; one hand-off to the session writing the neighbouring exchanges PRD, about how both state the exchange seam. State file deleted; the PRD's files committed. The user reads the PRD before the design starts.

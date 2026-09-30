---
name: autonomous-requirements-refinement
description: Multi-pass workflow that refines PRD, Technical Design, and Assumptions documents to implementation-ready state — small ranked batches, each answer folded into the documents as soon as it is known, progress checkpointed to an on-disk state file so an interrupted run resumes instead of restarting.
user-invocable: true
---

# Autonomous Requirements Refinement

Multi-pass workflow that refines requirements documents (PRD, technical design, assumptions, and any supporting materials they reference) to implementation-ready state. Each pass runs `implementation-readiness-check` for a small, ranked batch of questions, investigates them one at a time, folds each answer into the documents the moment it is known, and records progress in a state file on disk — so an interrupted run loses at most the questions in flight (three or fewer) and resumes from where it stopped.

---

## What Is This Skill?

This skill automates the loop humans do manually: run a readiness check, get questions, investigate them, update the requirements documents, check again, find the new questions the updates exposed, and repeat until the documents are solid enough to implement against.

**The goal:** by the end of the run, the PRD, technical design, and assumptions document are complete enough that implementation can proceed without the AI needing to guess or ask. Remaining uncertainties live in the assumptions document as implementable, stakeholder-validatable assumptions.

**The shape of the work matters as much as the goal.** The run is long — hours, often more than one session — and sessions end without warning: usage limits, sleep, network. So the skill is built around three rules:

1. **Every answer lands immediately.** An investigated question is written into the documents before the next question starts. Nothing valuable waits in memory for a later "fold" step.
2. **State lives on disk, not in the conversation.** A small markdown state file records every question and its status. A fresh session reads it and continues; it never restarts.
3. **Small batches, ranked by impact.** A pass handles a dozen questions, not a hundred. More passes are cheap because each one is checkpointed; one giant pass is expensive because losing it loses everything.

**This is an orchestrator skill** — it coordinates:
- `implementation-readiness-check` — to surface gaps and questions each pass
- `investigate-question` — one question at a time, in a subagent
- `assumptions-document-writing`, `technical-design-writing-standards`, `prd-writing-standards` — applied when writing into each document

---

## When to Use

Use this skill when:

- You have a draft PRD and Technical Design document for a feature
- You want them implementation-ready with minimal manual intervention
- You are willing to let the AI run for a long time, possibly across several sessions
- You want the AI to dig into code, data, and APIs to answer its own questions rather than asking you

**Do NOT use this skill when:**

- You want to stay closely involved in every decision — run `implementation-readiness-check` yourself and use `investigate-question` on specific items
- One readiness-check pass is enough for the feature's size
- You need to implement immediately and cannot wait for multiple passes

---

## Required Inputs

1. **Document paths** — both of the following are **required** (the skill will not run without them):
   - PRD document
   - Technical Design document

   The skill also looks for these **optional** supporting materials:
   - Assumptions document (created if it doesn't exist and assumptions are identified)
   - Any other documents the PRD or tech design reference (data model docs, mockups, API specs, etc.)

2. **Access to the codebase and relevant environments** — investigation reads code and may query databases, test APIs, or inspect infrastructure. Credential discovery follows `investigate-question`: check for skills that document credential handling, then the README, then existing config, before asking the user.

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Convergence threshold | 90% | A question is resolved when its answer reaches ≥90% confidence. Note the two thresholds in play: `implementation-readiness-check` *surfaces* anything below 95% (its own inclusion rule), and business questions below 95% become assumptions; this skill *closes* a question at 90%. The 90–95% band is deliberate — every item gets dispositioned, not every item must reach 95%. |
| Questions per pass | 12 | Hard cap on questions taken from discovery into a pass, ranked by impact and uncertainty. Configurable, but resist raising it — the cap is what keeps a pass inside one session. |
| Concurrent investigations | 3 | At most three `investigate-question` subagents in flight. Enough to overlap I/O; small enough that an interruption strands almost nothing. |
| Discovery yield stop | 3 | Stop running passes once a discovery pass surfaces fewer than three new questions below the threshold |
| Maximum passes | 8 | Stop after eight passes regardless |

There is no minimum pass count: per-question checkpointing makes extra passes cheap, so the yield rule decides when to stop. The final verification in Phase 7 is the mandatory re-check.

**Effort.** Every subagent this skill launches — discovery, investigation, writer, conformance — runs at **high** effort or above (subagents inherit the session's effort unless the launcher sets one, so a session at a higher level carries that level through); the work is real research and careful editing, and the caps above are what bound cost, not the effort of individual agents. The caps are binding regardless of session mode: a session running in an exhaustive or "ultracode" mode does not license parallel discovery panels, a larger batch, or auditing everything adjacent to the feature. Those are exactly what the scope gate below exists to prevent.

*Operator note:* a skill cannot change the session's effort or mode. If you want the run to stay inside a session limit, start it in a normal session, not an exhaustive one.

---

## The Scope Gate

A question earns a place in a pass only if **someone writing this feature's code would have to make a judgment call without it.** That is the whole test.

Things that fail the test, even when they are true and interesting:

- Pre-existing defects in surrounding systems that do not block this feature
- Infrastructure hygiene, hardening, or audit findings across the fleet
- "Would it be better if…" redesigns of contracts the documents already settle
- Questions answerable in two minutes by reading the code — answer those during discovery and never raise them
- Questions whose answer would create an obligation no PRD statement implies. Refinement never adds scope. A question passes when its answer narrows or makes precise something the PRD already requires (which records, what format, what happens when a required step fails). A gap the feature cannot work without goes to the design's Open Questions, not to **Noticed, out of scope**
- Under the **Salvage** posture (below), questions about how existing code behaves in cases the PRD does not call for

When an investigation trips over something out of scope, write one line under **Noticed, out of scope** in the state file and move on. Do not investigate it, do not write a script for it, do not fold it into the documents. Those lines are the user's to act on later.

The `implementation-readiness-check` skill's own guidance — *prefer fewer, high-signal questions over exhaustive lists* — governs discovery here. One reader of the documents, in implementation mode, capped and ranked. Not a panel of independent reviewers each producing a list.

---

## Existing Code Posture

Before the first discovery, record in the state file how existing code in the feature's area is treated. These are the same two terms `technical-design-writing-standards` uses:

- **Preserve** (the default): the existing code is in production, or other work relies on it. Its behavior constrains the design, and questions about fitting the new work to it pass the gate normally.
- **Salvage**: the existing code is unreleased, or left over from earlier work being restarted. The design reuses what fits the PRD and switches off, one line each, what the PRD does not ask for. It never designs around that code, and questions about how it behaves in cases the PRD does not call for fail the gate.

An area can be mixed; record it per component ("Salvage for the retry worker; Preserve otherwise").

**The posture is stated, not researched.** Take it from the user, then the PRD, then the design's Existing Code section, in that order when they disagree. Never work it out from deploy or merge history. If none of them says, use Preserve, and say so in one line when the run starts so the user can correct it before a pass runs; repeat it in the first checkpoint summary.

**Every subagent gets the posture**: discovery, investigation and writers. For Salvage code it overrides `implementation-readiness-check`'s invitation to ask about the behavior of existing code: only behavior a PRD requirement relies on is in scope. The writer records the posture as one line in the design's Existing Code section, so it outlives the state file.

---

## State File

**Location:** alongside the PRD — `{feature}-refinement-state.md` in its directory, under `docs/prds/` or `docs/changes/`.

**Lifecycle:** created in Phase 1, updated after every question, staged with the documents at each pass checkpoint, and **deleted in Phase 7** when the run completes. It is scaffolding, not a deliverable.

**Editing rule:** update rows and counts in place. Never regenerate the whole file from memory — that is how status gets silently lost.

### Template

```markdown
# Refinement State — {feature}

Started: {date}   Current pass: {N}   Status: {In progress | Paused: reason}
Branch: {branch the documents are on}
Existing code posture: {Preserve | Salvage | per component} (source: {user | PRD | TD | default})
PRD words: at start {wc -w} · growth baseline {wc -w; reset when the user says continue after a growth pause}
Last updated: {date time}

## Documents
| Document | Path |
|---|---|
| PRD | … |
| Technical Design | … |
| Assumptions | … |
| Supporting | … |

## Passes
| Pass | Surfaced (new) | Taken | Resolved | Assumptions | Deferred | Blocked | Dropped |
|---|---|---|---|---|---|---|---|
| 1 | 31 | 12 | 9 | 2 | 1 | 0 | 0 |

## Questions
| ID | Pass | Question (one line) | Type | Impact | Conf. start → now | Status | Landed in |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | … | Technical | HIGH | 55 → 95 | Resolved | TD §Data Models |
| Q2 | 1 | … | Business | HIGH | 40 → 80 | Assumption | DATA-001 |
| Q3 | 1 | … | Technical | MEDIUM | 60 → 60 | Blocked: needs dev DB access | — |

Status values: Pending · Investigating · Answered, not folded · Resolved · Assumption · Deferred (carried to next pass) · Blocked · Dropped (failed the scope gate on closer look; reason in notes). A Reframed question is replaced by a new row marked Pending with "reframed from Qn" in its notes.

## Question notes
One block per question that is not simply Resolved — required for Deferred, Blocked, and Answered-not-folded — holding the current proposed answer, evidence pointers (file:line, query, doc section), and what was checked. This is what the next investigation starts from and what a resumed session folds from.

### Q3
Proposed answer: … Evidence: … Checked: …

## Exploration scripts
| Script | Question | Finding |
|---|---|---|

## Noticed, out of scope
- {one line each — things investigation tripped over that fail the scope gate}

## Blockers
| Blocker | Questions affected | What unblocks it |
|---|---|---|

## Next action
{The single next thing to do. A resuming session starts here.}
```

---

## Orchestration Model

The orchestrator stays thin. It reads the state file, decides what to do next, launches subagents up to the concurrency limit, and records each result. It does not read full documents or do investigation itself.

| Step | Who | Returns to the orchestrator |
|------|-----|------------------------------|
| Setup / re-orientation | Orchestrator | — |
| Discovery | One subagent running `implementation-readiness-check` | Ranked question list, capped; each entry a few lines |
| Investigate one question | One `investigate-question` subagent | Verdict, confidence, the answer as document-ready prose, evidence pointers — a few hundred words, not a report |
| Fold one answer | One writer subagent, never more than one at a time | What changed, where — a few lines |
| Conformance | One subagent per pass | Issues found and fixed — a short list |
| Convergence, checkpoint | Orchestrator | — |

Subagents return distilled results, not transcripts. If a subagent's result would run past a page, it is doing too much per call — split the work.

### Interruption Recovery

If the session ends at any point:

- Every question already marked Resolved or Assumption is in the documents. Nothing to redo.
- Questions marked Investigating were in flight (at most three). On resume, re-run them; that is the whole cost.
- A question marked Answered, not folded has its answer in **Question notes**. On resume, fold it first; no re-investigation.
- The state file's **Next action** says where to pick up.

If a subagent fails, retry once. If it fails again:
- **Investigator:** mark the question Blocked with the error and continue with the next question.
- **Writer:** the answer is already known — never discard it. Record it verbatim under **Question notes**, mark the question Answered, not folded, and retry the fold before launching the next investigation.
- **Discovery:** the pass cannot proceed. Set Status to `Paused: discovery failed` with the error and report to the user.
- **Conformance:** skip it for this pass, note the skip in the state file, and run it at the next checkpoint.
- **Final verification:** report the documents as not verified; do not mark them ready.

Never let one failure end a pass.

If a session-limit or context warning appears: finish the in-flight question, update the state file, set Status to `Paused: session limit`, and stop cleanly. Do not start new questions into a closing window.

---

## Process

### Phase 1: Setup and Re-orientation

1. **Check for a state file** at the expected location. If present, read it, confirm the documents still exist, and continue from **Next action**. Do not restart from discovery unless the state file says the current pass is complete.
2. **If starting fresh**, locate all requirements documents — PRD, technical design, assumptions (if any), and supporting materials the documents reference — and create the state file from the template. Record the paths, the PRD's word count, and the existing code posture; do not read full contents here (search the PRD and design for a stated posture rather than reading them whole).
3. **Verify environment access** — databases, APIs, infrastructure, whatever investigation may need. Record limitations up front under Blockers rather than discovering them mid-pass.
4. **Confirm the repo state** — the documents' branch, and that the tree is clean apart from the requirements documents and state file. Record the branch in the state file.

### Phase 2: Discovery (once per pass)

Launch **one** subagent to run `implementation-readiness-check` against all the requirements documents, including supporting materials, with the scope gate and the existing code posture in its instructions. (That skill is not model-invocable; the subagent reads its SKILL.md and follows it.) It returns questions with proposed answers, confidence, impact, and Technical/Business classification.

Pass the subagent the state file too. A question is **new** only if it is not already tracked there under any status and is not on the out-of-scope list. Everything else the subagent would have raised is a repeat — it reports the repeat count and moves on. This is what makes the Surfaced count and the yield stop mean something.

The subagent must:
- Apply the scope gate before including anything
- Do its homework — answer by reading code where reading code answers it, and not raise those
- Skip questions the assumptions document already dispositions, unless it found evidence the assumption is wrong
- Return at most **2× the per-pass cap** candidates, ranked by impact and uncertainty (HIGH impact and low confidence first)

The orchestrator takes the top **Questions per pass** into this pass, marks the rest Deferred in the state file, and records the pass's Surfaced (new) and Taken counts.

**Questions carried from a prior pass** (Deferred, or Blocked with the blocker cleared) come first in the ranking. Draining the backlog beats surfacing new questions.

### Phase 3: Resolve, One Question at a Time

For each question in the pass, in rank order, with at most **Concurrent investigations** in flight:

1. **Triage.** A pure business-judgment question — one no amount of technical investigation can move — skips investigation (that is `investigate-question`'s own exclusion) and goes straight to step 3 as an assumption at the best-supported answer. Everything else proceeds.
2. **Mark it Investigating** in the state file, then **investigate** — launch `investigate-question` in a subagent with the question, proposed answer, confidence, impact, classification, the existing code posture, the **Question notes** evidence so far, and the document paths. It returns a verdict (Resolved / Refined / Blocked / Reframed), confidence, the answer written as document-ready prose, evidence pointers, and any exploration script it created.
3. **Fold immediately** — launch a writer subagent to integrate that one answer into the right document and section, following the disposition rules below, the writing standard for the target document (for the design, including its section on existing systems) and the existing code posture. Integrate into the most relevant existing section; create a section only when nothing fits. **Folds are serialized:** investigations may overlap, but only one writer runs at a time, so two writers never touch the same document at once.
4. **Update the state file** — status, confidence, where it landed, the script (if any), the **Question notes** block for anything not simply Resolved, and **Next action**.

Do not batch steps 3–4 for later. The pass's value is only as safe as the last question written.

#### Disposition rules

- **Technical, confidence ≥ 90%:** fold into the Technical Design.
- **Technical, confidence < 90%:** mark Deferred for another pass, with the improved answer and evidence in **Question notes**. Do not park a technical decision in the stakeholder-facing assumptions document to make the counts look clean. If a technical question is deferred in two consecutive passes at unchanged confidence, investigation has hit its ceiling: record it in the Technical Design as an explicit design decision with rationale and the evidence gap stated, and mark it Resolved by decision — an engineer must choose, and the design is where that choice belongs.
- **Business, ≥ 95%, whatever the impact:** fold the decision into the PRD.
- **Business, < 95%:** write it as an assumption stating the best-supported implementable answer, following `assumptions-document-writing` — plain-language proposed answer, why we believe it, confidence, impact, confirm-or-correct format. Technical detail the stakeholder cannot judge goes in the Technical Design, not the assumption. Proceed on that basis; stakeholder validation is asynchronous and is not a reason to pause. Use a Blocking Open Question only for the rare case that skill defines.
- **Blocked:** record what is needed. If three or more questions share one blocker, pause and report rather than continuing degraded.
- **Reframed:** the investigation showed the question was wrong. Mark the original Dropped (reason: reframed) and add the reframed question as a new Pending row noting its origin; it competes for a slot in the next pass on its own merits.

### Phase 4: Conformance (once per pass)

After the pass's questions are landed, launch one subagent to read all requirements documents and check placement and standards. It fixes what it finds and returns a short list.

| If it finds… | It belongs in… |
|---|---|
| Technical implementation detail in Assumptions | Technical Design |
| Business rules stated as technical specs in the Technical Design | PRD (if policy) or Assumptions (if uncertain) |
| Code-level decisions in the PRD | Technical Design |
| Open questions stated as facts | Assumptions |
| Decision history (who ruled what, when; superseded versions; dated correction notes), or descriptions of how existing code works, in the Technical Design | Removed; git keeps the history. Keep the decision as it stands now |
| Design built around code the posture says to salvage and switch off | One line in the Existing Code section saying it is switched off |

**Relocate, never delete.** The exceptions are the decision history and descriptions of existing code in the row above, which git already keeps, and superseded entry text and edit narratives in the assumptions document, which version control likewise keeps (`assumptions-document-writing`). Every other detail is preserved — copied to the right document, integrated (not appended), then removed from the wrong one. Apply each document's writing standard. Verify cross-document links and assumption-ID references resolve.

Conformance also confirms that the Technical Design's Open Questions section, and any statement it makes about which PRD acceptance criteria or assumptions it covers, are still true after this pass's edits. Anything conformance cannot fix because it is design work, not placement, goes into the state file as a Pending question for the next pass — not into a report the next session never reads.

### Phase 5: Checkpoint

1. Update the Passes table and **Next action** in the state file.
2. Stage the requirements documents and the state file — only those files; exploration scripts are the user's to stage — and include a proposed commit message in the checkpoint summary: `docs({feature}): requirements refinement pass {N} — {one-line summary}`, with a body naming what changed. **The skill does not run `git commit` unless the user explicitly says to.** The pass boundary is the user's review point; committing there is what protects the work from other sessions' git operations in the same checkout, so make the message good enough to use as-is.
3. Output the checkpoint summary:

```
=== Pass {N} complete ===
Surfaced (new) {S} · taken {T} · resolved {R} · assumptions {A} · deferred {D} · blocked {B} · dropped {X}
Documents: PRD +{n}/-{m} ({start} → {now} words) · TD +{n}/-{m} ({now} words) · Assumptions +{n}/-{m} ({k} entries)
Exploration scripts this pass: {list or none} (not staged — yours to add)
Out of scope noticed: {count} (see state file)
Blockers: {list or none}
Staged for review — proposed commit message follows
Next: {pass N+1 | final verification | paused: reason}
```

### Phase 6: Convergence

Using the state file's counts only:

- **Stop and go to Phase 7** when the pass's discovery surfaced fewer than **Discovery yield stop** new questions below the threshold and no Deferred questions remain, or when **Maximum passes** is reached.
- **Otherwise start the next pass** at Phase 2.

An implementable business assumption written to standard counts as dispositioned. It is not unresolved merely because stakeholder validation is still pending.

**Pause and report to the user** instead of continuing when:
- A business question genuinely meets the Blocking Open Question standard in `assumptions-document-writing`
- Three or more questions are blocked by the same missing access or prerequisite
- Two consecutive passes each resolved fewer than two questions — the run has hit a ceiling worth a human look
- The PRD (`wc -w` at the checkpoint) has grown by more than a quarter and more than 500 words since the growth baseline. Refinement clarifies requirements, so growth that large usually means scope or decision history is being added. Report what grew and let the user decide; if they say continue, reset the baseline to the current count

The ordinary count of business assumptions awaiting validation is never a reason to pause.

### Phase 7: Completion

1. **Final conformance pass** (as Phase 4).
2. **Final verification** — one more `implementation-readiness-check` subagent, scope-gated, against the finished documents. If it surfaces new questions below the threshold and passes remain, treat them as a new pass and go to Phase 3. If the maximum is reached with questions still below threshold, report `Maximum passes reached` and mark the documents not ready. Never label that result `Converged`.
3. **Write the completion report** (below) from the state file, while it still exists.
4. **Delete the state file.** The questions that mattered are in the documents; the rest is in the report.
5. **Final staging** — stage the requirements documents and the state-file deletion, and propose `docs({feature}): requirements refinement complete — {passes} passes, {questions} questions` for the user to review and commit. Put the **Noticed, out of scope** lines in the message body — once the state file is gone, the commit is their only durable home.
6. **Output the completion report:**

```
=== Autonomous Requirements Refinement Complete ===

Passes: {N}   Final status: {Converged | Maximum passes reached}
Existing code posture: {posture} (source: {source})   PRD words: {start} → {end}
Questions across all passes: {total} — resolved {R}, captured as assumptions {A}, still below threshold {W}

Document updates:
- PRD: {significant changes}
- Technical Design: {significant changes}
- Assumptions: {n} entries added or amended

Exploration scripts: {list, or none}
Out of scope, noticed and not acted on: {list from the state file}

Final verification: {clean | N questions, listed below}

Items below threshold (if any): {question — confidence — why}
Blockers not resolved (if any): {blocker — what's needed}

Ready for implementation? {Yes | No — items needing attention}

Recommended next steps:
1. Review assumptions awaiting business validation
2. Address blockers or final-verification items
3. Start the build with `implement-from-requirements`, which sizes the work and splits it with `phase-split` if needed
```

---

## Exploration Scripts

Investigation subagents create scripts in **`scripts/exploration/`** at the project root, per `investigate-question`:

- Descriptive names: `explore-notification-preference-codes.py`, `test-email-provider-api.py`
- Header comment stating the question being investigated
- **Read-only operations only** — SELECT, GET, list/describe/read
- **Dev and sandbox first** — read production only read-only, only when nothing else can answer the question, and only where the project allows it (`engineering-principles`, "Production Data")
- **Limit result sets** — TOP/LIMIT clauses

A script is warranted only when the question is in scope and a one-off read cannot answer it. Scripts written to audit systems outside the feature's scope are a sign the scope gate was skipped.

---

## Rules and Constraints

### DO

- Fold every answer into the documents the moment it is known
- Keep the state file current after every question; resume from it, never restart
- Apply the scope gate at discovery and again during investigation
- Take questions in impact-and-uncertainty order, backlog first
- Relocate misplaced content during conformance (never delete, except decision history and descriptions of existing code in the design, and superseded entry text and edit narratives in the assumptions document; see Phase 4)
- Follow each document's writing standard
- Document evidence and sources for findings
- Stop cleanly on a session-limit warning with the state file updated
- Delete the state file at completion

### DO NOT

- Write to production, or read it beyond what `engineering-principles`, "Production Data" allows
- Perform write operations (INSERT, UPDATE, DELETE, POST, PUT) against external systems
- Hold investigation results in memory for a later batch fold
- Run more than the configured concurrent investigations
- Run more than one writer at a time, or discard a known answer because its fold failed
- Fan discovery out across multiple parallel reviewers to be "thorough"
- Treat an exhaustive or "ultracode" session mode as license to exceed the caps or fan out discovery
- Investigate or script anything that fails the scope gate
- Regenerate the state file wholesale; update it in place
- Delete content during conformance cleanup, other than the decision history, descriptions of existing code, and superseded assumption-entry text and edit narratives Phase 4 names
- Continue past the maximum number of passes
- Pause merely because business assumptions await asynchronous validation
- Report completion when the final verification surfaced unresolved work
- Run `git commit` unless the user explicitly says to — stage only the requirements documents and state file, and hand the user the message
- Embed client-specific references (credential paths, private repo names) — those belong in your house engineering standards (README, "Plugging in your house engineering standards")

---

## Relationship to Other Skills

| Skill | How this skill uses it |
|-------|------------------------|
| `implementation-readiness-check` | Once per pass, scope-gated and capped, to surface and rank questions |
| `investigate-question` | One subagent per question, bounded concurrency |
| `assumptions-document-writing` | Applied when writing or amending any assumption, and during conformance |
| `technical-design-writing-standards` | Applied when folding into the design, and during conformance |
| `prd-writing-standards` | Applied when folding into the PRD, and during conformance |
| `review-technical-design` | Optional, runs before this skill: reviews a design with hard-to-reverse decisions, so refinement starts from a reviewed design |

---

## Example Walkthrough

### Starting state

```
PRD:          docs/prds/user-notifications/user-notifications-prd.md
Tech design:  docs/prds/user-notifications/technical-design.md
Assumptions:  (none yet)
State file:   (none — fresh run)
```

### Pass 1

- **Discovery** surfaces 23 candidates after the scope gate; the top 12 by impact and uncertainty are taken, 11 marked Deferred.
- **Resolve**, three at a time. Q1 (notification preference codes in the source system): subagent writes a read-only query, finds 12 codes mapping to 5 delivery channels, 55% → 98%, folded into the Technical Design's mapping section — state file updated before Q4 starts. Q2 (include deactivated accounts?): a meeting note says "import everything for audit trail", 40% → 80%, written as assumption DATA-001. Q7 is pure business judgment: written as an assumption at the best-supported answer. Q9 is blocked on database access; recorded. While investigating Q5, the subagent notices an unrelated retry bug in the sync job — one line under **Noticed, out of scope**, no investigation.

*The session ends here on a usage limit, mid-Q11.*

### Pass 1, resumed in a new session

- Phase 1 finds the state file: Q11 is Investigating, **Next action** says "re-run Q11, then Q12, then conformance." Q11 is re-run — the only cost of the interruption, because Q10 had already been folded.
- **Conformance** moves one API rate-limit detail from the assumption into the Technical Design; fixes a missing confidence line.
- **Checkpoint**: documents and state file staged; proposed message `docs(user notifications): requirements refinement pass 1 — preference mapping, deactivated-account policy, 9 of 12 resolved`. The user reviews and commits.

### Pass 2

- Discovery surfaces 6 new questions (the preference mapping added in pass 1 raised one about unknown codes) plus the 11 deferred, and Q9 rejoins them — its blocker cleared when the user granted the dev database access the pass 1 checkpoint listed. The top 12 are taken, Q9 among them. Ten resolve, including Q9, and two become assumptions.
- Checkpoint staged and reported.

### Pass 3

- Discovery surfaces 2 new questions — below the yield stop. With the 6 carried over from pass 2, all 8 are taken: six resolve, two become assumptions. No Deferred questions remain; convergence reached.

### Completion

- Final conformance clean. Final verification clean. State file deleted. Final staging. Report: 3 passes, Converged; 31 questions — 25 resolved, 6 captured as assumptions (4 awaiting validation), 0 still below threshold; ready for implementation.

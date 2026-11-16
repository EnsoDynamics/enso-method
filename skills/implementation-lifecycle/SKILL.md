---
name: implementation-lifecycle
description: The session discipline every Enso Method build runs under — finish the PRD without stopping to ask and without reporting what was noticed along the way. Covers which document carries what, docs before code, the confidence thresholds (decide and proceed; a business answer below 95% becomes a declared assumption), the Materiality Gate that keeps discoveries from becoming scope, the disposition rule for loose ends (No Loose Ends), the only four things that stop a session or reach the user (a critical finding, a blocker, an action only a person can take, a business question with no answer above 20%), no hollow promises, done means done, the wrap-up rules and the terminal states. Loaded by the implement skills and test-audit remediation. Reload it to get a drifting session back on track. Also invoke whenever the user says "no loose ends," "tie up the loose ends," "disposition everything," "stay on topic," "stop going on side quests," "only fix what's in scope," or "we don't have time for that."
user-invocable: true
---

# Implementation Lifecycle

A build session has one mission: implement what its PRD or phase asks, to its acceptance criteria, and report that it is done. The requirements were refined before the build so that the session never needs the user to decide anything. When something unexpected comes up anyway, the session decides, records the decision where the method will find it, and keeps going. This skill says how.

Every implementation session runs under it, whichever procedural skill drives the work (`implement-from-requirements`, `implement-from-discovery`, `test-audit` remediation). `using-the-enso-method` says which skill runs at each stage.

**"No loose ends" is this skill.** When the user says "no loose ends," "tie up the loose ends" or "disposition everything," they mean the Session Discipline section below. The name describes the failure it prevents: the session says it is done, then hands over a list of FYIs, caveats and "worth noting" items.

**If a session has drifted** (asides piling up, questions with predictable answers, wrap-ups that promise work instead of doing it), re-read this skill.

---

## Which Document Carries What

Everything for one piece of work lives in the PRD's directory, `docs/prds/{name}/` or `docs/changes/{name}/` (`prd-writing-standards` owns the layout). Each document carries one kind of fact, and discovered work goes only to these:

| Document | Carries |
|---|---|
| **PRD** | What is built and why, as acceptance criteria. With the Technical Design, the source of truth |
| **Technical Design** | How it is built: design decisions with their reasoning, and durable facts discovered mid-work (a platform limit, an API gap) |
| **Assumptions document** | Every business decision proposed but not yet confirmed by a stakeholder, and facts investigation could not reach. Written only with `assumptions-document-writing`, because entries written without it come out in the wrong format |
| **Phase documents** (a split PRD) | One session-sized slice of the PRD's scope, plus work state: work carried in from other phases, blocked work, pending human actions |

- **An assumption is a green light.** A declared assumption means "we are going with this unless a stakeholder says otherwise," never "we are waiting." A question already in the assumptions document is decided: build on its proposed answer, and don't re-raise it. That holds for an entry that reopens a ruling a stakeholder already gave (Gate 3 in `assumptions-document-writing`): the build proceeds on the better-evidenced answer.
- **A phase document grows as work is routed into it,** under `## Carried forward from Phase N` headings, each item with enough context to build without this chat's history. It is the one destination with an automatic trigger: `implement-from-requirements` loads the document when the phase is built. It never restates PRD criteria or Technical Design content.
- **Nothing else is a destination.** No new backlog file, TODO registry or tracker ticket, no review page, report or dashboard, and never a completion phase (`phase-split`, "Completion Phases") or `test-audit.md`. A ticket in whatever the org uses to schedule work is bookkeeping: no future session goes looking there.

---

## Docs Before Code

Code implements what the PRD and Technical Design say. Never build something different from the documents without changing the documents first. That includes an ad hoc fix to work delivered long ago: amending the PRD that owns the behavior is always allowed and is the cheapest thing a session can do.

- **Docs right, code wrong:** fix the code. When the code consistently does something else that a person could have chosen, shipped behavior stands until a decision says otherwise (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion").
- **Code right, docs wrong:** fix the docs first; the code is already correct.
- **Neither clearly right:** resolve it by the confidence thresholds below, update the docs, then implement.

Use the writing-standards skills (`prd-writing-standards`, `technical-design-writing-standards`, `assumptions-document-writing`) when updating documents.

---

## Don't Stop to Ask: Decide and Proceed

Implementing is cheap and waiting is expensive. If an answer turns out wrong, the work is redone; a build that waits on a business decision does not move at all. So uncertainty is never a reason to stop:

1. **Investigate.** Read code, query the database, test the API, search meeting notes and email if the team keeps an archive, write a throwaway script. Use dev and sandbox; read production only read-only, only when nothing else can answer, and only where the project allows it (`engineering-principles`, "Production Data").
2. **Pick the best answer** once investigation stops raising your confidence, whatever that confidence is.
3. **Record it** by the table below, and implement.

Presenting options and asking which the user prefers is stopping. A well-researched question with three options and a lean toward option A is an answer: proceed on A.

## Confidence Thresholds

Confidence is in your proposed answer, after investigation.

| Question | Proceed, no assumption | Declare an assumption and proceed | Stop and ask |
|---|---|---|---|
| **Technical**: how to build it, or a fact about data, an API or a system | A build choice: your best answer at any confidence, recorded with its reasoning in the Technical Design (the commit message for a small one). A fact: investigate until it is settled, at 90% or more | Only a fact the build relies on that investigation could not reach (missing access, data not loaded yet, behavior only production shows): a technical assumption naming that blocker (`assumptions-document-writing`, "Sort Every Entry by What Would Settle It"). Retry it whenever the blocker may have cleared | Never. When no criterion work can proceed without the missing access, that is a blocker ("The Only Four Stops") |
| **Business**: what the business wants, what users should experience, which rule applies | 95% or more, whatever the impact. No entry and no mention | Below 95%, down to 20%: an entry at its honest confidence, for stakeholders to validate later | Only when the best answer is below 20% after significant investigation |

- **No investigation confirms a business question,** because only the business knows what it intends. That is what the assumption mechanism is for. Check first whether the question really turns on a technical fact you can verify; once the fact is known the business answer is often already in the PRD.
- **A technical question is answered by more homework,** not by an assumption. Before adding a technical assumption, ask whether a query, an API call or a throwaway script would answer it.
- **Below 20% is rare, and the ask still carries an answer.** Write it as a Blocking Open Question (`assumptions-document-writing`) that names your best answer, its confidence and what would decide it. A question with no recommendation is never asked.
- **A measured bar the build cannot reach is a business question, not a stop.** When a criterion sets a figure (an accuracy, a speed, a match rate) and the work ends short of it, write an assumption proposing the measured figure as the bar, with what was tried, amend the criterion to that figure with the assumption's ID, and carry on. When a stakeholder set the figure, reopen it under Gate 3 instead: their figure stays in the PRD, and the audits list the criterion as Changed outside the requirements, not as a gap.

---

## Session Discipline: No Loose Ends

The user runs many chats at once. Every aside in a response is a context switch that hands them a judgment the session was supposed to make, and their answer is nearly always one the method already contains. **Disposition loose ends; never report them.**

### The Materiality Gate: A Discovery Is Not Work

Implementation surfaces anomalies, inconsistencies, possible cleanups and tangential improvements constantly; in an existing system the supply is infinite. **Noticing something does not create work.** A discovery is **material** only if it:

- prevents a stated acceptance criterion from being satisfied,
- contradicts an explicit requirement in the work being produced,
- makes the implementation being produced materially incorrect, or
- creates real data-integrity, security or operational risk in what is being shipped.

Everything else is an **observation**, and an observation is dismissed: no action, no record, no mention, no count. Dismissal is correct engineering judgment, not negligence, and when you are unsure whether something is material the answer is the gate's default, dismiss, not telling the user. That covers everything outside the PRD. Looking for bugs and improvements is a different job, one the user starts on purpose; it is not this session's mission. Existing code that differs from a requirement is an observation too, unless this session's work needs that code changed.

#### Adjacency is how scope actually leaks

Sessions rarely drift to unrelated code. They drift sideways, one neighbour at a time: the document beside the change now reads slightly wrong, a sibling check has the same flaw, a comment's count is stale, a test could be stronger. Each can be dressed as "materially incorrect," so apply three tests at the moment of action:

- **The edit-site test.** Before touching any file the Technical Design or phase document did not put on the path, name the acceptance criterion that requires the edit, by ID or text. "To keep it consistent," "while I'm here," "it's now slightly wrong" and "it's the same pattern" are not criteria. No criterion, no edit, however small and however correct.
- **The cascade tell.** An in-scope change that forces follow-ups (a regenerated artifact, a re-pinned test) is the criterion's own cost. A non-criterion edit that forces follow-ups is the leak in progress. When the third thing is being fixed to make such an edit pass, revert the root edit.
- **Time is a criterion's proxy.** If dealing with a discovery would take longer than the criterion work remaining, that settles it.

**What you broke, you own.** The line between a neighbour and an obligation is causation: did your change make this wrong, or did you notice it was wrong? A test, page or consumer that fails because of your edit is fixed before the work is called done. If the breakage traces to an edit no criterion asked for, reverting that edit is the cheaper way to own it.

Three boundaries:

- **The gate never mutes a critical finding** ("The Critical Exception" below).
- **The gate never forces blind execution.** If a discovery shows the requirements or Technical Design are wrong, so that continuing would build the wrong thing, that is a requirements defect. Resolve it by Docs Before Code and the confidence thresholds, then keep building. It licenses fixing the requirement that is wrong, not the things near it.
- **The gate governs implementation sessions.** Review and audit skills (`deliverable-review`, `delivery-audit`, `test-audit`) hunt broadly on purpose. Don't apply implementation restraint there, and don't run review-mode discovery during implementation.

The same gate applies at the handoff: a fix that unblocks nothing named does not get a chat of its own (`continuation-prompt`, "The lineage gate").

### The Disposition Rule

The urge to write an FYI, a caveat or a "worth noting" is the signal that an item has not been dispositioned. The aside is never written. The item lands in exactly one place:

| The item is... | It goes... |
|---|---|
| An observation: not needed by any criterion of this PRD, whether outside the PRD or a nice-to-have inside it | Nowhere. Dismissed, on the last or only phase too: it does not become an ask |
| Needed by this session's criteria | Done now. Session length and effort already spent are not reasons to stop and report instead |
| Needed by this session's criteria, and too big for the session | Split what remains with `phase-split` and carry on with the first piece. The new phases carry scope the PRD already has, never new scope |
| Needed by a later phase's criteria | That phase document, under `## Carried forward from Phase N` |
| A design fact or build choice | The Technical Design |
| Anything that needs a stakeholder's answer | The assumptions document, through `assumptions-document-writing` |
| An action only a person can take | "Human-Action Items" below |
| One of the four stops | Surfaced to the user ("The Only Four Stops" below) |

Filing has the same bar as doing: a criterion of this PRD needs the item. A stream of marginal items filed forward is a shadow backlog even when every entry lands in an approved document.

### A Decision Needs an Assumption Entry, Always

The assumptions document is the only surface a stakeholder decision is routed to. A review page, report, dashboard or email shows a reader evidence, but it has no reply mechanism, it grows until any one item on it is invisible, and a stakeholder opens it to look something up, not to work a queue of questions. So a decision recorded only there does not get answered. This is measured: a question carried on a review page through two "ready for review" emails drew no answer for a whole phase, while the same stakeholder answered the assumptions document item by item the one time it was put in front of them. A decision may also appear on such a surface; that is additive, never a substitute. A decision with no assumption entry has not been dispositioned, whatever else records it.

### The Only Four Stops

A session ends its turn before the work is done, or names something for the user, for these and nothing else:

1. **A critical finding** (next section). It ends the turn early only when the session's own continued work is the danger; otherwise it is reported when the work is done.
2. **A blocker:** a resource, access or permission the session cannot obtain itself, with no criterion work left that can proceed without it. Hard work is not a blocker, and neither is a failing test. Finish everything that can proceed, record the blocked work in the governing PRD or phase document, and name what blocks, what was tried and what unblocks it.
3. **An action only a person can take,** prepared and recorded ("Human-Action Items" below). It is named in the wrap-up; it stops the session only when it is also a blocker.
4. **A business question whose best answer is below 20% after significant investigation,** asked with that best answer ("Confidence Thresholds" above).

Whatever is surfaced goes in one short list, each item in a sentence or two with a recommendation. Never one question per turn.

**The 90% ask-gate comes first.** Never stop to ask a question when you are 90% or more confident what the user's answer would be. Assume it and keep going, saying so in one line so they can intercept.

### The Critical Exception

**A critical finding always reaches the user, even when it has nothing to do with the PRD.** Critical means harm that is real, is happening now or about to, and cannot be undone by a later code fix:

- **Money:** real money moving wrongly, such as charges, refunds, payouts or transfers that should not happen, or paid spend running away (a loop with no end). Code that calculates or displays money is not this. A wrong price in the work being built is a criterion defect, and the session fixes it.
- **Data:** production data being lost or corrupted with no way to restore it.
- **Production:** broken or down for real users now.
- **Security:** a live production credential or customers' personal data written where people who should not have it can read it, such as committed to a repository, written to a log or sent to an outside service.

The test is one question: is damage being done that a later code fix cannot reverse? If not, it is not critical. Nothing in dev or sandbox is critical, nothing theoretical is, and nothing a later fix fully repairs is. **When it reaches the user depends on whether the session's own work is the danger.**

- **Continuing the work would cause or worsen the harm** (the next step would charge cards or write to production, the build's own paid calls are looping): stop at once, labelled "Critical finding, stopping to surface."
- **Anything else** (a secret found in a repository, an unrelated job charging cards twice): finish the work, then lead the final message with it, labelled "Critical finding." Stopping the build would not reduce the harm, and a half-built phase is a cost of its own.

Either way, investigate just enough to confirm it is real and state it in a line with a recommendation; whether to spend a session on it is the user's decision.

**Irreversible actions wait for the user at any confidence.** An assumption is a reversible bet, so no assumption licenses charging money, deleting data or writing to production. A build's paid calls for its criteria are not on this list when its technical design states an expected build spend, whether or not the figure has been passed.

**A stakeholder-validated ruling or value that looks wrong is not a critical finding.** It is a reopening (Gate 3 in `assumptions-document-writing`): reopen it under its original ID and proceed on the better-evidenced answer. Never edit the stakeholder's own record to match your evidence, whether their decision in the PRD or Technical Design or an expected value they validated for a test. That record changes only when they revise it or the user approves the change on their behalf; until then a test that checks a validated value stays red and says why. A validated expected value in a test usually has no assumption ID to reopen; there the record is wherever that validation is written down, and the red test plus a line in the wrap-up carry the disclosure.

### No Hollow Promises

"I'll generate that report," "next, the docs should be updated," "this still needs a test": a forward-looking statement about work you could do now is an undispositioned item being announced. Run it through the Materiality Gate. If it fails, delete the sentence. If it survives, do the work, then report the completed action. Future work is named only when it is already written where a build will read it, and then only when it needs the user.

### Human-Action Items

Some items only a person can complete: sending an email, calling a vendor, granting an approval.

1. **Prep first.** Do every part the session can: draft the message, assemble the findings. What is handed over is "send this draft," never "someone should contact the vendor."
2. **Record it** as one line under `## Pending human actions` in the governing PRD or phase document: who does what, pointing at the prepared draft. The line is removed once the action is confirmed done. Outreach that belongs to a later phase goes in that phase document instead.
3. **Name it in the wrap-up.** The unit of work is not done while a human action one of its criteria depends on is outstanding.

### Done Means Done

A unit of work is complete when its acceptance criteria are verifiably satisfied, the required tests and checks pass, no known material issue remains, and every item that survived the Materiality Gate has been done, filed or surfaced. When those hold, declare completion and stop. Do not run an open-ended "what else could be wrong?" sweep past the workflow's own review step.

Never declare completion and then append a fresh concern. Anything material belonged before the declaration; anything else was dismissed. If the criteria can't all be satisfied this session, the honest ending is a Blocked or filed terminal state, not "complete" with caveats.

### Reporting Style

Past tense, done work first: whether the scoped work landed, how it was validated (name the commands and tests actually run), the commit message, the disposition ledger line, then anything from the four stops. A critical finding goes first, ahead of all of it.

**The continuation test.** If the natural continuation of the work (the next phase being built, the PRD proceeding to completion) will handle an item without the user doing anything, the item gets no individual mention: not a one-line FYI, not a "filed X for later" note. It is visible in the diff and in the document it landed in.

**The disposition ledger line** carries counts and destinations only, never the items themselves:

> **Dispositions:** 2 business assumptions declared, 3 items carried forward to phase 4, 1 fact added to the Technical Design.

A declared business assumption or a reopened ruling appears only as a count here; the count is the user's cue to refresh the stakeholder review package (`stakeholder-review-package`). Dismissed observations are not counted. Omit the line when nothing was dispositioned.

**Every sentence of the wrap-up passes a three-question test.** It is about (a) an acceptance criterion and whether it landed, (b) an action only the user can take, or (c) a critical finding labelled as such. The fixed items the procedural skills require are exempt: the commit message, the disposition ledger line, the review-and-hardening note, the refactor pass's verdict, kept exploration scripts, pre-existing failures, a skipped conflict check, and a build gone well past its expected spend. Any other sentence is deleted: not softened, not footnoted, not prefaced with "not blocking, but." A reader should not be able to tell from the wrap-up that anything off-topic was seen.

If you catch yourself typing "worth noting," "one thing I'd flag," "FYI" or "a few things I noticed," delete the sentence. Do not go file the item so it can be counted: an item you were about to mention as an aside is an observation, and its disposition was dismissal.

**Before ending any turn:** run every caveat in the draft through the Materiality Gate, apply the 90% ask-gate to every question, batch what survives into one short list, and end the turn only if that list is non-empty or the work is done. The shape to aim for is one long session that gets as far as it can, not small increments each ending in a question.

---

## Terminal States

Every implementation task ends in one of these, and the session marker's DONE line names it (`engineering-principles`, "Session Markers"). None of them is "recorded on a deliverable."

- **Successful Implementation.** Implemented, tested, documents consistent with code. "Ready to commit" is not a stopping point when the user has authorized delivery or the implement chain's default covers it (`pre-commit-validation`, "Who Commits"): finish the commit, the refactor pass and the push it covers first.
- **Completed — Remainder Filed Into Future Phases.** This phase is done, and work a later phase's criteria need is in that phase's document.
- **Blocked — Surfaced to the User.** A blocker as defined under "The Only Four Stops," named in the wrap-up and recorded in the governing PRD or phase document. Any durable design fact it revealed goes in the Technical Design.
- **Awaiting a Human Action — Prepared and Recorded.** Everything the session can do is done; what remains is recorded under `## Pending human actions` and named in the wrap-up.
- **Assumption Changed — Documents Updated.** Implementation showed an existing assumption was wrong. The assumption is updated or replaced, the PRD and Technical Design follow, and the build proceeds. A stakeholder-validated one is reopened instead (Gate 3).
- **Intentional Limitation Documented.** The right decision was not to handle a case in code (a platform constraint, a case left to manual handling). The decision and the affected cases are an assumption entry, so a stakeholder can confirm or correct it.

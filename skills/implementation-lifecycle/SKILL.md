---
name: implementation-lifecycle
description: The umbrella skill for the implementation methodology — how PRDs, technical designs, assumptions, and phase documents work together, plus the No Loose Ends session discipline every implementation session runs under. Covers the assumptions philosophy, confidence thresholds, decision flow, the materiality gate that keeps discoveries from becoming scope, the disposition rule for loose ends, the no-hollow-promises rule, the lineage gate, session markers, the done-means-done completion standard, and acceptable terminal states. Loaded automatically when implementing features, resolving gaps, or working from PRDs/technical designs. Also invoke whenever the user mentions loose ends — "make sure there are no loose ends," "tie up the loose ends," "disposition everything" — that discipline lives here. Reload it to get a drifting session back on track. Invoke it whenever the user says "stay on topic," "stop going on side quests," "only fix what's in scope," or "we don't have time for that."
user-invocable: true
---

# Implementation Lifecycle

How implementation works in this method. This is the single umbrella skill: the framework (philosophy and decision logic) plus the **No Loose Ends** session discipline (how a session behaves around decisions — disposition of loose ends, when to ask, how to report). For procedural steps, see the specific skills referenced throughout.

**"No loose ends" is this skill.** When the user says anything about loose ends — "make sure there are no loose ends," "no loose ends on this one" — they mean the Session Discipline section below. The name describes the failure it prevents: the AI says it's done, then hands over a list of FYIs, caveats, and "worth noting" items that are all undispositioned loose ends.

**If a session has drifted** — FYIs and caveats piling up, stopping to ask questions with predictable answers, wrap-ups that promise future work instead of doing it — re-reading this skill is the way back on track. Everything below applies to every implementation session, whichever procedural skill is driving it.

---

## The Four Entities

Every implementation area has up to four documents. They form a system. **All of them colocate inside the PRD's directory**, which lives under `docs/prds/` (a program) or `docs/changes/` (a bounded delivery — identical layout, identical handling; a directory in either root is what this skill means by "PRD") — see `prd-writing-standards` for the directory layout. The first three exist (or can exist) for every implementation area; phase documents exist only when the PRD has been split, but once they exist they are full entities, not scratch notes.

| Entity | Purpose | Location |
|--------|---------|---------|
| **PRD** | What we're building and why. Acceptance criteria. Scope. | `docs/prds/{feature}/{feature}-prd.md` |
| **Technical Design** | How we're building it. Data flows, mappings, integration points. | `docs/prds/{feature}/technical-design.md` |
| **Assumptions Document** | Business decisions we've proposed but haven't confirmed with stakeholders. | `docs/prds/{feature}/assumptions.md` |
| **Phase Documents** (when split) | Scope contract for one AI-session-sized slice of the PRD, plus the ledger of work routed into that phase from elsewhere. One file per phase at every depth; a phase that was split keeps its file as a short split record. | `docs/prds/{feature}/phase-{id}-{short-name}.md` — ids are positional (`2`, `2a`, `2a1`); `phase-split` owns the scheme |

Paths above show `docs/prds/`; a `docs/changes/` directory is identical.

**Upstream of the PRD, when an idea was too big for one:** a full brief and a PRD roadmap in `docs/roadmaps/{name}/` (`prd-roadmap` owns them). The full brief holds decisions that govern every PRD cut from it; the roadmap orders the planned PRDs. They are inputs to requirements work, not entities an implement session maintains. The one exception is the roadmap's Status column, which moves when a PRD is written and when its work reaches production.

**Beside them, once a test audit has run:** `test-audit.md` in the PRD's directory, the map of each criterion's test evidence. `test-audit` owns it, and only a `test-audit` session writes it; it is never a destination for discovered work.

**PRD and Technical Design are the source of truth.** Code implements what they say. If code and docs disagree, figure out which is right — fix the wrong one. Never implement something different from what the docs say without updating the docs first — and that includes ad hoc fixes to work delivered long ago: amending the PRD that owns the behavior is always allowed and is the cheapest thing a session can do. A change directory (`prd-writing-standards`, storage convention) is for work the user chooses to write up on its own, never a way around an amendment. When a later PRD or change directory changes behavior an earlier one defined, the later one owns it and the earlier one is not rewritten (see "When Later Work Changes Earlier Requirements" below).

**Assumptions Document is a green light.** A declared assumption means "we're going with this unless stakeholders tell us otherwise." It does NOT mean "we're waiting for confirmation." The whole point is to keep moving. That is not a rule with exceptions — it is what an assumption *is* — and it holds for an entry that reopens a ruling a stakeholder already gave (Gate 3 in `assumptions-document-writing`): the build proceeds on the better-evidenced answer; what a reopened entry owes is louder disclosure, not a hold. **When adding assumptions, always use the `assumptions-document-writing` skill** — assumptions have a specific format (proposed answer, rationale, confidence, impact, confirm-or-correct checkboxes) and they consistently get written incorrectly without referencing that skill.

**Phase Documents are born thin and grow into ledgers.** At creation (`phase-split`), a phase doc is a thin scope overlay — AC labels, dependencies, a summary. Over the project's life it legitimately accumulates the work routed into it: "Carried forward from Phase N" / "Inherited from Phase N" sections carrying items discovered in other phases, each with enough context for the implementing session to execute without the originating chat's history. That growth is the system working as designed, because **a future phase doc is the preferred landing place for discovered follow-up work that survives the Materiality Gate** (see Session Discipline below — most discoveries dismiss instead) — it's the one destination with an automatic trigger: `implement-from-requirements` loads the doc when the phase is built. Nothing automatically comes back for a ticket in whatever the org uses to schedule work. The one kind of growth that stays forbidden is duplication — a phase doc never restates PRD acceptance criteria or Technical Design content; it carries routed work, not copied requirements.

**Blockers are surfaced, never filed away.** A blocker is material by definition, so it goes to bucket 3 — surface it to the user now, with the blocked work recorded in the governing PRD/phase doc so the continuation sees it (and any durable design fact the blocker revealed folded into the Technical Design). Whatever the org uses to schedule work sits outside this methodology — a ticket is fine as bookkeeping, but it is not a disposition on its own: nothing triggers a future session to go look there, so work inside the current PRD must still be carried by its governing doc.

---

## Core Philosophy

### Implementation Is Cheap

With AI, implementing is fast. If an assumption turns out to be wrong, we re-implement. The cost of backtracking is low. The cost of waiting for business decisions is high. We never block on stakeholder feedback.

### Don't Stop to Ask — Decide and Proceed

When you encounter uncertainty, the answer is almost never "stop and ask the user." If you've done thorough investigation and have a proposed answer, **you have everything you need to proceed**, whatever its confidence. If it's a business question, declare it as an assumption; either way, implement it.

This applies even when the question is well-framed with clear options. Presenting the user with "Option A, B, or C — which do you prefer?" is still stopping and waiting. If your investigation points to option A with good reasoning, pick option A, document it as an assumption, and implement. The user validates asynchronously — not in the middle of your implementation flow.

The only time you stop and ask is when you cannot put forward an answer at all: the evidence favors none of the options over the others (in practice, a best answer under roughly 20%). A weak best guess is still a guess — it gets declared at its honest confidence, and the work proceeds on it.

**The workflow when uncertainty arises:**

1. **Investigate first** — read code, query databases, check APIs, search meeting notes and emails if the team keeps an archive, read documentation, write exploration scripts. Can you self-resolve to 95%+?
2. **Once investigation stops raising your confidence** — you're done deliberating. Pick your best answer at whatever confidence it has; if it's a business question below 95%, document it as an assumption; implement it.
3. **If you cannot put forward an answer at all** — the evidence favors none of the options — stop and ask. Name the options and what would decide between them. This is rare.

Stakeholders validate assumptions asynchronously. We correct course if they say we're wrong. But we don't wait.

### Docs Before Code

Before changing code, align the documents:

- **Docs right, code wrong** → fix the code; when the code consistently does something else instead, first apply "When Later Work Changes Earlier Requirements" below: shipped behavior someone could have chosen is not reverted to match a document without a decision
- **Code right, docs wrong** → fix the docs first, then code is already correct
- **Neither clearly right** → resolve through investigation or assumption, update docs, then implement

Use the writing standards skills (`prd-writing-standards`, `technical-design-writing-standards`, `assumptions-document-writing`) when updating documents.

---

## Confidence Thresholds

Confidence levels drive what action to take. These thresholds appear across multiple skills — here's the unified view.

| Confidence | What It Means | Action |
|-----------|---------------|--------|
| **95%+** | You're sure enough. | Just do it, whatever the impact. No need to disclose or ask. Don't fatigue stakeholders with things you're confident about. |
| **Below 95%** | Some uncertainty, slight to large. | **Research more first.** Exhaust investigation avenues — database queries, API tests, codebase analysis, meeting-note searches, web documentation, exploration scripts (`scripts/exploration/`). If still below 95% after research, put forward your best answer at the confidence it has, document it as an assumption using the `assumptions-document-writing` skill, and implement — at 30% as much as at 90%. Do NOT stop and present options to the user. |
| **No answer to put forward** | The evidence favors none of the options — in practice, a best answer under roughly 20%. | Stop and ask: a Blocking Open Question (`assumptions-document-writing`) naming the options and what would decide between them. Rare. |

**That table is the shared spine; the operative gate is two-tiered.** Which tier applies depends on whether the question is technical or business — the distinction defined in the next section. This is the gate the implement skills actually run, and the one the Session Discipline section below refers to as "the confidence gates":

| Question type | Proceed on your own | Declare a formal assumption | Stop and ask |
|---|---|---|---|
| **Technical** | Proceed on your best answer at whatever confidence, noting the reasoning in the commit message where it isn't obvious | Rarely — only when the choice is one a business stakeholder could meaningfully validate | Only when no answer can be put forward, after investigation |
| **Business** | 95%+, whatever the impact | Below 95% — a formal entry via `assumptions-document-writing` at its honest confidence, for asynchronous stakeholder validation | Only when no answer can be put forward |

Both tiers share one stop: no answer the evidence favors. Anything short of that proceeds.

### Technical vs Business Uncertainty

Not all uncertainty is the same. How you handle it depends on what kind of question it is.

**Technical questions** — about data characteristics, API behavior, field values, system constraints. These can almost always be self-resolved through investigation: query the database, test the API, read the code, write an exploration script or a temporary program. **Keep doing homework until the question is answered — more investigation nearly always gets there.** The safety rule for that probing: investigate in dev and sandbox environments; read production only read-only, only when nothing else can answer the question, and only where the project allows it (`engineering-principles`, "Production Data"); never write to production. Technical questions should rarely become formal assumptions — if you're about to add a technical assumption, ask yourself: "Could I answer this with a database query, an API call, or a quick throwaway script?" If yes, do that instead. And if a technical assumption does get declared, it's still yours to confirm: further investigation can usually verify it after the fact, so do that rather than leaving it hanging.

**Business logic questions** — about what the business wants, how users expect things to work, what the correct policy is. **These cannot be self-confirmed — no amount of investigation tells you what the business intends.** They are what the assumption mechanism exists for: propose the best answer, declare it, proceed, and route it to a stakeholder for validation. But check first: sometimes what looks like a business decision actually depends on a technical fact you can verify. Resolve the technical fact first — the business decision often becomes obvious once you know the data.

**Example:** "Should we include deactivated accounts?" sounds like a business question. But if the PRD says "import all historical user records for audit trail purposes," and deactivated accounts are historical records, the business decision is already made — you just need to verify the technical path for importing them.

### The Key Insight

The goal is always to **raise confidence through investigation**, not to immediately declare assumptions. Assumptions are for when you've done your homework and genuine uncertainty remains — not a shortcut to skip research.

**But once you've done that homework, proceed.** If you've thoroughly investigated and have a best answer, you are not blocked, whatever its confidence. Document it as an assumption if it's a business question, and implement. The user does not need to be consulted — that's the entire point of this framework. Presenting well-researched options and asking the user to pick one is the same as blocking on a business decision, which is exactly what this framework is designed to avoid.

---

## Decision Flow During Implementation

This flow is for questions the current work needs answered in order to proceed. A mid-implementation discovery is not automatically such a question — it first passes the Materiality Gate (Session Discipline below), and a dismissed observation never enters this flow or its investigation loop.

When you encounter a question or gap while implementing:

```
Question arises
    │
    ├─ Is this already in the assumptions document?
    │   └─ Yes → Treat it as decided. Implement per the proposed answer. Done.
    │
    ├─ Can I self-resolve through investigation?
    │   ├─ Yes → Investigate. If confidence reaches 95%+, just proceed. Done.
    │   └─ Partially → Investigate to raise confidence as high as possible.
    │
    ├─ After investigation, can I put forward a best answer?
    │   ├─ Yes, at any confidence → Pick it. If it's a BUSINESS question, declare an
    │   │        assumption (use the assumptions-document-writing skill); technical
    │   │        ones rarely need one — just proceed and note the reasoning in the
    │   │        commit message. Implement. Do NOT present options to the user.
    │   └─ No — the evidence favors no option → Stop. Ask the user, naming the
    │            options and what would decide between them.
    │
    └─ Note: "I have a well-researched question with 3 clear options and I lean
       toward option A" means you have a best answer.
       Pick option A, proceed on it, implement it.
```

**Already-captured assumptions are decided.** Don't re-raise them, don't wait for validation, don't defer. The assumption process exists so we can keep moving. If an assumption is later found wrong, we'll re-implement — that's the designed workflow.

---

## When Later Work Changes Earlier Requirements

A system accumulates PRDs, and a later one often changes what an earlier one said. Rewriting every earlier PRD to describe the system as it is now is neither affordable nor honest, because each was true when it was built. So:

- **The latest-built document that defines a behavior owns it.** The earlier criterion gets a `Superseded by:` line pointing to the criterion that changed it, and the later criterion carries `Replaces:` (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion", owns the format and the partial forms). Follow `Superseded by:` lines to the end of the chain before treating any criterion as current.
- **An ad hoc change amends the owner,** the criterion at the end of the chain, never a fully superseded one. A partly superseded criterion still owns the part in force.
- **`Replaces:` is written with the PRD; `Superseded by:` is written when the replacing criterion is built,** in the same commit as its code. The replacing criterion requires that edit to the earlier PRD, so it is in scope.
- **A fully superseded criterion is no longer owed.** A build skips it, or builds only the part in force, and phase plans, test hardening, test audits and wrap-ups leave it out as they do retired labels, listing it as superseded.
- **Existing code that differs from a criterion is an observation unless this session's work needs that code changed.** Only then does this rule decide which side is right. Not every change goes through this method: a teammate may have changed behavior on purpose with no requirements written at all, and the code may be right.
  - **A plain bug** is a malfunction nobody would choose: a crash, an error, corrupted or inconsistent output. Fix it; nothing below applies.
  - **A consistent contradiction** is a coherent alternative a person could have chosen: a different value, threshold, status or step, or a behavior that is gone. First, the conflict check: if a later-built criterion changed this one, that one owns the behavior; add the missing pointer pair.
  - **Otherwise, shipped behavior stands until a decision says otherwise.** Reverting it to match a document is a business question whose proposed answer is to keep it, decided by the usual thresholds: at 95% or more, amend the owning criterion to match ("code right, docs wrong"), or below that, an assumption entry proposing to keep it, and proceed. If that criterion records a stakeholder's ruling, it is a reopening at any confidence (Gate 3 in `assumptions-document-writing`). Evidence moves the confidence, never the default: `git log -S'<value>'` or `git log -L` on the code (look past commits that only reformat or move lines), a test, comment or config entry asserting the current behavior, a commit that set it after the criterion was written. Squashed, vague or missing history (imported code) lowers confidence; it never makes reverting the default.
  - **A later decision wins:** the user's direct request, or the ticket or report this session serves naming that behavior. Then revert, and name the reverted commit, when there is one, in the commit message.
  - **Building a criterion that would change existing behavior,** rather than add it, follows the same rule when the code's history shows that behavior was changed after the criterion was written: it is a conflict-check finding, intended or a business question.
  - Without pointers, tell which criterion was built later from `**Closed:**` lines, the git history of the code that implements each criterion, and what the code does now.

**The conflict check.** Nobody remembers every earlier PRD, so finding the criteria that new work changes is a step, not the author's memory. One subagent reads the criteria being checked and every other criterion in the repo's PRD roots (`docs/prds/`, `docs/changes/`, or the repo's established equivalent), built or not. When the roots hold no other PRD or change directory, there is nothing to check. It skips retired labels and fully superseded criteria, which keeps the read small as the system grows; where there are many directories, it shortlists them by title and summary first, then reads the shortlisted criteria in full. It reports each criterion that the ones being checked change, narrow, contradict or remove, quoting both. A check for a criterion being amended also asks the reverse, whether a later-built criterion already changed it; a check before changing code to match a criterion asks only that. Each finding that decides what the session does is resolved one of two ways; any other finding is an observation for the Materiality Gate, not pointer work:

- **The change is intended** (the new PRD says so, or plainly means it): a `Replaces:` or `Replaces in part:` line on the new criterion.
- **It is not:** the new work would break behavior someone asked for. That is a business question, decided by the usual thresholds, never a silent pick: at 95% or more, either change the new criterion to keep the earlier behavior or accept the change with a `Replaces:` line; below 95%, an assumption. Overturning a criterion a stakeholder personally ruled on is a reopening at any confidence (Gate 3 in `assumptions-document-writing`).

**If the check's subagent fails,** retry once, then run the check in the main chat. If that fails too, proceed: the risk is no worse than before the check existed, and the tripwire below still stands. Record `Conflict check skipped: <reason>` in the wrap-up and the commit body, never a `Conflict check:` line, so the next build runs its own.

It runs at these points, and each skill carries its own step:

| Where | What it checks |
|---|---|
| `autonomous-requirements-refinement`, pass 1 | The whole PRD, with findings resolved as questions in the run; at completion, again for criteria the run added or changed after pass 1 |
| `implementation-readiness-check`, when run on its own | The whole PRD |
| `implement-from-requirements`, after sizing and before building | The criteria this session builds, narrowed by the last recorded check; with none, the whole PRD, recorded for later phases |
| `implement-from-discovery`, `test-audit`, and anywhere else code is about to change to match a criterion | Amending: the criterion, both ways. Matching code to a criterion it consistently contradicts: only whether a later-built criterion changed it; the shipped-behavior rule covers the rest. Skipped when a check in this session already covered it |

**The test tripwire catches what the check missed.** Before changing the expected result of an existing test the session did not write, or deleting one, check that something accounts for the change: a criterion or Technical Design decision the session builds, amends or enforces requires the new expectation, or, where no criterion speaks to the behavior, the defect the fix serves (its ticket, incident or report) does. A test that a criterion's own change forces to change is accounted for. If nothing accounts for it, the session is changing behavior nobody declared: resolve it by the Doc Divergence rule (`implement-from-requirements`), which ends either in a criterion that accounts for it (an amendment, or a `Replaces:` line and its back-pointer) or in putting the behavior back. Renaming or restructuring a test without changing what it expects does not trip it.

---

## Session Discipline: No Loose Ends

The framework above governs *what to decide*; this section governs *how the session behaves* around those decisions.

The user is often running several chats at once. Every FYI, caveat, "worth noting," or "one thing I'd flag" in a response is a context-switch tax — and the usual outcome is that the user just tells you the obvious disposition anyway ("deal with it" or "note it for later"). Skip that round trip. **Disposition loose ends; don't report them.**

### The Materiality Gate: A Discovery Is Not Work

Implementation surfaces discoveries constantly — anomalies, inconsistencies, possible cleanups, theoretical defects, tangential improvements. In a brownfield system the supply is infinite. **Noticing something does not create work.** Before an item enters the disposition buckets below, judge it against what this session is converging on. A discovery is **material** only if it:

- prevents a stated acceptance criterion from being satisfied,
- contradicts an explicit requirement (in the work being produced; existing code that differs from a requirement is an observation unless this session's work needs that code changed, and only then does "When Later Work Changes Earlier Requirements" decide which side is right),
- makes the implementation being produced materially incorrect, or
- creates real data-integrity, security, or operational risk in what's being shipped.

Material discoveries are work — they enter the buckets below, almost always bucket 1. Everything else is an **observation**, and the default disposition for an observation is **dismiss: no action required.** Theoretical concerns, cosmetic issues, optional refactors, intentional properties of legacy systems, scenarios we don't support, improvements not worth their cost — dismissal is correct engineering judgment for all of these, not negligence. Real rigor includes knowing what not to do. A dismissed item is fully silent: no record, no wrap-up mention, no ledger count. The rare observation that is genuinely valuable future work — "we will actually want to do this," not "I noticed this" — files per bucket 2.

#### Adjacency is how scope actually leaks — the four criteria alone do not catch it

The four criteria above were written against *tangents*, and tangents are not the problem. Sessions do not drift by wandering off to unrelated code. They drift **sideways, one neighbour at a time**: the document that describes the thing just changed now reads slightly wrong; a sibling check uses the same pattern and has the same latent flaw; a count in a comment is stale; a test could be stronger; a nearby function does the same thing worse. Every one of these can be dressed as "materially incorrect" or "operational risk" with a straight face, which is exactly why a categorical gate lets them through. **The more capable the model, the more of these it sees — and seeing one is not a mandate to act on it.** This subsection exists because the categorical gate was in force and a session still spent most of its time on neighbours.

Three mechanical tests, applied at the moment of action rather than remembered from load time:

- **The edit-site test.** Before touching any file the Technical Design or phase doc did not already put on the path, name the acceptance criterion that requires the edit — the actual ID or text, not a category. **"To keep it consistent," "while I'm here," "it's now slightly wrong," and "it's the same pattern" are not criteria.** If no criterion can be named, the edit is not made, however small it is and however correct the result would be. This is the whole gate in one question, and it works precisely because it is asked at the keystroke, not in the abstract.
- **The cascade tell.** An in-scope change that forces follow-ups (a regenerated artifact, a re-pinned test, a drift gate) is normal — that is the criterion's own cost. A *non-criterion* edit that forces follow-ups is the leak in progress, and every downstream step will look mandatory because it arrives as a red test or a failing gate. **Disposition is decided at the root edit, never at its consequences.** When the third or fourth thing is being fixed to make an edit pass that no criterion asked for, the correct move is to revert the root edit, not to fix the fourth thing. The cost of the cascade is not sunk; it is the signal.
- **Time is a criterion's proxy.** If dealing with a discovery would take longer than the criterion work still remaining, that is the answer on its own. The session's budget is the acceptance criteria's; a neighbour does not get to spend it because it was noticed first.

**What you broke, you own — that is not a neighbour and none of the above excuses it.** The line between a neighbour and an obligation is *causation*, not location: did your change **make** this wrong, or did you **notice** it was wrong? A test that went red because of your edit, a page that renders wrong because of your edit, a consumer that now fails because of your edit — those are the criterion's own cost, and they are fixed before the work is called done, exactly as the cascade bullet says for in-scope changes. "No criterion, no edit" is never a licence to leave your own breakage behind. The two rules compose cleanly: if the breakage traces back to an edit no criterion asked for, reverting that edit is the cheaper way to own it — the one thing never allowed is the off-criterion edit *and* the abandoned breakage.

The same restraint applies inside the exceptions. A **critical** finding (The Critical Exception below) licenses surfacing it and *just enough* investigation to confirm it is real and state it in a line with a recommendation — not an audit of it; whether to spend a session on it is the user's decision. A **requirements defect** (the second boundary below) licenses fixing the requirement that is wrong, not the things near it. Neither exception is a door back into the neighbourhood.

`engineering-principles`' "scope follows intent, not literal words" is not in tension with any of this. Intent is the *whole* of what the criteria ask — end to end, not the minimum literal reading. It is never the neighbours of what they ask.

Three boundaries:

- **The gate never mutes critical findings.** Money at risk, data loss, production breakage — these stop the session regardless of whether they touch this phase's scope (see The Critical Exception below). Dismissal is for the immaterial, never a way to unsee something dangerous.
- **The gate never forces blind execution.** If a discovery shows the requirements or Technical Design themselves are wrong — continuing would build the wrong thing or produce bad data — that is a requirements defect, not an observation. Resolve it before building further, per Docs Before Code and the confidence gates — a decide-and-proceed, not a session stop: below 95% business confidence that means an assumption entry and the build continues on it (it stops only when no answer can be put forward, per Confidence Thresholds); and where a stakeholder had personally ruled, the entry is a reopening at any confidence. Merely finding another thing that could be improved is not a requirements defect.
- **The gate governs implementation sessions**, whose goal is convergence on a defined done state. Explicit review/audit skills (deliverable review, hardening audits) are supposed to hunt broadly for defects — don't apply implementation-mode restraint there, and don't run review-mode discovery during implementation.

### The Disposition Rule

The urge to write an FYI / caveat / "worth noting" / "you should know" is the signal that an item has not been dispositioned — the FYI itself is never the disposition, and it is never written. The item lands in exactly one of four dispositions. The first — **dismiss** — is the default for observations and already happened at the Materiality Gate above; it needs no further handling, and it is the right answer for nearly everything that arrives as an aside. What survives the gate lands in one of three buckets:

**1. Deal with it now.** If the current unit of work (PRD, phase, task) can't honestly be called done without it, it's in scope. Keep working. Session length, accumulated effort, or "I've already done a lot" are not reasons to stop and report instead. "Can't honestly be called done" is measured by the Materiality Gate — acceptance criteria, explicit requirements, material correctness and safety — never by general code quality; "the codebase would be better" puts nothing in this bucket.

**2. File it into the methodology.** Genuinely future work gets written where a future session will actually load it — never a chat-only mention, and never a random standalone doc. Filing has a bar: the item is work we will actually want to do, not merely something noticed. Filing is not a politer dismissal — a stream of marginal observations filed forward is a shadow backlog even when every entry lands in an approved doc. And never invent a new tracking surface for discovered work — no new backlog files, TODO registries, or tracker tickets outside the destinations in the routing table below; if nothing in the table fits, that's the table's last row (stop and ask), not licence to create one. A ticket in whatever the org uses to schedule work is bookkeeping, not a disposition: the methodology re-reads the governing docs, not trackers, so work inside the current PRD is carried by its governing doc, and work outside it is handed to the user (row below). Routing:

| The item is... | File it in... |
|---|---|
| Work belonging to a later phase of a multi-phase PRD | That future phase document, under a `## Carried forward from Phase N` / `## Inherited from Phase N` heading (or `Phase-specific notes` for small items) — with enough context for the implementing session to execute without this chat's history. Phase docs are born thin but legitimately grow as routed work lands in them; the only forbidden growth is restating PRD/Technical Design content |
| Future-ish work but this is the last/only phase | If it's material — the PRD isn't honestly complete without it — bucket 1: deal with it now. If it's non-material but genuinely valuable, ask the user in one line where it should live, with a recommendation — the user decides whether it becomes a change directory (`prd-writing-standards`); a session never creates one unasked. Never expand the finished phase to absorb it, and never park it in a register nothing works. Anything less than that: dismiss |
| A design-level fact or decision discovered mid-work | The Technical Design |
| A business-requirement implication, **or anything at all that needs a stakeholder's answer** | The assumptions document (via `assumptions-document-writing`) — see "A Decision Needs an Assumption Entry" below, which admits no exceptions. The PRD itself is the most protected doc; below the 95% business-confidence bar its intent changes only via the assumptions process (at ≥95%, the Docs Before Code rule lets you update it directly) |
| Work outside the current PRD that the user may want later | Not filed anywhere by the session. Named in the wrap-up as a one-line action item with a recommendation; the user decides whether it becomes a change directory or goes to whatever they use to schedule work. The methodology has no backlog, so it never implies an item is tracked — never say it "will" be done unless a build will read it: the PRD or change being built, or the phase document that will build it |
| An action only a human can take (send an email, contact a vendor, grant an approval) | Never just filed away — see "Human-Action Items" below: prep everything AI-doable, record it under `## Pending human actions` in the governing doc, surface it in the wrap-up |
| A genuine blocker you cannot resolve this session | Bucket 3 — a blocker is material by definition (the work can't complete without it), so the user hears about it now, as an action item: what blocks, what was tried, what's needed to unblock, with a recommendation. Record the blocked work in the governing PRD/phase doc so the continuation sees it; if the blocker also revealed a durable design fact (a platform limitation, an API gap), that fact goes into the Technical Design per the row above — the design carries facts, the phase doc carries work state. "Blocked — Surfaced to the User" is an accepted terminal state (see Terminal States below) |
| Something none of the above fits | Stop and ask — but propose a specific location, since it may need to be worked into the methodology |

**A review page, report, dashboard, email, or any other deliverable is NEVER a
destination in this table.** Recording something on a surface a stakeholder can look at
is publishing, not dispositioning. See "A Decision Needs an Assumption Entry" below.

**3. Ask the user — only when genuinely blocked.** Two legitimate reasons: (a) you're below the confidence gate on a decision that matters (see Confidence Thresholds above), or (b) you need a permission or approval only the user can grant. Format: one or two plain-English sentences plus your recommendation — never paragraphs of background. Batch every open ask into one short list with proposed defaults; never drip one question per turn.

If an item fits none of the three buckets, it was an observation all along — dismiss it silently.

### The Continuation Test — Dispositioned Means Silent

A disposition isn't complete until it passes this test: *will the natural continuation of the work — the next prompt being "implement the next phase" (or the PRD simply proceeding to completion) — cause this item to get handled without the user doing anything?*

**If yes, the item itself gets zero individual mention in the response.** Not a one-line FYI, not a "filed X for later" note, not a "for transparency" aside. The filed item is visible in the diff and in the governing doc it landed in — that is its audit trail. Mentioning it anyway forces the user to context-switch into the chat and think about something the methodology already decided how to handle; from their side, every mention reads as a question ("what do we do about this?") that they then have to answer with instructions the methodology already contains. That round trip is the exact cost this discipline exists to eliminate.

**The disposition ledger line.** What the wrap-up *should* carry is one aggregate line — **counts and destinations only, never the items themselves**:

> **Dispositions:** 2 assumptions declared, 3 items filed to phase-4, 1 fact folded into the Technical Design.

This is a checksum, not an FYI: it confirms the discipline ran and lets the user spot volume anomalies (a dozen items landing in one future phase is worth a look) without handing them anything to decide. The moment the line names or describes an item, it has become an FYI list again — counts and destinations, nothing more. If nothing was dispositioned, omit the line entirely; never write "0 items."

**What still gets named individually** is only what needs the user, as action items: a question that fell below the confidence gate (with a recommended default), a declared business assumption they must route to a stakeholder, a pending human action with its prepared draft, an out-of-scope item handed to the user to decide on (named as their decision, never as work that will be done), a critical finding. Everything else — items dealt with in-session, work filed into future phase docs, design facts folded into the Technical Design, technical assumptions self-confirmed by investigation — rides the continuation silently behind the ledger line's counts.

### A Decision Needs an Assumption Entry, Always

Every decision starts life as a question. The methodology's whole move is that we never
leave a question sitting as a question: we answer it ourselves, declare the answer as an
assumption, and keep building. **So the assumptions document is the standing surface for
every open stakeholder decision, without exception.** If a decision exists and there is
no assumption entry for it, it has not been dispositioned, whatever else was written
down.

**The failure this exists to stop is routing a decision to a review artifact.** It is
seductive because the artifact is real, the item genuinely belongs on it, and writing
"he sees it on the review page" feels like filing. It is not filing. A page is a
DISCLOSURE surface — it shows a reader the evidence and lets them satisfy themselves.
A decision needs a CHANNEL the stakeholder answers in, and a page is not one:

- A page has no reply mechanism. Reading it produces no artifact you can check.
- A page grows. An item that is one of four exceptions today is one of four hundred
  after the next phase, and nothing about it gets louder as it ages.
- A stakeholder opens a page to look something up, not to work a queue of open
  questions. The question is invisible unless they happened to want that exact row.

Measured instance, and the reason this section exists: on one project a boundary
question was carried on a review page as an explicitly-worded ask for a business read,
through two separate "ready for review" emails to the stakeholder, and drew no response
for an entire phase. The same stakeholder answered that project's assumptions document
item by item, unprompted, the one time it was put in front of them.

**The rule.** Anything needing a stakeholder's answer gets an assumptions entry with a
confirm/correct block, and gets named in the message that goes to them. It may ALSO
appear on a review page or a tracker — those carry the
evidence and the bookkeeping, and they are additive, never a substitute. When you
catch yourself writing a "where they see it" note that names a surface rather than a
question list, that item needs an assumption entry too.

**If you think the assumptions document is genuinely the wrong home** for a particular
decision, that is a methodology gap rather than a licence to route around it: stop and
ask, and propose where it should live. Do not invent a third channel silently.

### The 90% Ask-Gate

Never stop to ask a question when you're ≥90% confident what the user's answer would be. Assume the answer and keep going, narrating in one line so they can intercept. This gate governs *whether to stop at all*; the confidence gates above (technical proceeds on the best answer; business below 95% goes to a declared assumption) govern *what answer to proceed on*.

### No Hollow Promises

A forward-looking statement about work you could do right now is a loose end wearing a
to-do list's clothing. "I'll generate that report," "next, the docs should be updated,"
"this still needs a test," "we should also handle X" — each of these is an
undispositioned item being *announced* instead of dispositioned. The Materiality Gate
applies first: if the announced item wouldn't survive it, the right move is to delete
the sentence, not do the work. For survivors, the three buckets apply like anything
else: do it now (usually the right bucket — if you can describe the work, you can
usually just do it), file it where a future session will load it, or ask in one line
with a recommendation.

The test: **future work may be named only if it has already been filed somewhere
concrete** — a phase doc entry, a declared assumption, or a pending human action with its
draft already prepared — or it is an out-of-scope item handed to the user as their decision,
never as work that will be done. A "next steps" list whose items live nowhere but the chat is the same failure
as an FYI list. And being filed is necessary but not sufficient: per the continuation
test above, filed work is actually named only when it needs the user — filed work the
continuation will handle stays silent. Act first: do the work, then report the completed action — never report the
intention.

### Human-Action Items

Some items can only be completed by a human — sending an email, calling a vendor, reaching out to a third party, granting an approval. These are never silently stuffed into a future doc and never left as chat-only mentions:

1. **Prep first.** Before surfacing one, do every part the AI can do: draft the message, assemble the findings and artifacts the human needs. What gets handed over is ready to execute — "send this draft," never "someone should contact the vendor."
2. **Record it.** Add a one-line entry under a `## Pending human actions` heading in the governing PRD/phase doc: who needs to do what, pointing at the prepared draft/artifact. The line is removed once the action is confirmed done. If the outreach genuinely belongs to a future phase, file it in that phase doc instead.
3. **Surface it.** Name it in the wrap-up as an explicit action item — action items are not FYIs. The unit of work is not "done" while a current-phase human action is outstanding; a later completeness pass must find it recorded, not get a clean "all criteria met."

### The Critical Exception

Genuinely critical findings — money at risk, data loss, production breakage — do stop the session immediately. Label them explicitly: "Critical finding, stopping to surface." That's not an FYI; it's a blocker. Everything below that bar follows the disposition rule.

**This exception is about irreversibility, not uncertainty.** An assumption is a reversible bet — the feedback loop exists because being wrong is cheap to fix — so no assumption ever licenses an irreversible action: charging money, deleting data, writing to production. Those wait for the user however confident you are. That is a different gate from the confidence gates above: those govern what answer to proceed on; this one governs what may not be done on any answer.

**A stakeholder-validated ruling or value that looks wrong is not on this list.** It is a reopening, governed by Gate 3 in `assumptions-document-writing`: reopen it under its original ID, put the ruling and the new evidence side by side, and proceed on the better-evidenced answer like any other assumption. The one thing you never do is edit the stakeholder's own record to match your evidence — their decision in the PRD or Technical Design, or an expected value they validated for a test. That record changes only when they revise it, or the user approves the change on their behalf; until then a test that checks a validated value stays red and says why. The reopened entry, named in the wrap-up as an action item for the user to route, is what carries the disagreement — it is not a stop. (A stakeholder-validated expected value in a test usually has no assumption ID to reopen — there the record is wherever that validation is written down, and the red test plus the wrap-up case carry the disclosure.)

### Minimize Stop-and-Go

The round-trip is the expensive thing, not the session length. The ideal shape is one long first session that gets as far as it possibly can, and continuations that are also long — not a rhythm of small work increments each ending in a question. Before ending any turn:

1. Sweep the draft response: run every caveat/FYI through the Materiality Gate, then disposition the survivors into a bucket.
2. Apply the 90% ask-gate to every question you were about to ask.
3. Batch whatever survives into one short list with recommended defaults.
4. End the turn only if that list is non-empty or the work is genuinely done.

### Every Session Names What It Serves

Every implementation session exists in service of one named unit of work, and it can say which: three lines in a prompt, one line in a response. The **lineage** is: the PRD, by its full title; the phase, by its id *and* its full title (a bare `2a1` or `3b2` means nothing to anyone reading a tab strip or a prompt six weeks later), or `whole PRD, not split` when there is none; and what *this* session does for it — implements it, or fixes a named thing that blocks a named acceptance criterion of it. That block opens every continuation prompt (`continuation-prompt` owns its shape) and the first response of `implement-from-requirements` and `implement-from-discovery`; work from a ticket or issue carries its id in the chat name and the prompt already. A reader who opens any chat sees at the top what it is for.

**The lineage is a gate, not a label.** A session that cannot state it honestly does not get a prompt and does not get built. The measured failure this exists to stop: a phase session found a defect, handed off a chat to fix it; that chat found another and handed off again; four chats later, each running an hour or more, none of them could say which acceptance criterion of which phase the work was unblocking. The Materiality Gate above stops discoveries becoming work *inside* a session; this is the same gate at the session boundary, where the handoff was letting them through. A fix that unblocks nothing named is an observation that got promoted by being handed a chat of its own — at the boundary it goes back through the gate and the disposition table above, under the same 90% ask-gate: dismiss is the default; a genuinely valuable item files into the phase doc that will build it; work outside the current PRD is named in the wrap-up as the user's decision with a recommendation, never a mid-session stop. What it never gets is a prompt with a plausible-sounding purpose written to fill the block. On the user's explicit ask the prompt is written with the fixed head `no lineage found` in the block — the one greppable marker for an orphan, in prompts and commit messages alike.

**Work that legitimately has no PRD phase.** The gate is not "everything must be a phase." These shapes carry their own lineage, and the block names it as such:

- **Ticket-tracked work** — a ticket or issue somebody raised, in whatever tracker it lives in: a Jira ticket (`PROJ-4271`), a GitHub issue. Lineage is the id and what it reports. The id counts because someone other than this session decided the work matters. Filing a ticket is bookkeeping, not a disposition (the disposition table above), and citing an id this session just minted as the lineage for a chat it writes itself is the orphan chain wearing an id: a minted id makes work findable, not needed.
- **A declared ops or incident thread** with a session notes file in the repo recording its state. Lineage is the thread and the incident.
- **A component defect reported from outside**, no PRD in flight — the `implement-from-discovery` case. Lineage is the component's own PRD plus who reported it or what broke.
- **Requirements work** — refining, splitting, designing, writing the PRD. In service of the PRD itself; there is no phase yet. When the PRD is not written yet and comes from a PRD roadmap (`prd-roadmap`), the lineage is the roadmap and the planned PRD by name.
- **Methodology work** on the skills or instructions themselves.

The red flag is the one shape not on that list: a code-change chat whose only lineage is *another chat*. It names a symptom, and no acceptance criterion, no ticket id, no incident, no session file. That chat is the chain, and the honest block for it reads "no lineage found" — which is the block's whole value: an orphan reads as an orphan, so the user can decide whether it should exist at all, instead of discovering the chain from the inside a day later.

### Session Markers: Leave a Note Where You Work

Several sessions — Claude Code, Codex, anything else — often run at once in the same checkout or in sibling worktrees. Each leaves a small log in every repo it edits, so a person or another session that finds modified code, or wants to know what is in flight, can see who is working there and on what. It is a courtesy note that takes seconds; it never competes with the work for attention. **It is not a lock:** another session's log never stops or pauses yours. Before your first edit, though, a live log decides where you work (Parallel Sessions, below).

**Write.** Before your first edit in a repo, create `.agent-sessions/<date>-<tool>-<slug>.log` at the root of its shared checkout, even when you work in a worktree (Parallel Sessions, below) — date from `date +%Y-%m-%d-%H%M`, tool as a lowercase slug (`claude-code`, `codex`), slug the chat title or lineage in a few words, e.g. `2026-09-23-1412-claude-code-email-digest.log`. A session editing several repos keeps a log in each. Add `.agent-sessions/` to the repo's `.gitignore` if it isn't listed; that line rides in your commit, so put it in your expected changeset. A header, then one line per event, timestamped with `date +%Y-%m-%dT%H:%M%z`:

```
tool:       Claude Code
session:    claude-7 [a1b2c3]
chat title: Email digest scheduler
branch:     develop
serves:     Phase 2a — Email digest scheduler, of User Notifications

2026-09-23T14:12-0400  START    implement-from-requirements
2026-09-23T15:40-0400  WAITING  CI on PR #541
2026-09-23T15:58-0400  COMMIT   e4f5a6b pushed
2026-09-23T16:06-0400  DONE     Successful implementation — Phase 2a closed
```

`serves:` is the lineage above, in its full-title form. `session:` is whatever the tool exposes for addressing this chat — for Claude Code, the name and bracketed ref `ListAgents` reports, which lets Claude peers message it (the ref is the stable handle; the name changes when the chat is renamed); omit any field you don't have. **START and DONE are the only required lines.** DONE is written at any terminal state and names it (Terminal States below), so a reader can tell a finish from `DONE  Blocked — vendor API credentials expired`. Beyond those, append a line only at a moment you are already announcing to the user and a peer would care about: SCOPE (a split changed what you are building), WAITING (on CI or on the user), COMMIT, HANDOFF (the successor chat's name). A `test-audit` red check also writes REDCHECK and RESTORED around the moment it breaks code on purpose: a REDCHECK with no RESTORED after it means that file was left broken, so restore it from the copy the line names. Append only, and only to your own log; never rewrite. The rule lasts the whole chat, not just the skill's run: whenever you are about to edit a repo with no log of your own — a follow-up request that moves to another repo, work resumed after your DONE, or a chat already under way when it loads this skill — start one first (a new START line, or a new file if yours was pruned).

**Prune.** When creating your log, delete logs in the same folder whose last line is a DONE more than 7 days old, or that have had no write for 14 days. Never touch anything newer — other sessions may still be working in that checkout.

**Read.** Logs are hints, not truth. A missing DONE may mean the session is still running or that it ended without writing one; a DONE may predate later work. Weigh a log against its last-write time, the branch's uncommitted changes and merge state, and — for Claude peers — `ListAgents` busy/idle. To survey everything in flight, find each repo's worktrees with `git worktree list` and read `.agent-sessions/*` in every checkout it lists; one session's logs in different repos share its `session:` line. Message a peer only when the logs and git can't answer the question. When a session arrives in your checkout after you started, its uncommitted changes sit beside yours: leave them alone and stage only the files you changed.

### Parallel Sessions: Where to Work

**Default: the shared checkout, on the shared branch.** The shared checkout is the repo's normal working copy, the directory the user opens in the editor; `<org directory>` below is the folder that holds it and any sibling repos (`<org directory>/<repo>`). The shared branch is the integration branch sessions commit to directly (often `develop` or `main`). Most work runs one chat at a time, and a chat working there needs no worktree, no clone and no cleanup.

**Work in a worktree instead only when one of these two holds**, checked before the chat's first edit:

1. The prompt that started the chat says `Parallel: yes`.
2. Another agent session is live in a repo this chat will edit. That means an `.agent-sessions/` log in the shared checkout (Session Markers, above) with a START line, no DONE line, and a last line written within the past 12 hours. An older log without a DONE is an abandoned session, not a live one.

When neither holds, stay in the shared checkout, even if parallel work seems likely and even if the checkout has uncommitted changes you did not make (leave those alone and stage only your own files). A chat that isolates by default leaves directories behind for the user to find and delete. A chat that starts a few minutes after this one sees this chat's log and isolates itself, so this chat does not have to anticipate it. When any signal holds, every repo the chat will edit goes into the worktree folder, not only the repo that tripped it, so sibling repos stay siblings. Inside an authorized `phase-chain`, that skill's checkout rule governs instead: no worktree, and another live writer is a blocker.

**Never a clone** unless the user asks for one. A worktree does everything a clone would for this purpose, shares the repository's history and fetches, and `git worktree list` finds it again.

**Worktree mechanics.** The chat does all of this itself. Editor extensions do not create or clean up worktrees, so nothing else will.

- **Name:** a slug of the chat name: lowercase, spaces and slashes as hyphens, e.g. `phase-2a-email-digest`. A chat with no name uses its session log's slug. The slug names both the folder and the branch.
- **Where:** `<org directory>/.worktrees/<slug>/<repo>`, one folder per chat, with every repo it edits under it. Create each with `git -C <shared checkout> fetch origin`, then `git -C <shared checkout> worktree add --track -b wt/<slug> <org directory>/.worktrees/<slug>/<repo> origin/<shared branch>`. The `wt/` branch exists only because git refuses to check out the shared branch twice. It is never pushed as a branch.
- **Session log:** keep writing it in the shared checkout's `.agent-sessions/`, not in the worktree, so signal 2 sees this chat, and put the worktree path on the START line.
- **Run the code under test from the worktree.** A shared virtual environment or dependency install usually imports the shared checkout's code, not the worktree's. Point the interpreter at the worktree's sources (for Python, `PYTHONPATH=<worktree>/src`), or tests silently test the wrong tree.
- **Land each finished piece on the shared branch, when committing and pushing are authorized.**
  1. Fetch, rebase onto `origin/<shared branch>`, and re-run the tests the rebase could affect. Regenerate generated files after the rebase rather than merging them by hand.
  2. Push the result as the shared branch: `git push origin HEAD:<shared branch>`, a fast-forward.
  3. If the push is rejected because another chat pushed first, repeat from step 1. Never force a push to the shared branch.
  4. Fast-forward the shared checkout so the editor shows the work: `git -C <shared checkout> merge --ff-only origin/<shared branch>`. Always attempt it; it succeeds beside another session's uncommitted changes unless they touch the same files. If git refuses, say so in the wrap-up.

  Without authorization, stage in the worktree, present the commit message as usual for the user to commit there, and leave the worktree in place with its path in the wrap-up.
- **Clean up at wrap-up**, once `git log origin/<shared branch>..HEAD` is empty and `git status` is clean. Run the cleanup from the shared checkout, not from inside the worktree: `git -C <shared checkout> worktree remove <path>`, then `git -C <shared checkout> branch -d wt/<slug>`, then delete the chat's empty folder under `.worktrees/`. `-d` refuses to delete work that has not landed; if it refuses, stop and report, and never force it. The wrap-up says whether the worktree was removed. A worktree that outlives its chat shows up in `git worktree list` and in a log with no DONE.

**Parallel work still needs owners.** Worktrees stop two chats writing the same file. They do not stop two chats changing related behaviour that merges cleanly and then breaks. When one chat hands out several prompts, each prompt names the area its chat owns: files, modules, registry blocks. A chat that needs a change outside its area stops and says so.

### Done Means Done

A unit of work is complete when its stated acceptance criteria are verifiably satisfied, required tests and checks pass, no known material issue remains, and every item that survived the Materiality Gate has been fixed, filed, or asked about. When those hold, declare completion and stop. Do not run an open-ended "what else could be wrong?" sweep past the workflow's own review step — that is review-mode work, and the definition of done does not include "nothing anywhere could be improved."

Never declare completion and then append a fresh concern ("everything's done — but one thing you should know…"). Anything material belonged *before* the declaration; anything else was dismissed or filed. Conversely, if the criteria can't all be satisfied this session, the honest ending is a blocked or filed terminal state — not a "complete" announcement wearing caveats. The definition of done means something in both directions.

### Reporting Style

Past tense, done-work first: what was built/fixed, how it was validated (name the actual commands and tests run), the commit message, the disposition ledger line, then whatever needs the user. No FYI section, no caveat list, and no per-item inventory of dispositions that passed the continuation test — those are represented only by the aggregate ledger line's counts. If you catch yourself writing "I've filed X for later" about an item the continuation will handle — delete the sentence; it's already counted in the ledger line.

**The wrap-up passes a three-question test, sentence by sentence, before it goes out.** Each sentence is about (a) an acceptance criterion and whether it landed, (b) an action only the user can take, or (c) a critical finding labelled as such — money, data loss, production breakage. The fixed items the procedural skill's wrap-up list requires (commit message, disposition ledger line, the review-and-hardening note, kept exploration scripts, pre-existing failures) are exempt. Any other sentence that is none of the three is **deleted.** Not softened, not moved to a footnote, not folded into the ledger, not prefaced with "not blocking, but" — deleted. The reader should not be able to tell from the wrap-up that anything off-topic was seen at all.

If you catch yourself typing "worth noting," "one thing I'd flag," "FYI," "you should know," or "a few things I noticed" — **the answer is to delete the sentence, not to go disposition the item.** An item you were about to mention as an aside is, by that fact, an observation that failed the gate; the correct disposition was silent dismissal, and it already happened. Filing it now — so it can be counted, so it can be "handled" — is the second-worst outcome after mentioning it: a side quest does not earn a disposition by being noticed, and a long ledger line is evidence the gate was loose, not evidence of diligence.

The reason this is absolute: every off-topic sentence hands the user the materiality judgment the session was supposed to have made. They now have to stop and decide whether it is on topic, whether it matters, whether it threatens the criteria — the exact conversation the gate exists to make unnecessary. Reporting an observation is outsourcing the gate. If you are genuinely unsure whether something is material, that uncertainty is not resolved by telling the user; it is resolved by the gate's default, which is dismiss.

---

## Implementation Workflow

The typical sequence for implementing a feature or closing a gap:

1. **Read the PRD and Technical Design** — understand what you're building and how.

2. **Check the Assumptions Document** — treat all assumptions as decided facts.

3. **Establish readiness — but note this is a state, not a step that always runs.** "Implementation-ready" means the gaps have been thought through and remaining business uncertainty is captured as assumptions. Two skills can establish it, and **both are explicit user choices, not automatic**: `implementation-readiness-check` is the human checkpoint, surfacing everything below 95% for you to confirm or redirect (deliberately user-invoke-only); `autonomous-requirements-refinement` is the heavier multi-pass version that drives docs to ready state on its own.

   **The implement skills do NOT re-run a readiness check.** If you're going straight from a refined PRD to building, you don't need one: the same investigate → declare-an-assumption → proceed logic runs continuously inside the implement skill's own uncertainty handling, so no separate automated gate is needed (the build's narrow conflict check, `implement-from-requirements` Phase 4, is not a readiness check). Reach for a readiness check when you specifically want the gap analysis front-loaded as its own step — before deciding whether to phase-split, before handing requirements to someone else, or when you want a checkpoint before any code is written. And if an implement session finds the docs clearly under-baked, it stops and recommends `autonomous-requirements-refinement` (or a readiness check, for a human checkpoint) rather than pressing on.

4. **Size for a single AI session** — if the work is too large for one focused session, `phase-split` cuts it into phases (`implement-from-requirements` runs this sizing gate automatically, and neither skill stops to ask whether to split — the cut is declared and the session carries on with the first leaf). Sizing isn't one-and-done: mid-implementation you may discover that even a single phase is bigger than the split assumed. When that happens, re-invoke `phase-split` to cut the remaining work into child phases (`2a` under `2`, `2a1` under `2a`, one file each) rather than grinding on past coherent context. Re-cutting covers only the work the phase was already scoped to carry — it is never a vehicle for turning mid-implementation discoveries into new phases; those go through the Materiality Gate and disposition rule, and most are dismissed.

5. **Implement** — follow the Technical Design, applying existing code patterns, `engineering-principles`, and the house engineering standards named in the project's AGENTS.md/CLAUDE.md, if any.

6. **Test** — verify the implementation works (details vary by project type).

7. **Bring to terminal state** — every task must end cleanly (see next section), and the session marker's DONE line names the state reached.

For fully autonomous multi-pass document refinement, the `autonomous-requirements-refinement` skill orchestrates the readiness-check/investigate/update loop with state tracking and verification passes. Implementation itself runs through the implement skills — `implement-from-requirements` or `implement-from-discovery`.

---

## Terminal States

Every implementation task must end in one of these states. No loose ends, no ambiguous "in progress" status.

**None of them is "recorded on a deliverable."** A decision that needs a stakeholder's answer reaches a terminal state only through an assumption entry. Writing it onto a review page, a report, a dashboard or an email is publishing, not dispositioning: those surfaces carry no reply mechanism, they grow until any one item on them is invisible, and a stakeholder opens them to look something up rather than to work a queue. This is measured rather than theoretical — see "A Decision Needs an Assumption Entry, Always" above. Every decision starts as a question, and the framework's core move is that a question never stays a question: it is answered, declared as an assumption, and built on. So the assumptions document is the standing surface for all of them, and anything else that records the item is additive.

### Successful Implementation

The feature/gap is implemented, tested, and ready to commit. Documents are consistent with code. This is the desired outcome.

“Ready to commit” is not a stopping point when the user has authorized delivery.
Complete the authorized commit, push, and required project delivery tail first.
For an authorized sequence across fresh Codex tasks, use `phase-chain`: it owns
successor dispatch and distinguishes a delivered phase from a completed chain.

### Completed — Remainder Filed Into Future Phases

The current phase (or task) is done, and follow-up work discovered along the way — the survivors of the Materiality Gate, not every observation — is filed into the future phase docs where it naturally belongs. This is the preferred home for gate-surviving discovered work whenever a split exists — those docs get loaded automatically when `implement-from-requirements` builds the phase, so nothing is tossed into the void.

### Blocked — Surfaced to the User

You hit a wall that can't be resolved through assumptions, and no future phase doc can carry the item. A blocker is material by definition, so it is never quietly filed away: the wrap-up names it as an action item — what blocks, what was tried, what's needed to unblock, with a recommendation — and the governing PRD/phase doc records it so the continuation sees it. Any durable design fact the blocker revealed (a platform limitation, an API gap) is folded into the Technical Design — the design carries facts, the phase doc carries work state. This is an acceptable state; not every task is solvable in one session. Filing never substitutes for surfacing.

### Awaiting a Human Action — Prepared and Recorded

Everything the AI can do is done, and what remains can only be done by a person (send an email, contact a vendor, grant an approval). The draft or artifact is prepared, a one-line entry is recorded under `## Pending human actions` in the governing PRD/phase doc, and the item is named in the wrap-up as an action item. Per "Human-Action Items" above, the unit of work is not "done" while a current-phase human action is outstanding — so this is a distinct terminal state, not a variant of "Successful Implementation."

### Assumption Changed — Documents Updated

During implementation, you discovered something that changes an existing assumption. The assumption is updated (or a new one replaces it), the PRD/technical design are updated if affected, and implementation proceeds with the corrected understanding. If the assumption had already been validated by a stakeholder, it is reopened instead — same ID, the prior ruling acknowledged beside the new evidence, per Gate 3 in `assumptions-document-writing` — and the PRD/technical design keep the stakeholder's decision until they revise it; implementation still proceeds on the reopened answer.

### Intentional Limitation Documented

Sometimes the correct decision is not to handle a case in code — a platform constraint that can't be coded around, or a case deliberately left to manual handling. The decision and the affected cases are recorded as an assumption entry (via `assumptions-document-writing`) so a stakeholder can confirm or correct it.

---

## Relationship to Other Skills

This skill provides the **framework context**. Other skills provide the **procedures**.

| Skill | When to Use |
|-------|-------------|
| `implementation-readiness-check` | Pre-implementation gate — only when user explicitly requests a review checkpoint |
| `investigate-question` | Deep-dive investigation of specific questions surfaced during readiness checks or implementation |
| `assumptions-document-writing` | When writing or updating assumptions — formatting standards |
| `prd-roadmap` | Before any PRD, when an idea is too big for one: cuts it into right-sized planned PRDs beside a full brief that stays whole |
| `review-technical-design` | Optional, after the technical design is written and before `autonomous-requirements-refinement`: reviews a design that makes hard-to-reverse decisions |
| `autonomous-requirements-refinement` | Refining docs from draft to implementation-ready state |
| `implement-from-requirements` | Default skill when starting from a fresh PRD |
| `implement-from-discovery` | Implementing a fix or change identified during research/investigation |
| `phase-split` | Splitting a too-large PRD into AI-session-sized phases — and re-cutting when a phase turns out bigger than the original split assumed. Future phase docs are the preferred destination for discovered follow-up work that survives the Materiality Gate. |
| `engineering-principles` | The method's engineering principles during implementation (no silent fallbacks, the testing evidence standard, judgment when things are ambiguous), plus the extension point for a project's house engineering standards |
| `continuation-prompt` | The prompt that starts the next chat. Its first step applies this skill's document ownership rules (phase doc: work state; Technical Design: durable facts; assumptions: business logic) to move every repo-truth sentence out of the prompt and into the governing doc, so the next session starts from the docs, not from a prompt that has become a second requirements document. |


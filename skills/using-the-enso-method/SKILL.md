---
name: using-the-enso-method
description: Where to start and what comes next in the Enso Method — which skill runs at each stage, in what order, and where the user's review is recommended. Use when the user asks to use the Enso Method, asks "where do I start" or "what's next", or hands over requirements, an idea or a brief without naming a skill. A map only; each skill it names owns its own procedure.
user-invocable: true
---

# Using the Enso Method

The Enso Method builds software from requirements through a fixed order of documents, each written by one skill. Two points are recommended for the user's review, the refined PRD and the reviewed technical design; neither is required, and nothing waits on them unless the user asks it to. Beyond those, the user is not asked about requirements again. This skill is the map: it says which skill comes next and nothing about how that skill works. Load the skill it names for that. The philosophy and session discipline (assumptions, confidence thresholds, No Loose Ends) live in `implementation-lifecycle`.

## Find Where the Work Stands

Read the repo before choosing. Everything for one piece of work lives in `docs/prds/{name}/`, or `docs/changes/{name}/` for a bounded change, or wherever the repo already keeps its documents; an idea cut into several PRDs also has `docs/initiatives/{name}/` (`docs/roadmaps/{name}/` in older repos), and raw material that went through `requirements-intake` has its record in `source-material/{name}/`. When several rows match, the furthest stage reached (the lowest row) wins, except that a pending feedback-changes file (the last row) outranks every stage.

| What exists | Next skill |
|---|---|
| Raw material not yet in a requirements intake record, and no PRD: meeting transcripts, long threads, earlier AI sessions, a prior attempt's documents, or a large mixed pile | `requirements-intake`, which creates the record or extends the existing one |
| An idea, notes, a brief, or a requirements intake record (`source-material/{name}/{name}-requirements-intake.md`) with no raw material left outside it, no PRD | `initiative-breakdown` if it is bigger than one PRD, otherwise `prd-writing-standards` |
| A new initiative | `prd-writing-standards` for its first planned PRD. The others are written when the user chooses, one at a time or alongside each other, and each is built once the PRDs on its **Depends on:** line are done |
| A drafted PRD, not yet refined | `autonomous-prd-refinement`; one `deliverable-review` round is enough for a small PRD. A `{name}-prd-refinement-state.md` in the directory means a run is in progress: resume it |
| A refined PRD, no technical design | `technical-design-writing-standards`, after the user's review when the user wants one. A small change that follows an established pattern and adds no new interfaces can skip the design and go to `implement-from-requirements`, which proceeds without one. A stakeholder package made from the refined PRD does not move the work past this row. A follow-on PRD made for a stakeholder's new asks (a `**Follow-on to:**` line, with its scope taken from their saved feedback) with no package yet gets `stakeholder-review-package` first |
| A drafted technical design with no review commit after it, and no design refinement under way or finished | `review-technical-design`, in a fresh context |
| A reviewed technical design | `autonomous-design-refinement`, after the user's read of it when the user wants one. A `{name}-design-refinement-state.md` in the directory means a run is in progress: resume it |
| Refined requirements, stakeholder package missing or stale and not declined | `stakeholder-review-package` to create or refresh the HTML automatically before phase planning |
| Refined requirements, stakeholder package current or declined, not yet sized for phase planning | `phase-split` to decide whether phases are needed and plan them before implementation |
| Phase planning confirmed the work fits one session | `implement-from-requirements` on the unsplit PRD |
| Phase documents | `implement-from-requirements` for the first leaf phase, in plan-table order, without a `**Closed:**` line |
| Every phase closed, no current clean whole-PRD delivery audit (`delivery-audit` defines currentness) | `delivery-audit` on the whole PRD, in a fresh chat, including after completion phases or a test audit's implementation fixes. The completion phases either audit adds, marked `**Added by delivery audit:**` or `**Added by test audit:**` at the top, the feedback phases `assumptions-document-feedback` adds, marked `**Added by stakeholder feedback:**`, and the fix phases `implement-from-discovery` adds, marked `**Added by implement-from-discovery:**`, are phase documents like any other: the row above builds them |
| Every phase closed with a current clean whole-PRD delivery audit | `test-audit` on the whole PRD, in a fresh chat; it continues an existing `test-audit.md` and re-checks only what changed since its last audit. The PRD is complete when that run ends with `Done` and the delivery audit remains current. Never declare it complete from the file alone |
| A `{name}-pending-feedback-changes.md` in the directory, at any stage | `assumptions-document-feedback`, which resumes from that file, before the stage any other row names: a stakeholder round changed what this PRD must say. Then the row for the stage the PRD had reached |

Five stages leave no file: a finished PRD refinement (its `PRD refinement complete` commit, or `PRD refinement stopped` when the user ended it with findings open, which its body lists; a small PRD's one `deliverable-review` round commits under the same subject), the design review (its `technical design review` commit, which it makes even when it changed nothing or skipped itself), a finished design refinement (its `design refinement complete` commit, or `requirements refinement complete` from before the skill was renamed), a delivery audit that found no gaps (its `delivery audit complete (whole PRD)` commit) and a build that was not split (its feature commit). Read them from `git log -- <directory>`. The PRD refinement, the design review and the delivery audit commit empty when they changed nothing (`pre-commit-validation`, "Who Commits"), and a path-limited log leaves empty commits out. So also list the subjects since the directory's first commit, `git log --format=%s $(git log --reverse --format=%H -- <directory> | head -1)..HEAD`, and look for the stage's subject with the same scope as that commit. Ask the user when neither says. The user's reviews are never a stage to detect: they are recommended, not required.

## The Order

**1. Decide what to build**

The method starts from the user's own material, however rough: notes, emails, meeting transcripts, earlier chat sessions where decisions were made, and mockups or a prototype for anything with a screen. All of it is input to the PRD. Gather everything directly relevant before writing it, and ask once where else decisions live.

- `requirements-intake`: only when that material is raw (transcripts, long threads, earlier AI sessions, a prior attempt's documents, or a large mixed pile) rather than a brief or an email or two. It separates what the stakeholders decided from everything else and records it in their own words, quoted, and the next skill writes from that record instead of the pile. Start its session at a very high reasoning effort (`requirements-intake`, "Effort").
- `initiative-breakdown`: only when the idea is bigger than one PRD. A PRD is a medium body of work, about the size of an agile epic; an idea bigger than that is an initiative. Decide which applies with the PRD-sized test in `initiative-breakdown` (Step 2) rather than asking the user. Each planned PRD then goes through this whole sequence.
- `prd-writing-standards`: the PRD, saying what is built and why.
- `autonomous-prd-refinement`: reviews and fixes the drafted PRD, its assumptions and mockups in rounds until no Medium or High finding is left. **First recommended review point:** the user reads it, ideally with whoever owns the business decisions, before the design starts. For that read, `stakeholder-review-package` can be made now from the refined PRD, when the user asks or says they will not take the work through the design themselves. A business owner can review it and hand the directory to whoever builds it; the package is refreshed after design refinement as usual and then shows only what is still open, including anything the design raised.
- `technical-design-writing-standards`: the technical design, saying how, committed as a draft.
- `review-technical-design`: started by the drafting skill in a fresh context. It questions the design's approach, checks its claims against the real code and the house standards, revises it in place and commits the revision; it skips itself for a design that follows an established pattern. **Second recommended review point:** the user reads the sections the review lists as worth reading.
- `autonomous-design-refinement`: closes the gaps in both documents without the user. Technical questions are researched; open business decisions become assumptions, and the build proceeds on them. `implementation-readiness-check` is the alternative when the user wants to confirm each open question themselves; only the user can start it.
- `stakeholder-review-package`: when requirements are ready, automatically create or refresh the HTML after design refinement and consolidation, unless the user declines it. A follow-on PRD from stakeholder feedback gets its first package right after PRD refinement, before the design; the usual refresh follows design refinement. Do not wait to be asked; sharing and stakeholder feedback remain optional.

**2. Plan the phases, then build**

- `phase-split`: follows stakeholder-package preparation or the user's opt-out. Size the work, write phase documents only when needed, and hand off without implementing.
- `implement-from-requirements`: builds the first planned phase, or the whole PRD when phase planning found it fits one session. Its sizing and automatic split remain a safeguard for a direct implementation request or work that outgrows its plan.
- `continuation-prompt`: hands each next phase to a fresh session.

**3. Prove it works.** Inside every build, without being asked: `deliverable-review`, then `test-hardening`, then `pre-commit-validation`. Then the build commits, runs `refactor-pass`, and pushes a feature branch (a push to `develop` or `main` waits for the user's word), unless the user has said otherwise.

**4. Close out the PRD.** When the last phase of a split PRD closes, its build hands off to two audits, each in a fresh chat, before the PRD is done:

- `delivery-audit`: is every acceptance criterion built? Gaps become completion phases at the end of the plan, marked at the top as added by the audit, and `implement-from-requirements` builds them like any other phase. Repeat the delivery audit after repairs until it finds no gaps.
- `test-audit`: once nothing is left to build, do the tests prove every criterion? It fills the gaps, missing tests first, and its `test-audit.md` carries the work across chats until its Status line says `Done`.

Either audit can also be pointed at a single closed phase when the user asks.

## When to Start a New Chat

A stage that starts in a new chat works from the documents rather than a long conversation about them, and brings fresh eyes. The model cannot clear its own context, so the session says when to start over. At each of these points, end with a `continuation-prompt` for the next stage and tell the user plainly that the next step is a new chat, unless the user asked to carry on in this one:

- **Always:** after `requirements-intake` (the PRD is written from its record, not from the pile), between the requirements and the technical design (after `autonomous-prd-refinement`, which is also the first review point), before the build (except a change PRD `implement-from-discovery` writes and builds within one session), and when the user turns to a different piece of work. Each later phase and each audit already gets its own chat.
- **Recommended:** after drafting the PRD and before its refinement, and between each design stage. These refinements review in fresh subagents, so a break skipped here costs little.

An orchestrator that opens sessions itself uses the same points: one session per stage, never one long session for the whole sequence.

## Along the Way

- The automatically prepared stakeholder package combines selected PRD requirements, every open assumption and contextual mockups into one HTML review. Its use and sharing remain optional; it is not another implementation document or approval gate. The user sends it; the replies, including changes to requirements and mockups, come back through `assumptions-document-feedback`. Once the PRD's build has started, that skill keeps fixes in the PRD and sends new asks, apart from minor ones, to one follow-on PRD, so the build finishes on the scope it started with. A change that reaches another PRD, as its owner or because that PRD consumes a changed contract, is finished there in the same round and given one fresh check, without rerunning its refinement. Stakeholders respond on their own schedule; nothing waits on them.
- A fix or change to existing behavior already identified, mid-work or from a bug report: `implement-from-discovery`, at any size. It records the change in the requirements first, as nothing, an amendment or a change PRD of its own, and hands anything bigger than one session to `implement-from-requirements`. With only a symptom, `investigate-question` first.
- One question to research to an answer with a confidence level: `investigate-question`.
- A session drifting from the method: reload `implementation-lifecycle`.

## Routing Rules

- **The two reviews are recommended, not required.** The refined PRD and the reviewed technical design are where human judgment goes in best. At each, say it is a good point for the user's review and what to read, then carry on when the user says to, or straight away when the user, or the prompt that started the run, asked to go through without stopping. Nothing refuses to proceed because a review didn't happen: like an assumption, an unreviewed document is a green light, and the user's corrections are folded in whenever they arrive. Beyond these, the user is not asked about requirements again; they start each next phase and send assumptions to stakeholders.
- **The requirements skills, the builds and the audits commit their own work** unless the user says not to (`pre-commit-validation`, "Who Commits"). The requirements skills and the delivery audit never push by default; builds and the test audit push when the push lands on a feature branch.
- **Requirements come before the build.** A request to build something new with no PRD starts at `prd-writing-standards`, or `initiative-breakdown` when it is bigger than one PRD. When the user asks to skip or reorder a stage (build before the PRD is refined, build one piece first, a process of their own layered on the method), say once which stage is skipped and what it risks, then do what the user decides.
- **Feedback goes into the requirements before the code.** Reactions to working software ("this is wrong", "can you change X"), meeting notes and review comments change intended behavior, even when they read like a quick tweak. Don't edit the code from the chat. A change to software already built, whether the code misses what the PRD says or the PRD itself asked for the wrong thing, goes to `implement-from-discovery`, with answers to open assumptions going through `assumptions-document-feedback`. Its Phase 4 decides, whoever the change came from, whether it needs nothing written, an amendment or a change PRD of its own, borrowing `assumptions-document-feedback` Step 1a's test; it writes that first, then builds it or hands it on. While the owning PRD's build is still under way, a change to what an unstarted phase will build is carried into that phase rather than built beside the running build. When the user asks for the direct edit, say this in a sentence; if they still want it, it is their call. A separate `docs/changes/` directory is otherwise the user's call; never create one unasked. The two exceptions are for work someone asked for: the follow-on `assumptions-document-feedback` creates for a stakeholder's new asks, and the change PRD `implement-from-discovery` writes for the change it was asked to build.
- **Start at the stage the work has reached.** Existing documents are not rewritten to restart the sequence.

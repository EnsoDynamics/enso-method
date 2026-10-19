---
name: using-the-enso-method
description: Where to start and what comes next in the Enso Method — which skill runs at each stage, in what order, and where the user's review is recommended. Use when the user asks to use the Enso Method, asks "where do I start" or "what's next", or hands over requirements, an idea or a brief without naming a skill. A map only; each skill it names owns its own procedure.
user-invocable: true
---

# Using the Enso Method

The Enso Method builds software from requirements through a fixed order of documents, each written by one skill. Two points are recommended for the user's review, the refined PRD and the reviewed technical design; neither is required, and nothing waits on them unless the user asks it to. Beyond those, the user is not asked about requirements again. This skill is the map: it says which skill comes next and nothing about how that skill works. Load the skill it names for that. The philosophy and session discipline (assumptions, confidence thresholds, No Loose Ends) live in `implementation-lifecycle`.

## Find Where the Work Stands

Read the repo before choosing. Everything for one piece of work lives in `docs/prds/{name}/`, or `docs/changes/{name}/` for a bounded change, or wherever the repo already keeps its documents; an idea cut into several PRDs also has `docs/roadmaps/{name}/`. When several rows match, the furthest stage reached (the lowest row) wins.

| What exists | Next skill |
|---|---|
| An idea, notes or a brief, no PRD | `prd-roadmap` if it is bigger than one PRD, otherwise `prd-writing-standards` |
| A new PRD roadmap | `prd-writing-standards` for its first planned PRD. Later ones start only when the user chooses, usually after the previous PRD reaches production |
| A drafted PRD, not yet refined | `autonomous-prd-refinement`; one `deliverable-review` round is enough for a small PRD. A `{name}-prd-refinement-state.md` in the directory means a run is in progress: resume it |
| A refined PRD, no technical design | `technical-design-writing-standards`, after the user's review when the user wants one. A small change that follows an established pattern and adds no new interfaces can skip the design and go to `implement-from-requirements`, which proceeds without one |
| A drafted technical design with no review commit after it, and no design refinement under way or finished | `review-technical-design`, in a fresh context |
| A reviewed technical design | `autonomous-design-refinement`, after the user's read of it when the user wants one. A `{name}-design-refinement-state.md` in the directory means a run is in progress: resume it |
| Refined requirements | `implement-from-requirements` |
| Phase documents | `implement-from-requirements` for the first leaf phase, in plan-table order, without a `**Closed:**` line |
| Every phase closed, no whole-PRD delivery audit yet (no `delivery audit complete (whole PRD)` commit) | `delivery-audit` on the whole PRD, in a fresh chat. The completion phases either audit adds, marked `**Added by delivery audit:**` or `**Added by test audit:**` at the top, are phase documents like any other: the row above builds them |
| Every phase closed after a whole-PRD delivery audit | `test-audit` on the whole PRD, in a fresh chat; it continues an existing `test-audit.md` and re-checks only what changed since its last audit. The PRD is complete when that run ends with `Done`. Never declare it complete from the file alone: a completion phase built since the last audit changes what it must check |

Five stages leave no file: a finished PRD refinement (its `PRD refinement complete` commit, or `PRD refinement stopped` when the user ended it with findings open, which its body lists; a small PRD's one `deliverable-review` round commits under the same subject), the design review (its `technical design review` commit, which it makes even when it changed nothing or skipped itself), a finished design refinement (its `design refinement complete` commit, or `requirements refinement complete` from before the skill was renamed), a delivery audit that found no gaps (its `delivery audit complete (whole PRD)` commit) and a build that was not split (its feature commit). Read them from `git log -- <directory>`. The PRD refinement, the design review and the delivery audit commit empty when they changed nothing (`pre-commit-validation`, "Who Commits"), and a path-limited log leaves empty commits out. So also list the subjects since the directory's first commit, `git log --format=%s $(git log --reverse --format=%H -- <directory> | head -1)..HEAD`, and look for the stage's subject with the same scope as that commit. Ask the user when neither says. The user's reviews are never a stage to detect: they are recommended, not required.

## The Order

**1. Decide what to build**

- `prd-roadmap`: only when the idea is bigger than one PRD. A PRD is a medium body of work, about the size of an agile epic. Decide which applies with the PRD-sized test in `prd-roadmap` (Step 2) rather than asking the user. Each planned PRD then goes through this whole sequence.
- `prd-writing-standards`: the PRD, saying what is built and why.
- `autonomous-prd-refinement`: reviews and fixes the drafted PRD, its assumptions and mockups in rounds until no Medium or High finding is left. **First recommended review point:** the user reads it, ideally with whoever owns the business decisions, before the design starts.
- `technical-design-writing-standards`: the technical design, saying how, committed as a draft.
- `review-technical-design`: started by the drafting skill in a fresh context. It questions the design's approach, checks its claims against the real code and the house standards, revises it in place and commits the revision; it skips itself for a design that follows an established pattern. **Second recommended review point:** the user reads the sections the review lists as worth reading.
- `autonomous-design-refinement`: closes the gaps in both documents without the user. Technical questions are researched; open business decisions become assumptions, and the build proceeds on them. `implementation-readiness-check` is the alternative when the user wants to confirm each open question themselves; only the user can start it.

**2. Build it in phases**

- `implement-from-requirements`: sizes the work, splits it with `phase-split` when it is too big for one session, and builds the first phase. Run `phase-split` on its own only to plan the phases without building.
- `continuation-prompt`: hands each next phase to a fresh session. In Codex, `phase-chain` runs an authorized sequence of phases on its own.

**3. Prove it works.** Inside every build, without being asked: `deliverable-review`, then `test-hardening`, then `pre-commit-validation`. Then the build commits, runs `refactor-pass`, and pushes a feature branch (a push to `develop` or `main` waits for the user's word), unless the user has said otherwise.

**4. Close out the PRD.** When the last phase of a split PRD closes, its build hands off to two audits, each in a fresh chat, before the PRD is done:

- `delivery-audit`: is every acceptance criterion built? Gaps become completion phases at the end of the plan, marked at the top as added by the audit, and `implement-from-requirements` builds them like any other phase.
- `test-audit`: once nothing is left to build, do the tests prove every criterion? It fills the gaps, missing tests first, and its `test-audit.md` carries the work across chats until its Status line says `Done`.

Either audit can also be pointed at a single closed phase when the user asks.

## Along the Way

- When preparing material for business stakeholders, `stakeholder-review-package` can package selected PRD requirements, every open assumption and contextual mockups into one HTML review. It is an optional review aid, not another implementation document or approval gate. The user sends it; assumption answers come back through `assumptions-document-feedback`, and requirements or mockup corrections go through `prd-writing-standards`. Stakeholders respond on their own schedule; nothing waits on them.
- A change to behavior an existing PRD already owns: amend that PRD and its design first (`prd-writing-standards`, "Document Storage Convention"), then build. A separate `docs/changes/` directory is the user's call; never create one unasked.
- A fix already identified, mid-work or from a bug report, that fits one session: `implement-from-discovery`. With only a symptom, `investigate-question` first. Anything bigger goes back to the user to open a PRD or change directory.
- One question to research to an answer with a confidence level: `investigate-question`.
- A session drifting from the method: reload `implementation-lifecycle`.

## Routing Rules

- **The two reviews are recommended, not required.** The refined PRD and the reviewed technical design are where human judgment goes in best. At each, say it is a good point for the user's review and what to read, then carry on when the user says to, or straight away when the user, or the prompt that started the run, asked to go through without stopping. Nothing refuses to proceed because a review didn't happen: like an assumption, an unreviewed document is a green light, and the user's corrections are folded in whenever they arrive. Beyond these, the user is not asked about requirements again; they start each next phase and send assumptions to stakeholders.
- **The requirements skills, the builds and the audits commit their own work** unless the user says not to (`pre-commit-validation`, "Who Commits"). The requirements skills and the delivery audit never push by default; builds and the test audit push when the push lands on a feature branch.
- **Requirements come before the build.** A request to build something new with no PRD starts at `prd-writing-standards`, or `prd-roadmap` when it is bigger than one PRD.
- **Start at the stage the work has reached.** Existing documents are not rewritten to restart the sequence.

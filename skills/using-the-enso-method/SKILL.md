---
name: using-the-enso-method
description: Where to start and what comes next in the Enso Method — which skill runs at each stage, in what order, and where the user reviews. Use when the user asks to use the Enso Method, asks "where do I start" or "what's next", or hands over requirements, an idea or a brief without naming a skill. A map only; each skill it names owns its own procedure.
user-invocable: true
---

# Using the Enso Method

The Enso Method builds software from requirements through a fixed order of documents, each written by one skill. The user reviews the PRD and the technical design before the next stage starts; after that the user is not asked about requirements again. This skill is the map: it says which skill comes next and nothing about how that skill works. Load the skill it names for that. The philosophy and session discipline (assumptions, confidence thresholds, No Loose Ends) live in `implementation-lifecycle`.

## Find Where the Work Stands

Read the repo before choosing. Everything for one piece of work lives in `docs/prds/{name}/`, or `docs/changes/{name}/` for a bounded change, or wherever the repo already keeps its documents; an idea cut into several PRDs also has `docs/roadmaps/{name}/`. When several rows match, the furthest stage reached (the lowest row) wins.

| What exists | Next skill |
|---|---|
| An idea, notes or a brief, no PRD | `prd-roadmap` if it is bigger than one PRD, otherwise `prd-writing-standards` |
| A new PRD roadmap | `prd-writing-standards` for its first planned PRD. Later ones start only when the user chooses, usually after the previous PRD reaches production |
| A drafted PRD, not yet refined | `autonomous-prd-refinement`; one `deliverable-review` round is enough for a small PRD. A `{name}-prd-refinement-state.md` in the directory means a run is in progress: resume it |
| A refined PRD the user has not yet reviewed | Present it for review |
| A reviewed PRD, no technical design | `technical-design-writing-standards`. A small change that follows an established pattern and adds no new interfaces can skip the design and go to `implement-from-requirements`, which proceeds without one |
| A reviewed technical design | `autonomous-requirements-refinement`. A `{name}-refinement-state.md` in the directory means a run is in progress: resume it (a `{name}-prd-refinement-state.md` belongs to the PRD refinement row) |
| Refined requirements | `implement-from-requirements` |
| Phase documents | `implement-from-requirements` for the first leaf phase, in plan-table order, without a `**Closed:**` line |
| Every phase closed | Recommend `test-audit` in a fresh chat |

Four stages leave no file: the user's reviews, a finished PRD refinement (its `PRD refinement complete` commit, or `PRD refinement stopped` when the user ended it with findings open, which its body lists, or, for a small PRD, its one `deliverable-review` round), a finished requirements refinement (its `requirements refinement complete` commit) and a build that was not split (its feature commit). Read them from `git log -- <directory>`, and ask the user when the log doesn't say.

## The Order

**1. Decide what to build**

- `prd-roadmap`: only when the idea is bigger than one PRD. A PRD is a medium body of work, about the size of an agile epic. Decide which applies with the PRD-sized test in `prd-roadmap` (Step 2) rather than asking the user. Each planned PRD then goes through this whole sequence.
- `prd-writing-standards`: the PRD, saying what is built and why.
- `autonomous-prd-refinement`: reviews and fixes the drafted PRD, its assumptions and mockups in rounds until no Medium or High finding is left. **The user then reviews it, ideally with whoever owns the business decisions, before the design starts.**
- `technical-design-writing-standards`: the technical design, saying how. **The user reviews it.** For a design that makes hard-to-reverse decisions, `review-technical-design` runs first and says which sections need the user's own reading.
- `autonomous-requirements-refinement`: closes the gaps in both documents without the user. Technical questions are researched; open business decisions become assumptions, and the build proceeds on them. `implementation-readiness-check` is the alternative when the user wants to confirm each open question themselves; only the user can start it.

**2. Build it in phases**

- `implement-from-requirements`: sizes the work, splits it with `phase-split` when it is too big for one session, and builds the first phase. Run `phase-split` on its own only to plan the phases without building.
- `continuation-prompt`: hands each next phase to a fresh session. In Codex, `phase-chain` runs an authorized sequence of phases on its own.

**3. Prove it works.** Inside every build, without being asked: `deliverable-review`, then `test-hardening`, then `pre-commit-validation`. Then the build commits, runs `refactor-pass`, and pushes a feature branch (a push to `develop` or `main` waits for the user's word), unless the user has said otherwise; when the last phase of a PRD closes, `test-audit` is recommended for a fresh chat.

## Along the Way

- Assumptions go to stakeholders on their own schedule (the user sends them); their answers come back through `assumptions-document-feedback`. Nothing waits on them.
- A change to behavior an existing PRD already owns: amend that PRD and its design first (`prd-writing-standards`, "Document Storage Convention"), then build. A separate `docs/changes/` directory is the user's call; never create one unasked.
- A fix already identified, mid-work or from a bug report, that fits one session: `implement-from-discovery`. With only a symptom, `investigate-question` first. Anything bigger goes back to the user to open a PRD or change directory.
- One question to research to an answer with a confidence level: `investigate-question`.
- A session drifting from the method: reload `implementation-lifecycle`.

## Routing Rules

- **The two reviews are the user's.** The PRD and the technical design are where human judgment goes in. Present each one and move on only when the user is ready. After that the user is not asked about requirements again; they start each next phase and send assumptions to stakeholders. Builds commit their own work unless the user says not to, and push it when it lands on a feature branch.
- **Requirements come before the build.** A request to build something new with no PRD starts at `prd-writing-standards`, or `prd-roadmap` when it is bigger than one PRD.
- **Start at the stage the work has reached.** Existing documents are not rewritten to restart the sequence.

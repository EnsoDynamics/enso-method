# Technical design review revises in place, reviews are recommended, and requirements skills commit (decision record, 2026-10-18)

Maintainer notes for `skills/review-technical-design/SKILL.md` (Phases 5 and 6 and "A design someone else owns"), "Rejected Alternatives" and Steps 1 and 6–8 in `skills/technical-design-writing-standards/SKILL.md`, the requirements-skills paragraph of "Who Commits" in `skills/pre-commit-validation/SKILL.md`, and their touch points in `using-the-enso-method`, `prd-writing-standards`, `autonomous-prd-refinement`, `autonomous-design-refinement`, `phase-split`, `prd-roadmap`, `continuation-prompt`, `implementation-lifecycle`, `docs/how-the-enso-method-works.md`, `docs/enso-method-setup-guide.md` ("If your instructions restrict commits") and the README. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing when the review edits, its bar for changing an architecture, or which skills commit.

## The problem

The user wants to run everything before implementation unattended, from an outside orchestrator: PRD refinement, the technical design, its review, design refinement, the phase split and the stakeholder review package. Three things stopped that:

- **The review handed its findings to a person and changed nothing.** Its triage was built for a senior engineer to act on. Unattended, an orchestrator skipped it, so the only skill that questions a design's approach never ran, and `autonomous-design-refinement`, which deliberately never asks "would it be better if…", spent its passes hardening a first draft nobody had challenged.
- **The map treated the user's reviews as gates.** "A refined PRD the user has not yet reviewed: present it for review", "once the user has reviewed the design". A run nobody watches stalls there.
- **The requirements skills handed every commit back to the user.** A run nobody watches left its work in a shared index, and design refinement's consolidation never ran, because it starts from the completion commit.

## Options considered

1. **Two modes in the review: triage for a person at the keyboard, apply for an unattended run.** Rejected. Whether anyone is watching can't be told reliably and shouldn't change the quality of the output, and a conversation gives a person nothing a committed diff and its report don't.
2. **Fold the review into `autonomous-design-refinement` as a first pass.** Rejected, at about 85% confidence. Refinement's scope gate forbids redesigning the frame, which is the review's whole job, so one skill would carry opposite rules. The commit between the two is the review's own diff and the cheapest point for a person's read, while the design is still small. Merging would only have guaranteed the review runs; the drafting skill starting it gives that.
3. **Chosen:** the review revises the design it reviews and commits the revision, the drafting skill commits its draft and starts the review in a fresh context, the reviews become recommended review points, and the requirements skills commit by default.

## Decisions and why

**The review revises in place**

- **Its normal input is the drafting skill's own output,** perhaps nudged once by the user. Nobody else's design is being rewritten. The author model changed from a junior engineer directing an AI to an AI's first draft; the scrutiny is the same.
- **A design someone else owns keeps the old behavior:** findings with proposed resolutions, rated, posted on the pull request, no edits. It is the rare case, so it is one subsection.
- **It runs in a fresh context.** Its first move is sketching its own design before reading this one, and the session that wrote the draft can't.
- **It skips itself in one line** for a design that follows an established pattern, so an orchestrator can always call it.
- **One pass, no loop.** Refinement repeats; a second loop over the design would grow it twice.
- **It always commits, empty when it changed nothing or skipped itself.** Without a commit the map can't tell a review that ran from one that never did, and would send the design back to it every time; the empty commit also keeps the report. `git commit --allow-empty --only` makes it without taking another session's staged files. A path-limited `git log` leaves empty commits out, so the map also lists the subjects since the directory's first commit. The rule sits in "Who Commits" for the two stages the map reads from history, the design review and the PRD refinement, since a small PRD's one review round can fix nothing too.
- **The draft is committed first** so the review's changes are one diff of their own. The user asked for both commits.

**The bar for changing an architecture is a closed list of defects, not a confidence level**

- **A percentage was rejected.** The method's 90% and 95% thresholds are confidence that an answer is correct, and they work because investigation moves them with evidence. Whether one working architecture beats another is judgment; a confidence figure on it moves between runs, which is the flip-flopping the user worried about. "90% sure it's the best" also has no reference point, and "90% sure it's better" doesn't say better by how much.
- **Three kinds of finding.** A gap or an error is always fixed: there is no other reading to swing back to. A swap, replacing a choice that would work, needs a verified defect from a closed list: it doesn't work, it departs from the house standards without a requirement behind it, a moving part no requirement needs, it duplicates what exists, or it closes an expensive door a modest change keeps open. A suspected but unverified problem becomes a factual Open Question for refinement to investigate, never a swap.
- **"Materially better" means it removes a named defect.** Cleaner, more elegant and "I'd have built it differently" never qualify. A second run reaches the same verdict because the defects are checkable facts, and a swap back needs a defect in the swap. Changes only move toward fewer defects, so the design settles.
- **Settled decisions are never changed.** A simpler way across a PRD decision or a validated assumption is a question for the user in the report.

**Rejected alternatives stay out of the design**

- **The user questioned recording them,** and the reasoning holds. A later reader needs the constraint that decided a choice: it says what not to break and when the decision can be revisited. A list of losing options adds nothing to either, costs every later session context, and an implementer that reads one can drift toward it.
- **No second document either.** Nobody would load it; the only time it matters is when someone proposes the alternative again, and then the constraint answers them or an agent redoes the comparison. The review's report goes in its commit body, where git keeps it and nothing loads it.
- **The drafting standard says so too,** as "Rejected Alternatives" beside "Decision History", so a draft doesn't carry them in the first place.
- **The drafting skill loads the house standards.** It didn't, which was half the reason the review existed; a draft held to them leaves the review less to fix.

**Reviews are recommended, not required**

- **The user's ruling:** nothing in the method is required, the reviews included. They are where human judgment goes in best, so each skill says it is a good point to read and what to read, then carries on when the user says or straight away when a run-through was asked for.
- **An unreviewed document is a green light,** in line with assumptions: corrections are folded in when they arrive. The map no longer treats a review as a stage to detect.
- **Public copy keeps the review as a principle,** and never claims the design needs no human look. The README and website say the agents review and fix first so a person's read goes on the decisions; the "not required" nuance lives in the skills and in `docs/how-the-enso-method-works.md`, which describes how the method runs and still calls the review the place a person's judgment goes in.

**The requirements skills commit**

- **The reason they didn't is gone.** `implement-chain-commits-by-default-decision-2026-10-11.md` rejected their committing because the user was about to review the documents. Reviews are now optional, and an unattended run needs its work in history.
- **Every requirements skill, not only the two new commits,** so "Who Commits" stays one rule rather than a stack of exceptions, which is what the 2026-10-11 record set out to end. Test audit and standalone deliverable review and test hardening still present their commit.
- **A user's own "never commit unless I ask" rule still wins,** and it is the likeliest way the default goes quiet unnoticed. The setup guide's "If your instructions restrict commits" gives a carve-out line that points at "Who Commits" rather than listing skills, so it can't drift as skills change. It is a conditional section, not one of the recommended lines, because a user who wants every commit held is served by the restriction as it stands.
- **They never push by default.** A later push of the branch carries them, and a push to `develop` or `main` still waits for the user. The user's instructions override the commit, in the precedence "Who Commits" already sets.

## Revisit when

- Swaps get reverted by hand often. The defect list is then too loose, or a defect is being claimed without verification.
- A design visibly flip-flops between two runs of the review. Record the case; the "a swap back needs a defect in the swap" rule failed.
- Designs keep regrowing "alternatives considered" sections through refinement or by hand. Conformance in `autonomous-design-refinement` would then need a row for them.
- Unattended runs stall on a pause that only a person can answer more than occasionally. That pause needs a state an orchestrator can read, or a default.

## Revised 2026-10-18: the test audit commits too

Later the same day `test-audit` joined the implement chain's default: it commits its work and pushes when the push lands on a feature branch. See `delivery-audit-and-prd-close-out-decision-2026-10-18.md`.

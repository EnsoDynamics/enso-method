# How the Enso Method Works

*A human-readable overview of the method. The skills themselves are the full definition; `skills/implementation-lifecycle/SKILL.md` is the umbrella.*

---

## The Problem

AI-assisted implementation sessions frequently stall waiting for human input. The AI encounters a question — "Should we include cancelled orders? What format should this field use? Which of these three approaches is best?" — and stops to ask. The human answers, but the damage is done: momentum is lost, the session may have timed out or lost context, and the pattern repeats on the next question.

This is expensive. Not because the questions are bad, but because most of them don't actually need a human answer. The AI has enough context to make a reasonable decision — it just hasn't been told that making the decision is part of its job.

## The Core Idea

**Assumptions are green lights, not yellow lights.**

When the AI encounters uncertainty during implementation, it should:

1. **Investigate first** — query databases, read code, check APIs, search documentation. Most questions can be self-resolved with a bit of research.
2. **If still uncertain** — pick the best answer at whatever confidence it has and keep implementing; a business question also gets a formal assumption entry.
3. **Only stop to ask when there is no answer to put forward** — the evidence favors none of the options, which is rare.

The assumption gets written into an assumptions document with a proposed answer, rationale, and confidence level. Stakeholders review assumptions asynchronously and correct any that are wrong. If a correction comes in, we re-implement — which is cheap with AI.

## Why This Works

**Implementation is cheap; waiting is expensive.** With AI, re-implementing a feature after a corrected assumption takes minutes. Waiting days for a stakeholder to answer a Slack message about a business decision costs far more in lost momentum and context.

**Most assumptions turn out to be right.** When the AI has done thorough investigation, the proposed answer is usually correct, and the stated confidence tells a reviewer which ones to check first. The few that need correction are caught during stakeholder review and fixed quickly.

**Questions compound.** A single implementation task might surface 5-10 questions. If each one blocks on human input, the task takes days of calendar time even though the actual implementation work is minutes. The assumption mechanism lets all of them proceed in parallel.

## The Four Documents

Each implementation area maintains up to four documents that form a system, all colocated in the PRD's directory:

- **PRD** — what we're building and why (acceptance criteria, scope)
- **Technical Design** — how we're building it (data flows, mappings, integration points)
- **Assumptions Document** — business decisions we've proposed but haven't confirmed yet (treated as decided until corrected)
- **Phase Documents** — only when a PRD is too large for one AI session and gets split: each phase doc scopes one session-sized slice (or, once that phase is itself split, lists its children), one file per phase at every depth with `phase-split` owning the naming, and over the project's life accumulates the follow-up work other phases route into it

The PRD and technical design are the source of truth. Code implements what they say, and every change — ad hoc ones included — amends them first. Assumptions keep work unblocked. A genuine blocker that can't be resolved through assumptions is surfaced to the user right away, with the blocked work recorded in the PRD or phase document so the next session sees it. When a PRD has been split into phases, follow-up work discovered mid-implementation that survives the materiality gate gets filed into the future phase document it naturally belongs to: those docs are loaded automatically when the phase is built, whereas nothing automatically comes back for a ticket in whatever the org uses to schedule work.

These documents colocate inside `docs/prds/{prd-name}/` (a program) or `docs/changes/{name}/` (a bounded delivery — a ticket, a bug, a small enhancement — identical layout) so everything tied to a piece of work lives in one place. See `prd-writing-standards` for the full directory structure.

## Confidence Thresholds

| Confidence | Action |
|-----------|--------|
| **95%+** | Just do it, whatever the impact — no need to document or ask |
| **Below 95%** | Proceed on the best answer, and document it as an assumption for stakeholder review, at its honest confidence |
| **No answer to put forward** | Stop and ask — only when the evidence favors none of the options (in practice, a best answer under roughly 20%) |

That is the gate for business questions. Technical questions proceed on the best answer, with the reasoning in the commit message; they rarely become assumptions. The below-95% business range is where the framework adds the most value. Without it, all of these become blocking questions. With it, they become documented decisions that keep implementation moving.

## What This Means in Practice

An AI session working under this framework will:

- Read the PRD and technical design before starting
- Treat existing assumptions as decided facts
- Investigate questions thoroughly before declaring new assumptions
- Distinguish technical questions (usually self-resolvable) from business questions (may need the assumption mechanism)
- Never present the user with "Option A or B?" — instead, pick the better option and document why
- Finish the build with a two-step quality chain: **deliverable review** (fresh-eyes check that the work matches intent) followed by **test hardening** (fresh-eyes check that the tests actually prove the acceptance criteria — real resources over mocks, assertions that would fail if the behavior were wrong). Both run automatically; neither waits to be asked for. After the user commits, an optional **refactor pass** is recommended: a decline-biased judgment on whether the work left the code structurally worse, executing only small, structure-only tidies as their own commit — most sessions correctly end with "no refactor warranted". When the last phase of a split PRD closes, a **test audit** is recommended too: an independent grade of every acceptance criterion's test evidence across all the phases, which then fills the gaps, missing evidence first
- Disposition every loose end instead of reporting it: dismiss it (the default for anything immaterial), deal with it now, file it into a document a future session will load, or ask a one-line question with a recommended default — never end with a list of FYIs and caveats. Items the work's continuation will handle surface only as a one-line count summary ("2 assumptions declared, 3 items filed to phase 4"); only what needs the user is named
- Never announce future work it could do right now ("I'll add that test," "next X should be updated") — it does the work, or files it somewhere concrete, before wrapping up
- End every task in a clean terminal state: implemented, blocked and surfaced to the user (recorded in the PRD or phase document), awaiting a human action it has prepared and recorded, or intentionally left as-is with documentation

The session discipline ("No Loose Ends") is defined in full inside `implementation-lifecycle`, the umbrella skill for the whole methodology. If a session drifts — FYIs piling up, predictable questions, promised-but-not-done work — telling it to re-read `implementation-lifecycle` restores the whole methodology in one step.

The result is fewer interruptions, faster implementation, and a clear paper trail of every decision made along the way.

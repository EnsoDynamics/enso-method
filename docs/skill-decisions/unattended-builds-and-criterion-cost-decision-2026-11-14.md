# Unattended builds and criterion cost (decision record, 2026-11-14)

Maintainer notes for the new `skills/build-preflight/SKILL.md` and for edits to `prd-writing-standards` ("Criteria Describe What Is Built", "Keep Each Criterion Worth Its Cost", "The End-User Test Guide"), `autonomous-prd-refinement` ("Keep It Readable"), `technical-design-writing-standards` ("Price Each Criterion", "Delivery"), `review-technical-design`, `phase-split` (Step 3 and the leaf template), `implementation-lifecycle` ("Don't Stop to Ask") and `delivery-audit`, with their mentions in `using-the-enso-method` and the README. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing what may stop a build, what an audit counts as a gap, or what the preflight reports.

It builds on the 2026-11-08 change that took deploys, sign-offs and calendar time out of acceptance criteria.

## The problem

Once the requirements are settled, the build should run to one pull request with nobody watching and nobody asked. Two things kept breaking that.

**Builds stopped part-way.** The 2026-11-08 rules remove the stops a criterion causes. Stops also come from places those rules do not reach: phase documents that put a per-phase deploy back in, a repository's own instruction file requiring approval before spending, a session waiting on a job in a shared environment, the owner being asked what to do about a quality bar the build missed, proof that needs a person's signed-in browser, and a sign-in that expires before the first live test.

**Builds that ran cost far more than planned.** The delivery audit can add more completion phases than the plan had phases, including on PRDs written after the 2026-11-08 rules. The gaps behind those phases fall into four groups:

| Cause | What it is |
|---|---|
| Real defects | Something a user would hit. The audit working as intended, and usually the largest group. |
| Polish | Wording, counts and screen-width presentation. |
| Criteria by reference | Criteria taken from another PRD that was still changing. |
| Restarts | Whole-PRD audits run again after stakeholder feedback, or after a change to the audit skill mid-build. |

Many gaps cite the technical design, not the PRD. The audit does not settle: each run of rounds reaches zero and a change restarts it over every criterion. A few criteria produce most of the polish work, and they share shapes: a rule over every control on every screen, a criterion of several hundred words for a one-time check, criteria that grew to several times their first length. Criteria that refinement added carry no mark, so nothing downstream can tell them from what a stakeholder asked for.

Over-engineering in the strict sense (permanent machinery for a rare, short-lived state) is real but a small share. The reference example: a criterion to keep the last good page on screen during a ten-minute rebuild a few times a year, designed to the letter, needs permanent backward-compatibility machinery in every page script.

## The failures and where each is handled

| # | Failure | Where | How |
|---|---|---|---|
| | **The build cannot run unattended** | | |
| 1 | A person must act mid-build | `prd-writing-standards` | Not a criterion; before or after the build (2026-11-08) |
| 2 | Waiting on calendar time | `prd-writing-standards` | Behavior proved with a controlled clock (2026-11-08) |
| 3 | A deploy or merge in the middle | `technical-design-writing-standards`, Delivery | Only when a named criterion has no other proof (2026-11-08) |
| 4 | Phase documents put a stop back in | `phase-split`, Step 3 | A phase adds no stop Delivery does not list |
| 5 | Proof only a person can give | `prd-writing-standards` | Rewritten for a test sign-in or recorded data; the rest goes to the end-user test guide |
| 6 | The build asks the owner about a missed bar | `implementation-lifecycle` | The measured figure becomes an assumption and the build carries on |
| 7 | Hands-on work with no scripted way | Delivery and `phase-split` | Listed in the design, planned into the first phases, marked `**Attended:**` |
| | **It runs, but costs days** | | |
| 8 | A criterion that needs machinery out of proportion | `technical-design-writing-standards`, `review-technical-design` | Price each criterion; narrow or drop |
| 9 | A rule over everything, polish, or one-time work as a feature | `prd-writing-standards`, `autonomous-prd-refinement` | Three named shapes, kept out or narrowed |
| 10 | Refinement's own criteria are unmarked | `prd-writing-standards`, `autonomous-prd-refinement` | An `Added in refinement.` line |
| 11 | The audit judges against the design | `delivery-audit` | Required parts come from the PRD only |
| 12 | The audit chases polish | `delivery-audit` | Presentation is not a part unless the criterion quotes it |
| 13 | The audit loop does not settle | `delivery-audit` | A repair audit re-reads only what the repairs could have changed |
| 14 | The end-user test guide becomes homework | `prd-writing-standards` | Only what the build could not prove |
| | **The environment is not ready** | | |
| 15 | Missing access, expiring sign-ins, the wrong machine | `build-preflight` | Commands and yes-or-no items, before the build |
| 16 | House rules that force a stop | `build-preflight` | Named and settled once, before the build |

## Options considered

1. **One late review before the build that covers everything, criterion cost included.** Rejected. By then the user has finished the requirements, and a list of doubts about them with no sharp action attached sends them back into work they believed was done. The preflight is limited to what a command or a yes-or-no settles.
2. **A fixed list of banned criteria.** Rejected. Whether a criterion earns its cost depends on the product. The method names three shapes that are nearly always wrong and requires the design to weigh the rest.
3. **Hand the user the costly criteria to rule on.** Rejected. The method does not leave open questions. The agent narrows the criterion and declares an assumption, and the build proceeds on it.
4. **A cap on audit loops in the skill.** Left to the orchestrator. A person running sessions by hand sees a loop and asks about it; an orchestrator needs a number, and can also say what to do when it is reached. The skill instead removes the causes: the design as a yardstick, polish as a gap, and whole-PRD re-reads after every repair.
5. **Make the preflight part of `implement-from-requirements`.** Rejected. That skill runs once per phase and already checks its own session's access. The preflight looks across every phase once, and an orchestrator needs something it can run before any build session exists.

## Decisions and why

**Criterion cost**

- **Cost is judged at the design, shape at the PRD.** A criterion's wording shows its shape, so the three shapes are caught when it is written and refined. What it costs to build is only visible once it is designed, so pricing happens there, and the design review, which sketches its own simpler design first, is the fresh check.
- **Where a criterion came from decides how freely it changes, not whether it can.** One that refinement added is narrowed or dropped by the design. Any other is narrowed with an assumption a stakeholder can overrule. One that restates a stakeholder's decision, or a validated ruling, is reopened under Gate 3: the design builds the simpler version and the PRD keeps their words until they revise them, because the method never edits a stakeholder's own record. The audits already treat that as changed outside the requirements, not as a gap. Source material is not always a stakeholder's words, so the mark is set against `requirements-intake`'s "Whose Words Count", not against whether the source mentions it.
- **`Added in refinement.` marks only later additions.** Marking every criterion with its origin would be a second document of record. The first draft is written from the source; the additions are what nobody outside the refinement saw.
- **The review's "settled decisions" rule gives way here.** That rule kept a PRD decision in place and raised a question for the user. For cost out of proportion, a question nobody reads leaves the cost in. The swap bar for architecture is unchanged.

**The delivery audit**

- **The PRD is the only source of required parts.** The design says how the team chose to build it. A design detail that matters to a user breaks a criterion and is still found; one that does not is not a gap. The test audit already worked this way.
- **Presentation is not a part.** The build's own review has looked at the screens, and the user will. An audit that sends a build session after a tooltip costs more than the user fixing it in a sentence. Text or a value a criterion quotes is still checked.
- **A repair audit is narrower, and still the close-out audit.** It finds what to re-read from the files changed since the earlier audit, since no audit keeps a map of files to criteria. Its commit subject keeps `(whole PRD)` because the router and orchestrators read that fact. It keeps earlier statuses for criteria the repairs could not have touched, which is where the restarts spent their time.

**Stops**

- **A missed measured bar is an assumption at the measured figure, and the criterion is amended to it.** Asking is a stop, and working on indefinitely is a loop. Without the amendment the phase could not close and the delivery audit would report the bar as a gap again. A figure a stakeholder set is reopened under Gate 3 instead.
- **Hands-on work is listed, front-loaded and marked.** Some work has no API. Hiding it produces a build that stops three minutes in, after the user has left. The `**Attended:**` line lets a tool show it before the run.
- **The end-user test guide stays optional and short.** It is where a person's own look belongs, and a long one is a sign the criteria were not provable.

**The preflight**

- **Every item is a command or a yes-or-no.** Anything else is too late to be useful at that point.
- **The first line is fixed** (`Preflight: ready` or `Preflight: N items need you`) so an orchestrator can read it without parsing prose.
- **It changes no file,** except a phase document whose unlisted stop the user agreed to remove, which goes through `phase-split` and its commit rule, and the Delivery line that records an authorization. The authorization is recorded in the design, not passed in a prompt, because a prompt reaches only the first phase.
- **It is optional.** The method works without it and without an orchestrator.

## Not addressed

- **Criteria taken by reference from a PRD that is still changing.** The feedback skills already carry a changed contract into each PRD that consumes it; whether a build should pin what it referenced needs its own look.
- **A mid-build change to the method itself.** An orchestrator can pin the version for a run. Nothing in the skills can.

## Revisit when

- Designs narrow criteria that stakeholders then ask to have back. The pricing test is too eager, or the assumption is not reaching them.
- A repair audit misses a regression in a criterion it did not re-read. The test for "could have changed" needs tightening.
- Users report screens that are plainly wrong after a clean audit. "Presentation is not a part" is hiding real gaps.
- Preflight reports grow past a handful of items, or items appear that are not a command or a yes-or-no.

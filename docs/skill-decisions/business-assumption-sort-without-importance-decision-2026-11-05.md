# Business is a kind an entry qualifies for, and importance plays no part (decision record, 2026-11-05)

Maintainer notes for `skills/assumptions-document-writing/SKILL.md` ("Sort Every Entry by What Would Settle It") and `skills/stakeholder-review-package/`, plus the matching lines in `autonomous-prd-refinement`, `autonomous-design-refinement` and `assumptions-document-feedback`.

## The problem

- **Stakeholder reviews still held questions no stakeholder should get,** after the sort by what would settle it shipped. A sort run exactly as written could keep every open entry. Such entries included test-set sizes, the project's finish line, a build budget, and one stakeholder being asked whether another must approve something.
- **Nothing was skipped, so the fix had to be in the rule.** Build choice and fact were defined narrowly and business was what remained, and the tiebreak said that if a stakeholder might care, the entry is business.
- **The reviews were also hard to read.** The cards were long and in project shorthand, with the decision that set the outcome buried among the others.

## Options considered

1. **A fourth kind for calls the team can make, gated by a four-part test including "being wrong costs more than asking".** Tried and rejected. It worked as an importance filter, which sends away questions their owner would answer differently. It also lowered what a stakeholder sees, in a review that is the only place they see it.
2. **A cap of seven questions and word limits on cards.** Tried and rejected as arbitrary. Thin requirements honestly produce more assumptions, and a cap punishes that instead of the real fault, which is asking questions of the wrong kind.
3. **Name the ways an entry isn't a business question, and leave importance out.** Chosen.

## Decisions and why

- **The line is intent versus implementation,** the distinction the requirements field already draws. Business requirements are the why (objectives, success measures, scope), per Wiegers and Beatty's levels. The [Scrum Guide](https://scrumguides.org/scrum-guide.html) makes the product owner accountable for value and leaves how to build it to the developers alone. [SVPG's four risks](https://www.svpg.com/four-big-risks/) put value and viability, including legal, finance and brand, with the product side and feasibility with engineering, which is why a technical-sounding data-retention question can still be business. "How do we know we're done?" splits the way [acceptance criteria and the Definition of Done](https://agile.appliedframeworks.com/applied-frameworks-agile-blog/definition-of-done-vs-acceptance-criteria-a-deep-dive) do: did it deliver what was wanted, and was it built properly.
- **Impact now means how much the answer changes the outcome, not the cost of rework, and it sets the order only.** Rework cost told a reader nothing and never reached the review. The existing High, Medium and Low scale is kept because a percentage would be false precision. It is shown beside confidence, and sorts sections and the cards within them, keeping the written order within a level so a question defining a term can precede one using it, without a single list that would pull a question away from its mockup. A dollar figure alone doesn't make an entry High, since that would make nearly everything High in a product about money, though many entries there can rightly be. The register line is renamed from `Impact if Wrong` to `Impact`, and the renderer refuses a card with no Impact. The skills don't carry instructions for the old line: it is a short-lived migration, and every re-sort rates Impact by the current definition anyway. `implementation-readiness-check` and `investigate-question` keep their own in-chat `Impact if wrong` line, which is a different use.
- **Every business assumption goes to the review.** Whether something is important enough to show is never asked. Importance was already outside the method's inclusion rule, since 95% confidence leaves an entry out whatever its impact.
- **Business has to be qualified for.** A sort keeping an entry states what would be built differently. A sort that moves nothing gets a second look, because that result can't be told apart from a failed sort.
- **The ways an entry fails are named, because "obviously a business question" did not hold:** it is about how we build or run the work, it is already answered, it has only one sensible answer, both answers build the same thing, it is asked of the wrong person, or it is worded as a build question.
- **Running the work is build judgment.** Test sizes, quality bars and which checks prove the build works were reading as business because they matter. What a stakeholder will accept as done, or a budget only they hold, stays theirs.
- **A write-up is marked as the team's call.** An entry with one sensible answer leaves the body as `Written up` in the Validated table, so nobody later reads it as a stakeholder's ruling.
- **Moving an entry never changes what it says.** Moving an entry is no chance to change a value nobody decided. A figure that looks wrong goes to the person running the work.
- **A reading that narrows or departs from what a stakeholder said stays theirs.** Only a word with one sensible reading gets applied without asking.
- **The renderer enforces what isn't a judgment call:** each card says what the answer changes, Start here is filled from Impact, and common build shorthand and IDs the reader can't see are refused. A bare `#123` is left to the cold read, since real records are written that way too. These force clarity without limiting how many questions a review holds or how long a card runs.
- **A cold read replaces the author re-reading cards.** A fresh subagent with no project context answers each card as that person and says what was hard to read. It can send a card back for being the wrong kind, never for seeming unimportant.
- **Common practice is part of the lookup,** for questions about how a product should behave. It gives a proposal its reasoning and settles a question only when it leaves one sensible answer, because much of what a business wants is opinion.

## Not required on every entry

- A named answerer, or a marker addressing a card to a role. The review goes to its business stakeholders, and that is enough. When a question belongs to one person among several, or was asked of the wrong one, the entry says so in its text. The cold read accepts that, instead of treating a card's own stated handoff as a failure.

## Not changed

- Confirm and Change remain the only answer controls. Whether a question should instead offer worked options with a recommendation is a separate decision.

# Readable PRDs under review rounds, and two severity calibrations (decision record, 2026-10-12)

Maintainer notes for "Keep Criteria Readable as Cases Are Added" and the mockup-note bullet in `skills/prd-writing-standards/SKILL.md`, two calibration bullets, the Medium row's "unstated case" example, the Check Clarity question and the design-reference links rule in `skills/deliverable-review/SKILL.md`, and "Keep It Readable", "Say what settles each fix", the full-round questions and the criteria-words column in `skills/autonomous-prd-refinement/SKILL.md`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before loosening the readability rules or the two calibrations. It revises `autonomous-prd-refinement-decision-2026-10-12.md`, written the same day.

## The problem

The first full run of `autonomous-prd-refinement` refined a PRD with 44 criteria, 18 assumptions and 32 mockup states over 13 rounds (4 full, 9 delta). It found no High, 29 Medium and 151 Low, and fixed them all. The PRD came out more correct and much harder to read:

- **The criteria grew 66% with no new requirement.** The PRD went from 8,736 to 12,785 words, the criteria from 4,311 to 7,136, and the number of criteria stayed at 44. Four criteria grew three to five times; one went from 77 words to 386.
- **Each Medium added a clause.** Case walks kept finding one more case a stated rule had not spelled out, and the fix wrote it in. Rounds 5 to 8 were a chain: each fix exposed the next exit from the same rule ("nothing happens until an unknown result is known"), which the next round rated Medium.
- **Mockup links generated their own work.** Most Lows in the later rounds were about which mockup button linked to which state. The Mockups section's notes grew from 462 to 1,079 words explaining it.
- **Business decisions went in as rules.** Several fixes decided business behavior (what happens to a job's live work when it is deactivated, when a setting change takes effect) without becoming assumptions, so they would reach the stakeholder as text to skim rather than a question to confirm.
- **Full rounds kept finding Mediums.** The cap was reached at 12, raised once to 13, and the last full round still found two; the user stopped there.

The user's concern: a PRD nobody will read gets no real sign-off, and clause-on-clause criteria help an agent no more than they help a person.

## Options considered

1. **Raise the Medium bar across the board.** Rejected: most of the run's Mediums were real gaps. The trouble was narrower, in cases a stated rule already settled and in what the fixes wrote.
2. **A length limit on criteria.** Rejected as a limit: a hard number invites padding or cramming. Kept as a tripwire in words a reader recognizes ("no longer reads as one short paragraph").
3. **Leave the leftover edge cases to `autonomous-requirements-refinement`.** Partly: the technical design applies a stated rule to each place it touches, so a case a rule settles needs no PRD text. But a PRD that is not crisp makes everything downstream worse, so the readability rules apply while the PRD is written and refined, not later.
4. **Chosen:** readability rules in the writing standard, two calibrations in the severity scale, and the refinement loop tracking growth and asking about readability and assumptions at full rounds.

## Decisions and why

- **A case a stated rule already settles is Low at most.** The Medium test is "would have to stop and ask"; a reader who can apply a stated rule has nothing to ask. Medium stays for no applicable rule, or two rules that disagree. This cuts the chain that drove rounds 5 to 8 without lowering the bar for real gaps. The Medium row's "unstated case" example now says "that no stated rule settles", so the table and the calibration read the same. The table was otherwise left alone.
- **Readability of a sign-off document can be Medium.** A requirement buried in clauses, so a reader can no longer say what is being checked, defeats the sign-off the document exists for. Length alone is Low, so a long but clear criterion does not hold the loop open. The fix is a rewrite, a split or a table, never another clause.
- **Restate, don't append; tables for rules with many cases.** The user suggested a table beside a criterion that has many sub-rules. A table keeps the criterion to one checkable sentence and puts the cases where a reviewer reads them one row at a time and a test covers them one row at a time. It works the same for a person and for an agent.
- **"Today" stays as one short sentence.** Moving all context out of criteria was the first draft. On review it lost something a builder needs: when a criterion deliberately changes current behavior, one closing sentence saying so stops the old behavior being kept. Evidence and history still go elsewhere.
- **State each rule once.** Restated rules drifted, and every copy was one more place a fix had to reach; missed copies were a steady source of findings.
- **Links between mockup states are not reviewed, and notes stay short.** They are a convenience for stepping through a design reference, like layout polish, which was already excluded.
- **Say what settles each fix.** Source, existing rule, or new decision. Only a new business decision becomes an assumption: an assumption for every consequence would bury the real questions (`assumptions-document-writing` warns about review fatigue).
- **Full rounds also ask whether an assumption's answer now looks wrong.** Fourteen of the 18 assumptions were amended in the run, but only when a finding happened to touch one; nothing asked the reviewer to challenge them.
- **Track criteria words per round.** Growth was invisible until the run ended. A column in the Rounds table makes it visible each round, and the completion report gives the before and after.
- **The round cap stays at 12.** It did its job: it paused the run and handed the decision to the user. The diminishing returns it exposed are what the changes above address.

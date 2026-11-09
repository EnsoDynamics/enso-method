# Research every open business assumption during PRD refinement (decision record, 2026-11-09)

Maintainer notes for `skills/autonomous-prd-refinement/SKILL.md` ("The Research Pass"), `skills/investigate-question/SKILL.md` ("Researching a Business Assumption"), and the matching lines in `assumptions-document-writing`, `autonomous-design-refinement`, `requirements-intake`, `prd-writing-standards` and `stakeholder-review-package`.

## The problem

- **No step researched a business question.** The write-time lookup is bounded to minutes, `investigate-question` excluded business questions, and design refinement sent them straight to assumptions.
- **Review rounds only added.** Their fixes grew the register and added some of its weakest entries, while questions already answered by rulings stayed open.
- **Stakeholders' raw material was out of reach after intake,** though answers often sit in passages filed under another topic.

## Decisions and why

- **Research happens before each full round, per entry, with the proposed answer withheld,** because an investigator holding an answer finds support for it. A survey of competing libraries found none that takes each open question back to stakeholders' material.
- **All research is available:** stakeholders' raw words, market research, data queries and throwaway scripts.
- **Research rewrites rather than appends,** and an entry is moved, never deleted: a deleted assumption is the same open question, undisclosed.
- **A reader in the stakeholder's seat marks "why are you asking me?"** during refinement, not only at review-package time.
- **The line is judged strictly, never by count.** Touching money or authority does not put an entry above it; the answer must materially change the outcome. A cap on the asked list was tried and dropped again, as in the 2026-11-05 record: list length would have pushed real questions down, and a long list of good questions stands.
- **Research that reaches 95% settles the question,** with no assumption needed, so the bar still keeps the register short. An entry already holding an ID leaves as `Written up`, so its question stays on record.
- **A `**Researched**` line on the entry** survives the state file, tells later passes what was tried, and lets the review package research any entry that skipped refinement.
- **What stakeholders said about being asked** is captured at intake and applied.

## Not changed

- The review loop and its stop rules. A cold builder check as the loop's ending was considered and left for a separate decision.

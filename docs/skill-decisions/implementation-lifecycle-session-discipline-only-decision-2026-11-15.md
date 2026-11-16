# Cut implementation-lifecycle back to session discipline (decision record, 2026-11-15)

Maintainer notes for `skills/implementation-lifecycle/SKILL.md` and the sections that moved out of it into `prd-writing-standards` ("When Later Work Changes an Earlier Criterion"), `engineering-principles` ("The test tripwire", "Session Markers", "Parallel Sessions: Where to Work", "One Branch for a Split PRD") and `continuation-prompt` ("The lineage gate"), with matching lines in the implement skills and the assumptions skills.

## The problem

- **The skill existed for one job and had grown to carry six.** It was written so a build session would stop handing the user lists of questions and asides, and would decide by the method instead. Because it was called the umbrella, later rules landed in it: the conflict check, session markers, worktree and branch mechanics, the lineage gate, a workflow summary and a skill table. It reached 540 lines, about half of them unrelated to its job, and every build session loaded all of it.
- **The on-mission half repeated itself.** "Don't stop to ask" was stated about six times, the no-FYI rule about eight, and the assumption-entry rule four.
- **The skill authorized some of what it existed to stop.** Work noticed outside the PRD was named in the wrap-up as the user's decision; nice-to-have work on a last phase was asked about; each declared business assumption got its own callout.
- **Two of the stops were open to interpretation.** "Critical" and "no answer to put forward" had no definition tight enough to keep ordinary findings and ordinary uncertainty out.

## Decisions and why

- **The skill stays, as its own skill.** `using-the-enso-method` loads when routing, and the discipline has to be in the build chat's context. Three procedural skills share it, and a drifting session needs one name to reload.
- **No new skill was added.** Each section that left already had a half-owner:
  - The ownership rule, the shipped-behavior rule and the conflict check went to `prd-writing-standards`, which held the pointer format and pointed back for the rest. The refinement skills run the conflict check too, so it is a requirements rule.
  - The test tripwire went to `engineering-principles`, beside "never hack it green."
  - Session markers, where parallel sessions work and the one-branch rule went to `engineering-principles`, beside its git safety section, which every build already loads. `pre-commit-validation` loads at commit time, too late for rules that apply before the first edit.
  - The list of work that legitimately has no PRD phase went to `continuation-prompt`, which already owned the lineage block and its gate.
- **Deleted:** the implementation workflow summary, the related-skills table and most of the four-entities section. `using-the-enso-method` and the implement skills already say all of it. What remains is "Which Document Carries What."
- **An observation is dismissed, wherever it is.** Work no criterion of the PRD needs is not done, not filed, not asked about and not mentioned, on the last phase as much as the first. Looking for bugs and improvements is a job the user starts on purpose. Filing now has the same bar as doing: a criterion of this PRD needs the item.
- **Work a criterion needs that will not fit the session is split with `phase-split`,** silently. The new phases carry scope the PRD already has.
- **A declared business assumption is a count in the ledger line,** not a callout. The assumptions document is where it lives, and the count is the cue to refresh the stakeholder review package.
- **Four stops, each defined.**
  - A critical finding is harm that is real, happening now or about to, and not repairable by a later fix: real money moving wrongly, production data lost, production down, a live production credential or customer data exposed. Code that deals with money is not critical because it deals with money. It stops the session early only when the session's own continued work is the danger; otherwise the phase is finished and the finding leads the final message, because stopping the build does not reduce the harm and an orchestrated run would halt on a half-built phase. The security line was added after a scenario test: with only the first three, a leaked production secret outside the PRD was dismissed silently, where the old wording surfaced it.
  - A blocker is access the session cannot obtain, with no criterion work left that can proceed.
  - An action only a person can take is prepared and recorded.
  - A business question is asked only when its best answer is below 20% after significant investigation, and the ask still names that answer. The earlier wording, "under roughly 20%, no option favored," left room for a question with no recommendation.
- **A technical question never stops a session to ask.** A build choice is decided, a fact is investigated, and a fact out of reach is a technical assumption naming its blocker.

## Not changed

- The confidence thresholds at 95% and 90%, the Materiality Gate's four criteria, the adjacency tests, the three-question wrap-up test and the terminal states.
- The moved sections' rules. They were moved as written, with only their cross-references updated.
- The skill's name. It no longer describes the whole lifecycle, but about 140 references use it.

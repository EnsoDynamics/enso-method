# Implement chain commits and refactors by default, and pushes feature branches (decision record, 2026-10-11)

Maintainer notes for "Who Commits" in `skills/pre-commit-validation/SKILL.md` and its touch points in `implement-from-requirements`, `implement-from-discovery`, `refactor-pass`, `phase-chain`, `phase-split`, `continuation-prompt`, `deliverable-review`, `implementation-lifecycle`, `using-the-enso-method` and `docs/how-the-enso-method-works.md`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing who commits, who pushes, or when `refactor-pass` runs.

## The problem

Every skill that ended at a commit staged its files and handed the commit to the user, and the implement skills recommended `refactor-pass` for after that commit without ever running it. In manual use two things went wrong:

- **Commit behavior was inconsistent.** Some sessions committed and pushed, others stopped with "I didn't commit yet", within one project. The rule was stacked across several files ("Who Commits", each implement skill's wrap-up and rule lists, `refactor-pass`), each with its own exception wording, and sessions resolved the stack differently.
- **The refactor pass never ran.** It needed the user to commit, then to take up a one-line recommendation. Across many phases the user's answer was "keep moving", so the step existed only on paper.

## Options considered

1. **Keep "the user commits" and tighten the wording.** Rejected: the inconsistency came from a default the user overrode in most sessions anyway, and it leaves the refactor pass dependent on a recommendation nobody takes.
2. **Every skill that ends at a commit commits and pushes by default.** Rejected for now: design refinement, phase split and PRD roadmap produce documents the user is about to review, and a test audit's fixes are reviewed against its report. The friction that motivated the change was in the implement chain.
3. **Commit and push everywhere, by default.** Rejected: a push to `develop` or `main` publishes to the branch everyone builds on, and a person running one session on `develop` wants to look before that happens.
4. **Commit and push only off `develop` and `main`, judged by the branch the session is on.** Rejected: the motivating sessions were manual ones on `develop`, so they would go back to not committing and the refactor pass would stop running again. And a worktree chat sits on a `wt/` branch but lands straight on `develop`, so the session's branch doesn't say what the push publishes.
5. **Chosen:** the implement chain (`implement-from-requirements`, `implement-from-discovery`, and the `refactor-pass` they run) always commits and runs the refactor pass by default, and pushes by default only when the push lands on a feature branch. Every other skill keeps handing the commit to the user.

## Decisions and why

**Scope**

- **The implement chain only.** It is where the method runs end to end without the user, after the PRD and design reviews, so it is where a stop for a commit costs the most and buys the least.
- **The other skills are unchanged and say so.** "Who Commits" names them: design refinement, phase split, PRD roadmap, test audit, and `deliverable-review` or `test-hardening` run on their own present the commit for the user. A phase split called from an implement session needs no rule of its own: its phase docs ride the implement session's commit.

**Precedence**

- **The user's instruction in this chat or in the prompt that started it, then the user's instructions file (global or repository AGENTS.md or CLAUDE.md), then the skill's default.** A user who wants to review before anything lands says so once and the chain stops at a staged changeset with the message presented. "Don't push" stops it after its commits. An instructions file outranks the default so a team or a person can turn it off everywhere without repeating it per chat; where a global and a repository file disagree, the more restrictive wins, because a wrong push costs more than a stop.
- **Finishing the work is still not an instruction** for the skills outside the chain. Their old rule stands unchanged.
- **A restriction travels with the work.** A "don't push until I say so" given for a track is carried in the user's words into the next chat's prompt (`continuation-prompt`), or that chat's default would override it.

**What the default covers**

- **Finished work only:** the full suite green apart from failures that predate the work, and any terminal state but Blocked. A Blocked session stages and presents its commit, so partial work never reaches the remote on a default.
- **The feature commit comes after every wrap-up doc edit.** Before, the user's commit came after the wrap-up and caught every doc edit it made. Now the closure line, the continuation prompt's doc edits, the roadmap row, new assumption entries and filed items are written first, so they ride the feature commit, and the next chat's prompt is presented after the push with the real hashes.
- **The closure line no longer carries a commit hash.** A line inside a commit cannot name that commit, and with committing now the default the instruction would have forced an extra commit every phase. `git log -- <phase doc>` finds it.

**Push**

- **Commit always; push by where the push lands.** A push to a feature branch publishes nothing anyone else builds on, so it is the default. A push that would land on an integration branch — `develop`, `main`, `master`, a branch the repository's instructions name as shared, or a branch whose push releases to production — is held after the commits, with one line asking the user to say push. That covers a shared checkout on `develop` and a worktree chat landing on `develop` alike. The local commits keep the work consistent and revertible, and they give the refactor pass its baseline.
- **Orchestrators authorize explicitly.** A sequence run by an orchestrator gets its pushes from the prompt that starts each session, so the default never has to guess that a session is orchestrated. An orchestrator that works on a feature branch is covered by the default anyway. Opening the pull request at the end of a run is the orchestrator's integration decision, made in its own authorized session: a phase session cannot tell it is the last one, and the method has to work without any orchestrator.
- **Never force, never another branch, never a merge or pull request.** A pull request remains something the user or an orchestrator authorizes.
- **The refactor commit lands before the push.** One push carries the feature commit and, when there is one, the `refactor(scope):` commit, so the remote never holds the feature without its tidy.
- **A rejected push in the shared checkout is reported with the commits left local.** Rebasing in a checkout other sessions share can collide with their uncommitted work. A chat in a worktree keeps its existing fetch, rebase and retry when its landing is authorized.
- **No branch upstream:** the branch is pushed to `origin` under its own name with `-u`, so a new feature branch is published rather than the push failing. The pre-commit pull is skipped and the own-commits check uses `HEAD --not --remotes` for such a branch.
- **The refactor commit does not pull again.** The branch was brought current for the feature commit; pulling between the two commits would stop on a remote that moved and strand the tidy uncommitted. A moved remote surfaces as a rejected push instead, with both commits local.

**refactor-pass**

- **Called from the chain, it runs without asking**, after the feature commit and before any push, in the same chat that holds the evidence of whether the structure fought the change. Its decline bias, small-tidy gate and two-hats rule are unchanged; only who runs it and who commits changed.
- **It commits its own `refactor(scope):` commit when it changed anything**, never folded into the feature commit, so the two diffs are read apart.
- **A decline is a one-line verdict.** Now that it runs every time, a paragraph per session would be noise in every wrap-up.
- **Standalone, same default:** it commits its tidy and pushes it when the push lands on a feature branch, under the same precedence. It still refuses to run on uncommitted work; committing someone else's feature is not its job.
- **When the user said not to commit, it is recommended, not run.** It needs a committed baseline, so it waits for the user's commit.

**phase-chain**

- **The Codex orchestrator already committed and pushed under the user's chain request.** It now runs `refactor-pass` between its commit and its push, as the implement skills do, and still never makes it a gate on dispatching the next phase.

## Revisit when

- Refactor commits regularly need reverting. The refactor pass would then go back to a recommendation, or its gate would tighten.
- Users of the other skills report the same commit inconsistency. Extend the default to them one at a time, starting with `test-audit`, whose output is code like the implement chain's.
- A session pushes to a branch that turned out to be shared or to release to production. Record the case here; the integration-branch list would then need a concrete signal rather than names and "the repository's instructions".
- Held pushes pile up unreviewed in shared checkouts. The hold would then need a reminder, or the user may prefer pushing to `develop` by default.

## Revised 2026-10-18: the requirements skills commit too

Option 2's reason for leaving them out, that the user was about to review their documents, no longer holds: the reviews became recommended, not required, and an unattended run needs its work in history. The requirements skills now commit their documents by default and never push by default. See `review-technical-design-revises-in-place-decision-2026-10-18.md`.

## Revised 2026-10-18: the test audit commits too

As the Revisit list anticipated, `test-audit` now commits its tests, fixes and `test-audit.md` by default and pushes when the push lands on a feature branch, with no refactor pass. The new `delivery-audit` commits its completion phases like the requirements skills and never pushes by default. See `delivery-audit-and-prd-close-out-decision-2026-10-18.md`.

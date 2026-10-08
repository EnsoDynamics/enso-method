# Later PRDs superseding earlier criteria, and the conflict check (decision record, 2026-10-08)

Maintainer notes for the `Replaces:` / `Superseded by:` lines, the conflict check and the shipped-behavior rule. The format is owned by `prd-writing-standards` ("When Later Work Changes an Earlier Criterion"), the rules by `implementation-lifecycle` ("When Later Work Changes Earlier Requirements"), with steps in `autonomous-requirements-refinement`, `implementation-readiness-check`, `implement-from-requirements`, `implement-from-discovery`, `technical-design-writing-standards`, `review-technical-design`, `test-audit`, `deliverable-review`, `assumptions-document-feedback`, `phase-split` and `test-hardening`, and summaries in the README and `docs/how-the-enso-method-works.md`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session.

## The problem

The method said every change amends the PRD first, and that a change directory is "never a substitute for amending." Ad hoc fixes did amend in place. But a later PRD or change directory that changes behavior an earlier one defined had no rule. Read literally, the earlier PRD had to be rewritten to match, which nobody did or could keep doing. Meanwhile the build skills tell an agent to read a service's earliest PRD for context and to treat "docs right, code wrong" as the usual case, so an earlier criterion with nothing pointing forward would have an agent revert behavior a later PRD asked for. The same default would revert a deliberate change a teammate made without writing any requirements at all.

## Options considered

1. **Rewrite earlier PRDs to the current state** (OpenSpec's merge model). Rejected: the cost grows with every PRD, it erases what was true when each was built, and PRDs are scoped to deliveries, not to a description of the whole system.
2. **Layer PRDs with no links.** Rejected: the stale-criterion regression above.
3. **A separate index of current behavior.** Rejected: one more document to drift.
4. **Chosen:** the latest-built document that defines a behavior owns it; a `Replaces:` line on the new criterion and a `Superseded by:` line on the earlier one; a conflict check so the links don't depend on anyone's memory; and shipped behavior is not reverted to match a document without a decision.

## Decisions and why

**The pointers**

- **Each pointer goes to the next document, not the latest.** Changing a behavior already means finding its current owner, so marking that one criterion is a single edit. Pointing at the latest would mean rewriting every older pointer, for no gain in correctness: the chain already ends at the owner. The chain is the history, so no separate history is kept. Fan-out is a line naming both targets.
- **`Replaces:` is written with the PRD; `Superseded by:` when the replacing criterion is built,** in the same commit as its code. A PRD can change freely while drafted, and one never built, or built months later, never marks behavior superseded while the code still does it.
- **"Later" means built later.** Two PRDs can be written in one order and built in the other. A criterion superseded before it was built is skipped when its own PRD is built. A chain can fork when two unbuilt PRDs replace the same criterion; the second to build re-points its `Replaces:` to the end of the chain and treats it as a fresh conflict.
- **A fully superseded criterion is never edited and no longer owed:** builds, phase plans, test hardening, test audits and wrap-ups leave it out like a retired label. A partly superseded one still owns, and is amended for, the part in force. Pointers are not decision history, so conformance passes keep them.
- **Technical designs get the same lines, keyed by section heading,** because designs have no stable IDs. Weaker than a criterion label, and accepted.
- **A stakeholder ruling on an assumption whose criterion was since superseded is not folded** into the later criterion; the conflict goes to the user, because folding would silently reverse a later PRD.

**The conflict check**

- **It exists because the author can't be relied on.** No one holds every earlier PRD in their head. A subagent reads the criteria still in force across the repo's PRD roots, about 40k tokens in the largest real sets measured (23 and 42 PRDs, 2026-10-07), fewer as superseded criteria drop out. An intended change becomes a `Replaces:` line; an unintended one is a business question.
- **Refinement runs it first, in pass 1,** so findings resolve through the run's question loop, with a re-check at completion for criteria changed after pass 1. Running it only at completion would surface conflicts after that loop had ended. The result goes in the completion commit as a `Conflict check:` line, because the state file is deleted.
- **The build runs it again, narrowed.** Refinement is optional, and changes and ad hoc fixes usually skip it. With a recorded check (refinement's, a standalone readiness check's, or an earlier phase's), the build checks criteria changed since, and its criteria against PRD files that changed since; without one, it checks the whole PRD once and records it, so a split PRD doesn't pay per phase. It runs after sizing and after the credential preflight.
- **A failed check never stops a build.** Retry, run it in the main chat, then proceed and record `Conflict check skipped:`. Stopping would leave an unattended session idle over a risk no worse than before the check existed.
- **A test tripwire catches what the check misses.** An existing test's expectation changes only when something accounts for it: a criterion or design decision the session builds, amends or enforces, or the defect the fix serves. "Accounts for" rather than "the test's criterion is replaced", because re-pinned tests, tests with no criterion behind them and tests pinning a bug being fixed would otherwise all trip it.

**Shipped behavior, and repos that don't use the method consistently**

- **Existing code that differs from a criterion is an observation unless the session's work needs that code changed.** The Materiality Gate's "contradicts an explicit requirement" now says it means the work being produced. Deliverable-review and test-audit say so explicitly, since both had "spec wins" defaults.
- **A plain bug** (a malfunction nobody would choose: crash, error, corrupted output) is just fixed, with no check. Running the check on every bug fix would add a repo-wide read to most `implement-from-discovery` sessions.
- **A consistent contradiction** (a coherent alternative a person could have chosen) asks the conflict check whether a later PRD owns it. If none does, the shipped behavior stands until a decision says otherwise: reverting it is a business question whose proposed answer is to keep it, and the user's direct request, or the ticket the session serves, is the decision that wins.
- **Git history moves the confidence, never the default.** Keying on "was there a later commit" was tried and rejected: squash merges, reformat commits, imported code and a developer who shipped the deviation at the original build all defeat it.
- **Only the finding that decides what the session does gets a pointer pair.** Asking both directions on every fix turned bug fixes into pointer backfill.

## Known gaps

- Repos whose PRDs predate the convention have no pointers. An agent reading an old PRD only for context can still be misled. A one-time backfill (the conflict check run across every PRD) would close it; it is not required.
- The check reads criteria, not designs. A design-level conflict with no criterion behind it is caught only by `review-technical-design`, which is optional.
- The check is an agent's judgment. It reliably catches direct conflicts and can miss a new behavior that changes an old one's outcome indirectly; the tripwire catches some of those through tests.

## Revisit when

- A regression traces to a missed conflict, or a deliberate change was reverted anyway. Record the case here; the check's instructions and the plain-bug line are the first things to sharpen.
- Tests carry criterion labels. The tripwire could then be a script.
- A repo's criteria outgrow one subagent's read. The shortlist-by-title step would need to become the default.

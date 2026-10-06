---
name: phase-chain
description: Carry an authorized implementation plan through sequential fresh Codex tasks, one phase per task, with reviewed commits, pushes, and actual successor creation. Use when the user asks to keep implementing all planned phases without babysitting each handoff; not for a single-phase request or a prompt-only handoff.
---

# Phase Chain

**Codex only.** If you are not running in Codex with task creation and task inspection
tools, stop here: hand the next phase to a fresh chat with `continuation-prompt` instead.

Run the user's approved implementation scope to completion, one phase or subphase
per fresh Codex task. Adopt it at kickoff or during an existing chain; every
successor invokes this skill again. This is a Codex-only orchestration layer
requiring task creation and task inspection tools. Loading the skill alone does
not authorize creating tasks: the
user must request the sequential task chain, as in the kickoff example below.
A request to run that chain authorizes the default delivery cadence for the stated
scope, including its scoped phase commits, pushes, and successor creation. It does
not authorize integration merges, production deployments, destructive actions, or
other excluded actions unless the user says so. Merely loading this skill because
its rules are relevant does not activate or authorize a chain.

`implement-from-requirements` owns implementation, context loading, sizing,
validation, `deliverable-review`, and `test-hardening`. `phase-split` owns changes
to phase boundaries. `pre-commit-validation` owns staging and commit hygiene.
`continuation-prompt` owns successor naming, prompt composition, and moving repo
facts into governing documents. This skill owns the authorized delivery tail and
the transfer of responsibility to exactly one successor. Do not duplicate or skip
those skills' procedures.

## Default delivery cadence

Unless the user specifies otherwise, each phase ends with its required validation,
reviews, scoped commit and push to the established branch, then a handoff to the
next phase in the same checkout. Defer merging the accumulated work into `develop`,
`main`, or another integration branch until the end of the entire authorized
sequence, not the end of each phase or subphase. Do not add a per-phase PR, merge,
deployment, or broad-CI wait merely to start a fresh task.

Preserve a user-approved delivery contract that explicitly requires a different
cadence; do not infer one from an older assistant-written handoff template. If an
intermediate merge becomes essential to a concrete dependency or validation need,
explain why and evaluate it when encountered. Perform it only within the existing
authorization; obtain direction if it needs new authority. Routine task boundaries
and pending advisory CI are not such dependencies.

This default changes timing, not quality gates or branch strategy: do not create
a feature branch for work already on a shared branch. Keep required artifact
consistency checks at each handoff. Record the final integration target, required
CI and approval holds in the chain context; finish authorized integration at the
end, without treating this skill as permission to merge or deploy to production.

## Join a chain already in progress

A request such as “when you start the next chat, use phase-chain” adopts this
workflow for the existing authorized scope. It does not restart the plan or
authorize every remaining phase of a larger PRD. Recover the current unit, its
actual implementation/delivery state, the next unit, and the last authorized unit
from governing docs, git, and source tasks. Preserve the original authorization
source and this adoption message in the chain context; no original phase-chain
kickoff is required.

The current task finishes its already-owned phase under the existing implementation
workflow, then uses this skill's delivery and dispatch steps to hand off to the
next task. Continue from the first unfinished action: do not rerun completed
implementation, repeat satisfied gates without cause, or recommit a delivery that
already landed. Verify any existing successor before dispatching. A newly adopting
successor likewise recovers the actual chain state instead of returning to phase
one. Ask only if material scope or ownership remains unresolved after inspection.

## Establish the chain once; verify it in every task

Read live global and repository instructions, the original scope request, and any
midchain adoption request. In a successor, read the predecessor handoff and use
`read_thread` to recover original
user messages when evidence is missing or ambiguous. A predecessor's summary is
a pointer to authorization, not a replacement for its source.

Keep the following compact **chain context** in every successor prompt. It is
session truth, not a second requirements document:

- **Identity and scope:** original scope task ID/reference (the chain identity),
  adoption task ID/reference when different, current and next unit, last
  authorized unit, governing PRD/design/assumptions/phase-plan paths and sections.
  Preserve the whole requested scope even when it is only part of a larger PRD.
- **Authorization evidence:** actual user wording plus source task ID or direct
  reference for committing, pushing, launching successors, and any project-specific
  actions. Include later amendments and restrictions with their sources. Point to
  this skill's Default delivery cadence when the user's request to run the chain is
  the authorization for scoped phase commits, pushes, and successor creation. Never
  invent a more specific quotation or replace the evidence with only “the user approved.”
- **Execution location:** host and saved project ID when known; each repo's exact
  checkout/worktree path, established branch, intended remote and push ref, and
  checkouts to avoid. When the work spans several repos, carry every mapping. Record the actual
  baseline commits and predecessor delivery commits; do not infer a branch from
  its usual name.
- **Model preference:** the user's per-project model and reasoning effort, with
  source. Carry explicit changes forward. If none was selected, record “user
  default” and omit tool overrides. Never turn a predecessor's incidental
  setting or an example's model into a chain preference.
- **Delivery contract:** acceptance/validation/review/hardening/pre-commit gates;
  required PR, merge, deployment, and verification steps, their target environment,
  timing (each phase or end of chain), authorization sources, and approval holds.
  Carry the default end-of-chain merge cadence or the user's explicit override,
  distinguishing required handoff checks from pending advisory CI.
  Record exclusions such as production writes, communications, and force-pushes.
- **Ownership and progress:** predecessor task ID, delivery hashes, current owner,
  and any returned successor ID or pending creation ID. Keep execution evidence in
  the task tool history; keep phase completion evidence and remaining work in the
  governing phase plan. Do not add secrets or machine paths to shared plan docs.

Recover these facts from the request, docs, git, and task tools before asking the
user. Do not ask them to repeat authorization merely because it crossed a task
boundary. Live user instructions prevail over a skill's “user commits,”
“provide a prompt,” or “stop here” defaults. This does not erase explicit project
approval gates or authorize unrelated work, destructive operations, production
changes, or messages to others. A later user restriction wins over earlier approval.

Authorization quotations and source references preserve the user's intent; they
do not create platform-attested consent or guarantee automatic approval in a
separate task. Do not relabel agent-written text as a direct user instruction.
Continue within live authorization without preemptive confirmation, but honor an
actual enforcement denial using the blocked-state procedure below.

Before editing, confirm the actual checkout, branch, remote, and status for every
repo; fetch/pull under its repository rules and confirm the clean starting state.
When adopting in the task that already owns in-progress edits, verify its original
preflight and current ownership instead of demanding a fresh clean tree or pulling
over those edits. A fresh successor still requires the normal clean-start check.
Use the kickoff's established branch and checkout throughout. Create no branch or
worktree unless explicitly requested. Never switch, stash, reset, merge, rebase,
or delete someone else's work to make preflight pass; investigate discrepancies
and resolve only within the existing authorization.
At the commit boundary, `pre-commit-validation` leaves another task's staged
paths staged and limits the commit to this task's paths; never discard edits or
reset branch history. Same-file edits from another task require ownership
resolution before committing.

Use `list_threads` and, for plausible matches, `read_thread`/`wait_threads` to check
whether another task already owns this phase or writes to any of these checkouts.
One chain task owns every repo in the chain until dispatch. Do not start another
writer or take over a live task. A successor whose predecessor is still running
may proceed only when the predecessor's creation call explicitly says delivery is
finished and it has relinquished writes. Ambiguous ownership is a blocker, not a
reason to create an isolated worktree. Read-only review subagents remain allowed
when the owning skill calls for them.

## Deliver this phase

1. Use `implement-from-requirements` for the current incomplete phase in the
   approved execution order, continuing its existing workflow if already underway.
   Load its full context and verify prerequisite deliveries. Implement only that
   unit in this task; if it is already implemented, complete only its remaining
   delivery steps before dispatching the next unit.
2. Complete its acceptance criteria and required validation, deliverable review,
   test hardening, and all material fixes. For documentation-only deliveries use
   document review and relevant document/behavior checks; do not invent code tests.
   Record the actual evidence, not a bare “verified.” A failed required check is
   not a completed delivery merely because its failure was documented.
3. If another authorized unit remains, run `continuation-prompt` before staging
   so its governing-document updates are included in the delivery. Add the chain
   context above and an instruction to use both `phase-chain` and
   `implement-from-requirements`. The prompt must retain exact authorization
   wording even when that makes it longer than the usual one-screen target.
4. Recheck branch and ownership, then run `pre-commit-validation` for only this
   task's files. Announce the repo and full proposed message, then commit and push
   under the established authorization without a new confirmation round. Use
   the project's commit convention (`type(scope): concrete change` when none is
   set, per `pre-commit-validation` Step 7); name the PRD/work and qualified phase/subphase
   in the subject or detailed body. A bare “Phase 2” is insufficient. Recommend
   `refactor-pass` as optional after the feature commit; do not run it automatically
   or make it a prerequisite for the next phase.
5. Verify the scoped commit exists on the intended remote branch. For multiple
   repos, verify every required push. Complete all authorized delivery steps due
   at this boundary under the delivery cadence above. When CI or deployment is an
   actual prerequisite for this handoff, follow `wall-clock-awareness`: stay in
   the turn with bounded waits until there is an outcome. A pending required job
   or failed push blocks dispatch; pending advisory CI does not. Carry advisory
   run references and the obligation to assess their results to the successor,
   without relabeling known material failures or required checks as advisory.
   Do not force-push, silently change targets, or bypass deployment approval gates
   to close the phase.

If work needs re-splitting, delegate to `phase-split`; it decides and declares
the cut without a confirmation gate, and writes one document per child phase
under its positional id scheme. Keep the re-cut within existing scope. A
completed, reviewed planning delivery may be committed/pushed and handed to its
first implementation successor; describe it as planning complete, never as the
original implementation phase complete. Incomplete implementation cannot be
relabeled as a planning delivery to evade quality gates.

## Dispatch exactly one successor

Dispatch only after a completed delivery and its required tail, and only if there
is another authorized, unblocked unit. Do not queue all future phases.

1. Finalize the `continuation-prompt` with actual delivery hashes and the chain
   context. Give it a stable identity in prose: kickoff task, next unit, and
   predecessor delivery hashes. Say that the predecessor has finished delivery
   and relinquishes repository writes as soon as creation is accepted. The next
   task must verify that record before editing.
2. Before calling `create_thread`, inspect this task's previous creation results
   and matching tasks. If this successor already exists or creation is pending,
   inspect that result instead of dispatching again. Use its returned task ID and
   status, not title alone. If a resumed predecessor discovers that its successor
   has progressed, follow the existing chain; do not rerun the delivered phase.
3. Call `list_projects` and resolve the saved project on the established host.
   Explicitly request its existing **local** environment in `create_thread` so a
   Git project's default does not create a new worktree. Put every exact working
   path in the prompt, including existing user-authorized worktrees. A saved
   organization-level project may host the task when the prompt directs it to the
   established subrepo paths. If the tool cannot access the established checkout
   on that host, report the limitation; do not silently substitute a new checkout.
   Follow the live tool schema; pass model/reasoning overrides only from the user's
   recorded preference. If unavailable, surface that limitation rather than
   silently substituting a model.
4. Actually call `create_thread` with the finished prompt, title, resolved project,
   local environment, and authorized model settings. A printed prompt is not a
   launched task. After acceptance, make no further repository edits, commits,
   or pushes in the predecessor; the successor now owns them.
5. Preserve the returned `threadId` and `hostId`, or `clientThreadId` for pending
   setup, in the task's tool record and response. Never pass a pending client ID
   to tools requiring a real task ID. Resolve pending setup using the available
   task listing/status tools; do not create a replacement while it is unresolved.
   Use a bounded `wait_threads` call once a real ID is available to check startup.
   Do not wait for the entire chain to finish in its predecessors, and do not
   restart or interrupt a successor that is running or waiting for user input.
6. If creation times out or the response is ambiguous, inspect task history and
   matching tasks before any retry. Retry only after confirmed non-creation.
   An unresolved result is a dispatch blocker; never risk duplicate writers.
   On an explicit rejection, preserve the completed commit/push state, report
   the exact rejected action and reason, and resolve through permitted checks
   or required user action. Do not route around the denial using another tool.

Emit the app's created-task directive with the returned ID in the final response
(`::created-thread{threadId="..."}` or the `clientThreadId` variant). Describe the
phase as delivered and the successor as created/pending/running according to the
observed status. Do not claim the entire chain is done at this boundary.

## Stop truthfully

- **Chain complete:** verify every unit within the kickoff scope is complete and
  all required end-of-chain PR/merge/deployment/verification steps are finished.
  Check governing docs for remaining acceptance criteria and pending human actions.
  Report completion with delivery evidence; create no successor. Do not claim the
  larger PRD complete when the user authorized only a subset.
- **Blocked:** keep working on permitted, useful checks/fixes first. Stop when a
  material issue cannot be resolved within scope, a required approval is absent,
  an explicit stop-to-replan condition fires, ownership is ambiguous, or an
  enforcement/tool limitation prevents progress. Record the blocked unit and
  evidence in its governing doc where permitted; give the user the concrete action
  needed. Do not dispatch a next-phase task past this blocker.
- **Voluntary pause versus enforcement:** “the previous task chose to ask again”
  is not a tool denial. Recover live authorization and continue authorized work.
  A real automatic-review or tool denial must be named with its action and stated
  reason; source authorization does not permit bypassing it.

This skill is a task-to-task protocol, not a scheduler. Do not promise a wakeup
after an interrupted or failed task unless a real mechanism exists. When the user
resumes a stopped chain, verify its latest owner and delivery/dispatch records and
continue from the first unfinished authorized action without duplicating work.

## Invocation examples

> Use $phase-chain to implement all phases of the order-notifications PRD at
> `docs/prds/order-notifications/`, one phase per fresh task. After each phase's
> required validation and reviews, commit and push to the established branch,
> then launch the next task until the requested scope is complete. Preserve this
> project's checkout and model preference; no production deployment.

For a chain already underway:

> Use $phase-chain for the remaining authorized phases of this existing chain.
> Finish this phase and its required checks, commit and push if still outstanding,
> then launch the next chat with $phase-chain. Keep the established scope,
> checkout, branch, and model preference.

---
name: engineering-principles
description: The engineering principles the Enso Method depends on — no silent fallbacks, the testing evidence standard (every acceptance criterion proved at the boundary it is about), never hacking a failing test green, the test tripwire, questioning the first correct fix, production data (dev and sandbox first, read-only and only where allowed), working beside other sessions (git safety in a shared clone, session markers, when to use a worktree, one branch for a split PRD), bounded and visible scheduled jobs, and the judgment calls for ambiguous moments (finish what you started, don't dismiss failures, source of truth, scope follows intent, investigate before removing). Also defines how a project plugs in its own house engineering standards. Load for any code change, test work, error-handling decision, or ambiguity mid-implementation.
---

# Engineering Principles

The principles the methodology itself depends on. They hold in every stack and every
house. Stack, style, tooling and structure opinions are not here — those belong to the
project's house engineering standards (next section).

## House Engineering Standards

A project names its own standards in its `AGENTS.md` (or `CLAUDE.md` for Claude Code) with
one or more lines of the form:

```
Engineering standards: <skill name or file path>
```

A person working across several organizations may instead map directories to standards
in their global instructions file; a line in the repo's own `AGENTS.md` takes precedence
over that map. When the line is present, load everything it names alongside this skill. On stack, style,
tooling, structure, naming, configuration and deployment, the house standards win. The
principles in this skill are not overridable — a house standard that conflicts with one
is a gap to raise, not a license. When no line is present, follow this skill and the
conventions already visible in the codebase.

---

## Error Handling: No Silent Fallbacks

**Fail loudly when the conditions the code expects are not met.** Default values and
fallback logic are one of the most common ways bugs hide in production: the code appears
to work while the underlying situation is broken, and the problem surfaces later, harder
to trace, with a larger blast radius. A fast, obvious failure beats a slow, hidden one.

```python
# Bad: silently downgrades when the lookup fails
return customer_service.lookup_tier(customer_id) or "standard"

# Good: surface the failure
tier = customer_service.lookup_tier(customer_id)
if tier is None:
    raise ValueError(f"No tier found for customer {customer_id}")
return tier
```

Any time you are about to write `value or default`, a conditional fallback, or an
exception handler that swallows an error and substitutes something, stop and ask whether
you are hiding a problem that should surface. The most dangerous case is configuration
that silently defaults to an environment: code that runs against sandbox when production
was intended (or the reverse) gives no sign anything is wrong. Require the value
explicitly and fail when it is missing.

**AI-generated code is especially prone to this.** Assistants drift toward defensive code
that "just works" under any conditions — pleasant to demo, dangerous in production. A
missing required field is a reason to raise, not to substitute an empty string. Optimize
for code that is correct, observable and trustworthy, not code that runs on the first try.

**Catching per record is not a fallback.** A batch that runs for hours should not die on
one bad record, so catch, log and count each failure, keep going, and report exactly what
failed and why at the end. Nobody is pretending the failure didn't happen.

**When a fallback is acceptable:** truly optional cosmetic values (a display label, a log
prefix); a feature flag whose default state is intentional and documented; a cache whose
fallback is the source of truth. If you cannot say why the fallback value is safe and who
decided it is the right default, it should not be a fallback.

**Fail before you start.** Validate preconditions — required configuration present,
credentials valid (one lightweight call), dependencies reachable, inputs readable, outputs
writable — at startup, in one findable function, before the first real write. A missing
key discovered three hours into a run is far worse than one discovered in five seconds.
Bad data is a runtime failure handled per record; configuration and infrastructure
problems should never survive past startup.

---

## Do Not Stop at the First Correct Fix

A fix can be locally correct and still expose a poor system shape. Before adding a
transaction, lock, queue, coordination record, retry protocol, special mode or another
piece of state machinery, zoom out and ask:

- What invariant requires this machinery?
- Why can two actors reach conflicting states in the first place?
- Does the system already have an ownership or serialization boundary that should prevent
  the conflict?
- Is the added complexity proportionate to the workload and the actual risk?
- Would a simpler state model or responsibility boundary remove the need?

Treat surprising machinery as a smell to investigate, not an automatic rejection. Low
volume does not make a race impossible, and the new mechanism may still be the safest fix
for the current design — but proving that a mechanism closes the immediate race does not
prove the surrounding design is right.

Keep this check separate from scope expansion. If a simpler design is clearly within
scope, prefer it. If redesign would be disproportionate or was not requested, implement
the narrow safe fix and record the design fact in the Technical Design
(`implementation-lifecycle`, "The Disposition Rule") without starting an unsolicited rewrite.

**Example:** a low-throughput worker already prevents two processes from working the same
ticket, but separate control records create another same-ticket race. A database
transaction can correctly close it. Needing a second coordination protocol is still the
signal to question the state model before treating the transaction as the whole answer.

---

## Testing: The Evidence Standard

### Every acceptance criterion needs evidence at the boundary it is about

- **Mocks are fine for isolated logic** — deterministic rules, transformations,
  calculations, parsing and edge cases on our side of a boundary.
- **A mock is never the only evidence that an integration or data contract works.** It
  proves only that the code handles the response the test author wrote; the real system
  may return a different shape entirely.
- **Boundary-crossing behavior is proved against something real** — a sandbox, a local
  container, a recorded and verified contract, or a staging run. The preferred default is
  real sandbox/dev resources.
- **When no real counterpart exists, the evidence states the gap explicitly** rather than
  letting a mock hide it. Name the boundary that was not proved and why.
- **Evidence never comes from writing to production.** Test writes go to non-production
  targets, no exceptions. Where a service has no non-production counterpart and the project
  allows it ("Production Data" below), strictly read-only production access (GETs, SELECTs, a
  production-supported dry-run) can prove the read side; the write side is proved at the unit level and reported as a gap.

Narrow mocks are legitimate beside real evidence: for destructive operations, rate-limited
or costly APIs, and failure conditions you cannot reliably trigger (a timeout, a 500). Keep
the mock at the smallest boundary that creates the condition, and say in the test what it
does not prove.

### Prove risks, not test counts

Choose the smallest set of tests that gives credible evidence the change works. Pick the
level from what can actually fail: unit tests for isolated logic; integration tests for
API contracts, authentication, serialization, database behavior, queues, storage and
configuration; end-to-end or workflow checks when confidence depends on several real
components or a user-visible path. One well-chosen integration test may prove several
criteria; one high-risk criterion may need tests at several levels. Trivial accessors and
framework wiring covered upstream need no ceremonial tests. Before adding a test, be able
to name the failure it would catch and why no existing test already catches it.

### A failing test is information — never hack it green

A failing test means the code is wrong, the test is wrong, or the understanding of the
requirement is wrong. Work out which **before** changing anything. Never weaken an
assertion, skip or delete a test, broaden an exception handler, hardcode an expected value
or special-case a code path to get to green — those moves hide the problem and ship it. If
investigation shows the test itself is wrong, fixing it is a legitimate outcome, reached by
understanding the failure and stated explicitly when reporting the work.

### The test tripwire

The conflict check (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion") finds the earlier criteria new work changes; this catches what it missed. Before changing the expected result of an existing test the session did not write, or deleting one, check that something accounts for the change: a criterion or Technical Design decision the session builds, amends or enforces requires the new expectation, or, where no criterion speaks to the behavior, the defect the fix serves (its ticket, incident or report) does. A test that a criterion's own change forces to change is accounted for. If nothing accounts for it, the session is changing behavior nobody declared: resolve it by the Doc Divergence rule (`implement-from-requirements`), which ends either in a criterion that accounts for it (an amendment, or a `Replaces:` line and its back-pointer) or in putting the behavior back. Renaming or restructuring a test without changing what it expects does not trip it.

### Test data

Unit and component tests never depend on data that lives only on one developer's machine:
fixtures are committed and referenced by repo-relative paths. Integration tests use
deliberately created or explicitly identified test records in non-production systems,
tagged so they can be found and cleaned up — never an unexplained record that happens to
exist.

### Which tests to run

While iterating, run only the tests that cover the code you are changing. The full suite
is the gate before commit.

When the full run fails, the next run is the failed tests, not the suite. Run them alone,
by file or by name, and read the runner's first lines to see that the filter took: a
command that starts the whole suite anyway is stopped and its filter fixed. Fix what this
session's work broke and repeat on those tests until they pass; a failure that was there
before the session's work is named in the wrap-up and left. A test that passes alone with
nothing changed still failed for a reason: read its failure for the cause (a deadline
missed on a busy machine, state another test left behind) and name it in the wrap-up,
fixing it when a test this session wrote or changed left that state. Then:

- **The full run ran every test, and nothing has changed since but the failed tests
  themselves:** the gate is met. Every other test passed, and nothing it exercises has
  changed. The wrap-up gives the full run's command and time, and the tests run again
  after it.
- **Anything else changed** (implementation code, a helper or fixture other tests share),
  **or the run stopped before every test ran:** run the tests that cover the change, then
  the full suite again, on the finished code.

Tests, builds and CI are run again by every later session, and the person waiting pays for
every run. An agent does not feel that time, so read it from what the runner prints. When
you add or change a test, a build step or a CI job, run it alone, read how long it took,
and make it cheaper when it is slower than most tests around it without a reason you can
name. When you set up a suite or a pipeline, set it up to stay fast.
`wall-clock-awareness` has both.

---

## Production Data

Building new software rarely needs production data: work against dev and sandbox
environments. Read production only when a question genuinely can't be answered any other
way — a defect that only reproduces there, or a data characteristic only production holds —
and then read-only, and only where the project allows it. Regulated data (health, payment,
personal records) may rule it out entirely; the house engineering standards or the user
say so. **Never write to production** to investigate, test or prove anything.

---

## Git Safety When Several Sessions Share One Clone

Several AI sessions often work the same checkout at once. Two git mechanics bite in that
setup regardless of anyone's discipline.

**The index is shared — check it immediately before you commit.** There is one index per
working tree. When another session runs `git add`, its files land in your index, and
`git commit` with no paths takes everything staged. Checking `git status` when you stage is
not enough, because the other session may stage after you. Immediately before committing,
run `git diff --cached --name-only`; leave anything you did not stage alone and commit (or
hand the user) only your paths — `git commit -- <paths>` (`pre-commit-validation`). Never
`git add .` or `git add -A`. `git commit -- <paths>`
narrows which files land but not which edits within a file — if two sessions edited the
same file, committing it takes both sets of edits.

**`git checkout -- <file>` / `git restore <file>` discard every uncommitted change in that
file**, not just your last edit. The expensive failure: many edits to one file over a long
session, one goes wrong, the file is reverted to undo it, and everything else goes too.

- To undo one bad edit, undo that edit — re-apply the correct content.
- Stage completed work as it validates, so an accidental revert costs only the unstaged
  delta.
- Prefer a targeted replacement over a broad find-and-replace in a file carrying a lot of
  uncommitted work.

---

## Session Markers: Leave a Note Where You Work

Several sessions — Claude Code, Codex, anything else — often run at once in the same checkout or in sibling worktrees. Each leaves a small log in every repo it edits, so a person or another session that finds modified code, or wants to know what is in flight, can see who is working there and on what. It is a courtesy note that takes seconds; it never competes with the work for attention. **It is not a lock:** another session's log never stops or pauses yours. Before your first edit, though, a live log decides where you work (Parallel Sessions, below).

**Write.** Before your first edit in a repo, create `.agent-sessions/<date>-<tool>-<slug>.log` at the root of its shared checkout, even when you work in a worktree (Parallel Sessions, below) — date from `date +%Y-%m-%d-%H%M`, tool as a lowercase slug (`claude-code`, `codex`), slug the chat title or lineage in a few words, e.g. `2026-09-23-1412-claude-code-email-digest.log`. A session editing several repos keeps a log in each. Add `.agent-sessions/` to the repo's `.gitignore` if it isn't listed; that line rides in your commit, so put it in your expected changeset. A header, then one line per event, timestamped with `date +%Y-%m-%dT%H:%M%z`:

```
tool:       Claude Code
session:    claude-7 [a1b2c3]
chat title: Email digest scheduler
branch:     develop
serves:     Phase 2a — Email digest scheduler, of User Notifications

2026-09-23T14:12-0400  START    implement-from-requirements
2026-09-23T15:40-0400  WAITING  CI on PR #541
2026-09-23T15:58-0400  COMMIT   e4f5a6b pushed
2026-09-23T16:06-0400  DONE     Successful implementation — Phase 2a closed
```

`serves:` is the lineage (`continuation-prompt`, "The lineage gate"), in its full-title form. `session:` is whatever the tool exposes for addressing this chat — for Claude Code, the name and bracketed ref `ListAgents` reports, which lets Claude peers message it (the ref is the stable handle; the name changes when the chat is renamed); omit any field you don't have. **START and DONE are the only required lines.** DONE is written at any terminal state and names it (`implementation-lifecycle`, "Terminal States"), so a reader can tell a finish from `DONE  Blocked — vendor API credentials expired`. Beyond those, append a line only at a moment you are already announcing to the user and a peer would care about: SCOPE (a split changed what you are building), WAITING (on CI or on the user), COMMIT, HANDOFF (the successor chat's name). A `test-audit` red check also writes REDCHECK and RESTORED around the moment it breaks code on purpose: a REDCHECK with no RESTORED after it means that file was left broken, so restore it from the copy the line names. Append only, and only to your own log; never rewrite. The rule lasts the whole chat, not just the skill's run: whenever you are about to edit a repo with no log of your own — a follow-up request that moves to another repo, work resumed after your DONE, or a chat already under way when it loads this skill — start one first (a new START line, or a new file if yours was pruned).

**Prune.** When creating your log, delete logs in the same folder whose last line is a DONE more than 7 days old, or that have had no write for 14 days. Never touch anything newer — other sessions may still be working in that checkout.

**Read.** Logs are hints, not truth. A missing DONE may mean the session is still running or that it ended without writing one; a DONE may predate later work. Weigh a log against its last-write time, the branch's uncommitted changes and merge state, and — for Claude peers — `ListAgents` busy/idle. To survey everything in flight, find each repo's worktrees with `git worktree list` and read `.agent-sessions/*` in every checkout it lists; one session's logs in different repos share its `session:` line. Message a peer only when the logs and git can't answer the question. When a session arrives in your checkout after you started, its uncommitted changes sit beside yours: leave them alone and stage only the files you changed.

---

## Parallel Sessions: Where to Work

**Default: the shared checkout, on the shared branch.** The shared checkout is the repo's normal working copy, the directory the user opens in the editor; `<org directory>` below is the folder that holds it and any sibling repos (`<org directory>/<repo>`). The shared branch is the integration branch sessions commit to directly (often `develop` or `main`). Most work runs one chat at a time, and a chat working there needs no worktree, no clone and no cleanup.

**Work in a worktree instead only when one of these holds**, checked before the chat's first edit:

1. The prompt that started the chat says `Parallel: yes`.
2. Another agent session is live in a repo this chat will edit. That means an `.agent-sessions/` log in the shared checkout (Session Markers, above) with a START line, no DONE line, and a last line written within the past 12 hours. An older log without a DONE is an abandoned session, not a live one.
3. The user's instructions file requires a worktree for this kind of work.
4. The chat builds or audits part of a PRD split into phases, or changes the requirements documents of a PRD whose branch has not yet merged into the shared branch. It uses that PRD's branch and worktree, and "One Branch for a Split PRD" below replaces the naming, landing and cleanup steps here.

When none holds, stay in the shared checkout, even if parallel work seems likely and even if the checkout has uncommitted changes you did not make (leave those alone and stage only your own files). A chat that isolates by default leaves directories behind for the user to find and delete. A chat that starts a few minutes after this one sees this chat's log and isolates itself, so this chat does not have to anticipate it. When any signal holds, every repo the chat will edit goes into the worktree folder, not only the repo that tripped it, so sibling repos stay siblings.

**Never a clone** unless the user asks for one. A worktree does everything a clone would for this purpose, shares the repository's history and fetches, and `git worktree list` finds it again.

**Worktree mechanics.** The chat does all of this itself. Editor extensions do not create or clean up worktrees, so nothing else will.

- **Name:** a slug of the chat name: lowercase, spaces and slashes as hyphens, e.g. `phase-2a-email-digest`. A chat with no name uses its session log's slug. The slug names both the folder and the branch.
- **Where:** `<org directory>/.worktrees/<slug>/<repo>`, one folder per chat, with every repo it edits under it. Create each with `git -C <shared checkout> fetch origin`, then `git -C <shared checkout> worktree add --track -b wt/<slug> <org directory>/.worktrees/<slug>/<repo> origin/<shared branch>`. The `wt/` branch exists only because git refuses to check out the shared branch twice. It is never pushed as a branch.
- **Session log:** keep writing it in the shared checkout's `.agent-sessions/`, not in the worktree, so signal 2 sees this chat, and put the worktree path on the START line.
- **Run the code under test from the worktree.** A shared virtual environment or dependency install usually imports the shared checkout's code, not the worktree's. Point the interpreter at the worktree's sources (for Python, `PYTHONPATH=<worktree>/src`), or tests silently test the wrong tree.
- **Land each finished piece on the shared branch when pushing to it is authorized** — by the user in this chat or the starting prompt, their instructions file, or an orchestrator's prompt. Landing publishes to an integration branch, so the implement chain's default holds it (`pre-commit-validation`, "Who Commits"): commit in the worktree, then say in one line that it is ready to land.
  1. Fetch, rebase onto `origin/<shared branch>`, and re-run the tests the rebase could affect. Regenerate generated files after the rebase rather than merging them by hand.
  2. Push the result as the shared branch: `git push origin HEAD:<shared branch>`, a fast-forward.
  3. If the push is rejected because another chat pushed first, repeat from step 1. Never force a push to the shared branch.
  4. Fast-forward the shared checkout so the editor shows the work: `git -C <shared checkout> merge --ff-only origin/<shared branch>`. Always attempt it; it succeeds beside another session's uncommitted changes unless they touch the same files. If git refuses, say so in the wrap-up.

  When the work is not landed — the push is held for the user's word, the user said not to commit or push, the session ended Blocked, or a skill whose default doesn't push (a requirements skill, or one that presents its commit) has no authorization to — stage or commit in the worktree accordingly, present the commit message as usual, and leave the worktree in place with its path in the wrap-up. When the user later says push, land it (steps 1–4 above) and clean up.
- **Clean up at wrap-up**, once `git log origin/<shared branch>..HEAD` is empty and `git status` is clean. Run the cleanup from the shared checkout, not from inside the worktree: `git -C <shared checkout> worktree remove <path>`, then `git -C <shared checkout> branch -d wt/<slug>`, then delete the chat's empty folder under `.worktrees/`. `-d` refuses to delete work that has not landed; if it refuses, stop and report, and never force it. The wrap-up says whether the worktree was removed. A worktree that outlives its chat shows up in `git worktree list` and in a log with no DONE.

**Parallel work still needs owners.** Worktrees stop two chats writing the same file. They do not stop two chats changing related behaviour that merges cleanly and then breaks. When one chat hands out several prompts, each prompt names the area its chat owns: files, modules, registry blocks. A chat that needs a change outside its area stops and says so.

---

## One Branch for a Split PRD

**A PRD split into phases is built on one feature branch and reaches the shared branch once.** The first chat that needs the branch creates it in every repository the PRD changes: `git -C <shared checkout> fetch origin`, then `git -C <shared checkout> worktree add --no-track -b prd/<PRD directory name> <org directory>/.worktrees/prd-<PRD directory name>/<repo> <base>`, then `git push -u origin prd/<PRD directory name>` from the worktree. Every later chat on the PRD, phases and audits alike, works there; on a machine with no such worktree, it adds one from `origin/prd/<PRD directory name>`.

- **The base is `origin/<shared branch>`.** When commits this PRD needs are on the local shared branch and not on origin, the base is `<shared branch>`.
- **The user's branching instructions, or an orchestrator that assigns its own branch, take precedence over this section.**
- **Each chat commits here and follows its skill's default push** (`pre-commit-validation`, "Who Commits"). It leaves the shared branch alone and opens no pull request.
- **A chat that changes this PRD's requirements documents while this branch is unmerged commits them here,** whichever skill it is running, so the audits read the current criteria.
- **At the start of each phase, and before the closing pull request, bring it current:** `git fetch origin`, then merge `origin/<shared branch>` into it. Never rebase it once pushed, and never force a push.
- **Only an early merge the technical design's Delivery section names goes to a shared branch mid-build,** from the phase whose `**Early merge:**` line carries it, with permission recorded in that section or given by the user or an orchestrator. The phase opens a pull request into the line's target, merges it once its checks pass, and the PRD's branch carries on. With no permission, the phase ends Blocked and names the permission it needs.
- **Two phases running at once** each take a `wt/<slug>` worktree cut from this branch and land on it by the steps in "Parallel Sessions: Where to Work". Landing here needs no separate authorization, because this branch is not an integration branch.
- **The close is one pull request per repository,** opened by the test audit that closes the PRD, from this branch into the shared branch, and checked for conflicts once open. Merging waits for the user or an orchestrator they authorized. Until it merges the PRD is not delivered, so the wrap-up names the merge and the technical design's Delivery "After the build" items as the user's actions, and gives the command that removes the worktree afterward.

---

## Scheduled Jobs: Bounded Calls and Visible Failures

A scheduled job that hangs invisibly until its next fire, or crashes without leaving a
record, looks exactly like "everything's fine" to whatever watches it. People notice only
when a downstream signal breaks, hours later. Three layers, in priority order:

1. **Bound every external call.** Every call to an external service has a timeout — generous
   enough for the slowest legitimate call, bounded so a hang becomes a recoverable error.
   Client libraries often omit one by default; a process-wide default timeout is not a
   reliable substitute. If the library exposes no per-call timeout, inject one.
2. **Every exit writes the record a success writes.** Logging the exception is necessary but
   not sufficient: dashboards and people read the job's structured report, not its logs.
   The top-level handler writes the same report with a failed status and the error
   attached, inside its own error handling so a reporting failure cannot mask the original,
   then re-raises so the scheduler sees the failure. Otherwise the last successful run
   still shows as "latest."
3. **A watchdog is a backstop, not an error handler.** A hard-kill timer keeps hung runs
   from piling up across fires. Keep it generous and expect it almost never to fire;
   shrinking it to "fail faster" only produces faster opaque deaths.

Anti-patterns: broadening an exception handler to make the job "more resilient" (the run
shows green while the data is wrong); writing the failure report only for expected
exception types (hangs and crashes are by definition unexpected).

---

## Judgment When Things Are Ambiguous

### Finish what you started

When following a checklist, guide or multi-step process, complete every step. Don't stop at
step 5 of 8 to ask whether to do step 6 — it is on the list for a reason. Stop mid-process
only for a blocking ambiguity or an obstacle that needs the user; a discovery that would
change the scope goes through the Materiality Gate (`implementation-lifecycle`). *Example:* adding a report type is a documented six-step process; stopping after
the model to ask whether to wire the command defeats the request.

### Don't dismiss failures

When something doesn't work, find out why before removing it or working around it — the
failure may be surfacing the real problem. Optimize for understanding what happened, not
for making it pass. *Example:* several accounts in a test fixture set weren't found during
an export run. Removing them would have hidden that most had been closed before they were
ever selected — a fixture-selection bug.

### Source of truth means source of truth

When a system has an authoritative, committed source of truth — frozen expected values, a
config file, a standards document — use it. Don't re-derive the same information from
runtime data. If committed and runtime values disagree, the committed values win, or the
disagreement is surfaced; it is never papered over. *Example:* a validator that derived its
expected values from the extraction it was validating could never catch an extraction bug.

### Scope follows intent, not literal words

"Move X onto the new logging standard" means bring X into full compliance, end to end — not
just add the library. Read the intent; if a guide defines what "done" looks like, follow it
to completion. Intent is the **whole** of what was asked, never its *neighbours*: the doc
beside X that now reads slightly wrong, or the sibling of X with the same flaw, is
dispositioned by the Materiality Gate in `implementation-lifecycle`. This principle is
never a way around it.

### Investigate before removing

Before removing a test case, fixture, code path, error handler, feature flag or
configuration, understand why it is there. If you cannot explain why it was added, you may
be deleting something important. Query the data, read the history, then decide.

---
name: engineering-principles
description: The engineering principles the Enso Method depends on — no silent fallbacks, the testing evidence standard (every acceptance criterion proved at the boundary it is about), never hacking a failing test green, questioning the first correct fix, production data (dev and sandbox first, read-only and only where allowed), git safety when several sessions share one clone, bounded and visible scheduled jobs, and the judgment calls for ambiguous moments (finish what you started, don't dismiss failures, source of truth, scope follows intent, investigate before removing). Also defines how a project plugs in its own house engineering standards. Load for any code change, test work, error-handling decision, or ambiguity mid-implementation.
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
the narrow safe fix and disposition the underlying concern per `implementation-lifecycle`
(file it into the Technical Design, or ask in one line with a recommendation) without
starting an unsolicited rewrite.

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

### Test data

Unit and component tests never depend on data that lives only on one developer's machine:
fixtures are committed and referenced by repo-relative paths. Integration tests use
deliberately created or explicitly identified test records in non-production systems,
tagged so they can be found and cleaned up — never an unexplained record that happens to
exist.

### Which tests to run

While iterating, run only the tests that cover the code you are changing. The full suite
is the gate before commit. If a suite will take more than about two minutes, make it
parallel from day one; `wall-clock-awareness` has the tripwire and the concurrency-safety
checklist.

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

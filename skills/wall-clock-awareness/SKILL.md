---
name: wall-clock-awareness
description: Measure and reduce waiting time in implementation, tests, builds, CI and delayed acceptance. Identify genuine blockers, trigger equivalent interval work early when cadence is not itself under test, prepare long prerequisites, and continue authorized independent work without risky shortcuts or weakened proof. Preserve one owner for deferred checks and shared writes. Keep active CI and deployment waits in the turn; use a verified scheduled continuation only for unavoidable elapsed-time windows after useful work is exhausted. Use when repeated runs take minutes, a phase is waiting, or the user questions elapsed time. Loaded by engineering-principles and implementation skills.
user-invocable: true
---

# Wall-Clock Awareness

An agent never feels the clock. It optimizes for being right inside the session, and the
minutes spent waiting on a test suite, a build, a query job or a browser pass are invisible
to it — the human on the other side pays them. So nothing in the loop asks "what is taking
so long?", and the tax compounds silently.

**Measured on a real project:** one working session ran 3 h 36 m, about 80% of it waiting
on work that ran one item at a time — ~100 minutes on two test suites run eleven times,
single-process, on a machine that never got past 7 of 18 cores busy. Roughly a hundred
hours of sessions had run the same way before anyone asked. The fix took one afternoon: the
long suite went 19 minutes → under 2, the short one 3 minutes → 45 seconds, with an
identical pass/fail set. This skill exists so that afternoon
happens at the start, not after the hundred hours.

## The rule

**Measure wall time early, and when something you will run many times costs minutes, fix
the cheap causes now.** Not everything, and not heroically — the moves below are an
afternoon and pay back inside the week. The failure this prevents is not slowness, it is
never looking.

**The tripwire, in observable units:** a command the session runs more than a few times —
a suite, a build, a lint-and-test loop, a rebuild that proves an output — takes **more than
about two minutes**. Do the arithmetic once: runs per phase × minutes each. If that is
hours, it is the largest thing in the phase and it is not the code.

## Measure first — it is rarely where you think

1. **Time the thing.** The runner's per-test durations report, a `time` wrapper,
   timestamps on background task output.
2. **Find the floor.** Under parallelism, wall time is bounded by the single longest item.
   A long tail with a high per-item average means repeated work (0.45 s per test in the
   measured case above, because every test re-parsed the same large configuration file).
3. **Check utilization before blaming the machine.** Idle cores mean software running one
   thing at a time; more hardware or cloud runners will not move it.
4. **Separate CPU-bound from latency-bound.** A database query or an API call is bound by
   round-trip latency. Only concurrency at the request level moves it, never a bigger box.
5. **Record wall time in the evidence you already write** — suite totals, build durations —
   so the next reader sees the cost without re-measuring.

## The moves, ranked by return on effort

1. **Run less per iteration.** While iterating, run the tests that cover the code being
   changed; the full suite is the gate before commit, not the inner loop.
2. **Stop repeating work.** Cache the expensive parse, load the shared fixture once per
   run, use the fast parser that is already installed. The single biggest win in the case
   above was one line — the native-code parser instead of the pure-interpreted one, 12× on
   every read.
3. **Run independent work concurrently.** Configure the runner's parallel mode as the
   default; run independent query jobs, build steps or browser passes at once. Measured 3×
   and 6× on two suites nobody had tuned for it. Do it only after the checklist below.
4. **Split the longest single item.** Once parallel, the ceiling is the slowest test or
   job. A 20-second sweep parametrized into seven 3-second pieces lowers the ceiling.
5. **Rebuild only what changed.** A proof — a run that rebuilds an output and checks it
   against its inputs — keyed on whole shared files re-runs for edits that cannot affect
   it. Measured: of 271 commits to one shared configuration file in 60 days, **5** touched
   anything one output depended on; the other 266 each forced a 12-minute rebuild. Key it
   on the dependency slice, not the file.

## Decide what is actually blocked

At planning time, identify long prerequisites such as fixture aging, soak periods,
external approvals and scheduled windows. Start safe preparation early enough to
overlap implementation where practical. A test fixture is owned synthetic data;
record its owner, eligibility time and cleanup responsibility so advance preparation
does not become abandoned data.

Before accepting a long wait, distinguish the product or external constraint from
our chosen test setup and phase ordering. Name the exact result that cannot yet be
proved, then identify authorized work that does not require that result. A blocked
acceptance check does not automatically block design, implementation or unrelated
validation. Proceed with safe independent work; do not manufacture busywork or
silently relax an explicit user gate. When a gate really prevents useful overlap,
explain the concrete dependency and recommend a bounded change where appropriate.

**Do not wait for an interval merely because the normal flow is scheduled.** First ask
whether the scheduler or natural cadence is itself part of the behavior being proved, or
whether it is only the ordinary way the real worker starts. When an authorized manual
trigger runs the same deployed version with the same configuration, inputs and boundary
conditions, and its downside is negligible, prefer triggering it now. Hours saved from
the critical path outweigh fidelity to an incidental clock. Record the run honestly as
operator-triggered; do not describe it as the scheduled invocation.

Before triggering, verify temporal eligibility as well as task identity. A worker may be
safe to start yet intentionally ignore data until a UTC date rolls over, an upstream
window closes, or a fixture reaches a required age. If so, identify the earliest valid
instant and trigger then rather than waiting for the later normal schedule. A premature
run that cannot consume the fixture proves the gate, not the requested result.

Wait for the natural interval only when it adds material evidence: the requirement tests
the scheduler or cadence itself; an upstream system can produce the needed state only in
that window; manual dispatch follows meaningfully different code, identity, configuration
or side effects; or the trigger's operational risk is not negligible. State that reason
explicitly. “This is when it normally runs” is not enough.

Judge a workaround by its net value and risk. Reuse suitable existing test data or
prepare it earlier when that preserves the proof. Do not falsify timestamps, weaken
assertions, introduce runtime clock bypasses, add lasting production complexity, or
perform risky storage/infrastructure changes merely to shorten a test. Controlled
clocks in appropriately scoped tests prove simulated-time behavior, not that a real
elapsed-time acceptance gate passed. A modest unavoidable wait can be the right choice.

When work continues with a deferred check, retain its incomplete status and record
its exact artifact/version, owner, execution time, restoration/cleanup obligations,
and failure response. Keep one owner for shared checkout writes. Preserve the
version and environment needed by the check; overlapping code edits need not imply
permission to push or deploy over it. If the check fails, the current owner pauses
affected dependent work, fixes the issue and reruns the relevant checks on the
resulting version. Do not let several dependent phases accumulate behind an unproved
foundation. Transfer pending checks explicitly when handing off responsibility;
never relabel incomplete delivery as complete to unlock a successor.

For a genuinely unavoidable elapsed-time window, exhaust useful independent work
first. A real scheduled continuation may then own the remaining check; verify its
creation and report what will resume and when. A promise or a background shell is
not a wakeup. This exception does not turn an active CI/deployment wait into a reason
to end the turn: follow the foreground waiting rule below for those jobs.

## Concurrency safety — what changes that never mattered sequentially

Sequential execution hides a whole class of coupling. Before trusting a parallel default,
in any language and for jobs as much as tests, read for these rather than assuming:

- **Shared mutable state.** Anything writing into the repo or working directory instead of
  a per-run temp location, a cached in-memory object handed to every caller, a shared
  external table, row, queue or bucket, a fixed port, a git worktree, an environment
  variable or the current directory. Each is a collision waiting for two workers.
- **Order dependence.** An item that passed only because another ran first. Parallel
  scheduling reorders freely and exposes it as a flake that reproduces on one machine's
  core count and not another's.
- **Resource contention.** Connection-pool caps, API rate limits, licence seats, disk in
  a shared temp directory. Sequential never came near the limit; twelve workers will.
- **Single-item invocations.** A harness or gate that runs one test at a time still
  inherits the parallel default and pays a worker per core for one item. Its own
  invocation carries the runner's serial flag, in the script, not in anyone's memory.
- **The serial escape.** Know the runner's flag for one-process execution and write it
  beside the parallel config, because that is where the reader lands when it is needed.
  (For pytest-xdist it is `-n0`; `-p no:xdist` becomes a usage error once `-n auto` is
  in config.)
- **Prove the same outcome set.** Run sequential and parallel on the same tree and diff
  outcomes item by item, not the summary line. Once at setup, and again when a new kind
  of item lands. A parallel run that "mostly passes" is not set up.

Runner examples so this is not read as a Python rule: pytest-xdist, Jest and Vitest
workers, xUnit and NUnit parallelization, Go's per-package test parallelism.

## Set it up at the start, in config, not in memory

If a project will have a real suite, build or proof — even before it has one — put the
parallel default and the caching in the repo's configuration on day one. A step that lives
in memory as "remember to pass the flag" is not set up; a step that runs every time from
config is. Guard the properties that decay silently — a dropped parallel default, a
reintroduced slow path, a mutation of a shared cached object — with one small test each,
written in the same commit as the setup; each leaves the suite green and slow otherwise.

## Waiting on something external — CI, a deploy, a remote job

The moves above shrink work the session runs itself. A different tax is paid when the
session is waiting on something it cannot speed up — a pull request's CI, a deploy, a
scheduled job on another machine — and this one has a failure mode of its own that costs
more than the wait: **the session ends its turn, promises to "auto-resume when it's done",
and does not.** The human returns an hour later to a chat that has been idle since the
wait began, and cannot tell from the tab how long it has been.

**Measured on a real project:** a sub-phase's CI ran 25 minutes. The session
ended its turn promising to pick up again when CI finished. The wake-up worked that
time — and on the same machine, on other days, it had not. Research the same day found why
it cannot be relied on: wake-on-completion is specific to Claude Code, has open regressions
there, and **does not exist in Codex at all** — Codex's documented options for a
long-running command are to poll it, to stay inside a long-running tool call, or to hand
it to a subagent. These skills run under both tools, so a rule that works in one of them is
not a rule.

### The rule

**An active CI, deployment or remote-job wait never ends the turn.** For an unavoidable
elapsed-time window, first apply "Decide what is actually blocked" above. For active
jobs, follow these three parts in order:

1. **Start a watch in the background, writing to a file.** For a GitHub pull request the
   primitive is `gh pr checks --watch --fail-fast -i 30` (from the PR's branch; a number
   is optional). **Use `--watch`'s own polling, never a hand-rolled `while`/`sleep` loop
   against `gh run view` or the API** — that loop is a filed Claude Code defect
   (anthropics/claude-code#65985): it exhausts the 5,000/hour GitHub API limit and has no
   exit on a cancelled or errored run. This copy is the record, and in Claude Code it also
   gives an early notification if one arrives; it is not what the session sits on, and
   under Codex it is optional. **Do not start it in the first minute after the push**:
   until GitHub has registered at least one check run, `gh pr checks` exits 1 with *no
   checks reported*, which looks like red. Confirm one check is listed first, or retry on
   that message.

2. **Do independent work while it runs.** Work qualifies if it does not depend on the
   outcome and does not push to the branch under test — a push while CI is running starts
   a new run on the new head, and the wait begins again. The queue at this point is often
   short, and that is fine; what is usually there: recording the PR numbers in the
   governing document, memory notes, reading the next phase's governing documents. Doc
   edits made now are committed locally and pushed **after the PR merges**, as a docs
   commit on the integration branch — or before, accepting one more CI cycle (cheap when
   the workflow path-filters docs); never mid-run. The continuation prompt is not on this
   list: its doc edits ride the feature commit *before* the push, as the implement skills
   already order it. When the queue is empty, go straight to step 3 rather than inventing
   work.

3. **Before the turn ends, block on a fresh foreground watch, bounded and re-issued.**
   Bound the *command* to just under the tool's per-call ceiling and raise the tool's own
   timeout to that ceiling: in Claude Code `timeout 590 gh pr checks --watch --fail-fast`
   with the tool timeout at its 600 s maximum; in Codex `timeout 280 …` against its
   290 s background-poll cap (its interactive calls return within 30 s). `timeout` is GNU
   coreutils — present on Linux and CI runners, absent on a stock Mac, where Homebrew's
   `coreutils` provides it as `gtimeout`. Bounding only the tool is not enough — when the tool's timeout fires the
   call may be converted to a background task, which puts the session back on the wake
   mechanism this rule exists to avoid. Read the exit code, and note that `--watch`
   changes the codes from non-watch mode:
   - **0** — every check passed. Green.
   - **124** — `timeout` fired while checks were still pending. **Re-issue the same call.**
     A 25-minute CI is three chained calls in Claude Code, six in Codex; each is an
     ordinary synchronous tool call, the session is visibly running, and nothing has to
     wake it. Never end the turn on this exit.
   - **1** — a check failed, *or* `gh` hit an error (the "no checks reported" race above,
     an API failure). Read the output to tell which before calling it red.

**On red:** pull the failing log (`gh run view --log-failed`, or the failing check's URL
from `gh pr checks`), fix it, push — which restarts the clock — and return to step 1. End
the turn only with the outcome stated, green or red, with the next step handed to the user.

What makes step 3 hold is the session choosing the next call over ending the turn. That
is a discipline, not a harness guarantee — but it fails loudly (a chat stopped on
"pending") rather than silently (a chat idle with a promise), and it is the same
discipline as any multi-step tool loop. Only a subagent or scheduled task that the harness itself re-invokes can resume the
chat without the user; **a CI wait never qualifies, and neither does a background watch of
one** — never tell the user the chat will resume on its own.

### Take the wait off the critical path

Most of a CI wait is spent re-running tests the session already ran. It is on the critical
path only because local and CI differ, and the differences are mechanical: the local suite
reads the working tree while CI reads the commit; CI tests the branch merged with the
integration branch; CI lacks a sibling checkout the local tree has (or the reverse). Each
is reproducible locally. A repo script that exports the commit with `git archive`, merges
the integration branch into the export, and runs the exact test invocation CI runs turns
"wait for CI" into "CI will be green — proceed", and the wait leaves the critical path. It
is the same afternoon-sized fix as the parallel default above, and it pays back on every
pull request; write it the first time a repo's CI takes longer than the suite does
locally.

## When not to bother

- The arithmetic says no: a run under the tripwire, a script run once, a job run once per
  phase.
- The day-one config is already in place and wall time sits at the floor of the longest
  single item. Leave it; do not re-optimize every session.
- Latency-bound work with no independent pieces to overlap. (The waiting rule above
  still applies — it is about not ending the turn, not about overlap.)
- Anything whose concurrency safety you have not proven. A flaky suite costs more time
  than a slow one.
- Do not build infrastructure to fix a cost you have not measured.

## Relationship to other skills

| Skill | Relationship |
|---|---|
| `engineering-principles` | The general principles and the testing evidence standard; this skill is the clock-specific one. Points here from its testing section for slow suites. The repo's own test-runner configuration belongs to the house engineering standards it names. |
| `implement-from-requirements` / `implement-from-discovery` | Both load this at their test phase before running a slow suite repeatedly, and point here again from their pull-request step — opening a PR is where a session is about to wait on CI. |
| `test-hardening` | Not where the day-one guard tests go — that skill is bounded to a feature's acceptance criteria. Write them with the setup itself. |

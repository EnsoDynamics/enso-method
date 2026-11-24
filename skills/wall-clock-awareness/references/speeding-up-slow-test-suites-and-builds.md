# Speeding Up Slow Test Suites and Builds

Reference for `wall-clock-awareness`. Read it when setting up a test runner, a build or a
pipeline, and when the user asks why one takes so long or asks to speed it up. A session
building a feature does not start this work on a suite it did not set up.

## Contents

- The rule
- Measure first — it is rarely where you think
- The moves, ranked by return on effort
- Concurrency safety — what changes that never mattered sequentially
- Set it up at the start, in config, not in memory
- Take the CI wait off the critical path
- When not to bother

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

**Measure wall time first, and fix the cheap causes of whatever is run many times.** Not
everything, and not heroically — the moves below are an afternoon and pay back inside the
week. The failure this prevents is not slowness, it is never looking.

**What is worth fixing, in observable units:** a command a session runs more than a few
times — a suite, a build, a lint-and-test loop, a rebuild that proves an output — that
takes **more than about two minutes**. Do the arithmetic once: runs per phase × minutes
each. If that is hours, it is the largest thing in the phase and it is not the code.

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
   and 6× on two suites nobody had tuned for it. Do it only when the checklist below leaves
   you highly confident that it will not make the run flaky and will not exhaust the
   machine; otherwise keep it sequential.
4. **Split the longest single item.** Once parallel, the ceiling is the slowest test or
   job. A 20-second sweep parametrized into seven 3-second pieces lowers the ceiling.
5. **Rebuild only what changed.** A proof — a run that rebuilds an output and checks it
   against its inputs — keyed on whole shared files re-runs for edits that cannot affect
   it. Measured: of 271 commits to one shared configuration file in 60 days, **5** touched
   anything one output depended on; the other 266 each forced a 12-minute rebuild. Key it
   on the dependency slice, not the file.

## Concurrency safety — what changes that never mattered sequentially

Sequential execution hides a whole class of coupling. Parallelize only when highly
confident it will not make the run flaky or exhaust the machine. That confidence has a
definition: every item below was read for in the code, in any language and for jobs as
much as tests, not assumed, and the proof at the end passed. When an item cannot be
settled, keep the run sequential, or parallelize only the part that can be.

- **Shared mutable state.** Anything writing into the repo or working directory instead of
  a per-run temp location, a cached in-memory object handed to every caller, a shared
  external table, row, queue or bucket, a fixed port, a git worktree, an environment
  variable or the current directory. Each is a collision waiting for two workers. The fix
  is one of each per worker: name it by the runner's worker id (a schema, an account, a
  directory, a key prefix), and bind port zero so the system picks a free port.
- **Setup meant to run once.** Under most runners a fixture or hook scoped to the whole
  run executes once in every worker. Whatever it creates, such as a database, a server or
  seeded data, is then created several times at once, unless it is made per worker or
  guarded by a lock.
- **Order dependence.** An item that passed only because another ran first. Parallel
  scheduling reorders freely and exposes it as a flake that reproduces on one machine's
  core count and not another's. Each test builds the state it needs; none relies on what
  another left behind.
- **Timing that assumed an idle machine.** Fixed sleeps, tight timeouts and assertions on
  elapsed time pass when one test has the machine to itself and fail when several share
  it. Published studies of flaky tests find this the largest single cause. Search the
  suite for sleeps and timeouts before anything else: each waits on a condition, with a
  timeout sized for a loaded machine.
- **Resource contention.** Connection-pool caps, API rate limits, licence seats, disk in
  a shared temp directory. Sequential never came near the limit; twelve workers will.
- **Leftovers.** A child process, a connection, a container or a temp directory that a
  test does not release costs nothing one at a time and reaches a limit when many run
  together. Each test releases what it starts.
- **What each worker starts.** A browser, a server, a container or a child process per
  worker multiplies memory and CPU by the worker count, on a machine other sessions and
  worktrees may be using at the same time. Set the worker count explicitly, at what the
  machine holds with those running and not at its core count, and separately for CI,
  whose runners usually have fewer cores and less memory than a development machine.
- **Heavy tests.** Browser, emulator and container tests are the likeliest to turn flaky
  under load. Parallelism is not all or nothing: run the light tests in parallel and keep
  the heavy ones serial or in a small capped group, or run files in parallel and the
  tests within a file in order.
- **Single-item invocations.** A harness or gate that runs one test at a time still
  inherits the parallel default and pays a worker per core for one item. Its own
  invocation carries the runner's serial flag, in the script, not in anyone's memory.
- **The serial escape.** Know the runner's flag for one-process execution and write it
  beside the parallel config, because that is where the reader lands when it is needed.
  (For pytest-xdist it is `-n0`; `-p no:xdist` becomes a usage error once `-n auto` is
  in config.)
- **Prove the same outcome set, repeatedly.** Run sequential and parallel on the same
  tree and diff outcomes item by item, not the summary line. Then run the parallel
  configuration several times in a row, five as a floor, at the worker count and on the
  kind of machine it will use, CI included. One differing outcome in any run means it is
  not safe yet: find the cause in the list above, and never add retries to hide it. Do
  this at setup, and again when a new kind of item lands.

Runner examples so this is not read as a Python rule: pytest-xdist, Jest and Vitest
workers, xUnit and NUnit parallelization, Go's per-package test parallelism.

## Set it up at the start, in config, not in memory

If a project will have a real suite, build or proof — even before it has one — put the
caching, and the parallel default once the checklist above passes, in the repo's
configuration on day one. Where the runner's configuration lives and how it is laid out
belongs to the project's house engineering standards. A step that lives
in memory as "remember to pass the flag" is not set up; a step that runs every time from
config is. Guard the properties that decay silently — a dropped parallel default, a
reintroduced slow path, a mutation of a shared cached object — with one small test each,
written in the same commit as the setup; each leaves the suite green and slow otherwise.
They are written with the setup itself, not in `test-hardening`, which is bounded to a
feature's acceptance criteria.

## Take the CI wait off the critical path

Most of a CI wait is spent re-running tests the session already ran. It is on the critical
path only because local and CI differ, and the differences are mechanical: the local suite
reads the working tree while CI reads the commit; CI tests the branch merged with the
integration branch; CI lacks a sibling checkout the local tree has (or the reverse). Each
is reproducible locally. A repo script that exports the commit with `git archive`, merges
the integration branch into the export, and runs the exact test invocation CI runs turns
"wait for CI" into "CI will be green — proceed", and the wait leaves the critical path. It
is the same afternoon-sized fix as the parallel default above, and it pays back on every
pull request, most of all where a repo's CI takes longer than the suite does locally.

## When not to bother

- The arithmetic says no: a run under the tripwire, a script run once, a job run once per
  phase.
- The day-one config is already in place and wall time sits at the floor of the longest
  single item. Leave it; do not re-optimize every session.
- Latency-bound work with no independent pieces to overlap. (The waiting rule in this
  skill's `SKILL.md` still applies — it is about not ending the turn, not about overlap.)
- Anything whose concurrency safety you have not proven. A flaky suite costs more time
  than a slow one.
- Do not build infrastructure to fix a cost you have not measured.

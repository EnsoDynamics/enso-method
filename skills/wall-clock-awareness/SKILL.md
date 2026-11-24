---
name: wall-clock-awareness
description: Keep the loop that proves the work fast. Tests, builds, CI and waits are run again by every later session, and the person waiting pays for each run. Check what a test, build step or CI job costs when adding or changing it; set up a new suite or pipeline so it stays fast; report what the full run took instead of sensing it; decide what a scheduled wait really blocks; never end the turn on an active CI or deployment wait. Use when adding or changing tests, builds, CI or proof scripts, when setting up a test runner or pipeline, when a full run finishes, when a session is about to wait on CI, a deployment or a scheduled job, or when the user questions elapsed time. About development time, not the application's speed in production. Loaded by engineering-principles and the implementation skills.
user-invocable: true
---

# Wall-Clock Awareness

Everything a session runs to prove the work — tests, builds, CI, proof scripts — is run
again by every later session, and the person waiting pays for each run. This skill keeps
that loop from growing until someone has to ask why it takes hours. It covers development
time only, not how fast the application runs in production.

An agent never feels the clock: a run reads the same to it whether it took ten seconds or
an hour. So nothing here asks a session to notice time passing. Each part starts from an
action the session takes or a duration a tool prints:

- **Adding or changing a test, a fixture, a build step, a CI job or a proof script, or
  running the same dry run or test-environment run again while building.** Follow "What a
  new test or step costs" below.
- **A full suite, build or pipeline run finishes.** Follow "Report what the full run took"
  below.
- **About to wait on CI, a deployment or a remote job.** Follow "Waiting on something
  external" below.
- **About to wait for a scheduled run, a soak period, an approval or an aged fixture.**
  Follow "Decide what is actually blocked" below.
- **Setting up a test runner, a build or a pipeline, or the user asks to speed one up.**
  Read [Speeding up slow test suites and builds](references/speeding-up-slow-test-suites-and-builds.md)
  and follow it.

## What a new test or step costs

Whatever a session adds to the loop is run again long after the session ends: a test in
every full-suite run and every CI run, a CI job on every push. Before moving on from one:

1. **Run it alone and read its duration** from the runner's output.
2. **Compare it with its neighbours.** Run the file or folder it sits in and read the
   per-test durations; no full-suite run is needed. A new one slower than most tests
   around it needs a reason you can name: the boundary it proves cannot be reached more
   cheaply.
3. **Otherwise make it cheaper, without weakening what it proves.** Setup and teardown
   are the usual cost: build expensive setup once, share it across the tests that only
   read it, and tear it down once. Where each test changes that state, build it once and
   hand each test a cheap copy. Prove logic at the lowest level that reaches it, and
   keep the slow level for the boundary itself. Wait on the condition instead of sleeping
   a fixed time. Start a browser, server or container once per file, not once per test.

The same holds for what the session itself runs repeatedly while building, such as a dry
run or a run against a test environment: read how long one run takes, iterate on the
smallest input that shows the result, and run the whole thing once at the end.

## Report what the full run took

When the full suite, build or pipeline finishes at the commit gate, read its wall time
from the runner's summary and give it beside the command in the wrap-up: "full suite green
(`pytest`, 14 min)". The person then sees what the loop costs in every session, and growth
shows long before it hurts.

A session building a feature keeps its own tests cheap and reports the time. It does not
go on to tune a suite it did not set up: that is separate work the user starts, and the
speeding-up reference is how it is done.

## Waiting on something external

**An active CI, deployment or remote-job wait never ends the turn.** Start a watch in the
background, do work that does not depend on the outcome, then block on a bounded
foreground watch and re-issue it until the job finishes. Never tell the user the chat
will resume on its own. Before the wait begins, read
[Waiting on CI, deploys and remote jobs](references/waiting-on-ci-deploys-and-remote-jobs.md)
for the commands, exit codes and per-tool limits, and follow it.

## Decide what is actually blocked

Before accepting a wait for a scheduled run, a soak period, an approval or an aged
fixture, name the exact result that cannot yet be proved and carry on with the authorized
work that does not need it. Do not wait for an interval only because the normal flow is
scheduled. Read [Deciding what a wait actually blocks](references/deciding-what-a-wait-actually-blocks.md)
and follow it.

## Relationship to other skills

| Skill | Relationship |
|---|---|
| `engineering-principles` | Points here from "Which tests to run" whenever a session adds a test, a build step or a CI job, or sets up a suite or pipeline. |
| `implement-from-requirements` / `implement-from-discovery` / `test-hardening` / `test-audit` | Each points to "What a new test or step costs" at the step where it writes tests. `test-hardening` and `test-audit` report the full run's duration with its command at the commit gate. |
| `implement-from-requirements` / `implement-from-discovery` | Both point here from their pull-request step — opening a PR is where a session is about to wait on CI. |

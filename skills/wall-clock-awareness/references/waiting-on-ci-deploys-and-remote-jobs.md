# Waiting on CI, Deploys and Remote Jobs

Reference for `wall-clock-awareness`. Read it before a wait on CI, a deployment or a
remote job begins.

A session waiting on something it cannot speed up — a pull request's CI, a deploy, a
scheduled job on another machine — has a failure mode that costs more than the wait:
**the session ends its turn, promises to "auto-resume when it's done", and does not.**
The human returns an hour later to a chat that has been idle since the
wait began, and cannot tell from the tab how long it has been.

**Measured on a real project:** a sub-phase's CI ran 25 minutes. The session
ended its turn promising to pick up again when CI finished. The wake-up worked that
time — and on the same machine, on other days, it had not. Research the same day found why
it cannot be relied on: wake-on-completion is specific to Claude Code, has open regressions
there, and **does not exist in Codex at all** — Codex's documented options for a
long-running command are to poll it, to stay inside a long-running tool call, or to hand
it to a subagent. These skills run under both tools, so a rule that works in one of them is
not a rule.

## The rule

**An active CI, deployment or remote-job wait never ends the turn.** For an unavoidable
elapsed-time window, first apply `deciding-what-a-wait-actually-blocks.md`. For active
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

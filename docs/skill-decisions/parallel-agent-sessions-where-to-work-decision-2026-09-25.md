# Parallel agent sessions: where each chat works (decision record, 2026-09-25)

Maintainer notes for the rule in `implementation-lifecycle/SKILL.md` ("Parallel Sessions: Where to Work") and its prompt-side counterpart in `continuation-prompt/SKILL.md` (Step 3, "Where to work"). **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing either rule.

## The problem

- **One shared checkout, many chats.** One person runs several AI coding chats in the VS Code extension at once, all launched from the org directory. They all worked in the same shared checkout on the shared branch (`develop`). Measured failures in one day:
  - One chat could not fast-forward because another chat's staged files were in the way.
  - A `git add` swept another chat's staged work into a commit.
  - Two chats regenerated the same generated manifest within an hour and had to message each other to avoid reverting each other's changes.
  - A chat left uncommitted edits in files another chat needed.
- **Prompts named a branch, not a directory.** Continuation prompts said "work on develop in <repo>". One session had improvised a private clone to get around a blocked checkout. The prompt carried neither that choice nor an explicit "use the shared checkout", so the next chat had to guess which copy of the repo was meant.
- **Most work is sequential.** Isolation would not help there, and it creates directories to track down and delete. Any rule had to leave the one-chat-at-a-time case untouched.

## What we read (2026-09-25)

| Source | What it contributed |
|---|---|
| Claude Code docs, "Run parallel sessions with worktrees" (code.claude.com/docs/en/worktrees) | The documented pattern. A worktree is a separate working directory and branch sharing the repository's history. `claude --worktree <name>` and the `EnterWorktree` tool create them under `.claude/worktrees/`. Automatic cleanup applies only when an interactive `--worktree` session exits, and to subagent and background worktrees through a periodic sweep. `.worktreeinclude` copies gitignored files. The session is blocked from editing the main checkout. Worktrees share `.git`, and permission approvals follow them. |
| Upsun, "Git worktrees for parallel AI coding agents" | Worktrees isolate files, not runtime: ports, databases and services stay shared. "Why not clone five times?": a clone duplicates the object database, and one fetch serves every worktree. incident.io runs 4–5 agents at once. |
| Verdent, "Codex App Worktrees Explained" | The Codex app builds parallel threads on worktrees. A clone-vs-worktree table. The main gotcha is that gitignored files (`node_modules`, `.venv`, `.env`) don't exist in a new worktree. Independent tasks gave zero merge conflicts; tasks sharing files would not. |
| Nimbalyst, "How to run coding agents in parallel with git worktrees" | Semantic conflicts are the failure that survives worktrees: two agents change related behaviour, it merges cleanly and breaks. The fix is task decomposition, naming each session's owned files. Merge one branch at a time and test between merges. The real limit is "how many diffs you can genuinely read in an hour". Lockfile churn. |
| Augment Code, "How to use git worktrees for parallel AI agent execution" | Failure modes of agents sharing one directory: silent overwrites, stale context, `.git/index.lock` contention leaving uncommitted state behind. Per-worktree versus shared git state (HEAD and index private; objects, refs and config shared). |
| worktreewise.com, "Git worktree vs clone" | When a clone is warranted: a fully separate environment, forks, isolated histories, destructive operations such as rewriting history. Otherwise worktrees. Worktrees don't clean up after themselves; prune and remove them. |
| Stack Overflow 48307968, "git worktrees vs clone --reference" | A `--reference` or `-s` clone depends on the source repository's objects without the source knowing, so `gc` there can break it. Worktrees are tracked by the main repository. |
| incident.io, "How we're shipping faster with Claude Code and Git Worktrees" | A real team running 4–5 parallel agents on worktrees, with a small helper to create and enter them. |
| dev.to, "Trunk-based development with short-lived branches" | Branches live for hours, not days; merge early and often. That fits a shared-branch workflow if isolation branches are short-lived. |
| Laurent Kempé, "From 3 worktrees to N" | Worktree tooling (grove, worktrunk) and fan-out orchestration; per-agent file-write guards. |


## Options considered

1. **Always the shared checkout** (the old rule). Collides as soon as chats run in parallel. Rejected as the only rule; kept as the default.
2. **Always isolate: a worktree or clone for every chat.** Solves collisions, but leaves directories behind for every sequential chat, and nothing cleans them up in the VS Code extension. Rejected: most work is sequential.
3. **A private clone per chat** (what one session improvised). Its only advantage over a worktree is that it can check out `develop` a second time without a new branch. Costs: a separate object store, per-clone fetches, `-s` clones depending on the source's objects, and nothing in the main repository tracks them. Rejected except when the user asks.
4. **Claude Code's `--worktree` with its automatic cleanup.** The documented tool, but its cleanup runs only when an interactive `--worktree` session exits. Chats started from the VS Code extension don't get it, so a rule that relies on it leaves worktrees behind. Rejected as the mechanism; the chat creates and removes its worktree with plain git.
5. **Chosen: shared checkout by default; a worktree only on a stated or detected parallel signal; the chat cleans up itself.**

## The decision and why

- **Default: the shared checkout.** Most work is sequential, and it needs nothing to clean up.
- **Worktree only when a signal says the work is parallel:**
  - the prompt says `Parallel: yes`, which a coordinating chat sets whenever it hands out several prompts at once;
  - a live session log is present in the repo (START, no DONE, written within 12 hours; older logs are abandoned).
  The detection covers "four chats started a few minutes apart" without anyone declaring it: the first chat takes the shared checkout, and each later one sees the earlier chats' logs and isolates itself.
- **Worktrees, not clones.** This is the practice every source converges on. Clones only on request.
- **Worktree layout:** `<org directory>/.worktrees/<slug>/<repo>`, so a multi-repo chat keeps its repos as siblings and there is one folder per chat to find and delete. The slug is the chat name lowercased with hyphens, because chat names contain spaces and a branch name cannot. The branch is `wt/<slug>`, only because git refuses to check out the shared branch twice. Once any signal holds, every repo the chat edits goes under the folder. The chat's session log stays in the shared checkout, so later chats see it.
- **Land each piece as it's finished, when committing and pushing are authorized:**
  - rebase, push `HEAD:<shared branch>` as a fast-forward, and on rejection fetch, rebase and retry; never force;
  - always attempt to fast-forward the shared checkout, which succeeds beside another session's uncommitted edits unless they overlap.
  The fast-forward is what separates this from an earlier failure: pushing around a checkout's branch left a shared checkout dozens of commits behind. Without authorization, the chat stages in the worktree and leaves it in place for the user to review and commit.
- **The chat removes its own worktree at wrap-up,** running the commands from the shared checkout. It uses `git branch -d`, which refuses to delete unmerged work, and the wrap-up reports the result. This keeps the intent of the shared-branch default: nothing is left unmerged, and nothing merged is left behind.
- **Owned areas for parallel prompts,** because worktrees can't prevent semantic conflicts.

## Review findings folded in before release

A fresh-eyes review tested the git mechanics in a scratch repo and found:

- **Invalid branch names:** chat names contain spaces, so the rule now uses a slug.
- **Authorization:** landing needed the commit and push authorization rule; it now defers to it.
- **Fast-forward too cautious:** skipping the shared checkout's fast-forward when it was dirty would recreate the stale-checkout failure; the chat now always attempts it.
- **Push rejection:** a rejected push needed a rebase-and-retry rule, and force-pushing is excluded for the shared branch.
- **Split siblings:** one repo isolated while its sibling wasn't would break sibling-repo tests; every repo now moves together.
- **Log placement:** a worktree chat's log has to stay in the shared checkout so later chats detect it.
- **Cleanup location:** cleanup runs from the shared checkout, not from inside the worktree being removed.

It also confirmed that `git branch -d` succeeds once the `wt/` branch is merged into its upstream (`origin/<shared branch>`), even before the shared checkout fast-forwards.

## Revised after the user's review (same day)

- **Trigger removed.** A third trigger ("the shared checkout holds uncommitted changes this chat didn't make") was dropped. It went beyond the user's stated rule, which is to isolate only when the work is declared parallel or another agent session is live. It would also have fired on the user's own unsaved edits. The older rule, leave others' uncommitted files alone and stage only your own, covers that case.
- **Global instructions file cut to a minimum.** The rule lives in the skill. A global instructions file that forbids branches or worktrees outright needs only a one-sentence exception pointing at `implementation-lifecycle`, "Parallel Sessions: Where to Work".

## Open questions to revisit

- Whether 12 hours is the right window for "live". Long chats that wait on CI can go quiet for longer.
- Whether a small helper script (create a worktree, and list or remove leftovers) would beat instructions in prose.
- Runtime isolation (ports, scratch databases, virtual environments) is handled only by the `PYTHONPATH` note. A repo that runs servers or local databases will need more.

---
name: pre-commit-validation
description: Commit-boundary validation ("git police") — verify the staged changeset is clean, coherent, and safe on a shared multi-session workstation. Expected-changeset staging hygiene, secrets scan, diff sanity, concurrent-commit detection, and committing on the local branch (never building on the remote and pushing around it). Loaded by the implement skills at commit time, before presenting or creating any commit.
---

# Pre-Commit Validation ("Git Police")

## Metadata

- **Type:** reference (loaded by the implement skills at commit time)
- **Trigger:** Follow these guidelines at the commit boundary — after testing, deliverable review and test hardening, before committing
- **Purpose:** Ensure the staged changeset is clean, coherent, and safe — especially important on a shared workstation with concurrent sessions

---

## Why This Exists

This runs in a checkout where several agent sessions (Claude Code, Codex or others), manual edits, and other development work can happen concurrently in the same repo and branch. Files can appear in the staging area or working tree from unrelated work at any moment. Another session can commit to the same branch while you're validating. The autonomous workflow cannot assume that everything visible in `git status` belongs to it, or that the branch state is stable.

The deliverable review validates that the *work* is correct. This validates that the *commit* is correct — that only the right files are in it, nothing dangerous is in the diff, and the commit is a clean atomic unit. These are different concerns, and the state of the working tree can change between when the deliverable review runs and when you commit.

This is not optional. Every commit — interactive or autonomous — must follow these steps.

---

## Who Commits

The user does. Every skill that ends at a commit — implement, review, refinement, split, roadmap, refactor — stages its files, runs these checks, and presents the commit message, so the user can read the diff before it lands. A session runs `git commit` or `git push` itself only when the user has explicitly told it to, in this chat or in the request that started an authorized `phase-chain`. Finishing the work or passing every check is not that instruction.

**Another session's staged files stay staged.** Never unstage a file you did not stage: the shared index is how each session hands its commit to the user, and unstaging silently undoes another chat's hand-off. Stage your own files beside them and hand the user a commit limited to your paths — `git commit -m "<message>" -- <your paths>` — which commits exactly those files and leaves the rest staged. If another session has also changed one of your files, git cannot split the two sets of edits: say so in the hand-off rather than committing either. When the user has told the session to commit, it uses the same path-limited commit (or Step 9's temporary index).

---

## When to Follow These Guidelines

At the point in your workflow where you're ready to stage and commit — after deliverable review passes and before presenting the commit message. In `implement-from-requirements` and `implement-from-discovery`, it's the Phase 8 wrap-up step that stages and presents the commit. This skill encompasses staging; there is no separate staging step.

---

## Steps

### Step 1: Record HEAD and Inventory What You Changed

**Bring the local branch current first:** Run `git pull --ff-only` before anything else (in a worktree, `git fetch` and rebase onto `origin/<branch>` instead), so the moved-HEAD check below sees the other sessions' commits. If it refuses, see "If the local branch cannot fast-forward" in Step 9 and stop there.

**Record the current HEAD:** Run `git rev-parse HEAD` and note the hash. You'll need this later to detect if another session committed while you were validating.

**Build your expected changeset:** Before looking at git status, make a list from memory of every file you intentionally modified, created, or deleted during this task. Be specific — full relative paths from the repo root. File renames count as a deletion + an addition; include both paths.

For a typical fix, common expected files include:
- The source code file(s) you changed
- Assumptions document (if updated)

### Step 2: Check the Staging Area

Run `git status`. Before staging anything, check for contamination:

- **Files that are already staged but aren't in your expected changeset** — another session or manual work staged these. Leave them staged (see "Who Commits"). Do NOT commit them. Do NOT silently include them: your commit is limited to your own paths.
- **Files that are modified but unstaged and aren't in your expected changeset** — someone else's work-in-progress. Leave them alone. Do not stage, do not revert.
- **Files you expected to see modified but that aren't showing up** — Did you forget to save? Did another process revert your change? Investigate before proceeding.
- **Merge conflict markers in any file** — if `git status` shows merge conflicts, or if any file contains `<<<<<<<`, `=======`, `>>>>>>>` markers, do NOT proceed. Resolve conflicts, re-stage, and restart from Step 1.

### Step 3: Stage Your Files

Stage only the files from your expected changeset. Use explicit file paths — never `git add .` or `git add -A`.

### Step 4: Verify Change Coherence

Now that your files are staged, verify each one belongs:

- **For each of your staged files, state why it's in the commit.** If you can't articulate the connection to the task in one sentence, it doesn't belong.
- **Would reverting this commit cleanly undo exactly one logical change?** If reverting would also undo unrelated work, the commit is polluted.
- **Version bump, if required.** If the repo's own instructions require a version bump with each change, verify it is staged.

### Step 5: Scan the Staged Diff for Secrets

Run `git diff --cached -- <your paths>` and scan every addition (lines starting with `+`) for:

- API keys, tokens, passwords (patterns like `sk-`, `Bearer `, `password=`, `secret=`, `token=`, `key=` followed by what looks like an actual value rather than a variable reference)
- `.env` file contents or environment variable assignments with real values
- AWS access keys (`AKIA...`), secret keys, session tokens
- Private keys (`-----BEGIN`)
- Connection strings with embedded credentials
- Password-manager references that resolved to actual secrets instead of reference URIs
- Hardcoded URLs with authentication parameters

If anything suspicious is found: **stop.** Remove the secret from the source file, re-stage, and verify the diff is clean before proceeding. Flag it to the user in both interactive and autonomous mode — even if you can fix it mechanically, the user should know it happened so they can investigate how a secret ended up in the code.

### Step 6: Diff Sanity Check

Review `git diff --cached -- <your paths>` with fresh eyes for artifacts that shouldn't be committed:

- **Debugging artifacts** — `print()` statements, `console.log()`, `import pdb`, `breakpoint()`, temporary exploration scripts or code you added during investigation
- **Commented-out code you added** — if code was intentionally removed as part of the fix, remove it cleanly rather than commenting it out. Exception: if commenting out code IS the fix (e.g., temporarily disabling a problematic feature), that's fine as long as the re-enablement is recorded in the governing PRD or phase document.
- **Unintended whitespace changes** — large whitespace-only diffs suggest an editor reformatted a file you only meant to touch in one place; revert the whitespace changes if unintentional
- **TODO/FIXME/HACK comments you added** — follow-up work goes into the governing docs per `implementation-lifecycle`'s disposition rule (a future phase document, the Technical Design, or the assumptions document), not buried in code comments

### Step 7: Commit Message Format Check

Verify the commit message follows the project's convention before presenting it — its house engineering standards, or failing that the style of recent `git log`. Where neither sets one, use:

- Format: `type(scope): description`
- Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Scope should identify the component (e.g., `user-accounts`, `notifications`, `billing-sync`)
- Description should describe what actually changed — not reference ephemeral project artifacts as the primary subject
- Ticket or issue references (e.g., `(PROJ-123)`) go at the end as a suffix
- In autonomous mode, include `Co-Authored-By:` trailer with the current model

### Step 8: Final Staging Check

Right before committing (or presenting the commit to the user), do one last verification:

1. Run `git diff --cached --name-only` and compare against your expected changeset. If any file appears that you didn't stage, another session staged it between your Step 2 check and now. Leave it staged and keep it out of your commit — the path-limited commit ("Who Commits") does that.
2. Run `git rev-parse HEAD` and compare against the hash you recorded in Step 1. If HEAD has changed, another session committed while you were validating. In this case:
   - Your commit will still work (git handles concurrent commits to the same branch), but be aware that your changes sit on top of untested work
   - In autonomous mode, if the other commit touched the same files, flag this to the user rather than committing blindly

This step exists because the staging area is shared state that can change at any time on a multi-session workstation. Steps 2-6 are not atomic — this final check catches anything that slipped in between.

### Step 9: Commit on the Local Branch, and Push Only From It

The commit's parent is the **local** branch, and the local branch moves to it. The local branch was brought current in Step 1.

- **A path-limited commit or a temporary index is fine; a different parent is not.** The path-limited commit ("Who Commits") keeps another session's staged files out. So does committing through a temporary index built from `HEAD`: `export GIT_INDEX_FILE=$(mktemp)`, `git read-tree HEAD`, `git add <your paths>`, `git commit`, then `unset GIT_INDEX_FILE`. Agent tools usually start a fresh shell per call, so an `export` does not survive to the next call: run the whole sequence as one command, or record the temp path once and prefix every git command in it with `GIT_INDEX_FILE=<path>`. `git commit` builds on the current branch and advances it safely even if another session commits at the same moment. Steps 2, 3, 5 and 8 then run against that temporary index rather than the shared one. After unsetting it, run `git reset -q -- <your paths>` so the shared index matches the new `HEAD`; otherwise `git status` shows your own commit as staged changes in reverse.
- **Never build a commit on `origin/<branch>` and push it by refspec** (`git push origin <sha>:refs/heads/<branch>`). The commit reaches the remote, but the checkout's branch never moves, so every file the user opens shows the old state. In one real case this left a shared checkout dozens of commits behind, and the user saw a finished item as unfinished in their own editor.
- **The one exception is a chat working in a worktree** (`implementation-lifecycle`, "Parallel Sessions: Where to Work"). A worktree cannot check out the shared branch, so the chat commits on its own `wt/<slug>` branch and lands each piece by pushing `git push origin HEAD:<branch>` as a fast-forward after rebasing. It then fast-forwards the shared checkout (`git -C <shared checkout> merge --ff-only origin/<branch>`) so the editor shows the work; that fast-forward is what keeps this from being the failure above. If the push is rejected, fetch, rebase, re-test and push again, and never force. If the fast-forward is refused, say so in the wrap-up. In a worktree the index is private, so the temporary index above is unnecessary.
- **Push only when pushing is authorized, and only your own commits.** Before pushing, run `git log --oneline @{u}..HEAD`. If any commit listed is not yours, another session has unpushed work on this branch; stop and tell the user rather than publishing it with yours.
- **If the local branch cannot fast-forward, stop and tell the user.** Name the cause and let the user decide. It is one of three:
  - another session's modified or untracked files are in the way: list them, and for each say whether it already matches the remote (`git diff --quiet origin/<branch> -- <file>`);
  - your own uncommitted edits touch files the remote changed;
  - the branch has diverged (local commits not on the remote, and the remote has moved on).

  Do not route around the local branch, and do not delete, revert or stash another session's files yourself.

There is no exception to this step beyond the worktree case above. The known cases that tempted a session to push around the local branch were all blocked fast-forwards, and those have their own answer above.

---

## Output

Produce a brief validation summary as part of the commit presentation:

```
Pre-commit validation:
- Staged files: [list of files, each with one-line justification]
- Contamination check: [clean | N files staged by other work, left staged and excluded — list them]
- Secrets scan: clean
- Version bump: [verified | N/A — only if the repo requires one]
- Diff review: clean [or list what was fixed]
- Commit message: fix(scope): description ✓
- Final staging check: [clean | issues found — describe]
- Local branch: current with remote before commit; commit built on HEAD [push: only own commits in @{u}..HEAD | not authorized]
```

**By default:** Include this summary alongside the testing evidence when presenting the commit message to the user, and give the path-limited command to run: `git commit -m "<message>" -- <your paths>`.

**When the user has explicitly told this session to commit:** If all checks pass, proceed to commit with the path-limited command (or Step 9's temporary index). If any check fails and can be fixed mechanically (a debug print left in), fix it and re-validate. If a check fails and requires judgment (suspicious content, files you can't explain, HEAD moved with overlapping changes), stop and flag to the user.

---

## What This Does NOT Do

- **Does not run tests** — that's the calling workflow's responsibility
- **Does not validate business logic** — that's the deliverable review's job
- **Does not choose which branch to work on** — that is the user's branching rule; this skill only requires that the commit lands on the local branch (Step 9)
- **Does not replace human review** — this is a safety net, not a substitute for the user looking at the commit in interactive mode

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `implement-from-requirements` / `implement-from-discovery` | **Callers** — follow these guidelines before presenting the final commit |
| `deliverable-review` | **Complementary** — deliverable review validates work quality earlier in the pipeline; this validates commit hygiene at the commit boundary, after which the working tree state may have shifted due to concurrent work |
| `engineering-principles` | **Referenced** — its "Git Safety When Several Sessions Share One Clone" is the underlying rule for the staging checks here; coding standards come from it plus the house engineering standards the project names |

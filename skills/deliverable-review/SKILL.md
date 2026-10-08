---
name: deliverable-review
description: Verify completed work accomplishes what was intended — fresh-eyes sub-agent re-reads output files, traces requirements, checks for gaps and omissions, and reports findings for the main agent to fix.
---

# Deliverable Review

Verify that completed work accomplishes what was intended, and fix any issues found.

A sub-agent with a fresh context window re-reads the actual output files — avoiding the bias of the agent that produced the work reviewing it from memory. The main agent orchestrates, then fixes whatever the sub-agent finds.

In the standard implementation chain this is the second step (`implement-from-requirements` → `deliverable-review` → `test-hardening`): this skill verifies the deliverable matches intent, then `test-hardening` verifies the tests prove the requirements. (`refactor-pass` follows as an optional post-commit step, after the user has committed the feature work.)

---

## Process

### Step 1: State the Intent

Before reviewing details, articulate the goal of the work in 1-2 sentences:
- What were we trying to accomplish?
- If there's a ticket, story, or PRD that motivated this work, reference it

This becomes the anchor for the entire review. Write it down — you'll come back to it at the end.

### Step 2: Gather Context

Collect the information the sub-agent will need:

1. Run `git diff --stat` and `git status` to see what files changed
2. Summarize what was done in 2-3 sentences
3. List the key decisions made during the session, including:
   - What WAS decided (features, approaches, values)
   - What was explicitly NOT decided or deferred (scope exclusions, future work)
4. Note the deliverable type (code, documentation, configuration, mixed)

### Step 3: Launch Sub-Agent

Launch a single general-purpose sub-agent with:

- The stated intent from Step 1
- The context summary from Step 2
- The list of changed files
- Instruction to read this skill's `SKILL.md` — pass the absolute path of the file this skill was loaded from — and follow the **Review Checklist** section
- **Instruction to re-read every changed file from disk** — do not rely on conversation memory
- **Report all findings as a structured list. Do NOT fix anything** — the main agent will coordinate fixes after collecting results

### Step 4: Present Findings

After the sub-agent completes, present findings before fixing anything:
> "Found X issues: [brief list]. Proceeding to fix them."

This gives the user a chance to interject if something is intentional.

### Step 5: Fix All Issues

For reviews with multiple issues, use task tracking to stay organized.

Fix all issues — don't just report them.

### Step 6: Circle Back to Intent

Re-read the stated intent from Step 1. Ask: **Does this output actually accomplish the goal?**

This is a deliberate zoom-out after the detailed checks. It's possible to fix every detail and still miss the point. If the output doesn't accomplish the stated intent, flag what's missing and address it.

### Step 7: Summary

Provide a brief summary:
- What was found and fixed
- Confirmation that the stated intent is met
- Any remaining questions or concerns

If no issues were found, simply confirm the review is complete.

### Commit Message

Run standalone, provide a concise git commit message for the user to use when the review is complete; inside an implement chain, skip this — the calling skill presents the commit at wrap-up, after `test-hardening` and `pre-commit-validation`.

**Important:**
- Run `git status` first to see what files are actually staged/modified
- List the specific files that were changed during this work
- The commit message should reflect only the current uncommitted changes — not work that was already committed earlier in the conversation
- Return commit handling to the calling workflow under live user instructions, including explicit authorization carried across an active multi-task workflow. Review completion alone does not authorize a commit or revoke authorization already granted.

---

## Review Checklist

This is what the sub-agent follows.

**Critical instruction: Re-read every changed file from disk before evaluating.** Do not review from conversation memory. The whole point is fresh eyes on the actual output.

**Spec documents are the source of truth.** When the review is checking implementation against a technical design document, PRD, or other spec, the default assumption is that the spec is correct and the implementation should match it. The spec is the criterion that owns the behavior now: follow any `Superseded by:` line to the later criterion before judging code against an earlier one (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"). If the implementation diverges from the spec:
- The default finding should be **"implementation doesn't match spec"** — flag it as an implementation gap to fix.
- A divergence in code this session did not write is not an implementation gap: report it as an observation. It may be a deliberate change made outside the method. If the session's work depends on it, the main agent applies `implementation-lifecycle`, "When Later Work Changes Earlier Requirements".
- Only recommend a spec update when the divergence was a **deliberate, justified decision** made during implementation (e.g., a third-party API limitation that prevents the spec'd approach, or source data structured differently than the spec described). In that case, clearly label the finding as "spec update needed (justified divergence)" and explain why.
- Never silently update spec documents to match the implementation — that inverts the review's purpose. If a spec update is warranted, resolve it by the calling workflow's Doc Divergence rule (`implement-from-requirements`) — never silently, never over a stakeholder's ruling; run standalone, present the proposed change to the user for approval first.

### 1. Trace Decisions to Output

For each decision listed in the context summary:
- Positive decisions should be captured in the output
- Excluded/deferred items should NOT appear (or should be marked as out of scope)
- Flag anything missing or incorrectly captured

### 2. Check for Omissions

This is the most valuable and most often skipped check. Ask:

- What would a thoughtful engineer expect to see here that isn't there?
- Are there edge cases that should be handled but aren't?
- Are there acceptance criteria (from a ticket/story/PRD, if one exists) that aren't addressed? When checking against a spec, missing acceptance criteria are implementation gaps — do not recommend changing the spec to remove the criteria.
- For code: is there error handling, input validation, or logging that's absent?
- For documents: is there a section or topic a reader would expect that's missing?

Omissions are harder to catch than errors in what's present. Spend real effort here.

### 3. Check for Stale Content

Look for content written earlier in the session that wasn't updated when decisions changed later. Common culprits:
- API response examples
- Code samples or configuration values
- Diagrams or tables
- Section text that references an old approach

### 4. Check for Contradictions

Look for internal inconsistencies — statements that conflict, examples that don't match described behavior, terminology used differently in different places.

### 5. Check Clarity

Read the output as if you weren't part of the conversation. Is anything assuming context that isn't captured?

### 6. Verify Functionality (Code Deliverables)

For code changes:
- Run linter on modified files
- Check for unused imports or missing dependencies
- Confirm existing tests still pass (if applicable)

### 7. Scan for Secrets

Before staging, scan changed and new files for hardcoded secrets. This is a gate — nothing gets staged until this passes.

**How to scan:** Use `git diff` and `git status` to identify which files changed, then search those files for any string that looks like a real credential — API keys, tokens, passwords, connection strings with embedded credentials, private keys, etc. Examples of patterns to search for (not exhaustive):

- Known token prefixes (e.g., `ghp_` for GitHub, `sk_live_` for Stripe, `AKIA` for AWS)
- Variable assignments where names like `token`, `key`, `secret`, `password`, `pwd`, `sql_password`, or `db_password` are set to string literals instead of env var references
- Connection strings with embedded credentials (`Password=...`, `PWD=...`)

The key distinction is **real values vs. placeholders**. `ghp_xxxxx` or `your_api_key_here` are fine. A 32-character hex string or a real-looking password is not.

**If found:** Replace with environment variable references (e.g., `os.getenv("API_KEY")`), document in `.env.example` if one exists, and verify `.env` is in `.gitignore`. Do NOT stage until resolved.

### 8. Check Git Hygiene

Review `git status` for untracked or modified files that would be inappropriate to commit. Do NOT stage anything — just flag concerns for the user. Look for:

- **Binary files or compiled artifacts** — `.pyc`, `.o`, `.dll`, `.exe`, `.class`, compiled binaries, `.whl`, `.egg`
- **Build output and dependencies** — `node_modules/`, `dist/`, `build/`, `__pycache__/`, `.terraform/`, `vendor/`
- **IDE and OS files** — `.idea/`, `.vscode/settings.json`, `.DS_Store`, `Thumbs.db`
- **`.env` files** — these are NOT automatically inappropriate. Many projects intentionally commit `.env` files containing non-secret configuration (URLs, feature flags, environment names) to reduce onboarding friction, with secrets kept in separate files (e.g., `.env.secrets`) or injected at runtime. Do not flag `.env` files just for existing — only flag them if the secrets scan (item 7) finds actual credentials in them
- **Large or generated files** — database dumps, log files, media assets that belong in external storage
- **Missing `.gitignore` entries** — if any of the above exist and aren't already in `.gitignore`, recommend adding them

This is an advisory check. Report what you find and let the user decide what to do about it.

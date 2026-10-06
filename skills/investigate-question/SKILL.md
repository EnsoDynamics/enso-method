---
name: investigate-question
description: Thorough deep-dive investigation of a single question — read code, query data, test APIs, and explore to answer the question or significantly refine a proposed answer with updated confidence.
user-invocable: true
---

# Investigate Question

Investigate one specific question in depth — reading code, querying databases, testing APIs, analyzing data — to either answer it definitively or significantly refine a proposed answer with an updated confidence level.

This is the depth-first complement to breadth-first processes like the Implementation Readiness Check. The readiness check does a reasonable scan across many questions; this skill goes deep on one.

---

## When to Use

Use this skill when:

- A question from an `implementation-readiness-check` needs deeper investigation before the human can decide
- You encounter a question mid-conversation that could be answered with some digging rather than asking the human
- You need to verify a data assumption (what values exist, are there nulls, what's the distribution)
- You need to understand how existing code actually behaves (not just what the docs say)
- You need to confirm what an API actually returns vs. what you expect

**Do NOT use this skill when:**

- A quick glance at the code or docs would answer the question — just look
- The question is purely a business decision that no amount of technical investigation can resolve
- You're doing a broad discovery pass across many questions — use `implementation-readiness-check` for that

---

## Required Inputs

At minimum:

1. **The question** — what you're trying to answer
2. **Context** — enough background to understand why this question matters

Optionally (carry forward from `implementation-readiness-check` if that's where this originated):

3. **Classification** — Technical or Business
4. **Current proposed answer** and **confidence** (0–100%)
5. **Impact if wrong** — 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
6. **What's already been checked** — to avoid re-doing work from a prior breadth-first pass

---

## Process

### 1. Understand the Question

Before diving in, determine what would constitute an answer. What specific fact, behavior, or data point would resolve this?

**Set expectations based on the question's nature:**

- **Technical questions** (how does this code behave, what does this API return, what's in the data) can potentially be **fully resolved** through investigation. The goal is to get to 100% confidence if possible.
- **Business questions** (what should the system do, what's the intended behavior, what's the business rule) have a ceiling. You can gather evidence and raise confidence significantly, but only a stakeholder can confirm business intent. If a business question can't be confirmed in the current conversation, it would need to be captured as a stated assumption via `assumptions-document-writing` (though that's a separate step the user would initiate, not something this skill does directly).

### 2. Investigate

Identify the most promising avenues and **start with the one most likely to give a definitive answer**. Don't pursue all of them if the first one resolves it.

Common approaches:

- **Read code in depth**: Trace the full flow, not just the function signature. Check the tests — they often document edge case behavior more explicitly than the code itself.
- **Query the data**: Check data characteristics — what values exist, are there nulls, what's the distribution, how many records match a condition.
- **Test an API**: Make a test call to the sandbox environment to see what actually comes back.
- **Check external system behavior**: Look at actual records in sandbox environments (third-party APIs, vendor platforms, etc.) to see how the system represents things in practice.
- **Search documentation**: Check READMEs, API specs, config files, inline comments.
- **Check git history**: `git log` or `git blame` can reveal why something works the way it does.

If you need to write scripts, query databases, or connect to external systems, follow the exploration scripts, credential discovery, and environment safety guidance below.

**Know when to stop.** The goal is to meaningfully raise confidence, not necessarily to reach 99%. If you've tried two or three promising avenues and confidence has moved from 55% to 80%, that's a useful result — report it. Don't spiral down rabbit holes chasing a definitive answer when a well-informed proposed answer with solid evidence is good enough for the human to decide.

If investigation is genuinely stuck (each avenue leads to more questions), step back and report what you've learned so far. A partial result with clear evidence is more valuable than exhaustive but inconclusive digging.

**If investigation changes the question itself**, report that. Sometimes digging reveals the original question was the wrong question — e.g., "does the API paginate results?" becomes "the API was replaced with a webhook model 3 months ago." When this happens, report what you actually found, reframe the question, and let the human decide how to proceed.

### 3. Report Findings

Structure your output so it's immediately usable — whether the human is reading it directly or it's being folded back into a readiness check conversation.

**Output format:**

> **Question**: [The original question — or reframed question if investigation changed it]
> **Classification**: [Technical / Business]
>
> **Answer**: [Your answer or refined proposed answer based on investigation]
>
> **Confidence**: [Starting confidence] → [Updated confidence]
> **Impact if Wrong**: [🔴/🟡/🟢 LEVEL]
>
> **Evidence**:
> - [Specific finding — the code path, query result, API response, or document that supports this]
> - [Additional findings if applicable]
>
> **What was checked**: [Brief list of avenues explored]
>
> **Verdict**: [One of the following]
> - **Resolved** — investigation definitively answered this question (typically Technical questions where you confirmed the behavior through code, data, or API)
> - **Refined** — confidence raised, still needs human input (typically Business questions where evidence supports the proposed answer but stakeholder confirmation is needed; if this can't be confirmed in the current conversation, it would need to be captured as a stated assumption)
> - **Blocked** — could not investigate fully (include remediation block below)
> - **Reframed** — investigation revealed the original question was wrong; see revised question above

If blocked, include a clear remediation block:

> **⚠️ Investigation Blocked**: I attempted to investigate [question] but [specific blocker]. If you:
> - [Specific remediation step]
> - [Specific remediation step]
>
> I can [what becomes possible if unblocked].

---

## Exploration Scripts

When investigation requires code (querying a database, testing an API, etc.), create scripts to do the work.

**Where to put scripts:**

- **`scripts/exploration/`** (at project root) — for scripts that might be useful later. Add a header comment explaining the script's purpose. These get committed to git.
- **`/tmp/`** — for truly one-off throwaway scripts with no future value.

When in doubt, use `scripts/exploration/`. Keep scripts simple and focused — one script per question, no reusable utilities.

---

## Credential Discovery

Before asking the user for credentials, scan the codebase to self-discover:

1. **Check for related skills** — Look for installed skills that document credentials and connection setup (e.g., a cloud-credentials skill or a database-exploration skill).
2. **Check README files** — Often contain profile names, connection info, or pointers to credential storage.
3. **Check existing config and code** — `config.py`, `.env.example`, connection string patterns, how existing scripts and tests connect.

Only after scanning should you ask the user for help. Be specific about what you tried and what's missing.

---

## Environment Safety Rules

1. **Dev and sandbox first; never write to production** — read production only read-only, only when nothing else can answer the question, and only where the project allows it (`engineering-principles`, "Production Data"). If unsure which environment credentials point to, treat it as production.
2. **Read-only operations only** — SELECT, GET, list/describe/read. Never modify state.
3. **Limit result sets** — Use TOP/LIMIT clauses. Don't pull entire tables when 100 rows would answer the question.

---

## Examples

### Example 1: Technical Question — Fully Resolved

> **Question**: Do all user accounts have a valid team assignment, or are there orphaned accounts with no team?
> **Classification**: Technical
>
> **Answer**: All users have valid team assignments. Confirmed via data query (0 orphaned records), schema constraints (NOT NULL + FK), and application-layer validation on create.
>
> **Confidence**: 60% → 99%
> **Impact if Wrong**: 🟡 MEDIUM — orphaned accounts would break team-based permission checks
>
> **Evidence**:
> - Data query: `SELECT COUNT(*) FROM users u LEFT JOIN teams t ON u.team_id = t.id WHERE t.id IS NULL` → 0 rows
> - Schema: `team_id` is NOT NULL with FK constraint to `teams.id`
> - Code: `UserService.create()` validates team existence before insert
>
> **What was checked**: Queried users table, inspected schema constraints, traced UserService.create() flow
>
> **Verdict**: Resolved — investigation definitively answered this question.

### Example 2: Business Question — Refined but Not Resolved

> **Question**: When a document has been approved by some but not all of its required reviewers, should it be treated as "in_review" (which triggers downstream notifications) or stay "pending" until every approval is in?
> **Classification**: Business
>
> **Answer**: Treat it as "in_review" from the first approval — the current code and a test fixture both do this and nothing contradicts it, but neither states the intended rule.
>
> **Confidence**: 45% → 80%
> **Impact if Wrong**: 🔴 HIGH — status mapping drives downstream notification logic
>
> **Evidence**:
> - Test fixture `test/fixtures/documents.json`: document with 2/3 approvals has status `in_review`
> - Code comment in `sync_documents.py` (8 months old): "documents stay 'pending' until the first approval, then go to 'in_review'"
> - No contradictory evidence found
>
> **What was checked**: Searched codebase for partial approval references, reviewed DocumentStatusMapper, checked test fixtures, attempted the workflow service's admin CLI (not configured)
>
> ⚠️ **Partially Blocked**: Could not verify against live sandbox data — the workflow service's admin CLI is not configured in this environment. If you configure the CLI, I can query actual document records to confirm this definitively.
>
> **Verdict**: Refined — confidence raised from 45% to 80%, but this is 🔴 HIGH impact and below 95%, so unless the human confirms it in this conversation it becomes a stated assumption (`assumptions-document-writing`) and work proceeds on it.

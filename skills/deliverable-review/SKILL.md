---
name: deliverable-review
description: Verify completed work accomplishes what was intended — fresh-eyes sub-agent re-reads output files, traces requirements, checks for gaps and omissions, and reports findings rated High, Medium or Low for the main agent to fix; supports cheaper delta rounds when a caller reviews the same work repeatedly.
---

# Deliverable Review

Verify that completed work accomplishes what was intended, and fix any issues found.

A sub-agent with a fresh context window re-reads the actual output files — avoiding the bias of the agent that produced the work reviewing it from memory. The main agent orchestrates, then fixes whatever the sub-agent finds.

In the standard implementation chain this is the second step (`implement-from-requirements` → `deliverable-review` → `test-hardening`): this skill verifies the deliverable matches intent, then `test-hardening` verifies the tests prove the requirements. (The chain then commits the feature work, runs `refactor-pass`, and pushes a feature branch.)

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
4. Note the deliverable type (code, documentation, configuration, visual, mixed). Visual means anything a person looks at rather than reads as text: mockups, prototypes, diagrams, rendered pages, generated images. For each one, note whether it is the product itself or a design reference (Review Checklist, "Look at Visual Deliverables"), how to render it (the file to open; for the product, the screen sizes its spec names; for a design reference, the width its main users work at), and what rendering tools the machine has
5. Note any facts the session established with high confidence that contradict the material it started from (a handoff's mockups, sample data, an earlier draft), so the reviewer can check the deliverable against the facts rather than against that material

### Step 3: Launch Sub-Agent

Launch a single general-purpose sub-agent with:

- The stated intent from Step 1
- The context summary from Step 2
- The list of changed files
- Instruction to read this skill's `SKILL.md` — pass the absolute path of the file this skill was loaded from — and follow the **Review Checklist** section
- **Instruction to re-read every changed file from disk** — do not rely on conversation memory
- **For a visual deliverable, instruction to render it and look at the result** (Review Checklist, "Look at Visual Deliverables") — reading its source does not count. When it has more screens and sizes than one reviewer can look at with care (as a rule of thumb, more than about 20 images), launch one more sub-agent per group of screens, in parallel, for that item alone, and merge their findings with the main review's
- **When the same part of the work has produced a Medium or High finding in two rounds running, instruction to walk that part's cases** before reporting: list how it can be entered, the states it can be in and the inputs it takes, and name for each combination that matters the sentence that settles it. Reading for problems finds one edge case per round; a case walk finds the rest together
- **For a delta round** ("Delta Rounds", below), the previous round's findings with their severities, what was changed for each or, for a rejected finding, the reason, and the diff since that round
- **Report all findings as a structured list,** each with its severity (Review Checklist, "Rate Each Finding"), where it is, and the one sentence that names its consequence. **Do NOT fix anything** — the main agent will coordinate fixes after collecting results

### Step 4: Present Findings

After the sub-agent completes, present findings before fixing anything:
> "Found X issues: [brief list]. Proceeding to fix them."

This gives the user a chance to interject if something is intentional.

### Step 5: Fix All Issues

For reviews with multiple issues, use task tracking to stay organized.

Fix all issues — don't just report them.

- **A finding against a mockup or other visual is fixed in the visual,** regenerated in its own medium (`prd-writing-standards`, "Mockups Show What the Criteria Require"), never by a note describing what is wrong.
- **Carry each fix to every copy.** A finding names one place, but the same term, figure, name or rule is often repeated: in a summary, a table, a list, an example, a note, a mockup's text, a test fixture, a comment, a document beside this one. After fixing, search the whole deliverable and the documents that repeat it for each thing the fix changed, and update every copy. A fix that lands in one place and leaves a stale copy elsewhere is the next round's finding.
- **A fix is new content.** Before the next round, check each sentence or line a fix adds against the requirements, code or screens it touches. A fix that contradicts a neighbouring requirement becomes the next round's finding.

### Step 6: Circle Back to Intent

Re-read the stated intent from Step 1. Ask: **Does this output actually accomplish the goal?**

This is a deliberate zoom-out after the detailed checks. It's possible to fix every detail and still miss the point. If the output doesn't accomplish the stated intent, flag what's missing and address it.

### Step 7: Summary

Provide a brief summary:
- What was found and fixed
- Confirmation that the stated intent is met
- Any remaining questions or concerns

If no issues were found, simply confirm the review is complete.

### Delta Rounds (Optional)

A caller that reviews the same deliverable round after round, fixing between rounds, can ask for a **delta round** instead of a full one. A full round reads everything fresh. A delta round checks that the last round's fixes landed and broke nothing, for a fraction of the cost.

The caller passes, beyond Step 2's context, the previous round's findings with their severities, what was changed for each or, for a rejected finding, the reason, and the diff since that round. The reviewer, in a delta round:

- confirms each previous finding is fixed, and fixed everywhere its subject appears, or was rejected with a reason that holds
- reviews the changed content in full, and everything that shares a term, figure, name or rule with it (for code: its callers, what it calls and the tests that exercise it); where a change alters a rule, it walks the cases that rule governs
- renders only the visuals the fixes affected ("Look at Visual Deliverables")
- does not re-read unchanged material in full
- rates and reports new findings as in a full round

A delta round sees only what the fixes touched, so it cannot show that the deliverable is clean. A caller that loops on this review ends on a full round.

### Commit Message

Run standalone, provide a concise git commit message for the user to use when the review is complete; inside an implement chain, skip this — the calling skill handles the commit at wrap-up, after `test-hardening` and `pre-commit-validation`.

**Important:**
- Run `git status` first to see what files are actually staged/modified
- List the specific files that were changed during this work
- The commit message should reflect only the current uncommitted changes — not work that was already committed earlier in the conversation
- Return commit handling to the calling workflow, which commits by its own default (`pre-commit-validation`, "Who Commits") or under live user instructions, including explicit authorization carried across an active multi-task workflow. Review completion alone does not authorize a commit or revoke authorization already granted.

---

## Review Checklist

This is what the sub-agent follows.

**Critical instruction: Re-read every changed file from disk before evaluating.** Do not review from conversation memory. The whole point is fresh eyes on the actual output.

**Spec documents are the source of truth.** When the review is checking implementation against a technical design document, PRD, or other spec, the default assumption is that the spec is correct and the implementation should match it. The spec is the criterion that owns the behavior now: follow any `Superseded by:` line to the later criterion before judging code against an earlier one (`implementation-lifecycle`, "When Later Work Changes Earlier Requirements"). If the implementation diverges from the spec:
- The default finding should be **"implementation doesn't match spec"** — flag it as an implementation gap to fix.
- A divergence in code this session did not write is not an implementation gap: report it as an observation. It may be a deliberate change made outside the method. If the session's work depends on it, the main agent applies `implementation-lifecycle`, "When Later Work Changes Earlier Requirements".
- Only recommend a spec update when the divergence was a **deliberate, justified decision** made during implementation (e.g., a third-party API limitation that prevents the spec'd approach, or source data structured differently than the spec described). In that case, clearly label the finding as "spec update needed (justified divergence)" and explain why.
- Never silently update spec documents to match the implementation — that inverts the review's purpose. If a spec update is warranted, resolve it by the calling workflow's Doc Divergence rule (`implement-from-requirements`) — never silently, never over a stakeholder's ruling; run standalone, present the proposed change to the user for approval first.

**Mockups and inherited material are references, not truth.** Mockups, prototypes, sample data, and anything inherited from a handoff or an earlier draft show what someone intended when they were made. When the work has since established a fact with high confidence that contradicts them (a production record, a measured figure, a stakeholder's ruling, the written requirement itself), the finding is that the reference must change, not that the work should follow it. A mockup the work produced is corrected to match. Material from a handoff package is never edited: it stays as received, in its own labelled location apart from the work (`prd-writing-standards`, "Mockups Show What the Criteria Require"), and the work notes where it departs from it. A handoff original sitting where it could pass for the work's own requirements is a finding. A reference that contradicts a stakeholder's ruling is raised, not quietly changed in either direction.

**In a delta round** ("Delta Rounds", above), apply the items below to the scope that section sets, not to the whole deliverable.

### Rate Each Finding

Give every finding a severity, by what happens if the deliverable is used as it stands. Rate the consequence, never the effort of the fix: a one-word fix can be High, and a long rewrite Low. Write the consequence as one sentence; the level whose test that sentence meets is the rating, and when it meets two, the higher.

| Severity | The test | Typical findings |
|---|---|---|
| **High** | Following the deliverable as written gives a wrong result that is costly or hard to undo | a wrong behavior, money, data, safety or legal outcome; two passages that disagree where building either one would be costly to undo; a missing requirement the stated intent needs; a broken build or failing tests; a security hole |
| **Medium** | A competent builder, maintainer or reader following it literally would build or decide something other than what was intended, or would have to stop and ask | an ambiguity with two plausible readings; an unstated case on a path users reach in normal operation, that no stated rule settles; two passages that disagree with no way to tell which governs; a stale passage in governing text that contradicts current behavior |
| **Low** | A reader would still get it right | wording; formatting; bookkeeping; redundancy. Layout polish of a design reference, and how its states link to each other, are not reported at all ("Look at Visual Deliverables") |

**Governing text** is what a builder or reader acts on for a behavior: a requirement, a rule, a contract, the code that runs. **Bookkeeping** is text that records or points at governing text rather than stating it: indexes, lists of what a section covers, trace tables, cross-reference lists, counts, change notes, dates and status lines. A pointer a reader follows to find the governing text, such as a line naming the requirement that replaced this one, is not bookkeeping: rate it by where it sends the reader. When bookkeeping disagrees with governing text that is itself correct, a reader who follows the governing text still gets it right.

Calibrating the edges:

- **An edge case** reachable only through an unlikely combination of events, with a contained outcome (an error the user sees and retries, a question someone asks), is Low, unless it touches money, safety, data loss or legal exposure; then rate that outcome.
- **A fix that missed a copy** takes the severity of where the stale copy sits: in governing text, Medium or higher; in an index, a note, or a summary that only points at governing text, Low. A summary that restates a rule is stating it.
- **Sample data** in a mockup or example that contradicts established facts is Low, unless a reader would build, configure or confirm the wrong thing from it; then Medium.
- **A case a stated rule already settles** is Low at most, even on a normal path: when applying a rule the deliverable states gives the answer, its not being spelled out for that case leaves a reader nothing to stop and ask. It is Medium only when no stated rule applies, or two stated rules give different answers. Asking for every consequence of a rule to be written out grows a document clause by clause without making it more correct.
- **Readability of a document a person signs off** (a PRD, its assumptions, a design a stakeholder approves): a requirement buried under clauses, so that a reader can no longer say what is being checked, is Medium, because the sign-off it exists for will approve what nobody could read. Length alone is Low. The fix is a rewrite, a split or a table (`prd-writing-standards`, "Keep Criteria Readable as Cases Are Added"), never another clause.

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

Read the output as if you weren't part of the conversation. Is anything assuming context that isn't captured? For a document a person signs off, can that person read each requirement once and say what it checks?

### 6. Look at Visual Deliverables

A mockup, prototype, diagram, rendered page or generated image is reviewed by looking at it the way its audience will: rendered, as images you open and inspect. Its source (HTML, the data a page draws its screens from, SVG markup, a description of it) can show what it says, but never what it looks like. Reading the source is not a review of a visual deliverable, and a review that only read it must say so.

**First decide what the visual is for;** that sets how much looking it needs.

- **The product itself:** a built page or app screen, a published site, a report or image that ships. Its layout is part of what is delivered, so render every screen or state at each screen size its spec names, or at least the smallest and the largest it must support.
- **A design reference:** a mockup or prototype in a requirements document, a diagram in a design. It shows what is to be built, and the built product gets a review of its own. Render each screen or state once, at the width its main users work at, and review what it says against the criteria. Report its layout only where that makes content unreadable or misleading: a value cut off, one element hiding another, something the criteria require missing from the screen. Alignment, spacing and how it reflows at other sizes are left to the built product's review, and so are the links between its states: they are a convenience for stepping through, not part of what is specified. The screen sizes a requirements document names are requirements on the product, not on its mockups.

Then, for either kind:

- **Check the layout by script first, then look.** A short script over every state, at the sizes chosen above, can find what is measurable, such as text running past its box, elements off the screen and sideways scrolling, so the looking can go to what only a person sees.
- **Render as decided above.** Use a browser that can emulate a device for phone widths; a plain window-size setting can clip the right edge and fake a defect.
- **In a delta round, render only what the fixes affected:** the visuals whose content changed (when many come from one generator, compare each one's data or render, not the generator), and those that show a term, figure or rule a fix changed. A full round renders everything again.
- **Look at each image** for what a viewer would notice: text clipped, overlapping or running off the screen; type too small to read; for the product, a layout that breaks at a narrow width; something the spec requires that isn't on screen; screens that disagree with each other or with the spec; sample data that contradicts the facts the work established ("Mockups and inherited material are references, not truth", above).
- **Confirm a suspected visual defect** with a second rendering before reporting it (with another method, or, for the product, at another width); screenshot tools have artifacts of their own.
- **Look at one screen at a time, and write down what it shows before opening the next.** Keep a running notes file of findings per screen and size; a reviewer holding dozens of images in mind at once misses what it saw early and conflates screens. Split a tall screen into pieces that can be read at full size.
- **Report what was viewed:** which screens, at which sizes. If something could not be rendered, report that as a finding rather than review it from source.

### 7. Verify Functionality (Code Deliverables)

For code changes:
- Run linter on modified files
- Check for unused imports or missing dependencies
- Confirm existing tests still pass (if applicable)

### 8. Scan for Secrets

Before staging, scan changed and new files for hardcoded secrets. This is a gate — nothing gets staged until this passes.

**How to scan:** Use `git diff` and `git status` to identify which files changed, then search those files for any string that looks like a real credential — API keys, tokens, passwords, connection strings with embedded credentials, private keys, etc. Examples of patterns to search for (not exhaustive):

- Known token prefixes (e.g., `ghp_` for GitHub, `sk_live_` for Stripe, `AKIA` for AWS)
- Variable assignments where names like `token`, `key`, `secret`, `password`, `pwd`, `sql_password`, or `db_password` are set to string literals instead of env var references
- Connection strings with embedded credentials (`Password=...`, `PWD=...`)

The key distinction is **real values vs. placeholders**. `ghp_xxxxx` or `your_api_key_here` are fine. A 32-character hex string or a real-looking password is not.

**If found:** Replace with environment variable references (e.g., `os.getenv("API_KEY")`), document in `.env.example` if one exists, and verify `.env` is in `.gitignore`. Do NOT stage until resolved.

### 9. Check Git Hygiene

Review `git status` for untracked or modified files that would be inappropriate to commit. Do NOT stage anything — just flag concerns for the user. Look for:

- **Binary files or compiled artifacts** — `.pyc`, `.o`, `.dll`, `.exe`, `.class`, compiled binaries, `.whl`, `.egg`
- **Build output and dependencies** — `node_modules/`, `dist/`, `build/`, `__pycache__/`, `.terraform/`, `vendor/`
- **IDE and OS files** — `.idea/`, `.vscode/settings.json`, `.DS_Store`, `Thumbs.db`
- **`.env` files** — these are NOT automatically inappropriate. Many projects intentionally commit `.env` files containing non-secret configuration (URLs, feature flags, environment names) to reduce onboarding friction, with secrets kept in separate files (e.g., `.env.secrets`) or injected at runtime. Do not flag `.env` files just for existing — only flag them if the secrets scan (item 8) finds actual credentials in them
- **Large or generated files** — database dumps, log files, media assets that belong in external storage
- **Missing `.gitignore` entries** — if any of the above exist and aren't already in `.gitignore`, recommend adding them

This is an advisory check. Report what you find and let the user decide what to do about it.

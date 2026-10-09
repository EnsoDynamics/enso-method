---
name: continuation-prompt
description: "Produce the copy-paste prompt that starts the next chat. Line one is a short chat name; then the lineage block (the PRD and phase this chat serves, or an honest \"no lineage found\"); then the skill to use, the goal, where to work, pointers into the governing documents, and the single first action. Before writing the prompt it moves every fact the repo should own out of the prompt and into the governing document, so the prompt stays a pointer. Use whenever the user asks for \"a prompt for a new chat\", \"the prompt to continue this\", \"hand this off to a fresh session\", or when any skill reaches the point of handing work to a fresh chat (phase-split, implement-from-requirements wrap-up). NOT for a \"context package\", or anything that passes information back to a chat that is already running. Re-run it to regenerate a prompt that came out wrong. At the end of a track it produces no prompt and says so. Ships a UserPromptSubmit hook that turns that first line into the session title."
user-invocable: true
---

# Continuation Prompt

The last thing most working sessions do is hand the next session a prompt. This skill owns that prompt: what goes in it, what must be written somewhere durable instead, how the chat gets named, and when the prompt is actually safe to paste.

Three problems it exists to fix:

1. **Chat names.** Someone running a dozen chats finds them by tab title, and a tab shows roughly the first twenty characters. Auto-generated titles are summaries of the first prompt: too long, and they open with a generic verb. The name has to be short, its leftmost characters have to be the most distinguishing ones, and it has to be the very first characters of the prompt: the VS Code extension labels a new tab with the raw start of the first prompt until it picks up a title, so a prefix like `Chat:` there wastes the only real estate that matters.
2. **Prompts that carry facts the docs should own.** A continuation prompt drifts into a second requirements document: measured numbers, lessons learned, decisions, what a predecessor left behind. That content lives in the chat, goes stale, and the next session starts from the prompt instead of the docs. The fix is to write those facts into the governing document first and let the prompt point at them.
3. **Chats that cannot say what they are for.** A phase session finds a defect and hands off a chat to fix it; that chat finds another and hands off again; four hour-long chats later, none can name which acceptance criterion of which phase the work unblocks, and the ids they do carry (`2a1`, `3b2`) mean nothing without opening the phase doc. The fix is a fixed lineage block at the top of every prompt — PRD and phase by full title, and what this chat does for them — that doubles as a gate: a chat that cannot fill it honestly does not get a prompt (`implementation-lifecycle`, "Every Session Names What It Serves").

---

## When to Use

- The user asks for a prompt to paste into a **new** chat, in any wording that means starting a fresh session.
- A skill hands work to a fresh chat: `phase-split` after writing phase docs when the user invoked it directly (called from an implement session it produces no prompt — that session builds the first leaf, and its wrap-up produces the next one), `implement-from-requirements` at wrap-up when a next phase exists, `test-audit` when its remediation outlasts the chat.
- A prompt already given was wrong (bad name, too long, stale) and the user wants it regenerated. Re-run the whole skill; if only the name was wrong, only the name changes.
- A skill or the user invokes it at the **end of a track** — the unit just finished has no successor in its own chain. That is a legitimate invocation, and its correct output is a statement that the track is complete and **no prompt**. See the gate below.

### Not this skill: a context package

A **context package** is a message from this chat to another chat that is *already running*, carrying what that chat needs to know: file paths of anything downloaded or written, results, caveats, decisions made here. The user asks for it as "a context package", "give me something to paste back to Claude / Codex", "let the other chat know", "a summary for the other session". The tells are *back to* and *the other chat*: the recipient exists and has its own goal, so nothing in this skill applies — no chat name, no lineage block, no first action, no "does a next unit exist" gate, and no moving facts into the governing documents first (the receiving chat owns that decision). Write it directly as a plain briefing: what was done, the artifacts and their absolute paths, what is still open, and any caveat the other chat must carry. Nothing else.

**Measured failure this exists to stop:** a user asked for "a single context package that I can copy-paste back to Claude to let it know," listing the downloaded file paths. The session matched *hand this off* and loaded this skill, started composing a continuation prompt with a chat name and lineage block, and had to be stopped and corrected. A continuation prompt starts work; a context package informs work already in progress. When the ask could be read either way, the word *new* or *fresh* decides it — absent, it is a context package.

---

## Before Step 1: Confirm a Next Unit Exists in This Track, and Name What It Serves

This skill continues a track. It does not choose one. Before drafting anything, answer one question from the governing document: **is there a next unit of work in the chain the finished unit belongs to?** The chain is the one that document defines — the next phase or sub-phase of the same PRD, change, or phase plan that is not yet closed, in the order the document states. A test audit's governing document is its `test-audit.md` and its chain is that file's To fix list (`test-audit`): a next unit exists while its Status line still lists criteria to fix.

- **If there is, continue.** That unit is the prompt's subject and every step below applies to it.
- **If there is not — the unit just finished was the last in its track — produce no prompt.** Say the track is complete, name what closed it (date and commit hashes), and stop. That is this skill's correct output at the end of a track, not a failure to run it.

What the second case forbids, and why. When a track ends, the next thing to work on is a choice the user makes deliberately, not one this skill infers. It is not the next entry in some plan's suggested order, not a sibling track that looks related, and not whatever a search of the repository turns up as unfinished. **Measured failure this exists to stop:** a session closed the last sub-phase of one track, went looking for "the most logical thing next", and handed the user a prompt for a sub-phase of a *different* track — one the user already had running in another chat. The prompt was well-formed, pointed at real documents, and was wrong in the only way that mattered: nobody had asked for it. Someone running a dozen chats has usually already assigned the other tracks; a cross-track prompt silently reassigns work, and a chat named for a track it did not finish misleads every later reader of the tab strip.

The one exception is an explicit ask. If the user names what to continue with — a different track, a change directory, a ticket — that is a request, not an inference, and the skill runs normally for it. What it never does is supply the choice itself.

**A PRD roadmap is not a track.** When the last phase of a PRD that came from a PRD roadmap (`prd-roadmap`) closes, the roadmap's next planned PRD is not the next unit of that track. Moving on to it is a decision the user makes after the finished PRD reaches production, and the roadmap may be reordered by then. Say the PRD is complete, name the roadmap's next planned PRD in one line, and write no prompt unless asked.

The calling skills already agree: `implement-from-requirements` invokes this skill "when a next phase exists", `phase-split`, when invoked directly, for the first leaf it just wrote, and `prd-roadmap` for the first planned PRD of the roadmap it just wrote. If a caller invokes it and the answer to the question above is no, the caller's premise was wrong, and the right output is still no prompt.

### The lineage gate

The second question, asked of the unit the prompt is for: **what does it serve, and can I say so without inventing anything?** Fill the lineage block from Step 3 now, from the documents, before drafting anything else. The block has three lines and every line is checkable:

1. The PRD, by the full title in its H1 (`Order Notifications`), never the directory slug or the chat-name abbreviation.
2. The phase, by its id **and** the full title from the phase doc's H1 (`Phase 2a1 — Delivery receipts from the SMS provider`). For a leaf below a split parent, the leaf's own title; a positional id already carries the ancestry. An unsplit PRD has no phase: line 2 reads `whole PRD, not split`. A test audit of a whole split PRD reads `whole PRD, all phases`.
3. What this chat does for them, in one line: `implements it`, or `fixes <the thing> that blocks AC-DLV-04 of it`. A fix names the acceptance criterion it unblocks — the label, from the phase doc's "Acceptance criteria covered" — not a symptom. Chats that do not build use their activity's verb: `refines its requirements`, `splits it into phases`, `drafts its technical design`, `investigates <x> for it`, `reviews it`.

The shapes that legitimately have no PRD phase are listed in `implementation-lifecycle` ("Every Session Names What It Serves"): ticket-tracked work, a declared ops thread with a session file, a component defect reported from outside, requirements work on the PRD itself, methodology work. Each puts its own lineage on line 1 in place of the PRD, and `no phase — <shape>` on line 2; Step 3 item 2 shows the rendered block. One variant: writing a planned PRD from a PRD roadmap, where the PRD does not exist yet, puts the roadmap's full title on line 1 and the planned PRD on line 2 — `In service of: Acme Cloud PRD Roadmap` / `Cloud Ingestion — planned PRD, first in the roadmap` / `This chat: writes its PRD.`

**When the block cannot be filled honestly, there is no prompt.** The case this catches is a chat that would implement or fix something, and the only true lineage is *this chat*: the fix was found here, it unblocks no acceptance criterion anyone can name, it has no ticket id, no incident, no session file. That is a discovery that was about to be promoted into work by being handed a chat of its own, and it goes back through the Materiality Gate and the disposition table in `implementation-lifecycle` instead, under the same 90% ask-gate as everything else: **dismiss is the default**; a genuinely valuable item files into the phase doc that will build it; and only work outside the current PRD that the user may want is named — in the wrap-up, as the user's decision with a recommendation ("found X while closing Phase 2a1; it blocks nothing in the plan; recommend dismissing"), never as a mid-session stop. The user may then ask for the prompt anyway, and that is an explicit ask: write it, with the whole block in its honest form —

```
In service of: no lineage found
  no phase — spawned from <this chat's name>
  This chat: <the fix>; unblocks nothing named; run at the user's direction
```

— lines 1 and 2 included. Filling them with the spawning chat's PRD and phase is the fabrication the gate forbids: that chat's lineage is not this fix's. The fixed head `no lineage found` is the greppable marker, in prompts and in commit messages alike. What the skill never does is write a plausible purpose to fill the block. A lineage line that reads well and points at nothing is worse than an honest orphan, because it hides the one fact the block exists to expose.

**Filing the orphan as a ticket is not a way around the gate.** A ticket id counts as lineage because someone other than this session raised it. Opening a Jira ticket, a GitHub issue, or an entry in any other tracker for this session's own discovery, then writing the prompt with that id as its lineage, is the same orphan now wearing an id. A minted id makes work findable, not needed.

---

## Step 1: Move Repo Truth Into the Docs

Draft the prompt in your head, then sort every sentence into one of three bins. This is the step that keeps the prompt short and the docs current, and it is done **before** the prompt is written, not after.

| Bin | What belongs here | Where it goes |
|-----|-------------------|---------------|
| **Repo truth** | State of the work: what is closed and when, what is owed, measured facts and their dates, decisions and why, hazards the next implementer inherits, what not to re-derive, a predecessor's findings | The governing document, per `implementation-lifecycle`: the phase doc carries work state (a landed leaf gets its `**Closed:** YYYY-MM-DD` line under the title, per `phase-split`), the Technical Design carries durable design facts, the assumptions doc carries business-logic calls, and a test audit's state lives in its `test-audit.md`. Write it there now. |
| **Machine and session truth** | Which checkout or worktree to use and which to avoid, the branch to stay on, a local venv or interpreter quirk, a checkout that carries someone else's untracked files | The prompt. This is true of one machine on one day and does not belong in a repo document. |
| **Pointers** | Paths and section headings for everything in the first bin | The prompt. |

The test for the first bin: **if a future reader of the docs would need this sentence, it is in the wrong place.** A paragraph headed "four things the predecessor recorded as yours" is a phase-doc section wearing a prompt's clothes. Write the section, then point at it. The one exception is work with no future reader at all — see the one-shot exception below.

Two disciplines carry over from `implementation-lifecycle`:

- The Materiality Gate has no back door. An observation that was dismissed during the session does not reappear in the prompt as a "heads up." If it mattered it was filed; if it was filed the prompt points at the file.
- Writing the docs is work, not a note. The doc edits go into the commit this session is already proposing (see Step 5). Do not present a prompt whose facts exist only in an uncommitted file or in the chat, unless the one-shot exception below applies.

When there is no governing document at all (an ad-hoc investigation, a stakeholder thread), the durable home is a session notes file in the repo — or, for a code change the user has decided to do next, the change directory the user opens for it (`prd-writing-standards`), which the prompt then points at. Create one whenever anything downstream will inherit the facts; a prompt is not a durable record.

**The one-shot exception.** The first bin's test assumes the work has a future reader. Some work has none: the task completes within the session it is handed to, and nothing inherits what it found. For that work the measured facts are scaffolding, not findings. A document written to hold them is stale on arrival, and someone later has to notice it and delete it. The prompt is the record, and it carries the facts itself. This applies only when all three hold:

- No governing document exists for the work — no PRD, no phase document, no change directory, no session notes file. If one exists, the findings go there. Phase work can never qualify, because phase work has a governing document by definition.
- The task completes within the session that receives the prompt. If that session finds mid-flight that it cannot complete, it writes the facts into a durable home before handing off; the exception covers work that finishes, not work that turns out to be longer than it looked.
- Nothing downstream inherits its findings: no later session, document, or reader.

When the user says to pass the context in the prompt rather than write a document, that is a request, not an inference: do it, and do not create a document to satisfy this step. An explicit instruction wins even where a governing document exists, and it is the only thing that overrides the first condition above. Pointers still beat restatement wherever a durable document already carries a fact; the exception admits facts the docs will never hold, not paraphrases of facts they already do.

---

## Step 2: Name the Chat

The name is the first line of the prompt and the argument to the tool's rename command. Every name has the same shape: the unit of work (its id, plus a subject noun when the id alone is not recognisable), the project tag when the work has one, the product tag only when the directory holds more than one product, and the activity token. Rules, in priority order:

1. **Twenty characters is the target for everything before the activity token; thirty is the cap on the whole name.** Count them. A tab strip shows roughly the first twenty, and the token is the part allowed to fall past them.
2. **Order tokens by how much they distinguish this chat from the others likely open at the same time.** The specific unit of work comes first: the phase or sub-phase id, the issue or ticket id, the thread's subject noun. The project tag comes after, because every sibling chat shares it. When six tabs are all Phase 2 of one project, a name that opens with the phase spends its best characters saying nothing.

   The tag before the activity is the project: the PRD's name, abbreviated per rule 5 (`orderN`, `accountA`). It is the token most tempting to drop, because every sibling shares it, and it is the one that makes the unit id readable. A product tag (`BL`) is a separate token after it, taken from the shared prefix of a repo family (`billing-*`), and it earns its characters only when that family sits beside other products' repos in the same parent directory: `billing-invoice-export` there gives `IE-export BL refine`, and a name that stops at `IE-export` is wrong because `IE` means nothing outside that product. When every repo in the directory belongs to one product, the product is where the chat already lives and says nothing: `ph4b1 accountA impl`, never `ph4b1 accountA <product-tag> impl`. Where no PRD directory supplies a project tag (a ticket, a GitHub issue, an ad-hoc thread) there is none: the name closes on its subject noun, as `PROJ-4271 user import impl` and `dup accounts stage2 ops` do, and a tag is never coined from a lone repo name, a company, or a team. Shorten a tag the work has when the name runs long; never drop it.
3. **Every name ends with its activity, in one abbreviated word.** Whether the chat implements, refines the requirements, splits a phase, drafts a design, investigates, or reviews, the reader has to be able to tell, and the activity is the one fact the documents' identifiers do not carry. Implementation gets its token like everything else, so a name has one shape and "every implementation chat" is greppable. Use the same abbreviation every time, six characters or fewer:

   | Next chat runs | Token |
   |----------------|-------|
   | `implement-from-requirements`, `implement-from-discovery` | `impl` |
   | `autonomous-requirements-refinement` | `refine` |
   | `phase-split` | `split` |
   | Technical Design writing (`technical-design-writing-standards`) | `design` |
   | PRD writing (`prd-writing-standards`) | `prd` |
   | `prd-roadmap` | `rdmap` |
   | `investigate-question`, an issue or ad-hoc investigation | `invest` |
   | `deliverable-review`, a design, code or PR review | `review` |
   | `test-audit` | `audit` |
   | `refactor-pass` | `refac` |
   | an ad-hoc operational thread (a stakeholder volley, an incident) | `ops` |
   | anything else | the skill's own verb stem, cut to six characters |

   The token never opens the name (the tab is for finding the chat, and the unit id finds it) and is never spelled out or improvised: `ph3b2 orderN implementation` and `ph3b2 orderN build` are both wrong. When the name runs past the cap, pay for the token out of the middle: shorten the subject noun first, then the project tag. Never drop the unit id, the activity, or a tag the work has.
4. **Reuse the identifier the documents use, verbatim and with its casing.** `PROJ-4271`. The name must match what the user will grep for. A bare positional id from `phase-split` (`2b1`) takes the `ph` prefix so it reads as a phase: `ph2b1`.
5. **Abbreviate the project tag, never a unit id the documents give.** Under the target the words stay whole (`account alerts`). Past it, filler goes first (`expanded`, `completion`), then the tag collapses to its distinguishing word plus the initial of the word after it: `orderN` for Order Notifications, `accountA` for Expanded Account Alerts. The phase id stays whole. A PRD standing in as the unit has no id, so rule 6 applies to it.
6. **No dates, no articles, no punctuation that the tool might strip, and never the PRD title as written.** When the PRD itself is the unit (a refinement or a split), its subject noun abbreviated stands in: `IE-export`, not `billing-invoice-export`.

| Work | Name |
|------|------|
| A PRD phased under `phase-split`'s positional ids: phase 2b1 of User Onboarding (the id already carries its parents, so no separate phase token) | `ph2b1 userO impl` |
| Order Notifications phase 3b2, but the chat refines its requirements before any code | `ph3b2 orderN refine` |
| Phase 2 of the same project, being split into sub-phases (the phase is the unit, so it leads) | `ph2 orderN split` |
| Billing product, invoice-export PRD refined as a whole, no phases yet | `IE-export BL refine` |
| Writing the Cloud Ingestion PRD, a planned PRD in the Acme Cloud PRD roadmap (the planned PRD's short-name is the unit; the roadmap is the project tag) | `ingestion acmeCloud prd` |
| The only product in its directory; Account Alerts PRD, phase 4b1 | `ph4b1 accountA impl` |
| Jira ticket PROJ-4271 in user import | `PROJ-4271 user import impl` |
| PROJ-4271, root cause still unknown, no fix yet | `PROJ-4271 user import invest` |
| Ticket PROJ-4288, phone-number truncation | `PROJ-4288 phone impl` |
| Ad-hoc thread: duplicate account cleanup, stage 2 | `dup accounts stage2 ops` |

A name whose first token is `ph2` or `orderN` is wrong under rule 2 unless the phase or project really is the distinguishing token among the chats open at that moment. A name with no activity token is wrong under rule 3 whatever the chat does; nothing else in the tab says what the session is for. `IE-export refine` is wrong under rule 2: the product tag is missing, and the unit abbreviation is opaque on its own. `ph4b1 accountA <product-tag> impl` is wrong under rule 2 as well: the product is the whole directory, and its characters belonged to the project name.

---

## Step 3: Assemble the Prompt

Order matters. Tools that auto-title a session summarize the first prompt, and Anthropic's prompting guidance puts context before the ask and the ask last. The prompt reads, top to bottom:

1. **The name, alone on line one, then a blank line.** Nothing above it and no `Chat:` prefix. The title hook takes a short bare first line of a session's first prompt as the name; `Chat: <name>` is the explicit form for renaming mid-session, not the opening line.
2. **The lineage block**, filled per the gate above, in a fixed shape so it is greppable across chats:

   ```
   In service of: Order Notifications (PRD)
     Phase 2a1 — Delivery receipts from the SMS provider
     This chat: implements it.
   ```

   For a fix, line 3 reads `This chat: fixes the stale cache key that blocks AC-DLV-04 of it.` For the shapes with no phase, the ticket id, thread, or component takes the PRD line and `no phase — <shape>` the second:

   ```
   In service of: Jira PROJ-4271 — user import
     no phase — ticket-tracked work
     This chat: implements the fix.
   ```

   Full titles, never abbreviations: the name line is abbreviated because a tab strip is twenty characters wide; this block is where the words go.
3. **Skill and goal.** The skill to invoke by name (the name line's activity token must agree with this skill per Step 2 rule 3), then the goal in one or two sentences. State the unit of work exactly as the governing doc names it; the block above carries the titles, so this line is the *what*, not the *for whom*.
4. **Where to work.** Repos and the branch, with "stay here" made explicit. If the work is on the shared branch directly, say so. A worktree a chat created for parallel isolation is never handed on: it removes its own at wrap-up, and the next chat creates its own. A worktree the user established for the work (a `phase-chain`'s, for example) is named like any other checkout. Name any checkout to avoid and why. This is the machine-truth bin from Step 1.
   **Name the working directory by absolute path, and say what kind of checkout it is**: the shared checkout (the directory the user opens in the editor, e.g. `/Users/<user>/devel/<org>/<repo>`), a worktree, or a private clone. "Work on develop in <repo>" names a branch, not a directory, and the reader must never have to infer which copy of the repo is meant. If this session worked somewhere else (a private clone it made because the shared checkout could not fast-forward, a worktree it created), that choice does not carry forward on its own. The prompt names the directory the next session should use and, where it differs from the shared checkout, how the work gets back to it.
   **Parallel or not.** Write the prompt for the shared checkout unless the next chat will run in parallel with others: the user or the calling chat says so, this chat is handing out more than one prompt at once, or another agent session is live in a repo the next chat will touch. `implementation-lifecycle`, "Parallel Sessions: Where to Work", defines live and the worktree mechanics. When it will run in parallel, add `Parallel: yes` on its own line under the lineage block, name the worktree the next chat creates (`<org directory>/.worktrees/<slug>/<repo>` on branch `wt/<slug>`, the slug being the chat name lowercased with hyphens), and name the area the chat owns. The receiving chat runs the same check itself, so a prompt written for the shared checkout still isolates if it lands beside a live session (inside an authorized `phase-chain`, a successor stops as blocked instead). Do not infer parallel work from anything else, and never prescribe a clone unless the user asked for one.
5. **Governing documents.** Path and section heading for each, and what the reader will find there. Point, never restate. If Step 1 wrote a new section, this is where it is cited.
6. **State, as pointers.** What is closed (with dates and commit hashes, which are cheap and unambiguous), what is owed, and where each is recorded. One line per item. A predecessor's findings appear as "read section X of doc Y", not as the findings themselves. Under Step 1's one-shot exception there is no doc Y, and the facts appear in the prompt as themselves.
7. **Verification expected.** How the next session proves its work, if the governing doc does not already say. Usually one line naming the precedent to copy.
8. **Scope discipline.** What is explicitly out, when the doc's scope statement is not enough on its own. Known pre-existing failures the next session must not adopt as its own: a pointer to where Step 1 recorded them, with the date they were verified.
   For an authorized Codex `phase-chain`, also carry its chain context: actual authorization wording and sources, remaining scope, established checkout/branch/remote, model preference, delivery gates, and predecessor identity. These are session truth; preserve the evidence even if the prompt exceeds the usual length target.
9. **First action, last line.** The single concrete thing to do first. Not a list.

Length: the prompt should fit on one screen, roughly 18 to 33 lines including the lineage block. A prompt past 40 lines almost always failed Step 1; go back and move the facts into the docs. The exceptions are an authorized chain handoff (item 8 above) and a one-shot prompt under Step 1's exception; both carry facts the docs will never hold, and both run longer by design — still only the facts the receiving session will actually use, because a one-shot prompt is a work order, not a transcript. The old-style prompt that ran to a hundred lines was a document that had not been written yet.

What never appears:

- Content the docs already hold, paraphrased "for convenience."
- A narrative of what this session did. The commit message and the docs carry that.
- Test counts, file inventories, or a list of everything that was verified.
- FYIs, caveats, or "worth noting" items. They failed the gate or they were filed.
- Promises about what a later session will do. If it is owed, it is recorded in a doc and the prompt points there.

---

## Step 4: Output Block

For an active, authorized Codex `phase-chain`, return the composed prompt to that orchestrator for actual task creation after delivery; do not ask the user to paste it. Otherwise, present the result as one paste. With the title hook installed (see Adopting This Skill), the name line *is* the rename, so there is nothing to paste first:

````
Paste into the new chat:

```
ph3a2 orderN impl

In service of: Order Notifications (PRD)
  Phase 3a2 — Quiet-hours scheduling for SMS notifications
  This chat: implements it.

Use implement-from-requirements. Order Notifications phase 3a2: hold SMS
notifications that fall inside a customer's quiet hours and send them when the
window ends. Email is out; 3a1 already covers it.

Work in the shared checkout /Users/<user>/devel/<org>/notifications-service, on
develop directly. Pull first. Tests need
Node 22 (`nvm use`); the default Node on this machine is older.

Governing docs, all under docs/prds/order-notifications/:
  phase-3a2-quiet-hours.md — scope of record and "What 3a1 hands 3a2"
    (the scheduler's retry contract and the time-zone lookup it built).
  technical-design.md — "Scheduling" and "Delivery states".
  assumptions.md — NOTIF-007 (quiet hours default to
    9 pm–8 am local; open, not blocking).
Predecessor closed and on develop: 3a1 (2026-03-18, a41c9e2). Build on it.

Prove it the way 3a1 was proved; the phase doc's "Proof standard" names the
integration test to copy. Out of scope: per-customer quiet-hours settings (3b),
push notifications, and the pre-existing failures in the phase doc's "Known
failures" (verified 2026-03-18).

First: read the 3a2 phase doc in full, then size the work.
```

Valid once the commit proposed above lands (it carries the plan-doc sections this
prompt points at).
````

In that example the lineage block is the only place the PRD and phase appear by full title; the directory, branch, and Node-version lines are machine truth (prompt only); every other line is a pointer or a goal. The predecessor's findings and the proof standard live in the phase doc's named sections, which is where Step 1 put them.

The name line does double duty: the hook turns it into the session title, and it tells a reader who scrolls to the top what the chat is even if a tool later regenerates its own title. To rename a running session, send a message whose first line is `Chat: <new name>`; the bare form applies only to a session's first prompt, so an ordinary short reply never renames anything. Only when the user is on a tool without the hook (see the table below) does the output add a `/rename <name>` line above the prompt, to be typed first. In Claude Code, treat the hook as installed when `~/.claude/settings.json` mentions `session-title-from-chat-line`; check with a grep rather than asking.

### Naming mechanics by tool

State only the line for the tool the user is on when you know it. For Claude Code with the hook installed there is no line to state; without it, give the `/rename` form and note the others in a clause.

| Tool | How the name gets set |
|------|------------------------|
| Claude Code, terminal or VS Code extension | With the title hook installed, nothing to do: the name line sets the title before the prompt runs (the hook returns `sessionTitle` from `UserPromptSubmit`, Claude Code 2.1.94 and later; verified to write the same record `/rename` writes). Without the hook: `/rename <name>` typed in the chat (in the VS Code extension a *pasted* `/rename` can be sent as an ordinary message instead of running, so type it), `claude -n "<name>"` from a terminal, or Ctrl+R in the `/resume` picker. The docs describe the name showing in the prompt box, the `/resume` picker, and the terminal title; the VS Code extension shows it as the tab title in practice. An unnamed session's auto-title is a summary that starts from the name line but rewrites it, and accepting a plan in plan mode retitles an unnamed session; a named session keeps its name. |
| Claude desktop app | Rename from the session's UI in the desktop app. The assistant cannot set it. |
| Codex CLI | `/rename <name>` in the TUI (per the Codex CLI reference). |
| Codex VS Code extension | Click the chat name at the top of the panel. |
| Codex desktop app | May expose a thread-title tool to the assistant for local threads. If one is available and the prompt opens with a name line (or a `Chat:` line), set the title to that name before doing anything else. |

---

## Step 5: Commit Before the Prompt Is Valid

The prompt is a pointer into documents. It is only as good as the next session's ability to read them, and the next session often cannot see this session's working tree:

- A fresh worktree off the shared branch sees committed history, not uncommitted edits in another worktree.
- A second checkout on the same machine, or a Codex session with its own clone, sees the remote or the shared branch's history.
- Even in the same checkout, uncommitted edits are this session's work in progress, not the docs: the next session is pointed at the documents, and only committed edits are reliably there to read.

So: **the doc edits from Step 1 go into the commit this session is already proposing** (the feature commit or the phase-docs commit, whichever the calling skill produces). Label the prompt with any outstanding delivery prerequisites, or the actual delivery hashes if they already landed. This skill composes the handoff; the calling workflow owns commits and pushes under live user authorization, including authorization carried by an active `phase-chain`. A prompt-only request does not itself authorize delivery or task creation. What it will not do is present a prompt that depends on an uncommitted file without saying so.

**Push** is required when the user or project delivery contract requires it (including `phase-chain`), or the successor needs the remote history. Otherwise a successor using the same local repository may consume local commits. Separate clones need transfer even on the same machine; do not assume they share history. State the actual prerequisite.

---

## Rules and Constraints

### DO

- Run Step 1 first and write the facts into the docs before drafting the prompt, unless its one-shot exception applies
- Put the name alone on line one with a blank line under it, nothing above it, no `Chat:` prefix
- Fill the lineage block from the documents before drafting: PRD and phase by full title, and the acceptance criterion a fix unblocks; write `no lineage found` only on an explicit ask, never a plausible purpose
- Count the name's characters; twenty target before the activity token, thirty cap on the whole name
- Lead the name with the unit of work's own id, exactly as the docs spell it
- Close the name, before the activity token, with the project tag when the work has one (`orderN`, `accountA`), plus the product tag only when its repo family sits beside other products' repos (`BL`); shorten a tag, never drop it
- End the name with the fixed activity token, `impl` included
- Point at doc sections by path and heading; cite commit hashes and dates for closed work
- Name the working directory by absolute path and its checkout kind (shared checkout, worktree, private clone); never carry this session's improvised location forward unstated
- Default to the shared checkout; write `Parallel: yes`, a worktree and an owned area only on a stated or detected parallel signal
- End with the single first action
- Label the prompt with what must land before it is valid, or say it is valid immediately when nothing does
- Present one paste: the prompt, whose first line is the rename when the title hook is installed
- Re-run the whole skill when asked to regenerate; change only the name when only the name was wrong

### DO NOT

- Restate doc content in the prompt
- Name a branch without the directory it is checked out in
- Produce a prompt for a fix that unblocks no named acceptance criterion, ticket id, incident, or session file — that is a discovery being promoted into work by the handoff; send it back through the Materiality Gate or name it in the wrap-up as the user's decision
- Open a ticket in any tracker for an orphan fix and cite that id as its lineage; a minted id makes work findable, not needed
- Fill the lineage block with a phase id alone, a slug, or the chat-name abbreviation; the titles go there in full
- Open the name with a verb, the phase, or the project tag when a more specific id exists
- Leave the activity off the name, spell it out in full, or improvise a token the table's rows or its last-row rule do not produce
- Drop a project or product tag the work has, or invent one it does not; a unit abbreviation alone (`IE`) means nothing outside its product
- Spend characters on a product tag when every repo in the directory belongs to that product
- Carry dismissed observations into the prompt as FYIs
- Present a prompt whose facts live only in the chat or in an uncommitted file, unless the one-shot exception in Step 1 applies and the prompt itself carries them
- Treat a prompt-only request as authorization to commit, push, or launch tasks; those actions belong to the authorized calling workflow
- Ask the user to paste a `/rename` line when the title hook is installed
- Omit a required push from the handoff prerequisites just because the next task runs on the same machine
- Produce a prompt for a different track when the finished unit has no successor in its own chain; the end of a track is the user's decision point, and "the most logical thing next" is a guess wearing a handoff's clothes
- Load this skill for a context package — information going *back to* a chat that is already running. That is a plain briefing (what was done, artifact paths, what is open, caveats), not a continuation prompt; see "Not this skill" under When to Use

---

## Adopting This Skill

Two one-time steps.

**1. The instructions line.** Skills load on demand, so the assistant has to know to reach for this one when the user asks for a prompt in passing. Put this line in the instructions file your tools read (`~/.claude/CLAUDE.md` for Claude Code, `~/.codex/AGENTS.md` for Codex, or whatever single file you symlink to both); the README of this repository carries the same text:

> CONTINUATION PROMPTS: Whenever asked for a prompt to paste into a new chat, or when a skill hands work to a fresh chat, use the `continuation-prompt` skill. If a prompt you receive opens with a short name alone on its first line (or a `Chat:` line) and you have a tool that sets the thread or session title, set it to that name before anything else; if you have no such tool, say nothing about it (where the optional title hook is installed, it has already set the title).

**2. The title hook (Claude Code).** The assistant cannot rename its own session, but a `UserPromptSubmit` hook may return `sessionTitle` (Claude Code 2.1.94 and later), which sets exactly what `/rename` sets. The script in this skill's `hooks/` directory does only that, by two rules: on a session's first prompt, a bare first line that looks like a name (40 characters or fewer, no trailing punctuation, not a slash command, @-mention or pasted attachment tag, followed by a blank line and the body) becomes the title; on any prompt, a first line of `Chat: <name>` sets the title explicitly. Both rules read past a leading `<pasted_content id="...">` tag, which the VS Code extension wraps around pasted text, and past whole context blocks a client prepends to the message, such as the `<browser_instruction>` block the VS Code extension adds to a session's first message when Claude in Chrome is enabled (2.1.287 and later). Every other prompt passes through untouched and the hook never blocks one. Merge this into `~/.claude/settings.json`, keeping any hooks already there (this is the whole `hooks` key; if you already have one, add the group to its `UserPromptSubmit` list). Adjust the path if this skill is not linked under `~/.claude/skills`; if you installed the Enso Method as a plugin, point it at a clone of the repository (`<clone>/skills/continuation-prompt/hooks/…`), because the plugin's own copy moves with every update. The hook is global to Claude Code: one registration serves every skills repo.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command",
                     "command": "python3 ~/.claude/skills/continuation-prompt/hooks/session-title-from-chat-line.py",
                     "timeout": 5 } ] }
    ]
  }
}
```

Test it without Claude Code (`printf`, not `echo`: zsh and sh turn the `\n` into a real newline, which strict JSON rejects):

```
printf '%s' '{"prompt":"ph3b2 orderN impl\n\nUse implement-from-requirements."}' \
  | python3 ~/.claude/skills/continuation-prompt/hooks/session-title-from-chat-line.py
```

It prints a `hookSpecificOutput` object carrying the title. With the hook in place the name line is the rename and the user pastes once. Sending a later message that starts with `Chat: <new name>` renames the session.

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `implementation-lifecycle` | Defines which document owns which kind of fact (phase doc: work state; Technical Design: durable design facts; assumptions: business logic). Step 1 sorts into those homes. Also the Materiality Gate that keeps dismissed items out of the prompt, and "Every Session Names What It Serves", which the lineage gate applies at the handoff. |
| `implement-from-requirements` | Calls this skill at wrap-up when a next phase exists |
| `phase-split` | Calls this skill after the phase docs are written, for the first leaf's prompt — only when the user invoked it directly; called from an implement session it produces no prompt |
| `pre-commit-validation` | The doc edits from Step 1 ride in the commit that skill validates |

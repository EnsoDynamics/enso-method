---
name: build-preflight
description: Last check before a PRD's build starts, while the user is still there — prove the access the whole plan needs and that it will outlive the run, confirm the machine can build and test the project, confirm what the design says a person provides first, and find every stop left in the plan. Reports "ready" in one line, or a short numbered list where every item is a command to run or one named thing to settle. It changes no file. Not a review — it never comments on the requirements, the design, the criteria, scope or cost. Use after phase-split and before the first implement-from-requirements session, when the user asks whether a build is ready to run unattended, or as the first step of an orchestrator's run.
user-invocable: true
---

# Build Preflight

A build of a split PRD runs for hours or days with nobody watching. This skill runs once, just before it starts, to find anything that would stop it part-way and that the user can clear in a minute now.

It is optional. Nothing in the method waits on it, and `implement-from-requirements` still checks its own session's access. An orchestrator can run it as its first step.

**It is not a review.** The requirements are settled by this point. Never comment on a criterion, the design, the scope, the number of phases or what the build will cost. If something there looks wrong, it is out of this skill's scope and stays unsaid.

---

## What to Read

The PRD, its technical design (the Delivery section in full), every phase document, the repository's README and its instruction files (`AGENTS.md`, `CLAUDE.md`). Read for the five checks below and nothing else.

---

## The Checks

Run them in parallel where they don't depend on each other. The checks only read, with three exceptions: refreshing a sign-in, installing a missing tool, and running the project's tests.

1. **Access for the whole plan.** List every external dependency any phase will touch: cloud profiles, source hosting, databases, third-party APIs, paid services, a browser sign-in. Make one cheap read-only call per dependency against the environment the build will use, proving it reaches the specific resource (`implement-from-requirements`, "Preflight external access", has the call patterns). Re-authenticate yourself where a command does it.
2. **Access that outlives the run.** For each credential, find when it expires. A split PRD's build runs for a day or more, so one that expires sooner will expire mid-build: use the longer-lived alternative the project's credential guidance names, or say the exact command that refreshes it and whether that command needs a person.
3. **This machine can build and test.** The tools and versions the README names are installed, secrets and local configuration the tests read are present, and the project's test command passes before any change. A suite that is already red here is an item, with the count and the first failure.
4. **What a person provides first.** Each line under the Delivery section's "Before the build" is done, checked by a call where one exists. Work this PRD builds on (another PRD's branch, a service another team deploys) is merged or running where the build will look for it.
5. **Stops left in the plan.** Name each of these:
   - Phases marked `**Attended:**`, and each line under Delivery's "Planned stops" and "Early merges" with what the build waits on.
   - A stop in a phase document that Delivery does not list: a deploy, a merge, a wait, a step for a person.
   - A rule in the repository's instruction files that makes a build wait for a person, such as approval before spending or before a push.

---

## What Each Finding Becomes

Every item names one thing to settle before the build: a command to run, or what is missing and who provides it. No item is a question, because the preflight acts on no answer. A finding with nothing to settle does not go in the report.

| Finding | The item |
|---|---|
| Access missing or expiring | The exact command to run, or the one thing to grant and who grants it |
| The machine cannot build or test | The command that installs or fixes it. When the project is set up on another machine, name that machine and say to run the build there |
| A "Before the build" line not done | The line, and who does it |
| An attended phase, planned stop or early merge | One line each under "The build will stop", so the user knows before walking away |
| A stop Delivery does not list | One line under "The build will stop" that says the design does not list it |
| An instruction-file rule that makes the build wait | The rule, the file it is in, and the phase where the build will stop on it: "The repository's instructions say to ask before spending past the limit, and phase 6 will pass it. Nothing in the requirements authorizes that." |

---

## The Report

The first line is one of these two, exactly, so a person or a tool can read the result at a glance:

```
Preflight: ready
Preflight: 3 items need you
```

Under "ready": the number of phases, and one line for each stop the build will make (or "The build runs to the end without stopping"). Nothing else.

Under "items need you": the numbered items, each one or two lines, the blocking ones first. Then the "The build will stop" lines, if any. When the user has settled the items, run the failed checks again and report again.

**The preflight changes no file in the repository.** When the user, in this conversation, asks for a change that settles an item (an authorization, a raised limit, a stop taken out), that is requirements work and no longer the preflight. Make it everywhere the requirements carry it (the PRD, the technical design, the phase documents, the assumptions), through the skill that owns each document and with the care that skill asks for, never as one line added to make the item go away. Then run the checks again and report again.

```markdown
Preflight: 2 items need you

1. The cloud sign-in for the development account expires in 8 hours. Run `aws sso login --profile app-dev-longlived`.
2. The repository's instructions say to ask before spending past the limit, and phase 6 will pass it. Nothing in the requirements authorizes that.

**The build will stop** at phase 1, which needs you at the vendor's console (marked Attended). Phases 2 to 9 run without you.
```

---

## Rules and Constraints

### DO

- Check access for every phase, not only the first
- Fix what a command fixes before reporting it
- Phrase every item as a command to run, or as the one thing to settle and who settles it

### DO NOT

- Comment on the requirements, the design, the criteria, scope, size or cost
- Report an observation with no step attached
- Change any file in the repository, or ask a question whose answer would have you change one
- Start the build

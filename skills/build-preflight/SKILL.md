---
name: build-preflight
description: Last check before a PRD's build starts, while the user is still there — prove the access the whole plan needs and that it will outlive the run, confirm the machine has what it needs to build and test the project, confirm what the design says a person provides first, and find every stop left in the plan. It clears what a command clears (a sign-in refresh, a missing tool) and reports "ready" in one line, or a short numbered list of only what is left for a person. It changes no file. Not a review — it never comments on the requirements, the design, the criteria, scope or cost. Use after phase-split and before the first implement-from-requirements session, when the user asks whether a build is ready to run unattended, or as the first step of an orchestrator's run.
user-invocable: true
---

# Build Preflight

A build of a split PRD runs for hours or days with nobody watching. This skill runs once, just before it starts, to find anything that would stop it part-way and that the user can clear in a minute now.

It is optional. Nothing in the method waits on it, and `implement-from-requirements` still checks its own session's access. An orchestrator can run it as its first step.

**It is not a review.** The requirements are settled by this point. Never comment on a criterion, the design, the scope, the number of phases or what the build will cost. If something there looks wrong, it is out of this skill's scope and stays unsaid.

---

## What to Read

The PRD, its technical design (the Delivery section in full), every phase document, the repository's README and its instruction files (`AGENTS.md`, `CLAUDE.md`). A README is often out of date, so also read what the project itself declares: its package manifest and version files, its example environment file, its test configuration and setup files, and its CI workflow files. Search the code and tests the phases will change, without reading them through, for the credentials, services, tools and settings they name. Read for the five checks below and nothing else.

---

## The Checks

Run them in parallel where they don't depend on each other. The checks only read, with two exceptions, both done without asking: refreshing a sign-in, and installing a missing tool. A tool is software installed on the machine, outside the project: a runtime, a command-line program, a browser the tests drive, a system package. It is never the project's own dependencies.

1. **Access for the whole plan.** List every external dependency any phase will touch: cloud profiles, source hosting, databases, third-party APIs, paid services, a browser sign-in. Make one cheap read-only call per dependency against the environment the build will use, proving it reaches the specific resource (`implement-from-requirements`, "Preflight external access", has the call patterns). Re-authenticate yourself where a command does it.
2. **Access that outlives the run.** For each credential, find when it expires. A split PRD's build runs for a day or more, so one that expires sooner will expire mid-build. Switch to the longer-lived alternative the project's credential guidance names. Without one, run the refresh command now. A refresh that waits on a person (a browser approval, a device code) gets about a minute, then is stopped. Compare what is left with the clock: a credential that has expired, or will within two hours, is an item. One that lasts longer does not hold the build back: it is a line under "The build will stop" with the time it lapses and the command to run.
3. **This machine has what it needs to build and test.** The tools and versions the project names are installed, and the secrets and local configuration the tests read are on this machine. Check each with a version command or by confirming a file or variable exists, and run nothing else: no test (not even a single one, which often starts the whole suite anyway), no project script, and nothing that installs dependencies, compiles, lints, type-checks or starts a service. What the build sets up for itself is neither made nor reported: the project's own dependencies in whatever form the language keeps them (a virtual environment, a dependency or vendor folder, compiled output), which a fresh worktree lacks, and local configuration it can copy from the shared checkout. A suite that is already red is left for the build to find.
4. **What a person provides first.** Each line under the Delivery section's "Before the build" is done, checked by a call where one exists. Work this PRD builds on (another PRD's branch, a service another team deploys) is merged or running where the build will look for it.
5. **Stops left in the plan.** Name each of these:
   - Phases marked `**Attended:**`, and each line under Delivery's "Planned stops" and "Early merges" with what the build waits on.
   - A stop in a phase document that Delivery does not list: a deploy, a merge, a wait, a step for a person.
   - A rule in the repository's instruction files that makes a build wait for a person, such as approval before spending or before a push.

---

## What Each Finding Becomes

An item holds the build back until a person acts, and the person has often left by the time the report is ready. So sort each finding by who can clear it:

- **You can**, by refreshing a sign-in or installing a tool: do it. It reaches the report only if it failed or waits on a person.
- **The build will**, as part of its own work: leave it out.
- **Only a person can, and the build cannot get far without it:** an item.
- **Only a person can, and it matters hours from now:** a line under "The build will stop".

Every item names one thing for a person to settle before the build: a command only they can finish and what they do in it, or what is missing and who provides it. No item is a question, because the preflight acts on no answer. A finding with nothing to settle does not go in the report.

| Finding | The item |
|---|---|
| Access missing, or expiring within two hours, after the refresh was tried | The exact command and the step in it that needs the person, or the one thing to grant and who grants it |
| A tool is missing and the install failed or needs a person | The command, and what it returned or what it needs (an administrator password, a licence). When the project is set up on another machine, name that machine and say to run the build there |
| A "Before the build" line not done | The line, and who does it |
| An attended phase, planned stop or early merge | One line each under "The build will stop", so the user knows before walking away |
| A stop Delivery does not list | One line under "The build will stop" that says the design does not list it |
| A credential that lapses during the build, more than two hours from now | One line under "The build will stop": the time it lapses, the command to run then, and that running it now pushes the stop back |
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

1. The cloud sign-in for the development account has expired, and its refresh waits for you. Run `aws sso login --profile app-dev --use-device-code` and approve the code.
2. The repository's instructions say to ask before spending past the limit, and phase 6 will pass it. Nothing in the requirements authorizes that.

**The build will stop** at phase 1, which needs you at the vendor's console (marked Attended). Phases 2 to 9 run without you.

**The build will stop** at about 11:40 PM, when the reporting database's sign-in lapses. Run `gcloud auth login` then, or now to push that back.
```

---

## Rules and Constraints

### DO

- Check access for every phase, not only the first
- Run each refresh and install yourself, and report only what is left for a person
- Phrase every item as a command only a person can finish, or as the one thing to settle and who settles it

### DO NOT

- Comment on the requirements, the design, the criteria, scope, size or cost
- Report an observation with no step attached
- Hand the user a command you could have run, or setup the build does for itself
- Change any file in the repository, or ask a question whose answer would have you change one
- Start the build

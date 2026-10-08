---
name: technical-design-writing-standards
description: Standards and process for writing technical design documents — architecture decisions, interfaces, data models, and integration points, including designs for changes to an existing system. Use to write a design from a PRD, or to check one. Not implementation instructions.
user-invocable: true
---

# Technical Design Writing Standards

Guidelines for writing technical design documents.

---

## What Is a Technical Design Document?

A technical design document describes **how** we're going to build something. This is where technical decisions, interfaces, data models, and architecture choices are documented.

The technical design document bridges the gap between the business requirements (the PRD) and the actual implementation. It captures decisions that affect multiple phases or have long-term implications.

---

## When Do You Need a Technical Design Document?

Most PRDs need a technical design document. If you're building anything with interfaces, data models, or architecture decisions that need to be agreed upon before implementation, write one.

You can skip it when a feature is small, follows an established pattern, and doesn't introduce new interfaces or architectural choices — the PRD is sufficient in those cases.

---

## Writing a Technical Design

When asked to write a design, not just check one, this is the whole process. No separate research phase comes first; you read what the PRD's criteria touch, as you need it.

### Existing code: Preserve or Salvage

Most designs change a system that already exists. Before writing, know how to treat its code. This is **stated, not researched**: take it from the person asking or from the PRD, and never work it out from deploy or merge history. If nobody says and existing code is involved, use Preserve, the default, and say so in one line so the user can correct it.

- **Preserve:** the code is in production, or other work relies on it. Its behavior is a constraint the design keeps.
- **Salvage:** the code is unreleased, or left over from earlier work being restarted. Reuse what fits the PRD; anything else gets one line saying it is switched off or left alone, and the design never works around it.

A system can be mixed; say which parts are which. `autonomous-requirements-refinement` uses the same two terms.

### Steps

1. **Read the PRD in full**, plus any PRD or design it builds on, and settle the posture above.
2. **Work from the PRD outward, not from the code outward.** For each acceptance criterion, read the code and systems it touches until you know what already exists and what is missing. Stop there; a survey of the whole system is not needed.
3. **Write the sections in the example structure below, designing only the difference**: the new or changed interfaces, data models and decisions, each decision with its rationale. For an existing system, add a short **Existing Code** section that records decisions, not a description: the posture in one line; what is reused, named in a line each; what is switched off (Salvage); and, under Preserve, behavior the design must keep that the code alone would not tell you. Don't describe how the existing code works, anywhere in the design; the implementer reads the code, and a description only goes stale. Keep the section to about a dozen lines.
4. **Keep to the PRD.** The design never adds a requirement, and behavior the PRD doesn't ask for is out of scope. Technical choices you can make, make, and record why. A gap in the PRD goes in Open Questions; a business uncertainty also goes in the assumptions document per `assumptions-document-writing`.
5. **Check before handing it over.** Every acceptance criterion is covered by something in the design, nothing is designed that no criterion asks for, and it can be read in one sitting.
6. **For a design with hard-to-reverse decisions** — a new service, a schema or data model, a public interface — run `review-technical-design` next, before `autonomous-requirements-refinement`. It is optional; a design that follows an established pattern can skip it.

---

## What Belongs in a Technical Design Document

### Overview
Brief summary of what's being built and the key technical decisions. Link to the parent PRD.

When the PRD comes from a PRD roadmap (`prd-roadmap`), the design also honors the full brief's settled decisions and the roadmap's seams. It decides the shared contracts the roadmap says this PRD owns, and extends — never redesigns — contracts an earlier PRD owns. It covers only what this PRD ships, not the whole roadmap.

### Architecture Decisions
What choices are we making and why? Each decision should include rationale — not just "we chose X" but "we chose X because Y."

- **Workload type:** Is this a REST API, queue consumer, cron job, event processor, web application?
- **Starting point:** for new software, the seed project or existing repo whose patterns it copies — CI/CD, logging, configuration, project layout. The house engineering standards may name one; otherwise name the closest existing repo and say so. The method ships no seed projects.
- **Data store:** Which one, and why?
- **Hosting:** Where does it run — a new service, serverless functions, an existing service?
- **Dependencies:** What other services does this interact with?

### Interfaces

This is the most important section. Define the contracts:

**API Endpoints:**
```
POST /api/audit/data/{dataSourceId}

Request Body:
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "page": 1,
  "pageSize": 50,
  "filters": { ... }
}

Response:
{
  "data": [...],
  "totalCount": 1234,
  "totals": { ... }
}
```

**Queue Messages:** If using queues, what's the message format?

**Events:** If publishing events, what's the event schema?

### Data Models

Define the key data structures:

```
AuditDataRequest:
  - dataSourceId: string (required)
  - startDate: date (optional)
  - endDate: date (optional)
  - page: int (default: 1)
  - pageSize: int (default: 50)
  - filters: QueryBuilderRules (optional)
```

For database changes, describe new tables or modifications to existing schemas.

### Integration Points

If this feature needs to interact with other systems or services, describe those touchpoints:

- "Calls the existing Schema API to get field definitions"
- "Reads from the raw data tables created by the data ingestion process"
- "Publishes events to EventBridge when exports complete"

Don't name specific classes or describe internal structure—that's implementation.

### Open Questions

Document any decisions that still need to be made or areas of uncertainty.

### Changes to an Earlier Design

When this design changes a decision or interface an earlier PRD's design made, the decision carries a `Replaces:` line naming the earlier design and section: `Replaces: docs/prds/customer-returns/technical-design.md, §Status Mapping` (or `Replaces in part: … (what changed)`). When the change is built, the earlier section gets one line under its heading, `Superseded by: <path>, §<heading>`, or `Superseded in part by: … (what changed)`, in the same commit as the code. The rules are the PRD's (`prd-writing-standards`, "When Later Work Changes an Earlier Criterion"): the earlier text is never rewritten, each pointer goes to the next document, and the line is a pointer between documents, not decision history.

---

## What Does NOT Belong in a Technical Design Document

### Step-by-Step Implementation Instructions
A technical design document is not a recipe. Don't tell developers:
- Exactly which existing functions to modify
- Line-by-line code changes
- "Reuse function X from file Y with these tweaks"

### Implementation Code
This is a design document, not an implementation document. There should be no real code in here — no Python, no JavaScript, no SQL queries, no CloudFormation, no Terraform. Pseudocode is acceptable when it clarifies a design concept or algorithm that's hard to express in prose, but actual implementation code belongs in the codebase, not the design. Interface definitions (API payloads, data models, message schemas) are appropriate because they describe contracts, not implementation.

### File-by-File Change Lists
"Modify `SchemaService.cs` to add method `GetRawDataTableName()`" - this level of detail doesn't belong here. The developer will figure out where code goes.

### Decision History
State each decision and its rationale as it stands now. Who ruled on it and when, superseded versions, and dated correction notes belong in git history and the assumptions document, not the design. `Replaces:` and `Superseded by:` lines are pointers between documents, not history, and stay.

### Unnecessary Detail
A technical design document doesn't need to document every detail. Focus on:
- Decisions that matter
- Interfaces that need to be agreed upon
- Things that would be hard to change later

A reader should be able to get through the design in one sitting. A design more than about three times the length of its PRD is a signal, not a cap: it is usually documenting the existing system or carrying decision history, so cut it back.

---

## The Right Level of Detail

Think of the technical design document as the blueprint, not the construction manual.

A good technical design document:
- Captures architectural decisions and their rationale
- Defines interfaces clearly enough that different components can be built independently
- Provides enough context for developers to make good implementation decisions
- Doesn't dictate implementation details that the developer should decide

---

## Example Structure

```markdown
# Technical Design: [Feature Name]

**PRD:** [Link to PRD]

## Overview

[Brief summary of what we're building technically]

## Existing Code

[Only when changing an existing system, about a dozen lines: the posture (Preserve / Salvage), what is reused, what is switched off, and behavior that must be kept. Decisions, not a description of how the code works]

## Architecture

### Workload Type and Starting Point
[What kind of service is this? Which seed project or existing repo it copies its patterns from.]

### Database
[Where does data live? Why this choice?]

### Dependencies
[What does this interact with?]

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [What needed deciding] | [What was chosen] | [Why] |

## Interfaces

### API Endpoints
[Endpoint definitions with request/response formats]

## Data Models

[Key data structures — tables, schemas, field definitions]

## Integration Points

[External systems and services this interacts with]

## Open Questions

[Unresolved decisions]
```

---

## Where to Store Technical Design Documents

The technical design document lives **inside its parent PRD's directory**, alongside the PRD itself and any other supporting materials. See `prd-writing-standards` for the full directory structure.

```
docs/prds/{prd-name}/          ← or docs/changes/{prd-name}/ — a bounded delivery, identical layout
  {prd-name}-prd.md
  technical-design.md          <-- here
  assumptions.md (if applicable)
```

### Naming Convention

Use the simple filename `technical-design.md`. There's no need to repeat the PRD name — the directory already provides that context.

A PRD has exactly one technical design (`phase-split`, `prd-roadmap`). A PRD spanning several services covers each in its own section; work that genuinely needs separate designs is more than one PRD (`prd-roadmap`).

### Cross-Repo Initiatives

If the feature spans multiple repositories, designate one repo as the home for the PRD directory (typically the one that owns the primary interface or orchestration) and put the technical design alongside the PRD there.

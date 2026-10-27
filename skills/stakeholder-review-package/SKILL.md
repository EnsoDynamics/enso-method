---
name: stakeholder-review-package
description: Create or refresh a self-contained HTML stakeholder review package from a PRD, its assumptions and mockups. Combines selected business requirements with every open assumption and contextual screens, so people can respond in one place. The review is a derived human-facing document, never an implementation specification.
---

# Stakeholder Review Package

Give business stakeholders one approachable document they can understand and answer. The PRD and technical design retain the complete implementation contract; the assumptions register retains the decisions and their evidence. The HTML is a dated review of those sources, not another source of requirements.

## Read and select

Read the full PRD, the whole current assumptions register, and relevant mockups. Read the technical design only where needed to resolve context. Follow the sources' own writing skills before changing them; preparing a review does not authorize changing requirements, inventing decisions or marking assumptions confirmed.

Select requirements by business consequence: changed procedures, permissions, money or data outcomes, consequential exceptions, scope exclusions, and behavior a stakeholder might reasonably reject. Include important settled rules as well as uncertain ones. Leave internal construction, test mechanics and project history in the source documents. Do not turn every acceptance criterion into a shorter bullet.

**Every open assumption gets exactly one answerable place in the HTML.** Include provisional answers and reopened decisions still needing attention. Exclude settled entries unless explicitly reopened in the register. Keep original IDs. Inventory the IDs before writing and reconcile them after generation; the supplied renderer checks registers with ID-bearing Markdown headings and a `Validated Assumptions` section. For other formats, produce and check an explicit inventory rather than claiming that parser covers them.

If no assumptions register exists, confirm the PRD has no open assumptions and use `assumptions_source: null`, `open_assumption_ids: []` and an `inventory_note` explaining the absence. Do not invent assumptions or create an empty register just for the renderer. If a register exists, include it; a missing named source is an error. Recheck for a register when refreshing or preparing to share.

A genuine **Blocking Open Question** has no proposed answer to confirm. Surface it directly and resolve it through `assumptions-document-writing` before producing a complete Confirm/Change review. Never invent an ID or proposal to fit the form, or silently leave the question out. The renderer rejects the method’s `### Blocking: ...` entries even with an explicit inventory.

## Organize around the work

Use one brief per PRD by default. Start with two sentences on the outcome and scope, followed by a few sections organized around workflows, features or business topics. Each section brings together:

- A short account of what the person will do and what changes.
- The relevant mockup beside that explanation, with readable text and an enlargement control. Group alternate screens in a labelled gallery; avoid a separate wall of screenshots.
- The assumptions for that section, each shown once with its proposed answer and response controls.

Label the navigation **In this review** and the section eyebrows **Section**. Label the columns **Key acceptance criteria & mockups** and **Assumptions to confirm**. The first is selected; the second contains every open assumption relevant to that section. Do not call the assumptions “highlights” or “most relevant assumptions.” Keep a prominent, labelled **Feedback on acceptance criteria or mockups** box in the acceptance criteria/mockups column, beside the material it refers to. On narrow screens, it stays with that material before the assumptions.

When an assumption already states a behavior, let its card do that work: do not repeat the proposal in the overview, a highlights list and an assumptions appendix. Link back to the card when needed elsewhere. Prioritize through section order and a small, explained emphasis on consequential decisions; never hide lesser assumptions behind a filter, an accordion or a link to another document. Every question, proposal and answer control is visible by default. Evidence and longer examples may use expandable details.

**Compress words, not decisions.** Preserve actors, values, exceptions, scope, uncertainty, relevant counterevidence and material alternatives. If one ID contains several choices, show them separately within its one card. A business-sensitive detail belongs beside the answer, not hidden as background. Do not invent confidence scores or reinterpret a technical-rework impact rating as business importance. Show the source's confidence in a compact, clearly labelled badge at the top of each assumption card, visible without expanding evidence. Preserve the source value; omit the badge when the source has no confidence. Keep its styling neutral so confidence is not confused with confirmation or business importance. Evidence and the rationale for the confidence may remain expandable.

A reviewer must be able to answer without opening the full PRD. Source links offer depth and traceability. One page is a useful goal for the narrative, not a cap on the decisions: a genuinely large decision set stays large, organized into bounded workflow sections.

## Preserve sources and freshness

Put a visible notice near the start: **For business review. Selected acceptance criteria and all open assumptions. Implementation must use the full PRD and technical design.** Make clear that the complete review includes every question, while partial feedback is welcome and unreviewed items remain unanswered.

Store the single HTML file beside the canonical PRD in the project's own Git repository. Derive `{name}` from the PRD filename by removing `.md` and a trailing `-prd`, if present. Use exactly `{name}-stakeholder-review.html`. For the method's standard layout:

```text
docs/prds/{name}/
  {name}-prd.md
  {name}-stakeholder-review.html
```

The same filename applies in `docs/changes/{name}/` or the PRD's existing directory. Refresh this file in place; the preparation date and version belong inside the HTML, with earlier versions retained by Git. Keep it in version control when committing is authorized.

**Keep and send only the HTML.** It embeds the review content, images, scripts and non-executable authoring data. The renderer reads that authoring data to regenerate the review and check freshness; no companion JSON is needed. Use temporary JSON for the first build or while editing the embedded authoring data, then remove it after verifying the HTML retains it. The authoring data holds condensed prose and source mappings, not another canonical assumptions register. Each displayed rule and assumption points to its source, using criterion IDs and assumption IDs; link to actual sections rather than an entire long document where possible.

A self-contained file is a snapshot. Show its preparation date and version and link to the current canonical documents. Record source hashes, including mockup sources and their dependencies, and check freshness before sharing. Refresh the brief after source changes; do not claim that links to a moving branch make embedded content live. Previous feedback keeps its version and IDs; compare against current sources before applying it through `assumptions-document-feedback`. Never carry a confirmation onto a changed question automatically.

Render canonical mockups into embedded images or reuse their markup safely. Record each screen's source and ID. These are generated views, not independently maintained designs. Preserve the depicted scenario, including any deliberate later-release state, and label that scope plainly. A contradiction with current requirements is a source issue to resolve, not something a disclaimer repairs. Do not embed executable third-party prototypes with access to the review's answers. Do not make private material publicly accessible to obtain an image URL.

## Build the HTML

Use [the authoring contract](references/stakeholder-review-authoring.md) and the supplied [renderer](scripts/render_review.py) with [the template](assets/stakeholder-review.html). They provide a neutral responsive layout, decision cards, image enlargement, optional browser-local drafts, a portable saved copy and feedback export. Adapt the presentation where it improves comprehension; preserve the coverage and feedback invariants.

Use inline CSS and small vanilla JavaScript, system fonts and embedded images. No CDN, telemetry, server, third-party form or client-specific branding. Retain the template’s small “Prepared with the Enso Method” footer, embedded Enso mark and link to https://ensomethod.org; keep the review itself visually neutral. Compress images without making screen text hard to read; prefer a file under 1 MB when feasible and report its actual size. Do not omit a necessary screen to hit a byte target. All substantive content remains readable without JavaScript; enhanced controls should explain when JavaScript is needed.

Feedback controls start unanswered and offer only **Confirm** and **Change**. A reviewer may leave an item untouched when they cannot decide; silence is not approval, disagreement or evidence that they read it. Expressed uncertainty belongs under Change with a comment; there is no separate discussion or defer option. Never default to approval or provide "approve all." Mark Change with no explanation as incomplete. Preserve comments even when no button is selected, labelling them as comment-only feedback rather than confirmation.

Export a self-contained reply in two parts, keeping the review title, version, preparation date, reviewer and export timestamp at the top:

1. **Reviewer's feedback:** assumption IDs with Confirmed, Change, incomplete Change or comment-only status and the reviewer's full comments. Separate entries with a line of dashes; do not repeat questions, proposals or source links here. Include acceptance criteria and mockup feedback in full, clearly distinguished from assumption answers and labelled with its section. Collect all IDs with neither a selection nor a nonblank comment into one **No response given** line (or None). These assumptions and their confidence remain unchanged and unconfirmed; do not infer why they were skipped.
2. **Wording reviewed — reference only:** for every item with a selection or nonblank comment, include its ID, exact displayed question and proposal (preserving paragraphs), and source references. Separate entries with dashes. Identify this as historical context, not additional feedback, and instruct the processor to compare it with the current assumption before applying the response. Omit untouched items' wording; their IDs remain in the first part.

Retain every reviewer comment and section note without summarizing or rewriting it. Download and clipboard both include both parts. The appendix makes the reply interpretable without a Git commit or access to an old HTML file; the version and links provide traceability, not a substitute for the wording reviewed.

Explain the two downloads by purpose: **Save editable copy (.html)** keeps the review and answers for the reviewer to reopen and edit; **Download reply (.txt)** produces the response to return to the requester. Add **Copy reply to clipboard** alongside the TXT download, using the same complete feedback text so reviewers can paste it into an email or message. Confirm copying only after the browser reports success; if copying is unavailable or denied, explain that visibly and point to the TXT download. Put a short explanation beside each action. Keep the downloads separate; no ZIP or automatic paired download. Downloading saves a local file; it does not send anything or update canonical sources. State that beside the actions, followed by: **Send the downloaded reply (.txt), or paste the copied reply into a message to the person who requested this review.** This instruction works for email, chat or another sharing channel. If browser storage fails, say so and name the editable-copy action.

## Check before handing over

- Compare every proposed rule to its source for meaning, especially exceptions and release boundaries. Verify all open assumption IDs appear once and no settled ID is asked again.
- Check source URLs and access; a private-repo URL may require recipient access. Do not silently publish material to solve access.
- Render and inspect the HTML at a phone width and desktop width. Inspect each included screen at readable size. Exercise responses, incomplete corrections, draft restore, saved-copy reopening, enlargement, feedback download, clipboard success and failure, and keyboard navigation. Confirm source confidence stays visible with evidence collapsed at both widths, and copied replies contain the same information as downloaded replies. Verify untouched IDs appear only in the grouped no-response list, comment-only and incomplete Change entries survive with their reviewed wording, the appendix preserves the displayed wording, unreviewed items never count as approved, and no runtime network request is needed.
- Run the renderer's freshness check and its tests. A matching hash proves which sources were used, not that the prose faithfully summarizes them; perform both checks.
- For a public skill or reusable example, scan every changed file for client names, URLs, record IDs, screenshots and operational facts. Examples must be fictional and unrelated to the private pilot. Keep pilot content and audit evidence in the private project.

Deliver the single HTML file for review, report its size and any meaningful limitation, and open it for the user when the environment supports that. Do not send, publish, commit or add a new review gate merely because this skill ran.

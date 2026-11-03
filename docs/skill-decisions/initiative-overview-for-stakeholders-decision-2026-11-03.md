# Initiatives get a one-page overview for stakeholders (decision record, 2026-11-03)

Maintainer notes for `skills/initiative-breakdown/SKILL.md` (Step 5, "The initiative overview") and the matching lines in `stakeholder-review-package`, `assumptions-document-feedback`, `implement-from-discovery`, `autonomous-prd-refinement`, `prd-writing-standards` and `requirements-intake`. This file is outside every skill directory and is not loaded by any skill.

## The problem

- **A review package arrives with no picture of the whole.** Each package covers one PRD. When an initiative is cut into several, the stakeholder who gets the first one sees a narrow slice and cannot tell what the overall work is, how the pieces fit, or why this one comes first.
- **Nothing the method produced was fit to send.** The PRD list holds the order and dependencies, but it is a markdown table for the people running the work, linking into the PRD contracts.

## Options considered

1. **A slimmer review covering every PRD.** Rejected: the packages already select. Cutting further means fewer questions answered, not better orientation.
2. **Have `stakeholder-review-package` write it.** Rejected: that skill works from one PRD, and the overview is needed before most PRDs are written. Only `initiative-breakdown` has the whole initiative in view.
3. **Have `requirements-intake` write it.** Rejected: intake quotes and never summarizes, runs before any cut exists, and also runs for work that is one PRD.
4. **Chosen:** `initiative-breakdown` writes a one-page HTML overview beside the PRD list, and each review package names its place in the order and lists the overview as a source, so it is linked and its changes make the package stale.

## Decisions and why

- **Derived and decides nothing.** It restates the brief and the PRD list for a business reader, so it cannot become a second source of requirements.
- **No assumptions and no status.** Assumptions keep their one answerable place in each PRD's package. Status changes often and would leave a sent page stale; the overview changes only when a PRD's name, order or outcome does.
- **A screen or two, and nothing but what changes and the PRDs in order.** A stakeholder who opens a long page closes it. Dependencies, the review process and background were left out: the order already shows the first, and the rest is length that costs the reader more than it gives.
- **HTML in the review template's look,** because stakeholders already receive packages that way. No renderer of its own: it has no feedback controls to render.
- **Intake hands off to `initiative-breakdown` directly** when its record is bigger than one PRD, matching `using-the-enso-method`, instead of routing through `prd-writing-standards`' size check.

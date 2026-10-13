# Deliverable review: looking at visual deliverables, and references that are not truth (decision record, 2026-10-11)

Maintainer notes for the "Look at Visual Deliverables" checklist item and the "Mockups and inherited material are references, not truth" rule in `skills/deliverable-review/SKILL.md`, and the two context notes Step 2 now gathers for them. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing how the review treats mockups or other visual work.

## The problem

A PRD with 15 mockup states went through five rounds of deliverable review. Every reviewer read the mockup page's source, the HTML and the data each screen is drawn from, and none rendered a screen. Mockup findings came up in four rounds, all of them about content: dates, labels, missing rows. Nobody checked what a receiver on a phone-sized handheld would see, which is where layouts break. The checklist never said a visual deliverable has to be looked at, and "re-read every changed file from disk" steered reviewers to the source.

The same work showed a second gap. The mockups started from a stakeholder's handoff, and the session's research then established facts that contradicted parts of it. The review's only rule on sources was "spec documents are the source of truth", which a reviewer can read as making the handoff's mockups authoritative too.

## Decisions and why

- **A visual deliverable is reviewed rendered, as images the reviewer opens.** Reading the source can find what a screen says but not what it looks like, so a source-only reading is not a review of it, and a reviewer who could not render it reports that as a finding.
- **Every screen or state, at the sizes the spec names, or at least the smallest and largest.** Layout defects live at the edges, mostly the narrowest width. (Narrowed to visuals that are the product itself on 2026-10-12, below.)
- **Device emulation for phone widths, and a second rendering before reporting a defect.** A plain headless window-size setting has clipped the right edge of mockups at phone width, producing a defect that wasn't there.
- **The reviewer says what it viewed.** Without that, "reviewed" can still mean "read the source".
- **Mockups, prototypes, sample data and inherited material are references, not truth.** When the work has established a fact with high confidence that contradicts one, the reference changes, not the work. The work's own mockup is corrected; an original kept unedited as a record of a handoff stays as it is, and the work notes where it departs; a reference that contradicts a stakeholder's ruling is raised, never quietly changed either way. This sits beside "spec documents are the source of truth" rather than replacing it: the written requirement still governs its own mockups.

## Options considered

1. **A separate visual-review skill.** Rejected: the problem was a review that skipped part of its deliverable, and a second skill would need its own trigger that sessions forget to pull.
2. **Leave rendering to the main agent before review.** Rejected: the reviewer would then judge someone else's screenshots, chosen by the agent that made the work, which defeats the fresh eyes.

## Added the same day: keeping the looking manageable

The first rendered review looked at about 70 screenshots in one sub-agent, opening image after image with nothing written down between them. It worked, but nothing kept findings from early screens from fading or blurring together by the end. Three additions:

- **A layout script runs before the looking.** Overflow, off-screen elements and sideways scrolling are measurable across every state and size in seconds, and the reviewer that did this found it reliable; eyes then go to what a script can't judge.
- **One screen at a time, with a running notes file.** Each screen's findings are written before the next image is opened, so the report is built from notes, not from memory of 70 images.
- **More than about 20 images splits across parallel sub-agents by screen group,** each doing only the visual item, merged with the main review. The threshold is a rule of thumb, not a measured limit.

## Added the same day: wrong mockups are redrawn, in their own medium

The same PRD's later rounds kept finding mockups that disagreed with a criterion, and the cheap response, a note saying where the drawing is wrong, leaves a builder with two specifications. The user ruled that the PRD and its mockups must both show the intended behaviour when the work ends. The rule went into `prd-writing-standards` ("Mockups Show What the Criteria Require"), since that skill makes mockups, and `deliverable-review`'s fix step points to it.

- **Regenerate in the mockup's own medium.** The user first proposed sending every regeneration to Codex, whose image generation is stronger. That was narrowed: code mockups (HTML, SVG, generated pages) are edited and re-rendered, because an image generator redraws pixels, cannot keep record numbers exact or states consistent, and produces nothing a script can measure or a diff can show. Image generation is for mockups that exist only as images.
- **Codex from Claude Code was tested, not assumed.** On 2026-10-11, `codex exec` (CLI 0.162.1) generated a test image with its built-in `image_gen` tool, signed in through ChatGPT with no `OPENAI_API_KEY`, and saved it under `~/.codex/generated_images/<session>/`. The output has to be copied into the workspace.
- **Fallback:** rebuild as HTML or SVG and render it; failing that, an open finding, never a note.
- **Handoff packages stay apart and unedited.** The user ruled that nothing in a handoff package is edited, and that the package lives in its own location, labelled by source and date, never mixed with the PRD's files, so no one confuses a handoff original with the requirements the PRD produced.
- **A fix is new content.** Twice in that PRD's review, one round's fix caused the next round's Medium: a criterion sentence added for one screen contradicted another criterion. The fix step now says to check each added sentence against its neighbours before the next round.

## Added the same day: a case walk when one area keeps producing findings

In that PRD's rounds 9 to 12, the text reviewer found a new Medium each round, every one an edge case in the same flow (the supplier arrival), and some caused by the previous round's fix. Round 13 told the reviewer to walk the flow's cases instead (how it is entered, the states a parcel can be in, the inputs its scan box takes, the connection states, the save) and to name the sentence that settles each. It covered about 40 cases, found 34 settled, and reported the remaining one Medium and five Lows together. Step 3 now asks for a case walk once the same part has produced a Medium or High finding in two rounds running.

## Revised 2026-10-12: design references are reviewed for content, at one width

"Every screen or state, at the sizes the spec names, or at least the smallest and largest" now applies only to a visual that is the product itself: a built page, a published site, an image that ships. A design reference, such as a mockup in a requirements document or a diagram in a design, is rendered once per screen at the width its main users work at and reviewed for what it says. Its layout is reported only where it makes content unreadable or misleading, and a delta round renders only the screens the fixes affected.

The rule was too costly for requirement mockups. On another PRD it meant about 80 images a round over 14 rounds, and most of the layout findings were polish the built product's own review would catch. The user ruled that layout across screen sizes is beyond what business requirements need: the sizes a PRD names are requirements on the product, not on its mockups. The reasoning is in `autonomous-prd-refinement-decision-2026-10-12.md`.

## Revised 2026-10-12: visual means the change is about how something looks

Step 2 used to call anything a person looks at a visual deliverable, so a change that only renamed a skill on a website was reviewed as the product itself: 13 screenshots at desktop and phone widths, Playwright installed for the purpose, about 49 tool calls. Nothing could be found, because the new name was shorter than the old one and sat in unchanged markup. Now the work is visual when what it delivers or changes is how something looks (a mockup, a graphic, layout or styling, a new screen). A change to what a page says or does is reviewed as text or code, gets at most one look at the affected spot when there is a specific reason to suspect the layout breaks, and the review says in one line why it rendered nothing.

The user chose a broad test over a list of cases such as "same-length or shorter text". A rule that names cases has to keep growing, and a reviewer judging what the change could break covers the cases nobody listed. The escape hatch stays because a functional change can still break a layout: a new button, a much longer message, an extra table column.

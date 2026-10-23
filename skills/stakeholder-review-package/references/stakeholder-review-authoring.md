# Stakeholder Review Package Authoring Contract

The renderer uses Python's standard library. Keep only the generated HTML beside the PRD, using the exact naming rule in [Preserve sources and freshness](../SKILL.md#preserve-sources-and-freshness). It retains the complete authoring object below in its non-executable `authoring-data` block. The renderer can read this HTML directly; temporary JSON is an authoring convenience, never a required repository file or attachment. All prose fields are plain text and HTML-escaped. Source citations use a source key, optional section fragment, and a human-readable label (usually criterion or assumption IDs).

```json
{
  "title": "Community class bookings",
  "subtitle": "Let residents reserve a place and manage a booking.",
  "scope": "This release covers booking and cancellation. Payment is outside this release.",
  "date": "2026-01-15",
  "assumptions_source": "assumptions",
  "sources": {
    "prd": {"path": "docs/prds/class-bookings/class-bookings-prd.md", "url": "https://example.org/project/class-bookings-prd", "label": "Full PRD"},
    "assumptions": {"path": "docs/prds/class-bookings/class-bookings-assumptions.md", "url": "https://example.org/project/class-bookings-assumptions", "label": "Assumptions register"}
  },
  "sections": [{
    "id": "booking",
    "title": "Reserve a place",
    "intro": "Residents choose a class and see whether places are available.",
    "rules": [{"text": "A full class offers a waiting list.", "refs": [{"source": "prd", "anchor": "waiting-list", "label": "AC-BOOK-01"}]}],
    "mockups": [],
    "decisions": [{
      "id": "RULE-001",
      "title": "How late can someone cancel?",
      "proposal": ["Residents may cancel until the class starts."],
      "attention": "Affects last-minute availability",
      "evidence": "The booking brief specifies cancellation but gives no cutoff.",
      "confidence": "70%",
      "refs": [{"source": "assumptions", "anchor": "rule-001-cancellation", "label": "RULE-001"}]
    }]
  }]
}
```

Fields shown above are required except `attention`, `confidence`, and citation `anchor`. `attention` explains the consequence without labelling other decisions optional. Use several short `proposal` paragraphs when one ID contains several independently meaningful conditions. A plain-language title must not bury the choice behind an internal ID. Evidence can include existing source examples and contrary evidence; decisions that depend on that evidence must keep the needed detail in the visible proposal.

When no assumptions register exists and the PRD has no open assumptions, set `assumptions_source` to `null`, omit the absent register from `sources`, and supply `open_assumption_ids: []` with an `inventory_note` explaining the absence. Decisions must then be empty; selected PRD rules can still be reviewed. Do not use this form when a register exists or to suppress open questions. Recheck for a register when refreshing or preparing to share; hashes cover listed sources, not newly created files.

`mockups` entries contain `id`, `title`, `file` (a basename under `--images-dir`), `alt` (a meaningful description), `caption` (scenario or scope), and `refs`. Each is an existing canonical screen rendered as PNG, JPEG or WebP. Optional `focus: "bottom"` initially scrolls a tall preview to its bottom when that is where the behavior being reviewed appears; the whole image remains available. Add the canonical mockup files and their stylesheet/script dependencies to `sources`, so changes invalidate the snapshot. The temporary raster files need not be committed separately; the output embeds them. Rerender them from those sources when rebuilding. Never put a private capture in this skill's assets.

Every section may have zero or more rules, mockups and decisions. The renderer labels selected acceptance criteria separately from assumptions, places an acceptance criteria and mockup feedback box in the same column as those materials, and exports that feedback with its section title. Assumptions offer only Confirm or Change; Change requires a comment, including when the reviewer is uncertain. The two download actions distinguish an editable HTML copy to keep from a TXT reply to return to the person who requested the review, using any sharing channel. The complete document's decision IDs must exactly equal the open IDs in the assumptions source. The parser recognizes headings starting with IDs such as `RULE-001` and excludes headings after `## Validated Assumptions`. It refuses an ambiguous nonempty register with no IDs, and rejects unresolved `### Blocking: ...` questions even alongside numbered assumptions or an explicit inventory. Those questions have no proposal to confirm: surface and resolve them through the source-authoring workflow before generating this review. For a genuinely empty register, use `"open_assumption_ids": []`; for other register formats, supply `open_assumption_ids` after manually checking the inventory. This overrides only parsing, never the completeness obligation. Record why an explicit inventory was needed in `inventory_note`.

Build and check (substitute actual paths):

```bash
# First build: write the authoring object to a temporary JSON file.
python3 <skill>/scripts/render_review.py \
  --repo-root <project> --input <temporary-authoring-json> \
  --images-dir <temporary-rendered-screens> --output <prd-directory>/<name>-stakeholder-review.html

# Thereafter: use the single stored HTML as both input and output.
python3 <skill>/scripts/render_review.py \
  --repo-root <project> --input <prd-directory>/<name>-stakeholder-review.html \
  --images-dir <temporary-rendered-screens> --output <prd-directory>/<name>-stakeholder-review.html
python3 <skill>/scripts/render_review.py \
  --repo-root <project> --input <prd-directory>/<name>-stakeholder-review.html \
  --output <prd-directory>/<name>-stakeholder-review.html --check
python3 -m unittest discover -s <skill>/scripts -p 'test_*.py'
```

For changed requirements, update the embedded authoring object to match the current sources before rebuilding. It can be extracted with the renderer's `load_authoring(Path(...))` helper, edited as temporary JSON and passed back to `--input`; verify that the generated HTML retains the object, then remove the temporary file. Do not hand-edit the rendered content while leaving its authoring data unchanged. Re-render canonical mockups when rebuilding. A rebuild starts unanswered; it never applies answers embedded in a reviewer's saved copy.

Older HTML without `authoring-data` needs its original JSON for one rebuild. Verify that the new HTML retains the authoring object and passes freshness checks before removing that old sidecar.

Source paths must be repo-relative; URLs must be HTTPS. The generated source manifest records file hashes, the canonical authoring-content hash, template/renderer hashes and hashes of the actual embedded images. Changing a capture changes the review version. The freshness check verifies embedded bytes against that manifest; also pass `--images-dir` to compare against newly rendered captures. The visible version identifies this snapshot, not an approval. Current-source links can change later; exported feedback records the version and exact proposal reviewed. The freshness command needs the current local checkout and the stored review HTML; the HTML makes no live freshness claim.

For shareable links, use the repository's current shared branch and checked section anchors. Before sending, ensure the canonical files are published and accessible to the intended readers. Keep unpublished pilot artifacts local until their release is authorized.

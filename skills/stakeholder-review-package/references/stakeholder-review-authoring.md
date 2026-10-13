# Stakeholder Review Package Authoring Contract

The renderer uses Python's standard library. Keep the editorial JSON in the project, not in the public skill. All prose fields are plain text and HTML-escaped. Source citations use a source key, optional section fragment, and a human-readable label (usually criterion or assumption IDs).

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

`mockups` entries contain `id`, `title`, `file` (a basename under `--images-dir`), `alt` (a meaningful description), `caption` (scenario or scope), and `refs`. Each is an existing canonical screen rendered as PNG, JPEG or WebP. Optional `focus: "bottom"` initially scrolls a tall preview to its bottom when that is where the behavior being reviewed appears; the whole image remains available. Add the canonical mockup files and their stylesheet/script dependencies to `sources`, so changes invalidate the snapshot. The temporary raster files need not be committed separately; the output embeds them. Rerender them from those sources when rebuilding. Never put a private capture in this skill's assets.

Every section may have zero or more rules, mockups and decisions. The renderer labels selected requirements separately from assumptions, places a requirements/mockup feedback box in the same column as those materials, and exports that feedback with its workflow title. Assumptions offer only Confirm or Change; Change requires a comment, including when the reviewer is uncertain. The two download actions distinguish an editable HTML copy to keep from a TXT reply to return. The complete document's decision IDs must exactly equal the open IDs in the assumptions source. The parser recognizes headings starting with IDs such as `RULE-001` and excludes headings after `## Validated Assumptions`. It refuses an ambiguous nonempty register with no IDs, and rejects unresolved `### Blocking: ...` questions even alongside numbered assumptions or an explicit inventory. Those questions have no proposal to confirm: surface and resolve them through the source-authoring workflow before generating this review. For a genuinely empty register, use `"open_assumption_ids": []`; for other register formats, supply `open_assumption_ids` after manually checking the inventory. This overrides only parsing, never the completeness obligation. Record why an explicit inventory was needed in `inventory_note`.

Build and check (substitute actual paths):

```bash
python3 <skill>/scripts/render_review.py \
  --repo-root <project> --input <editorial-json> \
  --images-dir <temporary-rendered-screens> --output <review-html>
python3 <skill>/scripts/render_review.py \
  --repo-root <project> --input <editorial-json> \
  --output <review-html> --check
python3 -m unittest discover -s <skill>/scripts -p 'test_*.py'
```

Source paths must be repo-relative; URLs must be HTTPS. The generated source manifest records file hashes, the editorial input hash, template/renderer hashes and hashes of the actual embedded images. Changing a capture changes the review version. The freshness check verifies embedded bytes against that manifest; also pass `--images-dir` to compare against newly rendered captures. The visible version identifies this snapshot, not an approval. Current-source links can change later; exported feedback records the version and exact proposal reviewed. The freshness command needs the current local checkout and editorial input; the HTML makes no live freshness claim.

For shareable links, use the repository's current shared branch and checked section anchors. Before sending, ensure the canonical files are published and accessible to the intended readers. Keep unpublished pilot artifacts local until their release is authorized.

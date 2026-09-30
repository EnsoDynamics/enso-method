#!/usr/bin/env python3
"""PreToolUse hook: name the governing skill when an assumptions document is edited.

WHY THIS EXISTS. An assumptions document is edited far more often by sessions doing
something else — recording a ruling while building a phase — than by sessions that set
out to edit it. Those sessions have loaded `implement-from-requirements`, not
`assumptions-document-writing`, so the format rules are simply not in context, and the
document drifts a little on each pass: correction history piling up in the body, update
paragraphs stacking in the header, status narrative in headings, a checklist growing at
the top.

A directive comment at the top of the file only helps when the model reads the top of the
file, and the reason these documents drift is that they get long enough to read in pieces.
A PreToolUse hook is read every time, however the file was opened.

WHAT IT DOES. Emits `additionalContext` naming the two skills, and NOTHING ELSE.

    IT DELIBERATELY DOES NOT EMIT `permissionDecision`. On PreToolUse, a
    `permissionDecision` of "allow" does not mean "do not block" — it means "skip the
    permission prompt", silently auto-approving every write to any assumptions document on
    the machine. `additionalContext` on its own injects the reminder and leaves the user's
    own permission settings to decide the edit, which is the only correct behaviour for a
    hook whose entire job is to say something.

It fires once per (session, document) so a session making twenty edits is told once, and it
fails open on every path: any error, and the edit proceeds with no reminder.

INSTALL. See "Adopting This Skill" in ../SKILL.md. Registered in ~/.claude/settings.json
under PreToolUse with matcher "Edit|Write|MultiEdit".
"""

import hashlib
import json
import pathlib
import sys
import tempfile

#: The tools that change a file's bytes AND can carry an assumptions document.
#: `NotebookEdit` is deliberately absent: it passes `notebook_path` rather than
#: `file_path`, and an assumptions document is never a notebook. Keep this set in step with
#: the `matcher` in settings.json — a tool in one and not the other is dead code.
EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}

#: The document is colocated with its PRD as `docs/prds/{prd}/assumptions.md` (or under
#: `docs/changes/`). Matching on the filename rather than the directory covers both roots,
#: and also covers a repo that names it `{feature}-assumptions.md`.
def _is_assumptions_doc(file_path: str) -> bool:
    name = pathlib.PurePath(file_path).name.lower()
    return name == "assumptions.md" or name.endswith("-assumptions.md")


REMINDER = (
    "This file is an assumptions document, whose format is owned by the "
    "`assumptions-document-writing` skill. Load that skill with the Skill tool BEFORE "
    "making a structural change here — adding or rewriting an entry, folding a "
    "stakeholder's answer, moving an item to the validated table, or editing the header — "
    "and read its section 'Editing an Existing Document', which governs edits to a "
    "register that already exists. If you are folding stakeholder feedback, load "
    "`assumptions-document-feedback` too. Five rules registers actually drift on, so check "
    "them even for a small edit: (1) ONE `**Last Updated**` line, replaced rather than "
    "stacked — the commit log is already the narrative of edits, so do not keep a second one "
    "by hand; (2) superseded entry text comes OUT rather than being layered under the live "
    "entry — version control holds it and the ruling date is the handle, and do NOT start a "
    "history file beside the register; (3) no "
    "checklist, ranking or triage block at the top of the document; (4) a heading carries "
    "at most the question, a status marker, a tag from the closed vocabulary and a "
    "confidence — no narrative; (5) an entry the stakeholder already answered, left in the body, must "
    "say on its first line what has changed since they answered. A fix that only makes this "
    "one edit look right, while leaving the document in a shape the skill forbids, is not "
    "a fix."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    try:
        if payload.get("tool_name") not in EDIT_TOOLS:
            return 0

        file_path = (payload.get("tool_input") or {}).get("file_path") or ""
        if not file_path or not _is_assumptions_doc(file_path):
            return 0

        # ONCE PER SESSION PER DOCUMENT. Non-blocking context is cheap, but repeating it
        # on every one of twenty edits is noise that trains the reader to skip it.
        session = str(payload.get("session_id") or "no-session")
        key = hashlib.sha256(f"{session}\0{file_path}".encode()).hexdigest()[:32]
        marker = pathlib.Path(tempfile.gettempdir()) / "claude-assumptions-hook" / key
        try:
            if marker.exists():
                return 0
        except OSError:
            pass

        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": REMINDER,
                }
            },
            sys.stdout,
        )
        sys.stdout.flush()

        # MARKED ONLY AFTER THE REMINDER IS ACTUALLY OUT. Touching the marker before the
        # write meant a failed write (closed stdout, broken pipe) suppressed this
        # document's reminder for the rest of the session — the one direction this hook
        # must not fail in.
        try:
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.touch()
        except OSError:
            pass
    except Exception:
        # FAIL OPEN, ALWAYS. This hook's worst possible behaviour is stopping an edit.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook: name the session from the prompt's first line.

The `continuation-prompt` skill puts the chat name alone on line one of every
prompt that starts a new chat, e.g.

    PROJ-2718 api logs impl

    Use implement-from-discovery. PROJ-2718: ...

Claude Code cannot rename its own session from inside a conversation, but a
UserPromptSubmit hook may return `sessionTitle` (Claude Code 2.1.94 and later),
which is what `/rename` would have set. Two rules, checked in order:

1. `Chat: <name>` as the first non-blank line sets the title on ANY prompt. This
   is the explicit form: use it to rename a session mid-conversation.
2. On the FIRST prompt of a session only, a bare first line that looks like a
   name (at most 40 characters, no trailing punctuation, not a slash command,
   an @-mention or a pasted attachment tag, followed by a blank line and then
   the body of the prompt) becomes the title. A one-line
   prompt is never a name, and later prompts never match this rule, so
   "yes\\n\\ngo ahead" mid-session renames nothing.

Both rules look inside a leading `<pasted_content id="...">` tag: the VS Code
extension wraps pasted text in one, so a pasted prompt's name line is the line
after the tag, not the tag itself.

Why not always require the `Chat:` prefix: the VS Code extension seeds a new
tab's label from the raw first prompt and does not pick up a hook-set title
until its session list refreshes, so the first characters of line one are what
the user sees in the tab. A prefix there wastes the only real estate that matters.

Any other prompt passes through untouched, and the hook never blocks a prompt:
bad input exits 0 silently.

Install (once) in ~/.claude/settings.json:

  {
    "hooks": {
      "UserPromptSubmit": [
        { "hooks": [ { "type": "command",
                       "command": "python3 ~/.claude/skills/continuation-prompt/hooks/session-title-from-chat-line.py",
                       "timeout": 5 } ] }
      ]
    }
  }

Adjust the path if this skills repo is not linked under ~/.claude/skills.
Test without Claude Code (printf, not echo: zsh and sh `echo` turn the \\n into a
real newline, which strict JSON rejects):

  printf '%s' '{"prompt":"ph2 orderN impl\\n\\nUse implement-from-requirements."}' \\
    | python3 session-title-from-chat-line.py
"""
import json
import os
import re
import sys

MAX_LEN = 60          # hard cap on the title we return
BARE_NAME_MAX = 40    # a bare first line longer than this is a sentence, not a name
PASTE_OPEN = re.compile(r'<pasted_content\b[^>\n]*>[ \t]*\n')


def is_first_prompt(event: dict) -> bool:
    """True when the session transcript has no user message yet.

    Claude Code passes `transcript_path`; before the first prompt is written the
    file is absent or holds no `"type":"user"` line. When the field is missing
    (an older Claude Code, or a hand-built test event) assume first prompt.
    """
    path = event.get("transcript_path")
    if not isinstance(path, str) or not path:
        return True
    try:
        with open(os.path.expanduser(path), "rb") as fh:
            for line in fh:
                if b'"type":"user"' in line:
                    return False
    except OSError:
        return True
    return True


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0  # not JSON; never block the prompt
    if not isinstance(event, dict):
        return 0
    prompt = event.get("prompt")
    if not isinstance(prompt, str):
        return 0

    text = prompt.lstrip()
    # The VS Code extension (2.1.280 and later) wraps a pasted prompt in
    # <pasted_content id="..."> ... </pasted_content id="...">; the name line
    # is the first line inside it.
    wrapper = PASTE_OPEN.match(text)
    if wrapper:
        text = text[wrapper.end():].lstrip()
    lines = text.split("\n")
    first = lines[0].rstrip()
    title = None

    explicit = re.match(r"^Chat:\s*(.+?)\s*$", first)
    if explicit:
        title = explicit.group(1)
    elif (
        first
        and len(first) <= BARE_NAME_MAX
        and not first.endswith((".", "?", "!", ":", ","))
        and not first.startswith(("/", "@", "[", "<"))
        and len(lines) > 2
        and lines[1].strip() == ""
        and any(l.strip() for l in lines[2:])
        and is_first_prompt(event)
    ):
        title = first

    if not title:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "sessionTitle": title[:MAX_LEN],
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())

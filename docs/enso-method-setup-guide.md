# Enso Method Setup Guide

Everything past the one-line install: plugging in your own engineering standards, the
recommended global instructions, the optional hooks, and forking. Start with the
[README](../README.md) if you haven't installed the skills yet.

## Install and update

Install with the [skills CLI](https://skills.sh), which supports Claude Code, Codex and most
other coding agents:

```bash
npx skills add EnsoDynamics/enso-method -g                           # every agent it finds on this machine
npx skills add EnsoDynamics/enso-method -g -a claude-code -a codex   # only these two
npx skills update -g                                                 # later, to update
```

`-g` installs for your user rather than for one project.

Or install the same skills as a plugin. A plugin names each skill `enso-method:<skill>`, so it
cannot collide with a same-named skill from another source:

```bash
claude plugin marketplace add EnsoDynamics/enso-method        # Claude Code
claude plugin install enso-method@enso-method
claude plugin marketplace update enso-method                  # later, to update
claude plugin update enso-method@enso-method

codex plugin marketplace add EnsoDynamics/enso-method         # Codex
codex plugin add enso-method@enso-method
codex plugin marketplace upgrade enso-method                  # later, to update
```

Claude Code still accepts the bare `/prd-writing-standards` unless another skill uses that
name. Codex matches plugin skills only by their full name: pick them from the `$` menu or type
`$enso-method:prd-writing-standards`. Claude Code doesn't update plugins from other
marketplaces on its own; to have it do so, turn on auto-update for `enso-method` under
`/plugin` → Marketplaces. Use one install method, not both, or every skill loads twice.

## Plugging in your house engineering standards

The method carries principles, not stack opinions. Your team's own standards (language,
frameworks, project layout, configuration, deployment, naming) plug in without forking the
method:

1. Add a line to the project's `AGENTS.md`, one per standard:
   `Engineering standards: <skill name or file path>` — a skill you install alongside these,
   or a file in the repo.
2. For Claude Code, put `@AGENTS.md` in `CLAUDE.md` (an import), or symlink `CLAUDE.md` to
   `AGENTS.md`.

Sessions load what the line names alongside `engineering-principles`. Your standards win on
stack, style and tooling; the method's principles still apply.

The method ships no seed projects. For new software, your standards can name a seed project
or an existing repo whose patterns new work should copy — CI/CD, logging, configuration,
layout — and a technical design says which one it follows.

### Working across several organizations

Your own work plus clients or partners, say: each organization has its own standards, and
you may not be able to add a line to every repo you work in. If you keep one folder per
organization (e.g. `~/devel/<github-org>/`), put a map in your global instructions file
(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`), keyed by those folders, with a default for
everything else:

```markdown
- ENGINEERING STANDARDS — chosen by where the repo lives; a repo whose own AGENTS.md names engineering standards uses those instead:
  - Organization A, `~/devel/org-a/`: `Engineering standards: org-a-engineering-standards`
  - Organization B, `~/devel/org-b/`: `Engineering standards: ~/devel/org-b/ai-skills/development-practices/SKILL.md`
  - Everything else: `Engineering standards: my-org-engineering-standards`
```

Name every standards skill after its organization: `<org>-engineering-standards`, not a
generic name like `development-practices`. Skills are installed into one folder per tool,
keyed by name, so on a machine that installs several organizations' skills, two generic
names collide and one silently wins. An organization-specific name also marks it as that
organization's standards, not part of the method. Where you can't rename a skill, name it by
file path instead, as Organization B does above.

## Recommended global instructions

Add these lines to the instructions file your tools read (`~/.claude/CLAUDE.md`,
`~/.codex/AGENTS.md`), so hand-offs between chats and edits to assumptions registers go
through their skills:

> - CONTINUATION PROMPTS: Whenever asked for a prompt to paste into a new chat, or when a skill hands work to a fresh chat, use the `continuation-prompt` skill. If a prompt you receive opens with a short name alone on its first line (or a `Chat:` line) and you have a tool that sets the thread or session title, set it to that name before anything else; if you have no such tool, say nothing about it (where the optional title hook is installed, it has already set the title).
> - ASSUMPTIONS DOCUMENTS: Before editing any `assumptions.md` (or a `*-assumptions.md`), load the `assumptions-document-writing` skill and read its "Editing an Existing Document" section — most edits to these files are made in passing by sessions doing something else, which is how the format drifts.

## Optional Claude Code hooks

Two hooks ship with the skills; merge them into `~/.claude/settings.json`, keeping any hooks
already there:

- `continuation-prompt/hooks/session-title-from-chat-line.py` (`UserPromptSubmit`) — turns
  a continuation prompt's first-line chat name into the session title.
- `assumptions-document-writing/hooks/assumptions-doc-skill-reminder.py` (`PreToolUse`,
  matcher `Edit|Write|MultiEdit`) — reminds any session editing an assumptions register to
  follow `assumptions-document-writing`. It only adds context; it never approves or blocks
  an edit.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "timeout": 5,
          "command": "python3 ~/.claude/skills/continuation-prompt/hooks/session-title-from-chat-line.py" } ] }
    ],
    "PreToolUse": [
      { "matcher": "Edit|Write|MultiEdit",
        "hooks": [ { "type": "command", "timeout": 5,
          "command": "python3 ~/.claude/skills/assumptions-document-writing/hooks/assumptions-doc-skill-reminder.py" } ] }
    ]
  }
}
```

## Forking and adding a skill

1. Create a directory under `skills/` with a plain, descriptive name (lowercase, hyphens).
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and the instructions.
3. Install your fork the same way: `npx skills add <your-org>/<your-fork> -g`. To install it as
   a plugin, first change `name` in `plugin.json`, `.claude-plugin/plugin.json` and
   `.claude-plugin/marketplace.json` to your fork's own name, which becomes its skill prefix.

Decision records for skill rules live in [`skill-decisions/`](skill-decisions/), outside
every skill directory so they never load into a running session. Read the relevant one
before changing a rule.

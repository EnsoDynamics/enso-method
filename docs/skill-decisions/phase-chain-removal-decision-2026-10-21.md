# Removing phase-chain (decision record, 2026-10-21)

Maintainer notes for the removal of `skills/phase-chain/` and its touch points in `implement-from-requirements`, `phase-split`, `continuation-prompt`, `implementation-lifecycle`, `pre-commit-validation` ("Who Commits"), `using-the-enso-method` and the README. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before adding any skill that hands a phase to a new session on its own.

## The problem

`phase-chain` was a Codex-only orchestrator: after each phase it committed, pushed and called Codex's task creation tool to start the next phase in a fresh task, carrying the user's authorization along in the prompt. In practice it only partly worked. Chains stalled or needed a person to step in, so the "no babysitting" promise did not hold.

Its cost was spread across the method. Six skills carried "inside an authorized `phase-chain`, do this instead" branches, and those branches existed only for this one skill on one agent.

## Decision

Remove the skill and every branch that referred to it. Between phases, the next chat starts from `continuation-prompt`'s copy-paste prompt on both Claude Code and Codex.

Running every phase of a PRD unattended belongs to Kiln, a separate harness that starts each phase itself and checks the result, rather than relying on one agent session to launch the next.

## What was checked before removing it

- Kiln never loads or relies on `phase-chain`. Its phase prompt names only `implement-from-requirements`.
- No manifest, CI check or test referred to it. Both plugin manifests find skills by scanning the skills folder.
- Every other mention was a conditional branch, so removing those branches leaves the normal path unchanged.

## Known gap

Kiln v1 drives Claude Code only. Until it drives Codex, a Codex user moves between phases by pasting the continuation prompt.

## Revisit when

- Kiln drives Codex. There is then nothing to revisit.
- Codex's task tools become reliable enough that an in-agent chain works without supervision, and Kiln is not an option for some users.

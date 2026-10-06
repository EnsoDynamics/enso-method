# Phase sizing, and one phase per session (decision record, 2026-10-02)

Maintainer notes for `skills/phase-split/SKILL.md` ("Session Capacity Calibration", the per-phase sizing gate, "A fresh plan is flat") and the sizing gate in `implement-from-requirements`. **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing the capacity anchors.

## The problem

- **A user could not tell a phase from a session.** A split reported its plan as more working sessions than phases, because one top-level phase was a planning-time split record over several children. The skill allowed that depth at planning time for a "natural group" of slices, so a phase and a session were different counts.
- **The sizing band produced far too many phases.** The August 2026 anchor ("10-15 files and several hundred to ~a thousand net lines") plus "when borderline, split it" put a lean PRD's 25 acceptance criteria into 21 phases, about one criterion each, against the skill's own 3-7 band. Another PRD reached 291 phase documents, with split records citing the band directly: a group of about 25 files was treated as a session on its own.
- **The band had no measured basis.** Its commit (2026-08-29) called it "a judgment call informed by benchmark and practitioner data"; no source was recorded.

## Evidence (gathered 2026-10-02)

- **Measured sessions, Opus 5.5 in Claude Code.** One production PRD's first two phases each landed in a single implement chat at about 200 files and 20,000-26,000 added lines each, about 60% tests, a dozen-plus criteria each, and went live the same day. Each chat split the build across several helper agents and integrated the results. Several review rounds in-session found and fixed defects; a handful of follow-up fixes landed in the days after. Integration, review, two full test-suite runs and the live check took several hours per phase.
- **Phase commits across our repos since 2026-08-29:** median 11 files, p90 23. That mostly measures the band itself. Almost no splits were forced by a phase overrunning mid-implementation; nearly all were made at sizing time against the band.
- **METR time horizons** (https://metr.org/time-horizons/, May 2026): the 50% horizon runs 4-10x the 80% horizon; 80% ("dependable") sits around 1-3 expert-hours for early-2026 models. These are single attempts scored by a script, with no PRD, test loop or review passes, so they understate a structured session. No published horizon for Opus 5.5 (https://metr.org/blog/2026-09-22-claude-opus-5-5/).
- **Anthropic engineering posts.** November 2025 (https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Opus 4.5 failed by "trying to do too much at once"; one feature per session fixed it. March 2026 (https://www.anthropic.com/engineering/harness-design-long-running-apps): with Opus 4.6 the per-feature sprint construct was removed, on runs of about four hours.
- **Benchmarks by change size** (SWE-bench Pro, https://labs.scale.com/leaderboard/swe_bench_pro_public_v2; FeatBench, https://arxiv.org/html/2509.22237v1) show success falling with files and lines. Those breakdowns are for 2025 models, and top SWE-bench Pro scores are now near 90%.
- **Human review.** Defect-finding drops past 200-400 lines per sitting (SmartBear/Cisco study, 2006); Google calls ~100 lines reasonable and 1,000 usually too large (https://google.github.io/eng-practices/review/developer/small-cls.html). AI-assisted PRs wait far longer for review and merge far less often (LinearB 2026, https://linearb.io/blog/8-million-prs-engineering-productivity).

## Options considered

1. **Raise the file band** (say to 50-100 files). Rejected: file count does not track difficulty (a 40-file rename versus a 3-file concurrency change), and any number would be a guess dressed as a limit, the same flaw as before.
2. **Anchor on METR hours.** Rejected as the anchor: it measures single unassisted attempts, not a session with a PRD, tests and review passes, and has no figure for the current model. Kept as the reason for the "size for the dependable case" line.
3. **Cap acceptance criteria per phase.** Rejected as a cap; kept as a typical range ("often 5 to 15"), from the measured phases' dozen-plus and the old 3-7 band's lower end.
4. **Chosen: size by capability and real seams, with the measured sessions as the reference size.**

## Decisions and why

- **Every phase is one session; a fresh plan is flat.** A split parent is a split record, not a phase, and a plan is reported as one count: phase documents with no `## Split into` table. Planning-time depth is gone; depth appears only when an already-referenced phase is re-split, where lettered children keep existing ids valid.
- **The unit is one coherent capability with every criterion machine-verifiable in the session.**
- **The reference size is our measured sessions, stated with its limits.** Two successes, not a dependable rate. Those sessions split their build across helper agents, which the methodology does not prescribe; the skill mentions that only in general terms, to qualify the evidence, and a session building in one context is sized by the capability test alone until one is measured.
- **The bias is inverted, in both directions.** Borderline stays whole, and adjacent phases that together fit one session with no real seam between them merge. Each phase has a fixed cost (reload, review and hardening passes, full suite, CI, merge, live check: hours each), and a phase that overruns is re-split in the same chat without losing work. The observed failure was over-splitting, not overruns, though only under the old small band.
- **"Size for the dependable case" stays as one line.** The old paragraph argued for the small band; its core point, that models finish larger tasks sometimes than reliably, still holds.
- **Dependencies are named; parallelism is not planned.** Each phase doc and the plan table name the phases a phase directly needs, with what it needs, or "None". The plan still runs in order; the explicit tree is what lets a person, or an agent they ask, see which phases could run at the same time, and that stays the user's call. A yes/no "parallelizable" mark was rejected: it hides why, and goes stale when a phase changes.
- **Splitting one phase's build across helper agents is not part of the methodology.** `implement-from-requirements` builds one phase per chat and prescribes nothing about fanning that build out.
- **Human review is named as a separate limit.** Where a team reads every line, the answer is several smaller commits within a phase, not more sessions. This is the main trade-off of bigger phases, and it stays a team choice.

## Revisit when

- A phase sized under these anchors overruns its session or lands with defects the session's own review missed. Record the case here.
- A session that builds in one context, with no helper agents, is measured; give it its own anchor.
- METR or Anthropic publish dependable-horizon data for the current model.
- The phase-count guidance ("typically 2-4; past about six, look for merges") and `prd-roadmap`'s "3 to 10 phases" PRD band were set under the old phase size. With phases several times larger, both may now be too generous; not changed here.

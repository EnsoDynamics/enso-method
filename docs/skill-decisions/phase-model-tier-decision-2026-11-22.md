# Phase model tier (decision record, 2026-11-22)

Maintainer notes for the `**Model tier:**` line in `skills/phase-split/SKILL.md` (the "Model Tier" section, Step 3's declaration, Step 4, the templates and "Completion Phases"). **This file is deliberately outside every skill directory and nothing in a `SKILL.md` links to it**, so it never loads into a running session. Read it before changing the tier values, what earns each one, or what the line may say.

## The problem

One model and one effort setting were chosen for a whole PRD and used for every phase. Phases are not equally hard. A phase that defines the data model every later phase builds on deserves the strongest model available, and a phase that repeats an existing pattern five more times does not need it. A person with more than one subscription also wants to know which phases could run on the other one. Nothing in the plan said which phase was which, so the choice was either one setting for everything or a guess made phase by phase with the plan closed.

The session that splits the PRD is the one that knows. It has just walked through each phase's implementation to size it.

## Options considered

1. **Name a model in the phase document.** Rejected. A skill that says which model is stronger is wrong as soon as the ranking changes, and it assumes the reader has that vendor's subscription. A phase document that names a model also goes stale while the plan is still being built.
2. **Recommend an effort setting.** Rejected. Effort levels are not comparable between vendors or between models from one vendor: the same phase may want medium on one model and high on another. Effort belongs with the model it is set on.
3. **Recommend several equivalent models per phase.** Rejected for the same reason as option 1. Which models are interchangeable is the reader's mapping, made once per tier, not a judgment repeated in every phase document.
4. **Two values, standard and demanding.** Rejected. The cheaper direction is the one a person saving usage most wants to see, and leaving it out hides the phases where a lighter model would do.
5. **Put the tier in the continuation prompt.** Rejected. A person pasting the prompt does not read it for settings, and the session that receives it cannot change its own model.
6. **Let the tool that runs phases judge the tier itself.** Rejected. It would need a model session of its own to read the plan, and it would judge with less than the splitting session already knows.

## Decisions and why

- **The line describes the phase, never the model.** Three values, `demanding`, `standard` and `mechanical`. A tool that runs phases, or a person, maps each tier to a model and an effort setting, and that mapping is where vendor preference, cost and fallback choices live.
- **Every leaf carries the line, standard included.** The first draft left standard unwritten, the way `**Attended:**` and `**Early merge:**` are absent when they do not apply. Those lines are flags. A tier is one of three values, and a missing value cannot be told from a phase nobody judged: a plan written before this rule, a phase written by hand, a completion phase whose author skipped the test. A reader, or a tool showing the plan, needs to say "judged standard" and "not judged" differently. Writing it every time also makes the judgment a step that cannot be skipped by doing nothing. A phase document with no line is unjudged.
- **Demanding needs two things at once: hard to get right, and costly if wrong.** The first draft had a flat list of six triggers, any one enough. That mixed two different properties. Money and access are about what a mistake costs, not about how likely a capable model is to make one, and a great deal of ordinary work touches them. Concurrency, interacting rules and an open design decision are about difficulty: the phase's tests can pass while the work is wrong. A standard model handles either property alone. The stronger model earns its cost where a hard thing sits on something expensive. Requiring any two triggers from one list was rejected because two stakes (money and access) would qualify with nothing hard in the phase.
- **The hard thing must be required by a criterion.** Nearly every phase uses a queue or an access check somewhere. The phase is hard when the PRD made the hard thing an acceptance criterion, which an agent checks by reading the criteria instead of judging importance.
- **"Shared code changed with thin tests" was dropped as a trigger.** Brownfield work changes shared code constantly, and thin tests are `test-hardening`'s subject.
- **"Built on" means a choice the design did not make.** It first read "a later phase builds on the structure or behavior it fixes". Nearly every phase has a later phase that depends on it, so the cost test was almost always true and demanding rested on the hard test alone. It now counts only a data model or interface this phase chooses because the design left it open, which a later phase or an outside system is then written against.
- **Building the shared data model is standard when the design specifies it.** The technical design, already reviewed and refined, made the decisions, so the phase is neither hard nor a choice later phases are written against.
- **The data cost is lost or corrupted records, not only migrations.** It first read "rewrites or deletes rows that already exist, in place", which a reader could take to mean migrations alone. That left out a race on a stock count or a booking, with no money or access in it, which is as clear a demanding case as any. Money likewise covers moving it, not only computing it.
- **A criterion counts when the phase owns or completes it.** A cross-cutting criterion listed as "also applies" belongs to the phase that owns it.
- **Size is not part of the test.** A phase that is merely large is the sizing test's subject.
- **Mechanical has a strict, all-of bar.** The cost of a wrong mark is not symmetric. A demanding mark on an ordinary phase wastes some usage. A mechanical mark on a phase that needed judgment produces work the delivery audit pays to repair, on a foundation later phases may already have built on. So every condition must hold, and doubt means standard.
- **Mechanical needs a worked example it can name.** "Follows a pattern" is a judgment; a path or a phase id is a fact. An earlier phase of the same plan counts, because the common case is a PRD that builds the same thing several times and only the first is new.
- **Mechanical has no size condition, and the tier never changes the cut.** The first draft required a mechanical phase to be about half a normal phase's size, because the Session Capacity Calibration anchors were measured on a strong model. It was removed. The figure was a guess with no measurement behind it, and it nearly emptied the tier: sizing merges neighbours that fit one session, so repeated work usually lands in a full-size phase. The other four conditions remove the judgment a lighter model is weaker at. What is left is session length, and a phase that overruns is caught by the existing checks and re-split in the same chat.
- **The name is `mechanical`, not `routine` or `light`.** `routine` read too close to `standard`. `mechanical` says why a lighter model is enough: the phase needs no judgment. A small phase that still needs judgment stays standard.
- **Completion phases get a tier by the same test.** A gap in concurrency handling is as demanding to repair as it was to build.
- **A split record carries no tier.** It is never implemented, and its children can differ.
- **The tier is a recommendation.** Whoever starts the session decides what it runs on. Nothing in the method reads the line or depends on it.

## Not addressed

- **The audits.** `delivery-audit` and `test-audit` are not phases and get no tier. What they run on is the choice of whoever starts them.
- **Whether tiers pay.** No measurement yet shows that a demanding phase built on a stronger model, or a mechanical phase built on a lighter one, changes how many gaps the audits find.

## Revisit when

- Plans mark most phases demanding. The bar is too loose, and the line stops carrying information.
- Mechanical phases built on a lighter model draw more delivery audit gaps than standard ones. Tighten the bar or drop the value.
- No plan ever marks a phase mechanical. The bar is too strict to be worth a value.
- Models stop differing enough in capability or cost for the choice to matter.

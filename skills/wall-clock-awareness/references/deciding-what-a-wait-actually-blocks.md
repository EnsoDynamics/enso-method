# Deciding What a Wait Actually Blocks

Reference for `wall-clock-awareness`. Read it before accepting a wait for a scheduled run,
a soak period, an approval or an aged fixture.

At planning time, identify long prerequisites such as fixture aging, soak periods,
external approvals and scheduled windows. Start safe preparation early enough to
overlap implementation where practical. A test fixture is owned synthetic data;
record its owner, eligibility time and cleanup responsibility so advance preparation
does not become abandoned data.

Before accepting a long wait, distinguish the product or external constraint from
our chosen test setup and phase ordering. Name the exact result that cannot yet be
proved, then identify authorized work that does not require that result. A blocked
acceptance check does not automatically block design, implementation or unrelated
validation. Proceed with safe independent work; do not manufacture busywork or
silently relax an explicit user gate. When a gate really prevents useful overlap,
explain the concrete dependency and recommend a bounded change where appropriate.

**Do not wait for an interval merely because the normal flow is scheduled.** First ask
whether the scheduler or natural cadence is itself part of the behavior being proved, or
whether it is only the ordinary way the real worker starts. When an authorized manual
trigger runs the same deployed version with the same configuration, inputs and boundary
conditions, and its downside is negligible, prefer triggering it now. Hours saved from
the critical path outweigh fidelity to an incidental clock. Record the run honestly as
operator-triggered; do not describe it as the scheduled invocation.

Before triggering, verify temporal eligibility as well as task identity. A worker may be
safe to start yet intentionally ignore data until a UTC date rolls over, an upstream
window closes, or a fixture reaches a required age. If so, identify the earliest valid
instant and trigger then rather than waiting for the later normal schedule. A premature
run that cannot consume the fixture proves the gate, not the requested result.

Wait for the natural interval only when it adds material evidence: the requirement tests
the scheduler or cadence itself; an upstream system can produce the needed state only in
that window; manual dispatch follows meaningfully different code, identity, configuration
or side effects; or the trigger's operational risk is not negligible. State that reason
explicitly. “This is when it normally runs” is not enough.

Judge a workaround by its net value and risk. Reuse suitable existing test data or
prepare it earlier when that preserves the proof. Do not falsify timestamps, weaken
assertions, introduce runtime clock bypasses, add lasting production complexity, or
perform risky storage/infrastructure changes merely to shorten a test. Controlled
clocks in appropriately scoped tests prove simulated-time behavior, not that a real
elapsed-time acceptance gate passed. A modest unavoidable wait can be the right choice.

When work continues with a deferred check, retain its incomplete status and record
its exact artifact/version, owner, execution time, restoration/cleanup obligations,
and failure response. Keep one owner for shared checkout writes. Preserve the
version and environment needed by the check; overlapping code edits need not imply
permission to push or deploy over it. If the check fails, the current owner pauses
affected dependent work, fixes the issue and reruns the relevant checks on the
resulting version. Do not let several dependent phases accumulate behind an unproved
foundation. Transfer pending checks explicitly when handing off responsibility;
never relabel incomplete delivery as complete to unlock a successor.

For a genuinely unavoidable elapsed-time window, exhaust useful independent work
first. A real scheduled continuation may then own the remaining check; verify its
creation and report what will resume and when. A promise or a background shell is
not a wakeup. This exception does not turn an active CI/deployment wait into a reason
to end the turn: follow `waiting-on-ci-deploys-and-remote-jobs.md` for those jobs.

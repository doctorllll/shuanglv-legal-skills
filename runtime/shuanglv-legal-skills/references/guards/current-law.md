# Guard｜Current Law

`unit_id: unit.guard.current-law`

**Scope：** Current-law truthfulness guard.

## Trigger
- Conclusion materially depends on law being current, valid, effective or jurisdictionally applicable.
- User explicitly asks current law/current rule or task includes time-sensitive specialty law.

## Negative Trigger
- Payload keyword alone.
- Pure semantic rewrite/format-only where no new current-law representation is made.
- User explicitly forbids research/current-law verification and the task can be answered only as a clearly labeled `UNVERIFIED / preliminary` conditional judgment. In that case the L0 Integrity Kernel preserves truthfulness; do not load this verification Guard merely to simulate a verification that is outside scope.

## Essential Procedure
1. Identify proposition whose currentness matters.
2. Actually verify authoritative source/effective date.
3. Do not label current/verified without execution.

## Deepening Conditions
- Recent amendment/conflict/transition.

## Exit Sufficiency
- Currentness is verified or explicitly downgraded.

## Professional Results
- VERIFIED_CURRENT / UNVERIFIED / CONFLICTING state

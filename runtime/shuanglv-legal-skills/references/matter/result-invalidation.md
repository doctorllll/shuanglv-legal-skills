# Matter｜Result Invalidation

`unit_id: unit.matter.invalidation`

**Scope：** Targeted result invalidation and recomputation.

## Trigger
- New/changed material affects a previously stored result.

## Negative Trigger
- No dependent prior result.

## Essential Procedure
1. Identify changed input.
2. Follow lightweight dependencies.
3. Invalidate only affected results.
4. Reuse unrelated CURRENT results.

## Deepening Conditions
- Key evidence/law change.

## Exit Sufficiency
- All materially affected results are updated or marked stale; unrelated results remain reusable.

## Professional Results
- CURRENT/STALE/REBUILD updates
- affected-result writeback


## Result Metadata / Invalidation

- Receive changed/new source or result.
- Find directly dependent CURRENT results.
- Mark only those results STALE unless dependency breadth makes local preservation unsafe.
- Propagate STALE through explicit result dependencies only.
- Recompute/review affected results; write back new CURRENT version.
- Leave unrelated CURRENT results reusable.

Result status: `CURRENT / STALE / REBUILD`. Invalidation follows explicit source/result dependencies only.

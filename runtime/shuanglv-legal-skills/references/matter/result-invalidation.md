# Matter｜Result Invalidation

`unit_id: unit.matter.invalidation`

**Scope：** Targeted result invalidation and recomputation.

## Trigger
- New/changed material, fact, evidence, law, research result, decision or shared field affects a previously stored result/deliverable.

## Negative Trigger
- No dependent prior result.

## Essential Procedure
1. Identify changed upstream object.
2. Follow explicit lightweight `DependencyEdge` relations.
3. Invalidate only materially affected downstream results.
4. Reuse unrelated CURRENT results.
5. Recompute/review affected results and write back a new CURRENT version where possible.

## Deepening Conditions
- Key evidence/law change.
- Dependency breadth makes local preservation unsafe.

## Exit Sufficiency
- All materially affected results are updated or marked stale; unrelated results remain reusable.

## Professional Results
- `CURRENT / STALE / REBUILD` updates
- affected-result writeback
- DependencyEdge updates

# DependencyEdge Contract

`DependencyEdge` 只表达“哪个上游对象的变化可能使哪个下游专业结果失效”，不要求建立完整 DAG Engine。

最小字段：
- `edge_id`；
- `upstream_ref`：Source / Fact / Evidence / Rule / Case / Research / Decision / SharedMatterField 等；
- `downstream_ref`：Finding / Argument / Result / DeliverableClaim / Deliverable 等；
- `dependency_type`：`SUPPORTS / CONTRADICTS / REQUIRED_INPUT / LEGAL_BASIS / SHARED_FIELD / DECISION_INPUT / OTHER`；
- `materiality`：`MATERIAL / NON_MATERIAL / UNKNOWN`；
- `status`：`ACTIVE / SUPERSEDED / BROKEN`；
- `last_checked_at`。

## Invalidation rules

- Receive changed/new upstream source or result.
- Find directly dependent CURRENT results through ACTIVE edges.
- Mark only materially dependent results `STALE` unless dependency breadth makes local preservation unsafe.
- Propagate `STALE` through explicit result dependencies only.
- If correctness cannot be preserved by local updates, mark `REBUILD` and explain why.
- Recompute/review affected results; write back new CURRENT version and update edges.
- Leave unrelated CURRENT results reusable.
- An `UNKNOWN` materiality edge cannot be silently treated as NON_MATERIAL when the conclusion is high-impact; inspect or require review.

Result status remains: `CURRENT / STALE / REBUILD`. DependencyEdge is a lightweight invalidation aid, not an independent truth source.

## Execution Ledger 接口

当 `unit.interop.execution-control` 已加载，依赖失效的 canonical 判断仍由本文件负责；执行控制只接收结果并把受影响模块状态投影为 `INVALIDATED / IN_PROGRESS / REVIEW_REQUIRED`。不得由执行账本另造第二套依赖真值。

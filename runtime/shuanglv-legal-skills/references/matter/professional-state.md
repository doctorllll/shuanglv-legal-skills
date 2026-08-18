# Matter｜Professional State

`unit_id: unit.matter.state`

**Scope：** Minimal professional continuity state, not a case database.

## Trigger
- Task spans sessions/turns or requires reusable Source/Result/Decision/OpenIssue/Resume state.
- Large multi-material work needs continuity across capability outputs.

## Negative Trigger
- Simple one-turn task with no reuse/continuation need.
- Do not create FullMatter solely from material volume/document type.

## Essential Procedure
1. Attach to the intended matter.
2. Persist only professional continuity objects.
3. Maintain cross-matter isolation.

## Deepening Conditions
- Long/iterative matter or multiple result dependencies.

## Exit Sufficiency
- Sufficient state exists to resume/reuse without storing a general project database.

## Professional Results
- Source Index
- Result Index
- Decision state
- Open Issues
- Resume Capsule


## Matter State Contract

- Matter State is professional continuity state, not a case database/CRM/project-management system.
- Persistent Rich, Recover Minimal.
- No Silent Cross-Matter Merge.
- State continuity does not imply authorization continuity.

### Attachment
- Attach only to an explicitly identified matter or a contextually unambiguous matter.
- When two or more plausible matters could materially change the answer, mark AMBIGUOUS and request only the minimum disambiguation.
- A brief non-legal interlude does not detach the matter; the next legal turn may resume if reference is unambiguous.
- Never merge facts/results across matter_id without explicit cross-matter relation.

### Source Index
- RECEIVED ≠ REVIEWED.
- OCR/transcript/summary never silently upgrades to ORIGINAL.
- Each source remains matter-scoped.

### Result Index
- A result is reusable only when CURRENT and its material dependencies remain current.
- A changed source/result invalidates only dependent results.
- REBUILD is used only when local invalidation cannot preserve correctness.
- Result reuse precedes recomputation.

### Decisions
- Reserved substantive decisions have human_required=true.
- Decision state is not action authorization.

## Bundle / Shared Field Continuity Boundary

需要跨轮次维护成套交付一致性时，Matter State 可以保存 `DeliverableBundle` 和 `SharedMatterField` 的**最小索引/状态引用**，但不因此升级为完整文档管理数据库。

- 共享字段仍引用上游 Source/Fact，不独立制造“真相”；
- 字段变化只使依赖的 Deliverable/Result 进入 STALE；
- 法律/策略变化不得作为纯字符串传播处理；
- Host 不支持持久化时，输出可携带的最小状态/Resume Capsule，不声称已经长期保存。

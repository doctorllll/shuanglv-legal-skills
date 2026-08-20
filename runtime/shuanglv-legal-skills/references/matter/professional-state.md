# Matter｜Professional State

`unit_id: unit.matter.state`

**Scope：** Minimal professional continuity state, not a case database.

## Trigger
- Task spans sessions/turns or requires reusable Source/Fact/Evidence/Research/Result/Decision/OpenIssue/Deliverable/Resume state.
- Large multi-material work needs continuity across capability outputs.

## Negative Trigger
- Simple one-turn task with no reuse/continuation need.
- Do not create FullMatter solely from material volume/document type.

## Essential Procedure
1. Attach to the intended matter.
2. Persist only professional continuity objects/references needed for reuse or invalidation.
3. Maintain cross-matter isolation.
4. Reuse CURRENT results before recomputing; new input invalidates only materially dependent results.

## Deepening Conditions
- Long/iterative matter or multiple result dependencies.

## Exit Sufficiency
- Sufficient state exists to resume/reuse without storing a general project database.

## Professional Results
- `MatterProfessionalIndex`
- Source / Fact / Evidence / Research / Result indexes
- Decision and Deliverable state
- Open Issues
- Resume Capsule

# Matter State Contract

- Matter State is professional continuity state, not a case database/CRM/project-management system.
- **Persistent Rich, Recover Minimal.** Host 可以持久化丰富专业对象，但恢复当前任务时只投影最低充分状态。
- **No Silent Cross-Matter Merge.**
- State continuity does not imply authorization continuity.

## 1. Attachment / isolation

- Attach only to an explicitly identified matter or a contextually unambiguous matter.
- When two or more plausible matters could materially change the answer, mark `AMBIGUOUS` and request only the minimum disambiguation.
- A brief non-legal interlude does not detach the matter; the next legal turn may resume if reference is unambiguous.
- Never merge facts/results across `matter_id` without explicit cross-matter relation.

# MatterProfessionalIndex｜最小专业连续性索引

`MatterProfessionalIndex` 是跨轮次续接的**引用层**，不是把全部案件内容再复制一遍。建议最小字段：

- `matter_id`；
- `matter_label`；
- `current_stage`；
- `party_role_refs`：当事人/客户/对方/机关/关键主体及当前角色引用；
- `source_refs`：Matter-scoped 来源索引；
- `verified_fact_refs`：当前已核验重要事实引用；
- `disputed_fact_refs`：争议、冲突或相互竞争事实引用；
- `evidence_issue_refs`：证据真实性、合法性、关联性、证明力、缺口等问题引用；
- `research_result_refs`：仍可复用的法律研究/案例研究结果；
- `finding_refs`：已形成分析发现/法律结论引用；
- `decision_refs`：人工保留决定及其状态；
- `deliverable_state_refs`：报告、文书、合同稿、矩阵等交付物状态引用；
- `execution_state_refs`：仅对跨轮次仍未结束的复杂任务保存 TaskExecutionContract / ModuleExecutionLedger 的最小续跑引用；简单任务不持久化执行台账；
- `open_issue_refs`：待解决问题；
- `dependency_edges`：上游变化影响下游结果的轻量依赖边；
- `recommended_next_units`；
- `updated_at`。

### 索引纪律

- 上述字段优先保存对象引用/状态，不复制全部正文；
- 每个对象的事实真值、来源状态、证据评价、法律有效性仍由其 canonical owner 负责；
- MatterProfessionalIndex 不得把 `ALLEGED / INFERRED / DISPUTED / UNKNOWN` 静默升级为 VERIFIED；
- 不要求简单事项为了 schema 完整而创建所有字段，缺失可为 `[] / UNKNOWN / NOT_APPLICABLE`。

## 2. Source / Fact / Evidence continuity

### Source Index
- `RECEIVED ≠ REVIEWED`。
- OCR/transcript/summary never silently upgrades to ORIGINAL.
- Each source remains matter-scoped.

### Fact / Evidence indexes
- Matter State 只索引已存在的 Fact/Evidence 对象及其状态；
- 新材料改变重要事实或证据评价时，通过 `dependency_edges` 影响相关 Result/Deliverable；
- 不把一个事项的证据关系复制到另一个事项。

## 3. Result / Research / Finding continuity

- A result is reusable only when `CURRENT` and its material dependencies remain current.
- A changed source/result invalidates only dependent results.
- `REBUILD` is used only when local invalidation cannot preserve correctness.
- Result reuse precedes recomputation.
- 已完成法律研究只有在法域、关键时间、规范有效性和检索范围仍满足当前问题时才可继续复用。

## 4. Decisions

- Reserved substantive decisions have `human_required=true`.
- Decision state is not action authorization.
- 历史同意/授权不得仅因 Matter 恢复而自动延续到新的外部处理、发送、提交、签署或其他副作用动作。

## 5. Deliverable continuity

需要跨轮次维护成套交付一致性时，Matter State 可以保存 `DeliverableBundle`、`DeliverableClaim` 和 `SharedMatterField` 的**最小索引/状态引用**：

- 共享字段仍引用上游 Source/Fact，不独立制造“真相”；
- 字段变化只使依赖的 Deliverable/Result 进入 `STALE`；
- 法律/策略变化不得作为纯字符串传播处理；
- 正式交付前必须处理 materially relevant 的 STALE/PENDING 状态。

## 6. Host persistence boundary

Host 不支持持久化时，输出可携带的最小状态/Resume Capsule，不声称已经长期保存。爽律skill 定义状态语义，不自建 CRM、数据库或项目管理软件。

## 长任务执行状态续接

跨轮次长任务需要继续执行时，可以保存 `execution_state_refs`，用于恢复尚未完成、受阻或已失效的主要模块状态。恢复时仍遵循 `Persistent Rich, Recover Minimal`，只投影当前子任务需要的状态和完成依据，不把执行账本扩张成通用项目管理数据库。

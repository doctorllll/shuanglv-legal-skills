# Interop｜Legal Artifact Contract

`unit_id: unit.interop.artifact`

**Scope：** Shared professional schema and truthfulness contract for common legal deliverables/artifacts; not an Office/PDF renderer.

## Trigger
- Multiple capabilities must converge into a structured legal artifact or a reusable deliverable shape.
- User asks for a named legal table, matrix, index, timeline, diagram, ledger, revision set or formal legal document.

## Negative Trigger
- Pure conversational answer with no reusable artifact structure needed.
- Physical rendering details alone belong to `unit.external.document-render`.

## Essential Procedure
1. Select the appropriate `artifact_type`.
2. Resolve `required_fields` from current goal/domain, not from a universal giant template.
3. Apply `source_requirements` and object status rules from canonical owners.
4. Separate professional content completeness from physical file/rendering completion.
5. Make `file_existence_claim` only after the Host actually created and verified the claimed file.

## Exit Sufficiency
- The artifact has the minimum professional fields and source/status fidelity required for its purpose, and any physical-file claim is truthful.

## Professional Results
- `LegalArtifactContract`
- artifact profile / artifact instance metadata

# LegalArtifactContract

Minimum common fields:
- `artifact_id`；
- `artifact_type`；
- `matter_id`（如适用）；
- `purpose`；
- `audience`；
- `required_fields`；
- `source_requirements`；
- `status_requirements`；
- `owner_units`；
- `rendering_requirement`：`NONE / OPTIONAL / REQUIRED / NATIVE_REQUIRED`；
- `file_existence_claim`：`NOT_REQUESTED / NOT_CREATED / CREATED_UNVERIFIED / VERIFIED_EXISTS`；
- `version_or_hash`；
- `quality_checks`。

## Canonical artifact profiles

以下是**高频专业成果类型**，不是固定列模板。具体字段仍随案件/任务变化。

### `EVIDENCE_CATALOG`｜证据目录
至少包含：证据标识、名称/类型、来源、locator、拟证明命题、事实状态、证据问题、备注。

### `ELEMENT_EVIDENCE_MATRIX`｜要件—证据矩阵
至少包含：法律要件/待证命题、支持证据、反向证据、证明责任/标准、缺口、结论状态。

### `CASE_COMPARISON_TABLE`｜类案比较表
至少包含：案例身份、裁判机关/案号/日期、决定性事实、裁判理由/规则、相同点、区别点、使用目的、原文 locator。

### `TIMELINE`｜时间线
至少包含：日期/时间、事件、主体、来源、状态、与争点/程序节点的关系。

### `RELATIONSHIP_MAP`｜主体关系图
至少包含：节点、关系、依据来源、关系状态、必要的角色/控制/代理/交易属性。

### `MONEY_FLOW`｜资金流
至少包含：时间、付款/收款主体、金额/币种、账户/链路标识、交易依据、来源、异常/争议状态。

### `DOSSIER_INDEX`｜卷宗/材料索引
至少包含：material_id、名称、类型、来源、时间、review_status、locator、关联争点/下一步。

### `CONTRACT_RISK_LEDGER`｜合同风险台账
至少包含：条款/场景、风险、触发条件、影响、客户立场、建议、备选/让步、原文 locator、状态。

### `CONTRACT_REVISION`｜合同修改成果
至少区分：原文/修改文本/修改理由/风险与交易目的；需要原生 Track Changes 时必须由 Host 真实执行。

### `FORMAL_LEGAL_DOCUMENT`｜正式法律文书
至少满足：文种/受众/立场、事实与法律来源、核心论证、内部→外部边界、正式交付 Guard、版本与实体文件真实性。

### `DD_ISSUE_LIST` / `DD_RISK_LEDGER`｜尽调问题/风险台账
至少包含：主题、来源、核验状态、Expected-but-Missing、Red Flag、影响、补救/条件、待补资料。

### `BATCH_REVIEW_TABLE`｜批量审查结果表
至少包含：item_id、source_ref、核心字段/问题答案、item_status、error_or_gap、review_reason；同时关联 BatchRunRecord。

### `VERIFICATION_LEDGER`｜核验台账
复用 Review 的 VerificationLedger；不得另创事实/法律状态。

### `LEGAL_VISUALIZATION`｜法律可视化成果
统一承载静态或交互式法律可视化，具体图型（如 `TIMELINE / RELATIONSHIP_MAP / MONEY_FLOW`）可继续作为兼容 subtype/profile。至少包含：

- `visual_id`、`visual_type`、`purpose`、`audience`、`use_context`；
- `presentation_modes`：`STATIC / INTERACTIVE / BOTH`；
- `legal_visual_spec_ref` 与 `data_version_or_hash`；
- `source_requirements`、`status_requirements`、`visual_profile`；
- `static_artifacts`、`interactive_artifacts`、`snapshot_artifacts`（按实际请求/能力存在）；
- `view_state_ref`（交互时）；
- `quality_checks`；
- `file_existence_claim`。

静态、交互和快照不得各自重新理解案件；它们必须消费同一 `LegalVisualSpec` / 数据版本。ViewState 只记录筛选、聚焦、图层、时间窗口等“怎么看”，不得重写 Fact/Evidence/Issue/Argument 的 native status。

## Source / status authority

Artifact Contract 只规定成品需要什么，**不重新拥有** Facts/Evidence/Research/Current-law/Matter 的状态。

- 事实与来源：Facts/Review；
- 证据评价：Evidence；
- 法律/案例研究：Research + Current-law Guard；
- STALE/依赖：Matter Invalidation；
- 核验台账：Review；
- 可视化方法与 `LegalVisualSpec`：Visualization Capability；
- 实体文件/渲染：Document Render。

## Physical delivery truthfulness

- Markdown/JSON/结构化对象完成 ≠ DOCX/PDF 已生成；
- `CREATED_UNVERIFIED` 不得对用户表述为“文件已经存在且可用”；
- 只有实际创建并检查路径/附件/内容后才能使用 `VERIFIED_EXISTS`；
- 原生修订、批注、PDF 页码、图形等必须以当前 Host 真实能力为准。

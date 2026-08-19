# Interop｜Batch Processing

`unit_id: unit.interop.batch`

**Scope：** Shared batch orchestration for repeated legal-work operations across multiple materials/items; not a spreadsheet engine or background job system.

## Trigger
- Multiple items require the same or comparable extraction/review/research/drafting operation and consistency, scale, cost or resumability makes batch coordination useful.
- Large/heterogeneous material review needs a stable question/schema before broad execution.

## Negative Trigger
- A few simple items can be handled directly with no meaningful consistency/cost/resume risk.
- Pure deterministic file operation already safely handled by the Host without legal semantic review.

## Essential Procedure
1. Define `BatchJobProfile` from the current legal goal, not from a generic fixed table.
2. Apply `Pilot Sample Gate` when semantic uncertainty, scale, cost or error propagation justifies a sample run.
3. Freeze/revise the field/question/schema only after checking pilot quality when a pilot is needed.
4. Execute remaining items in batches/chunks with per-item status and source fidelity.
5. Preserve `checkpoint` / resume state where the Host can persist it; otherwise export an honest BatchRunRecord.
6. Aggregate exceptions, conflicts, missing items and high-risk items for targeted review.

## Deepening Conditions
- Large item count/size; heterogeneous sources; expensive external calls; material error propagation; sensitive data; irreversible side effect; high-risk legal conclusion.

## Exit Sufficiency
- Required items are processed or explicitly accounted for; exceptions are visible; high-risk/unresolved items are routed for appropriate review; no unprocessed item is silently represented as completed.

## Professional Results
- `BatchJobProfile`
- pilot quality record where applicable
- `BatchRunRecord`
- exception/review queue

# BatchJobProfile

Minimum fields:
- `batch_id`；
- `matter_id`（如适用）；
- `objective`；
- `item_scope`：哪些文件/记录/合同/案例/对象属于本次 batch；
- `operation`：抽取、比较、核验、审查、起草、转换等；
- `question_or_field_schema`；
- `source_locator_requirement`；
- `acceptance_criteria`；
- `failure_policy`；
- `risk_or_cost_profile`；
- `checkpoint_policy`；
- `human_gate_conditions`。

# Pilot Sample Gate

**小样本不是仪式性步骤。** 当以下任一因素足以造成批量错误扩散时，先选择有代表性的少量样本试跑：
- 字段/问题定义尚不稳定；
- 来源类型差异大；
- 模型需要分类/抽取/判断且错误可能系统性复制；
- 外部调用成本较高；
- 后续批量结果难以逆转或人工返工代价高。

低风险、小规模、结构稳定或可确定性验证的任务，可以跳过 pilot，但应记录原因。**不得机械要求用户对每个普通批量任务反复确认。**

Pilot 质量至少检查：
- 问题/字段是否足以回答真实任务；
- 重要原文是否有 locator；
- 缺失与“不存在”是否被区分；
- 分类口径是否一致；
- 是否遗漏决定性不利信息；
- 是否出现系统性误识别。

如 pilot 暴露结构问题，先修正 schema，再批量；已经按旧 schema 处理的样本按需要重跑。

# Batch execution / checkpoint

- 对大批量任务按 Host 能力分 chunk 执行，不把全部材料简单拼成长上下文；
- 每个 item 保留 `item_id / source_ref / item_status / result_ref / error_or_gap / review_reason`；
- `checkpoint` 至少记录已完成范围、未完成范围、schema/version、异常队列和下一批起点；
- Resume 时只继续未完成或被要求重跑的项目，不因为中断默认整批重算；
- 任何 `PARTIAL/FAILED` 项不得计入已完整完成。

建议 item status：
`PASS / PARTIAL / FAILED / CONFLICT / HIGH_RISK / REVIEW_REQUIRED / SKIPPED`。

# BatchRunRecord

结束时至少汇总：
- 总项目数 / 已处理数 / 未处理数；
- `PASS / PARTIAL / FAILED / CONFLICT / HIGH_RISK / REVIEW_REQUIRED / SKIPPED` 计数；
- schema/version；
- 处理范围与实际工具/能力；
- 关键异常清单；
- 待人工复核队列；
- 是否存在会影响总体结论的 unresolved item；
- 最后 checkpoint / generated_at。

# Human gate boundary

只有在规模、成本、敏感外发、不可逆副作用、重大法律风险或用户明确要求时设置人工闸门。普通内部批量分析默认继续执行；Side-effect Authorization、External Processing 和 Reserved Human Decision 仍由各自 Guard 独立负责。

# Ownership / delegation

- 材料抽取和任务驱动 ReviewQuestionSet 仍由 `unit.cap.facts` 负责；
- 专业判断由相应 Facts/Evidence/Research/Reasoning/Domain owner 负责；
- 文件/表格/OCR 等确定性执行由 Host/External capability 负责；
- 本单元只负责共享 batch orchestration、status、checkpoint 和 exception aggregation。

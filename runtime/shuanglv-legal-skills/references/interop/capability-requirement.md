# Interop｜Capability Requirement

`unit_id: unit.interop.capability`

**Scope：** External capability need/input-output/fallback contract.

## Trigger
- Task requires an external capability/tool/service.

## Negative Trigger
- No external capability needed.

## Essential Procedure
1. Specify needed capability rather than implementation fantasy.
2. Define input/output quality and downgrade/failure semantics.
3. Never equate capability availability with authorization.

## Deepening Conditions
- Missing/degraded capability.

## Exit Sufficiency
- Capability requirement is satisfied or an honest downgrade/failure is explicit.

## Professional Results
- capability request
- input/output quality/fallback state


## Capability Request Contract

- Request capability, not a fictitious implementation.
- Capability availability/API key does not authorize use with sensitive data or external side effects.

Required fields: `request_id`, `needed_capability`, `purpose`, `minimum_input`, `expected_output`, `quality_requirements`, `failure_or_downgrade`, `side_effect_profile`

## Capability Fallback Ladder

外部能力不可用时按正确性约束选择：

1. `EQUIVALENT`：存在同等可信替代能力，继续；
2. `DOWNGRADED`：可用次优方案完成且不破坏核心正确性，披露影响和人工复核需要；
3. `BLOCKED`：核心资料无法读取、用户强制要求的原生能力无法提供、或现行法无法可靠核验等关键要求无法满足。

不得把“曾经某个 Agent/版本支持”当成当前能力已存在；也不得把工具失败自动升级为整个法律任务失败。

## Legal Source Connector Contract

法律规范、案例、官方解释或其他研究信源使用供应商无关 normalized result contract；数据库/知识库/搜索服务的专有语法、认证、分页和字段留在 Adapter。

最小字段：`query_or_issue`（检索问题）；`source_identity`（可核验来源身份）；`jurisdiction`；`effective_date`；`validity_status`；`authoritative_level`（仅连接器元数据，不替代 Research 判断）；`case_metadata`；`original_text_locator`；`retrieval_scope`（全文/摘要/片段、结果上限、过滤及时间地域边界）；`source_completeness`（`COMPLETE / PARTIAL / DEGRADED / UNKNOWN`）；`failure_or_degradation`；`permission_or_sensitivity`。

纪律：返回成功只证明 retrieval 发生，不证明现行有效、规范效力、案例可比或结论充分；`UNKNOWN/PARTIAL/DEGRADED` 不得静默补全；Adapter 不得因供应商不同改变字段语义；新增数据库不新增爽律核心规则；capability/API key/可访问性不等于敏感材料使用授权。

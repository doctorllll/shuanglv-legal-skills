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

纪律：返回成功只证明 retrieval 发生，不证明现行有效、规范效力、案例可比或结论充分；`UNKNOWN/PARTIAL/DEGRADED` 不得静默补全；Adapter 不得因供应商不同改变字段语义；新增数据库不新增爽律skill 核心规则；capability/API key/可访问性不等于敏感材料使用授权。


# CapabilitySlot｜类型化外部能力槽

`CapabilitySlot` 把“法律工作需要什么能力”与“当前宿主用哪个 Provider/工具实现”分开。核心只声明 capability，不把任何具体厂商写成默认依赖。

## Slot request fields

- `slot_id`；
- `needed_capability`；
- `purpose`；
- `minimum_input`；
- `expected_output`；
- `required_fidelity`；
- `source_or_locator_requirement`；
- `data_class`；
- `side_effect_profile`；
- `acceptable_equivalents`；
- `failure_or_downgrade`；
- `provider_binding`：默认 `NONE`；只有用户/团队明确配置或当前 Host 真实能力解析后才绑定具体实现。

## Canonical slot taxonomy

### 法律信息
- `LEGAL_NORM_SEARCH`：法规/司法解释/规范文件发现；
- `LEGAL_NORM_ORIGINAL_TEXT`：权威原文回源；
- `LEGAL_VALIDITY_CHECK`：效力、施行、废止/修改/过渡状态核验；
- `CASE_SEARCH`：案例发现；
- `CASE_ORIGINAL_TEXT`：裁判/案例原文获取；
- `CASE_ID_VERIFY`：案号/案例身份核验；
- `LEGAL_CITATION_LOCATOR`：条款、裁判理由、原文位置定位。

### 文件与办公
- `PDF_READ`；
- `PDF_PAGE_RENDER`；
- `OCR`；
- `DOCX_READ`；
- `DOCX_EDIT`；
- `TRACK_CHANGES`；
- `PDF_RENDER`；
- `SPREADSHEET_READ_WRITE`。

### 外部数据与知识
- `PUBLIC_WEB_SEARCH`；
- `BUSINESS_REGISTRY_QUERY`；
- `USER_KNOWLEDGE_BASE`；
- `CLOUD_FILE_READ`；
- `PROJECT_FILE_READ`。

### 多模态
- `IMAGE_UNDERSTANDING`；
- `AUDIO_TRANSCRIPTION`；
- `VIDEO_UNDERSTANDING`。

### 法律可视化
- `VECTOR_DIAGRAM_RENDER`：SVG/矢量确定性图形；
- `RASTER_DIAGRAM_RENDER`：PNG 等位图派生；
- `GRAPH_LAYOUT`：关系图、流程图、时间线等确定性布局；
- `INTERACTIVE_VISUAL_RENDER`：自包含 HTML/Web 或 Host-native 交互成果；
- `VISUAL_SNAPSHOT_EXPORT`：把当前交互视图冻结为静态快照；
- `PRESENTATION_GRAPHIC_EXPORT`：PPTX/演示型可编辑图形；
- `GENERATIVE_VISUAL_ENHANCEMENT`：只用于确定性法律结构之上的可选视觉增强。

可视化 Slot 不写死 D3、G6、Cytoscape、Graphviz 或任何具体前端库。Provider/工具只在 Adapter/Host 层解析；`GENERATIVE_VISUAL_ENHANCEMENT` 可用也不等于已授权敏感案件内容外发，更不取得事实、金额、日期、关系、方向或状态的语义所有权。

## Resolution rules

1. 先解析当前任务真正需要的 Slot，不因为 Host 里“有工具”就调用；
2. Host/Adapter 再把 Slot 映射到真实工具或 Provider；
3. 用户/团队明确 Provider 偏好或排除项时尊重配置，但不得牺牲关键来源可核验性；
4. 多个 Provider 都能完成时，按原始性、完整性、法域/时间覆盖、权限、成本、隐私与当前可用性选择；
5. Provider 名称只进入真实调用记录、来源标注、配置或 Adapter 状态，不成为爽律skill 核心法律规则；
6. Slot 可用、Connector 已连接、API Key 存在均不等于敏感材料外发授权；
7. 关键正确性无法满足时使用 `BLOCKED`，不得用模型记忆伪装为工具结果。

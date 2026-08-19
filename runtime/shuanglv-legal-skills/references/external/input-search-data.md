# External｜Input / Search / Data

`unit_id: unit.external.input-data`

**Scope：** Actual OCR/multimodal/search/legal DB/spreadsheet/database execution contract.

## Trigger
- Task requires actual OCR/multimodal parsing/search/database/spreadsheet operation.

## Negative Trigger
- No external data operation needed.

## Essential Procedure
1. Execute only via available capability.
2. Retain provenance/processing method/locator/quality state.
3. Do not upgrade OCR/transcript/parsed content into original verified truth.

## Deepening Conditions
- Low-quality OCR, incomplete retrieval, conflicting data.

## Exit Sufficiency
- Usable data is returned with fidelity state or honest failure/downgrade.

## Professional Results
- processed/retrieved data with provenance and quality state

## Conditional Guards
- unit.guard.external-processing

## Input Fidelity Contract｜文件与多模态输入保真

外部输入能力的目标不是“尽量读出文字”，而是向法律分析提供**可定位、可核验、尽可能保留结构与上下文**的数据。

### 最低保真要求

- 文本 PDF：正文与页码/位置对应；
- 扫描 PDF/图片：OCR/视觉结果保留页码或区域定位；
- 表格：尽量保留 Sheet、行列、公式、合并单元格及会影响法律理解的关键格式；
- 音频/视频：关键内容尽量保留时间戳和说话人状态；
- DOCX/PPTX：按任务需要保留结构、批注、修订或对象关系；
- 仅审阅部分页/部分文件时必须明确范围。

读取异常必须显式标记：页码错位、OCR 低质量、表格结构丢失、文件损坏/加密、图片/附件未读、音频不可辨、部分审阅等。`RECEIVED ≠ OPENED ≠ REVIEWED`。

### Tool Resolution

优先顺序：`当前 Agent 原生能力 → 用户已有工具 → 本地能力 → 用户控制基础设施 → 第三方云服务`。进入第三方云处理敏感材料前，必须加载 External Processing Guard。

大批材料不应简单拼成长上下文；先建立材料目录与 ReviewQuestionSet，分批抽取可追溯记录，再进行跨文件比较。

### Credential Security

需要 API 凭证时，仅使用 Host 安全机制（例如环境变量、Secret Store、受控 Connector）；不得把密钥写入项目文件、交付物、日志或 Matter State。**API Key ≠ 对当前材料外发的授权。**

### Legal Source Adapter Boundary

法律数据库、官方检索源、用户知识库、MCP/其他数据库等均通过 Adapter 执行各自的查询语法、认证、分页和原始字段解析；爽律skill Runtime 不绑定供应商。Adapter 返回法律研究候选结果时，应归一化到 Interop 的 `Legal Source Connector Contract`，至少真实传递 `retrieval_scope`、`source_completeness`、`failure_or_degradation`、原文定位和权限/敏感性状态。

Adapter 不得把片段返回伪装成全文，不得把元数据缺失静默补齐，也不得把 provider 自带的“权威/相关度”标签直接升级为爽律skill 的 SourceRole、规范效力判断或案例可比性结论。连接器降级时保留真实范围与失败状态，由 Research 决定继续检索、限制结论或阻断。

### Knowledge Base Boundary

用户知识库可作为事实线索、内部制度、历史成果、模板和经验来源，但“知识库里写过”不自动等于现行法律或当前案件已核验事实；按用途进入相应 SourceRole/FactStatus。

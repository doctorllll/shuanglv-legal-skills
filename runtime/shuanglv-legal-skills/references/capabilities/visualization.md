# Visualization｜法律可视化

`unit_id: unit.cap.visualization`

**Scope：** 决定法律任务是否值得可视化，并把既有 Facts / Evidence / Reasoning / Review 等上游专业对象组织为可追溯的 `LegalVisualSpec`；负责目的、受众、结构识别、图型路由、信息取舍、表达立场、静态/交互判断与视觉质量要求。**不**拥有第二套事实/证据真值，不直接承担 SVG 坐标、Canvas/WebGL、前端框架或文件系统执行。

## Trigger
- 用户明确要求时间线、关系图、交易结构图、资金流、流程图、证据图、问题树、论证图、图表、交互图、动态展示、庭审展示或其他可视化成果。
- 多主体、多时间节点、多跳资金/资产/数据流、多阶段履行/程序、复杂证据或论证结构，用纯文字会显著增加理解成本。
- 正式法律成果、客户汇报、庭审/仲裁演示或内部分析需要把隐藏结构显式化。
- 交互筛选、钻取、观点切换或来源回看能提供静态图无法提供的明显增益。

## Negative Trigger
- 简单事实或单一结论，图形不能降低理解成本。
- `FORMAT_ONLY` 且不存在图形交付要求。
- 仅因材料出现“时间、关系、证据、资金”等词。
- 图形会丢失决定性限定条件、制造虚假确定性，或把相关性误画为因果。
- 交互只增加“炫酷感”，不增加分析、理解、说服或操作价值。

## Persuasion ≠ Distortion｜说服不等于扭曲

说服型可视化允许围绕代理/辩护目标进行主线选择、视觉层级和重点强调，但不得把推断升级为事实、把相关性画成因果、改变金额/日期/关系方向、隐藏决定性反向证据，或以空间大小、颜色、位置等设计手段制造来源不支持的确定性。选择性展示必须与“完整事实”区分，必要时提供全貌视图或明确说明范围。

## Essential Procedure
1. 运行 `Visual Necessity Test`；无明显增益时不画。
2. 明确 `purpose + audience + use_context`。
3. **Reuse Before Recompute**：从既有 canonical objects 读取候选，不重新抽取第二套事实/证据/争点。
4. 识别主要信息结构：时间、层级、网络关系、交易、资金、流程、证据、要件、争点、论证、方案、统计。
5. 先形成完整候选集合，再确定主线，再按任务目的精简；不得为了好看静默删除决定性反向信息。
6. 选择 `visual_type / layout_family`，记录为何该图型优于表格或文字。
7. 确定 `perspective / stance / emphasis`：分析型、说服型、操作型或解释型。
8. 判断 `STATIC / INTERACTIVE / BOTH`；静态是默认基础，交互只在有增益且 Host 支持时进入。
9. 生成 `LegalVisualSpec`，只引用 canonical object refs；必要显示快照同时保留 `object_ref + snapshot_at`。
10. 交给 `LegalArtifactContract + CapabilitySlot + Document Render/Renderer` 真正生成实体成果。
11. 回收实际 artifact 做 `Semantic Fidelity → Cognitive Clarity → Interaction → Visual Quality` QA。
12. 用户未要求交互时：先完成静态；若交互明显有价值且当前 Host 真正支持，再询问是否同时需要交互版。用户已明确要求交互时直接生成，不重复确认。
13. 生成式视觉增强与交互是两个独立选择；只有明显有价值且满足授权/能力边界时才进入。

## Deepening Conditions
- 节点/关系/事件数量大到一张静态图无法可读呈现。
- 需要按主体、时间、金额、证据类型、事实状态筛选或钻取。
- 需要控辩、原被告或不同案件理论切换。
- 正式交互成果需要冻结 ViewState、版本/hash 与静态伴随件。
- 生成式视觉增强会接触敏感材料或进入外部处理。

## Exit Sufficiency
- 已明确“为什么画/为什么不画”；
- 图型与任务结构、受众匹配；
- 所有关键节点/关系可回到上游对象或来源；
- 静态/交互形态决定真实匹配 Host 能力和用户要求；
- 任何视觉强调未改变事实、状态、方向、金额、日期或证据独立性；
- 实体文件由实际 Renderer 创建并验证，或已诚实降级。

## Professional Results
- `VisualNecessityDecision`
- `LegalVisualSpec`（兼容 `DiagramSpec v1`）
- `ViewState`（如适用）
- `VisualProfile`
- visualization QA result

---

# 1. Visual Necessity Test｜可视化必要性判断

进入可视化需要回答：**图形是否比文字/表格更快、更准确地揭示当前任务的重要结构？**

以下任一信号通常支持可视化：

- 多主体关系难以线性叙述；
- 时间顺序、时间间隔或持续期间本身影响法律判断；
- 资金、资产、数据存在多跳流转；
- 多阶段流程、条件、审批、履行或程序依赖；
- 一个待证命题对应多项支持证据、反向证据、同源材料与缺口；
- 多个要件、争点、规则、事实之间有层级或交叉；
- 多个方案/案件理论需要比较；
- 材料规模使线性阅读成本显著上升；
- 用户明确要求；
- 交互筛选/钻取/路径高亮/来源回看能增加静态图无法提供的价值。

以下情形原则上不建议可视化：

- 一句话或一张小表已经足够；
- 图只是把文字换成几个框；
- 图无法保留关键限定语、争议状态或不确定性；
- 受众只需要一个明确结论；
- 正式载体不可靠且无静态伴随件；
- 图会把 `INFERRED` 画成 `VERIFIED`、把观点画成事实、把同源材料画成独立印证。

`VisualNecessityDecision` 至少记录：`decision`、`purpose`、`audience`、`structure_signals`、`expected_gain`、`risk_if_visualized`、`preferred_nonvisual_alternative`（如不画）。

---

# 2. Purpose / Stance｜目的与表达立场

`purpose` 至少支持：

- `ANALYTICAL`：内部探索复杂事实、关系、证据、时间与冲突；
- `ADVOCACY`：庭审、仲裁、辩护/代理意见、说服性汇报；
- `OPERATIONAL`：合同、交易、履行、尽调、审批、交割、条件和风险触发；
- `EXPLANATORY`：向客户或非专业受众解释程序、结构和复杂关系。

`ADVOCACY` 允许强调，但不允许失真：

- 强调必须有 `emphasis_reason`；
- 选择性展示需要能够说明是否存在被隐藏的重大反向信息；
- 不得通过节点大小、空间远近、箭头粗细、颜色饱和度暗示上游没有支持的“重要性/因果性/确定性”；
- 对方观点、我方主张、推断、已核验事实必须保持可区分状态。

---

# 3. Visual Routing｜图型路由

| 信息结构 | 推荐 `visual_type` | 核心纪律 |
|---|---|---|
| 一般先后顺序 | `TIMELINE` | 不用均匀间距暗示真实时间比例 |
| 精确日期/间隔 | `PROPORTIONAL_TIMELINE` | 时间比例来自真实日期，不手工拉伸 |
| 持续期间 | `PERIOD_GANTT` | 起止边界与是否精确必须可见 |
| 多主体并行时间 | `SWIMLANE_TIMELINE` | lane 只表达主体/程序层，不制造优先级 |
| 自由主体网络 | `ENTITY_RELATIONSHIP` | 关系类型、方向、依据、状态可追溯 |
| 严格层级/控制 | `HIERARCHY_RELATIONSHIP` | 只在真正层级关系存在时使用树 |
| 交易结构 | `TRANSACTION_STRUCTURE` | 合同角色与实际履行关系可分层 |
| 资金流 | `MONEY_FLOW` | 金额、币种、账户、方向、时间不得漂移 |
| 履行/业务流程 | `PERFORMANCE_FLOW` | 顺序、条件、责任主体、分支准确 |
| 法律/程序流程 | `PROCEDURE_FLOW` | 期限、例外、程序阶段与适用前提可见 |
| 证据—事实 | `EVIDENCE_MAP` | 支持/反向/缺口/同源不能被抹平 |
| 要件—事实—证据 | `ELEMENT_EVIDENCE_MAP` | 涵摄与证明结构同时可追溯 |
| 争点层级 | `ISSUE_TREE` | 层级不等于结论强弱 |
| 论证支持/攻击 | `ARGUMENT_MAP` | 观点不得静默升级为事实 |
| 方案比较 | `OPTION_TREE` / `COMPARISON_VIEW` | 成本、风险、前提与不可逆点并列 |
| 真实数量/统计 | `CHART_OR_TABLE` | 无数据不画数值图，不用面积误导 |

图型名称允许由 Renderer 映射到实现库，但 Runtime 不绑定 D3、G6、Cytoscape、Graphviz、Mermaid 或具体 UI 框架。

---

# 4. LegalVisualSpec｜DiagramSpec v2

`LegalVisualSpec` 是法律语义与物理渲染之间的中间合同；兼容旧 `DiagramSpec` 的节点/关系/标签/来源/布局意图，但不把最终像素坐标作为法律语义真相。

最小字段建议：

```text
visual_id
schema_version
matter_id?
purpose
audience
use_context
visual_type
layout_family
node_refs[]
relation_refs[]
event_refs[]
evidence_refs[]
issue_refs[]
argument_refs[]
source_refs[]
source_locators[]
native_status[] / status_authority[]
uncertainties[]
perspective
stance
emphasis[]
visible_layers[]
hidden_by_default[]
interactive_suitable
requested_presentation_modes[]  # STATIC / INTERACTIVE / BOTH
editable_requirement
print_requirement
mobile_requirement
recommended_layout
ordering_constraints[]
grouping_constraints[]
time_scale_mode
directionality
split_recommendation
density_hint
snapshot_at?
data_version_or_hash?
```

规则：

1. `*_refs` 优先引用 Facts/Evidence/Reasoning/Review/Matter 的既有对象 ID；
2. 为实体 artifact 保存显示快照时，同时保留 `object_ref + snapshot_at`；
3. `native_status` 必须保留 canonical owner 语义，Visual 层只能显示，不得重定义；
4. 推断、争议、未知应有可辨识的视觉状态，但颜色不能是唯一编码；
5. Renderer 可以生成 canonical geometry，但坐标属于派生结果，不反写为法律事实；
6. 静态版与交互版必须来自同一个 `LegalVisualSpec` 或同一版本派生快照。

---

# 5. ViewState｜视图状态不是事实状态

`ViewState` 记录“当前怎么看”，不记录“事实是什么”。建议字段：

`visual_id`、`view_state_id`、`filters`、`selected_nodes`、`selected_relations`、`active_layers`、`time_window`、`perspective`、`expanded_groups`、`zoom_or_viewport`、`sort_or_focus_path`、`created_at`、`data_version_or_hash`。

硬规则：

- **隐藏 ≠ 删除；筛选 ≠ 否认；聚焦 ≠ 事实更重要。**
- ViewState 不得修改 Fact/Evidence/Issue/Argument 的 native status。
- 正式交互交付应能冻结 `ViewState snapshot + data hash/version + timestamp`。
- 默认过滤不得把决定性反向证据、重大不利事实或 materially unresolved 项静默隐藏；如因受众目的需要隐藏，必须有可发现的状态提示与恢复入口。

---

# 6. Static / Interactive Decision｜静态与交互

## 6.1 默认

- 静态是可靠基础交付；交互是有明确增益时的增强交付；两者都可以是正式成果。
- 用户未指定：先完成静态；只有交互明显增益且 Host 真正支持，才在静态完成后询问是否增加交互版。
- 用户明确要求交互：直接进入交互路径，不重复确认。
- 正式交互成果原则上同时有静态 companion snapshot，便于打印、归档、长期复现与兼容。
- 交互失败时回退静态，不得拖垮已能完成的核心任务。

## 6.2 `interactive_suitable = true` 的典型信号

- 节点/关系超过单页可读容量；
- 需要主体/时间/金额/证据类型/事实状态筛选；
- 需要点击节点查看来源；
- 需要时间滑块、路径高亮、展开/折叠；
- 需要不同案件理论/立场切换；
- 需要多视图联动或从同一大图导出多个静态视图。

## 6.3 最小交互能力分层

**P0：** 节点详情、来源定位、搜索、基础筛选、图层显示/隐藏、当前筛选状态可见、恢复默认、导出当前静态快照。

**P1：** 时间滑块、focus+context、路径高亮、多视图联动、展开/折叠、事实状态筛选、观点切换、保存/恢复 ViewState。

**P2 预留：** 自动聚类、异常关系提示、证据缺口提示、冲突事实提示、大规模 Canvas/WebGL、Visual Analytics 工作台。P2 不作为 v0.50 核心 Release 必须项。

---

# 7. VisualProfile｜视觉配置

`VisualProfile` 只改变呈现，不改变语义。至少支持：

- `PROFESSIONAL_GENERAL`：专业通用；
- `JUDICIAL_PRINT`：司法/打印优先，黑白可辨；
- `PRESENTATION`：客户/庭审/汇报演示；
- `CUSTOM_BRAND`：用户/律所明确提供的品牌规范。

Design Token contract 至少覆盖：

- `Typography`：中文标题、节点、注释、数字层级；
- `Color`：低饱和、少色、语义化、黑白仍可辨；
- `Spacing`：间距、边距、层级、留白；
- `Shape`：节点类型、边框、圆角、线型；
- `Relation`：方向、支持/攻击/不确定关系；
- `State`：selected / filtered / disabled / disputed / inferred；
- `Motion`：短、可关闭，只解释状态变化；
- `Accessibility`：颜色非唯一编码、键盘/文字等价路径、reduced motion。

设计目标：**克制、清晰、秩序、精确、现代、专业；不以装饰密度代替信息结构。**

---

# 8. Optional Generative Enhancement｜可选生成式视觉增强

生成式视觉增强不是结构来源，必须在确定性语义之后：

`上游对象 → LegalVisualSpec → 确定性静态/交互图 → 可选生成式视觉增强`

允许：背景、非语义插画、装饰性图标、视觉氛围、封面性增强。

禁止让生成式模型决定或改写：人名、金额、日期、比例、证据编号、箭头方向、法律关系、事实状态、证据独立性、争点结论。

- 用户开头明确要求高级信息图/生成式视觉版，可视为已选择该表现目标；
- 否则只有明显视觉增益时才询问；
- 涉及敏感案件材料且调用外部服务时，必须进入 `External Processing Guard`；
- 增强后必须做 semantic consistency QA；
- 生图失败不得使确定性版本失败。

---

# 9. QA｜从“正确”到“拿得出去”

## 9.1 Semantic Fidelity QA｜法律语义准确（Hard Gate）

任何一项命中即不得 FINAL：

- A→B 被改成 B→A；
- 金额/币种/日期/比例漂移；
- 模糊日期被画成精确日期；
- `INFERRED / ALLEGED / DISPUTED / UNKNOWN` 被画成 `VERIFIED`；
- 同源材料视觉上变成独立印证；
- 对方观点/我方主张被画成事实；
- 筛选后默认隐藏决定性反向证据且无提示；
- 节点/关系引用不存在；
- 生成式增强改写法律语义。

## 9.2 Cognitive Clarity QA｜认知清晰

- 一图一主题；过密则拆图；
- 主线、分支、例外与不确定性可区分；
- 不用布局制造无依据的因果/层级；
- 时间比例模式与实际语义一致；
- 手机/常规屏幕/打印场景满足任务要求。

## 9.3 Interaction QA｜交互高效

- 当前筛选/隐藏状态可见；
- 可恢复默认视图；
- 搜索/筛选/图层不会改变底层数据；
- 来源定位真实可达；
- 正式交互版能冻结 ViewState 与版本；
- 导出快照与当前视图语义一致。

## 9.4 Visual Quality QA｜视觉成熟

- 无明显 overlap、clip、off-canvas、箭头遮挡、文本溢出；
- CJK 字体有合理 fallback；
- 层级、留白、对齐、字号和线型一致；
- 黑白打印可辨；
- 视觉强调有节制且与目的相符。

## 9.5 Accessibility QA｜可访问性

- 颜色不是唯一状态编码；
- 动效可关闭/支持 reduced motion；
- 关键图形有文字等价说明或可读取标签；
- 交互控件在当前 Host 能力允许时支持键盘或等价访问路径。

---

# 10. 与其他 Owner 的边界

- `Facts / Evidence / Reasoning / Review`：拥有事实、证据、争点、论证、来源与状态；Visualization 只引用。
- `LegalArtifactContract`：定义 `LEGAL_VISUALIZATION` 成果需要哪些专业字段、静态/交互/快照与真实性要求。
- `CapabilitySlot`：声明 `VECTOR_DIAGRAM_RENDER / GRAPH_LAYOUT / INTERACTIVE_VISUAL_RENDER` 等能力需求。
- `Document Render`：拥有物理渲染、deterministic geometry、SVG/PNG/PDF/PPTX/HTML 派生、字体/换行/几何 QA 与文件存在真实性。
- `Formal Delivery Guard`：正式动态成果的可打开、离线/依赖、版本、ViewState、静态伴随件与多文件一致性门。
- `External Processing Guard`：敏感材料外发/第三方生图或云渲染授权。
- `Specialist/Host`：可以实现复杂布局和交互，但不得取得法律事实/证据/论证的 canonical ownership。

# Facts｜事实与结构化审阅

`unit_id: unit.cap.facts`

**Scope：** Task-driven review and fact modeling from materials.

## Trigger
- Directive asks to review/reconstruct/compare/structure material facts, chronology or gaps.
- A substantive capability cannot proceed safely because material facts/source state are unresolved.
- Large or heterogeneous materials require structured review questions.

## Negative Trigger
- Pure wording rewrite with no fact validation requested.
- FORMAT_ONLY / render-only task.
- Do not trigger solely because payload contains legal/factual terminology.

## Essential Procedure
1. Define task-specific ReviewQuestionSet.
2. Register material/source state before substantive use.
3. Extract only task-relevant facts with locators.
4. Mark ALLEGED/INFERRED/UNKNOWN rather than upgrading silently.
5. Surface conflicts and decision-changing gaps.

## Deepening Conditions
- Multi-volume or multi-source matter.
- Material contradictions.
- Domain extension requires additional fact fields.
- Fact gap changes downstream legal conclusion.

## Exit Sufficiency
- Task-relevant facts are sufficient for the requested next capability.
- Material gaps are explicitly labeled and no further available source can resolve them.

## Professional Results
- source-linked fact records
- chronology
- fact conflicts/gaps
- review question results

## External / Delegated Capability
- `unit.external.input-data`：实际 OCR/多模态/表格/数据库等输入执行。
- `unit.interop.batch`：当批量规模、语义不确定性、成本或恢复需求使共享 batch orchestration 有价值时加载；Facts 仍拥有 ReviewQuestionSet 与事实建模。


## Structured Review Method

## 一、目的

复杂法律事项往往同时包含大量合同、卷宗、聊天记录、表格、交易凭证、行政材料、公司文件或其他来源。爽律skill 对这类材料不默认采用“逐份长摘要”的方式，而应优先建立**可横向比较、可追溯、可继续分析的结构化审阅记录**。

该规范适用于刑事、民商事、合同、尽调、法律顾问、专项调查和复杂法律研究。它不是刑事阅卷专用工具。结构化审阅形成的材料记录和来源定位，应继续按 `references/capabilities/review.md` 的全链路溯源规则连接到事实、证据、问题、规则、论证和最终交付。

## 二、何时展开结构化审阅

满足以下任一情况时，原则上建立结构化审阅表或同等结构化对象：
- 多文件、多版本或多来源材料；
- 需要比较同类文件、当事人陈述或交易记录；
- 存在证据冲突、事实争议或时间线问题；
- 需要把材料与请求、抗辩、罪名、要件、风险或法律问题逐项连接；
- 需要批量审阅合同、卷宗、尽调文件或长期事项材料；
- 用户明确要求清单、矩阵、表格或批量分析。

单一、简单材料可以只建立简化材料记录，不为了形式完整制造大表格。

## 三、基础材料记录

每份材料至少尽可能记录：

| 字段 | 含义 |
|---|---|
| `material_id` | 本次任务内唯一标识 |
| `name` | 文件或材料名称 |
| `material_type` | 合同、笔录、聊天记录、账单、判决、表格等 |
| `source` | 谁提供、从何处取得 |
| `date_created` | 形成时间，未知则明确标记 |
| `review_status` | RECEIVED / REVIEWED / PARTIAL / UNREADABLE |
| `source_locator` | 页码、段落、单元格、时间戳等 |
| `actors` | 涉及主体 |
| `events_or_topics` | 关键事件或主题 |
| `fact_contribution` | 能支持、反驳或影响哪些事实 |
| `adverse_content` | 对当前客户立场可能不利的内容 |
| `contradictions` | 与哪些材料存在冲突或差异 |
| `open_questions` | 仍需核验的问题 |
| `linked_issues` | 对应哪些法律或业务问题 |
| `next_action` | 补件、询问、检索、核验或其他动作 |

`RECEIVED` 不等于 `REVIEWED`。

## 四、业务扩展字段

### 民商事争议解决

可增加：
- 对应请求、否认、抗辩或反抗辩；
- 对应构成要件；
- 待证命题与证明责任；
- 对我方/对方的支持程度；
- 证据缺口；
- 对保全、和解或执行的影响。

### 刑事案件办理

可增加：
- 指控或控告待证命题；
- 罪名或法律要件；
- 控方、辩方、被害人侧意义；
- 证据独立性和印证关系；
- 反向证据和替代解释；
- 程序、强制措施、财产或量刑意义。

### 合同与交易工作

可增加：
- 条款或章节定位；
- 交易阶段；
- 权利、义务、条件、陈述、保证；
- 履行依赖；
- 风险场景；
- 客户立场；
- 修改或谈判建议。

### 尽职调查与专项调查

可增加：
- 调查主题；
- 核验来源；
- 红旗事项；
- 信息缺口；
- 风险影响；
- 是否需要补充文件或第三方核验。

### 法律顾问与专项法律分析

可增加：
- 对应法律问题；
- 业务背景和决策意义；
- 事实状态；
- 需要研究的规则；
- 选项和行动建议。

### 法律研究

可增加：
- 文献类型和权威层级；
- 支持或反对哪个法律命题；
- 适用时间、地域和主体；
- 案例可比事实；
- 是否属于反向来源；
- 仍需追索的上位或原始来源。

## 五、从审阅表到案件分析

结构化审阅不是最终成果，应进一步生成或更新，并按 `references/matter/result-invalidation.md` 的依赖/回写规则把这些对象交给后续分析：

```text
材料记录
→ 事实记录
→ 证据对象
→ 问题记录
→ 请求/抗辩/指控/风险
→ 法律研究
→ 分析发现
→ 策略与交付
```

一份材料可以关联多个事实和问题；一个事实也可能由多份材料共同支持或反驳。不得强迫一对一映射。

## 六、多文件交叉分析

结构化审阅完成后，按任务需要进行：
- 时间线比对；
- 主体和关系比对；
- 金额、资金、数量比对；
- 同一事实不同来源比对；
- 同一主体前后陈述比对；
- 版本差异；
- 应出现但缺失的材料；
- 重大不利材料；
- 重复材料和同源信息；
- 需要进一步核验的冲突。

## 七、输出形态

爽律skill 只规定审阅结果应具备的字段和质量。实际载体可以是 Markdown 表格、电子表格、数据库临时表、JSON 或当前 Agent 支持的其他结构。

当数据量大、需要筛选排序、公式或批量操作时，应优先调用当前 Agent 可用的电子表格能力；爽律skill 本身不实现表格软件。

## 八、质量要求

- 每项重要结论能回到原始材料定位；
- 未读材料不得假装已读；
- 不把 OCR 识别结果自动当作原文无误；
- 同一来源的重复信息不得冒充独立印证；
- 有利和不利材料同时保留；
- 结构化字段缺失时标记未知，不自行补齐；
- 表格中的压缩表达不得丢失决定性上下文。

## 九、任务驱动的审阅问题集

复杂批量审阅原则上先按本文件下文“任务驱动的审阅问题集”确定本次真正要从材料中回答的问题，再展开业务扩展字段。基础字段负责来源、状态和可追溯性；动态问题负责本次争点。不得把某一业务模板永久固定为所有材料的审阅列。

---

## 一、核心规则

结构化审阅表不应是一张对所有案件固定不变的“大表”。除通用基础字段外，复杂材料审阅应根据本次任务、问题树和客户目标动态生成**审阅问题集**，再把问题转化为列、字段或审阅标签。

其核心关系为：

```text
TaskProfile
→ IssueTree
→ ReviewQuestionSet
→ StructuredReviewRecord
→ Fact / Evidence / Issue
```

## 二、问题集的来源

审阅问题应优先来自：

- 当前任务要解决的核心问题；
- 构成要件、请求/抗辩、指控/辩护或风险模型；
- 已识别的信息缺口；
- 需要横向比较的事实维度；
- 对抗性审查发现的薄弱点；
- 用户明确要求的提取字段。

不得因为某模板存在某一列，就在所有任务中机械提取。

## 三、每个审阅问题至少定义

- `question_id`：稳定标识；
- `label`：表头或短标签；
- `question`：真正要从材料中回答的问题；
- `answer_type`：文本、日期、金额、枚举、布尔、引用等；
- `source_locator_required`：是否必须保留原文定位；
- `linked_issue_ids`：服务于哪些争点；
- `comparison_mode`：是否用于跨文件横向比较；
- `missing_value_policy`：无法回答时必须如何标记。

## 四、示例

### 合同批量审阅

如果本次目标是识别控制权变更风险，审阅问题可以围绕：是否存在控制权变更条款、触发条件、通知义务、解除/终止权、豁免、原文定位等；不必同时提取与任务无关的几十个普通合同字段。

### 刑事卷宗

如果争点是涉案金额，审阅问题可以围绕：各主体对金额的具体陈述、陈述时间、金额口径、计算基础、客观流水支持、相互矛盾、同源信息和原文定位。

### 民商事争议

如果争点是解除权是否成立，问题集可以围绕履行义务、履行期限、违约事实、催告、补救、解除通知、对方异议、损失和相关证据。

## 五、动态更新

新法律研究或新材料改变争点时，允许增加、修改或停用审阅问题。问题集发生重大变化后，应评估已经审阅的材料是否需要按新问题重新扫描，不得只对后来材料使用新标准。

## 六、质量要求

- 每个关键答案尽量保留来源定位；
- “未找到”与“不存在”必须区分；
- 无法判断时使用未知/待核，不推测填充；
- 横向比较字段的定义和口径必须一致；
- 问题集应服务于案件分析，而不是为了表格完整；
- 表格提取结果不能替代对决定性原文的上下文复核。

---

## 一、定位

当当前 Agent 或输入工具能够从文件、扫描件、表格、聊天、音视频中抽取结构化信息时，爽律skill 可以把这些结果转化为**法律对象候选**，以提高后续结构化审阅效率。

候选对象不是已核验事实。其默认状态必须与原始材料和核验状态区分。

## 二、常见候选对象

- PERSON：自然人；
- ORGANIZATION：组织或主体；
- EVENT：事件或行为；
- DATE：日期/期间；
- AMOUNT：金额/数量；
- RELATION：主体关系；
- DOCUMENT：文件或凭证；
- CLAIM：陈述、主张或指控；
- LEGAL_TERM：法律或业务术语；
- OTHER：其他任务相关对象。

## 三、候选对象至少保留

- 所在原始材料；
- 精确来源定位；
- 抽取到的原文或必要上下文；
- 规范化字段；
- 抽取方式；
- 当前抽取状态；
- 核验状态；
- 与既有对象可能的关联。

## 四、状态边界

建议区分：

- `EXTRACTED`：成功提取，但尚未核验；
- `AMBIGUOUS`：原文存在歧义；
- `CONFLICTING`：与其他来源存在冲突；
- `UNREADABLE`：无法可靠读取。

核验状态至少区分：

- `NOT_VERIFIED`；
- `VERIFIED`；
- `REJECTED`。

`EXTRACTED` 绝不自动等于 `VERIFIED`。OCR、语音识别、实体抽取和模型归一化都可能出错，重要对象仍需回到原文定位复核。

## 五、进入正式事实模型

只有完成必要核验后，候选对象才可以用于创建或更新 FactRecord、EvidenceItem、MaterialRecord 等正式工作对象；尚未核验的候选可以作为检索、询问或审阅线索，但不得作为无保留事实结论。

## Quick Understanding Profile｜事项快速理解与法律对象候选

### 1. 事项快速理解包

当用户明确需要快速理解，或复杂材料在进入深度分析前确有显著理解收益时，可生成轻量 `QuickMatterBrief`。它不是强制前置步骤，也不因“材料多”自动触发。

按需包含：
1. 一句话事项说明；
2. 主体、标的/行为、金额、期限、关键节点、当前程序/履行状态等核心概要；
3. 最有助于理解的一项或数项结构化示意：主体关系、交易结构、资金流、时间线、履行流程、证据关系、问题树或方案树；
4. 3—7 个核心关注点；
5. 重大未知、争议或待核验事项；
6. 详细成果导航。

概要必须继承 FactStatus 与 SourceLocator；图形化表达不是新的事实来源。

### 2. LegalObjectCandidate

OCR、视觉、语音转写、表格解析或模型抽取得到的人物、组织、事件、日期、金额、关系、文件、主张等，先进入候选状态，不直接升级为正式事实。

候选至少保留：原始材料、精确定位、必要上下文、规范化值、抽取方式和当前状态。推荐状态：

`EXTRACTED / AMBIGUOUS / CONFLICTING / UNREADABLE`，核验状态另分 `NOT_VERIFIED / VERIFIED / REJECTED`。

只有完成必要核验后，候选才进入正式 Fact / Evidence / Material 记录；未核验候选只能作为检索、追问或审阅线索。


## Batch orchestration handoff

Facts 负责定义**本次材料到底要回答什么问题**，不独占批次调度。需要批量处理时：

`TaskProfile → IssueTree → ReviewQuestionSet (Facts) → BatchJobProfile / Pilot / checkpoint (Interop Batch) → StructuredReviewRecord (Facts) → downstream legal analysis`

- 小批量、低风险、结构稳定任务可以直接执行，不强制 pilot；
- 大规模/高成本/异质材料/错误易扩散时，由 `unit.interop.batch` 负责 Pilot Sample Gate、BatchRunRecord、异常分桶和恢复；
- 任何批量状态不得改变 FactStatus、SourceLocator 或 Evidence 的 canonical authority。

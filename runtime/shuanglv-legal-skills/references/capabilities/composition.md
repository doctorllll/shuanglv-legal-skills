# Composition｜法律写作与交付内容

`unit_id: unit.cap.composition`

**Scope：** Legal drafting, semantic rewrite, structured deliverable construction and finalization.

## Trigger
- Directive asks to draft/generate/rewrite/substantively revise a legal deliverable.
- A prior capability result must be expressed as a legal document or client-ready text.

## Negative Trigger
- FORMAT_ONLY task that expressly forbids content change routes to document-render contract instead.
- Do not load Research/Evidence/Strategy merely because source text contains those concepts.

## Essential Procedure
1. Fix reader, purpose and deliverable mode.
2. Preserve instructed position and semantic constraints.
3. Use only supported facts/law/evidence.
4. Apply legal-work preference/House Style when available.
5. Finalize meaning separately from physical rendering.

## Deepening Conditions
- Formal legal deliverable.
- Long/complex document with multiple issue sections.
- User-provided template/House Style.
- Substantive change would create admission/waiver/risk.

## Exit Sufficiency
- Requested content is complete, coherent, supported and semantically finalized; rendering may still be delegated.

## Professional Results
- draft/rewrite
- document architecture
- citations/source locators when material
- semantic finalization state

## Conditional Guards
- unit.guard.formal-delivery

## External / Delegated Capability
- unit.external.document-render


## Composition / Document Quality Method

## 一、这个技能负责什么

这是所有业务技能共同使用的最后一道质量控制。它不重新办一遍案件，也不替换业务技能的实体判断，而是把已经形成的事实、法律研究、分析结果和草稿，转化为**内容完整、事实可靠、论证清楚、语言自然、格式规范、引用可追溯、版本真实、可以正式交付的文书**。

## 二、主流程

```text
确认谁写、写给谁、为什么写
→ 检查内容是否回答真正任务
→ 检查关键事实及其状态
→ 重构文书论证结构
→ 根据读者调整详略和语言
→ 统一术语、句法和段落
→ 检查法律引用、证据引用和附件
→ 套用对应Composition Capability和统一样式
→ 明确输出格式、修订方式和版本
→ 分轮校对
→ 最终交付检查
```


## 三、执行步骤速查表

| 步骤 | 要做什么 | 主要方法 | 阶段产物 |
|---|---|---|---|
| 1. 文书角色 | 明确作者、读者、目的和文种 | 写作者—读者—目的分析 | 文书任务说明 |
| 2. 内容检查 | 判断是否真正回答任务 | 上游分析与文稿逐项对照 | 缺失问题清单 |
| 3. 事实检查 | 防止事实状态被写错 | 事实—来源—状态核验 | 事实修正清单 |
| 4. 论证重构 | 让观点可以被跟随 | 观点—事实/证据—规则—分析—回应—结论 | 论证结构 |
| 5. 读者适配 | 调整专业程度、顺序和详略 | 法院/机关/客户/公众差异化表达 | 表达方案 |
| 6. 语言编辑 | 提高准确性和自然度 | 术语一致、完整自然段、去AI碎片化 | 清洁文本 |
| 7. 引用核验 | 确保法律、案例、证据可回查 | 来源和附件一致性检查 | 引用修正 |
| 8. 文种规范 | 应用不同文书的结构要求 | Composition Capability + 统一样式 | 版式要求 |
| 9. 交付模式 | 明确DOCX/PDF/修订/批注/版本 | 输出契约、能力真实性 | 交付组合 |
| 10. 最终校对 | 分开检查语义和机械错误 | 多轮校对、必要时独立复核 | 最终QA结果 |

## 四、先明确文书角色

写作前要明确作者、主要读者、次要读者、文书功能、希望读者采取的行动、内部/客户/法院/检察机关/监管/公开版本，以及是否有强制格式。同一个法律观点写给客户和写给法院，表达方式应不同。

## 五、正式文书不能直接从原始材料生成

推荐链条是：原始材料 → 结构化事实/证据/问题 → 业务技能形成分析和方案 → 文书结构 → 正文。原始材料通常混有未核验陈述、矛盾版本、无关信息和内部不利材料，直接“喂卷宗写辩护词”会把材料顺序误当成论证结构。

## 六、事实完整性

关键事实尽量对应来源和事实状态。重点检查：已核验事实是否准确；当事人陈述是否被写成客观事实；推断是否写成确定事实；是否遗漏改变结论的反向事实；人名、日期、金额、主体名称是否一致。未知事实不能为行文顺畅而补全。

## 七、论证结构

一个完整法律论点通常包括：观点 → 支持事实/证据 → 法律规则 → 为什么适用于本案 → 对重要反方观点的回应 → 结论或行动请求。

只列法条不是论证；只讲事实也不是论证。重要争点要让读者清楚知道我方主张、理由、对方最强反驳以及该反驳是否改变结论。

## 八、文章和段落方法

重要结论尽量前置；标题表达真实观点；一个自然段承担一个完整论点；段首先说明这一段要解决什么；事实、法律、分析不反复跳跃；复杂证据、时间线、风险和方案可用表格。

特别避免 AI 问答式写法：一句话一个段落、大量无意义小标题、机械“首先其次最后”、每句话都加粗、套话和重复总结。

默认正式中文法律文书中，正文自然段首行缩进 2 个中文字符；正文内承担结构层次功能的小标题原则上也首行缩进 2 个中文字符。主标题保持居中；“诉讼请求：”“事实和理由：”“此致”等固定栏目或特定文种标签按官方样式、受理机关要求或用户模板处理，不机械套用小标题规则。

## 九、读者适配

法官/仲裁员更关心争点、事实、证据、法律和请求之间的关系；检察官/侦查机关关心阶段、证明体系和程序动作；客户/管理层关心结论、风险、选项和行动；对方文书应清晰克制、可执行，不做无依据的人身评价或威胁。

## 十、语言与术语

默认准确、克制、专业、自然。不能为了“正式”堆复杂长句，也不能为了“简洁”写成碎片短句。同一概念原则上全文使用同一称谓。

## 十一、引用和附件

检查法律是否为现行版本，案例名称/案号/机关是否准确，卷宗/证据是否保留回查定位，附件编号与正文一致，网络资料是否需要网址和日期，引用内容是否真的支持正文结论。

## 十二、Composition Capability

不同文书不是只有字体差别。辩护意见、法律意见书、尽调报告、合同审查、律师函、会见记录等应有不同的内容结构和表达要求，统一由本文件的 Document-Type Profiles 与相关 Domain Delta 维护。

## 十三、输出和版本

本模块只规定怎么交付，不自建 Office 引擎。用户要求 DOCX、原生修订、批注、清洁稿、PDF 等时，当前 Agent 调用已有文档能力实现。

如果当前环境不能真实做 Word 原生修订，必须告知并降级为差异稿 + 清洁稿，不能用红字冒充原生修订。

## 十四、仅格式调整模式

用户明确“只调格式”时，不得顺手改事实、法律结论、条款含义、金额日期或其他实体内容。发现实体错误可以提示，但不能静默修掉。

## 十五、多轮校对

至少区分语义校对和机械校对。语义校对看事实、逻辑、法律、任务是否回答、结论是否过度；机械校对看错别字、编号、标题层级、交叉引用、附件、页码、格式、文件名、版本和修订残留。重要文件最好有独立第二视角复核。

## 十六、主要产出

文书质量审查结果、正式文稿、清洁稿、差异稿/原生修订要求、批注意见、修改说明、版本记录和最终交付检查结果。




---

## 正式交付前：统一对抗性审查

---

## 核心规则

| 规则编号 | 规则 | 等级 |
| --- | --- | --- |
| LDQ-R010 | 统一样式规范 不得覆盖机关/文种更高优先级要求 | L1 |
| LDQ-R011 | 原生修订模式 能力必须真实检测；不支持时不得虚假声称，按输出契约（OutputContract）降级/阻断 | L3/工程硬约束 |
| LDQ-R012 | FORMAT_ONLY 不得改变实体内容 | L1 |

---

## 统一样式整合规则

Composition 负责确定**文书类型、读者、交付目的、是否存在官方/机关/用户模板，以及应采用哪一个 `DocumentStyleProfile`**；具体的字体、字号、页边距、行距、页码、Styles 映射等物理格式参数，由 `unit.external.document-render` 作为唯一 Canonical Owner 维护并执行，避免同一套参数在多个 Runtime 单元重复漂移。

样式优先级必须保持：

1. 特定机关/平台强制要求；
2. 特定文种官方规范或用户指定模板；
3. 现行国家语言/格式标准；
4. 爽律默认法律文书样式基线；
5. Renderer / AI 默认。

Composition 至少要向渲染层明确：标题层级、编号体系、文种固定栏目、引用/脚注要求、表格语义、签名区/附件结构、日期金额口径、是否允许修订/批注，以及任何不得被格式化动作改变的实体内容。

### 标题与段落的语义边界

- 主标题、正文结构层次小标题、固定栏目/法定标签必须先区分角色，再交给 Style/Profile 映射；
- 默认法律文书的正文自然段及正文结构层次小标题采用两中文字符首行缩进，但具体物理实现由 Document Render 使用段落 Style 完成；
- 主标题不套用正文缩进；固定栏目、诉讼文书法定/官方标签以及特定机关模板另有要求的，从其要求；
- 不得通过手敲全角空格代替确定性的段落缩进样式。

---

## Office实现边界

`Composition / Review Capability` 负责：
- 文书类型选择；
- 内容完整性；
- 事实/来源一致性；
- 论证结构；
- 行文与语言；
- 统一样式规范；
- 文书 Type Profile；
- 输出契约（OutputContract）；
- Artifact QA要求。

它**不负责实现**：
- DOCX SDK；
- OOXML 原生修订模式；
- Excel引擎；
- PPT渲染器；
- PDF生成器。

实体文件由当前 Agent / 用户已有 Office/PDF 技能实现。

---

## 先例复用门控

复用既有咨询/模板前检查：客户/对方名称、事实、法域、日期、法律版本、项目背景、立场、附件、批注/修订历史、利益冲突、先例结论是否仍正确。任何差异必须重新研究而非直接复制。

---

## 版本与修订规则

## 文档版本

推荐：

```text
v0.x  草稿
v1.0  首次正式定稿
v1.x  小幅实质更新
v2.0  重大结构/法律结论变化
```

## 每次修改记录

```text
document_id
version
parent_version
status
change_summary
content_change
legal_basis_change
rendering_change
author_or_agent
reviewer
```

## 编辑模式

### 清洁重写（CLEAN_REWRITE）
输出完整清洁稿。

### 差异稿（REDLINE）
必须可识别插入/删除/替换。

### 原生修订（TRACK_CHANGES）
只有运行能力确认支持原生 OOXML 修订时使用。

### 批注审阅（COMMENT_REVIEW）
评论必须有定位、问题、理由、建议、状态。

### 仅格式调整（FORMAT_ONLY）
任何实体变更都属于越权。

## FINAL 条件

只有：
- 阻断性QA问题为0；
- 所需附件齐全；
- 版本元数据完整；
- 必要人工复核完成；
才能标记 FINAL。


| 规则编号 | 规则 | 等级 |
| --- | --- | --- |
| LDQ-R013 | 复杂/正式文书起草前必须形成 DocumentCompositionPlan 或记录合理豁免 | L1 |
| LDQ-R014 | 内部分析结构不得机械等同最终文书结构 | L1 |
| LDQ-R015 | 论点篇幅按决定性、争议性、读者阻力和依赖关系分配，不按材料数量平均分配 | L1 |
| LDQ-R016 | 重要初稿至少完成一轮 DraftDefect → RewriteDecision 结构性重写 | L1 |
| LDQ-R017 | 存在 BLOCKING/MAJOR 成文缺陷未解决时不得 FINAL | L1 |
| LDQ-R018 | Gold Corpus 只能用于比较与测试，禁止句段复制和名家腔调固化 | HARD/L1 |

---

## 1. 强制分层

复杂或正式法律文书的默认链路：

`MatterWorkingModel / IssueTree / ArgumentMap`
→ `DocumentCompositionPlan`
→ Draft
→ `DraftDefect[]`
→ `RewriteDecision[]`
→ RevisedDraft
→ FINAL_QA

**内部分析完整 ≠ 最终正文全部写入。**

## 2. Composition Plan

起草前至少确定：
- primary_reader；
- desired_decision_or_action；
- decision_friction；
- 至少两个可行 entry angle（简单/法定固定文种可豁免并说明）；
- selected_entry_angle；
- core_arguments priority；
- argument dependency；
- depth_plan；
- excluded_internal_analysis；
- stop_conditions。

## 3. Depth

默认以四项决定展开尺度：

`decisiveness × controversy × reader_friction × dependency`

材料多、法条多、案例多本身不增加篇幅等级。

## 4. Stop Condition

当某论点已经：
1. 到达可核验终局理由；
2. 关键反理由已经处理；
3. 新增段落不再增加可理解性、可验证性、排除力或救济可接受度；

则停止展开。避免“为了显得全面”继续堆积。

## 5. Internal Analysis → External Deliverable Boundary

**内部分析完整 ≠ 内部工作语言可直接进入对外交付。** Composition 按 reader / purpose / position 将拟进入正文的信息分为：`INTERNAL_ONLY`（仅供内部判断/策略/执行）、`EXTERNALIZABLE`（有对外价值但须改写）、`EXTERNAL_CLAIM`（已有支持、确定性匹配且适合当前受众）。

需默认拦截或转换的典型内容：internal strategy；self-undermining / 自我削弱；work-process / 工作过程；adversarial/red-team / 对抗审查残留；unverified assumption / 未核实假设；AI/tool/research-process / AI/工具/检索过程；TODO/placeholder；internal instruction / 内部指令；audience-inappropriate / 受众不适配信息。

处理只允许三种：无当前交付价值的排除；有价值的提炼为可核验命题并按受众/文种/立场重写（如内部“证据较弱”可转为“现有证据尚不足以证明……”）；未核实事项不得晋升，必要时改为范围限制/不确定性披露或阻断。**真实重大风险不得以“防泄漏”为由删除**，而应转化为适当外部表达。`AdversarialReviewRecord`、Matter State、内部清单和策略记录默认不直接进入正文。

同时继续禁止把 IssueTree、Rule/Fact/Evidence/Counter 标签、“事实—法律—分析—结论”固定四段或全部要件平均展开等内部结构机械外显。外部结构按 reader + purpose + friction + argument dependency 决定；正式交付再由 Formal Delivery 运行 `External Deliverable Hygiene Check`。

## 6. Rewrite

实质性文书至少做一轮 structural rewrite。`RewriteDecision` 不等于语言润色。允许：
DELETE / REPLACE / MERGE / REORDER / FRONTLOAD / DEFER / REFRAME / BRIDGE / COMPRESS / EXPAND / REWRITE_FOR_READER / DISPOSITION_FIX。

## 7. Anti-template

不同事项不得仅替换姓名、金额、法条而保持相同：
- 开篇路线；
- 标题树；
- 论点顺序；
- 段落展开模式；
- 结尾请求。

跨文书相似性只是风险信号，不以单一数值自动判定失败；必须结合文种法定结构和案件争议判断。

## 8. Gold Corpus 边界

Gold Corpus 用于比较：
- 角度；
- 顺序；
- 详略；
- 证据嵌入；
- 反方回应；
- 成熟语气；
- 风格多样性。

禁止复制原句、固化名家腔调或从样本反推实体法律规则。

---

## 文书论证质量检查

检查：观点先行、每个观点有Fact/规则/来源、反方重要观点已回应、段落主题明确、逻辑层级不过深、术语一致、事实有证据、结论与分析匹配、无AI碎片化标签、无一句话一段的机械排版。

---

## 最终质量检查

## 实体内容
- [ ] 回答真正的问题
- [ ] 无未经支持事实
- [ ] 未将争议事实写成确定事实
- [ ] 法律依据状态明确
- [ ] 结论与上游分析一致
- [ ] 风险/限制未被删除

## 结构
- [ ] 核心观点易定位
- [ ] 标题与内容一致
- [ ] 逻辑层级不过深
- [ ] 无明显重复
- [ ] 正文自然段首行缩进符合适用规范
- [ ] 正文结构层次小标题默认首行缩进 2 个中文字符；特定模板另有要求的已按模板处理
- [ ] 主标题/固定栏目未被错误套用小标题缩进规则
- [ ] 论据支持论点

## 语言
- [ ] 术语一致
- [ ] 人名/主体一致
- [ ] 日期/金额一致
- [ ] 无明显错别字
- [ ] 标点检查
- [ ] 无无意义AI标签
- [ ] 无机械一句话一段

## 引用与附件
- [ ] 法条/案例引用正确
- [ ] 附件存在
- [ ] 交叉引用正确
- [ ] 证据编号一致
- [ ] 无先例残留他人信息

## 渲染与版本
- [ ] 输出契约（OutputContract）满足
- [ ] 原生修订模式真实或已降级
- [ ] Version完整
- [ ] 父版本完整
- [ ] 修改说明完整
- [ ] Final状态合理

---

## 前置检查

- [ ] 谁在写
- [ ] 写给谁
- [ ] 为什么写
- [ ] 文种
- [ ] 官方格式要求
- [ ] Task 范围
- [ ] 上游事实/问题/争点/Rule可用
- [ ] 输出契约（OutputContract）
- [ ] 运行环境 Capability
- [ ] Edit Mode
- [ ] 父版本（修改时）
- [ ] 统一样式规范 配置（如有）


- [ ] primary reader 与 desired decision/action 明确
- [ ] 已识别最主要 decision friction
- [ ] 已比较可行 entry angle（适用时）
- [ ] core arguments 已排序并说明依赖关系
- [ ] 已根据 Signal × Materiality 识别必要深化点，并遵循 Deepen Before Broaden；未套用统一深度档位
- [ ] 已记录“分析过但不进入正文”的内容及理由
- [ ] 未将内部 Issue/Rule/Evidence 标签机械变成目录
- [ ] 已处理决定性反理由
- [ ] 已执行 stop condition，删除无新增功能内容
- [ ] 重大初稿已形成 DraftDefect 与 RewriteDecision
- [ ] 不同案件未出现无业务理由的高同构开头/标题/结尾
- [ ] 结尾请求/建议与正文论证精确闭合

## Template / Deliverable Bundle Fidelity

当用户要求“整套材料、全部立案材料、配套文书、一整套合同文件”等，或多个交付物明显共享同一事实基础时，Composition 应把任务理解为 `DeliverableBundle`，而不是互不关联地逐文件生成。

### Bundle requirement source

拟交付物至少区分：
- `USER_REQUIRED`：用户明确要求；
- `VERIFIED_REQUIRED`：经现行规则/官方要求核验确属本次必需；
- `RECOMMENDED`：专业建议但非已核验强制；
- `OPTIONAL`；
- `UNKNOWN_NEEDS_CHECK`。

不得把通用经验清单冒充某法院/仲裁/行政机关当前必交清单。

### SharedMatterFields

主体名称、地址、日期、金额、案号、请求、合同信息等在多文书间复用时，应使用同一上游事实/来源引用，避免各文书分别生成导致漂移。共享不改变事实状态：`ALLEGED / DISPUTED / UNKNOWN` 不因被重复使用而变成 `VERIFIED`。

共享字段发生实质变化时，必须检查所有受影响正式交付物；法律或策略变化不得只做字符串批量替换。

### Template Resolution

用户指定或已有适用模板时，先解析模板的 `STRICT_STRUCTURE / GUIDED_STRUCTURE / STYLE_REFERENCE` 用法，再结合文种强制规范与当前事实生成。找不到模板要说明，不得静默改用系统默认后声称已按用户模板完成。

## Document-Type Profiles｜文种保真

文种 Profile 只补充该类文书特有的结构/质量要求，不取代 Domain、Research、Evidence 或官方模板。

- **案件分析报告**：可包含事实矩阵、争点、证据、法律研究、风险、策略；事实状态不得被行文抹平。
- **合同审查/修订**：优先尊重原合同版式和客户模板；可交修订/差异稿、批注、清洁稿、修改说明；编号、定义、交叉引用、附件保持一致。
- **辩护/代理意见**：核心观点易识别，重大事实/证据可回卷定位，语气专业克制，不把未核验陈述写成客观事实。
- **尽调报告**：明确 Scope、来源、基准日、限制；事实、风险评价、建议分层，重大事项优先。
- **证据矩阵/质证意见**：以待证命题/争点组织，保留来源定位、支持/反向意义、真实性/合法性/相关性/可靠性及冲突/缺口；不做无基础总分。
- **阅卷报告**：保留卷号/页码或等价 locator；控方证明结构、关键事实、证据、矛盾、缺口分层；不删关键不利证据。
- **律师函**：事实简洁、请求及必要期限明确；法律评价仅保留行动目的所需部分；不得使用夸张、威胁性或无依据表述；对外发送仍进入 Human/Authorization Guard。
- **法律意见书**：委托/目的、审阅材料、事实、假设、问题、法律分析、反向观点、风险、方案、建议、行动计划、范围/时间边界按需组成；Research Gap 必须传递。
- **会见记录**：时间、地点、人员、阶段、来源明确；当事人陈述保留陈述属性；事实记录与律师分析分开，不做文学性润色。
- **类案检索报告 / 法律研究备忘录 / 法规沿革 / 裁判趋势分析**：由 Research Deliverable Profile 提供研究骨架；趋势类必须披露样本/来源/时间/地域及外推限制。

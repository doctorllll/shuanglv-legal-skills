# Research｜法律研究与类案

`unit_id: unit.cap.research`

**Scope：** Authoritative legal research, current-law verification support and case comparison.

## Trigger
- User directive explicitly requests legal research, current law, authorities, cases or source verification.
- Reasoning materially depends on unsettled/time-sensitive law or authority.
- A domain method explicitly requires specialty-law research.

## Negative Trigger
- Target/quoted/attached content merely contains words such as “法律依据/案例/辩护” without a directive to research.
- Pure semantic rewrite preserving existing meaning.
- FORMAT_ONLY/render-only task.

## Essential Procedure
1. Frame the legal question and jurisdiction/time scope.
2. Prioritize authoritative source hierarchy.
3. Actually retrieve/verify when claiming current/verified law.
4. Compare cases by legally material facts and reasons, not labels.
5. Resolve authority conflict and stop at research saturation.

## Deepening Conditions
- Recent amendment or time-sensitive law.
- Conflicting authority/case lines.
- Specialty law outside baseline competence.
- Counter-research could flip the conclusion.

## Exit Sufficiency
- Sufficient authority supports each material proposition and remaining uncertainty is explicit.
- Further search is unlikely to change the conclusion materially.

## Professional Results
- research question map
- authority/source package
- currentness state
- case-comparison matrix
- conflict/counter-research notes

## Conditional Guards
- unit.guard.current-law

## External / Delegated Capability
- unit.external.input-data


## Research Method

## 一、总原则：渠道中立，角色分层

法律研究不能把“数据库、官网、公众号、网页”直接当作权威等级。搜索工具负责**发现来源**，`SourceCard / SourceProfile` 负责**评价来源**。

评价至少围绕：发布主体、内容性质、原始程度、可核验性、时间/法域、专业权威性、规范效力、事实证明力和本次用途。

同一来源可以非常权威，但仍可能不是正式法源；同一公众号也可能同时发布正式文件全文、典型案例、法官解释文章和宣传信息，必须逐项评价。

## 二、SourceRole

重要来源至少标明当前用途：

```text
FORMAL_NORM
OFFICIAL_CASE
JUDGMENT
OFFICIAL_INTERPRETATION
PRACTICE_SIGNAL
SCHOLARLY_VIEW
PROFESSIONAL_ANALYSIS
RESEARCH_LEAD
```

其中：

- `FORMAL_NORM` 负责规范依据；
- `OFFICIAL_CASE / JUDGMENT` 负责裁判适用与事实比较；
- `OFFICIAL_INTERPRETATION / PRACTICE_SIGNAL` 负责解释司法政策、辖区实践和裁判者视角；
- `SCHOLARLY_VIEW / PROFESSIONAL_ANALYSIS` 负责解释争议、方法和实务经验；
- `RESEARCH_LEAD` 只负责引导继续检索，不能被静默升级为已核验法源或案例。

## 三、权威图谱

重要法律研究不能以“搜到一条法条”作为研究终点。围绕一个重要 Issue，应按任务需要建立**权威图谱**，说明不同来源在当前问题中的层级、角色、时间状态和相互关系。

典型结构：

```text
Issue
→ 上位规范 / 基础规则
→ 核心实体或程序规则
→ 司法解释 / 配套规则
→ 官方解释与司法政策资料
→ 官方案例 / 生效裁判
→ 司法实践信号
→ 理论与专业实务分析
→ 仍待追溯的研究线索
```

权威图谱不意味着所有来源同等权威。每个来源都应说明“能支持什么”和“不能替代什么”。

## 四、权威图谱至少记录

- 对应 Issue；
- 来源身份和原始出处；
- 发布主体/作者及渠道；
- `SourceRole`；
- 适用法域；
- 时间效力或核验日期；
- 专业权威性与规范效力分别如何；
- 来源在当前问题中的具体作用；
- 支持/限制的具体命题；
- 精确定位；
- 特别规则、冲突、例外或适用限制；
- 尚未补齐的上位或原始来源。

## 五、Research Ladder｜递进检索路径

类案和疑难法律研究原则上不依赖一次关键词搜索，而按问题需要逐层推进：

```text
L1 直接命中
法条 / 规范名称 / 罪名案由 / 核心争点 / 已知案号
↓
L2 要件与事实拆解
行为 / 主体 / 主观要素 / 结果 / 金额 / 证据 / 程序节点
↓
L3 类案扩展
同义表达 / 相邻案由 / 相似事实 / 边界案例 / 反向结果
↓
L4 引文与关系滚雪球
案例引用 / 法条关联 / 文章脚注 / 被引用材料 / 官方专题
↓
L5 解释与实践补强
官方解释 / 审判白皮书 / 实务总结 / 学术与专业分析
```

并非每项研究都要机械跑完五层。进入下一层的触发条件是：当前层仍不足以解决 Issue、出现重要分歧或需要解释决定性事实差异。

## 六、类案矩阵

案例检索不是“找到几个相似案件”。需要利用案例支持重要判断时，按任务需要形成 `CaseMatrix`，至少比较：

- 案例基本信息与来源；
- 决定性事实；
- 核心争点；
- 裁判结论和关键理由；
- 与本案相似点；
- 与本案区别点；
- 对当前命题的使用方式；
- 对我方不利的部分；
- 原文定位。

案例用途至少可区分：`SUPPORT / COUNTER / BOUNDARY / DISTINGUISH / EXCEPTION / PROCEDURE / CONSEQUENCE`。

## 七、案例比较禁止模式

- 只因案由或罪名相同就视为类案；
- 只比较裁判结论，不比较决定性事实；
- 只找支持我方的案例；
- 用普通个案替代明确的现行规范；
- 把检索不到反向案例表述成不存在反向案例；
- 未阅读裁判理由就根据摘要推断案件规则；
- 因来源在公众号/网页发布就自动降级；
- 因来源来自商业数据库就自动视为高权威。

## 八、Search Saturation｜研究充分性

研究停止依据是**信息覆盖和信息增益**，不是案例数量。

达到 `SATURATED` 的候选条件包括：

- 核心现行法及时间问题已核验；
- 关键定义、特别规则、例外已检查；
- 至少存在相互独立的检索路径；
- 与当前问题有关的支持、反向、边界案例已合理覆盖；
- 重要官方解释/司法实践信号在其确有意义时已检查；
- 关键理论或专业争议在法规范/案例不足以回答时已检查；
- 新一轮检索的信息增益显著下降；
- 仍存缺口已记录，且不会被伪装为无保留确定结论。

若现行法、时间适用、重要反向路径或真实性核验仍可能改变结论，应标记 `INCOMPLETE / BLOCKED / HUMAN_REVIEW_REQUIRED`。

## 九、Research Deliverable Profile｜研究交付物

研究结果与正式交付物不是同一个对象。相同研究底稿可以根据用途形成不同交付：

- `CASE_RESEARCH_REPORT`：类案检索报告；
- `LEGAL_RESEARCH_MEMO`：法律研究备忘录；
- `LEGAL_OPINION_INPUT`：供法律意见书使用的研究包；
- `NORM_HISTORY_REPORT`：法规沿革报告；
- `JUDICIAL_TREND_ANALYSIS`：裁判趋势分析；
- `RESEARCH_PACKAGE_ONLY`：只交付结构化研究包，不写正式报告。

系统可以提供默认结构，但**用户/事项已有模板与长期习惯优先保留**，遵循 `Hard Guardrails > Matter Override > User Personalization > Version Defaults`。研究方法由 Core 约束，最终版式和表达习惯优先服从合法用户模板。

## 十、研究回写

权威图谱、SourceProfile、Research Ladder 或 CaseMatrix 发现规则层级、司法实践、关键区别事实、反向案例或解释材料足以改变原 Issue / Argument / Finding 时，必须按 `references/matter/result-invalidation.md` 的依赖失效/回写规则更新受影响的上游对象。

---

## 一、这个技能解决什么问题

这个技能不是“帮我搜几个网页”，而是把一个法律问题推进成一份**可复核、可追溯、知道边界在哪里，并且知道资料各自能证明什么的研究结果**。

它要解决五件事：真正的问题是什么；到哪里发现资料；找到的资料在当前问题中是什么角色和权重；研究到什么时候算够；最终应该以何种研究交付物服务律师工作。

## 二、主流程

```text
明确任务目标、法域、时间与交付用途
→ 拆解 Issue 与决定性事实
→ 定义需要的信息角色 SourceRole
→ Source Discovery：多渠道发现候选来源
→ Source Evaluation：逐项评价主体、内容、原始性、效力与用途
→ Research Ladder：递进式多路径检索
→ 核验现行法律规范及时间效力
→ 提取案例规则并比较决定性事实
→ 补充官方解释、司法实践信号、理论/专业观点（按需）
→ 主动检索反向、例外和边界
→ 融合不同 SourceRole，处理冲突
→ Search Saturation：判断是否达到当前任务所需充分性
→ Research Deliverable Profile：按用途组织交付
→ 需要时回写业务分析
```

研究不是“先把法找完，再回头看事实”。正确方式是**事实—规范—案例—实践来回迭代**：现有事实提示检索方向，检索结果又提示还缺哪些事实或解释，新增事实再反过来改变 Issue 和检索路径。

## 三、执行步骤速查表

| 步骤 | 要做什么 | 主要方法 | 阶段产物 |
|---|---|---|---|
| 1. 任务与交付界定 | 明确为什么研究、给谁看、最终用在哪里 | 法域/时间/读者/用途 | ResearchRequest / DeliverableProfile |
| 2. 问题界定 | 把宽泛问题拆成可检索问题 | IssueTree、决定性事实、未知事实 | 研究问题清单 |
| 3. 信息角色设计 | 先判断当前问题需要何种资料 | SourceRole | 信源需求清单 |
| 4. 来源发现 | 通过数据库、官网、公众号、网页、知识库、引文追踪等发现候选材料 | Source Discovery | 候选来源池 |
| 5. 来源评价 | 不按渠道贴标签，评价主体、内容、原始性、效力、用途 | SourceProfile / SourceCard | 已评价来源 |
| 6. 递进检索 | 从直接命中推进到事实/类案/解释/理论 | Research Ladder | ResearchTrace |
| 7. 规范核验 | 确认现行法及时间状态 | 版本、效力、特别/例外规则 | Norm Package |
| 8. 类案研究 | 判断真正可比之处 | 决定性事实、理由、区分 | CaseCard / CaseMatrix |
| 9. 实践与解释补强 | 规则/案例不足时补充官方解释、实践信号、理论和专业分析 | SourceRole-aware synthesis | 解释/实践资料包 |
| 10. 对抗研究 | 主动找不支持当前结论的材料 | COUNTER / BOUNDARY / EXCEPTION | 反向路径 |
| 11. 充分性判断 | 判断新检索是否还有实质信息增益 | Search Saturation | SaturationAssessment |
| 12. 正式交付 | 根据用途选择不同报告结构，并尊重用户模板 | Research Deliverable Profile + Template Asset | 报告/备忘录/研究包 |
| 13. 业务回写 | 研究改变原分析时回写 | ResearchResult → WriteBack | 更新后的业务判断 |

## 四、核心方法

### 1. 问题拆解

不要把整段案情直接扔进搜索框。每个研究问题至少明确：法域、时间、关键事实、希望得到的答案类型、依赖问题、未知事实。复杂问题拆成能够分别检索和验证的子问题。

### 2. Source Discovery ≠ Source Evaluation

数据库、网页搜索、微信公众号搜索、知识库只是发现候选材料的渠道。发现之后必须评价：**谁发布、是什么内容、是否原始、是否可核验、在本案中承担何种 SourceRole、权威性/规范效力/事实证明力分别是什么。**

禁止把“官网”自动等同于正式法源，也禁止把“公众号”自动等同于二手低权威材料。

### 3. SourceRole 驱动研究

研究不同问题需要不同信息：

- 规则是什么 → `FORMAL_NORM`；
- 法院如何适用 → `OFFICIAL_CASE / JUDGMENT`；
- 司法机关如何理解或当前实践如何运行 → `OFFICIAL_INTERPRETATION / PRACTICE_SIGNAL`；
- 为什么存在不同解释 → `SCHOLARLY_VIEW / PROFESSIONAL_ANALYSIS`；
- 出处暂时不明 → `RESEARCH_LEAD`。

同一材料可以承担多个功能，但不得越权使用。

### 4. 规范包核验

找到一条法条不等于研究完成。重要问题应尽量核验：当前有效文本、生效时间、修改废止情况、过渡规则、相关司法解释或实施规则、上下位规范关系。历史行为还要核对行为发生时的法律版本。

**Jurisdiction Stack Closure：** 当事项具有明确地域且地方规则可能影响程序路径或结论时，在标记 `SATURATED` 前应核到与争点有关的国家→省级→当地规则，特别检查受理条件、管辖、期限、程序衔接、报告/告知等地方特别规定；地方规则对一般规则有合法补充或收窄时，应明确并列说明，不得只核全国规则即结束。

### 5. Research Ladder

不要在一个数据库里反复换关键词。根据研究缺口逐层推进：直接命中 → 要件/事实拆解 → 类案扩展 → 引文/关系滚雪球 → 官方解释/司法实践/理论与专业分析。每进入下一层都要有原因，不机械跑满所有层级。

### 6. 公众号与网页的正确使用

高质量公众号和网页资料可以是正式研究材料。例如法院、检察院等官方主体发布的原创典型案例、白皮书、审判思路、司法解释解读，本身可能具有很高的司法实践或官方解释价值。专业机构和作者身份明确、论据透明的文章也可承担理论/实务分析角色。

但应区分“具有专业权威性”和“具有正式法源效力”。二次转载、出处不明、截屏式传播材料优先追溯原文。

### 7. 类案比较

类案不是关键词越像越好。比较法律争点、决定性事实、适用法律版本、程序阶段、证据结构、裁判理由和差异点。每个案例至少说明：它真正支持什么命题；为什么可能不适用于本案。

### 8. 对抗性研究

重要问题必须主动找反向案例、例外规则、不同解释、对方可能主张的路径，以及会使当前结论失效的事实条件。研究结果应能够承受反驳，而不是只搜支持材料。

若用户当前 Directive **明确只要求寻找支持性材料**，可以按其范围完成，不应偷偷扩大成完整对抗研究；但交付必须标明研究范围和限制，不能把单向支持性检索标记为 `SATURATED`，也不能据此包装成无保留正式法律结论。

### 9. “没搜到”不等于“不存在”

公开数据库无结果，只能说明当前检索路径没有找到。记录检索范围、关键词、无法访问来源和后续建议，不得直接写成“没有相关规定/案例”。

### 10. Search Saturation

研究不是无限继续，也不能“搜三篇就结束”。可以停止的候选条件通常包括：核心现行法已核验；关键案例路径已覆盖；支持/反向/边界/例外已有合理检查；需要时已经检查官方解释/司法实践和理论争议；新一轮检索的信息增益明显下降；剩余缺口不会被掩盖。

仍有可能改变结论的重要缺口时，标记 `INCOMPLETE / BLOCKED / HUMAN_REVIEW_REQUIRED`。

### 11. Research Deliverable Profile

同一研究底稿可以输出成不同交付物：

- 类案检索报告；
- 法律研究备忘录；
- 法律意见书的研究输入包；
- 法规沿革报告；
- 裁判趋势分析；
- 仅结构化研究包。

系统只定义应完成的专业任务，不垄断最终外观。**用户/事项已有模板和长期写作习惯属于 Personalization / Template Asset Layer，优先于系统默认格式。**

## 五、关键人工复核点

以下情况应提示律师判断：权威来源实质冲突；法律版本无法确定；关键事实未知导致多条法律路径同时成立；类案高度依赖细微事实差异；不同法院/地区实践明显分化；用户要求的确定程度超过现有资料能够支持的范围。

## 六、主要产出

- ResearchRequest / 问题清单；
- SourceProfile / SourceCard；
- ResearchTrace；
- 现行法律规范及时间效力信息；
- AuthorityMap；
- CaseCard / CaseMatrix；
- 官方解释、司法实践信号、理论/专业观点及其用途；
- 反向观点、例外和边界；
- ResearchSaturationAssessment；
- ResearchResult；
- ResearchDeliverableProfile；
- 研究缺口与必要回写。

研究可以独立形成报告，也可以作为刑事、民商、合同、法律顾问、尽调等业务技能的研究输入。

## 七、与其他技能怎么配合

业务技能需要现行法、类案、司法实践或解释材料时调用本模块；正式研究报告还要遵循“Composition / Review Capability”。若用户已有类案报告或法律备忘录模板，按 Template Asset Layer 调用，不因版本升级覆盖。

## 八、正式交付前统一对抗性审查

重要研究形成初步结论后，应主动检查反向来源、来源越权使用、渠道偏见、重要实践信号遗漏、检索未饱和和模板覆盖冲突。发现问题必须回写正文或研究状态，而不是在末尾附一句“已复核”。

## 九、外接数据库与公开来源

法律研究所需数据由当前运行环境提供。爽律skill 不绑定某一家数据库或某一种公开渠道；有专业数据库时可以利用其结构化检索优势，有官方网页/公众号等高质量原始来源时也可直接评价并使用。不能真实访问的来源不得伪造访问结果。

---

## A. 渠道中立与信源评价

### LR-R011｜渠道不得直接决定权威等级（L1）

数据库、官网、公众号、网页、知识库仅表示发现/承载渠道。必须根据发布主体、内容性质、原始性、可核验性、时间/法域和当前用途评价来源。

### LR-R012｜Source Discovery 与 Source Evaluation 分离（L1）

“搜到”不等于“可用”。正式纳入研究的候选来源应形成 SourceCard / SourceProfile，说明 `SourceRole`、权威性、规范效力、事实证明力和允许用途。

当复杂/深度任务加载 `unit.interop.execution-control` 时，Research 的 `SATURATED / INCOMPLETE / BLOCKED` 状态及其完成依据必须回写执行账本；只有搜索命中、打开数据库页面或获得候选案例，均不得把 Research 标记为 COMPLETE。

### LR-R013｜权威性、效力与证明力不得混写（HARD/L1）

高质量官方解释可以很权威但不是正式法律规范；专业文章可以很有解释价值但不能自动证明本案事实；正式规范能证明规则但不能替代本案证据。

### LR-R014｜公众号与网页逐项评价（L1）

官方机关、专业机构或高质量专业作者在公众号/网页发布的原创资料，经核验后可以直接作为正式研究资料。二次转载、出处不明、截屏材料默认作为 `RESEARCH_LEAD`，优先追溯原文。

## B. SourceRole

推荐角色：

- `FORMAL_NORM`
- `OFFICIAL_CASE`
- `JUDGMENT`
- `OFFICIAL_INTERPRETATION`
- `PRACTICE_SIGNAL`
- `SCHOLARLY_VIEW`
- `PROFESSIONAL_ANALYSIS`
- `RESEARCH_LEAD`

角色描述“在当前问题中做什么”，不等于固定权威排名。

## C. 法律规范核验

必须检查：原文来源、发布机关、文号、发布/生效时间、当前状态、行为发生时状态、修订/废止、过渡、位阶、特别法、地域/主体/事项、配套司法解释/实施规范。

现行法不得仅凭模型记忆、标题、摘要或二手转述标记为已核验。

## D. 案例

分别记录：发布/裁判机关、是否官方案例、是否生效、审级、法律问题、决定性事实、当时法律背景、裁判规则/理由、区分点、使用目的、原始来源。

案例服务法律论证，不证明本案事实。

## E. 专业观点、官方解释与实践信号

至少检查：作者/发布机关、机构、时间、专业背景、原始发布、论据、引用法源、适用范围、潜在利益相关。

官方解释/实践信号要特别记录：其是否具有正式规范效力、适用辖区、发布时间以及能否反映当前司法实践。

## F. 类案比较与区分

关键比较维度：

```text
same legal issue
material facts
dispute focus
applicable rule
normative background
procedure / evidence
holding / rule
reasoning
authority
time / jurisdiction
intended use
```

禁止单一总分、禁止只看关键词或结论。

对不利类案依次检查：决定性事实、争议问题、法律规则/版本、程序证据、案例权威与推理差异。

## G. Research Ladder｜检索式工程

每个重要 Issue 可从以下路径按需组合：

```text
L1 Direct: 概念 / 法条 / 规范 / 已知案号
L2 Elements: 要件 / 主体 / 行为 / 结果 / 证据 / 程序
L3 Analogical: 类案 / 相邻案由 / 边界 / 反向
L4 Snowball: 引文 / 脚注 / 案例引用 / 官方专题
L5 Interpretation: 官方解释 / 实践信号 / 理论 / 专业实务
```

关键 Issue 原则上至少两条独立检索路径。数据库语法按适配器记录，不假定跨平台相同。

## H. Search Saturation｜研究充分性

### SATURATED 候选条件

- [ ] 核心现行法及必要历史版本已核验；
- [ ] 定义、特别规则、例外已检查；
- [ ] 至少2条独立检索路径（简单问题可说明豁免）；
- [ ] 支持/反向/边界/例外已按任务需要检查；
- [ ] 关键案例来源已检查；
- [ ] 对实际裁判理解有意义时，已检查必要的官方解释/实践信号；
- [ ] 法规与案例仍不足时，已检查必要理论/专业分析；
- [ ] 重要分歧已显式记录；
- [ ] 新一轮扩检未产生会改变规则/结论的实质新信息；
- [ ] 剩余缺口与当前用途相容。

### 强制 INCOMPLETE

- 现行法未核验且任务要求现行法；
- 时间适用未核验且可能改变结论；
- 关键来源真实性无法确认；
- 只有单向支持性检索且任务要求完整研究；
- 重要分歧/反向路径尚未检查；
- 仍有高概率改变结论的关键来源缺口。

**LR-R010：研究停止以覆盖与信息增益为准，不得以检索数量替代覆盖判断。**

## I. Research Deliverable Profile

研究交付类型至少区分：

- `CASE_RESEARCH_REPORT`
- `LEGAL_RESEARCH_MEMO`
- `LEGAL_OPINION_INPUT`
- `NORM_HISTORY_REPORT`
- `JUDICIAL_TREND_ANALYSIS`
- `RESEARCH_PACKAGE_ONLY`

系统提供默认专业结构；若存在用户/事项模板，按 `Hard Guardrails > Matter Override > User Personalization > Version Defaults` 解析。不得以新版默认模板静默覆盖用户模板。

## J. 基础硬规则

| 规则编号 | 规则 | 等级 |
| --- | --- | --- |
| LR-R009 | 未能核验的来源必须显式降级，不得补全 | HARD/L1 |
| LR-R010 | 研究停止以覆盖与信息增益为准，不得以检索数量替代 | L3 |
| LR-R011 | 不得以发布渠道直接替代来源评价 | L1 |
| LR-R012 | 来源发现与来源评价必须分开 | L1 |
| LR-R013 | 权威性、规范效力、事实证明力必须区分 | HARD/L1 |
| LR-R014 | 公众号/网页来源逐项评价，不得一棒子降级 | L1 |
| LR-R015 | 正式研究交付前应确定 ResearchDeliverableProfile，并尊重用户模板 | L2 |

---

## 前置检查

- [ ] 已创建 Issue / ResearchRequest
- [ ] 法域明确
- [ ] 关键时间明确或标记 UNKNOWN
- [ ] 研究目标与最终用途明确
- [ ] 已识别需要的 SourceRole，而非只列“去哪个平台搜”
- [ ] 已读取 RuntimeCapabilityProfile
- [ ] 已识别需要读取的案件/项目附件
- [ ] 未把未核验事实写进检索前提
- [ ] 若用户有研究报告/备忘录模板，已进入 Template Resolution

## Source Discovery / Evaluation

- [ ] 没有把搜索排名、数据库命中或公众号渠道直接当作权威等级
- [ ] 关键来源已记录发布主体、内容性质、原始性、时间/法域
- [ ] 关键来源已标记 SourceRole
- [ ] 权威性、规范效力、事实证明力已经分别判断
- [ ] 官方公众号/网页原创资料没有因渠道被机械降级
- [ ] 二次转载、出处不明或截屏材料已追溯原文，或保持 RESEARCH_LEAD 状态

## 规范与案例

- [ ] 核心现行法当前有效状态已核验
- [ ] 时间适用已检查
- [ ] 案例有决定性事实和区分点
- [ ] 案例原始来源/发布状态尽可能核验
- [ ] 观点、官方解释、实践信号与正式法源分层
- [ ] 支持 / 反向 / 边界 / 例外按任务需要检查

## Research Ladder / Saturation

- [ ] ResearchTrace 足以复现主要路径
- [ ] 关键 Issue 使用了独立检索路径，或记录合理豁免
- [ ] 新一轮检索的信息增益已评估
- [ ] 关键来源缺口已明示
- [ ] 没有把“没搜到”写成“不存在”
- [ ] SATURATED / INCOMPLETE / BLOCKED / HUMAN_REVIEW_REQUIRED 状态合理
- [ ] 若标记 SATURATED，已形成 ResearchSaturationAssessment 或等价记录

## 正式研究交付

- [ ] 已确定 ResearchDeliverableProfile
- [ ] 类案检索报告与普通法律研究备忘录没有混为同一种固定模板
- [ ] 样本范围、检索方法和限制在需要时已披露
- [ ] 用户/事项已有模板和长期习惯得到保留
- [ ] 新版系统默认未静默覆盖用户模板
- [ ] 重要结论可回到 Source / Rule / Case / Argument / Finding
- [ ] 需要人工判断之处已升级

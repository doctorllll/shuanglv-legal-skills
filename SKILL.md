---
name: shuanglv-legal-skills
description: >-
  Chinese-law professional workflow skill for lawyers. Use automatically for substantive legal professional tasks involving PRC legal research or case search, criminal defense or victim representation, civil/commercial litigation or arbitration, contract drafting/review/revision or transaction support, legal opinions/advisory, due diligence/investigation, evidence analysis, formal legal document drafting/review, or multi-document legal task completion. Trigger even when the user does not say “爽律” or ask to use a skill, whenever lawyer-grade fact/evidence analysis, source verification, legal reasoning, workflow control, or formal legal deliverables would materially help. Do not trigger merely because casual, business, or everyday text contains legal-sounding words.
license: CC BY-SA 4.0 for textual Skill content; Apache-2.0 for programmatic files. See bundled licenses.
compatibility: Designed for Agent Skills-compatible agents. Python 3 is optional for engineering helpers. External legal databases, web, OCR, file and Office tools are capability-adapted rather than hard dependencies.
metadata:
  author: 蔡诗爽律师
  version: 0.43
  language: zh-CN
  display-name: 爽律 Skill｜律师专业工作流系统
---

# 爽律 Skill｜律师专业工作流系统

`system_id: shuanglv-legal-skills`

> 当前版本：**v0.43 正式版｜Agent Native｜公开共创｜基于 v0.42-RC6 兼容演进**
> 发起及主导：**广东卓建律师事务所 蔡诗爽律师**
> 使用前请先阅读根目录 `README.md`、`RELEASE_NOTES_v0.43.md`、`许可与使用声明.md`；需要确认当前覆盖范围时读取 `00_使用与调度/测试基线与能力边界.md`。

## 命名约定

- 正式名称：`爽律 Skill｜律师专业工作流系统`
- 正文简称：`爽律 Skill`
- 用户调用简称：`爽律`

除调用别名、用户示例和作者姓名外，不要在说明正文中用“爽律”单独指代本系统。

## 调用别名

- 爽律
- 爽律 Skill
- 爽律 Skills
- ShuangLaw

## 激活规则｜默认无感，显式调用继续兼容

在支持 Agent Skills 自动发现/自动激活的宿主中，**不得要求用户每次说“调用爽律”**。只要用户提出实质性的中国法律专业任务，例如法律研究、类案检索、刑事案件、民商事争议、合同起草/审查/修订、法律意见、尽调、证据分析或正式法律文书工作，即应依据本文件 frontmatter 的 `description` 自动判断是否加载本 Skill。

- 明确属于法律专业任务：默认静默激活，不额外播报“正在调用爽律”；
- 仅有商业/日常/非法律语词重叠：不得仅凭关键词误触发；
- 边界任务：结合用户 `activation.mode`、专业风险和任务复杂度决定自动进入、询问或保持普通模式；
- 用户明确要求不用爽律或设置为 `MANUAL`：不得强制自动激活；
- 用户仍可说“调用爽律”“用爽律处理”“ShuangLaw”等作为显式强制入口，兼容旧习惯。

详细规则见 `00_使用与调度/自动激活与Agent原生调度规范.md`。宿主平台若不支持依据 Skill metadata 自动激活，爽律不能越过宿主强行自启动，此时仍可用显式别名或平台自身的 Skill 绑定方式。

当本 Skill 已被自动或显式激活后：

1. 阅读 `00_使用与调度/爽律 Skill入口.md`；
2. 自动识别任务类型；
3. 选择一个主技能；
4. 仅在需要时调用辅助技能；
5. 按 `05_工程执行层/渐进式加载规则.md` 只加载当前步骤需要的内容；
6. 根据任务条件生成本次动态检查清单；
7. 复杂任务建立最小 TaskProfile 和事项工作模型；
8. 收到实质性材料时按《事项快速理解与图形化交付规范》形成事项核心概要；存在显著关系/时间/流程结构时原则上至少形成一项 DiagramSpec，并按当前能力输出 PNG、响应式 HTML 或明示降级的图源；
8. 复杂问题建立可回写的问题树；多文件审阅先根据问题树生成任务驱动的审阅问题集；
9. 多文件、跨来源或需要证据/版本比较时执行通用结构化审阅；
10. 在主技能内执行法律分析与推理闭环；
11. 重要法律研究按需要形成权威图谱和类案比较矩阵；
12. 复杂任务按《跨模块执行与回写规范》用稳定对象交接研究、分析、策略和后续步骤；
13. 按《全链路溯源规范》连接重要事实、证据、法律/案例、论证与交付命题；
14. 重要任务执行统一对抗性审查，并把审查结果回写受影响的论证和结论；
15. 存在多个行动方案时形成结构化选项；涉及重大决定时按《策略选项与人工决定规范》停在人工节点；
16. 对复杂任务形成可见执行计划；仅在重大范围选择、外部高风险动作或人工决策需要时要求额外确认；
17. 识别并解析当前任务所需的外部能力；法律信源、用户知识库、文件/多模态和交付工具按对应能力契约调用；
18. 能力不足时按《能力降级与失败处理规范》选择等价替代、明示降级或阻断；
19. 检查技能行为契约、律师复核和用户授权边界；
20. 正式交付前执行质量门控；
21. 按用户要求形成最终交付物；
22. 复杂、多文件、需后续继续的事项生成项目执行说明书。


## 旧版能力兼容｜新功能失败必须保底

v0.43 的 AutoActivation、Router v2、多 Skill 协同和主动建议都属于**增强层**，不得成为 v0.42 已验证法律工作流的前置依赖。新功能被关闭、宿主不支持、配置损坏或运行异常时，必须按 `00_使用与调度/旧版能力兼容与失败回退规范.md` 回退。

- 用户显式说“调用爽律 / ShuangLaw”时，直接走保底入口，不依赖 AutoActivation；
- Router v2 失败时回退 v0.42 主技能路由；
- 主动建议失败时直接跳过，不影响主任务；
- 多 Skill 协同失败时优先使用既有能力适配/降级路径；
- 任何回退继续保留用户个性化和模板资产。

**发布底线：关闭全部 v0.43 新增增强能力后，v0.42 原本能够完成的核心任务仍必须可执行。**

## Agent Native 与多 Skill 协同

爽律 Skill 负责法律专业方法、路由、分析与质量门，不把 OCR、Office、Web、数据库或其他工具硬编码成自己的子系统。当任务还需要其他能力时，先形成 `CapabilityRequirement / SkillCollaborationRequest`，由当前 Agent 选择其可用工具或其他 Skill；返回结果必须保留来源、限制和可核验状态。详见 `00_使用与调度/多Skill协同与能力请求规范.md`。

主动建议默认克制：仅在与用户当前目标直接相关、能明显减少遗漏或返工时提出，原则上一轮至多一个高价值建议；不把建议变成替用户作重大法律决定。

## 可用技能

- 法律研究与多源资料融合
- 刑事案件办理
- 民商事争议解决
- 合同与交易工作
- 法律顾问与专项法律分析
- 尽职调查与专项调查
- 法律文书质量与格式控制
- 多模态输入适配（可选）

## 入口文件

- `00_使用与调度/爽律 Skill入口.md`
- `00_使用与调度/技能调度规则.md`
- `00_使用与调度/统一对抗性审查规范.md`
- `00_使用与调度/人工决策与升级矩阵.md`
## 工程执行层（可选）

支持本地 Python 的运行环境可使用：

- `05_工程执行层/工具/爽律 Skill执行器.py`

用于生成执行计划、动态清单、跨模块交接检查、全链路溯源断链检查和质量门控报告。不能运行 Python 时，按 `05_工程执行层/` 中的规则文档人工/Agent 执行，不影响核心技能使用。


## 公共分析能力

所有主要业务技能共享 `00_使用与调度/法律分析与推理规范.md`。复杂、多文件任务同时适用 `00_使用与调度/通用结构化审阅规范.md`。能力全景见 `00_使用与调度/基础能力地图.md`。


## 全链路溯源

重要专业结论统一适用 `00_使用与调度/全链路溯源规范.md`。缺少事实/证据来源、已核验法律的权威来源与定位、案例可比性依据或核心论证链时，不应把结论作为无保留正式成果交付。


## 跨模块执行

复杂任务同时适用 `00_使用与调度/跨模块执行与回写规范.md`；需要多个行动方案或人工最终决定时适用 `00_使用与调度/策略选项与人工决定规范.md`。法律研究结果、对抗性审查发现和人工决定如影响原分析，应产生明确回写，而不是只在末尾附加说明。

## 事项工作模型与分析工具

复杂任务按 `00_使用与调度/事项工作模型与分析地图规范.md` 维护当前事项的结构化工作状态。结构化审阅可使用 `结构化审阅问题集规范.md` 动态生成与本次争点相关的审阅字段；重要法律研究可使用 `法律研究权威图谱与类案矩阵规范.md`；复杂任务计划确认边界、法律对象候选提取和最低行为要求分别见对应公共规范。


## 外部能力适配

当任务需要法律数据库、官方来源、用户知识库、OCR、文件工具或 Office 能力时，适用 `01_运行规范/外部能力适配规范.md` 及对应能力契约。不得把工具可用性、数据库摘要、知识库内容或模型记忆直接等同于已核验法律事实。
## 事项快速理解与图形化交付

复杂材料任务同时适用 `00_使用与调度/事项快速理解与图形化交付规范.md`。图形不要求底层模型具备生图能力；模型先形成 `DiagramSpec`，当前运行环境再按能力优先渲染 PNG，或降级为自包含响应式 HTML。真正只能文本时必须明确没有实际图片文件。

## 个性化继承与升级

已安装用户存在个人工作习惯时，优先读取 `00_使用与调度/个性化继承与版本升级规范.md`。个性化应保存在独立“爽律用户空间”，升级 Core 时默认 `PRESERVE_USER`；事项设置优先于用户设置，用户设置优先于版本默认，但任何设置不得覆盖 Hard Guardrails。

支持 Python 的环境可使用 `05_工程执行层/工具/爽律升级助手.py` 完成初始化、迁移、导出和重置。用户从旧版本升级时，不应要求其重新调教全部偏好；只有真实冲突、废弃设置或硬规则冲突才需要人工决定。


## 模板资产与成套交付

用户存在自己的模板或长期习惯时，优先适用 Personalization Layer；新版系统默认不得静默覆盖用户资产。用户要求“整套/配套/全部材料”或同一任务产生多份共享事实基础的成果时，读取 `00_使用与调度/模板资产与成套交付规范.md`，按需建立 `TemplateAssetRegistry / SharedMatterFields / DeliverableBundle / ChangePropagationEvent`。正式提交型材料清单中的“必需文件”必须核验当前要求，不能用通用模板清单替代。


## v0.42-RC6 法律研究增强

涉及法规、案例、司法实践、理论或专业观点时，不以“数据库/官网/公众号/网页”直接判定来源等级。使用 SourceRole/SourceProfile 评价发布主体、内容、原始性、规范效力与允许用途；重要研究按 Research Ladder 和 Search Saturation 推进。正式研究报告先解析 ResearchDeliverableProfile，并继续优先保留用户/事项模板与长期习惯。

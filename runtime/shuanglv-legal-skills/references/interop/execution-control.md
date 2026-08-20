# Interop｜Execution Control & Visible Verification

## Scope

本单元负责把“已经读取爽律skill规则”转换为**可持续约束任务执行的状态协议**。它不重新拥有 Facts / Evidence / Research / Reasoning / Review / Matter 的专业真值，也不保存模型私有推理链。

### Trigger

在下列情形加载：

- 爽律skill进入实质性专业执行，且不属于极小型单点低风险操作；
- 同一任务实际触发多个主要专业模块，并且它们存在前后依赖；
- 深度法律研究、完整阅卷/证据梳理、重大正式交付；
- 长任务、多文件、多来源或需要阶段续跑；
- 用户明确要求显示执行流程、进度、完成依据或核验状态。

简单单点改写、低风险格式调整、单一事实问答等不加载完整账本，只做与目标相称的最小完成检查；不得为“流程完整”展示无关模块或制造重型台账。

## 1. TaskExecutionContract｜任务执行契约

任务进入实质执行后，建立任务级 `TaskExecutionContract`，至少记录：

- `task_goal`：用户原始目标；
- `role_and_stance`：角色/立场（如适用）；
- `material_scope`：应处理的材料范围；
- `target_deliverables`：目标交付物；
- `user_constraints`：用户明确限制；
- `triggered_modules`：本任务真正触发的主要模块；
- `required_outputs`：各模块退出前必须产生的专业结果；
- `dependencies`：模块依赖；
- `final_conditions`：可以进入正式交付的条件；
- `human_intervention_points`：真正需要人工决定/授权/补料的节点。

不得在执行过程中静默缩小用户原始目标。需要降级时必须记录原因、影响和未完成范围。

## 2. ModuleExecutionLedger｜模块执行账本

每个被触发主要模块只允许使用以下状态：

- `NOT_STARTED`：未开始；
- `IN_PROGRESS`：正在执行；
- `PARTIAL`：已有产物但未达到退出条件；
- `COMPLETE`：达到退出条件且存在可核验完成依据；
- `BLOCKED`：材料、权限、授权、工具或其他真实条件阻断；
- `INVALIDATED`：此前结果因上游实质变化失效；
- `NOT_APPLICABLE`：经路由判断本任务不适用。

`COMPLETE` 不能由一句“已完成”自我声明获得。每条 COMPLETE 至少关联 `proof_of_work`、关键产物引用和未关闭缺口状态。

## 3. Proof of Work｜完成依据

完成依据必须与模块类型相匹配，不以统一百分比代替专业判断。例如：

- **材料/阅卷**：应处理材料总数、实际打开/阅读/核验范围、部分审阅项、OCR/原件回查状态；
- **事实**：FactRecord/时间线/主体关系/未知项及来源定位；
- **证据**：待证命题、支持/反向证据、证明问题与缺口；
- **法律研究**：Issue、现行法/来源核验、研究路径、支持/反向/边界/例外覆盖、未核实项；
- **类案研究**：检索路径、候选、全文阅读、纳入矩阵、支持/反向/区分用途；
- **策略**：主攻/支持/备选/兜底、证据依赖、风险、程序动作和切换条件；
- **对抗性审查**：发现的实质缺陷、处理结论、回写位置或仍开放问题；
- **成文/交付**：研究/审查状态、重要命题可追溯性、实体文件状态与正式交付门结果。

“找到文件”“搜索有命中”“HTML 已经生成”“代码已经写出”都只能证明局部物理动作，不能自动证明专业模块 COMPLETE。

## 4. Dependency & Targeted Invalidation｜依赖与定向失效

任务执行依赖至少遵循：

```text
材料/来源
→ 事实
→ 证据与争点
→ 法律/类案研究
→ 论证
→ 策略
→ 成文
→ 审查
→ 正式交付
```

上游来源、材料、事实、法律、案例、关键假设发生实质变化时，调用 `references/matter/result-invalidation.md` 识别受影响下游，并把相应 Ledger 状态改为 `INVALIDATED` 或重新进入审查。不得通过在最终报告末尾追加一段文字绕过受影响正文的重新计算。

## 5. Deliverable Lifecycle｜成果生命周期

专业完成状态与实体文件状态必须分离。任务成果至少区分：

1. `STRUCTURE_PROTOTYPE`：结构原型；
2. `WORKING_DRAFT`：研究/核验尚未完成的工作草稿；
3. `RESEARCH_COMPLETE`：研究充分性门已通过，但未完成独立完成审查；
4. `REVIEWED_DRAFT`：必要审查已完成并完成实质回写；
5. `FINAL_DELIVERABLE`：通过 Formal Delivery Gate 的最终成果。

DOCX/PDF/HTML/表格/图形真实存在，只能证明相应 `artifact_physical_state`；不能单独把 `professional_lifecycle_state` 提升为 FINAL。

## 6. Negative Feedback Reset｜否定性反馈重置

当用户反馈实质否定此前的完成判断，例如“没有做类案检索”“没有用我指定的数据库”“这只是简略版”“关键材料没看”，应把它视为**可能的状态重置事件**：

1. 识别被否定的完成假设；
2. 判断哪些 COMPLETE 状态因此不再可信；
3. 将受影响模块标记为 `INVALIDATED / PARTIAL / IN_PROGRESS`；
4. 沿依赖链重新执行；
5. 重新完成必要审查与正式交付门。

不得把根本性缺口只作为局部补丁追加到旧“最终版”。

## 7. Research Sufficiency Gate｜研究充分性门

需要深度法律/类案研究时，在 Research 标记 COMPLETE 前至少检查：

- 直接法律问题是否覆盖；
- 法域、时间、规范层级和现行效力是否核验；
- 用户指定或可用的专业数据库/知识库是否按任务权限和能力真实路由；
- 支持、反向、边界、区别、例外是否按任务需要处理；
- 重要候选案例是否完成原始来源/全文/裁判理由核验；
- 是否仍存在合理可能改变结论而尚未检索的路径；
- 无法继续检索的限制是否进入 BLOCKED/INCOMPLETE 披露。

“有若干搜索命中”不能通过该门。具体研究方法与 `SATURATED / INCOMPLETE / BLOCKED` 判断仍由 Research owner 负责。

## 8. Independent Completion Auditor｜独立完成审查

重大正式交付前，在原执行阶段之外增加 Completion Audit。宿主支持独立 Agent/隔离上下文时优先使用；不支持时至少进入与起草阶段分离的验收阶段。

Completion Auditor 只检查可审计完成条件，不要求也不得索取私有推理链：

- 用户原始目标是否仍完整；
- triggered modules 是否齐全；
- COMPLETE 是否都有完成依据；
- 是否掩盖 PARTIAL / BLOCKED / INVALIDATED；
- 上游变化是否已传播；
- 对抗性审查发现的问题是否真实回写；
- 实体文件生成是否被错误当成专业完成；
- 最终成果与 TaskExecutionContract 是否一致。

## 9. Formal Completion Gate｜完成声明阻断

任何对当前目标必需的模块处于 `NOT_STARTED / PARTIAL / BLOCKED / INVALIDATED`，且该缺口未被合法降级、明确披露并获得必要的人类决定时，不得使用“全部完成”“最终版”“正式成果”“已完整执行爽律skill”等无保留完成性措辞。

Formal Delivery Guard 拥有最终交付门；本单元提供任务执行状态和完成依据。

## 10. Visible Execution Ledger｜用户可见执行核验

### 任务开始

对进入实质执行且不是极小型单点任务的爽律skill任务，向用户展示**本任务实际触发的主要流程**及初始状态。复杂、多模块、长任务或重大正式交付显示主要模块状态；小型实质任务可压缩为一句流程说明。只显示与当前任务有关的项。

### 执行中

在有意义的阶段节点更新：`已完成 / 进行中 / 部分完成 / 受阻 / 已失效需重跑 / 未开始`。进度消息发送后，如无真正人工干预节点，继续执行下一未完成模块，不默认停下来等待“继续”。

### 最终交付

附简洁的“爽律skill执行核验”，至少包含：

- 主要要求；
- 当前状态；
- 最小完成依据；
- 仍存在的限制/阻断（如有）。

用户可见状态必须由内部 `ModuleExecutionLedger + proof_of_work` 投影生成，不得维护另一套表演式清单。

## 11. Privacy Boundary｜不展示私有推理链

可展示：工作流程、模块状态、材料覆盖、检索/核验范围、来源、产物、完成依据、缺口、阻断、失效和交付状态。

不得展示或要求：模型隐藏 chain-of-thought、逐 token 推理、内部私有草稿。对抗性审查只输出可复核问题、结论和修改结果。

## 12. Long Task Continuation｜长任务续跑

只有以下情形允许自然暂停等待用户：

- 重大人工决定；
- 敏感外发/副作用授权；
- 缺少会实质改变结论的关键材料且无法自行恢复；
- 权限或工具真实阻断；
- 用户明确要求暂停。

除此之外，阶段性汇报不能替代继续执行。

## 13. Unauthorized Mutation Guard｜未经授权修改保护

发现任务执行失败时，先区分：规则缺失、规则未加载、规则未转化成状态、状态未阻断完成、或执行者绕过了阻断。只有确认规则确实缺失，才形成 Skill 改进建议。

**不得因为一次执行失败就擅自修改用户安装的爽律skill。** 修改、覆盖、升级用户本地 Skill 必须来自当前用户明确指令，并同时遵守 Side-effect Authorization 与 `UPDATE_INSTRUCTIONS.md` 的用户资产保护规则。

## 14. 与既有 Owner 的接口

- 专业真值：Facts / Evidence / Research / Reasoning / Review 各自拥有；
- 现行法：Current-law Guard；
- 依赖失效：Matter Invalidation；
- 专业连续性：Matter Professional State；
- 重要命题核验：Review / VerificationLedger；
- 实体文件：Document Render / Host；
- 正式交付：Formal Delivery Guard；
- 对外/删除/写入授权：Side-effect Authorization；
- 爽律skill自身升级安全：`UPDATE_INSTRUCTIONS.md`。

本单元只拥有**任务执行契约、模块执行状态、完成依据、成果生命周期与用户可见执行投影**，不得建立第二套法律事实、证据或法律来源真值。

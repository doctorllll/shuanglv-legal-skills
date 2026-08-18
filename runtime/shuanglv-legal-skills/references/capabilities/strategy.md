# Strategy｜策略与选项

`unit_id: unit.cap.strategy`

**Scope：** Legal option generation, sequencing, risk and decision support.

## Trigger
- Directive asks what to do, how to respond, sequence actions, choose among legal options or manage procedural/negotiation risk.
- A substantive legal conclusion must be translated into options and timing.

## Negative Trigger
- Pure rewrite or formatting.
- No decision/action question and no strategic consequence.

## Essential Procedure
1. Generate feasible options.
2. Compare legal upside/downside, evidence dependence, timing and reversibility.
3. Identify reserved human decisions.
4. Recommend sequence without converting recommendation into authorization.

## Deepening Conditions
- High consequence or irreversible option.
- Procedural deadlines/statement strategy/settlement position.
- Multiple domains interact.

## Exit Sufficiency
- User has a decision-ready option set and unresolved assumptions are visible.

## Professional Results
- option set
- risk/tradeoff matrix
- sequence/timing plan
- decision points

## Conditional Guards
- unit.guard.human-decision
- unit.guard.side-effect-auth


## Strategy Method

## 一、目的

法律上“可以做”不等于律师“应当做”。爽律 Skill 对存在多条程序、诉讼、辩护、控告、合同或交易路径的任务，应把法律分析转化为可比较的行动选项，并把不可替用户决定的事项停在明确的人工作业节点。

## 二、什么时候建立选项

出现以下任一情形时，应考虑形成结构化选项：

- 主位与备位法律路径并存；
- 起诉、仲裁、和解、保全、执行等存在路径选择；
- 刑事案件中存在不同辩护重点、披露时点、认罪认罚等选择；
- 控告案件存在刑事、民事、行政或证据保全等并行路径；
- 合同存在接受、修改、拒绝、附条件接受或以对价换风险的选择；
- 尽调发现风险后存在交割前解决、先决条件、赔偿保障、价格调整或终止等方案；
- 法律顾问事项存在多个业务方案。

## 三、统一比较维度

根据任务性质选择必要维度，常见包括：

- 法律可行性；
- 事实和证据成熟度；
- 程序时点与期限；
- 对方可能反应；
- 对后续举证、调查或谈判空间的影响；
- 时间和经济成本；
- 可执行性和回收可能；
- 商业关系或声誉影响；
- 可逆性；
- 需要用户承担的重大风险。

不要求伪精确量化，不默认计算“综合得分”。

## 四、推荐与决定分离

Agent 可以在 B 级事项中形成专业推荐，但必须说明依据和限制。

C 级事项必须区分：

> **专业推荐**：Agent/律师认为哪个方案在当前信息下更优；
>
> **最终决定**：用户是否接受该方案及相应后果。

不得把“推荐方案 A”自动写成“用户决定选择 A”。

## 五、决定后的回写

用户或律师作出决定后，应检查是否需要更新：

- 客户目标；
- `IssueRecord` 优先级；
- 后续研究范围；
- 证据收集计划；
- `Finding`；
- `OptionRecord` 状态；
- 文书策略和 `DeliverableClaim`。

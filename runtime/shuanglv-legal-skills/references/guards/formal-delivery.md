# Guard｜Formal Delivery

`unit_id: unit.guard.formal-delivery`

**Scope：** Formal legal deliverable completeness guard.

## Trigger
- Directive asks for a final/formal legal deliverable such as pleading, defense opinion, formal opinion, contract final or equivalent.

## Negative Trigger
- FORMAT_ONLY source document with no substantive legal finalization requested.
- Informal exploratory answer.

## Essential Procedure
1. Check required sections/content support.
2. Check traceability and unresolved uncertainty.
3. Require adversarial review when material/high-stakes.
4. Separate semantic finalization from rendering.
5. Run `External Deliverable Hygiene Check` before FINAL.
6. When `unit.interop.execution-control` is triggered, require Completion Audit and verify no required `NOT_STARTED / PARTIAL / BLOCKED / INVALIDATED` state is hidden before FINAL.
7. If the requested deliverable is a rendered/native document, require resolution of the applicable `DocumentStyleProfile` and rendering QA; authority/document-type/user template overrides the 爽律skill default baseline.
8. If a legal visualization is FINAL, require semantic/cognitive/visual QA; interactive FINAL additionally passes the `Dynamic Delivery Fidelity Gate`.

## Deepening Conditions
- High stakes/long complex formal document.

## External Deliverable Hygiene Check

按 Composition 的 Internal Analysis → External Deliverable Boundary 对最终正文做阻断式检查，至少覆盖：internal strategy leakage；self-undermining language；work-process leakage；adversarial/red-team residue；unverified assumption promotion；AI/tool/research-process residue；TODO/placeholder；internal instruction leakage；audience-inappropriate information。

**命中并不等于一律删除。** 有对外价值的先转成来源支持、确定性匹配且适合当前受众的 `EXTERNAL_CLAIM`；无必要内容排除；未核实事项不得晋升；真实重大风险不得被卫生检查隐藏。无法安全转换且影响可靠性时阻断 FINAL，避免因机械清理造成信息损失。

## Exit Sufficiency
- Formal deliverable is substantively complete and all blocking defects resolved/labeled.
- `External Deliverable Hygiene Check` 已通过：不存在未处理的内部泄漏，且有价值的内部分析没有因机械删除而造成实质信息损失。
- If a rendered/native artifact was requested, its applicable format/profile requirements are satisfied or any unsupported fidelity is explicitly disclosed.

## Professional Results
- delivery-readiness state

## Bundle / Artifact Fidelity Gate

正式交付如果包含多个相互依赖文件：

- 用户明确要求和 `VERIFIED_REQUIRED` 的交付物必须完成或明确阻断；
- 共享主体、日期、金额、请求、案号、附件编号等不得在不同文件间漂移；
- 影响正式内容的 STALE/PENDING 结果或共享字段变化必须关闭、更新或明确阻断；
- 实体文件须能正常打开，声称的 DOCX/PDF/Track Changes/comments/图形能力必须与真实 artifact 一致；
- 同一正式版本导出的 Redline / Clean Copy / PDF / 其他派生交付物，其**实体内容必须一致**；差异只能来自修订标记、批注、版式或载体，不得出现一份已改而另一份仍保留旧实体内容；
- 任何格式、工具或能力降级必须显式披露。


## Dynamic Delivery Fidelity Gate｜动态正式交付保真门

交互 HTML/Web/Host-native visual 可以作为正式成果，但必须额外验证：

1. **Openability**：实际成果能够打开和运行，不以“已生成代码”冒充“可用交付物”；
2. **Dependency truth**：外部网络/CDN/字体/脚本依赖真实披露；正式离线要求下不得暗含网络依赖；
3. **Sensitive-data boundary**：交互包是否携带客户秘密、个人信息、证据原文等敏感数据，外发边界已处理；
4. **Frozen semantics**：保存 `LegalVisualSpec` / 数据版本或 hash，不能在交付后静默改变底层数据；
5. **Reproducible ViewState**：当前筛选、图层、时间窗口、聚焦路径可冻结/复现；
6. **Static companion**：原则上同时保留可打印/归档的静态快照；确有例外必须显式说明；
7. **Target compatibility**：目标浏览器/设备/演示环境可用，或明确兼容性限制；
8. **No hidden counter-evidence by default**：默认筛选/折叠不得隐藏决定性反向证据、重大不确定性或关键限定条件；
9. **Snapshot consistency**：从动态成果导出的 SVG/PNG/PDF/截图与同一 ViewState 语义一致；
10. **Graceful degradation**：动态失败不得拖垮已经可靠完成的静态基础成果。

动态交付的视觉交互状态不是事实状态。`隐藏 ≠ 删除；筛选 ≠ 否认；聚焦 ≠ 证明。`

## Execution Completion Gate｜v0.51 执行完成门

当任务加载 `references/interop/execution-control.md` 时，Formal Delivery 在 FINAL 前必须读取其 `TaskExecutionContract / ModuleExecutionLedger / proof_of_work` 投影：

- 目标交付物与用户原始目标一致；
- 所有必需模块均达到可接受退出状态；
- `COMPLETE` 均有最小完成依据；
- `PARTIAL / BLOCKED / INVALIDATED` 未被隐藏；
- 上游变化已传播到受影响成果；
- 必要的 Completion Audit 已完成；
- 实体文件存在状态没有被偷换成专业完成状态。

任一必需缺口仍未关闭且未被明确降级/披露时，只能交付工作稿、部分成果或受阻说明，不得无保留标记 `FINAL_DELIVERABLE`。

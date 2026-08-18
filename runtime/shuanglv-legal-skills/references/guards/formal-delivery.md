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
6. If the requested deliverable is a rendered/native document, require resolution of the applicable `DocumentStyleProfile` and rendering QA; authority/document-type/user template overrides the 爽律 default baseline.

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

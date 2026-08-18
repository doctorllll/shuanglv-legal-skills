# External｜Document Render

`unit_id: unit.external.document-render`

**Scope：** Actual DOCX/PDF/rendering/Track Changes capability contract + canonical physical legal-document style baseline.

## Trigger
- Directive requires formatting/rendering/file output/native document operations.

## Negative Trigger
- No artifact/rendering requested.

## Essential Procedure
1. Preserve semantic content constraints. FORMAT_ONLY must not silently alter facts, legal conclusions, clauses, dates, amounts or other substantive meaning.
2. Resolve the applicable `DocumentStyleProfile` before rendering.
3. Apply style priority: specific authority/platform mandatory requirement > official document-type rule or designated template > current national language/format convention > 爽律 default legal-document baseline > renderer default.
4. Use actual renderer capability.
5. Claim native Track Changes/comments only if supported and executed.
6. Keep semantic changes distinguishable from rendering changes.
7. After rendering, verify page/paragraph/style/numbering/version fidelity rather than assuming the renderer applied the profile correctly.

## Default Legal Document Style Baseline

This baseline fills gaps only. It is **not** represented as a mandatory court/procuratorate/arbitration format. A specific authority, user template or document-type requirement overrides it.

### Page
- Paper: A4.
- Top / bottom margins: 2.54 cm.
- Left margin: 3.0 cm.
- Right margin: 2.5 cm.
- Page number: centered footer by default, unless the applicable template requires otherwise.
- Do not create pagination by stacking blank paragraphs.

### Main title
- Prefer a formal Chinese title serif such as 小标宋-type font when available.
- If unavailable, use a compatible formal serif such as 宋体 / 思源宋体 with appropriate bold treatment.
- Approximately 16 pt（三号）.
- Centered; no two-character first-line indent.
- Avoid unnecessary color, shadow, decorative lines or marketing-style effects.

### Level-1 heading
- 黑体 / 思源黑体 or compatible sans-serif heading font.
- 14 pt（四号）.
- Default numbering: `一、二、三……`.
- When used as a structural heading inside body text, first-line indent 2 Chinese characters unless an official/template rule overrides it.

### Level-2 heading
- 宋体 or 黑体 bold; use 楷体 only where the applicable authority/document profile calls for it.
- 12 pt（小四）.
- Default numbering: `（一）（二）（三）……`.
- Structural body heading: first-line indent 2 Chinese characters unless overridden.

### Level-3 and below
- Prefer `1.` then `（1）`.
- Structural body heading: default first-line indent 2 Chinese characters.
- Avoid more than four heading levels; restructure instead of creating excessive hierarchy.

### Heading-indent boundary
- The two-character indent applies to body structural headings, not the centered main title.
- Functional labels such as `诉讼请求：`、`事实和理由：`、`此致`、`附件` follow the relevant official/document-type/template convention and are not mechanically treated as ordinary headings.
- When a structural heading wraps, first line remains indented two Chinese characters and continuation lines align with the body convention.
- Use paragraph/style properties; do not fake indentation with manually typed full-width spaces.

### Body text
- Formal Chinese serif such as 宋体 / 思源宋体.
- 12 pt（小四）.
- Default line spacing: 1.5 lines.
- Natural paragraph first-line indent: 2 Chinese characters; continuation lines flush to the paragraph margin.
- Paragraph spacing before/after: 0 by default.
- Do not reproduce AI-style one-sentence-per-paragraph fragmentation.

### Quotations / footnotes
- Legal/case/document citations must remain traceable to source.
- Footnote default: 9–10.5 pt.
- Do not use a bare URL as a substitute for formal source identification unless the delivery context specifically requires it.

### Tables
- Usually 9–10.5 pt where needed for density, while preserving readability.
- Clear headers; consistent units, dates and currency formatting.
- Avoid large decorative color blocks.
- Evidence/risk matrices prioritize legibility over decoration.

### Numbers and dates
- Default formal Chinese date pattern: `YYYY年M月D日`；use the actual document date, not a fixed example date.
- First occurrence of an amount may use a form such as `人民币106,000.00元`; keep the chosen convention consistent thereafter.
- Percentages, currencies, units, article numbers, evidence numbers and attachment names must be consistent throughout.

### Prohibited / discouraged rendering patterns
- Do not carry Markdown `#` or `**` markers into Word output.
- Do not use blank lines as layout controls.
- Do not use gratuitous bold, emoji, decorative effects or inconsistent style overrides in formal legal documents.
- Prefer deterministic named Styles/Templates over asking the language model to improvise formatting on every run.

## Deepening Conditions
- Native Track Changes/comments.
- Complex artifact fidelity, long documents, mixed tables/footnotes/appendices, authority-specific templates, or a user-supplied style template.

## Exit Sufficiency
- Applicable style profile was resolved.
- Artifact exists with claimed fidelity, or limitation is explicitly stated.
- FORMAT_ONLY semantic preservation has been checked.
- Required page, heading, body, numbering, page-number and version properties have been verified where applicable.

## Professional Results
- rendered artifact or explicit capability downgrade
- applied `DocumentStyleProfile`
- rendering QA result

## Graphical Delivery Contract｜图形化法律交付

当图形相较自然语言能够显著降低理解成本、揭示关系/时间/资金/证据结构，或用户明确要求时，Document Render 负责把上游结构化结果渲染为用户可见图形；**不得仅因“可以画图”就自动生成。**

### DiagramSpec 中间层

上游 Capability 先提供可追溯 `DiagramSpec`，至少描述节点、关系、标签、事实状态、来源引用和推荐布局。常见类型：

`ENTITY_RELATIONSHIP / TRANSACTION_STRUCTURE / MONEY_FLOW / TIMELINE / SWIMLANE_TIMELINE / PERFORMANCE_FLOW / EVIDENCE_MAP / ISSUE_TREE / OPTION_TREE / ARGUMENT_MAP`。

一图一主题；复杂事项拆图，不把所有信息塞成一张蜘蛛网。

### 渲染能力与降级顺序

实际能力应按 Host 验证，而不是按模型想象：

1. 有可靠本地/受控 PNG 渲染能力 → 优先 PNG；
2. 无 PNG 但可创建/打开 HTML → 自包含响应式 HTML（内嵌 SVG/CSS，不依赖外部网络）；
3. Mermaid / Graphviz / PlantUML 等可作为中间图源并尽量渲染成用户可见格式；
4. 只能文本 → `DiagramSpec + 可渲染图源 + 最简文本安全版`，并明确**未实际生成图片文件**。

不得因本地无渲染器而静默把敏感案件信息发送到第三方在线图形服务；需外部处理时进入 External Processing Guard。

### 图形 QA

- 主体、金额、日期、关系不得超出上游支持；
- 重要节点保留 source/locator；
- 手机可读，过密时拆图；
- 关键法律含义不只依赖颜色；
- 文字重叠、箭头错误、节点截断或图片模糊时不得作为正式成果。

## Native Editing / Track Changes Downgrade

在交付前实际检查 DOCX 原生修订、批注、Redline、Clean Copy、PDF、页码/引用等能力。

- 若用户只要求“体现修改”而原生 Track Changes 不可用，可在不违反用户指令的情况下降级为：`Redline + Clean Copy + Change Summary`，标记 `DOWNGRADED`；
- 若用户明确要求**必须**原生 Track Changes，而 Host 不支持，则 `BLOCKED`，不得用红字或普通文本冒充原生修订；
- 批注同理：只有实际生成可定位 comments 才可声称已完成批注。

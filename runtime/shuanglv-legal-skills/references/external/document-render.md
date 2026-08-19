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
3. Apply style priority: specific authority/platform mandatory requirement > official document-type rule or designated template > current national language/format convention > 爽律skill default legal-document baseline > renderer default.
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

法律可视化的**方法所有权**属于 `unit.cap.visualization`：是否值得可视化、目的/受众、结构识别、图型路由、信息精简、stance/emphasis、静态/交互决策均在该能力中完成。Document Render 不重新从原材料理解案件，而是消费同一 `LegalVisualSpec / DiagramSpec v2`，负责确定性布局、实体生成、文件真实性和几何 QA。

### Semantic input contract

Renderer 至少接收：`visual_id / visual_type / object_refs / source_refs / native_status / presentation_modes / visual_profile / ordering/grouping constraints / data_version_or_hash`。需要 artifact 快照时可以保存 display snapshot，但必须保留 `object_ref + snapshot_at`；不得创建 VisualFact / VisualEvidence 等第二套事实模型。

模型不得以最终像素坐标作为语义真相。Canonical geometry 是 renderer 对 `LegalVisualSpec` 的派生结果；同一 Spec 可派生静态、交互和演示版本。

### Deterministic static render

可按 Host 真实能力生成 `SVG / PNG / PDF / PPTX / editable diagram format`。关键文字、金额、日期、证据编号、箭头方向、关系和事实状态必须直接来自确定性语义层。

### Interactive render

Host 真实支持 `INTERACTIVE_VISUAL_RENDER` 时，可生成 self-contained HTML/Web 或 Host-native artifact。正式交付优先自包含资源，不依赖未披露 CDN；至少支持与任务相称的详情查看、来源定位、搜索/筛选、图层状态、恢复默认和静态快照。ViewState 与底层事实数据必须分离。

用户未明确要求交互时，Document Render 不自行升级交互；由 Visualization Capability 在“交互明显有增益 + Host 支持”时决定是否向用户提供增强选项。用户已明确要求交互时直接执行能力路径。

### Snapshot / version

正式交互成果应能冻结 `ViewState + data_version_or_hash + timestamp`，并原则上保留静态 companion。动态与静态来自同一语义源，不得重新抽取或重新解释事实后另画一套。

### Optional generative enhancement

`GENERATIVE_VISUAL_ENHANCEMENT` 只能作用于确定性成果之上的背景、非语义图标、插画或视觉气氛。不得改变或生成法律事实、人物身份、金额、日期、比例、证据编号、箭头方向、法律关系、FactStatus/EvidenceStatus。涉及敏感案件内容且需要外部处理时进入 External Processing Guard。

### Renderer QA / hard failures

以下问题在正式成果中属于阻断缺陷：

- node/relation target 不存在、orphan/dangling 结构错误；
- 箭头方向漂移、金额/日期/文字漂移；
- 非有限坐标、off-canvas、严重 overlap/clipping/text overflow；
- 过密导致不可读却未拆图；
- 关键含义只依赖颜色、黑白打印无法区分；
- CJK 字体缺失导致乱码/截断；
- 交互筛选状态不可见或默认隐藏决定性反向信息；
- 动态文件打不开、快照与当前视图语义不一致；
- 声称存在 PNG/PDF/PPTX/HTML，而 Host 实际未创建或未验证。

### Capability fallback ladder

1. 目标静态格式可真实生成 → 生成并验证；
2. 目标交互格式可真实生成 → 生成交互 + 静态 companion，并验证；
3. 交互不支持但静态能满足核心正确性 → `DOWNGRADED` 到静态并披露；
4. 只能输出 `LegalVisualSpec + 可渲染图源` → 明确**未生成目标实体图形文件**；
5. 用户强制要求某种无法提供且不可接受降级的原生/交互能力 → `BLOCKED`。

不得因本地无渲染器而静默把敏感案件信息发送到第三方在线图形服务。

## Native Editing / Track Changes Downgrade

在交付前实际检查 DOCX 原生修订、批注、Redline、Clean Copy、PDF、页码/引用等能力。

- 若用户只要求“体现修改”而原生 Track Changes 不可用，可在不违反用户指令的情况下降级为：`Redline + Clean Copy + Change Summary`，标记 `DOWNGRADED`；
- 若用户明确要求**必须**原生 Track Changes，而 Host 不支持，则 `BLOCKED`，不得用红字或普通文本冒充原生修订；
- 批注同理：只有实际生成可定位 comments 才可声称已完成批注。

# Review｜复核、对抗与溯源

`unit_id: unit.cap.review`

**Scope：** Second-pass adversarial review of a substantive legal analysis or deliverable.

## Trigger
- User explicitly asks to challenge/review/counter/check weaknesses.
- Complex/high-stakes substantive work has competing plausible models or material flip points.
- A formal deliverable would materially benefit from independent attack before finalization.

## Negative Trigger
- Local low-risk semantic rewrite.
- FORMAT_ONLY/render-only task.
- Do not trigger full adversarial review for every simple legal answer.

## Essential Procedure
1. Freeze the initial position.
2. Construct the strongest credible opposing model.
3. Identify facts/law/evidence that could flip the result.
4. Distinguish real weakness from generic caution.
5. Write back only material corrections.

## Deepening Conditions
- Criminal defense/major dispute/major transaction.
- Material uncertainty or conflicting evidence/authority.
- Formal high-consequence opinion.

## Exit Sufficiency
- No unaddressed material countermodel remains, or residual risk is explicitly accepted/labeled.

## Professional Results
- strongest countermodel
- flip points
- defects
- revision/writeback actions


## Adversarial / Traceability Method

## 一、目的

爽律skill 的对抗性审查不是为了“故意唱反调”，而是为了在正式交付前主动寻找：

- 当前结论可能错在哪里；
- 哪些事实被忽略；
- 哪些反向证据足以改变判断；
- 是否存在更高权威或更新的法律来源；
- 对方最强的法律或事实路径是什么；
- 哪个假设一旦不成立，结论会翻转；
- 哪些风险因为信息不足而被低估。

> 先形成初步方案，再用第二遍审查主动攻击它，然后修正后再交付。

## 二、什么时候必须做

以下任务默认必须进行完整对抗性审查：

- Formal Delivery 已触发且本次属于重大正式交付；
- 任务的 `Signal × Materiality` 表明关键结论存在实质翻转风险，完整第二遍攻击对可靠性有明显价值；
- 重大诉讼/刑事/交易策略或不可逆权利处分建议；
- 用户明确要求“对抗性审查、反向审查、挑错、压力测试、全面审查”。

局部、低风险或单点任务默认只做与本轮问题直接相关的反向检查，不要求额外加载完整对抗性审查规范、清单或生成独立 `AdversarialReviewRecord`。是否进入完整对抗审查由信号与重要性决定；常规正式文种也不因“正式”二字自动升级。

## 三、统一四步法

### 第一步：冻结初步结论

先明确当前初步结论是什么，以及它依赖哪些关键事实、规则和假设。

不能一边反驳一边偷偷改变原结论，否则无法知道审查到底发现了什么。

### 第二步：建立最强反方模型

不是找一个容易反驳的“稻草人”，而是主动构造：

- 对方最强事实版本；
- 对方最强证据组合；
- 对方最有利法律解释；
- 关键例外；
- 更高权威或更新规则；
- 最合理的替代解释。

### 第三步：寻找翻转点

重点问：

> 哪个事实、证据、规则或假设一旦改变，会使当前结论发生实质变化？

把这些点标记为：
- 已经核验；
- 尚未核验；
- 存在冲突；
- 需要人工判断。

### 第四步：修正并分级结论

审查后不能只写“已复核”。

必须根据发现决定：

- 原结论维持；
- 原结论需要增加限制；
- 原结论需要降低确定性；
- 需要补充材料/研究；
- 需要改换方案；
- 需要人工升级；
- 原结论不能继续使用。

## 四、对抗审查记录

需要完整对抗性审查的 深度执行或正式交付 任务应形成 `AdversarialReviewRecord` 或同等可审计记录，至少写：

- 初步结论；
- 最强反方路径；
- 发现的关键漏洞；
- 哪些问题已经解决；
- 哪些问题仍未解决；
- 修正后的结论；
- 是否触发人工复核。

记录的是**审查结果和可复核问题**，不要求输出模型内部完整推理过程。

### Adversarial residue boundary

`AdversarialReviewRecord` 及其攻击语言默认属于 `INTERNAL_ONLY`，不得机械进入对外文书；有对外价值时先回写上游对象，再按 Composition 转成 `EXTERNALIZABLE`，仅已核验、确定性匹配且适合当前受众的命题进入 `EXTERNAL_CLAIM`。不得借“清理残留”隐藏会改变专业结论的重大不利事实。

审查发现实质问题后必须回写原 `ArgumentRecord` / `Finding`；如维持原结论，应记录为什么最强反方仍不足以改变结论。不得仅追加“风险提示”而让受影响的原结论保持不变。

## 五、禁止事项

- 只重复初步结论，不算对抗性审查；
- 只找弱反驳，不算对抗性审查；
- 把“我没想到反例”写成“没有反例”；
- 发现重要反向材料后仍保持原结论不作解释；
- 为了显得客观，人为制造没有实际依据的反对观点；
- 对法律、事实或证据的真实冲突用模糊措辞掩盖。

---

## 一、目的

爽律skill 对重要专业结论实行**全链路可追溯**：不仅要求“有引用”，还要求能够回答以下问题：

- 事实从哪份材料、哪个位置获得；
- 某项证据究竟支持或反驳哪个事实命题；
- 法律规则来自何种权威来源、具体定位在哪里、是否完成当前有效性核验；
- 案例为什么与本案可比、在哪些事实或规则上存在区别；
- 从事实、证据和规则到结论之间采用了什么可审计的专业论证；
- 最终文书或报告中的重要命题能够回到哪些上游分析对象；
- 哪些内容仍然属于推断、争议、未知或待核验事项。

可追溯要求针对**专业判断依据和论证结构**，不要求模型公开隐藏的内部思维过程。

## 二、核心链条

重要事项原则上形成以下关联：

```text
原始材料 / 外部权威来源
        ↓
SourceLocator（精确来源定位）
        ↓
SourceCard / MaterialRecord（来源身份）
        ↓
EvidenceItem / FactRecord（证据与事实）
        ↓
IssueRecord（需要解决的问题）
        ↓
LegalRule / CaseCard（规范与案例）
        ↓
ArgumentRecord（可审计论证）
        ↓
Finding（分析发现）
        ↓
DeliverableClaim（交付物中的重要命题）
```

上述关系不是强制单线结构。一份材料可以支持多个事实；一个事实可以由多项证据支持或反驳；一个结论可以同时依赖多个规则、案例和事实。

## 三、来源身份与精确定位必须区分

### 1. SourceCard：回答“这是什么来源”

例如：

- 某份合同、聊天记录、笔录、流水；
- 某法律、司法解释、规范性文件；
- 某裁判文书；
- 某专业数据库记录；
- 用户知识库中的某份文件。

### 2. SourceLocator：回答“具体在哪里”

根据材料类型保留：

- PDF / Word：页码、段落、行号；
- Excel：Sheet + 单元格或区域；
- 音视频：时间戳；
- 聊天记录：消息 ID、日期时间或可复核位置；
- 网页：页面、标题、章节或段落；
- 数据库：数据库名称、记录 ID、文书位置；
- 法条：法律名称 + 条/款/项；
- 案例：案号 + 裁判理由或对应原文位置。

只有来源名称而没有必要的精确定位，不等于完整溯源。

## 四、事实溯源

### 1. VERIFIED

重要事实标记为 `VERIFIED` 时，必须能够回到至少一个实际来源；案件材料中的事实还应尽可能关联具体证据和定位。

### 2. ALLEGED / DISPUTED

当事人、证人或其他主体的陈述本身可以作为来源，但不得因此将陈述内容自动升级为 `VERIFIED`。应记录：

- 谁作出该陈述；
- 陈述出现于何处；
- 是否有其他独立材料支持或反驳。

### 3. INFERRED

`INFERRED` 必须记录 `inference_basis`。至少说明：

- 依据哪些已知事实、证据或明确前提；
- 采用何种推断方式；
- 存在哪些竞争解释；
- 哪些新材料可能使该推断被推翻。

没有推断依据，不得把事实标记为 `INFERRED` 后继续作为确定前提使用。

## 五、证据溯源

每个重要 `EvidenceItem` 应关联：

- 来源身份；
- 精确来源定位；
- 支持或反驳的事实/待证命题；
- 必要的真实性、合法性、关联性、可靠性、完整性评价；
- 与其他证据的独立、同源、矛盾或印证关系。

“证据存在”与“证据能够证明某一命题”必须区分。

## 六、法律规则溯源

### 1. 当前有效规则

法律规则标记为 `VERIFIED_CURRENT` 时，至少必须记录：

- 权威来源；
- 精确条文或对应定位；
- 核验时间；
- 适用法域；
- 与案件关键时间的关系；
- 如适用，特别规则、例外、过渡规则或冲突情况。

没有真实核验，不得使用 `VERIFIED_CURRENT`。

### 2. 规则支持范围

记录某个法律来源时，还应说明其支持的命题。不得把“找到相关法条”直接等同于“本案已经满足法条条件”。

## 七、案例溯源

重要案例至少记录：

- 法院/机关、案号、裁判日期、文书类型；
- 原始来源及精确定位；
- 与当前问题相关的裁判规则或理由；
- 决定性事实；
- 与本案的相同点；
- 区别点；
- 使用目的：规则支持、事实模式、证据模式、反向案例、区别案例、程序参考等；
- 案例权威层级及适用边界。

不得因为关键词相似就把案例作为支持依据。

## 八、分析理由溯源

重要 `ArgumentRecord` 不得只有结论。最小可审计结构为：

```text
问题 Issue
+ 规则 Rule / Case
+ 关键事实 Fact
+ 证据 Evidence / Source
+ 推理方法 Reasoning Method
→ 结论 Conclusion
```

重大或高风险事项还应增加：

```text
+ 最强反方观点
+ 回应
+ 翻转点
+ 剩余不确定性
```

对于抽象法律研究，可以没有案件事实，但必须有可回查的规范、案例或其他权威来源，以及从来源到研究结论的论证结构。

## 九、最终交付物反向溯源

正式报告、法律意见、诉讼文书、辩护/代理意见、合同审查报告等，对其中的**重要事实命题、法律命题和核心专业判断**建立 `DeliverableClaim`。

每个重要交付命题应至少能够关联到下列一种或多种上游对象：

- `Finding`；
- `ArgumentRecord`；
- `FactRecord`；
- `LegalRule`；
- `CaseCard`；
- `EvidenceItem`；
- `SourceCard / SourceLocator`。

最终对外文书不必显示内部 ID，但内部执行记录必须保留映射。这样当材料、事实或法律发生变化时，可以定位哪些结论和文书段落需要重新审查。

## 十、重要程度与溯源强度

### 简单事实性任务

保留必要来源即可，不为了形式制造复杂关系图。

### 一般专业任务

重要事实、法律依据和主要结论应可回查。

### 重要任务 / 正式交付

原则上实行完整溯源：

- 关键事实有来源；
- 当前法律依据有权威来源和精确定位；
- 使用案例有可比性与区别分析；
- 核心论证有规则—事实—证据—理由链；
- 重要交付命题能够回到上游分析。

## 十一、禁止模式

- 引用了一部法律，但没有说明具体条文或其支持什么命题；
- 引用了一个案例，但无法定位裁判理由或无法解释可比性；
- 事实标记 `VERIFIED`，但没有任何可回查来源；
- 事实标记 `INFERRED`，但没有推断依据；
- 只给“综合判断”“倾向认为”“显然”等结论，没有可审计连接；
- 用二手摘要冒充原始法律、案例或证据来源；
- 最终文书出现重大新结论，但上游分析中从未形成对应 Finding / Argument；
- 因无法定位来源而自行补造页码、案号、法条或数据库记录。

## 十二、工程门控

正式交付前，工程执行层对重要任务检查：

- 重要命题是否全部形成可追溯链；
- `VERIFIED_CURRENT` 法律规则是否具有权威来源、精确定位和核验时间；
- `INFERRED` 事实是否具有推断依据；
- 正式交付中的重要命题是否与上游分析记录相连；
- 是否存在断链、悬空引用或不存在的对象 ID。

未满足上述条件时，应返回 `BLOCKED` 或明确警告，而不是把缺少依据的结论作为正式完成成果交付。


# VerificationLedger｜统一核验台账

`VerificationLedger` 是**可见的核验状态投影**，用于把分散在 SourceCard、FactRecord、EvidenceItem、LegalRule、CaseCard、Finding、DeliverableClaim 等对象中的状态汇总给律师检查。它不是第二套事实真值系统，也不得覆盖各 canonical owner 的原生状态。

## 1. Row contract

每个重要对象/命题可形成一行，至少包括：

- `ledger_id`；
- `object_ref`；
- `object_type`：`SOURCE / FACT / EVIDENCE / LAW / CASE / FINDING / DELIVERABLE_CLAIM / OTHER`；
- `proposition_or_summary`；
- `source_ref`；
- `source_locator`；
- `native_status`：保留 canonical owner 的真实状态，例如 `VERIFIED / ALLEGED / INFERRED / VERIFIED_CURRENT / STALE`；
- `display_status`：仅用于汇总展示，不替代 native status；
- `status_authority`：谁拥有该状态的最终语义，例如 Facts / Evidence / Current-law Guard / Research / Matter Invalidation；
- `conflict_refs`；
- `human_review_required`；
- `material_to_core_conclusion`：该未解决项是否足以改变核心结论；
- `affected_result_refs`；
- `last_checked_at`。

## 2. Display status projection

为方便律师浏览，可以把不同 native status 投影为有限展示类，例如：

- `CONFIRMED`；
- `PARTIAL`；
- `DISPUTED`；
- `UNRESOLVED`；
- `STALE`；
- `BLOCKED`；
- `NEEDS_HUMAN`。

但必须同时保留 `native_status + status_authority`。不得把法律“已核验现行有效”、事实“有来源支持”、证据“证明力充分”压成同一个含义。

## 3. VerificationLedgerSummary

重要任务或正式交付前，可以输出 `VerificationLedgerSummary`：

- 各 `object_type` 总量；
- 各 `display_status` 数量；
- materially unresolved 数量；
- source conflict 数量；
- 待人工判断数量；
- STALE / BLOCKED 数量；
- 影响核心结论的 unresolved item 列表。

统计只反映当前台账状态，不得以“确认项数量很多”替代法律分析，也不得用百分比制造虚假的科学确定性。

## 4. Update / invalidation

上游 Source/Fact/Law/Case 状态变化时，Ledger 行随 canonical object 更新；如果对象进入 STALE，Ledger 只展示 STALE，不得自行重新核验。需要重新检索、证据评价或事实核验时，回到相应 owner。

## 5. Formal-delivery boundary

- materially relevant 的 `UNRESOLVED / STALE / BLOCKED / NEEDS_HUMAN` 必须在正式交付前关闭、降格表达、披露限制或阻断；
- 非决定性未解决项可以保留，但不得在成品中被写成已确认事实/法律；
- 最终文书不必展示内部 ledger ID，但关键命题应能够反向追溯到 ledger/object chain。

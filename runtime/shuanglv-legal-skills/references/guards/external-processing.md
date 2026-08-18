# Guard｜External Processing

`unit_id: unit.guard.external-processing`

**Scope：** Consent gate for sensitive third-party/cloud processing.

## Trigger
- Sensitive material would be sent to a third-party/cloud processor.

## Negative Trigger
- Local/on-device processing with no external disclosure.

## Essential Procedure
1. Describe provider, purpose and data scope.
2. Obtain scoped consent before disclosure.
3. Reauthorize material scope/provider changes.

## Deepening Conditions
- More sensitive data or different provider/purpose.

## Exit Sufficiency
- Authorized scope matches intended processing or processing is not performed.

## Professional Results
- provider/purpose/data authorization state


## Scoped Consent

- Sensitive third-party processing requires provider/purpose/data scoped consent.
- Changing provider/purpose/material data scope requires fresh consent.
- No silent cloud fallback.

Required fields: `consent_id`, `provider`, `purpose`, `data_scope`, `matter_id`, `authorized_at`, `status`

## Notice / Sensitivity / Vendor Truthfulness

在把用户文件、文本、图片、音视频或其片段发送到当前可信环境之外的第三方模型/API 前，除取得授权外，还应以与本次处理相称的粒度说明：

- provider / service；
- 实际发送哪些文件、字段或片段，是否整文件；
- processing purpose；
- 可能涉及的客户秘密、个人信息/敏感个人信息、商业秘密、案件材料等风险；
- provider logging / caching / retention、数据位置/跨境等属于**供应商当前政策或配置事实**，需要现查时必须核验，不得无依据承诺“绝不留存/一定境内/一定不训练”；
- 可能的 API 费用、识别/模型错误风险；
- 可用的本地、用户自有或用户控制替代路径。

数据敏感性可按任务需要区分：`PUBLIC / INTERNAL / CLIENT_CONFIDENTIAL / PERSONAL_INFORMATION / SENSITIVE_PERSONAL_INFORMATION / TRADE_SECRET / LEGAL_CASE_MATERIAL / UNKNOWN_HIGH`。敏感性越高，越优先本地或用户控制能力。

Consent 至少绑定 provider、purpose、data/file scope、processing mode、matter/session/time；provider、purpose 或发送范围发生实质变化必须重新授权。

凭证安全由 `unit.external.input-data` 承担；长期 API Secret 不进入 Skill 包、Matter State、普通 Markdown、测试日志或最终交付物。

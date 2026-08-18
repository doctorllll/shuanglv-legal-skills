# Preference｜Legal Work

`unit_id: unit.preference.legal-work`

**Scope：** Legal-work deliverable preferences only.

## Trigger
- Legal drafting/delivery needs stored length/heading/conclusion/research/format/House Style preference.

## Negative Trigger
- General chat personality.

## Essential Procedure
1. Apply only legal-work preferences relevant to deliverable.
2. Do not infer general persona.

## Exit Sufficiency
- Relevant preference is applied or absent.

## Professional Results
- legal-work preference projection

## Legal Work Preference / Template Resolution

法律工作偏好只处理**可合法个性化**的工作层，不得覆盖事实真实性、现行法核验、敏感数据授权、Reserved Human Decision、来源追溯等硬边界。

### 优先级

`Hard Guardrails > Matter/User Current Directive Override > User Legal-Work Preference & Template > Version Default`

- 用户当前任务明确指定模板/风格时，只影响其指定范围；
- 单次表现、语气或模型猜测不得静默升级为长期偏好；
- 找不到用户模板时不得声称“已按你的模板完成”；
- 用户模板只能提供结构/样式/表达参照，不能把旧案件的事实、主体、金额、结论或法律版本复制进新事项。

### Template Asset minimum metadata

长期模板若由 Host/用户资产层提供，至少可识别：`asset_id / name / scope / document_types / source / application_mode / status / version-or-hash`。

`application_mode` 可区分：`STRICT_STRUCTURE / GUIDED_STRUCTURE / STYLE_REFERENCE`。STRICT_STRUCTURE 也不能覆盖现行法、官方格式或事实状态纪律。

### Persistence boundary

爽律只规定如何解析和使用 legal-work preference/template，不自称拥有长期文件存储。Host 无持久化能力时，提示用户把模板保存在其项目、云盘或可复用资产位置；不得假装已经长期记住二进制模板。

## Preference State / User Operations

当 Host 实际提供可读写的法律工作偏好存储时，爽律可以操作这些**法律工作偏好状态**，但不自建记忆引擎。

推荐状态：
- `ACTIVE`：已确认并生效；
- `DISABLED`：用户关闭但保留；
- `SUGGESTED`：仅推测到可能偏好，未确认、不生效；
- `DEPRECATED`：旧设置已被新设置替代；
- `ORPHANED`：新版无对应能力，保留但不生效；
- `BLOCKED_BY_GUARDRAIL`：与硬边界冲突，记录保留但禁止生效；
- `REVIEW_REQUIRED`：迁移或冲突无法自动判断。

只有用户明确长期指令、用户导入的偏好档案或可验证的旧版迁移结果才能直接进入 ACTIVE；单次风格表现和模型猜测不得静默激活。

在 Host 能力允许时，用户可要求：列出当前法律工作偏好、关闭某项、恢复版本默认、只保留某类偏好、导出偏好、检查冲突/废弃项。体检只能提出清理建议，不得未经用户确认删除 ACTIVE 设置。

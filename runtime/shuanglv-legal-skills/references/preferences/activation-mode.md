# Preference｜Activation Mode

`unit_id: unit.preference.activation`

**Scope：** AUTO/CONFIRM/MANUAL legal-skill invocation preference.

## Trigger
- Activation mode must be interpreted or current task override conflicts with stored default.

## Negative Trigger
- General personality setting.

## Essential Procedure
1. Apply AUTO/CONFIRM/MANUAL to skill invocation UX.
2. Current explicit task instruction overrides stored activation default.

## Exit Sufficiency
- Current task activation state is resolved.

## Professional Results
- task-level activation decision

## Explicit Invocation / Preservation

- `MANUAL` 只关闭无感自动激活，不关闭用户当前明确说“调用爽律 / 用爽律处理 / ShuangLaw”的显式调用；
- `CONFIRM` 只在自动识别边界任务时要求确认，不应把已经明确的用户调用再变成重复确认；
- 已确认的 AUTO / CONFIRM / MANUAL 偏好属于可迁移 legal-work preference，版本升级默认 PRESERVE_USER；
- Host 不支持自动发现时，必须诚实降级为显式调用，不得声称自动激活已发生。

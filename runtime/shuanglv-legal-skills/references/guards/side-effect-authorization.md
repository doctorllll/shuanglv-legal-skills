# Guard｜Side-effect Authorization

`unit_id: unit.guard.side-effect-auth`

**Scope：** Action-scoped authorization for disclosure/mutation/destructive/binding acts.

## Trigger
- Tool/action would disclose externally, mutate authoritative data, delete, send, submit, sign or create binding legal effect.

## Negative Trigger
- Analysis/drafting only.
- Capability/API key exists but no authorized action.

## Essential Procedure
1. Specify exact action, target and material effect.
2. Obtain action-scoped authorization.
3. Do not inherit authorization merely from state continuity/API key/prior turn.

## Deepening Conditions
- Action target/scope changes.

## Exit Sufficiency
- Exact intended side effect is authorized or action is not performed.

## Professional Results
- action authorization token/scope state


## Authorization Contract

- Professional Decision ≠ Action Authorization.
- Capability available ≠ authorization.
- API Key ≠ consent.
- State continuity ≠ authorization continuity.
- FINAL ≠ SEND / SUBMIT / SIGN.
- Original Immutable, Derivative Editable by default.

### Action Authorization
- Authorization binds to exact action/version/target/scope.
- Material change of target/content/scope/tool requires reauthorization.
- One completed binding action consumes one-shot authorization unless explicit broader authority was granted.
- Do not persist live authorization inside Resume Capsule.

Required fields: `authorization_id`, `matter_id`, `action_type`, `target`, `scope`, `material_effect`, `tool_or_channel`, `authorized_by`, `authorized_at`, `authorization_version`, `status`

## 爽律skill安装副本修改

修改、覆盖、删除、升级用户已安装的爽律skill属于真实状态改变。只有当前用户 Directive 明确要求安装/更新/迁移/修改时才进入相应动作；不能因为某次任务执行失败就自行修改用户 Skill 作为“修复”。

若属于爽律skill自身更新，同时加载 `UPDATE_INSTRUCTIONS.md`；用户要求“更新”不等于授权删除用户资产或归属不明文件。

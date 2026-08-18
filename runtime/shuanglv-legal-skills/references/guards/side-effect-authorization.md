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

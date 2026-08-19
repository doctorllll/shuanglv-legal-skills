# Preference｜Legal Work

`unit_id: unit.preference.legal-work`

**Scope：** Long-term legal-work configuration and deliverable preferences only; not general personality or a memory engine.

## Trigger
- A legal task can reuse confirmed lawyer/team preferences, templates, verification standards, source preferences, jurisdiction defaults or handling boundaries.
- Current directive conflicts with or temporarily overrides a stored legal-work preference.
- User asks to inspect, export, disable, update or migrate legal-work settings.

## Negative Trigger
- General chat personality or unrelated lifestyle preference.
- Case-specific facts/evidence that belong to Matter State.
- One-off stylistic behavior that has not been confirmed as a long-term preference.

## Essential Procedure
1. Resolve the minimum relevant `LegalWorkProfile` fields for the current task.
2. Apply precedence without allowing preferences to override hard professional or security boundaries.
3. Reuse confirmed configuration before asking; ask only for a missing field that can materially change the result.
4. Keep Matter-specific facts and current instructions out of long-term profile storage unless they are legitimate reusable preferences.

## Exit Sufficiency
- Relevant preference/profile field is applied, explicitly absent, or truthfully unavailable from the current Host.

## Professional Results
- legal-work preference projection
- `LegalWorkProfile` projection/update request

# LegalWorkProfile｜统一长期执业配置

`LegalWorkProfile` 只保存**跨事项可以合法复用**的律师/团队工作设置。它不保存案件事实真值，不替代 Matter State，不等于 Host 已经具有长期记忆或数据库。

## 1. Profile layers

配置按层分开，避免把长期习惯、业务领域偏好和单案状态混在一起：

1. **Global / Team**：律师或团队长期通用配置；
2. **Domain Override**：刑事、民商、合同、尽调等业务领域的增量配置；
3. **Matter Override**：仅对当前事项生效的覆盖；
4. **Current Directive**：用户当前任务的明确指令，只对当前范围生效。

统一优先级：

`Hard Guardrails > Current Directive > Matter Override > Domain Override > Global / Team > Version Default`

当前指令也不能覆盖事实真实性、来源追溯、现行法真实性、敏感材料授权、Reserved Human Decision 或 Side-effect Authorization 等硬边界。

## 2. Minimum profile contract

Host 若提供可持久化设置，可使用下列字段；没有持久化能力时只做当次投影，不得声称“已经长期记住”。

- `profile_id`：稳定标识；
- `profile_scope`：`USER / TEAM`；
- `default_jurisdiction`：默认法域，仅在当前事项未明确指定时补缺；
- `legal_source_preferences`：信源/数据库/官方来源/知识库的用户偏好或排除项；可以记录用户明确指定的 Provider，但核心规则不得自行制造品牌默认；
- `verification_standard`：事实、法律、案例、来源的默认核验强度；
- `deliverable_preferences`：篇幅、标题、结论呈现、研究深度、格式、House Style 等；
- `template_refs`：可复用模板资产引用；
- `sensitive_material_policy`：脱敏、最少披露、本地优先等长期处理偏好；
- `external_processing_preference`：例如“优先本地/必要时询问/默认不外发”等偏好，**不构成对某次敏感材料外发的授权**；
- `human_confirmation_boundaries`：用户/团队希望额外确认的高成本、高风险或重要节点；不得把它扩张为每一步都确认；
- `domain_overrides`：各业务领域只保存相对 Global / Team 的增量配置；
- `status`：`ACTIVE / DISABLED / SUGGESTED / DEPRECATED / ORPHANED / BLOCKED_BY_GUARDRAIL / REVIEW_REQUIRED`；
- `source_or_provenance`：明确用户指令、导入配置或可验证迁移来源；
- `version_or_hash`；
- `updated_at`。

### legal_source_preferences 的边界

该字段表达“用户/团队如何选信源”，不是爽律skill 自身数据库清单。选择时至少考虑：
- 用户明确指定/排除；
- 是否能完成所需 capability；
- 原始性、可核验性与法律权威层级；
- 法域、时间和内容覆盖；
- 当前权限/可访问性；
- 成本、隐私和授权边界。

新增数据库或知识库 Provider 不应新增爽律skill 核心法律规则。

## 3. Lazy acquisition｜禁止冷启动长问卷

不得首次使用就强迫用户填写完整 profile。优先顺序：

`已有确认配置 → 当前事项/模板可直接读取的设置 → 当前明确指令 → 仅在 materially necessary 时询问最小缺口`

- 能从现有配置或用户资产读取的，不重复问；
- 可以安全沿用 Version Default 的，不为了“完整资料”提问；
- 只有缺失值会实质改变当前结果且无法自行恢复时，才询问；
- 模型推测只能进入 `SUGGESTED`，不得静默变成 `ACTIVE`。

## 4. Template Asset minimum metadata

长期模板若由 Host/用户资产层提供，至少可识别：`asset_id / name / scope / document_types / source / application_mode / status / version-or-hash`。

`application_mode` 可区分：`STRICT_STRUCTURE / GUIDED_STRUCTURE / STYLE_REFERENCE`。STRICT_STRUCTURE 也不能覆盖现行法、官方格式或事实状态纪律。

用户当前任务明确指定模板/风格时，只影响其指定范围；找不到用户模板时不得声称“已按你的模板完成”。用户模板只能提供结构/样式/表达参照，不能把旧案件的事实、主体、金额、结论或法律版本复制进新事项。

## 5. Persistence boundary

爽律skill 只规定如何解析、投影和更新 legal-work preference，不自建记忆引擎。

- Host 无持久化能力时，提示用户把模板/配置保存在其项目、云盘或可复用资产位置；
- 不得假装已经长期记住二进制模板或配置；
- 不得在长期偏好里保存具体案件事实、证据原文、客户秘密或无必要敏感信息；
- Matter 信息保持 Matter scope。

## 6. Preference State / User Operations

当 Host 实际提供可读写的法律工作偏好存储时，用户可以要求：列出当前偏好、关闭某项、恢复版本默认、只保留某类偏好、导出 profile、检查冲突/废弃项或更新某个字段。

只有用户明确长期指令、用户导入的偏好档案或可验证的旧版迁移结果才能直接进入 `ACTIVE`；体检只能提出清理建议，不得未经用户确认删除 ACTIVE 设置。

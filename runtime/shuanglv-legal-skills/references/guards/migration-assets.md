# Guard｜Migration Assets

`unit_id: unit.guard.migration-assets`

**Scope：** User legal asset migration guard.

## Trigger
- Upgrade/migration changes physical paths or defaults for user templates/House Style/legal assets.

## Negative Trigger
- No migration or user asset involved.

## Essential Procedure
1. Resolve old path via stable ID.
2. Preserve user asset unless explicitly replaced.
3. Do not infer general persona from legal-work assets.

## Deepening Conditions
- Path/schema change.

## Exit Sufficiency
- All user assets have preserved mapping or explicit replacement decision.

## Professional Results
- stable asset mapping

## Preservation Rules

升级默认策略：**PRESERVE_USER**。

- 新版默认模板/样式不得静默覆盖、替换或删除用户已有模板与已确认 Legal Work Preference；
- 设置或资产废弃时保留可识别记录并提供迁移/替代说明，不把路径变化解释为资产不存在；
- 与硬规则冲突时只阻止冲突部分生效，资产本身仍保留；
- Host 无法持久迁移时，明确要求导出/导入或由用户资产系统保存，不伪称已迁移；
- 不得在用户级长期偏好中保存具体案件事实、证据原文、客户秘密或无必要敏感信息；Matter 信息必须保持 Matter scope。

迁移需要覆盖/替换现有用户资产时，必须有显式决定；API Key、文件存在或旧版本路径存在均不构成替换授权。

## 爽律skill自身更新的特别规则

当任务是安装、升级、更新、迁移或替换爽律skill自身运行层时，本文件不单独决定删除范围，必须先加载根目录 `UPDATE_INSTRUCTIONS.md`：

- 官方程序层与用户层先分离；
- `UNKNOWN = PRESERVE`；
- 未完成资产清单、备份/迁移和可读取验证前，不得递归删除整个安装目录；
- 更新后必须核验用户模板、偏好/配置、Matter/Resume 与用户自建文件；
- 资产恢复/验证失败时保留备份并阻断“更新成功”声明。

# 爽律用户空间模板

本目录只是**模板**，不是用户真实个性化数据。

正式安装建议在爽律 Skill Core 的同级位置单独建立 `爽律用户空间/`，不要把真实用户设置写进 Core 包。本模板可用于初始化：

```text
爽律用户空间/
├─ user-profile.json
├─ matters/
├─ custom-rules/
├─ custom-templates/
├─ snapshots/
├─ migrations/
└─ legacy-customizations/
```

支持 Python 的环境可运行：

```text
python "05_工程执行层/工具/爽律升级助手.py" init --user-space "../爽律用户空间"
```

平台不支持持久文件时，可导出/导入个性化包，但系统不得宣称已经自动持久保存。


## 模板资产

用户自己的正式模板属于 Personalization Layer，不属于可被版本升级覆盖的 Core。建议在用户空间增加：

```text
├─ template-assets.json
└─ custom-templates/
```

`template-assets.json` 只登记模板元数据和适用范围，实际 DOCX/MD 等文件放在 `custom-templates/`。同一文种存在多个模板时，优先级为：当前事项明确指定 > 事项/客户项目模板 > 用户长期模板 > 爽律版本默认。找不到用户模板时必须说明，不得静默改用系统模板并声称仍按用户模板执行。

跨环境导入发生同路径模板冲突时，默认保留当前用户空间中的版本；只有用户明确选择时才可采用传入模板覆盖。


## v0.43 激活偏好

用户可在 `user-profile.json` 的 `settings` 中显式保存 `activation.mode`（AUTO / CONFIRM / MANUAL）、`activation.show_notice` 等。未显式保存时使用当前版本默认；一旦用户确认并保存，后续升级按 `PRESERVE_USER` 继承。

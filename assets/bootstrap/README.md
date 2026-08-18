# 爽律用户空间 Bootstrap（示例）

本目录仅提供初始化示例，不包含真实用户数据，也不意味着爽律自身拥有 Memory Engine。

Host 如果支持持久化，可将用户明确确认的合法偏好、模板资产和 Matter 续接信息保存在 Host 的用户空间；不支持持久化时必须如实说明。

推荐逻辑分离：`user-profile.json`（偏好状态）/ `template-assets.json`（模板登记）/ `custom-templates/`（实际模板）/ `matters/`（Host-managed Matter data）。Core 升级不得静默覆盖这些用户资产。

# 维护说明（仓库层）

本仓库由 v0.48 正式运行包和仓库治理层组成。

## 分层

| 层 | 内容 | 升级方式 |
|---|---|---|
| 正式运行层 | `runtime/shuanglv-legal-skills/`、`PACKAGE_MANIFEST.json`、`docs/`、`assets/bootstrap/`、根目录许可证与说明 | 以经过验收的正式成果包整体替换 |
| 仓库治理层 | `.github/`、`assets/brand/`、README/CONTRIBUTING 仓库附录、CHANGELOG.md、`.gitignore` 补充段 | 保留并在新版本上重新套用 |

## 升级规则

1. 先检查正式包版本、发布状态、清单哈希和文档一致性。
2. 移除旧正式运行层，保留 `.github/`、`assets/brand/` 和 Git 历史。
3. 导入正式包，不导入开发包及研发材料。
4. 运行 `.github/scripts/apply_repo_layer.py`，再检查路径、JSON、敏感信息和许可证残留。
5. 更新 `CHANGELOG.md`，提交并打对应版本 tag。

当前根目录许可证为 **ShuangLaw Professional Use License 1.0**。不得重新加入 v0.43 的 CC BY-SA 4.0 / Apache-2.0 许可证文件或表述。

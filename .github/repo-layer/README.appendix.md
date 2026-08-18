<!-- repo-appendix:start ｜ 仓库层，由 .github/scripts/apply_repo_layer.py 生成；不要手改本段。以上为作者 README 正文。 -->

---

## 附：仓库层说明

本仓库的 v0.48 正式运行层位于 `runtime/shuanglv-legal-skills/`。安装时应将仓库作为整体提供给 Agent，并以该目录下的 `SKILL.md` 作为运行入口。

### 目录结构

```text
.
├── runtime/shuanglv-legal-skills/  # 唯一正式运行层
├── docs/                           # 用户指南、安装、反馈与许可说明
├── assets/bootstrap/               # 不含真实用户数据的初始化示例
├── assets/brand/                   # 爽律品牌资源，不在许可证授权范围内
├── PACKAGE_MANIFEST.json           # 正式成果包清单
└── .github/                        # 仓库治理、模板与维护脚本
```

### 安装

```bash
git clone https://github.com/zj-ai-lab/shuanglv-legal-skills.git
```

宿主应读取 `runtime/shuanglv-legal-skills/SKILL.md`，并按需访问同目录的 `references/`。`docs/`、开发包和测试材料不得作为 Runtime 常驻指令加载。

### 版本与历史

当前 `main` 为 v0.48 正式架构。v0.43 及更早版本保留在 Git tag 和历史提交中，可通过对应 tag 下载。

### 许可

v0.48 适用根目录 `LICENSE` 所载的 **ShuangLaw Professional Use License 1.0**。`assets/brand/` 品牌标识另受权利人控制。

<!-- repo-appendix:end -->

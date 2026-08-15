# 维护说明（仓库层）

本仓库 = **作者交付的爽律 Skill 版本（原样）** + **仓库层**。两层分开维护，升级新版时不手工合并作者文件。

## 分层

| 层 | 内容 | 谁维护 | 升级时 |
|---|---|---|---|
| 作者层 | 除下列仓库层文件外的一切：`SKILL.md`、`manifest.json`、`00`–`05` 目录、`LICENSE*`、`NOTICE`、`许可与使用声明.md`、`公开共创版本说明.md`、`系统说明.md`，以及 `README.md` / `CONTRIBUTING.md` / `.gitignore` 的**作者正文部分** | 作者（蔡诗爽律师）；社区 PR 经作者终审后并入 | 整体以新版替换 |
| 仓库层 | `.github/`、`assets/`、`CHANGELOG.md`；`README.md` 的头部（`repo-header`）与文末附录（`repo-appendix`）；`CONTRIBUTING.md` 文末附录；`.gitignore` 的"仓库层补充"段 | 仓库维护者 | 重新套在新版作者文件上 |

`README.md` / `CONTRIBUTING.md` / `.gitignore` 里仓库层片段都用 `<!-- repo-header:start/end -->`、`<!-- repo-appendix:start/end -->`、`# --- 仓库层补充 ---` 标出。

## 升级作者新版本的步骤

1. 拿到作者新版文件夹 `SRC`，先与上一 tag 全量 diff，看新增 / 删除 / 修改，重点看 `manifest.json`、许可文件、`SKILL.md`、`README.md`、`CONTRIBUTING.md`；
2. 跑一遍脱敏与凭证扫描（命令见 `CONTRIBUTING.md` 7.4）；
3. 删除工作树中作者层旧文件（保留 `.github/`、`assets/`、`CHANGELOG.md`），`rsync -a --exclude .DS_Store SRC/ ./`；`diff -rq SRC . -x .git -x .github -x assets -x CHANGELOG.md` 必须 IDENTICAL；
4. 提交「升级到 vX.Y（作者原始交付逐字节导入）」并打 tag `vX.Y`；
5. 把仓库层重新套上：README 头部 + 附录、CONTRIBUTING 附录、`.gitignore` 补充段；更新徽章版本号、附录里的结构树与 `CHANGELOG.md`；
6. 第二个提交「仓库层：套用于 vX.Y」，推送。

## 分支保护

`main` 使用 `.github/rulesets/protect-main.json`（禁删除 / 禁强推 / 须 PR + 1 个批准 + CODEOWNERS 审查 / squash 合并；管理员可绕过）。作者交付版本的导入由维护者以管理员身份直接推送到 `main`，社区改动一律走 PR。

启用 / 更新规则集（免费账号仅公开仓可用）：

```bash
gh api -X POST repos/doctorllll/shuanglv-legal-skills/rulesets \
  -H "Accept: application/vnd.github+json" \
  --input .github/rulesets/protect-main.json
```

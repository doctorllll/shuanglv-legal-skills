# 维护说明（仓库层）

本仓库 = **作者交付的爽律 Skill 版本（原样）** + **仓库层**。两层分开维护，升级新版时不手工合并作者文件。

## 分层

| 层 | 内容 | 谁维护 | 升级时 |
|---|---|---|---|
| 作者层 | 除下列仓库层文件外的一切：`SKILL.md`、`manifest.json`、`00`–`05` 目录、`LICENSE*`、`NOTICE`、`许可与使用声明.md`、`公开共创版本说明.md`、`系统说明.md`，以及 `README.md` / `CONTRIBUTING.md` / `.gitignore` 的**作者正文部分** | 作者（蔡诗爽律师）；社区 PR 经作者终审后并入 | 整体以新版替换 |
| 仓库层 | `.github/`、`assets/`、`CHANGELOG.md`；`README.md` 的头部（`repo-header`）与文末附录（`repo-appendix`）；`CONTRIBUTING.md` 文末附录；`.gitignore` 的"仓库层补充"段 | 仓库维护者 | 重新套在新版作者文件上 |

`README.md` / `CONTRIBUTING.md` / `.gitignore` 里仓库层片段都用 `<!-- repo-header:start/end -->`、`<!-- repo-appendix:start/end -->`、`# --- 仓库层补充 ---` 标出；它们由 `.github/scripts/apply_repo_layer.py` 从 `.github/repo-layer/` 模板生成。作者以 PR 提交新版时若整体覆盖了 README / CONTRIBUTING，不必在 PR 里修，合并后维护者跑一次脚本即可。

## 升级作者新版本的步骤

1. 拿到作者新版文件夹 `SRC`，先与上一 tag 全量 diff，看新增 / 删除 / 修改，重点看 `manifest.json`、许可文件、`SKILL.md`、`README.md`、`CONTRIBUTING.md`；
2. 跑一遍脱敏与凭证扫描（命令见 `CONTRIBUTING.md` 7.4）；
3. 删除工作树中作者层旧文件（保留 `.github/`、`assets/`、`CHANGELOG.md`），`rsync -a --exclude .DS_Store SRC/ ./`；`diff -rq SRC . -x .git -x .github -x assets -x CHANGELOG.md` 必须 IDENTICAL；
4. 提交「升级到 vX.Y（作者原始交付逐字节导入）」并打 tag `vX.Y`；
5. 运行 `python3 .github/scripts/apply_repo_layer.py` 把仓库层套回（README 头部 + 附录、CONTRIBUTING 附录、`.gitignore` 补充段；版本 / 阶段徽章自动取自 `manifest.json`；可重复运行）。要改头尾内容，改 `.github/repo-layer/` 下的模板再运行脚本，**不要直接改 README / CONTRIBUTING 里的仓库层片段**。然后更新 `CHANGELOG.md`；
6. 第二个提交「仓库层：套用于 vX.Y」，推送。

## 归属与权限

仓库归 GitHub 组织 **`zj-ai-lab`**（2026-08-16 自 `doctorllll` 转入，同日由 `shuanglaw` 改名；旧地址自动重定向）。组织 Owner = 全部仓库管理员；作者 @csslaw 与维护者 @doctorllll 均应为 Owner。作者交付版本既可由维护者按下文步骤直接导入，也可由作者自己以 PR 形式提交（如 v0.41 的 PR #2）——后者合并后维护者仍需补做第 5–6 步（把仓库层套回去、更新徽章版本与 CHANGELOG）。

## 分支保护与提交约定

`main` 上有两条规则集（JSON 在 `.github/rulesets/`）：

| 规则集 | 内容 | 谁能绕过 |
|---|---|---|
| `main-guard` | 禁止删除 `main`、禁止强推（改写历史） | **没有人**——Owner 也不能 |
| `require-pr` | 改动须经 PR + 1 个批准 + CODEOWNERS 审查，squash 合并 | 组织 Owner / 仓库管理员（作者与维护者） |

由此形成三档：

1. **Owner（作者 @csslaw、维护者 @doctorllll）——可直接提交到 `main`，不需要互相审批。** 推送时 GitHub 会回一行 "Bypassed rule violations"，属正常。可以选择开 PR 再自己合并（`gh pr merge --squash --admin`），只是为了留一条改动说明，不是必须。
2. **其他维护者（将来加入的管理员）**——加为组织成员并放进 `maintainers` team、给仓库 Maintain 角色：能审、能合并他人的 PR、能管 Issue，但不能绕过规则集，一律走 PR；**不要再增加 Owner**。
3. **社区贡献者**——Fork → PR → 维护者初审 → 涉及业务规则的等作者批准 → squash。

Owner 直接提交时的几条约定（不是技术限制，是彼此的默契）：

- **地盘**：法律业务内容（`SKILL.md`、`manifest.json`、`00`–`05` 目录、许可与说明文件）是作者的；仓库层（`.github/`、`assets/`、`CHANGELOG.md`、README / CONTRIBUTING 头尾模板）是维护者的。改自己的地盘直接推；要改对方地盘，先打个招呼或开个 PR 让对方看一眼再合。
- **推前先拉**：`git pull --rebase origin main` 再 push；两人同时改到同一文件时以作者的业务内容为准。
- **动了作者的 README / CONTRIBUTING / .gitignore 后**，运行 `python3 .github/scripts/apply_repo_layer.py` 再提交，头尾不会丢。
- **作者升版本**（改 `manifest.json` 的 `version`）时打同名 tag（`git tag -a vX.Y -m … && git push origin vX.Y`），并在 `CHANGELOG.md` 记一段；维护者看到没打的会补。
- **绝不** `git push --force` 到 `main`（规则集也不允许）；改错了用新提交修正。

启用 / 更新规则集：

```bash
gh api -X PUT  repos/zj-ai-lab/shuanglv-legal-skills/rulesets/20885834 -H "Accept: application/vnd.github+json" --input .github/rulesets/require-pr.json
gh api -X POST repos/zj-ai-lab/shuanglv-legal-skills/rulesets          -H "Accept: application/vnd.github+json" --input .github/rulesets/main-guard.json
```

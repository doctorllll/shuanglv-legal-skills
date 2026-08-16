<!-- repo-appendix:start ｜ 仓库层，由 .github/scripts/apply_repo_layer.py 从 .github/repo-layer/CONTRIBUTING.appendix.md 生成；不要手改本段。以上为作者原文。 -->

---

## 七、仓库操作细则（维护者补充）

以上一至六节是作者对"贡献什么、质量要求、许可与隐私"的规定，以其为准。本节只补充在 GitHub 仓库里**怎么操作**。

### 7.1 两条路径

- **开 Issue（无需 Git）**：[New issue](../../issues/new/choose) 选模板——「真实失败反馈」「问题反馈」「提案」；模板字段就是第三节要求的说明结构。
- **Pull Request**：Fork → 从 `main` 切分支（建议 `fix/…`、`docs/…`、`skill/…`、`schema/…`）→ 修改 → 过一遍 PR 模板自检 → 发起 PR。小改动一个 PR 一件事；新技能、新模块、不向后兼容的 schema 变更请先开「提案」Issue 讨论范围与边界。

### 7.2 目录与联动更新

- 业务技能目录标准文件：`技能定义` / `详细说明与工作流程` / `分析与推理方法` / `核心规则汇总` / `检查清单汇总` / `对抗性审查清单`，可选 `业务模块汇总` 与 `数据结构/`。
- **新增或重命名技能时须同步**：`manifest.json`（`skills` / `optional_skills`）、`00_使用与调度/技能总览.md`、`00_使用与调度/技能调度规则.md`、README 技能表，以及 `05_工程执行层/配置/` 下按技能名索引的 `加载清单.json` 与 `动态清单注册表.json`。
- 平台适配只改入口与能力声明（`SKILL.md`、`01_运行规范/` 能力契约），不为适配平台改法律业务规则本身。

### 7.3 JSON Schema 约定

- JSON Schema 2020-12；每个 schema 带 `$id`（`https://legal-skill.local/schema/<name>/<major.minor>`）与 `title`，顶层 `schema_version` 用 `const` 锁定。
- **不向后兼容的改动必须递增 `$id` 与 `schema_version` 版本号**，并在 PR 中说明迁移方式；跨技能共享的放 `02_公共接口/数据结构/`，仅某技能使用的放该技能的 `数据结构/`。
- 程序性文件（`.py` / `.json` / schema）按 Apache-2.0；改动执行器请保持"仅标准库、不联网、不写入仓库外路径"。

### 7.4 写作与脱敏自查

- 说明正文统一用"爽律 Skill"，只有用户调用示例中才单用"爽律"；简体中文，术语与现行法律法规一致。
- 提交前自查（PR 模板里也有）：

```bash
grep -rnoE '[（(][12][0-9]{3}[）)][^号]{1,30}号' .            # 真实案号
grep -rnoE '\b[0-9]{17}[0-9Xx]\b|\b1[3-9][0-9]{9}\b' .      # 身份证 / 手机号
grep -rnoiE '(sk|key|token|secret)[-_ ]?[a-z0-9]{20,}' .      # 凭证
```

如已误提交真实材料，请立即联系维护者——公开仓库需要重写历史才能真正抹除。

### 7.5 评审与发布

1. 维护者初审：结构、格式、脱敏、平台适配、联动文件是否同步；
2. 作者终审：凡涉及法律业务规则、门控、对抗性审查点、人工升级边界的改动；有分歧以作者意见为准；
3. 通过后 squash 合并到 `main`，记入 `CHANGELOG.md`；`main` 受分支保护，不接受直接推送；
4. 作者交付的每个版本按原样导入（或由作者自提 PR 合并）并打 tag；仓库层（README / CONTRIBUTING 头尾、`.github/`、`CHANGELOG.md`）与作者正文分层维护，合并作者新版后运行 `python3 .github/scripts/apply_repo_layer.py` 即可套回，见 `.github/MAINTAINING.md`。

<!-- repo-appendix:end -->

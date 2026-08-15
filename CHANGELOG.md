# 版本记录 · Changelog

本文件记录 **爽律 Skill｜律师专业工作流系统** 的版本变化。版本号沿用作者的 `manifest.json` 中的 `version`；仓库层（README / CONTRIBUTING / 模板）的变化单独列出，不改变系统版本号。

---

## [未发布]

### 仓库层
- 新增仓库级 `README.md`（保留作者原 README 全部实质内容，增加安装、仓库结构、参与共创、版本路线、许可状态等章节；作者原 README 见 tag `v0.33`）。
- 新增 `CONTRIBUTING.md`、`CHANGELOG.md`、`.github/`（Issue / PR 模板、CODEOWNERS）、`.gitignore`。
- 未新增 `LICENSE` 文件：公开版许可待作者确认（见 README 第十一节）。
- README 融入作者个人主页「爽律刑法空间」（csslaw.cn）与作者简介；GitHub 仓库 homepage 指向该主页。
- 新增 `assets/brand/`：作者主页的「爽律」品牌标识（日/夜两版，透明底），README 头部按明暗主题自动切换；标识不在仓库许可范围内，见目录内说明。
- 加入 `.github/rulesets/protect-main.json`（main 分支保护规则集，转公开后启用）。

### 待作者确认后进行
- 更新 `manifest.json`（`release_stage` / `license_status`）与 `SKILL.md`、`内测版本提示.md`、`许可与使用声明.md`、`00_使用与调度/爽律 Skill入口.md`、`00_使用与调度/快速上手.md` 中的版本状态措辞。
- 为 `SKILL.md` 补充 YAML frontmatter（`name` / `description`），不改业务规则。

---

## [0.33] — 内测版（仓库基线）

- 作者交付的 v0.33 内测版原始内容逐字节导入，未作任何修改。tag：`v0.33`。
- 包含 8 个业务技能（法律研究与多源资料融合、刑事案件办理、民商事争议解决、合同与交易工作、法律顾问与专项法律分析、尽职调查与专项调查、法律文书质量与格式控制、多模态输入适配（可选））、17 个公共数据结构、3 个使用示例。
- 系统标识 `shuanglv-legal-skills`；作者：卓建律师事务所 蔡诗爽律师。

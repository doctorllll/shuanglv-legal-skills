<!-- repo-appendix:start ｜ 仓库层，由 .github/scripts/apply_repo_layer.py 从 .github/repo-layer/README.appendix.md 生成；不要手改本段。以上为作者 README 正文。 -->

---

## 附：仓库层说明

> 本节由仓库维护者维护，说明"怎么装、仓库怎么组织、谁来评审"。系统本身的规则、许可与专业边界，以上文作者正文和 `许可与使用声明.md` 为准。

### 安装

作者对"安装成功"的定义（`00_使用与调度/安装与调用说明.md`）是：Agent 能访问**完整**系统；能把 `SKILL.md` 或《爽律 Skill入口》作为入口；用户说"爽律"时能路由到入口；入口能继续读取 `00`–`05` 目录。因此**不拆分、不删减**，把整个仓库作为一个目录交给 Agent 即可。

| 平台 | 常见放置位置（以各平台官方文档为准） |
|---|---|
| Claude Code | `~/.claude/skills/shuanglv-legal-skills/`（项目级可放 `.claude/skills/`） |
| Codex CLI | `~/.codex/skills/shuanglv-legal-skills/` |
| Hermes Agent | `~/.hermes/skills/shuanglv-legal-skills/` |
| OpenClaw | 工作区 `skills/shuanglv-legal-skills/` |
| Cursor / Trae / 其它 IDE Agent | 作为项目目录或规则文件加载，并在系统指令中注册别名（见下） |
| Coze / Dify / 企业知识库类平台 | 作为"项目文件 / 知识文件 / Workspace Instructions"整体上传，选择能让 Agent **在执行时稳定读取完整目录**的机制 |

以 Claude Code 为例：

```bash
git clone https://github.com/zj-ai-lab/shuanglv-legal-skills.git ~/.claude/skills/shuanglv-legal-skills
```

可选的工程执行层（`05_工程执行层/工具/爽律 Skill执行器.py`）只依赖 Python 标准库；没有 Python 的环境直接按规则文档执行即可，不影响核心 Skill。

**平台不能自动识别入口时**：当前 `SKILL.md` 是纯 Markdown 入口、未附带 YAML frontmatter（`name` / `description`），部分平台可能不会把它自动列为可触发技能。此时按作者《安装与调用说明》第五节，在平台的系统指令 / 项目规则（如 `CLAUDE.md`、`AGENTS.md`）中加入一句：

> 当用户说"调用爽律""用爽律做""用爽律处理"时，读取 `<安装路径>/SKILL.md` 并按其中规则执行。

### 仓库结构（v{{VERSION}}）

```text
.
├── SKILL.md                     # Agent 机器入口
├── manifest.json                # 系统元数据：system_id / version / skills / 各策略文件指针 / 许可
├── 系统说明.md · 公开共创版本说明.md · 许可与使用声明.md
├── LICENSE · LICENSE-CC-BY-SA-4.0.txt · LICENSE-APACHE-2.0.txt · NOTICE
├── 00_使用与调度/               # 入口、路由、调度、对抗性审查、人工升级、法律分析与推理、全链路溯源、
│                                #   跨模块执行与回写、事项工作模型、事项快速理解与图形化交付、测试基线与能力边界 等规范
├── 01_运行规范/                 # 输入质量、运行能力契约、外部能力适配、法律信源 / 用户知识库 /
│                                #   文件多模态 / 交付工具 / 图形化交付能力契约、能力降级与失败处理 等
├── 02_公共接口/                 # 公共接口规范 + 跨技能共享的 JSON Schema（2020-12）
├── 03_技能/                     # 8 个业务技能（见下）
├── 04_使用示例/                 # 端到端示例（部分附 JSON 对象示例）
├── 05_工程执行层/               # 可选：渐进式加载 / 动态清单 / 质量门控规则、配置 JSON、执行器 .py、示意图 HTML 模板、schema
├── assets/brand/                # 「爽律」品牌标识（作者所有，不随仓库许可开放）
├── CONTRIBUTING.md              # 作者的共创与贡献指南（+ 维护者补充的仓库操作细则）
├── CHANGELOG.md                 # 版本记录（仓库层维护）
└── .github/                     # Issue / PR 模板、CODEOWNERS、分支保护规则集、仓库层模板与脚本、维护说明
```

每个业务技能目录：

```text
03_技能/<技能名>/
├── 技能定义.md              # Agent 调用条件、边界、输入输出和总流程（含 skill_id）
├── 详细说明与工作流程.md      # 给人看的完整方法地图
├── 分析与推理方法.md         # 该技能的横向分析与推理闭环（v0.40 新增）
├── 核心规则汇总.md           # 必须遵守的规则、门控和禁止事项
├── 检查清单汇总.md           # 执行完成前的质量控制
├── 对抗性审查清单.md         # 该技能专属的第二遍审查
├── 业务模块汇总.md           # 每一步具体如何执行（部分技能）
└── 数据结构/                # 该技能扩展的 JSON Schema（部分技能）
```

### 关于作者

**蔡诗爽**，广东卓建律师事务所专职律师，深圳刑事辩护律师，2017 年起执业，专注刑事控告与刑事案件全流程辩护，核心领域为诈骗类犯罪、商标类知识产权刑事犯罪、虚拟货币相关刑事犯罪、印章与国家机关证件类刑事犯罪；广东省刑事辩护律师库首批入库律师，深圳市律师协会数字经济法律专业委员会副秘书长；参与撰写"深圳律师实务丛书"《元宇宙法律实务》（法律出版社）。

爽律 Skill 的系统设计、全部业务规则与工作流均由蔡律师完成，蔡律师亦是本仓库**法律业务规则的终审人**。他的个人主页 **[爽律刑法空间 · csslaw.cn](https://csslaw.cn/)** 收录了刑事观察文章、亲办案例节选与刑事实务工具（刑事程序地图、常见罪名速查），可作为理解本系统刑事工作流设计取向的延伸阅读。"爽律"既是本系统的调用简称，也是他的个人专业品牌。

### 维护、评审与反馈

- **发起及主导 / 业务规则终审**：蔡诗爽律师；
- **归属**：GitHub 组织 [`zj-ai-lab`](https://github.com/zj-ai-lab)，作者与维护者同为组织 Owner；
- **仓库维护**：[@doctorllll](https://github.com/doctorllll)——仓库结构、共创流程、平台适配与发布；
- **评审分两层**：维护者初审结构、格式、脱敏与平台适配；凡涉及法律业务规则、门控、对抗性审查点、人工升级边界的改动由作者终审；有分歧以作者意见为准；
- **反馈入口**：[Issues](../../issues/new/choose)（真实失败反馈 / 问题反馈 / 提案）与 [Discussions](../../discussions)；涉及案件材料的反馈请先按 `CONTRIBUTING.md` 第六节脱敏；
- **版本**：作者交付的每个版本按原样导入（或由作者自提 PR 合并）并打 tag（`v0.33`、`v0.40`、`v0.41` …），变更摘要见 [CHANGELOG.md](CHANGELOG.md)；维护流程见 [`.github/MAINTAINING.md`](.github/MAINTAINING.md)。

### 品牌标识

[`assets/brand/`](assets/brand/) 下的「爽律」品牌标识为蔡诗爽律师所有，**不在本仓库文本 / 代码许可范围之内**，仅用于标识本系统与作者；未经作者许可不得另作他用。

### 致谢

- Anthropic 制定并开源的 Agent Skills 规范，是本系统的组织形式基础；
- [`THUYRan/Legal-Skills-Chinese`](https://github.com/THUYRan/Legal-Skills-Chinese) 为中文法律 Agent Skills 的开放协作提供了在先实践。

<!-- repo-appendix:end -->

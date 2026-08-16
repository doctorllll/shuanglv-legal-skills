# 爽律 Skill v0.43｜正式版发布说明

> **版本：v0.43 正式版｜Agent Native｜公开共创**  
> **发布日期：2026-08-17**  
> **发起及主导：广东卓建律师事务所 蔡诗爽律师**

## 版本定位

v0.43 将爽律从“需要用户主动说调用爽律的专业 Skill”推进为更接近 Agent Native 的律师专业能力层。在支持 Agent Skills metadata 自动发现/选择的宿主中，用户直接提出实质性中国法律专业任务即可由宿主判断是否加载爽律；显式“调用爽律 / ShuangLaw”仍永久保留为兼容与保底入口。

本版本按正式版发布。后续真实用户反馈、宿主差异和新增需求进入后续版本迭代，不以“尚未覆盖所有宿主真实场景”为由长期停留在测试标签。

## v0.43 主要新增

- AutoActivation：支持法律专业任务的无感激活语义；
- Activation Preference：`AUTO / CONFIRM / MANUAL` 纳入用户个性化；
- Skill Router v2：支持 Agent Native 路由，同时保留 v0.42 旧路由回退；
- Multi-Skill Collaboration：OCR、Web、法律数据库、Office 等通过能力请求协同，不绑定厂商；
- Proactive Suggestion：仅在直接服务当前目标时提出克制建议；
- Legacy Compatibility Contract：所有 v0.43 增强能力失败时，必须退回 v0.42 已验证工作路径；
- Feature Flags：AutoActivation、Router v2、多 Skill 协同、主动建议可独立关闭；
- `GATE-LEGACY-COMPAT`：旧版可完成而新版因增强层失败无法完成，视为发布级回归缺陷。

## 兼容底线

**新功能失败，只允许损失新功能，不允许拖死旧功能。**

- 显式“调用爽律”绕过自动激活，直接进入保底路径；
- Router v2 关闭或异常时回退 v0.42 主技能路由；
- 主动建议异常时跳过建议，主任务继续；
- 多 Skill 协同不可用时优先采用既有能力适配/降级路径；
- 所有回退继续保留用户个性化、模板资产和事项设置；
- 关闭全部 v0.43 增强能力后，v0.42 原本能完成的核心任务必须仍可执行。

## 已完成工程验证

正式发布前已完成：Agent Skills frontmatter、JSON/JSON Schema、Python 编译、自动激活正反例、六大业务域路由、AUTO/CONFIRM/MANUAL、显式调用兼容、用户退出、个性化继承、模板保留、Legacy Regression、Feature Flag 故障回退、Markdown 相对链接、Core Manifest 和 ZIP 完整性检查。最终正式版验证结果见开发包。

## 宿主能力说明

自动激活最终是否由某一具体 Agent 宿主执行，仍取决于该宿主是否支持依据 Skill metadata 发现/选择 Skills。宿主不支持时，不影响爽律核心能力：用户仍可使用显式“调用爽律”或宿主自身的 Skill 绑定方式。

## 升级与个性化

升级默认 `PRESERVE_USER`。用户长期习惯、用户模板和事项模板不随 Core 更新被静默覆盖；Hard Guardrails 不允许被个性化关闭。

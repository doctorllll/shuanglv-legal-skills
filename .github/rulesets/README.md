# 分支保护规则集

`protect-main.json`：`main` 分支禁止删除、禁止强推，改动必须经 PR、至少 1 个批准、CODEOWNERS 审查、squash 合并；仓库管理员可绕过。

免费账号的私有仓库不支持规则集；仓库转公开后执行：

```bash
gh api -X POST repos/doctorllll/shuanglv-legal-skills/rulesets \
  -H "Accept: application/vnd.github+json" \
  --input .github/rulesets/protect-main.json
```

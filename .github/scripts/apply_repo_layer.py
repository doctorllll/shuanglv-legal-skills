#!/usr/bin/env python3
"""把仓库层（维护者头尾）幂等地套到作者文件上。

用法：在仓库根目录运行  python3 .github/scripts/apply_repo_layer.py
- README.md       ← .github/repo-layer/README.header.md + 作者正文 + README.appendix.md
- CONTRIBUTING.md ← 作者正文 + CONTRIBUTING.appendix.md
- .gitignore      ← 作者版本 + gitignore.appendix
模板中的 {{VERSION}} / {{STAGE_BADGE}} 取自 manifest.json。
已存在的仓库层片段（以 HTML 注释标记 / 分隔注释识别）会先剥离再重新套，因此可重复运行。
"""
from pathlib import Path
import json, re, sys, urllib.parse

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / ".github" / "repo-layer"

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
version = str(manifest.get("version", "")).strip()
stage_map = {
    "public_co_creation_testing_baseline": "公开共创版 · 实测基线",
    "public_co_creation_pretest_candidate": "公开共创版 · 实测候选基线",
    "internal_beta": "内测版",
}
stage_text = stage_map.get(manifest.get("release_stage", ""), manifest.get("release_stage", "公开共创版"))
stage_badge = urllib.parse.quote(stage_text, safe="").replace("-", "--").replace("_", "__")

def render(name: str) -> str:
    t = (TPL / name).read_text(encoding="utf-8")
    return t.replace("{{VERSION}}", version).replace("{{STAGE_BADGE}}", stage_badge)

def strip_block(text: str, start_marker: str, end_marker: str) -> str:
    return re.sub(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}\n?", "", text, flags=re.S)

# README
readme = (ROOT / "README.md").read_text(encoding="utf-8")
body = strip_block(readme, "<!-- repo-header:start", "<!-- repo-header:end -->")
body = strip_block(body, "<!-- repo-appendix:start", "<!-- repo-appendix:end -->").strip("\n")
if not re.search(r"(?m)^\s*# ", body):
    sys.exit("README.md 作者正文应以 H1 开头，请检查")
(ROOT / "README.md").write_text(render("README.header.md").rstrip("\n") + "\n\n" + body + "\n\n" + render("README.appendix.md").rstrip("\n") + "\n", encoding="utf-8")

# CONTRIBUTING
contrib = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
cbody = strip_block(contrib, "<!-- repo-appendix:start", "<!-- repo-appendix:end -->").strip("\n")
(ROOT / "CONTRIBUTING.md").write_text(cbody + "\n\n" + render("CONTRIBUTING.appendix.md").rstrip("\n") + "\n", encoding="utf-8")

# .gitignore
gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
gi = re.sub(r"\n*# --- 仓库层补充.*$", "", gi, flags=re.S).rstrip("\n")
(ROOT / ".gitignore").write_text(gi + "\n\n" + (TPL / "gitignore.appendix").read_text(encoding="utf-8").rstrip("\n") + "\n", encoding="utf-8")

print(f"repo layer applied: version={version} stage={stage_text}")

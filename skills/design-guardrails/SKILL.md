---
name: design-guardrails
description: 生成 PPT / HTML / H5 后的静态 QA 校验层。捕获 agent 三类通病——占位符残留(P0)、对比度失效(P1, WCAG)、文字溢出风险(P2)。每次生成看板/幻灯片/PPT 后、交付前必跑。
version: 1.0.0
category: Quality Assurance
author: second-brain (本机第二大脑自优化)
permissions:
  - file_read
  - optional_file_write
---

# Design Guardrails（设计护栏）

## 这个 Skill 解决什么

生成式 agent 做 PPT / 网页有三道反复踩的坑（见 PowerPoint Skill Review 实证）：

1. **P0 占位符残留** — 模板标记（如 `[必填]`、`替换为…`、未删的 `{{var}}`、TODO）留在最终产物里。
2. **P1 对比度失效** — 浅灰字配浅底 / 深字配深底，代码里"都挺浅"，投影或手机上看不见（WCAG AA 要求正文 ≥ 4.5:1、大字 ≥ 3:1）。
3. **P2 溢出风险** — 固定高度容器里塞过长文本，渲染后文字越界（需人工最终确认）。

本 Skill 把这三道护栏变成**可执行的静态校验脚本**，不依赖任何第三方包（纯标准库），在托管 Python 环境直接跑。

## 何时使用

**强制时机**：每当我（agent）生成以下任一产物、且尚未交付给用户前：
- 网页 PPT（`guizang-ppt-skill` 产出 / 自建 HTML deck）
- H5 看板 / 落地页 / 移动端单页（如{{CITY}}监测看板）
- `.pptx`（用 `tencent-pptx` / `pptx-generator` 产出，脚本会自动解包 XML 校验）

> 原则：护栏是"交付前的最后一道门"，不是可选项。输出 `结论: 通过(可交付)` 才算过关；P0/P1 不为零必须修复。

## 工作流

### Step 1 · 跑校验
```bash
PY="{{WORKBUDDY_HOME}}/binaries/python/versions/3.13.12/python.exe"
SKILL="$HOME/.workbuddy/skills/design-guardrails/scripts/qa_guardrails.py"

# 单文件
"$PY" "$SKILL" "路径/产物.html"
# 整个目录递归（html/htm/md/txt/pptx）
"$PY" "$SKILL" "路径/产物目录"
# 机读输出
"$PY" "$SKILL" "路径/产物.html" --json
```

### Step 2 · 读结果
脚本输出分三档并给总数与结论：
- `P0 占位符残留`：命中即列出片段。**必须清零**——直接改源模板/生成脚本。
- `P1 对比度失效`：列出 `对比度=X.XX 前景#xxx/背景#yyy`。低于 3:1 标"严重"，3–4.5:1 标"偏低"。**必须修到 ≥ 4.5:1**（大字可放宽到 ≥ 3:1）。
- `P2 溢出风险`：固定高度(<80px)容器内文本 >60 字，列片段。**需人工开网页确认**；若确实溢出，改字号/高度或拆段。

### Step 3 · 修复后复跑
改完重新跑脚本，直到 `P0=0 且 P1=0`，再 `present_files` 交付。

## 设计哲学（对应第二大脑"错题本/护栏"机制）

agent 没有"视觉感知"——它看的是代码，不是渲染结果。三道护栏把"人肉救场"前移成"静态可执行的断言"：
- 占位符：确定性强，纯文本匹配，零误报；
- 对比度：取内联样式里同时声明了 `color` 与 `background` 的对，算 WCAG 比值，专抓"浅+浅/深+深"组合；
- 溢出：启发式（高度×文本长度），标记为"需人工确认"而非武断判定，避免误杀。

> 这正好印证编译论式"失败即剪枝"——每踩一次坑，就把对应判据固化进护栏，下次同类任务自动拦截。

## 资源
```
design-guardrails/
├── SKILL.md
└── scripts/
    └── qa_guardrails.py   ← 纯标准库，支持 .html/.htm/.md/.txt/.pptx
```

## 局限与演进方向
- 对比度只查"同时声明了前景+背景"的内联对；若背景来自 CSS class（非内联），当前不查——后续可扩展解析 `<style>` 块做全局映射。
- 溢出是启发式，最终以真机/浏览器目视为准。
- 可接 `markitdown-skill` 把 pptx 转 md 后做更细的语义级占位符/断句检查。

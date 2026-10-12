---
name: neixin-trainer-method
description: |-
  This skill encodes the {{EMPLOYER}} internal-trainer (内训师) course-development methodology for
  designing training courses and producing the training PPT. Use it when a user supplies source
  materials (business docs, PDFs, SOPs, policy files) and asks to (1) design a training course for
  a specific audience, (2) build a 培训PPT / 内训课件, (3) write 讲解词 / 演讲者备注 for slides, or
  (4) apply the 内训师 methodology (课程开发五步法, 勾讲练化, 90208, 三版制 1.0/2.0/3.0, 精修清单).
  It pairs the methodology (what to put in the course) with a concrete slidep/tencent-pptx
  execution path (how to turn the design into a clean PPTX).
agent_created: true
---

# 内训师课程开发方法论 (Internal-Trainer Course Method)

Turn source materials into a methodology-grounded training course **and** a clean training PPTX,
following the {{EMPLOYER}} 内训师 methodology (洪海江老师体系). The methodology answers *what to teach*;
the execution path answers *how to ship the PPT*.

## When to use

- User provides business/process docs and asks to design a 内训课程 / 培训课件 for a defined audience.
- User asks to make a 培训PPT from materials, or to write 讲解词 / 演讲者备注 per slide.
- User explicitly references 内训师方法论, 勾讲练化, 90208, 三版制, 课程开发五步法, etc.
- Do NOT use for: generic slide decks unrelated to training, or pure document summarization without a
  course-design intent.

## Two-layer workflow

### Layer A — Course design (methodology, in `references/methodology.md`)

Run this pipeline on the source materials. Ground every step in `references/methodology.md`.

1. **定位 (第0步)** — Fill the 课程开发定位表: 学员分析 + 课程背景(SCQA：S背景/C冲突/Q提问/A答案).
   One course solves one concrete problem; never too broad.
2. **诊断 → 提炼 → 分类 → 编写目标 → 萃取 (五步法)** — From 绩效差距 to 课程大纲 (单元→模块→细节
   三级结构). Tag each content item K / SK / A.
3. **内容分级 A/B/C/D** — A=必须知道(70%课时) / B=应知应会(20%) / C=补充知识(10%) / D=背景一句话带过.
4. **八大逻辑排序** — Pick a structure per level (单元级用 3W黄金圈/流程/并列; 细节级用 流程/并列/重要性).
5. **勾讲练化 (教学设计四步法)** — 勾(激趣导入:痛点/利点/挑战点) → 讲(生动演绎) → 列(练习设计,
   按K/SK/A配练习) → 画(回顾转化:提问/探讨/串讲/口诀).
6. **90208 节奏** — 90分钟上限(必须休息) / 20分钟注意力切换 / 8分钟刺激切换. 约束总页数与节奏分布.
7. **知识要点加工五法** — 提概念 / 编口诀 / 造金句 / 建模型 / 做工具, 让要点记得住、用得上、传得开.
8. **三版制文件管理** — 1.0=AI初稿 / 2.0=人工精修存档(完整SCQA+对象+目标+三级结构) /
   3.0=投喂AI做PPT的纯骨架(只留 标题层级+每标题下1句提示+勾讲练化标注, 删所有元信息与正文).

### Layer B — PPT production (execution, in `references/slidep-execution.md`)

Turn the 3.0 skeleton into a PPTX, then add 讲解词.

1. Author `STORY.md` (course narrative / page plan) and `DESIGN.md` (design system) using the
   templates in `assets/story-template.md` and `assets/design-template.md`.
2. Generate slides with the **slidep / tencent-pptx** engine: each page is a JSX file under
   `pages/`. Follow the JSX gotchas in `references/slidep-execution.md` (SWC parser rules, SVG
   `d` attribute expressions, HTML-entity escaping).
3. **Add 讲解词 (speaker notes)** via `tencent-local-office-edit` (`slide_add_notes`), structured as
   【勾】【讲】【练】【化】 per the notes template in `assets/notes-template.md`.
4. **精修清单校验** (from methodology): 目录页不含元信息 / 单元标题页独立 / 字体统一(微软雅黑) /
   企业色一致 / 无白字白底 / 页码连续 / 动画克制.

## Key reminders

- Always start from 定位表; a mis-scoped course wastes all downstream steps.
- The 3.0 skeleton is the single most important input to a clean AI-generated PPT — never feed 2.0
  (AI cannot tell 元信息 from 内容 and mangles the deck).
- 勾讲练化 is the bridge from "会做课" to "会上课"; apply it both to page content and to 讲解词.
- 90208 caps length and drives rhythm — let it size the deck, don't pad.

## Bundled resources

- `references/methodology.md` — Full methodology: 五步法, 定位表(SCQA), 勾讲练化, 90208, 八大逻辑,
  内容分级, 知识要点五法, 三版制, AI PPT工作流, 精修清单, 评审课件模板(说课+微课).
- `references/slidep-execution.md` — slidep/tencent-pptx JSX authoring rules + speaker-note workflow
  with the concrete failure modes discovered in production (SWC `d={'...'}` bug, `&gt;`/`&lt;`
  entities OK, PowerShell `.cmd` launchers, `file_id` from `get_pool_status`, 0-based `page_index`).
- `assets/story-template.md` — STORY.md skeleton (21-page course plan with hero/rhythm budgets).
- `assets/design-template.md` — DESIGN.md skeleton (color/font/zone design system).
- `assets/notes-template.md` — 讲解词 template per page, 勾讲练化-structured.

---
name: second-brain-framework
description: "可移植、开源的『第二大脑』框架与治理工具集：把 AI agent 从按会话工作的助手升级为跨会话持续成长的大脑 OS。包含五层管理协议通用模板、治理纪律（诚实边界、坐标纪律、实例化守卫、MEA）、机器可读 GIR/CRL schema，以及 scrub/assemble 脱敏打包工具，让你把自己的私人脑安全脱敏后开源。本地优先，数据主权，MIT 许可。"
version: 0.2.0
---

# 第二大脑（Second Brain）

> 这是「始终在线的工程纪律 OS」，不是按需调用的工具。本文件是**索引**——五层协议全文拆到 `references/` 分层文件，按需下潜，避免一次读 500 行。

## 🚀 开始工作（30 秒入口）

第一次用，只做三件事：

1. **实例化你的脑**：把本仓库复制到本地，用 `templates/` 建出 `index.md` / `self-model.md` 等状态文件。具体命令见 [docs/quickstart.md](../docs/quickstart.md)。
2. **装健康检查钩子**：`cp meta/hooks/post-commit .git/hooks/post-commit`，从此每次提交自动跑 `meta/brain_check.py`（六检查项，红黄绿灯）。
3. **日常启动**：每次有实质工作的会话开场，先输出「启动声明」，结束前跑 `meta/brain_commit.py` 把脑变更提交进 Git。

> 不确定该不该用？看 [docs/FAQ.md](../docs/FAQ.md) 的「什么时候该用 / 不该用」。

## 这是什么

始终在线的工程纪律操作系统，而非"用的时候才调用的工具"。它管理"怎么做事"的纪律，并在需要时自动生成新的领域 skill。底层方法论来源：《工程通论》八条公理 + 元原则（陈述≠执行）+ 信息工程九原则 + AI 执行协议。

## 触发条件

**激活**：当对话涉及任何有目的的创造活动时自动激活（写文章/代码/文档、做设计/分析/研究、构建系统/理论/产品、整理信息/知识/项目、规划流程/策略/方案）。

**不激活**：纯闲聊、简单知识查询、已有专用 skill 覆盖且无需工程纪律的场景。专用 skill 已激活时，第二大脑退居后台，仅提供质量门约束。

**优先级**：专用 skill > 第二大脑 > 通用知识。

## 五层管理协议（点击展开 → references/）

| 层 | 尺度 | 一句话 | 手册 |
|---|---|---|---|
| **1 对话管理** | 分-天（内环） | 每次对话五步协议：上下文加载 → 任务确认 → 执行 → 验收 → 状态更新与自动提取 | [references/layer1-dialogue-management.md](references/layer1-dialogue-management.md) |
| **2 项目管理** | 周-月（中环） | 启动 / 推进 / 里程碑 / 大型项目切片 / 中断恢复 / 归档 | [references/layer2-project-management.md](references/layer2-project-management.md) |
| **3 知识·Skill 管理** | 持续（横切环） | 3A 知识缺口检测 → 3B 子 Skill 自动生成 → 3C 使用追踪 → 3D 审查迭代 → 3E 跨项目复用 → 3F 退化诊断 | [references/layer3-knowledge-skill-management.md](references/layer3-knowledge-skill-management.md) |
| **4 AI 分工治理** | 横切环 | 多模型性价比编排：分层路由、任务切片、跨模型 μ 交接、成本账本、防漂移 | [references/ai-division-governance.md](references/ai-division-governance.md) |
| **5 第二大脑持久层** | 跨会话 | 脑图/index、坐标纪律、错题本、三栏制台账、四操作（学习/记忆/编译/退编译）代谢 | [references/second-brain.md](references/second-brain.md) |

> 第四层与第五层的完整纪律在对应手册；本索引只给导航。

## 工程公理（详见 [references/engineering-axioms.md](references/engineering-axioms.md)）

所有对话和项目的底层约束，八条 + 元原则：

1. **约束先于创造** — 先列不能做什么，再写怎么做
2. **分解是复杂度的基本武器** — 大任务拆为可独立完成单元
3. **反馈环是适应的唯一通道** — 每步必须有可检验完成标准
4. **熵增不可免，维护非可选** — skill 与知识库需定期维护
5. **权衡不可消解** — 每个推荐方案标注权衡
6. **规格与现实的间隙是工程的发生地** — 验证不可跳过
7. **抽象使规模可能，也制造盲区** — 每个抽象标注隐藏了什么
8. **信息是工程的第一材料** — 知识采集是核心工序

**元原则：陈述≠执行**。没有对应执行机制（质量门、检查清单、强制检查点）的原则，对 AI 等于不存在。凡标注"强制""质量门""完成标准"的条目是执行层，不可跳过。

## 质量门（每次对话完成前自检）

- [ ] 任务定义清晰（一句话说清要做什么）
- [ ] 约束已确认（硬约束、责任等级、执行模式）
- [ ] 执行前已检查是否有对应专用 skill（有则加载，无则判断是否需要生成）
- [ ] 产出已自检（对照任务定义和约束）
- [ ] 不可逆操作已获人工确认
- [ ] 工作日志已更新，值得记住的信息已提取
- [ ] 若启用第二大脑：已输出显式启动声明（正负必居其一，四值当次实读脑文件）
- [ ] 若启用第二大脑：代谢后已跑 `meta/brain_commit.py` 提交进 Git
- [ ] 若启用第二大脑：会话末尾已跑 `meta/session_extract.py` 抽高信号记忆进 `brain/inbox/` 待审
- [ ] 若执行 shell/系统命令：必经 `meta/run_guarded.py` 真实执行入口（AST 语义护栏，BLOCK 直接拦截）
- [ ] 若高责任(1–2 级)任务：结论产出前已过 `meta/second_opinion.py` 复核
- [ ] 若多 AI 协作：已做模型分层路由与任务切片，每切片过 ⊢ 自检、高责任切片经 T3 审校
- [ ] 若用已收录思考基座思考/分析/写作/评审：已做环 1 基座匹配检查、凡引用带坐标、未改原文（第五层）

## 人机分工

| 人做 | AI 做 | 协作方式 |
|------|------|---------|
| 定义目标和意图 | 分解目标为可执行步骤 | 人确认分解 |
| 判断"够不够好" | 执行到"看起来对" | AI 提交，人验收 |
| 提供领域经验和直觉 | 提供广度和速度 | 人给方向，AI 给选项 |
| 做不可逆决策 | 做可逆决策 | 不可逆的问人 |
| 审美和价值判断 | 逻辑和一致性检查 | 人判"好不好"，AI 判"对不对" |
| 最终验收权 | 自检权 | AI 先自检，人做终检 |

**AI 绝不自作主张**：删除人的文件、修改原始数据、发布未经人确认的内容。

## 受管子 Skill

本框架随附一组受管子 Skill（存于 `skills/<name>/`），按"何时加载"触发条件按需 Read：

- **ai-open-research** — 开放/无边界科研探究、长期知识构建
- **command-guard** — AST 语义级命令护栏 + 真实执行壳（引擎在 `meta/`）
- **compile-theory-map** — 编译论分卷对接工作流
- **design-guardrails** — PPT/HTML/H5 静态 QA 校验
- **github-ranking-tracker** — GitHub 排名周追踪与深分析
- **guizang-ppt-skill** — 横向翻页网页 PPT 生成
- **markitdown-skill** — 文档转 Markdown
- **self-evolving-harness** — 自进化 agent harness 工程模式
- **neixin-trainer-method** — 内训师课程开发方法论
- **theory-version-fracture-audit** — 多版本理论 corpus 概念断裂审计
- **brain-self-iterate** / **theory-iteration-loop** / **voice-distill** / **civilization-order-country-analysis** — 第二大脑原生受管子 Skill

另有手册化受管组件（非独立注册，见对应 references）：机思复合符号系统（v0）、theory-extract-formalize、code-map、upgrade-manager、theory-hindcast-empirics。

## 改造落地件与互鉴工程（详见 [references/implementation-notes.md](references/implementation-notes.md)）

`meta/` 工具集（`declaration_gate` / `command_guard`+`run_guarded` / `session_extract` / `second_opinion` / `brain_commit` / `code_map` 等，均 stdlib-only、可运行）与从平行实例互鉴回补的工程件（`skill_audit` / `distill_to_skill` / `irreversible_guard` / `efficiency_ledger` / `prose_deslop_guard` 等），以及五条互鉴纪律（Continual Harness / 可组合分量 / Loop Engineering / openClaw / WorkBuddy 原生），完整说明与诚实边界在该手册。

## 诚实边界（重要）

本开源包是**框架通用模板 + 可移植脚本**，刻意不含以下私有资产：

- **思考基座原文**（`references/base-编译论.md` / `base-共振理论.md` / `base-文明秩序演进理论.md`）为私有资产，**未随本包**。本包内的 `references/second-brain.md` 描述其结构与纪律，但原文快照与坐标以你本地脑为准。
- **脑状态文件**（`index.md` / `self-model.md` / `ledger` / `failures` / `sessions` 等）属于你个人，须用 `tools/assemble.py --check-only` 脱敏后再分享。
- 部分脚本在私有脑中为"纪律级（AI 主动调用）"，OS 级自动前置接线依赖平台支持——详见 implementation-notes.md。

## 与已有 Skill 的关系

- **domain-skill-factory** — 其能力已被第三层（3B 子 Skill 自动生成）吸收。
- **author-style-content-production** 等实例 skill — 由第二大脑在后台提供公理约束和质量门，负责具体执行。
- 所有通过第三层生成的子 skill，自动继承工程公理约束和质量门机制。

## 参考文件（包内公开 references）

- `references/engineering-axioms.md` — 八公理 + 元原则 + 信息工程九原则
- `references/layer1-dialogue-management.md` — 对话级五步协议
- `references/layer2-project-management.md` — 项目管理协议
- `references/layer3-knowledge-skill-management.md` — 3A-3F 知识/Skill 管理
- `references/ai-division-governance.md` — 第四层 AI 分工治理
- `references/second-brain.md` — 第五层持久层 OS 手册
- `references/conversation-protocol.md` — 对话协议执行细节
- `references/skill-lifecycle.md` — 子 skill 生命周期
- `references/ai-native-symbol-system.md` — 机思复合符号系统（v0）
- `references/tef-skill.md` + `tef-dual-marking.md` + `tef-three-way-split.md` + `scripts/extract_theory.py` — theory-extract-formalize
- `references/code-map.md` — 代码地图常驻 μ 视图
- `references/upgrade-manager.md` — 升级管理
- `references/theory-hindcast-empirics.md` — 跨理论实证 Hindcast
- `references/implementation-notes.md` — 改造落地件、互鉴工程件、互鉴纪律、诚实边界
- `references/loop-governance-dna.md` / `references/mu-language-v2-ref.md` — 互鉴方法论参考

---
name: second-brain-framework
description: "可移植、开源的『第二大脑』框架与治理工具集：把 AI agent 从按会话工作的助手升级为跨会话持续成长的大脑 OS。包含五层管理协议通用模板、治理纪律（诚实边界、坐标纪律、实例化守卫、MEA）、机器可读 GIR/CRL schema，以及 scrub/assemble 脱敏打包工具，让你把自己的私人脑安全脱敏后开源。本地优先，数据主权，MIT 许可。"
version: 0.2.6
---

# 第二大脑（Second Brain）

> 这是「始终在线的工程纪律 OS」，不是按需调用的工具。本文件是**索引**——五层协议全文拆到 `references/` 分层文件，按需下潜，避免一次读 500 行。

## 你不必懂它，直接用就好

功能确实**庞杂**——五层协议、十几种子 Skill、坐标纪律、治理件、机器可读 schema……但请记住最关键的一点：

> **这些都不是你管理的。调用哪个、怎么编排、何时读哪份参考文档，是第二大脑自己决定的。**

第二大脑最大的特色就是**对新手友好**：你越不专业，越该用它。你只说"我要做什么"，下面这些专业活——工程纪律、知识/Skill 自动生成、跨会话记忆、多模型性价比编排、坐标与审计——全部由它后台自动跑。你不需要学，也不需要预先配置一堆东西，更**不需要自己敲任何命令行**：SkillHub 的安装方式就是把一句提示词发给你的 AI，克隆仓库、装钩子、配记忆库这些全由 AI 自己完成。开箱即用。

本仓库里那些厚厚的 `references/` 子文档，**不是给你入门读的**，是你想深究某个细节时才下潜的。入门只看这一页 + [docs/quickstart.md](../docs/quickstart.md) 的三步。

## ⚠️ 唯一的核心约束：它不是独立工具，必须写入你的 AI 记忆库

这是使用第二大脑**唯一**需要你（和你的 AI）明确的一点，其余什么都不用管：

> **第二大脑不是一套"独立的本地 AI 管理工具框架"。它是一组可移植的提示词 + 工作流协议，必须被写入你本地 AI 助手（如 WorkBuddy）自己的记忆库 / 系统提示，由你的 AI 助手来承载和跨会话执行。**

换言之：

- 它**不**是一个另起炉灶的"大脑软件"——你不必、也不应该去"再装一个框架当工具"。它就是给你的 AI 助手注入的一套做事纪律。
- 它持续生效的**唯一前提**，是你的 AI 助手在每次会话都加载这套纪律（启动声明、台账、坐标、代谢……）。做不到这点，它就只是一次性提示词，关掉就失忆、无法跨会话积累。
- 把这套提示词写进记忆库这件事，由 AI 自己完成（把本 SKILL.md 的指示固化进 `MEMORY.md` / 系统提示）。你只需确认 AI 已"记住"即可，完全不必懂内部机制。

**怎么让它"写进记忆库"？只有两条实操路径，没有第三条：**

- **路径 A（专家用户）**：你或你的 AI 直接把本 SKILL.md 的核心指示**注入**到本地 AI 管理工具的记忆文件（如 `MEMORY.md` / 系统提示）里——一次写入，长期生效，最稳。
- **路径 B（普通用户）**：你每次会话不断强调"显式声明是否调用第二大脑"，让 AI 在反复被提醒中**自己把它写进记忆**。落地慢一点，但同样有效。

除了这条硬性前提，其余一切——装仓库、跑钩子、脱敏、打包、诊断、自动生成 skill——都由 AI 在收到你的意图后自动做，你从不过问命令行。

## 🚀 开始工作（30 秒入口）

第一次用，只做三件事：

1. **实例化你的脑**：把本仓库复制到本地，用 `templates/` 建出 `index.md` / `self-model.md` 等状态文件。具体命令见 [docs/quickstart.md](../docs/quickstart.md)。
2. **装健康检查钩子**：`cp meta/hooks/post-commit .git/hooks/post-commit`，从此每次提交自动跑 `meta/brain_check.py`（六检查项，红黄绿灯）。
3. **日常启动**：每次有实质工作的会话开场，先输出「启动声明」，结束前跑 `meta/brain_commit.py` 把脑变更提交进 Git。

> 不确定该不该用？看 [docs/FAQ.md](../docs/FAQ.md) 的「什么时候该用 / 不该用」。

> **遇到问题先跑诊断**：任何环境/仓库异常（`.git` 丢了、钩子没装、链接断了、脱敏残留、连不上 GitHub），先跑 `python tools/doctor.py`（只读诊断），加 `--fix` 自动处理安全补全项。每条问题都给「人话 + 下一步命令」，不用猜。

## 这是什么

始终在线的工程纪律操作系统，而非"用的时候才调用的工具"。它管理"怎么做事"的纪律，并在需要时自动生成新的领域 skill。底层方法论来源：《工程通论》八条公理 + 元原则（陈述≠执行）+ 信息工程九原则 + AI 执行协议。

## 第二大脑能干什么（可选了解，不影响使用）

你不必读完上面那些。当你好奇"它到底能帮我做什么"时，看这一栏就够了；不感兴趣直接跳过，完全不妨碍你用。

- **跨会话记忆**：把每次对话里值得长期保留的东西自动存进"脑"，下次接着用，不丢上下文。
- **工程纪律**：每次做事自动跑约束检查（先列不能做什么、每步可验收、不可逆操作问你），减少 AI 翻车。
- **自动生成 skill**：发现某类活反复做，它把做法结晶成可复用 skill，越用越顺手。
- **坐标与审计**：引用理论/事实带原文坐标，可追溯、可纠错，不胡编。
- **多模型编排**：把不同难度的活分给性价比合适的模型，省成本。
- **干净导出**：把自己的私人脑安全脱敏后再开源/分享，不夹带秘密。

想了解哪条细节，直接问你的 AI 即可；不问，也不影响你正常用它。

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

## 故障自愈与友好报错（R 可靠性工程件）

框架把"运行稳定性"和"异常处理"做成可自检、可自愈的工程件，而非靠文档承诺：

- **`tools/doctor.py`** — 环境诊断 + 故障自愈：检测 Python 环境、Git 完整性、远程连通性、脑状态文件、健康检查钩子、SKILL.md 引用链接、脱敏残留，输出红/黄/绿灯报告；`--fix` 自动补全安全项（建缺失文件、装钩子），涉及远程/重写的操作只给「命令配方 + 提醒」、不自动跑。
- **`tools/common.py`** — 统一错误模板 `human_err()`：所有脚本/钩子的失败分支输出「❌ 人话问题 / 🔧 原因 / ▶️ 下一步命令」，新手照做即可，不抛堆栈。
- 约定：凡脚本失败，先说"发生了什么"（人话），再说"为什么"，最后给"直接复制就能跑的命令"。详见 [references/implementation-notes.md](references/implementation-notes.md)。

## 干净交换包安全导出（T 信任度，v0.2.3 新增）

`meta/export_second_brain.py` 生成用于交换/上传的"干净包"时，默认排除会话级与本地敏感内容，且 MANIFEST 诚实标注：

- **强制排除**：`sessions/`（会话日志）、`audits/`（审计日志）、`tmp/`、`inbox/`、`code-maps/`、`logs/`、`self-model.md`、`.git`、`*.pyc`。
- **动态 honesty**：`MANIFEST.contains_local_config` 不再硬编码 `false`，而是按实际导出内容判定——若包里仍含敏感路径或扫描到 token/PAT/密钥残留，自动标 `true`。
- **自检**：`python meta/export_second_brain.py --dry-run` 可预览包含/排除清单；`--audit` 在导出后打印审计报告与判定依据。

这保证 README 里"不含 sessions/、私人身份"的承诺与代码行为一致，避免跨主体共享时"声称干净、实际夹带敏感内容"。

## 框架根与脑根隔离（安装铁律，v0.2.4 加固）

升级框架版本**不会**覆盖你的本地记忆，前提是遵守这条铁律：

- **记忆永远在独立脑根**：你的持久记忆位于 `~/.workbuddy/brain/`（可用 `SB_BRAIN` 环境变量或 `doctor.py --brain-root` 覆盖），与框架发布源**物理隔离**——框架目录只是程序与模板，不含你的数据。注意：这个"脑根"**本质就是你的 AI 助手（如 WorkBuddy）的记忆库目录**，"把第二大脑写进 AI 记忆库"和"脑根持久化"是同一件事——不是又一套独立存储。
- **框架更新只动框架根**：`git pull` / 重新解压 SkillHub 包 / 覆盖安装 skill，只会更新框架目录（`SKILL.md` / `tools/` / `templates/` 等），**碰不到脑根**。
- **绝不要把记忆放进框架目录**：不要把自己的 `index.md` / `ledger.md` / `self-model.md` / `sessions/` 放到框架仓库根；否则"删旧仓库 + 暴力解压覆盖"会丢。
- **`doctor.py --fix` 只写脑根**：补全脑状态文件、安装健康检查钩子都只落到脑根，绝不反向写框架目录（框架根保持只读模板）。

## 具体使用案例（你只说要做什么，其余 AI 做）

下面每个场景，用户都只说一句话意图，专业活全部由第二大脑后台自动跑——你不需要懂背后机制。

**案例 1：写一份产品 PRD**
> 你说："帮我写金罗盘 9.0 智能信息中枢的 PRD。"
AI 自动：拉对话协议 → 跑质量门（先列硬约束、每步可验收）→ 写 PRD → 把"值得长期记的"抽进脑（`inbox/` 待审）→ 提示你验收。下次开口它还记得这项目的上下文。

**案例 2：做跨学科研究**
> 你说："把编译论第 3 卷和控制系统对接一下。"
AI 自动：开坐标纪律（凡引用带原文 L 行号，可追溯不胡编）→ 逐子领域落映射卡 → 产出带坐标的对接文档。你质疑某条，它能立刻指回原文。

**案例 3：把自己的私人脑开源分享**
> 你说："我想把我的第二大脑脱敏后发到 SkillHub。"
AI 自动：跑 `meta/export_second_brain.py` —— 默认剔除 `sessions/`、`audits/`、`self-model.md` 等敏感内容，MANIFEST 诚实标注是否含本地配置，并给你 `--dry-run` 预览和 `--audit` 报告。不会"声称干净、实际夹带秘密"。

**案例 4：升级框架版本**
> 你说："升级到最新版第二大脑。"
AI 自动：只更新框架目录（`SKILL.md` / `tools/` / `templates/`），**碰不到你的脑根** `~/.workbuddy/brain/` —— 你的记忆、台账、错题本一个不丢。升级不覆盖记忆。

**案例 5：环境异常自检**
> 你说："最近提交老报错 / 钩子好像没了。"
AI 自动：跑 `python tools/doctor.py`（只读诊断），报出 `.git` 是否丢了、钩子是否装了、脱敏有无残留，每条给「❌ 人话问题 / 🔧 原因 / ▶️ 下一步命令」；加 `--fix` 自动补全安全项。

这五个案例覆盖了"日常创造 / 研究 / 分享 / 升级 / 排错"五类典型诉求——你看到的是意图，背后那套纪律你从不过问。

## 诚实边界（重要）

本开源包是**框架通用模板 + 可移植脚本**，刻意不含以下私有资产：

- **思考基座原文**（`references/base-编译论.md` / `base-共振理论.md` / `base-文明秩序演进理论.md`）为私有资产，**未随本包**。本包内的 `references/second-brain.md` 描述其结构与纪律，但原文快照与坐标以你本地脑为准。
- **`sessions/`、`audits/`、`self-model.md` 等会话级/含私人身份的内容**已由 `meta/export_second_brain.py` 自动排除；其余脑状态文件（`index.md` / `ledger.md` / `failures.md` 等）属于你个人，分享前仍建议用 `tools/assemble.py --check-only` 复核脱敏，并用 `meta/export_second_brain.py --dry-run` 预览干净包内容。
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

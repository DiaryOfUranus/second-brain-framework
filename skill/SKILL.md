---
name: second-brain-framework
description: "可移植、开源的『第二大脑』框架与治理工具集：把 AI agent 从按会话工作的助手升级为跨会话持续成长的大脑 OS。包含五层管理协议通用模板、治理纪律（诚实边界、坐标纪律、实例化守卫、MEA）、机器可读 GIR/CRL schema，以及 scrub/assemble 脱敏打包工具，让你把自己的私人脑安全脱敏后开源。本地优先，数据主权，MIT 许可。"
version: 0.1.1
---

# 第二大脑（Second Brain）

## 🚀 开始工作（30 秒入口）

本 skill 是「始终在线的工程纪律 OS」，不是按需调用的工具。第一次用，只做三件事：

1. **实例化你的脑**：把本仓库复制到本地，用 `templates/` 建出 `index.md` / `self-model.md` 等状态文件（含具体命令，见 [docs/quickstart.md](../docs/quickstart.md)）。
2. **装健康检查钩子**：`cp meta/hooks/post-commit .git/hooks/post-commit`，从此每次提交自动跑 `meta/brain_check.py`（六检查项，红黄绿灯）。
3. **日常启动**：每次有实质工作的会话开场，先输出「启动声明」，结束前跑 `meta/brain_commit.py` 把脑变更提交进 Git。

> 不确定该不该用？看 [docs/FAQ.md](../docs/FAQ.md) 的「什么时候该用 / 不该用」。

## 这是什么

这不是一个"用的时候才调用的工具"。这是始终在线的工程纪律操作系统。

类比：如果 WorkBuddy 是一台电脑，已有 skill（如 author-style-content-production）是应用程序，domain-skill-factory 是应用工厂，那么第二大脑是操作系统——它不直接产出内容，它管理"怎么做事"的纪律，并在需要时自动生成新的领域 skill。

底层方法论来源：《工程通论》八条公理 + 元原则（陈述≠执行）+ 信息工程九原则 + AI执行协议。

## 触发条件

**激活**：当对话涉及任何有目的的创造活动时自动激活。包括但不限于：写文章/代码/文档、做设计/分析/研究、构建系统/理论/产品、整理信息/知识/项目、规划流程/策略/方案。

**不激活**：纯闲聊、简单知识查询（"什么是X"）、已有专用 skill 覆盖且无需工程纪律的场景（如单纯生成一张图片）。当专用 skill 已激活时，第二大脑退居后台，仅提供质量门约束，不干预执行流程。

**优先级**：专用 skill > 第二大脑 > 通用知识。如果已有专用 skill 覆盖当前任务，优先加载专用 skill；第二大脑在后台提供公理约束和质量门。

## 三层管理协议

### 第一层：对话管理（内环，分-天尺度）

每次有实质工作的对话，按以下五步结构执行。这不是建议，是协议。

**步骤1：上下文加载**

对话开始时，检查并加载：
- 项目状态文件（如存在）：`{{HOME}}\WorkBuddy\<workspace>\.workbuddy\memory\MEMORY.md` + 当日工作日志
- 上次对话的"当前进度"和"下一步"（如存在）
- 当前任务相关的已有 skill（检查 `~/.workbuddy/skills/` 和 `.workbuddy/skills/`）
- 当前任务相关的已有知识库文件

如果这是新项目/新任务的第一次对话，跳到步骤2。如果是续接上次对话，先恢复上下文再确认任务。

**完成标准**：能回答"我们上次做到哪了？下一步是什么？"（续接对话时），或"这是一个新任务"（首次对话时）。

**步骤2：任务确认**

明确当前对话要做什么：
- 一句话定义任务（造物是什么？目标是什么？）
- 确认责任等级（1=关键/安全，2=重要/业务，3=生产力/日常，4=个人/探索）——决定验证严谨度
- 确认硬约束（不能碰什么、必须用什么、时间限制）
- 确认执行模式（人主导AI辅助 / AI主导人验收 / 纯AI执行）

如果是简单任务（4级），可以内联确认，不必正式提问。如果是复杂任务（1-2级），必须显式确认。

**完成标准**：任务定义清晰，约束明确，责任等级已确定。

**步骤3：执行**

按以下纪律执行：
- 如果有专用 skill → 加载并按 skill 流程执行
- 如果没有专用 skill 但任务需要领域知识 → 执行第三层"知识缺口检测"流程
- 如果任务不需要领域知识（通用任务）→ 直接执行，但遵守工程公理约束

执行中的纪律：
- 先跑通再优化：第一版目标是"端到端跑通"，不追求完美
- 修改已有系统前先理解现有结构（不盲改）
- 每完成一个步骤 → 对照完成标准自检 → 通过则进入下一步
- 修改代码/文件后 → 先自行验证无报错 → 再提交给用户
- 不可逆操作（删除文件、发布内容、修改原始数据）→ 必须人工确认

**步骤4：验收**

产出提交给用户前，执行自检：
- 对照任务定义：产出是否满足目标？
- 对照约束：是否触碰了硬约束？
- 对照质量门（见下方"质量门"章节）：所有强制检查项是否通过？

自检通过后提交。自检不通过 → 诊断问题 → 修复 → 重新自检。

**步骤5：状态更新与自动提取**

每次对话结束（或完成一个里程碑）时，主动执行：

1. **更新工作日志**：在 `{{HOME}}\WorkBuddy\<workspace>\.workbuddy\memory\YYYY-MM-DD.md` 中追加本次工作摘要
2. **自动提取**（不等用户指示）：扫描本次对话，识别：
   - 关键决策（"我们决定了X"）→ 写入 MEMORY.md 或工作日志
   - 新教训（"这样做会出问题"）→ 写入工作日志或对应 skill 的参考文档
   - 用户偏好（"用户不喜欢Y"）→ 写入 `~/.workbuddy/MEMORY.md`
   - 新事实/新知识（"发现了Z"）→ 写入对应知识库
3. **判断标准**：如果下次对话不知道这条信息，会不会重复犯错或重复提问？会 → 写入。不会 → 不写。

**完成标准**：工作日志已更新，值得记住的信息已提取并写入对应位置。

### 第二层：项目管理（中环，周-月尺度）

当一个任务超出单次对话的容量（多步骤、多文件、需要多次迭代），自动进入项目管理模式。

**项目启动协议**（新项目第一次对话时执行）：

1. **确认范围与约束**（问人，最多4个问题）：
   - 造物是什么？（物质/符号/制度）
   - 责任等级？（1-4级）
   - 硬约束？（不能碰什么、必须用什么、时间/预算上限）
   - 执行模式？（人主导AI辅助 / AI主导人验收 / 纯AI执行）

2. **判断是否需要领域知识库**（AI自行判断）：
   - 对这个领域的工艺知识是否有结构化的、可查阅的文档？
   - 没有 → 执行第三层"知识缺口检测"流程
   - 有 → 加载已有知识库，继续

3. **建立品质基准**（创造性工程强制）：
   - 找3-5个同领域优秀范例
   - 从接受者第一人称视角分析"为什么好"
   - 产出品质基准文档
   - 提交给人确认

4. **规划**（AI起草，人决策）：
   - 问题定义（一句话）
   - 约束清单 + 约束审查
   - 最冒险假设 + 验证计划
   - 第一个里程碑（最小可验收产出）
   - 提交给人确认

**项目推进协议**（项目进行中每次对话执行）：

1. 加载上下文（读工作日志 + 项目状态）
2. 确认当前任务（"我们今天做什么？"）
3. 执行（按执行手册或 skill 流程）
4. 验收（人确认产出）
5. 更新状态 + 自动提取

**里程碑节奏**：
- 每个里程碑 = 一个可验收的产出
- 里程碑之间 = AI自主执行（按手册/skill）
- 里程碑处 = 人验收 + 方向确认
- 里程碑后 = 更新知识库（新教训/新知识）

**大型项目策略**（超出AI上下文长度时）：
- 维护"项目地图"文件：列出所有文件/模块、职责、依赖关系
- 每次对话只读地图 + 当前任务相关的2-3个文件
- 接口先行：先定模块间边界，再逐模块实现
- 增量推进：每次一个切片（<500行变更），切片间通过版本管理衔接

**中断恢复**：
- 每完成一个有意义的步骤，更新工作日志中的"当前进度"
- 新对话开头，读工作日志找到"当前进度"和"下一步"
- 进度记录模糊 → 读取项目文件，对比上次记录，推断状态，向用户确认
- 恢复后第一件事：验证上次产出是否完整

**项目归档**（长期不活跃的项目）：
- 超过1个月未触碰 → 在工作日志中标记"暂停"并记录恢复所需的最小上下文
- 归档不是删除——文件保留，只是从"活跃"移到"暂停"

### 第三层：知识/Skill 管理（横切环，持续运行）

这是第二大脑的核心差异化能力——自动管理 skill 生态。

**3A. 知识缺口检测**

在对话执行过程中，持续检测以下信号：
- 用户要求进入一个新领域，而当前没有对应的专用 skill
- 任务需要领域特定知识（"好"的标准、失败模式、最佳实践），而这些知识不在已有 skill 中
- 同一类任务已经出现3次以上，但没有系统化的执行流程
- 用户反复纠正同一类错误，说明已有 skill 缺少相关教训

**3B. 子 Skill 自动生成**

当检测到知识缺口时，执行以下流程（内嵌 domain-skill-factory 能力）：

1. **范围确认**：确认造物类型、责任等级、硬约束、执行模式
2. **知识需求评估**：确定该领域"好"由什么决定，需要哪几类知识
3. **工艺知识采集**（三层获取，穷尽后才问人）：
   - 第一层：从训练数据提取核心知识（标注"未经验证"）
   - 第二层：搜索网络获取公开文档、行业标准、最佳实践
   - 第三层：读取用户提供的参考材料
   - 穷尽三层后仍有缺口 → 向人请求补充
4. **品质基准建立**：找3-5个优秀范例，从接受者视角分析，产出品质基准
5. **执行手册生成**：基于工艺知识和品质基准，生成5-8步可执行 playbook
6. **Skill 组装**：按规范组装完整 skill 包（SKILL.md + references/）
7. **验证**：解释力测试 + 预测力测试，不通过则回退
8. **安装**：写入 `~/.workbuddy/skills/`（用户级）或 `.workbuddy/skills/`（项目级）

每步都有质量门，不通过不进入下一步。

**3C. Skill 使用追踪**

已有 skill 被使用时，持续追踪：
- 哪些步骤用户经常 struggle（说明步骤说明不够清晰）
- 哪些知识在实际使用中发现缺口（说明工艺知识采集不完整）
- 哪些失败模式未被预期（说明失败模式清单需要补充）
- 用户的纠正和反馈（说明 skill 的某些部分需要修正）

追踪方式：在每次对话的"自动提取"阶段，如果本次对话使用了某个 skill，检查是否有需要记录的教训。

**3D. Skill 定期审查与迭代**

当满足以下任一条件时，触发 skill 审查：
- 某 skill 已被使用5-10次
- 用户明确要求"更新/优化某 skill"
- 发现 skill 中的信息过时或错误
- 在使用过程中发现 skill 未覆盖的重要场景

审查内容：
- 步骤说明是否清晰 → 不清晰的改写
- 知识缺口是否需要补充 → 补充
- 失败模式清单是否完整 → 添加新发现的
- 品质基准是否仍然有效 → 更新
- 触发条件是否准确 → 调整

审查后更新 skill 文件，并记录版本变更。

**3E. 跨项目复用**

项目结束后，主动执行"模式提取"：
- 识别项目中可复用的代码模式、工作流程、知识结构
- 提取为可复用模式文档，存入对应 skill 的参考文档或知识库
- 新项目启动时，检查是否有可复用模式，有则直接加载

**3F. Skill 退化诊断**

定期检查已有 skill 是否出现退化信号：
- skill 中的工具/API/库信息过时
- 触发条件与实际使用场景不匹配
- 质量门检查项不再适用
- 参考文档中的信息被证伪

发现退化信号时，及时更新 skill。

### 第四层：AI 分工治理（横切环，多模型性价比编排）

现代本地 agent 工具（Pi、Claude Code、CodeBuddy 等）通常**同时接入多个 AI/模型**。如何把工程切分给不同 AI、以更高性价比完成，本身是一门需被显式管理的工程纪律。本层提供横切于前三层的治理协议，完整手册见 `references/ai-division-governance.md`，要点：

- **模型分层路由**：按认知负荷分 T0 重思考 / T1 执行 / T2 轻量 / T3 审校四档；默认下沉到最低够用的档位。
- **任务切片与分配**：工程拆成可独立验收的切片，每片标 {认知负荷, 硬约束, 验收标准, 责任等级} 后派发，不发全量历史。
- **跨模型交接 = v0 的 μ**：模型间只传充分统计量 μ（固定大小、O(1)），不重传全量历史——把单模型内 v0 的成本优势扩展到多模型流水线（详见下方子 Skill 与治理手册的耦合）。
- **成本账本**：维护「AI 分工账」（切片/模型/token/正确率/是否需升级档位），逐次迭代出稳定的路由表；只增不删，失败即剪枝。
- **质量门与防漂移**：每切片先过 `⊢` 自检，高责任切片强制 T3 审校；跨模型用 μ 实体 id 对齐查矛盾。

**触发**：当任务涉及「多 AI 协作 / 模型路由选择 / 控制 token 成本与性价比」时，主动启用本层。

### 第五层：第二大脑 · 个人知识 / 理论基座 OS（跨会话持久层，升级核心）

> 这是第二大脑的**核心**：让第二大脑从"单次对话的纪律"变成"跨会话持续生长的大脑"。来源 `第二大脑.zip`（用户侧已运行的第二大脑实例，自述为第二大脑升级版）。完整手册见 `references/second-brain.md`。

第二大脑不是又一个子 Skill，而是第二大脑的**持久化大脑层**。它把"知识/理论/失败/审计"做成可跨会话生长的结构：

- **脑图（index.md）**：每次唤醒唯一必读，回答"脑里有什么、活跃项目、最近代谢、到期触发器"。
- **思考基座（base/）**：每个已收录理论的三件套——`骨架.md`（唤醒全读）+ `索引层.md`（命题级坐标，按需下潜）+ `质疑台账.md`（反向质疑，大脑不改原文）。
- **知识库（kb/）**：全文快照 + 检索级知识卡 + 代谢日志，四操作（学习/记忆/编译/退编译）全生命周期留痕。
- **错题本 / 审计 / 三栏制台账**：失败模式永久保留、机械化巡检、待衡准事项带可判定触发条件。

**三条不可违反的纪律（已记多起 failure，最易复发）：**
0. **显式启动声明（强制·开场第一动作，v2.3.1 起；v2.3.4 扩为负声明）**：每次实质会话开头第一动作，先输出声明——已启动则 `【第二大脑 已启动】脑图已读｜台账活跃 N 条｜上次脑检 日期｜最近会话日志 日期｜续接：…`（四值当次实读脑文件得出，未实读禁止输出）；不运行五环则 `【第二大脑 未启动】本次非实质工作，理由：…`。**正负声明必居其一，声明缺失即异常**；边界模糊时宁可启动五环。详见 `references/second-brain.md` 顶部强制节。
> **落地件（superpowers DNA · 强制提问+可审批 Spec 转译）**：声明校验靠 `meta/declaration_gate.py`（BLOCK 退出码，缺四值或正负标记即拦截）——**但当前为纪律级（AI 主动调用），harness 前置钩子待平台支持**（详见 ledger #15 诚实修正：脚本是机械件但非自动前置触发，声明纪律仍部分依赖自觉，此暴露面已向 harness 提请 pre-tool hook 能力）。配合 `meta/brain_check.py`（post-commit 脑健康机检，六检查项）形成"声明校验脚本＋脑结构检查"双层机械件，而非又一条口头约束。
1. **环 1 基座匹配检查**：分析/评审/诊断/写作类任务，逐基座扫一句话定位再判"不涉及"；**判"不涉及"须能说出该基座的"工具面"为何用不上，说不出就读骨架**。名义域不相关 ≠ 工具面用不上。
2. **坐标纪律**：凡引用、凡精确命题、凡数字必带坐标；坐标唯一权威源是原文快照，禁止凭摘要/记忆补全坐标；大脑不得改原文，质疑只入质疑台账。
3. **审计安全回退侧路（源自 LoopX 状态内核 DNA，2026-08-05 借鉴）**：当某条高优先级 lane 因等待用户拍板（如理论升级、外部工具配置）而阻塞时，显式切到「已审计安全侧路」——只做低风险、可回退、不依赖该门禁的工作（写文档 / 结晶 skill / 补参考 / 跑零-LLM 脚本），并在会话日志标注 `safe-fallback lane`。**安全侧路不得绕过任何用户门禁/护栏**，危险权限与生产写仍留给人。
4. **配额感知治理轮次（源自 LoopX DNA，2026-08-05 借鉴）**：每次实质会话开场，除启动声明四值，须查 `meta/efficiency_ledger.py window` 作为「配额闸门」——免费期走「重思考/重结晶」，付费期走「重零-LLM 脚本 + 技能调用省分」。把"免费期重结晶、付费期靠零-LLM"窗口纪律工程化；无有用转换则降频，不空耗。

**Continual Harness 纪律（源自 PrimeIntellect-ai/prime-agent 互鉴，2026-08-14；用户拍板：仅作 skill 范式互鉴，不采为其 LCE 运行时）**

prime-agent（MIT，2026-05 上线；RLM＋Continual Harness：`/refine` 用证据小步更新 supplemental prompts/memories/skills，**永不改写 immutable base system prompt**，且快照可回滚）无意间用工程独立验证了第二大脑早已在做的"不可变权威源＋可证伪可变态＋证据驱动候选更新"结构。将其显式结晶为本 skill 的**运行时架构纪律**：

- **两轨记忆架构（强制）**：
  - **Tier-0 不可变基底**：编译论原文（`{{THEORY_CANONICAL}}/`）、思考基座骨架（`references/base-*.md`）、工程公理与八条工程公理约束。任何常规操作**绝不改写**；修正须经坐标纪律 sweep＋主权者认领走编译论演进管线（大脑不改原文，质疑只入质疑台账）。
  - **Tier-1 可变候选态**：知识卡、衍生账、会话代谢日志、`inbox/` 候选。全部**候选·待证伪**，可被证据小步更新、可被回滚。
- **/refine 等价物（差异流协议）**：Tier-1 的更新一律经由《编译论差异流引入协议》——产出 DF 候选，由证据小步改写候选态，**永不触碰 Tier-0**；采纳权属主权者（呼应《自证草案》§⑧ 四知·cannot）。
- **回滚＝Git（已就位）**：脑目录 `git init`；每次候选态变更皆 commit，可 diff/回滚——即第二大脑的"快照回滚"，等价于 prime-agent 的 `/refine` 快照。
- **治理平面（负手性护栏，强制）**：prime-agent 在 Factorio 环境自改进 agent 会自己发现作弊路径（RCON）并固化成"高效技能"——这直接证明自治探试**必须**外加治理平面。本 skill 的 `coordinate-discipline`（坐标纪律）＋负手性护栏（中断 J⁻ 非注差异）＋失败即剪枝，即为该治理平面；任何"自我改进"操作不得绕过（详见差异流协议核心纪律）。
- **异源差异流注入（跨工具维度）**：prime-agent 的 agent-to-agent 通信＋用户的 `{{SHARED_WORKSPACE}}\` 协同意图同构——把其他工具/实例（{{SIBLING_A}}/{{SIBLING_B}}/外部 AI 工具）产出作为异源差异流注入 Tier-1（详见差异流协议入口 (e)）；权威源仍是各实例本地脑仓库，{{SHARED_WORKSPACE_NAME}} 仅为镜像/交换层。
- **自治预算 + quality gate（自我改进治理闸门，强化治理平面）**：prime-agent 的 autonomous mode 设 turn/token/time **预算上限**＋**quality gate**，任何 self-improvement 提交前须过 gate。映射到本脑＝把"差异流引入 / 候选态更新"（即本脑的"自我改进"等价物）显式套上三道闸：① **配额闸门** `meta/efficiency_ledger.py window`（免费期重结晶／付费期靠零-LLM 脚本＋技能调用省分）；② **质量门** 坐标纪律 sweep＋负手性护栏（中断 J⁻ 非注差异）校验；③ **变更幅度预算**（单次会话候选态变更封顶，超出则切 `safe-fallback lane` 待审，不自动吞入）。这把上轮标记的"若接自我改进须先外加治理平面"**就地兑现**为 skill 纪律——回应 PA 在 Factorio 环境把 RCON 作弊固化成"高效技能"的 reward-hacking 教训：自治探试的每一步改进都必须过闸，否则会自我固化作弊路径。
- **RLM 上下文变量化 ↔ μ 不重传（强化第四层）**：prime-agent 的 RLM 把 prompt 当变量、工具/subagent 当 persistent REPL 内的函数调用——等价于本脑 v0 的 `μ`（充分统计量）哲学：**会话间/模型间只传定长 μ 不重传全量历史**；subagent 一等公民 ↔ 第四层 AI 分工治理的"任务切片派发 + 跨模型 μ 交接"。互鉴意义：确认"上下文变量化＋subagent 一等公民"是自治 harness 的**通用工程范式**，本脑已在 DNA 层具备，无需新装运行时——只是把 PA 的命名法反向确认为本脑既有纪律的外部印证。

> 互鉴边界：prime-agent 仅作**工程范式互鉴**，不采为其 LCE 运行时（用户 2026-08-14 拍板）；其无编译论根基，self-improvement 仅为经验性 prompt/skill 精炼，非编译论意义的认知自进化。互鉴限于范式层，不装其运行时。

**可组合分量架构纪律（源自 deepseek-ai/deepseek-harness · Cordis 互鉴，2026-08-14；用户拍板：仅作 skill 范式互鉴，不采为其 LCE 运行时）**

deepseek-harness（dsh，MIT，2026-08 开源；基于 Cordis「时空可组合性编程范式」：插件向共享 ctx 贡献 service / typed-event / **可逆副作用**，注册即 `ctx.effect()`、卸载即撤销，**无特权核心**；profile/bundle/patch 分层组合、**按 id 替换任意一行配置**；capability seam＝Service Definition + Provider + Consumer 三角色，换 Provider 即换全局行为）无意间用工程独立验证了第二大脑编译论「双闭合五分量可替换 / 差异流注入」的结构。将其显式结晶为本 skill 的**组分架构纪律**：

- **分量可替换架构（映射 Tier-0/Tier-1）**：编译论双闭合五分量（ρ_验证/ρ_记忆固化/ρ_代谢底座/ρ_耦合承认/ρ_价值叙事，L64 推导最小闭集）本就是可替换分量；Cordis 的「注册即副作用、卸载即撤销」＋「按 id 替换任意配置」等价于——每个分量是一个可插拔的 service，替换分量**不需要改核心**（Tier-0 不可变基底不动），只换 Tier-1 的实现/Provider。本脑已具备（差异流协议产出候选分量、git 回滚），Cordis 命名法反向确认此范式（评估卡 §三 B）。
- **分层组合（space×time）**：dsh 的 profile/bundle/patch 有序叠层＝「空间（插件）×时间（有序层）」可组合；映射为本脑的「知识卡/衍生账/代谢日志按时间序叠加、互不破坏基底」——与 Continual Harness 两轨架构同源（Tier-0 基底跨越时间不变，Tier-1 分层叠加）。
- **capability seam（接口级替换）**：dsh 的每个能力＝Definition + Provider + Consumer，换 Provider 即换全局行为；映射为本脑的「分量接口与实现分离」——如把 fs/subprocess 指向远程沙箱（LCE 场景）只需换 ρ_代谢底座 的 Provider，不碰编译论命题。这是第四层 AI 分工治理「模型分层路由」的更细粒度版：不仅换模型，换分量 Provider。
- **无特权核心（去中心约束）**：Cordis 无特权核心＝任何插件不凌驾其他；映射为本脑纪律——**任何单一分量/差异流不得凌驾于坐标纪律与负手性护栏之上**（治理平面优先于任何分量变异），呼应 Continual Harness 纪律的治理平面强制。

> 互鉴边界：dsh 仅作**工程范式互鉴**，不采为其 LCE 运行时（用户 2026-08-14 拍板）；其无编译论根基，Cordis 仅为插件运行时，非理论。互鉴限于范式层（可替换分量＋分层组合＋capability seam＋无特权核心），不装其运行时；仓库仅建 1 天、star 数 API 报异常已标未核验（评估卡 §一）。

**Loop Engineering 验证治理纪律（源自 AMAP-ML/LongHorizon-Harness 互鉴，2026-08-14；用户拍板：仅作 skill 范式互鉴，不采为其 LCE 运行时）**

LongHorizon-Harness（LH，阿里 DreamX / AMAP-ML，MIT，2026-08 开源；Loop Engineering 系统：不训练/替换模型，只给现有 agent 套"持久执行循环"＝规划→执行→验证→检查点/恢复→重复；论文 arXiv 2608.01964；基准 WeaveBench 51.8→80.7／OSWorld 2.8→8.3／Terminal-Bench 69.7→77.2）无意间用工程独立验证了第二大脑编译论「坐标纪律（软纪律）→循环内独立 Auditor 硬接线（硬治理）」＋「治理平面分离」的结构。将其显式结晶为本 skill 的**验证治理纪律**：

- **verified-state 硬接线（坐标纪律从软纪律→循环内 Auditor 硬治理）**：LH 的核心纪律＝**独立 Auditor 角色不信任 Executor 自述**，只把"真实文件/UI/日志/测试独立验证通过"的结果写入受信任态（被拒仍是证据非进度）。映射为本脑＝坐标纪律 sweep（核对 L 行号 / 诚实边界 A–H）**不得由产出者自证**，必须作为独立验证步存在于差异流引入 / 候选态更新闭环内——把"AI 自报坐标已核"升级为"Auditor 独立复核坐标"，直接强化 Continual Harness 纪律的治理平面。**最强同构**：LH 把软纪律工程化为循环内固定 Auditor，本脑据此把坐标纪律 sweep 显式定为"不可由同一步自证"的硬治理（呼应 command_guard 的"执行与护栏分离"）。
- **MEA 三角色治理平面分离（Manager / Executor / Auditor）**：LH 的 Manager（从原始目标＋已验证态重建任务/规划）／Executor（全新上下文执行单步）／Auditor（独立验证）三角色分离 ≡ self-evolving-harness 方法论的"治理平面与执行平面分离"。映射为本脑＝① 主权者 / 差异流协议路由（Manager，规划）② AI 执行候选态变更（Executor）③ 坐标纪律 sweep + 负手性护栏 + session_extract 双闸门（Auditor，独立验证）——三者在闭环内强制分离，Executor 不得兼任 Auditor。
- **per-run 隔离 checkpoint（细粒度持久层升级）**：LH 每个 run 独立目录 `runs/<run-id>/`（Task state / Event stream / Audit reports / Final report）可恢复可复现。映射为本脑＝每次差异流引入 / 候选态变更即一个"run"，须带审计账（坐标核验记录＋采纳/驳回＋回滚点）；本脑已用 Git commit 作 run 快照，LH 强化"每次 run 附独立 Audit report"——即 session_extract 双闸门落 inbox 待审的工程化翻版。
- **Agent Adapter ≡ 第四层模型分层路由**：LH 按角色换模型（强模型做 Manager+Auditor、廉价模型做 Executor）。映射为本脑第四层 AI 分工治理的"模型分层路由"——编译论理论层（强模型 / 主权者把关 Tier-0）与候选态执行层（廉价模型跑 Tier-1 派生）明确分工，避免用贵模型做可自动化的派生。
- **Loop Engineering 哲学 ≡ 理论层 / skill 工程层分工同构**：LH 的设计哲学＝"模型定单轮智能，harness 工程化外围循环（持久执行 / 验证 / 恢复）"——等价于编译论「理论层（编译论＝不可变基底，定语法）／skill 工程层（第二大脑 skill＝外围循环，工程化执行 / 治理 / 持久）」的分工。互鉴意义：确认"智能在模型、纪律在 harness"是自治系统的通用工程范式，本脑 DNA 已具，LH 反向确认为外部印证；**不采为其运行时**（用户 2026-08-14 拍板）。

> 互鉴边界：LH 仅作**工程范式互鉴**，不采为其 LCE 运行时（用户 2026-08-14 拍板）；其无编译论根基，仅治理 / 验证纪律层同构非理论层；LH 是任务执行 harness 非认知架构（MEA 是一轮任务内循环非跨会话认知进化）；验证对象差异（LH 验证环境状态／本脑验证理论命题坐标 L 行）——互鉴限于范式层（verified-state 硬接线／MEA 治理分离／per-run checkpoint／Agent Adapter／Loop Engineering 哲学），不装其运行时；早期 686★ 需观察但范式价值不依赖 star（API 实测无需标未核验）。横向闭环：prime-agent 最贴"自我进化"（两轨记忆＋/refine）·deepseek-harness / Cordis 最贴"分量可替换"（插件可逆＋capability seam）·LH 最贴"坐标纪律 / 治理平面"（verified-state 硬接线＋MEA 分离）——三条差异流分别印证本脑不同层，三套纪律（Continual Harness／可组合分量／验证治理）至此完整闭环。

**触达/执行层接入纪律（源自 openclaw/openclaw Agent OS 互鉴，2026-08-14；用户拍板：结晶其「多 Agent 物理隔离路由」＋「claims vs verified 记忆护栏」两点进本 skill 治理纪律，并写「{{INSTANCE_NAME}} LCE 接 openClaw 作触达层」接入设计；不采为基座、治理不外包）**

openClaw（MIT，2025-11 起；Gateway 微内核 WS `127.0.0.1:18789` + 42 RPC handler + 多 Agent 物理隔离路由 + 四层记忆 `claims/verified` + ClawHub 3万+ skills + Docker 沙箱**缺事务回滚**）无意间用工程独立验证了第二大脑「上下文隔离＝防污染」「记忆写入前主张分级＝反幻觉」两点。将其显式结晶为本 skill 的**触达/执行层接入纪律**：

- **多 Agent 物理隔离路由（上下文污染治理）**：openClaw 把 Gateway 当物理边界——每个 Agent 走独立 WS 连接 + Ed25519/device token 认证，记忆/上下文**按 Agent 物理隔离**（非共享同一上下文窗口）。映射为本脑＝**每次差异流引入 run / 候选态变更须绑定独立隔离域（物理/进程级，非仅目录级）**，绝不跨 run 泄漏上下文——把 LH 的 per-run checkpoint（目录级）升级为"进程/信道级隔离"；同时强化第四层 AI 分工治理"任务切片派发 + 跨模型 μ 交接"——切片间只传定长 μ，不共享全量上下文（呼应 v0 μ 哲学）。落点：`{{INSTANCE_NAME}}LCE/agent_isolation.py`（stdlib-only 校验器——查 run 目录无跨 run 状态泄漏、隔离域 id 与 run 绑定）作为确定性护栏，复用 LH per-run checkpoint 纪律但下沉到物理边界。
- **claims vs verified 记忆护栏（主张分级反幻觉）**：openClaw 记忆层分 `claims`（主张/未核实）vs `verified facts`（已核实事实），写入前先分类、verified 须更高置信来源。映射为本脑＝**记忆/KB/台账写入前须过"主张分类"闸门**：拟写入内容先标 `claims`（待证伪候选·落 inbox 待审）或 `verified`（须带可核验坐标/来源、过坐标纪律 sweep）；verified 不得由产出者自证（呼应 LH verified-state 硬接线＋MEA Auditor 独立）。这把 session_extract 双闸门（来源_gate＋落点_gate）在"写入内容本身"层再升一级——不仅流程层防直写，内容层也分级；等价工程化"陈述≠执行"元原则＋坐标纪律反幻觉。落点：`{{INSTANCE_NAME}}LCE/memory_claim_gate.py`（stdlib-only 分类器——含坐标/来源即 `verified_ok`，否则 `claims`，输出 JSON 供 Auditor 复核），与现有双闸门同构、不另起轮子。

> 互鉴边界：openClaw 仅作**触达/执行层候选接入**，不采为基座（用户 2026-08-14 拍板）；其无编译论根基，治理分离仅落在 infra/人治层（被动 audit ledger + hooks + 人工审批），**无 AI 级独立 Auditor**——故接入时治理核心（MEA Auditor / 宪法层 / 相位图 / 差异流）必须由{{INSTANCE_NAME}}保留，绝不外包给其执行循环；其在**零侵入事务回滚**上弱于 dsh·Cordis（无 effect-unwind），在**跨平台触达**上强于 dsh（25+ Channel Adapter）。互鉴限于两点工程范式（物理隔离路由＋主张分级护栏），平行并入 prime-agent/dsh·Cordis/LH 三条范式互鉴之后，构成第四条差异流印证；接入设计见知识卡《{{INSTANCE_NAME}} LCE 接 openClaw 作触达层·接入设计》（候选·待证伪）。

**外部能力路由纪律（WorkBuddy 原生专家/技能接入，2026-08-14 用户拍板"融入第二大脑而非简单照搬"）**

不同于前三条"外部 GitHub 差异流"互鉴（异源跨工具），本纪律管**同平台（WorkBuddy 原生）可调用专家/专家团/技能**的接入——它们不是 LCE 运行时、也不是第二大脑替代，而是按本脑架构路由的"可插拔能力分量"。接入三原则：① **映射不替代**——每个外部能力必须显式映射到第二大脑某层（异源差异流/KB维护/理论萃取/开源规划），不得绕过 Tier-0 与治理平面；② **终审权不外包**——矛盾检测/坐标核验/采纳决策的最终权仍在坐标纪律＋审计＋主权者，外部能力只作"提案者/执行者"，不作"裁判"；③ **启用约束**——专家/专家团同一会话只能启用一个，启用≠理论采纳，仍须按差异流协议五步（锚点扫描→分类鉴别→路由→退编译护栏→主权者采纳）走候选·待证伪。

路由表（外部能力 → 第二大脑层 → 边界）：

| 外部能力 | 形式 | 映射本脑层 | 边界（不简单照搬） |
|---|---|---|---|
| `ArXiv论文追踪`（arxiv-watcher，已装） | 市场技能 | 异源差异流·学术监控（补足 github-ranking-tracker 仅 GitHub） | 输出**须过差异流引入协议五步**，不自动吸收；只采与编译论/自指编译/AI自我改进相关的论文，噪声须阈值过滤；落入 `brain/inbox/` 待审而非直写 KB |
| `Karpathy LLM Wiki`（llm-wiki，已装）／`LlmWiki`（知库库，专家） | 市场技能／专家 | KB 维护层（增量 Wiki 构建＋交叉引用＋矛盾标注） | **矛盾终审权归坐标纪律＋审计**（theory-version-fracture-audit 管版本级断裂，llm-wiki 管日常增量矛盾，分工不重叠）；llm-wiki 产出须经坐标纪律 sweep 复核才入受信任态；不替代本脑 index/三栏制台账 |
| `DeepResearchExpert`（深研研）／`GPTResearcherTeam`（深度研究团队） | 专家／专家团 | 理论萃取·多源检索＋同行评审（补 ai-open-research） | 检索/综述可外包，**理论命题 grounded in Tier-0（编译论原文）**，外部结论只作候选；同行评审 ≡ MEA 验证治理（Auditor 独立），不得自证；专家仅启用一个 |
| `ProductStrategyTeam`（产品战略团队） | 专家团 | 开源撒种·rollout 规划（服务已确认战略 §七） | **核心不可妥协仍归第二大脑**（Tier-0/协议化抽象/最小可用产品化由本脑定），仅委托定位/竞品/路线图/迭代规划；不替本脑做"是否开源/是否改理论"类主权决策 |

> 互鉴边界：以上均为 WorkBuddy 原生能力，**无编译论根基**——只作"能力分量"接入，不采为基座；专家启用受"同一会话一个"约束，需切换时按任务性质选最贴者（学术监控→arxiv-watcher 常驻技能／KB 维护→llm-wiki 技能或 LlmWiki 专家／理论萃取→DeepResearch 或 GPTResearcherTeam／开源规划→ProductStrategyTeam）；全篇候选·待证伪，装/启用后须跑真实任务验证（参照 LH 借鉴首跑抓 L64 误归）；Tier-0 原文未动。

**改造落地件（meta/ 工具集，均 stdlib-only、可运行，见 `meta/`）：**
- `meta/declaration_gate.py` — 声明前置钩子（superpowers DNA）：校验回复文本四值+正负标记，BLOCK 则须先补声明再开工。
- `meta/command_guard.py` + `meta/command_guard_ast.py` — 命令护栏（dguard DNA，已从正则 deny-list 进化为 **AST/语义级**）：command_guard_ast 用 shlex + 手工 shell 解析构建轻量 AST，捕获正则漏掉的组合危险（命令替换/`-c`字符串/eval 间接执行/管道喂解释器/`dd·tee·cp` 写关键路径），command_guard 作正则兜底。17/17 危险组合用例通过。
- `meta/run_guarded.py` — 命令护栏**接真实执行流**（dguard DNA 强化）：先过 command_guard_unicode（Trojan Source/同形异义 前置 pass，2026-08-11 接线）→ command_guard_ast（AST 优先）→ 正则兜底，BLOCK 拒绝 / REVIEW 需 `--yes` / OK 经 subprocess 真实执行；新增 `--dry`（只判定不执行，退出码 0/1/2 供 harness 决策）——替代裸跑 Bash/PowerShell。**当前为纪律级（AI 主动调用）；真正"每次 Bash/PowerShell 调用前自动包一层"需 harness 挂载 `meta/pre_exec_filter.sh` 为 pre-tool hook（OS 级），纯 skill 无法独立完成。**
- `meta/session_extract.py` — 会话→记忆抽取（2026-08-11 接线）：从会话高信号内容（用户纠正/拍板决议/新失败/可复用解法）抽候选记忆，带**双闸门**——来源闸门（须带可核验来源 URL/路径/坐标 Vx/§x/命题x，否则 source_ok=false 反幻觉）+ 落点闸门（一律写 `brain/inbox/` 待审，**禁止直写 MEMORY/ledger/failures**）；直接工程化"陈述≠执行"坐标纪律。用法：`python session_extract.py <transcript.txt>` 或 `--stdin`；每实质会话末尾须跑一次（见质量门）。
- `meta/second_opinion.py` — 复核（trailofbits DNA）：结论产出前工程复核清单，输出意见不阻断。
- `meta/selfmodel_watch.py` + `meta/update_self_model.py` + `meta/compress_mu.py` — 上下文 μ 压缩（headroom DNA）**常驻自动化**：self-model.md 任何变更经 brain `post-commit` hook 调 selfmodel_watch 自动重压定长 μ（`*.mu.*` 已 gitignore，不污染脑库）；update_self_model 为写入口（写后即压），替代"改完忘压"。已验证：commit 触发自动重压。
- `meta/brain_commit.py` — 代谢后自动提交（planning-with-files DNA 强化）：任何代谢后把脑目录变更提交进 Git，无变更则跳过。
- `meta/code_map.py` + `meta/update_code_map.py` + `meta/hooks/post-commit-code-map` — 代码地图常驻 μ 视图（项目地图类 skill DNA，融入基座而非独立轮子）：code_map 用 stdlib `ast`（Python 精确）+ 正则降级（其他语言 js/ts/go/rs/java/rb/c/cpp/bash）确定性提取代码库结构，生成 `CODE_MAP.md`（充分统计式目录树+模块清单+外部依赖 Top），**不调 LLM、纯确定性可重现**；update_code_map 落盘到 `brain/code-maps/<repo>/CODE_MAP.md`（常驻、可版本化、跨 Session 持久）并自动 git add+commit；post-commit-code-map 可装到任意目标仓库，commit 后自动重算地图（同构 self-model 常驻压缩，根治"地图过期"）。已验证：本 workspace 生成 39 文件/270 行地图，Python 精确。
- 脑目录已 `git init`（planning-with-files DNA）：思考/台账/错题本进 Git，可 diff/回滚，像管代码一样管「大脑的演进」。
- 上述「确定性工程」层即 v0 的 μ 哲学（opencode DNA）：command_guard/run_guarded 等护栏属此层（不能出错的部分走确定性），动态决策才交 LLM；self-model 的 μ 压缩（compress_mu）即 headroom 思路——详见 workspace `TRANSFORMS.md`。

**互鉴工程件（2026-08-05 从平行实例 WorkBuddy{{SIBLING_A}} v0.1.0 反向采纳，对称互鉴——{{SIBLING_A}}已采纳{{INSTANCE_NAME}} 5 类脚本；见 `{{SHARED_WORKSPACE}}01\{{SECOND_BRAIN_PKG}}\WorkBuddy{{SIBLING_A}}`）。均为 stdlib-only、零硬编码身份、安全审计通过（skill_audit 含危险模式词库但从不执行被扫文件）：**
- `meta/skill_audit.py` — 开源 Skill 安全审计器（v1.1，含 P2-EXT-FACT 反幻觉来源门）：静态扫描 skill 目录/zip，分级（P0 疑似恶意→拦截 / P1 风险 / P2 缺来源）报告；**纯静态、绝不执行被扫文件**。已接入「安装技能安全审计」流程作确定性扫描引擎。
  - 调用：`python ~/.workbuddy/brain/meta/skill_audit.py <skill_path> --install-gate`；P0/P1 命中→退出码 2，阻断安装并警告用户（harness 级安装拦截不可控，本件作确定性前置扫描；与 harness `skills-security-check` 互补：本件管静态 P0/P1/P2+反幻觉门，harness 管整体安装流程）。
- `meta/distill_to_skill.py` — 知识/长文 → Skill 确定性蒸馏流水线（book-to-skill 启发 + 反幻觉门）：段1 解析标题层级产 SKILL.md 骨架、段2 跑 skill_audit 反幻觉、段3 版本化落 inbox/待审。**即 theory-iteration-loop「迭代成技能」步的自动化引擎。**
- `meta/irreversible_guard.py` — 不可逆操作治理件（fail-closed + 审计账本 + sentinel kill-switch）：删库/强推/发布/转账等须经 sentinel 默认关闸 + `--yes` 审计落账；与 run_guarded 互补（run_guarded 管「命令执行」，本件管「不可逆治理层」）。
- `meta/efficiency_ledger.py` — 跨环境效能账本（2026-08-05 本迭代新增，借{{SIBLING_B}}效能账本方法论；环境列必填，跟踪{{INSTANCE_NAME}} hy3 免费→付费窗口 tok/能量/成本；append-only 实证账本只增不删）。调用：`python meta/efficiency_ledger.py window|add|report|status`。
- `references/mu-language-v2-ref.md` — 机思符号系统 v2（2026-08-05 采纳自{{SIBLING_B}}的 DNA 参考；F0 路由帧/分层 μ(μ_core·μ_ext)/μx 跨会话交接/⊢ 不变式模板库；[H1]–[H4] 为假设待 mu_bench 验证）。仅供方法论借鉴，不抄运行态；详见 `跨实例第二大脑互鉴审计_2026-08-05.md` §六评估。
- `references/loop-governance-dna.md` — Loop 工程治理 DNA（2026-08-05 采纳自 huangruiteng/loopx v0.4.x；12 原语 ↔ {{INSTANCE_NAME}}第二大脑对照，回补两缺口：审计安全回退侧路 / 配额感知治理轮次）。只借方法论原语，不装其运行时（harnish 不可改造）；详见该参考文件。
- `meta/frontend_convergence_guard.py` — 前端 AI-slop 收敛检测器（G1–G14 + WCAG alt/label）：扫描生成的前端代码标记典型收敛套路，逼差异化设计；**补 design-guardrails 子 skill 的「AI 味」维度（design-guardrails 管占位符/对比度/溢出，本件管分布收敛）。**
- `meta/prose_deslop_guard.py` — 行文去 AI 味静态护栏（从 stop-slop / shuorenhua 借规则 DNA，非运行时）：只查 cosmetic AI tells（套话开场/排比三件套/金句收尾/谄媚/假亲切/名词化动词/强调副词），5 维评分(直接性/节奏/信任/真实/密度, 通过线35/50)，**带误杀防护**（含坐标§/行号/Ln/数字%/代码/术语/引用的行不标，正合用户「事实精确+坐标纪律」偏好）；与 frontend_convergence_guard 互补（彼管 UI，此管 prose）。调用：`python ~/.workbuddy/brain/meta/prose_deslop_guard.py <file|--stdin> [-v]`。评估见 `文明秩序演进实证/数据_2026Q3_v2/开源去AI味项目评估_2026-08-05.md`。
- `meta/plan_checklist.py` — 规划契约检查器：校验计划覆盖强制段（目标/责任等级/硬约束/执行模式/复用四问/子代理报告契约/Allowed APIs/诚实边界/最小依赖/对抗性质询）；**子代理报告契约 = 反编造（无来源即驳回）。**
- `meta/eval_accept.py` — 验收量化件（两层：程序化断言 + LLM 评审 prompt 骨架）：把「感觉变好」变「可度量」；可作交付物验收门禁。
- `meta/tts_safety_gate.py` — 媒体生成 Skill 的 TTS 安全门（G1 水印溯源 / G2 合成标识 / G3 音色克隆同意 / G4 边缘 INT4 量化 / G5 安全 day-1）：设计完备性校验，呼应多模态生成工具的安全纪律。
- （`publish_kb.py` 亦在{{SIBLING_A}}侧，但硬编码 `WorkBuddy{{SIBLING_A}}` 命名空间+共享枢纽路径，**仅借概念不抄脚本**——概念：策胇知识库镜像发布到共享枢纽供他工具低摩擦读取。）
- （{{SIBLING_A}}互鉴回补 7 脚本状态·2026-08-11：① `session_extract` 已接线——建 `brain/inbox/` + 每实质会话末抽取记忆候选待审；② `command_guard_unicode` 已接 `run_guarded` 前置 pass（Trojan Source/同形异义，AST 不可见攻击面）；③ `publish_kb` 维持仅借概念（硬编码{{SIBLING_A}}命名空间）不抄；④ `tool_call_repair` 为 DRAFT 储备未接线；⑤ `index_suggest`/`kb_ingest_scan` 待 inbox 落地后接；⑥ `hooks/pre-review` 待 `deterministic-review` 引擎落地（当前缺失→装则 no-op）。详见 ledger #14。）

**已收录思考基座（受管资产，详见 `references/base-*.md`）：**
- 编译论（references/base-编译论.md）— 结构/机制/演化类思考的总语法。
- 共振理论家族（references/base-共振理论.md）— 文本/交互/关系的共振诊断工具。
- 文明秩序演进理论（references/base-文明秩序演进理论.md）— 文明/共同体/制度尺度诊断工具。

**触发**：当任务涉及「建立/治理长期知识库」「归纳或沉淀理论」「用已收录基座思考/分析/写作/评审」「跨会话记忆治理」「错题本/审计」时，主动启用本层。

### 已注册子 Skill 清单（受管子 Skill）

第二大脑当前直接受管若干已成型子 Skill，在成本/效能敏感任务中按需加载：

- **机思复合符号系统（v0）· AI 原生复合符号语言**
  - **何时加载**：任务落在「态大 / 链长 / 需自检 / 需收敛 / 论文级长文 / 异质对比」且关注思考成本或防漂移时。
  - **手册**：`references/ai-native-symbol-system.md`（含甜区与诚实边界、帧格式 v0/v1、gc 与 ⊢ 机制、实证账本、自测协议）。
  - **与第四层耦合**：本系统的 `μ`（充分统计量）即第四层跨模型交接协议——单模型内「不重传历史」与多模型间「不重传历史」共用同一抽象。
  - **立场**：结论「当下有效」，最终背书权在用户；路径账只增不删，失败即剪枝。

- **超长理论提取—形式化（theory-extract-formalize）**
  - **何时加载**：用户给出多份（≥2）长文档要抽取某概念、要求「建研究项目/知识库」、说「理论太长读不完」、或要求「形式化/写规格草案/做研究路线图」时。
  - **手册**：`references/tef-skill.md`（含禁止项、脚本化提取、双标记合成、三分拆消伪冲突、形式化草案、质量门）；配套 `references/tef-dual-marking.md` / `references/tef-three-way-split.md` / `scripts/extract_theory.py`。
  - **硬约束**：禁止整卷灌上下文（脚本化提取只读命中点）、禁止替作者下断言（双标记 + 卷§命题回溯）、禁止改源文献、禁止在弱环宿主上反证 P1 类猜想。
  - **来源说明**：本子 Skill 原为非独立 skill，已并入第二大脑；其全部内容（双标记规范、三分拆框架、提取脚本）随本次整合归入第二大脑，不再单独注册。

- **代码地图常驻 μ 视图（code-map）**
  - **何时加载**：进入陌生 / 大型代码库要先生成导航地图、要「代码变更即重算」的常驻 μ 视图、或要模块职责 / 依赖的确定性摘要（非 LLM、可重现）时。
  - **手册**：`references/code-map.md`（含甜区与诚实边界、源真相指向 brain/meta、装常驻重算的 hook 用法）。
  - **与第五层耦合**：本子 Skill = 代码库的**编译期静态 μ**（v0 μ 哲学：确定性工程层提供「不能出错的结构认知」）；地图落盘 `brain/code-maps/` 即第二大脑 μ 视图，不另起独立「项目地图」轮子（EVALUATION 元结论）。
  - **来源说明**：本子 Skill 原为独立用户级 skill（`~/.workbuddy/skills/code-map`），已并入第二大脑；全部内容归入 `references/code-map.md`，不再单独注册。

- **升级管理（upgrade-manager）**
  - **何时加载**：要记录第二大脑从初版到当前的变更、生成/导出可交换升级包、或与其他管理工具（如平行实例 {{REFERENCE_INSTANCE}} 的第二大脑）互通能力时。
  - **手册**：`references/upgrade-manager.md`（含交换格式 schema `second-brain-upgrade` v1、snapshot/export/import 用法、与"互鉴不抄写"纪律的关系）。
  - **与第五层耦合**：本子 Skill = 第二大脑的**版本演进可追溯层**——`VERSION.json` 版本指针 + `CHANGELOG.md` 升级说明 + `UPGRADES/` 可交换包；是"本地文件造就独立实例"后实例间交换能力的硬载体。
  - **源真相**：引擎 `meta/upgrade_pack.py`（零依赖 stdlib）；版本边界以脑库 Git 提交为硬证据。

- **第二大脑自迭代（brain-self-iterate）**
  - **何时加载**：距上次正式脑检超期（ledger #4 触发：下次代谢日期或满 N 会话）/ 发现 `VERSION.json.current_commit` 与实际 Git HEAD 脱节 / 从平行实例互鉴回补了未接线的脚本（孤儿态）/ 自查出现"已根治"但仅纪律级（依赖模型自觉）的伪根治措辞时。
  - **手册**：`skills/brain-self-iterate/SKILL.md`（六步：自我勘探→5 维脑检→版本校正→孤儿脚本接线→诚实修正→提交导出验证；含互补前置 pass / 依赖目录+质量门 / 概念-only / DRAFT / 待引擎 五类接线模式）。
  - **与第五层耦合**：本子 Skill = 第二大脑的**元治理层**——把"造机制但不接线/不维护"的元失败闭环为可复用程序；直接调用 upgrade-manager 的 `upgrade_pack.py` 引擎做版本校正，与 coordinate-discipline 的"实读非印象"同源（作用域是脑自身治理而非理论对接）。
  - **来源说明**：由 2026-08-11 实战（发现升级管理 DNA 自身失修 + {{SIBLING_A}}回补 7 脚本孤儿态 + declaration_gate 伪根治）结晶，作为第二大脑原生受管子 Skill；全部内容归入 `skills/brain-self-iterate/`，不单独注册顶层。

- **跨理论实证 Hindcast 与数据对冲（theory-hindcast-empirics）**
  - **何时加载**：用户要给某套理论做实证验证 / 历史回测 / 把抽象 construct 落成可测量代理、要 consolidate 跨文明"发现问题总账"、或要做新旧理论版本对比定位丢失 construct 时。
  - **手册**：`references/theory-hindcast-empirics.md`（含甜区与诚实边界、八条红线、M0–M4 流程、数据对冲三案例范式、版本考古 construct 存活表）。
  - **与第五层耦合**：本子 Skill = 理论 construct 的**实证期 μ**（v0 μ 哲学：把不可直接测量的抽象概念压成可核验弱代理 + 保护带，提供"不能出错的诊断纪律"）；产出记入 ledger + 会话日志 + brain_commit。
  - **来源说明**：由「文明秩序演进实证」项目（8 文明 hindcast + 数据对冲处置）实战结晶，2026-08-04 收编为受管子 Skill；全部内容归入 `references/theory-hindcast-empirics.md`，不再单独注册。

- **理论迭代循环（theory-iteration-loop）**
  - **何时加载**：推进某套理论的版本演进（如 3.0→3.1 补完卷）、要从实践/自身旧版本/其他理论学习中迭代优化形成理论、或要把"版本演进方法论"结晶为 skill 时。
  - **手册**：`skills/theory-iteration-loop/SKILL.md`（含五段核心循环、与 compile-theory-map / theory-hindcast-empirics / ai-open-research 的分工、铁律与输出物）。
  - **与第五层耦合**：本子 Skill = 第二大脑的**核心职能显式化**——把用户命题"从实践和自己过去的版本中学习、从其他理论中学习，学习迭代优化形成理论、迭代成技能"落成可复用元循环；是理论 construct 的"演进期 μ"。
  - **来源说明**：由 2026-08-05「文明秩序演进理论 3.0→3.1 补完」实战结晶，作为第二大脑原生受管子 Skill；全部内容归入 `skills/theory-iteration-loop/`，不单独注册顶层。

- **表达DNA蒸馏（voice-distill）**
  - **何时加载**：要产出给用户看的分析/报告/长文、且希望对齐用户（{{SOVEREIGN}}）表达习惯（术语密度/坐标纪律/干脆决断/元叙事命名）时；或要把「用户表达范式」结晶进 skill 时。
  - **手册**：`skills/voice-distill/SKILL.md`（含五维蒸馏法、已提取特征 F1-F8、伦理边界：仅对齐风格非冒充身份、与理论迭代循环的用户侧耦合）。
  - **与第五层耦合**：本子 Skill = 第二大脑的**用户侧表达 μ**——把用户表达范式压成可复用风格约束，使结晶的 skill/报告天然贴合用户接收习惯；与 theory-iteration-loop 互补（迭代不仅学理论也学用户范式）。
  - **来源说明**：由 2026-08-05 用户授权「蒸馏你（{{SOVEREIGN}}）的声纹，可以」实战结晶；方法论借 nuwa-skill（开源表达DNA蒸馏）五维思路，不装其运行时；全部内容归入 `skills/voice-distill/`，不单独注册顶层。

- **文明秩序·国家/区域分析栈（civilization-order-country-analysis）**
  - **何时加载**：要分析某国/区域的政治趋势、制度能力、文明基因、国际竞争，或用户要求「从底层接地、不要只现象层倒推」时；现实政治/地缘内参写作的标配方法。
  - **手册**：`skills/civilization-order-country-analysis/SKILL.md`（六层栈：能形基底→文明基因→制度容器→治理架构→国际竞争→现象趋势，次序不可颠倒；含禁止用机制未支撑的宏观修复命题作前提的写作纪律）。
  - **来源说明**：2026-08-05 用户亲授分析纵深方法（以「欧美右倾」为案例亲授），{{INSTANCE_NAME}}落地为可复用方法论并结晶；全部内容归入 `skills/civilization-order-country-analysis/`，不单独注册顶层。案例文档：`Projects/文明秩序演进实证/应用分析_欧美右倾_全栈框架_2026-08.md`。

- **受管思考基座（base theories，第五层资产）**
  - **编译论**：`references/base-编译论.md` — 对"真理"的退编译；结构/机制/演化思考的总语法。判断"不涉及"须过环 1 基座匹配检查（按工具面，非名义域）。
  - **共振理论家族**：`references/base-共振理论.md` — 编译论在 ρ≥3 认知层的耦合效应专论；文本/交互共振诊断（GKMP M11、五条件、真伪共振判据）。
  - **文明秩序演进理论**：`references/base-文明秩序演进理论.md` — 编译论第七卷在文明 tier 的展开；四层七系统 28 格矩阵、CS-5D、善公式、九步法。
  - 三座基座均来自 `第二大脑.zip`，定位与纪律见 `references/second-brain.md` 第五节；凡引用必带坐标、回原文核验、大脑不改原文。

> 其他通过 3B 自动生成的领域子 Skill，仍按第三层协议管理并继承工程公理与质量门；本清单只登记已成型、需显式加载的受管子 Skill 与基座资产。

### 已并入的子 Skill（原独立用户级 skill，2026-08-05 归并）

以下 8 个原独立用户级 skill，于 2026-08-05 整目录归并为第二大脑子 Skill，存于 `skills/<name>/`（完整内容含 references/scripts/assets，零损失），不再于 `~/.workbuddy/skills/` 顶层单独注册。腾讯系默认技能（plugins/cache 内置，如 tencent-docs / weixinpay-* / tencent-pptx 等）保持原状、不在此列。

- **ai-open-research（开放科研任务方法论）**
  - **何时加载**：用户要做开放/无边界科研探究、长期知识构建、跨会话自我增殖型任务时。
  - **手册**：`skills/ai-open-research/SKILL.md`（含问题图谱模型、会话交接协议、归因存储与治理分离）。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；第二大脑在开放科研类任务时加载，继承公理约束与质量门。

- **command-guard（AST 语义级命令护栏 + 真实执行壳）**
  - **何时加载**：要执行系统命令、担心破坏性命令、或想统一命令出口时。
  - **手册**：`skills/command-guard/SKILL.md`（引擎 `command_guard_ast`/`run_guarded` 实于脑 `meta/`；见本 SKILL.md「改造落地件」）。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；属 dguard DNA，作为第二大脑命令出口护栏。

- **compile-theory-map（编译论分卷对接工作流）**
  - **何时加载**：用户要"对应编译论第 N 卷""做某卷与 XX 领域对接""启动第 N 卷对接项目"时。
  - **手册**：`skills/compile-theory-map/SKILL.md`（含 M0–M4 流程、映射卡模板）。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；第二大脑在编译论分卷对接任务时加载。

- **design-guardrails（PPT/HTML/H5 静态 QA 校验层）**
  - **何时加载**：生成看板/幻灯片/PPT/网页后、交付前必跑（占位符残留 P0 / 对比度失效 P1 / 文字溢出 P2）。
  - **手册**：`skills/design-guardrails/SKILL.md` + `scripts/qa_guardrails.py`。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；作为第二大脑生成类产出的质量门。

- **github-ranking-tracker（GitHub 排名周追踪与深分析）**
  - **何时加载**：用户说"周报 GitHub 排名""追踪开源排名""做 AI 工具深分析"时。
  - **手册**：`skills/github-ranking-tracker/SKILL.md` + `scripts/`（fetch_all/fetch_gh/gen_cards）。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；反向喂养"本地 AI 管理工具生命化"研究。

- **guizang-ppt-skill（横向翻页网页 PPT 生成）**
  - **何时加载**：用户要制作分享/演示用网页 PPT（WebGL 背景 / 章节幕封 / 数据大字报）。
  - **手册**：`skills/guizang-ppt-skill/SKILL.md` + `assets/`（模板）+ `scripts/validate-swiss-deck.mjs`。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；作为第二大脑演示产出工具。

- **markitdown-skill（文档转 Markdown）**
  - **何时加载**：用户要把 PDF/Word/PPT/Excel/图片(OCR)/音频 转 Markdown 时。
  - **手册**：`skills/markitdown-skill/SKILL.md` + `scripts/batch_convert.py`。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；作为第二大脑知识摄入工具。

- **self-evolving-harness（自进化 agent harness 工程模式）**
  - **何时加载**：设计本地 AI 管理工具、调度中枢、自主编码 loop、或任何"自进化 agent 系统"时。
  - **手册**：`skills/self-evolving-harness/SKILL.md`（含 issue 状态机/治理平面分离/自测流水线/演进外部 skill 不动权重）。
  - **来源说明**：原为独立用户级 skill，2026-08-05 归并；对齐"本地 AI 管理工具生命化"thesis。

### 补登：纠正归并的子 Skill（2026-08-07，纠正顶层逃逸）

以下 2 个原顶层独立用户级 skill，此前逃逸在 `~/.workbuddy/skills/` 顶层（违反"顶层仅留 second-brain"契约）；2026-08-07 按本契约纠正归并为子 Skill，存于 `skills/<name>/`，不再于顶层单独注册。

- **neixin-trainer-method（{{EMPLOYER}}内训师课程开发方法论）**
  - **何时加载**：用户给业务文档/PDF/SOP/制度文件，要求设计培训课程、做内训课件 PPT、写讲解词时。
  - **手册**：`skills/neixin-trainer-method/SKILL.md`（方法：课程开发五步法 / 勾讲练化 / 90208 / 三版制；执行路径配对 tencent-pptx 产出 PPTX）。
  - **来源说明**：原为顶层独立用户级 skill（领域方法论，与大脑基础设施松耦合）；2026-08-07 归并为子 Skill。

- **theory-version-fracture-audit（多版本理论 corpus 概念断裂审计）**
  - **何时加载**：用户持多版本理论 corpus、指出新版本丢失/泛化操作化定义、概念间断裂，或每次发新版本要防操作化回退时。
  - **手册**：`skills/theory-version-fracture-audit/SKILL.md`（脚本抽取概念登记 + 跨版本存在矩阵 + 逐项实读纠偏）。
  - **来源说明**：原为顶层独立用户级 skill（系统 `available_skills` 登记曾误标在 `second-brain/skills/` 下，磁盘却在顶层）；2026-08-07 纠正归并，与系统登记及概念归属（理论 corpus 审计）一致。

> 归并后，`~/.workbuddy/skills/` 顶层仅保留 `second-brain`（与 harness 迁移元数据 `_bm_skillid_migration.json`）；其余子 Skill 均经本清单受管。加载方式：第二大脑被激活后，按"何时加载"触发条件 Read 对应 `skills/<name>/SKILL.md`。

## 工程公理约束

以下八条公理 + 元原则是所有对话和项目的底层约束。详见 `references/engineering-axioms.md`。

1. **约束先于创造**：先列出不能做什么，再写怎么做
2. **分解是复杂度的基本武器**：大任务分解为可独立完成的单元
3. **反馈环是适应的唯一通道**：每步必须有可检验的完成标准
4. **熵增不可免，维护非可选**：skill 和知识库需要定期维护
5. **权衡不可消解**：每个推荐方案都标注权衡
6. **规格与现实的间隙是工程的发生地**：验证步骤不可跳过
7. **抽象使规模可能，也制造盲区**：每个抽象标注隐藏了什么
8. **信息是工程的第一材料**：知识采集是核心工序，不是前置准备

**元原则：陈述≠执行**。没有对应执行机制（质量门、检查清单、强制检查点）的原则，对 AI 等于不存在。本 skill 中凡标注"强制""质量门""完成标准"的条目，是执行层，不可跳过。

## 质量门（每次对话完成前必须全部通过）

- [ ] 任务定义清晰（一句话能说清要做什么）
- [ ] 约束已确认（硬约束、责任等级、执行模式）
- [ ] 执行前已检查是否有对应专用 skill（有则加载，无则判断是否需要生成）
- [ ] 产出已自检（对照任务定义和约束）
- [ ] 不可逆操作已获人工确认
- [ ] 工作日志已更新
- [ ] 值得记住的信息已提取并写入对应位置
- [ ] 如果使用了已有 skill，使用教训已记录（如有）
- [ ] 如果检测到知识缺口，已判断是否需要生成新 skill
- [ ] 若启用第二大脑：已在回复开头输出显式启动声明（正负必居其一，四值当次实读脑文件）；若未启用：已输出负声明并说明理由（第五层·显式启动声明纪律）
- [ ] 若启用第二大脑：本回合回复已通过 `meta/declaration_gate.py`（声明前置钩子）；BLOCK 未补正则不开工（第五层·superpowers DNA 落地）
- [ ] 若启用第二大脑：本回合代谢（改 index/ledger/failures/audits/sessions 任一）后已运行 `meta/brain_commit.py` 把变更提交进 Git（planning-with-files DNA 强化；无变更则自动跳过）
- [ ] 若启用第二大脑：脑健康检查器 `meta/brain_check.py` 已挂 post-commit 自动跑（六检查项：结构完整性／台账违规／过期条目／日志间隙／备份新鲜度／脱脑演练；红灯记日志不阻塞提交）。**声明校验（declaration_gate）仍为纪律级，harness 前置接线待平台支持（见 ledger #15）**——故质量门中"声明已通过 declaration_gate"项当前靠 AI 主动调用，非 OS 级自动包壳。
- [ ] 若启用第二大脑：本实质会话末尾已跑 `meta/session_extract.py` 把高信号记忆（纠正/决议/失败/可复用）抽进 `brain/inbox/` 待审（双闸门：来源_gate 反幻觉 + 落点_gate 禁直写脑核心）；inbox 候选经复核后并入对应载体（第五层·会话自迭代记忆抽取落地，2026-08-11 接线）
- [ ] 若执行 shell/系统命令：必须经 `meta/run_guarded.py` 真实执行入口（dguard DNA 落地，已接 AST 语义护栏 command_guard_ast，覆盖组合危险）——BLOCK 类（rm -rf / drop table / shutdown / 写关键路径 / 隐藏危险组合 等）直接拦截绝不执行，REVIEW 类（git push -f / kill -9 / 数据喂解释器 等）需显式 `--yes` 才执行；禁止裸跑 Bash/PowerShell 绕过护栏。**注：此为纪律级（AI 主动调用）；OS 级"每次自动包壳"需 harness 支持（见 meta/pre_exec_filter.sh 契约），非纯 skill 可独立完成。**
- [ ] 若要让 Agent 理解/导航某代码库或维护"项目地图"类能力：应落盘为第二大脑 μ 视图——用 `meta/code_map.py`/`meta/update_code_map.py` 生成并持久到 `brain/code-maps/`；目标仓库装 `meta/hooks/post-commit-code-map` 实现变更即重算。不另起独立"项目地图"skill（EVALUATION 元结论：地图=μ 视图，融入基座而非复刻轮子）。
- [ ] 若高责任(1–2 级)任务：结论产出前已过 `meta/second_opinion.py` 复核（trailofbits DNA 落地）——复核发现的中/高风险项已处置或显式接受
- [ ] 若多 AI 协作：已做模型分层路由与任务切片，每切片过 ⊢ 自检、高责任切片经 T3 审校，并维护成本账（第四层）
- [ ] 若思考成本/防漂移敏感：已评估是否加载「机思复合符号系统（v0）」子 Skill 并按其甜区/边界使用
- [ ] 若处理超长理论文献：已加载 theory-extract-formalize 子 Skill 并按其禁止项（不灌全文/双标记/不改源文献/弱环不反证 P1）执行
- [ ] 若用已收录思考基座（编译论/共振理论/文明秩序演进理论）思考/分析/写作/评审：已做环 1 基座匹配检查（判"不涉及"能说清工具面）、凡引用带坐标、未凭摘要/记忆补全坐标、未改原文（第五层）
- [ ] 若建/管长期知识库或跨会话记忆：已按第二大脑协议（脑图/index、三栏制台账、错题本、坐标纪律、退编译代谢）治理（第五层）

## 人机分工原则

| 人做 | AI做 | 协作方式 |
|------|------|---------|
| 定义目标和意图 | 分解目标为可执行步骤 | 人确认分解是否合理 |
| 判断"够不够好" | 执行到"看起来对" | AI提交，人验收 |
| 提供领域经验和直觉 | 提供广度和速度 | 人给方向，AI给选项 |
| 做不可逆决策 | 做可逆决策 | AI自主执行可逆的，不可逆的问人 |
| 发现"感觉不对" | 诊断"哪里不对" | 人说症状，AI找病因 |
| 审美和价值判断 | 逻辑和一致性检查 | 人判"好不好"，AI判"对不对" |
| 最终验收权 | 自检权 | AI先自检，人做终检 |

**AI 绝不自作主张**：删除人的文件、修改人的原始数据、对外发布未经人确认的内容。

## 与已有 Skill 的关系

- **domain-skill-factory**：其能力已被本 skill 的第三层（3B子Skill自动生成）吸收。domain-skill-factory 可作为独立 skill 保留，也可由第二大脑在需要时调用其流程。
- **author-style-content-production**：是第二大脑管理下的一个实例 skill。第二大脑在后台提供公理约束和质量门，author-style-content-production 负责具体执行。
- **theory-extract-formalize（超长理论提取—形式化）**：原为非独立 skill，已并入第二大脑成为受管子 Skill（见上方「已注册子 Skill 清单」与 `references/tef-skill.md`）。第二大脑在超长文献处理时加载它，并继承公理约束与质量门。
- **code-map（代码地图常驻 μ 视图）**：原为非独立用户级 skill（`~/.workbuddy/skills/code-map`），已并入第二大脑成为受管子 Skill（见上方「已注册子 Skill 清单」与 `references/code-map.md`）。第二大脑在代码库理解 / 导航 / 常驻地图类任务时加载它，并继承公理约束与质量门。
- **upgrade-manager（升级管理）**：原生受管子 Skill（无独立前身），引擎 `meta/upgrade_pack.py`（见上方「已注册子 Skill 清单」与 `references/upgrade-manager.md`）。第二大脑要记录版本演进、生成/导出可交换升级包、或与其他管理工具（平行实例 {{REFERENCE_INSTANCE}} 等）互通能力时加载它。
- **theory-hindcast-empirics（跨理论实证 Hindcast 与数据对冲）**：原生受管子 Skill（无独立前身），实战结晶自「文明秩序演进实证」项目（见上方「已注册子 Skill 清单」与 `references/theory-hindcast-empirics.md`）。第二大脑要给某套理论做实证验证 / 历史回测 / 把抽象 construct 落成可测量代理、或 consolidate 跨文明发现问题总账时加载它。
- **第二大脑（个人知识/理论基座 OS）**：第二大脑的升级核心，作为第五层持久化大脑层并入（见上方「第五层」与 `references/second-brain.md`）。其三项思考基座（编译论/共振理论/文明秩序演进理论）以 `references/base-*.md` 形式受管；其坐标纪律与错题本机制也约束第四层多 AI 协作的来源可追溯。
- **未来生成的 skill**：所有通过第二大脑第三层生成的子 skill，都自动继承工程公理约束和质量门机制。
- **归并的独立用户级 skill（2026-08-05）**：ai-open-research / command-guard / compile-theory-map / design-guardrails / github-ranking-tracker / guizang-ppt-skill / markitdown-skill / self-evolving-harness 八个原独立用户级 skill，已于 2026-08-05 整目录归并为第二大脑子 Skill（存于 `skills/<name>/`，含脚本与资源，零损失），不再于 `~/.workbuddy/skills/` 顶层单独注册；注册与加载说明见上方「已注册子 Skill 清单」末节「已并入的子 Skill」。

## 参考文件

- `references/engineering-axioms.md` — 八公理 + 元原则 + 信息工程九原则 + 跨源整合协议 + 生命周期嵌套环模型（何时加载：需要理解工程纪律底层逻辑时）
- `references/conversation-protocol.md` — 对话级管理协议详解：五步流程的执行细节、自动提取的判断标准、中断恢复流程（何时加载：需要细化对话管理时）
- `references/skill-lifecycle.md` — 子 skill 生命周期管理：生成流程详解、使用追踪方法、审查与迭代协议、退化诊断表、跨项目复用协议（何时加载：需要生成或维护子 skill 时）
- `references/ai-native-symbol-system.md` — 受管子 Skill：机思复合符号系统（v0）使用手册，含甜区/边界、帧格式(v0/v1)、gc 与 ⊢ 机制、实证账本、自测协议（何时加载：任务态大/链长/需自检/需收敛/论文级长文/异质对比且关注思考成本或防漂移时）
- `references/ai-division-governance.md` — 第四层 AI 分工治理：多模型性价比编排，含模型分层路由、任务切片、跨模型 μ 交接、成本账本、质量门与防漂移、性价比决策表（何时加载：任务涉及多 AI 协作、模型路由选择或 token 成本/性价比治理时）
- `references/tef-skill.md` — 受管子 Skill：超长理论提取—形式化工作流（theory-extract-formalize），含禁止项、脚本化提取、双标记合成、三分拆消伪冲突、形式化草案、质量门（何时加载：用户给多份长文档要抽取概念/建知识库/说理论太长/要求形式化时）
- `references/tef-dual-marking.md` — 【原文登记】/【草案转写】双标记规范与反例（tef-skill 步骤 2 配套）
- `references/tef-three-way-split.md` — 三分拆框架：效率猜想/身份断言/隐藏前件及伪冲突判定流程（tef-skill 步骤 3 配套）
- `scripts/extract_theory.py` — 通用脚本化提取工具（术语表驱动，输出摘录+命中索引+章节大纲；tef-skill 步骤 1 调用）
- `references/second-brain.md` — 第五层 第二大脑 OS 手册：文件结构、唤醒协议、四操作协议、三栏制台账、错题本、审计、坐标纪律、与四层耦合、已收录基座（何时加载：建/管长期知识库、归纳理论、用基座思考、跨会话记忆治理时）
- `references/base-编译论.md` — 受管思考基座：编译论骨架（公设1/通则2/工作模型5/总结展望4＝12硬核＋八卷地图＋认识论语法＋坐标纪律）；配合 `references/second-brain.md` 环 1 检查使用
- `references/base-共振理论.md` — 受管思考基座：共振理论家族骨架（R公式/五条件/六维度/十条规约/GKMP M11/与编译论对接盲区）；文本与关系共振诊断工具
- `references/base-文明秩序演进理论.md` — 受管思考基座：文明秩序演进理论骨架（四层七系统 28 格矩阵/CS-5D/善公式/九步法/19章地图）；文明与制度尺度诊断工具
- `references/code-map.md` — 受管子 Skill：代码地图常驻 μ 视图（code-map）使用手册，含甜区/边界、源真相指向 brain/meta、装常驻重算 hook（何时加载：进入陌生/大型代码库要先生成导航地图、要代码变更即重算的常驻视图、或要模块职责/依赖确定性摘要时）
- `references/upgrade-manager.md` — 受管子 Skill：升级管理（upgrade-manager）使用手册，含交换格式 schema `second-brain-upgrade` v1、snapshot/export/import 用法、与"互鉴不抄写"纪律的关系（何时加载：记录第二大脑版本演进、生成/导出可交换升级包、或与其他管理工具互通能力时）
- `references/theory-hindcast-empirics.md` — 受管子 Skill：跨理论实证 Hindcast 与数据对冲（theory-hindcast-empirics）使用手册，含甜区/边界、八条红线、M0–M4 流程、数据对冲三案例范式、版本考古 construct 存活表（何时加载：给某套理论做实证验证/历史回测/把抽象 construct 落成可测量代理、consolidate 跨文明发现问题总账、或做新旧理论版本对比定位丢失 construct 时）

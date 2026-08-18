# 实现说明与互鉴来源（implementation-notes）

> ⚠️ **诚实边界**：本节记录框架在私有实例中的「工程落地件」与「外部互鉴来源」，供深度读者追溯。其中部分 `meta/*.py`（如 `declaration_gate` / `command_guard` / `session_extract` / `second_opinion` 等）为**私有脑资产**，本开源纯净包**仅随附** `meta/brain_check.py` `brain_commit.py` `brain_offline_drill.py` `export_second_brain.py` `upgrade_pack.py` 及 `meta/hooks/post-commit` 等可移植脚本。接入时**请以本仓库 `meta/` 实际文件为准**，不要假设下列所有脚本都已随包发布。

---

## 改造落地件（meta/ 工具集，均 stdlib-only、可运行）

- `meta/declaration_gate.py` — 声明前置钩子（superpowers DNA）：校验回复文本四值+正负标记，BLOCK 则须先补声明再开工。
- `meta/command_guard.py` + `meta/command_guard_ast.py` — 命令护栏（dguard DNA，已从正则 deny-list 进化为 **AST/语义级**）：command_guard_ast 用 shlex + 手工 shell 解析构建轻量 AST，捕获正则漏掉的组合危险（命令替换/`-c`字符串/eval 间接执行/管道喂解释器/`dd·tee·cp` 写关键路径），command_guard 作正则兜底。17/17 危险组合用例通过。
- `meta/run_guarded.py` — 命令护栏**接真实执行流**（dguard DNA 强化）：先过 command_guard_unicode（Trojan Source/同形异义 前置 pass）→ command_guard_ast（AST 优先）→ 正则兜底，BLOCK 拒绝 / REVIEW 需 `--yes` / OK 经 subprocess 真实执行；新增 `--dry`（只判定不执行）。**当前为纪律级（AI 主动调用）；真正「每次 Bash/PowerShell 调用前自动包一层」需 harness 挂载 `meta/pre_exec_filter.sh` 为 pre-tool hook（OS 级），纯 skill 无法独立完成。**
- `meta/session_extract.py` — 会话→记忆抽取：从会话高信号内容抽候选记忆，带**双闸门**——来源闸门（须带可核验来源，否则 source_ok=false 反幻觉）+ 落点闸门（一律写 `brain/inbox/` 待审，禁止直写 MEMORY/ledger/failures）。
- `meta/second_opinion.py` — 复核（trailofbits DNA）：结论产出前工程复核清单，输出意见不阻断。
- `meta/selfmodel_watch.py` + `meta/update_self_model.py` + `meta/compress_mu.py` — 上下文 μ 压缩（headroom DNA）**常驻自动化**。
- `meta/brain_commit.py` — 代谢后自动提交：任何代谢后把脑目录变更提交进 Git，无变更则跳过。**（本开源包已随附）**
- `meta/code_map.py` + `meta/update_code_map.py` + `meta/hooks/post-commit-code-map` — 代码地图常驻 μ 视图。**（post-commit-code-map 思路同本包随附的 post-commit 钩子）**
- 脑目录已 `git init`：思考/台账/错题本进 Git，可 diff/回滚。
- 上述「确定性工程」层即 v0 的 μ 哲学（opencode DNA）。

## 互鉴工程件（2026-08-05 从平行实例反向采纳，对称互鉴；均为 stdlib-only、零硬编码身份、安全审计通过）

- `meta/skill_audit.py` — 开源 Skill 安全审计器（v1.1，含 P2-EXT-FACT 反幻觉来源门）：静态扫描 skill 目录/zip，分级（P0 疑似恶意→拦截 / P1 风险 / P2 缺来源）报告；**纯静态、绝不执行被扫文件**。
- `meta/distill_to_skill.py` — 知识/长文 → Skill 确定性蒸馏流水线。
- `meta/irreversible_guard.py` — 不可逆操作治理件（fail-closed + 审计账本 + sentinel kill-switch）。
- `meta/efficiency_ledger.py` — 跨环境效能账本（跟踪 hy3 免费→付费窗口 tok/能量/成本；append-only 实证账本只增不删）。
- `references/mu-language-v2-ref.md` — 机思符号系统 v2（仅供方法论借鉴，不抄运行态）。
- `references/loop-governance-dna.md` — Loop 工程治理 DNA（12 原语 ↔ 第二大脑对照）。
- `meta/frontend_convergence_guard.py` — 前端 AI-slop 收敛检测器。
- `meta/prose_deslop_guard.py` — 行文去 AI 味静态护栏（5 维评分，带误杀防护）。
- `meta/plan_checklist.py` — 规划契约检查器。
- `meta/eval_accept.py` — 验收量化件（程序化断言 + LLM 评审 prompt 骨架）。
- `meta/tts_safety_gate.py` — 媒体生成 Skill 的 TTS 安全门。

---

## 互鉴纪律（外部差异流 → 本框架治理纪律）

> 以下五条「互鉴纪律」均为**工程范式互鉴**，不采为运行时；每条都明确标注了「互鉴边界」。它们把外部开源项目的工程经验反向确认为本框架既有纪律的外部印证。

### Continual Harness 验证治理纪律（源自 prime-agent / deepseek-harness 互鉴）

- **verified-state 硬接线**（坐标纪律从软纪律→循环内 Auditor 硬治理）：独立 Auditor 角色不信任 Executor 自述，只把「真实文件/UI/日志/测试独立验证通过」的结果写入受信任态。
- **MEA 三角色治理平面分离**（Manager / Executor / Auditor）：主权者/差异流协议路由（Manager）＋ AI 执行候选态变更（Executor）＋ 坐标纪律 sweep + 负手性护栏 + session_extract 双闸门（Auditor），三者强制分离。
- **per-run 隔离 checkpoint**：每次差异流引入 / 候选态变更即一个「run」，须带审计账（坐标核验记录＋采纳/驳回＋回滚点）。
- **Agent Adapter ≡ 第四层模型分层路由**：按角色换模型（强模型做 Manager+Auditor、廉价模型做 Executor）。

### 可组合分量架构纪律（源自 deepseek-harness / Cordis 互鉴）

- **分量可替换架构**（映射 Tier-0/Tier-1）：每个分量是一个可插拔的 service，替换分量不需要改核心（Tier-0 不可变基底不动）。
- **分层组合**（space×time）：知识卡/衍生账/代谢日志按时间序叠加、互不破坏基底。
- **capability seam（接口级替换）**：分量接口与实现分离，换 Provider 即换全局行为。
- **无特权核心（去中心约束）**：任何单一分量/差异流不得凌驾于坐标纪律与负手性护栏之上。

### Loop Engineering 验证治理纪律（源自 LongHorizon-Harness 互鉴）

- **verified-state 硬接线** / **MEA 三角色治理平面分离** / **per-run checkpoint** / **Agent Adapter ≡ 第四层模型分层路由** / **Loop Engineering 哲学 ≡ 理论层 / skill 工程层分工同构**。
- 互鉴意义：确认「智能在模型、纪律在 harness」是自治系统的通用工程范式。

### 触达 / 执行层接入纪律（源自 openClaw 互鉴）

- **多 Agent 物理隔离路由**（上下文污染治理）：每次差异流引入 run / 候选态变更须绑定独立隔离域（物理/进程级，非仅目录级）。
- **claims vs verified 记忆护栏**（主张分级反幻觉）：记忆/KB/台账写入前须过「主张分类」闸门。

### 外部能力路由纪律（WorkBuddy 原生专家/技能接入）

- 映射不替代：每个外部能力必须显式映射到第二大脑某层，不得绕过 Tier-0 与治理平面。
- 终审权不外包：矛盾检测/坐标核验/采纳决策的最终权仍在坐标纪律＋审计＋主权者。
- 启用约束：专家/专家团同一会话只能启用一个；启用≠理论采纳，仍须按差异流协议五步走候选·待证伪。

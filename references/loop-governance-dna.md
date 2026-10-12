# Loop 工程治理 DNA（源自 huangruiteng/loopx，v0.4.x）

> **互鉴纪律（实例化守卫）**：LoopX 是外部开源项目（MIT，agent 无关本地控制平面），本文件**只借鉴其方法论原语**，不安装其运行时（WorkBuddy harness 不可改造，且 LoopX 需 Codex/Claude Code 宿主调度 / cron）。所引原语与{{INSTANCE_NAME}}第二大脑既有治理对照，标注〔已具备〕/〔缺口〕/〔借鉴〕。本文件为 DNA 参考，非运行态拷贝。

## 一、LoopX 状态内核 12 原语 ↔ {{INSTANCE_NAME}}第二大脑对照

| # | LoopX 原语 | {{INSTANCE_NAME}}对应 | 状态 |
|---|---|---|---|
| 1 | Lifetime Goal Invariant（目标为不变式，所有状态围绕其投影） | `ledger.md` #N 活跃目标 + 收敛阶梯 | 〔已具备〕 |
| 2 | Agent-Native Kanban（卡片带 identity/authority/evidence/continuation） | TaskCreate 任务卡 + `sessions/` + `audits/` 证据 | 〔已具备〕 |
| 3 | Concrete User Gates（具体门禁替代模糊等待） | `command_guard`(OK/REVIEW/BLOCK) / `irreversible_guard`(fail-closed) / `skills-security-check`(P0 拦截) | 〔已具备〕 |
| 4 | Peer Claims & Leases（无 leader，依声明/租约定序） | 单实例，无多 agent 对等 | 〔不适用〕 |
| 5 | **Audited Safe Fallback（阻塞时隔离审计回退，不破门禁）** | 无显式"安全侧路"概念 | 〔缺口→借鉴〕 |
| 6 | **Quota-Aware Scheduling（先查配额，验证后计费）** | `efficiency_ledger.py` 记账，但无 `should-run` 决策 | 〔部分→借鉴〕 |
| 7 | Evidence-Backed Writeback（回写须验证方成证据） | `brain_commit` + `audits/`（非强制门） | 〔已具备·强化〕 |
| 8 | Read-First Management Surface（面板只读，内核权威） | `index.md`/`ledger.md` 为权威，`present_files` 仅展示 | 〔已具备〕 |
| 9 | Public/Private Boundary（私有状态不公开） | `.git` 提交锁 / 不抄他人脑运行态 | 〔已具备〕 |
| 10 | Capability Transition Typing（能力调用结果类型化） | 无形式化 | 〔借鉴·可选〕 |
| 11 | Compact Run History / decision lineage | `sessions/` + `audits/audit-log.md` | 〔已具备〕 |
| 12 | Governed Turn（验证收据+新鲜配额+中立预算→纯边界轮次） | 第二大脑启动声明 + 配额检查 | 〔已具备·强化〕 |

## 二、两个值得回补的缺口（已写入第二大脑纪律）

### 缺口 A：审计安全回退侧路（Audited Safe Fallback Lanes）
- **LoopX 做法**：当用户门禁阻塞某条高优先级 lane，一条**单独审计的安全回退**可继续推进低风险工作，但**不得绕过该门禁**。
- **{{INSTANCE_NAME}}借鉴（已落地为纪律）**：当因等待用户拍板（如 3.1 §6 机思升级、Serena 配置）而某 lane 阻塞时，显式切到「已审计安全侧路」——做低风险、可回退、不依赖该门禁的工作（写文档 / 结晶 skill / 补参考 / 跑零-LLM 脚本），并在会话日志标注 `safe-fallback lane`。
- 价值：避免"等拍板=闲置"，把阻塞期变成可审计的产出期。

### 缺口 B：配额感知治理轮次（Quota-Aware Governed Turn）
- **LoopX 做法**：每个自动 turn 先 `quota should-run`（查配额），仅验证回写后 `spend-slot`；无有用转换则安静跳过。
- **{{INSTANCE_NAME}}借鉴（已落地为纪律）**：把 `efficiency_ledger` 从"事后记账"升级为"事前门"——每次实质会话开场，除启动声明四值，增加第 5 值**「配额闸门」**：依据 `efficiency_ledger window`（免费期/付费期窗口 + 本次任务预估成本）决定走「重思考/重结晶」还是「重零-LLM 脚本 + 技能调用省分」。
- 价值：把用户定的"免费期重结晶、付费期靠零-LLM"窗口纪律**工程化**。

## 三、诚实边界（LoopX 明示 NOT，与{{INSTANCE_NAME}}纪律同构）
- NOT 授予凭证 / NOT 批准破坏性操作 / NOT 代表用户发布 / NOT 把未验证运行当成功证据 → 同构于 `command_guard`(BLOCK/REVIEW) + `irreversible_guard`(fail-closed) + `skills-security-check`(P0 拦截)。
- **结论**：LoopX 的诚实边界与我既有护栏**同构**，无需新增，仅作外部印证。

## 四、不采纳项（实例化守卫）
- **不安装 LoopX 运行时**：它需宿主调度（Codex App automation / cron）+ 持久 `.loopx/` 状态；WorkBuddy harness 不可改造，且{{INSTANCE_NAME}}第二大脑已是等效控制平面（ledger+sessions+audits+brain_commit+efficiency_ledger）。只借原语 DNA。
- **不抄 LoopX 的运行态**（无本机实例；其 `ledger`/`sessions` 属他人运行态，抄之即伪造动态脑值）。

## 五、对 Serena（oraios/serena）的对照注记
- Serena 是 **MCP 工具**（语义代码检索/编辑），非 skill、非状态内核；与 LoopX 不同轴。
- 其"symbol-level retrieval / IDE for agent"能力补{{INSTANCE_NAME}}在**大而无法通读的代码库**上的短板（跨文件重命名、引用查找、类型层级、依赖跳转），grep/code-explorer 在大规模陌生仓库上偏弱。
- 代价：需 `uv` + 各语言 LSP 本地安装、持久外部进程；对{{INSTANCE_NAME}}典型的小规模自有代码/理论文件边际收益低。
- 处置：作为**可选 MCP 连接器**候选（不违反"技能只作第二大脑子技能"纪律，因 MCP 连接器≠skill），待用户拍板是否配置。

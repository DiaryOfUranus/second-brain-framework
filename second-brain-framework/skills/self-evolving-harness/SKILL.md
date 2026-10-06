---
name: self-evolving-harness
description: 构建/评审"自进化智能体 harness"的工程模式参考——issue 状态机 + 治理平面分离 + 自测流水线 + 演进外部 skill 不动权重。当设计本地 AI 管理工具、调度中枢、自主编码 loop 或任何"自进化 agent 系统"时调用，对齐"本地AI管理工具生命化"thesis 与判词四落点。
---

# Self-Evolving Agent Harness 工程模式

## 何时用
设计或评审一个能"自进化"的 agent 系统时（本地 AI 管理工具 / 调度中枢 / 自主编码 loop），用本 skill 核对架构是否具备生产级自进化所需的四个部件，并对照实证 `oh-my-cli`（qwen-code-dev-bot/oh-my-cli，428 commits 全公开）。

## 四部件（生产级自进化 harness 必备）
1. **循环工程（Loop Engineering）**：issue 状态机 `ready → leased → active` + dispatcher + monitor + watchdog 合一执行循环。需求→issue→agent 认领→实现→E2E+CI→PR 合并。
2. **自测流水线（Self-testing）**：每次更新触发 Build / Unit Test / E2E / (Desktop) Lifecycle 验证；异常路由回 issue/PR 修复重验。这是"出口审计 / 质量分级"的操作版。
3. **多源进化（Multi-source Evolution）**：社区经验 + 用户/开发者反馈 → 可执行工作 → 演进**程序性命令 / skill**（如 /goal /resume / Dynamic Workflow / Session Replay）。演进**外部固退（代码/skill/issue），不碰模型权重**。
4. **治理平面分离（宪法权禁授）**：AUTONOMY.md + policy + CODEOWNERS + workflows 构成受保护治理平面，由人持有；运营 Bot 可提议治理变更但**不可自行应用**。即"裁判与选手分离"。

## 对齐判词四落点（本地AI管理工具生命化）
- 落点1 两端管辖：入口＝issue 规范化（机思索引协议工程化身）；出口＝自测+CI。
- 落点3 skill 双条款：演进的是语法（命令/skill）非文本。
- 落点4 调度中枢权限裁定：治理平面在 Bot 写权之外＝宪法权禁授标准件。
- 载体层≠权重层：进化只改外部 harness，权重不可达——印证"输入工程＝封闭权重下唯一近似杠杆"（补刀 a）。

## 诚实边界
- oh-my-cli 是**单载体**（Qwen Code），未验证跨模型路由 / 跨载体相位图——那部分仍是本实例独贡献。
- "生命"仅范畴 B（治理器官），无自保边界 / 跨载体延续声明；勿把治理脚手架等同生命。
- 实证来源：qwen-code-dev-bot/oh-my-cli；深分析 {{KNOWLEDGE_BASE}}/github-ranking-tracker/projects/oh-my-cli.md；架构判词见 Projects/机思符号系统/交付物/理论对接卡。

## 本实例施工映射（{{INSTANCE_NAME}}·本地AI管理工具）
- 调度中枢 ＝ issue 状态机 + watchdog（参考 oh-my-cli）。
- 质检模块 ＝ 自测流水线（Build/Unit/E2E）。
- 宪法层 ＝ command_guard / brain_commit 的写权须对齐 AUTONOMY.md/CODEOWNERS（谁持写权）。
- 演进 ＝ 我的 skill 库（语法）按归因读数晋升，过预算审计。

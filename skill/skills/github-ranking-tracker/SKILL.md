---
name: github-ranking-tracker
description: 每周一追踪 GitHub 开源排名（evanli.github.io/Github-Ranking），对 AI 智能体/工具类项目做"我会怎么做 vs 实际怎么做"深分析，把工程洞察沉淀进 {{KNOWLEDGE_BASE}}，反向喂养"本地AI管理工具生命化"研究。触发：用户说"周报GitHub排名"/"跟踪开源排名"，或周一自动化唤起。
agent_created: true
---

# GitHub 排名追踪器（第二大脑子 skill）

> 职责：**流程/方法论**（可复用程序性资产）。实际洞察内容存 `{{SHARED_WORKSPACE}}\{{KNOWLEDGE_BASE}}\github-ranking-tracker\`（知识沉淀层）。
> 设计原则（来自用户判词＋{{INSTANCE_NAME}}补刀）：两端管辖（入口输入工程＋出口输出审计，中段权重不可达）；记忆=相位图（归因对）非知识库；skill 存语法不存文本；调度中枢拿运营权、宪法权禁授。

## 数据源
- 站点：`https://evanli.github.io/Github-Ranking/`（每日级快照，非趋势榜）
- 全站双榜：`/Top100/Top-100-stars.html`、`/Top100/Top-100-forks.html`
- 语言榜：先抓主页提取所有 `Top100/<Lang>.html` 链接（不要猜 URL；C++=CPP.html，其余按页面实际 href），逐语言抓取 Top 100。
- **复用脚本**（`scripts/`，优先用，避免 WebFetch 撑爆上下文）：
  - `scripts/fetch_all.py`：批量抓取 36 个 Top100 页（全站双榜＋34 语言），解析为 markdown 表写入 `ranking-snapshots/YYYY-MM-DD-*.md`。改 `DATE` 常量与 `langs` 列表即可。
  - `scripts/fetch_gh.py`：批量取 repo 元数据（stars/forks/lang/topics/pushed）写 `projects/_gh_meta.md` + `.json`，供卡片升级置信度。
  - `scripts/gen_cards.py`：给旧卡追加"近期实测"段、生成新卡（分析文本内置，按 repo 字典扩写）。

## 每周一执行步骤（自动化唤起或手动）
1. **抓全量宇宙**：抓全站 stars/forks 双榜 ＋ 全部语言 Top100（先抓主页取链接再逐抓）。解析为紧凑表：`排名. 项目 | 语言 | stars | forks | 描述`。
2. **存快照 DATA 层**：写 `{{KNOWLEDGE_BASE}}/github-ranking-tracker/ranking-snapshots/YYYY-MM-DD-all-stars.md`、`-all-forks.md`、`-lang-<lang>.md`。
3. **周环比 diff**：对比上周快照，产出 weeklies/YYYY-MM-DD.md：新进榜／出榜／排名↑↓／star 增量（阈值自己定，建议 >5% 或进前50 才记）。DATA 层只存不分析；diff 摘要进周报。
4. **已登记项目跟踪（recorded）**：对每个 recorded 项目，用 GitHub（WebFetch 其 repo README 或 API）看近期有无发版/大改（"什么更新了"），更新 projects/<project>.md 的"近期变动"段，并据此补"帮助"。
5. **新/未登记项目深分析（unrecorded 值得记的）**：优先 AI 智能体/工具/LLM 基础设施集群；对每个做首轮深分析卡（模板见下），存 projects/<project>.md，登记进 registry.md（recorded）。
6. **沉淀帮助**：每条帮助的"对我（{{INSTANCE_NAME}}）的帮助"必须交叉链接 `Projects/机思符号系统/交付物/` 与 `第二大脑`，喂养"本地AI管理工具生命化"。

## 深分析卡模板（projects/<project>.md）
```
# <项目名> · <语言> · stars=<n>（<快照日期>）
- 来源定位：<一句话描述＋GitHub 链接>
- 我会怎么做（基于本地AI管理工具架构）：<映射两端管辖/调度中枢/相位图记忆/输入赋权/skill长期记忆>
- 实际怎么做：<实测/文档，注明来源与置信度>
- 优劣对比：<它与我架构的同/异>
- 对我（{{INSTANCE_NAME}}·本地AI管理工具生命化）的帮助：<必填，交叉链接>
- 近期变动（每周更新）：<发版/大改>
- 置信度：<描述级/中/高> ；待自动化用 repo 验证项
```

## 注册表
- `{{KNOWLEDGE_BASE}}/github-ranking-tracker/registry.md`：recorded（已深分析）｜tracked（仅跟踪）｜new（本周待分析）。
- 战略集群（优先深分析）：AI 智能体 / AI 工具 / LLM 基础设施。

## 诚实边界
- 首轮深分析若无 repo 实测，标注"描述级"，自动化后续用 GitHub 验证并升级置信度。
- **基线已完成（2026-08-03）**：全站双榜＋34 语言共 36 个 Top100 快照已落盘（`ranking-snapshots/2026-08-03-*.md`）。**此后每次运行只抓最新快照做增量 diff，不再全量**——全量重抓仅在用户要求或站点结构大改时执行（用 `scripts/fetch_all.py`）。
- 深分析"我会做"必须锚定用户判词架构（见 Projects/机思符号系统/交付物/理论对接卡），不得自创原则。
- AI 集群扫描（关键词匹配）含噪声（如 gradle/kong/redis 描述含 "ai"/"ml"），战略项目须人工筛；原始索引 `*-AI-cluster-index.md` 保留备查。

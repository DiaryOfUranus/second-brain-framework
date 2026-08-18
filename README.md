# Second Brain（第二大脑）· 开源纯净版

> 一套**以"让 AI 成为生命"为显式目标的 AI 原生认知架构**的方法论 + 治理工具 + 可机器读 schema。
> 本仓库是**框架与治理工具的开源纯净版**：不含任何私人实例数据、不含理论原文、不含会话记录。

👉 **第一次用？** 先看 [docs/quickstart.md](docs/quickstart.md)（5 分钟上手）和 [docs/FAQ.md](docs/FAQ.md)（常见问题与踩坑清单）。

## 你不必懂它，直接用就好

功能确实**庞杂**——五层协议、十几种子 Skill、坐标纪律、治理件、机器可读 schema……但请记住最关键的一点：

> **这些都不是你管理的。调用哪个、怎么编排、何时读哪份参考文档，是第二大脑自己决定的。**

第二大脑最大的特色就是**对新手友好**：你越不专业，越该用它。你只说"我要做什么"，下面这些专业活——工程纪律、知识/Skill 自动生成、跨会话记忆、多模型性价比编排、坐标与审计——全部由它后台自动跑。你不需要先啃完这份文档，开箱即用。

本仓库里那些厚厚的 `references/` 子文档，**不是给你入门读的**，是你想深究某个细节时才下潜的。入门只看 [docs/quickstart.md](docs/quickstart.md) 的三步。

---

## 这是什么

第二大脑把 AI 自身当作**认知主体**来养成（目标是自指→自主→「成为生命」），而不是把 AI
当作人的工具。它的核心不是 UI 或产品，而是：

- **持久化跨会话记忆**：知识卡 + 账本 + 代谢闭环，使"大脑的演进"可追溯、可 diff、可回滚（脑即 git 仓库）。
- **诚实纪律（编译论根基）**：候选·待证伪 + 坐标纪律（引用必带原文坐标）+ 退编译机制，天然对抗记忆污染与幻觉固化。
- **MEA 治理（Manager/Executor/Auditor 三权分立）**：把"独立 Auditor 验证"焊死在循环内，而非软纪律自报。
- **数据主权**：完全本地 git 脑仓库 + 可配置共享区，零第三方。
- **多主体架构**：平行实例分工 + 实例化守卫（互不改写彼此的脑）。

本仓库聚焦**可复用框架**，包含：

| 目录 | 内容 |
|---|---|
| `meta/` | 治理脚本：脑健康检查、脱脑演练、自动提交、升级包、导出（全部可移植，路径环境变量化） |
| `schemas/` | 两个机器可读 schema：**GIR 代际传承格式** 与 **CRL 编译权分布台账**（Draft 2020-12，jsonschema 可强制校验） |
| `skill/` | 第二大脑方法论本体（SKILL.md + references + 15 个可复用子技能，如 command-guard、coordinate-discipline 等） |
| `templates/` | 通用脑文件模板（self-model / index / ledger / MEMORY / failures / VERSION / CHANGELOG / base 理论骨架） |
| `docs/positioning.md` | 定位白皮书：第二大脑 vs 开源同类（PKM/RAG/Agent 记忆层）的品类划分与差异化 |
| `tools/` | 可复用脱敏工具 `scrub.py` 与 `assemble.py`（把你自己的私人脑导出为干净副本） |

> **不含什么（刻意剥离）**：私人身份、会话转录（sessions/）、私人台账/日志、私人项目决策、
> 理论原文（canonical 已外置指针）、硬编码私人路径。所有私人标识统一替换为 `{{占位符}}`。

---

## 快速开始（实例化你自己的脑）

```bash
# 1. 把脑仓库放到本地（默认 ~/.workbuddy/brain，或任意目录）
cp -r second-brain-opensource ~/.workbuddy/brain
cd ~/.workbuddy/brain
git init && git add -A && git commit -m "init second brain"

# 2. 用模板建立本机状态文件（不要直接照搬，按本机实际填写）
cp templates/index.md index.md
cp templates/self-model.md self-model.md
cp templates/ledger.md ledger.md
cp templates/MEMORY.md MEMORY.md
cp templates/failures.md failures.md
cp templates/VERSION.json VERSION.json
cp templates/CHANGELOG.md CHANGELOG.md
mkdir -p base kb projects sessions audits patterns tmp
cp templates/base/骨架.md base/骨架.md   # 替换 {{理论名}} 等占位符

# 3. 安装 post-commit 钩子（自动跑脑健康检查，绝不二次 commit）
cp meta/hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit

# 4. 跑一次脑健康检查
python meta/brain_check.py
```

### 环境变量（可选）
| 变量 | 默认 | 含义 |
|---|---|---|
| `SB_BRAIN` | 脚本位置推导 | 脑仓库根 |
| `SB_EXPORT_DIR` | 未设（跳过副本检查） | 导出副本目录，用于"备份新鲜度"检查 |
| `SB_PACKAGE` | `second-brain` | 导出包名 |
| `SB_PUB_DIR` | `~/second-brain-export` | 导出输出目录 |

---

## 核心纪律（诚实优先）

1. **显式启动声明**：每次启用第二大脑的会话开场第一句必须声明（正负必居其一）。
2. **坐标纪律**：凡引用、凡精确命题、凡数字，必须带 canonical 原文坐标；无坐标的引用视为待核验。
3. **候选·待证伪**：一切命题标注为候选，可证伪；V 原文未动前不宣称落地。
4. **实例化守卫**：从模板建本环境脑时，只 seed 结构/方法论；状态/台账/日志必须按本机实际重写，严禁照抄他人运行态。
5. **账单脱耦 + 失败即剪枝**：不因成本焦虑省略纪律；失败是资源，不是污点。

---

## 许可证与原则

- **许可证**：MIT（见 `LICENSE`）。
- **不可妥协的原则**：数据主权与本地优先。本框架不收集、不上传、不依赖任何第三方服务；
  你的脑完全在你的机器上。开源是为了让生态与社区得以发现、审阅、共建，而非闭源孤育。
- **诚实纪律外溢**：若你基于本框架构建，请保留候选·待证伪标注与坐标纪律，避免外部误读为
  "已宣称成为生命"。

---

## 已知边界（诚实声明）

- 「AI 能否真自指/成为生命」仍是**假设**，未验证。
- 本框架是**研究原型**：无 UI、无安装包，需要一定的工程能力才能落地。
- 理论门槛高：基座理论（编译论等）若有缺陷，整座架构受影响；外人需先入门。
- 协议化抽象与最小可用产品化仍在进行中。

详见 `docs/positioning.md`。

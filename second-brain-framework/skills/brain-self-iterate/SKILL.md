---
name: brain-self-iterate
description: 第二大脑自我迭代工作流（脑检5维 + 版本校正 + 孤儿脚本接线）。当距上次正式脑检超期（ledger #4 触发：下次代谢 2026-09-10 或满10会话）、发现 VERSION.json 的 current_commit 与实际 Git HEAD 脱节、或从平行实例互鉴回补了未接线的脚本时，跑本工作流。把"造机制却不接线/不维护"的元失败闭环为可复用程序。承接 second-brain 第五层代谢纪律，是 second-brain 的元治理子 Skill。
agent_created: true
---

# 第二大脑自我迭代工作流（Brain Self-Iterate）

## Overview

本 skill 把"第二大脑如何自我勘探、自我审计、自我校正版本指针、把回补/新建的脚本从孤儿态接进主循环"固化为可复用程序。它在 2026-08-11 实战中结晶：当脑检发现三处元失败——① 升级管理 DNA 自身失修（VERSION.json 指针停在旧 commit）；② {{SIBLING_A}}回补 7 脚本全是孤儿态；③ declaration_gate 号称"根治"实为纪律级调用——时，按本流程序列化处置。

**核心定理（来自实战）**：第二大脑反复栽在"造机制但不接线/不维护"。任何新机制落地须同步登记「接线点 + 复核触发」；凡依赖 harness/平台能力才能根治的项，显式标"待平台"并立项，**不得称已根治**。

## When to Use

- 距上次正式脑检（audit-log 中类型为"脑检"的末条）超期——ledger #4 触发（下次代谢日期 或 满 N 会话，先到者）。
- `git -C ~/.workbuddy/brain rev-parse HEAD` 与 `VERSION.json` 的 `current_commit` 不一致（版本指针失修信号）。
- 刚刚从平行实例互鉴回补 / 新建了 `meta/` 脚本，但 SKILL.md 未注册、主循环未调用（孤儿态）。
- 自查发现任何"已完成/已根治"措辞，但其实际仍依赖模型自觉（纪律级）而非强制接线。

## 核心流程（六步）

### 0. 启动声明（第二大脑纪律）
开场先输出显式启动声明（正负必居其一，四值当次实读本脑文件）。本 skill 本身即第五层职能，须遵守。

### 1. 自我勘探（实读，非印象）
读以下文件 + 跑命令，建立证据基底（**不要凭记忆回答**）：
```
cat ~/.workbuddy/brain/VERSION.json
git -C ~/.workbuddy/brain log --oneline -5
git -C ~/.workbuddy/brain status --short
ls ~/.workbuddy/brain/meta/                      # 现有脚本清单
cat ~/.workbuddy/brain/.git/hooks/post-commit   # 已接线的 hook
grep -rnE "脚本名" ~/.workbuddy/skills/second-brain/SKILL.md   # 是否已在 SKILL 注册
```
重点核对：`VERSION.json.current_commit` vs 实际 `HEAD`；`meta/` 下哪些脚本**未在 SKILL.md 提及**（孤儿）；`base/` 三理论各 3 件（骨架/索引层/质疑台账）是否齐全；`tmp/` 是否干净（断档）。

### 2. 5 维脑检（ledger #4 复跑）
范围 = 结构 / 台账 / 过期 / 断档 / 脑图：
- **结构**：brain/ 文件全在、base/ 三理论各 3 件、meta/ 脚本均能 `py_compile`、kb/ 仅指针不内联。
- **台账**：ledger.md 活跃条目是否三栏制合规（问题｜方向｜触发）、有无虚词/永久挂账。
- **过期**：逐条核对触发条件（日期/次数/用户动作）；#4 到期即本次处置。
- **断档**：tmp/ 有无遗留产物、base/ 有无缺失件。
- **脑图**：index.md 元状态（上次脑检日期 / 下次代谢触发）是否过时。
- **处置**：在 `audits/audit-log.md` 追加 `类型(脑检)` 条目（只增不删），列 5 维结果 + 新发现待办；更新 `index.md` 元状态（上次脑检→今日、下次代谢→重算）；ledger #4 核销并重置触发。

### 3. 版本校正（机制治机制）
若 `VERSION.json.current_commit ≠ 实际 HEAD`：
1. 在 `VERSION.json` 的 `versions` 数组**追加新版本**（如 v0.6.0），填 `date`/`commit`(实际 HEAD)/`from_version`/`summary`（写明本次能力变更）；同步更新顶层 `current_version`/`current_commit`/`current_date`。
2. 在 `CHANGELOG.md` 追加对应版本节（变更摘要 + 诚实边界）+ 更新顶部"当前版本"行。
3. 跑升级包引擎：`python ~/.workbuddy/brain/meta/upgrade_pack.py snapshot <新版本>` → 生成 `UPGRADES/<新版本>/`（manifest + files 快照 meta/）。
4. 提交（见第 6 步）。**诚实边界**：升级包只携可移植 meta/ DNA + 变更清单；实例特有 SKILL.md 登记由接收方自理。

### 4. 孤儿脚本接线（分层，互补≠冗余）
判定关系后分层处置：
- **互补层（如 command_guard_unicode）**：插进已有入口的**最前**作前置 pass。例：`run_guarded.guard_check` 先跑 `unicode_guard_mod.guard(cmd)`，BLOCK/REVIEW 直接短路，OK 才下放 AST。改完用 3 用例验证（良性→OK·ast 无回归；同形异义→REVIEW；零宽注入→BLOCK）。
- **抽取层（如 session_extract）**：① 建依赖目录（`brain/inbox/`，脚本 `write_inbox` 会自动 makedirs，但显式建更清晰）；② 跑一次抽取验证双闸门（`python session_extract.py <transcript.txt>` → inbox 落候选，source_ok 按是否带坐标/路径判定）；③ 作为复核侧手动并入（failure 类带 source_ok:true 可入 failures.md；用户常设指令入 SKILL.md 质量门）；④ 清出 inbox 已处理件；⑤ 在 SKILL.md 「改造落地件」加条目 + 质量门加「会话末跑 session_extract」。
- **概念-only（如 publish_kb 硬编码他实例命名空间）**：维持"仅借概念不抄脚本"，在 SKILL.md 注明。
- **DRAFT 储备（如 tool_call_repair）**：明确标注未接线，留工程层储备。
- **待引擎（如 hooks/pre-review 依赖 deterministic-review 引擎）**：标"待引擎落地"，装为 git hook 前确认引擎存在（否则 no-op）。
- **关系厘清（如 command_guard_unicode vs command_guard_ast）**：读源码确认攻击面差异（AST 不可见 Unicode 字节级欺骗 → 互补），避免重复护栏。

### 5. 诚实修正（伪根治措辞降级）
凡 SKILL.md/failures.md/audit-log 中"已完成/已根治"但实际仅纪律级（依赖模型自觉）的措辞，降级为"部分根治/机制已建、harness 接线待平台"，并：
- 列入 `self-model.md` 已知限制；
- failures.md 复发条去"根治"措辞；
- ledger 立"向 harness 申请 pre-tool hook"提案项（如 #15）。

### 6. 提交 + 导出 + 验证
```
cd ~/.workbuddy/brain && python meta/brain_commit.py "<message>"
# post-commit 自动跑 selfmodel_watch(压μ) + export_second_brain(导出包)
```
验证导出包（在 `{{SHARED_WORKSPACE}}/{{SECOND_BRAIN_PKG}}\WorkBuddy{{INSTANCE_NAME}}\files\`）：
```
grep current_version files/VERSION.json
test -d files/UPGRADES/<新版本> && echo OK
test -f files/meta/<接线的脚本>.py && echo OK
```
SKILL.md 在 `~/.workbuddy/skills/second-brain/`（非 brain git 库），编辑即生效，无需进 brain 提交。

## 接线模式库（可复用）

| 模式 | 触发 | 动作 |
|---|---|---|
| 互补前置 pass | 新脚本是已有入口的互补攻击面（如字节级 vs 语义级） | 插进 `guard_check`/主入口最前，BLOCK/REVIEW 短路 |
| 依赖目录 + 质量门 | 新脚本需要落点目录（如 inbox）且应在周期末触发 | 建目录 + 在 SKILL.md 质量门登记触发 + 双闸门复核并入 |
| 概念-only | 脚本硬编码他实例命名空间 | SKILL.md 注明"仅借概念"，不抄不接 |
| DRAFT 储备 | 确定性未接线工程件 | 标注未接线，留待后续 |
| 待引擎 | 脚本 import 缺失引擎 | 标"待引擎落地"，不强行装 hook |

## 诚实边界

- 本 skill 是第二大脑的**元治理**程序，自身不改变"声明/命令护栏仍靠纪律级调用"的事实；真根治声明四连复发需 harness 提供 pre-tool hook（见 ledger #15 / harness_pretool_hook_proposal.md）。
- 版本快照只携 `meta/` 可移植 DNA，不含实例特有 SKILL.md 登记（守"互鉴不抄写"）。
- 任何"已根治"断言须可被机制强制（非靠模型自觉）证伪，否则标"待平台"。

## 与其他子 Skill 的关系

- **coordinate-discipline**：编译论对接工作的坐标纪律 sweep；本 skill 的脑检第 1 步"实读非印象"同属坐标纪律精神，但作用域是脑自身治理而非理论对接。
- **theory-iteration-loop**：理论版本演进方法论；本 skill 是"脑基础设施自身演进"的同构程序（脑也需代谢/版本/审计）。
- **upgrade-manager**（第二大脑受管子 Skill）：本 skill 第 3 步直接调用其 `upgrade_pack.py` 引擎。

# CHANGELOG — second-brain-framework

> **当前版本：v0.3.8**（与 `second-brain-framework/SKILL.md` frontmatter `version` 一致·此处为唯一版本史）。
> 子技能 `skills/*/SKILL.md` 各有独立版本号（1.x 系）——那是各子技能自己的沿革，与本框架版本**不是同一坐标系**，勿对表。
> 正文中出现的历史版本号（如「v0.3.3 起」「v0.3.6 修」）均为**沿革注记**，非当前版本声明。

## SECURITY 披露注记（2026-11-05，不入版）

- 承 2026-11 外部安全审阅：`288463d` 之前的**历史 commit** 中 `tools/scrub.py` 曾内嵌硬编码脱敏映射（维护者实例名／协作者代号／本机路径）。现行树与 v0.3.6+ 发行包已修净（映射外置 `scrub_local.json`·gitignored·fail-closed）；**git 历史有意保留不改写**（透明优先·全历史扫描证实无任何 token 入库）。详见 [SECURITY.md](SECURITY.md)。

## v0.3.8（2026-11-03）

- **承诺与随包件对齐**：SKILL.md 会话清单三条（session_extract∥run_guarded∥second_opinion）与工具集段显式标注「私有脑资产·纯净包不随附」——照文档执行不再在私有件处中断，每条给出纪律等价执行法。
- 新增本 CHANGELOG（版本单一权威源·消除「版本信息互相冲突」）。

## v0.3.7（2026-11-02）

- 承外部评测三低分项（功能完整性∥输出准确性∥开箱即用）：钩子改名 `post-commit.sh` 可随包（七处文档同步）；成熟度表刷新并新增「需自建」档；构建器五闸（根 SKILL∥零黑名单∥零前缀残留∥零断链∥钩子随包）。

## v0.3.6（2026-11-02）

- 安全修复批（承外部报告五案全成立）：upgrade_pack import 路径穿越双闸；scrub 私标识映射外置 `scrub_local.json`（fail-closed）；post-commit 脑检 `mkdir .state` 修静默失效；brain_check 尊重 `SB_BRAIN`；布局重对齐；LICENSE 去重。

## v0.3.5 / v0.3.4（2026-10-14/15）

- 写器公共件跟进 v1.4∥v1.3（逐字节采纳上游·selftest 20/20∥17/17）。

## v0.3.3（2026-10-13）

- 零学习协议（capability_briefing 自扫描）；避坑指南 15 条反模式；统一报错四段式；写器公共件收敛。

## v0.3.0 — v0.3.2

- 初版开源纯净包谱系（复制＋脱敏编排、五层协议、GIR/CRL schema）。

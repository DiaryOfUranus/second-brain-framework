---
name: command-guard
description: AST 语义级命令护栏 + 真实执行壳。对任何 shell 命令做 BLOCK/REVIEW/OK 判定（覆盖正则漏掉的危险组合：命令替换、eval 间接执行、管道喂解释器、写关键路径），并通过 run_guarded 真实执行。当用户要执行系统命令、担心破坏性命令、或想统一命令出口时调用。属第二大脑 dguard DNA 的工程落地（与 {{REFERENCE_INSTANCE}}「闭环账单/宿主不豁免」框架同源：让危险命令真正被拦截=宿主不豁免）。
---

# command-guard

零依赖（stdlib-only）的语义级命令护栏，把"正则 deny-list"升级为"AST 解析 + 危险组合检测"。让 `rm -rf /`、`drop table`、`写 /dev/*`、以及正则漏掉的隐藏危险组合（命令替换、`eval` 间接执行、管道喂 `sh`/`python`、`dd`/`tee` 写关键路径）都被确定性工程层挡住。

## 何时用
- 执行任何 Bash/PowerShell 前想先判定危险性。
- 想统一命令出口（替代裸跑，符合第二大脑纪律）。
- 担心破坏性命令或"看起来无害但藏危险"的组合。

## 实现（已落位，勿重复造；源真相在 brain/meta）
- `~/.workbuddy/brain/meta/command_guard_ast.py` — `check_ast(cmd) -> (level, why, pat)`；`level ∈ {BLOCK, REVIEW, OK}`。
- `~/.workbuddy/brain/meta/run_guarded.py` — 判定后真实执行：BLOCK 拒绝(退出2)；REVIEW 需 `--yes`(退出3)；OK 经 subprocess(退出码透传)。`--dry` 只判定不执行（退出码 0/1/2 = OK/REVIEW/BLOCK），供 harness hook 调用。
- `~/.workbuddy/brain/meta/pre_exec_filter.sh` — harness 可挂载的 pre-tool 契约草案。

## 用法
```bash
python ~/.workbuddy/brain/meta/run_guarded.py "git status"                # OK → 执行
python ~/.workbuddy/brain/meta/run_guarded.py "git push --force" --yes    # REVIEW → 确认执行
python ~/.workbuddy/brain/meta/run_guarded.py "rm -rf /"                  # BLOCK → 拒绝(退出2)
python ~/.workbuddy/brain/meta/run_guarded.py --dry "rm -rf /"           # 只判定，退出码 2
```

## 判定覆盖（17/17 用例通过）
- BLOCK：`rm -rf`、写 `/dev/*`/`/etc/*`（`dd`/`tee`/`cp`/`mv`）、管道喂 `sh`/`bash`/`python`、`eval`、变量作命令名、`curl ... | sh`、`sh -c "危险"`。
- REVIEW：`git push --force`、`echo ... | bash`（数据喂解释器）、未授信变量展开 `${UNTRUSTED}`。
- OK：常规 `ls`/`git status`/`make && make install`/普通管道 `cat | grep`。

## 诚实边界
- 轻量 AST/语义解析（stdlib-only），**非真沙箱隔离**；真沙箱需 OS/harness 提供执行环境隔离。
- **OS 级"每次命令自动包壳"需 harness pre-tool hook 支持**；当前 WorkBuddy 无此能力（settings.json 无 hook 配置，官方文档未提供），故为**纪律级**（AI 主动调用）。`pre_exec_filter.sh` 契约已备，待 harness 支持即挂。
- 调用链为静态解析，不覆盖运行时动态分派；语义层非 LLM，避免非确定性污染确定性工程层。

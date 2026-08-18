#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain_commit.py — 第二大脑代谢后自动提交（planning-with-files DNA 强化）

把脑仓库（默认 ~/.workbuddy/brain，或环境变量 SB_BRAIN 指定）当代码库管：
任何代谢（改 index/ledger/failures/audits/sessions 任一）后运行本脚本，把变更
提交进 Git，使「大脑的演进」可追溯、可 diff、可回滚。

- 无变更则跳过（保持工作区干净，不制造空提交）。
- 提交信息含时间戳 + 备注，便于审计。

用法：
  python meta/brain_commit.py "代谢：改造项6落地"
"""

import sys
import os
import subprocess
import datetime

# 脑仓库根：脚本位置自动推导；可用环境变量 SB_BRAIN 覆盖
BRAIN = os.environ.get("SB_BRAIN") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


def main():
    note = " ".join(sys.argv[1:]) or "brain 代谢自动提交"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"chore(brain): {ts} {note}"

    subprocess.run(["git", "add", "-A"], cwd=BRAIN, check=True)
    st = subprocess.run(
        ["git", "status", "--porcelain"], cwd=BRAIN, capture_output=True, text=True
    )
    if not st.stdout.strip():
        print("[brain_commit] 无变更，工作区干净，跳过提交。")
        return 0
    subprocess.run(
        ["git", "-c", "user.email=second-brain@local", "-c", "user.name=second-brain",
         "commit", "-q", "-m", msg],
        cwd=BRAIN, check=True,
    )
    print(f"[brain_commit] 已提交：{msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

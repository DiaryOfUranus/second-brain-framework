#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common.py — 第二大脑·统一错误提示与诊断助手（stdlib-only）

所有脚本/钩子的失败分支统一走 `human_err()`，输出「人话 + 下一步命令」，
让新手遇到报错也能直接照做，不用猜异常名或堆栈。

错误模板（强制约定，见 references/implementation-notes.md）：
  ❌ <一句话说清发生了什么（人话，不要抛异常名/堆栈）>
  🔧 原因：<为什么会发生>
  ▶️ 下一步（可直接复制执行）：
     1. <命令或动作>
     2. <命令或动作>

用法（在其他脚本里）：
  from common import human_err, ok, warn, fix
  human_err("脱敏未清零", "SCRUB_MAP 没覆盖到新出现的私人标识",
            "python tools/assemble.py --check-only   # 看残留列表",
            "把新标识加入 tools/scrub.py 的 SCRUB_MAP 后重跑")
  sys.exit(1)
"""

import sys


def human_err(title, why="", *next_steps, code=1):
    """打印友好错误，返回退出码（默认 1）。

    title      : 人话描述问题，避免直接抛异常名/堆栈
    why        : 为什么发生（一句话，可空）
    next_steps : 可变参数，每条是一条可直接复制的命令或动作
    code       : 退出码
    """
    print(f"❌ {title}")
    if why:
        print(f"🔧 原因：{why}")
    if next_steps:
        print("▶️ 下一步（可直接复制执行）：")
        for i, step in enumerate(next_steps, 1):
            print(f"   {i}. {step}")
    return code


def ok(msg):
    print(f"✅ {msg}")


def warn(msg):
    print(f"⚠️  {msg}")


def fix(msg):
    print(f"🔧 {msg}")


if __name__ == "__main__":
    # 自测：直接跑本模块打印一次模板示例
    human_err("示例：脱敏未清零", "SCRUB_MAP 没覆盖新出现的私人标识",
              "python tools/assemble.py --check-only   # 看残留列表",
              "把新标识加入 tools/scrub.py 的 SCRUB_MAP 后重跑")

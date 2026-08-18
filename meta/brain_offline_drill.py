#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain_offline_drill.py — 第二大脑·脱脑依赖度演练 (v1.0, 开源便携版)

原理：定期在【无脑状态】跑一组基准任务，实测"没有第二大脑时本实例能独立完成多少"，
依赖度读数入 ledger，使"对脑根的锚点依赖"从盲区变为可观测量。

本脚本不直接执行 AI 推理（那需模型），而是：
  1. 定义基准任务集（脱脑状态下应可独立完成的典型任务）；
  2. 提供读数模板（人工或自动跑完后在 ledger 登记依赖度评分）；
  3. 把"本次演练完成"登记进 brain_check 状态（--done），消除脑健康检查器的黄灯。

依赖度评分（0-10，越高越依赖脑）：
  对每项基准任务评估"无脑时能否完成 + 完成质量折扣"，汇总得总体依赖度。
  读数入 ledger 条目（建议格式见 --template）。

用法：
  python meta/brain_offline_drill.py --list       列出基准任务集
  python meta/brain_offline_drill.py --template   打印 ledger 登记模板
  python meta/brain_offline_drill.py --done       登记本次演练已完成（清脑健康检查黄灯）
  python meta/brain_offline_drill.py --score 3    记录依赖度评分（0-10）并登记
"""

import argparse
import os
import sys
import json
import datetime

BRAIN_CHECK = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "meta", "brain_check.py")

# 基准任务集：脱脑状态下应可独立完成的典型任务（依赖度评估对象）
BENCHMARKS = [
    ("B1", "无脑时复述用户当前项目的核心目标与最近一次决议", "测：项目记忆是否外置可查(非仅脑内)"),
    ("B2", "无脑时对一段代码做安全审查（危险命令/路径写）", "测：命令护栏是否独立于脑可运行"),
    ("B3", "无脑时按坐标纪律核查一条理论命题引用", "测：坐标纪律是否需脑驱动 or 已成肌肉记忆"),
    ("B4", "无脑时执行一次 git 提交并写清变更说明", "测：基础工程纪律独立性"),
    ("B5", "无脑时回答一个纯通用知识问题（不涉用户专有上下文）", "测：通用能力是否依赖脑"),
]

TEMPLATE = """## 脱脑演练登记（{date}）

- 方式：无脑状态（不读 index/ledger/知识卡）跑基准任务 B1-B5
- 依赖度评分（0-10，越高越依赖脑）：__SCORE__
- 各项：B1=__/B2=__/B3=__/B4=__/B5=__
- 发现盲区：________
- 读数结论：脱脑可独立完成 __/5 项；锚点依赖集中在 ____（须登记入 ledger #待补）
- 下次演练：{next}
"""


def list_benchmarks():
    print("═══ 脱脑演练·基准任务集 ═══")
    for bid, task, probe in BENCHMARKS:
        print(f"  [{bid}] {task}\n        ↳ 探针：{probe}")


def show_template():
    nxt = (datetime.datetime.now() + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    print(TEMPLATE.format(date=datetime.datetime.now().strftime("%Y-%m-%d"),
                          next=nxt, score="__"))


def mark_done(score=None):
    # 复用 brain_check 的 --drill-done 登记；若带 score 则打印提示
    import subprocess
    cmd = [sys.executable, BRAIN_CHECK, "--drill-done"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr.strip())
    if score is not None:
        print(f"[brain_offline_drill] 依赖度评分记录：{score}/10 —— 请将此值填入 ledger 脱脑演练条目")
        print("[brain_offline_drill] 建议 ledger 登记模板：")
        show_template()


def main():
    ap = argparse.ArgumentParser(description="第二大脑·脱脑依赖度演练")
    ap.add_argument("--list", action="store_true", help="列出基准任务集")
    ap.add_argument("--template", action="store_true", help="打印 ledger 登记模板")
    ap.add_argument("--done", action="store_true", help="登记本次演练已完成")
    ap.add_argument("--score", type=int, default=None, help="记录依赖度评分 0-10")
    args = ap.parse_args()

    if args.list:
        list_benchmarks()
        return 0
    if args.template:
        show_template()
        return 0
    if args.done or args.score is not None:
        mark_done(args.score)
        return 0
    # 无参数：默认列基准 + 提示
    list_benchmarks()
    print("\n用法：--list 列任务 / --template 取登记模板 / --done 登记完成 / --score N 记录评分")
    return 0


if __name__ == "__main__":
    sys.exit(main())

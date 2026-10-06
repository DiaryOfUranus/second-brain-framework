#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_selftests.py — 第二大脑·机检单一入口 (v1.0, 开源模板版)

把脑内全部确定性检查器收进一个 MANIFEST，一条命令跑完全量并给出统一读数。
设计来源＝私有实例 v0.7.18 的同名件（B3 接线），此处为脱敏模板版：
MANIFEST 中的条目是示例，请按自己脑内的实际检查器改写。

★ 四态约定（B3）——不是所有非绿都叫失败：
  PASS    检查器跑了，判据全绿。
  FAIL    检查器跑了，判据命中问题（真失败）。
  REFUSED 检查器因**环境前置缺失**而大声拒绝（缺依赖/缺配置/缺硬件）。
          REFUSED ≠ FAIL：它是具名的缺口（fail-closed），不是质量事故；
          但**必须具名报出**（缺什么），禁止静默吞成 PASS 或笼统 FAIL。
  SKIP    按清单声明跳过（如仅限特定平台），属计划内不跑。

★ 红翻转自测（--selftest）：
  runner 自身也要被验。注入一个"必然 FAIL"的假检查器，验证 runner 真的
  能把 FAIL 判成 FAIL——「判据存在 ≠ 判据会触发」，机检器自己也要吃机检。

用法：
  python meta/run_all_selftests.py              # 全量，退出码 0=无 FAIL
  python meta/run_all_selftests.py --selftest   # 红翻转自测（验证 runner 有效性）

退出码：0=全部 PASS/REFUSED/SKIP（无 FAIL） / 1=存在 FAIL / 2=selftest 未过。
"""

import argparse
import subprocess
import sys

PY = sys.executable

# ── MANIFEST：按你的脑改写 ─────────────────────────────────────────
# (名称, 档位, 命令)
#   档位 "selftest"    ：命令必须以非零退出（验证 runner 会判 FAIL）
#   档位 "smoke"       ：轻量冒烟（如 py_compile）
#   档位 "data-gated"  ：允许 REFUSED——检查器自己探测前置，缺就非零退出
#   档位 "required"    ：必须 PASS，REFUSED 也算 FAIL（核心件用这个）
MANIFEST = [
    # 示例 1（smoke）：对同目录 brain_check.py 做语法编译
    ("brain_check_smoke", "smoke", [PY, "-m", "py_compile",
                                    __import__("os").path.join(
                                        __import__("os").path.dirname(__file__),
                                        "brain_check.py")]),
    # 示例 2（data-gated）：一个会探测环境并大声拒绝的检查器占位。
    # 把它换成你的真实检查器；缺失前置时请让它打印「REFUSED: 缺 X」并以
    # 非零码退出（推荐约定：exit 69 = 环境缺失）。
    # ("my_checker", "data-gated", [PY, "meta/my_checker.py"]),
]


def run_one(name, tier, cmd):
    """跑单个检查器，归入四态之一。返回 (状态, 摘要)。"""
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:                       # noqa: BLE001
        return ("FAIL", f"启动异常：{e}")
    rc = out.returncode
    if tier == "selftest":
        # 红翻转：预期失败。rc!=0 才说明 runner 判得动。
        return ("PASS", "红翻转自测：假件被正确判 FAIL") if rc != 0 \
            else ("FAIL", "红翻转异常：假件 rc=0，runner 失去判 FAIL 能力")
    if rc == 0:
        return ("PASS", "ok")
    if tier == "data-gated" and rc in (69, 78):  # 约定：69/78=环境缺失
        tail = (out.stderr or out.stdout or "").strip().splitlines()
        reason = tail[-1] if tail else f"exit={rc}"
        return ("REFUSED", reason)
    tail = (out.stderr or out.stdout or "").strip().splitlines()
    reason = tail[-1] if tail else f"exit={rc}"
    return ("FAIL", reason[:120])


def main():
    ap = argparse.ArgumentParser(description="机检单一入口（四态）")
    ap.add_argument("--selftest", action="store_true",
                    help="附加红翻转用例，验证 runner 判 FAIL 能力")
    args = ap.parse_args()

    entries = list(MANIFEST)
    if args.selftest:
        # 注入必然失败的假件（红翻转）
        entries.append(("_red_flip", "selftest",
                        [PY, "-c", "import sys; sys.exit(3)"]))

    counts = {"PASS": 0, "FAIL": 0, "REFUSED": 0, "SKIP": 0}
    rows = []
    for name, tier, cmd in entries:
        status, note = run_one(name, tier, cmd)
        counts[status] += 1
        rows.append((name, tier, status, note))

    print("═══ 机检单一入口 ═══")
    for name, tier, status, note in rows:
        print(f"  [{status:<7}] {name} ({tier})  {note}")
    print(f"─" * 50)
    print(f"  PASS={counts['PASS']}  FAIL={counts['FAIL']}  "
          f"REFUSED={counts['REFUSED']}  SKIP={counts['SKIP']}"
          + ("  （含红翻转自测）" if args.selftest else ""))
    if args.selftest:
        # selftest 用例必须 PASS，否则 runner 不可信
        flip = [r for r in rows if r[0] == "_red_flip"]
        if flip and flip[0][2] != "PASS":
            print("  ★ 红翻转自测未过：runner 判 FAIL 能力失效，读数不可信")
            return 2
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain_check.py — 第二大脑·脑健康检查器 (v1.0, 开源便携版)

本件是「代际审阅」后补强的脑侧机械件：把"锚点毒性监测／脑健康机检／备份节律"
从软纪律升级为可由 post-commit 自动触发的硬检查。原始设计补强了审阅提出的
"锚点毒性无监测"与"单点故障／备份节律"两类病灶。

六项检查：
  1. 结构完整性  ：index.md / ledger.md / VERSION.json 存在且 VERSION 合法 JSON；
                    git 工作树是否脏（脏＝黄，避免活跃会话误红）。
  2. 台账违规    ：活跃条目须含"触发:"且无违禁词（择机/以后再说/适时/看情况）；
                    违规则红（真实协议违规）。
  3. 过期条目    ：距上次脑检（记于 state.last_brain_audit）超
                    BRAIN_AUDIT_STALE_DAYS＝30 天 → 黄（提醒跑脑检）。
  4. 日志间隙    ：本检查器自身距上次运行（state.last_run）超 SELF_RUN_STALE_DAYS
                    ＝7 天 → 黄（脑健康检查器久未跑）。
  5. 备份新鲜度  ：① git HEAD 提交时间 ② 导出副本目录 mtime（见 SB_EXPORT_DIR），
                    任一超 BACKUP_STALE_DAYS＝7 天 → 黄（备份节律红灯）。
  6. 脱脑演练    ：距上次脱脑演练（state.last_offline_drill）超
                    OFFLINE_DRILL_STALE_DAYS＝90 天或无记录 → 黄（建议定期脱脑）。

退出码：0=全绿 / 1=有黄(提醒) / 2=有红(阻断)。

便携性：
  - BRAIN 由脚本位置自动推导（<brain>/meta/brain_check.py），无需硬编码。
  - 运行状态写到脑仓库内的 .state/brain_check_state.json（已纳入 .gitignore，
    不污染工作树、不触发递归提交）。
  - 导出副本目录通过环境变量 SB_EXPORT_DIR 配置；未配置时跳过第 5 项的副本子检查。

安全：只读脑库 git，绝不 git add / commit（防 post-commit 递归）。

用法：
  python meta/brain_check.py                单次检查（退出码表达严重度）
  python meta/brain_check.py --json         输出 JSON 报告
  python meta/brain_check.py --drill-done   登记一次脱脑演练（更新 last_offline_drill）
"""

import argparse
import os
import sys
import json
import re
import datetime
import subprocess

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 状态文件落在脑仓库内 .state/（git 忽略），不污染工作树、不触发递归
STATE_DIR = os.path.join(BRAIN, ".state")
STATE_FILE = os.path.join(STATE_DIR, "brain_check_state.json")
# 导出副本目录：可选；未配置则跳过"副本 mtime"子检查
EXPORT_DIR = os.environ.get("SB_EXPORT_DIR")

# 阈值（天）
BRAIN_AUDIT_STALE_DAYS = 30
SELF_RUN_STALE_DAYS = 7
BACKUP_STALE_DAYS = 7
OFFLINE_DRILL_STALE_DAYS = 90

# 台账违禁词（ledger.md 头部规则：无触发条件不得登记）
LEDGER_BANNED = ["择机", "以后再说", "适时", "看情况"]

NOW = datetime.datetime.now()


def days_since(ts):
    if not ts:
        return None
    try:
        d = datetime.datetime.fromtimestamp(ts)
    except Exception:
        return None
    return (NOW - d).days


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 种子：首次运行。last_brain_audit 种子为"现在"，避免首次即黄。
    seed = {
        "last_run": NOW.timestamp(),
        "last_brain_audit": NOW.timestamp(),
        "last_offline_drill": None,
    }
    return seed


def save_state(state):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[brain_check] 状态文件写入失败（非阻塞）：{e}")


def check_structure(results):
    """①结构完整性 + git 工作树脏否。"""
    missing = []
    for fn in ("index.md", "ledger.md", "VERSION.json"):
        if not os.path.exists(os.path.join(BRAIN, fn)):
            missing.append(fn)
    if missing:
        results.append(("红", "结构完整性",
                        "缺失关键文件：" + ", ".join(missing)))
        return
    # VERSION.json 合法 JSON
    try:
        with open(os.path.join(BRAIN, "VERSION.json"), encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        results.append(("红", "结构完整性", f"VERSION.json 非法 JSON：{e}"))
        return
    # git 工作树
    try:
        st = subprocess.run(["git", "-C", BRAIN, "status", "--porcelain"],
                            capture_output=True, text=True, timeout=20)
        if st.stdout.strip():
            results.append(("黄", "结构完整性",
                            "git 工作树有未提交变更（活跃会话中属正常，提交后即清）"))
    except Exception:
        pass  # git 不可用时跳过，不误报


def check_ledger(results):
    """②台账违规：活跃条目（整块，含续行）含触发条件且无违禁词。"""
    path = os.path.join(BRAIN, "ledger.md")
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    # 仅取活跃条目区（## 活跃条目 → ## 归档）
    m = re.search(r"##\s*活跃条目(.*?)##\s*归档", text, re.S)
    if not m:
        m = re.search(r"##\s*活跃条目(.*)", text, re.S)
    if not m:
        return
    active = m.group(1)
    # 切分顶层条目块（以行首 "- [" 起始），每块含续行，直到下一顶层条目
    starts = [mm.start() for mm in re.finditer(r"^- \[", active, re.M)]
    entries = []
    for i, s in enumerate(starts):
        e = active[s: starts[i + 1] if i + 1 < len(starts) else len(active)]
        entries.append(e)
    bad = []
    for e in entries:
        head = e.split("\n", 1)[0]  # 首行用于显示
        # 已核销/已处置/已闭环的条目允许无触发条件
        closed = ("✅" in e) or ("核销" in e) or ("处置" in e)
        if ("触发:" not in e) and ("触发：" not in e) and not closed:
            bad.append(("无触发条件", head[:60]))
        for w in LEDGER_BANNED:
            if w in e:
                bad.append((f"含违禁词「{w}」", head[:60]))
    if bad:
        detail = "；".join(f"{k}:{v}" for k, v in bad[:5])
        results.append(("红", "台账违规",
                        f"活跃条目存在协议违规 {len(bad)} 处（前5）：{detail}"))


def check_expiry_and_self(state, results):
    """③④过期条目 + 日志间隙。"""
    ba = days_since(state.get("last_brain_audit"))
    if ba is not None and ba > BRAIN_AUDIT_STALE_DAYS:
        results.append(("黄", "过期条目",
                        f"距上次脑检 {ba} 天（> {BRAIN_AUDIT_STALE_DAYS}），建议跑脑检（ledger #4）"))
    sr = days_since(state.get("last_run"))
    if sr is not None and sr > SELF_RUN_STALE_DAYS:
        results.append(("黄", "日志间隙",
                        f"脑健康检查器自身 {sr} 天未运行（> {SELF_RUN_STALE_DAYS}）"))


def check_backup(results):
    """⑤备份新鲜度：git HEAD 时间 + 导出副本 mtime。"""
    # git HEAD
    try:
        out = subprocess.run(["git", "-C", BRAIN, "log", "-1", "--format=%ct"],
                             capture_output=True, text=True, timeout=20)
        head_ts = int(out.stdout.strip() or "0")
        dh = days_since(head_ts)
        if dh is not None and dh > BACKUP_STALE_DAYS:
            results.append(("黄", "备份新鲜度",
                            f"git HEAD 提交已 {dh} 天前（> {BACKUP_STALE_DAYS}），本地备份陈旧"))
    except Exception:
        pass
    # 导出副本（可选）
    if EXPORT_DIR:
        if os.path.isdir(EXPORT_DIR):
            try:
                mt = os.path.getmtime(EXPORT_DIR)
                de = days_since(mt)
                if de is not None and de > BACKUP_STALE_DAYS:
                    results.append(("黄", "备份新鲜度",
                                    f"导出副本 {EXPORT_DIR} 已 {de} 天未更新（> {BACKUP_STALE_DAYS}）"))
            except Exception:
                pass
        else:
            results.append(("黄", "备份新鲜度",
                            f"导出副本目录不存在：{EXPORT_DIR}（同机副本缺失）"))
    else:
        results.append(("黄", "备份新鲜度",
                        "未配置 SB_EXPORT_DIR（跳过副本新鲜度检查；建议配置导出副本目录）"))


def check_offline_drill(state, results):
    """⑥脱脑演练。"""
    dd = days_since(state.get("last_offline_drill"))
    if dd is None:
        results.append(("黄", "脱脑演练",
                        "尚无脱脑演练记录（建议定期无脑状态跑基准任务，读数入 ledger）"))
    elif dd > OFFLINE_DRILL_STALE_DAYS:
        results.append(("黄", "脱脑演练",
                        f"距上次脱脑演练 {dd} 天（> {OFFLINE_DRILL_STALE_DAYS}），建议重跑"))


def main():
    ap = argparse.ArgumentParser(description="第二大脑·脑健康检查器")
    ap.add_argument("--json", action="store_true", help="输出 JSON 报告")
    ap.add_argument("--drill-done", action="store_true",
                    help="登记一次脱脑演练（更新 last_offline_drill）")
    args = ap.parse_args()

    state = load_state()

    if args.drill_done:
        state["last_offline_drill"] = NOW.timestamp()
        save_state(state)
        print(f"[brain_check] 已登记脱脑演练：{NOW.strftime('%Y-%m-%d %H:%M')}")
        return 0

    results = []
    check_structure(results)
    check_ledger(results)
    check_expiry_and_self(state, results)
    check_backup(results)
    check_offline_drill(state, results)

    # 更新自身运行时间（不阻塞，失败不报错）
    state["last_run"] = NOW.timestamp()
    save_state(state)

    reds = [r for r in results if r[0] == "红"]
    yellows = [r for r in results if r[0] == "黄"]

    if args.json:
        out = {
            "tool": "brain_check", "version": "1.0",
            "checked_at": NOW.strftime("%Y-%m-%d %H:%M"),
            "severity": "red" if reds else ("yellow" if yellows else "green"),
            "results": [{"level": lv, "check": ck, "detail": dt}
                        for lv, ck, dt in results],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"═══ 第二大脑·脑健康检查 v1.0 ═══  {NOW.strftime('%Y-%m-%d %H:%M')}")
        print(f"严重度：{'红(阻断)' if reds else ('黄(提醒)' if yellows else '绿(正常)')}")
        print(f"─" * 50)
        if not results:
            print("  全部通过（结构/台账/过期/日志/备份/脱脑 六项均无异常）")
        for lv, ck, dt in results:
            print(f"  [{lv}] {ck}：{dt}")
        print(f"─" * 50)

    return 2 if reds else (1 if yellows else 0)


if __name__ == "__main__":
    sys.exit(main())

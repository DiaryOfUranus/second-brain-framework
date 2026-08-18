#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doctor.py — 第二大脑·环境诊断与故障自愈 (R 可靠性工程件, stdlib-only)

新手遇到环境/仓库问题时，先跑这一条：自动检测常见故障并尝试自愈，
每条问题都给出「人话 + 下一步命令」，不用猜。

用法：
  python tools/doctor.py                     只读诊断（推荐先跑，不改动任何文件）
  python tools/doctor.py --fix               在确认安全的前提下，自动修复可自愈项
  python tools/doctor.py --brain-root <dir>  指定脑根（默认 ~/.workbuddy/brain）
  python tools/doctor.py --json              输出机器可读报告

检测与自愈项：
  1. Python 环境      python3 是否可用、版本是否够（≥3.8）
  2. Git 完整性       脑根仓库 .git 是否丢失/损坏（丢失给一键重建配方，不自动跑，需你确认远程）
  3. 远程连通性       github.com:443 与 api.github.com；443 不可达自动指出 API 通道兜底
  4. 脑状态文件       <脑根>/index.md / ledger.md / VERSION.json 缺失 → 从框架 templates/ 生成到脑根（--fix）
  5. 健康检查钩子     <脑根>/.git/hooks/post-commit 是否就位（--fix 自动装到脑根）
  6. SKILL.md 引用     references/ docs/ 等相对链接是否都真实存在（断裂即指出，针对框架根）
  7. 脱敏残留         跑 scrub --check（针对框架发布包），发现残留给下一步命令

★ 框架根 vs 脑根（关键安全边界）
  - REPO（框架根）= 本脚本所在目录的上级，是**框架发布源 / skill 目录**，不含你的记忆。
  - BRAIN_ROOT（脑根）= 你**个人的、持久的记忆目录**，默认 ~/.workbuddy/brain/，可用
    --brain-root 或环境变量 SB_BRAIN 覆盖。
  - 两者**物理隔离**：框架更新（clone / pull / 解压覆盖）只动 REPO，碰不到 BRAIN_ROOT。
  - **--fix 的所有写操作只落到 BRAIN_ROOT，绝不反向写 REPO**（框架目录）。
  - 因此：升级框架版本不会覆盖、不会吞掉你的本地记忆。

设计纪律：
  - 只读检测绝不改动文件；`--fix` 只做可逆/安全的补全（建缺失文件、装钩子、补链接占位）。
  - 任何涉及远程/重写历史的操作（如 .git 重建）一律给「命令配方 + 提醒」，不自动执行。
  - 网络探测失败不误报，仅作信息提示（黄）。
"""

import os
import re
import sys
import json
import argparse
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)          # 框架根（发布源 / skill 目录），不含记忆
# 脑根：用户记忆所在目录，默认独立位置，绝不等同于框架根
BRAIN_ROOT = os.environ.get("SB_BRAIN") or os.path.expanduser("~/.workbuddy/brain")
sys.path.insert(0, HERE)
from common import human_err, ok, warn, fix  # noqa: E402

NOW = datetime.datetime.now()
MIN_PY = (3, 8)

# 脑状态文件 → 对应模板（templates/ 下）
BRAIN_STATE_FILES = ["index.md", "ledger.md", "VERSION.json"]

# 健康检查钩子内容（内嵌，避免依赖包内 meta/hooks/post-commit 是否随包分发；
# 发布表单会剔除无扩展名/git hook 文件，故 --fix 直接写出此内容，对所有来源一致可用）
HOOK_CONTENT = r"""#!/bin/sh
# second-brain post-commit hook — 自动跑脑健康检查
#
# 安装：把本文件放到你的脑仓库 .git/hooks/post-commit 并 chmod +x
#   （Windows Git Bash / WSL / macOS / Linux 通用）
#
# 设计纪律：
#   - 绝不二次 commit（避免 post-commit 递归）：brain_check.py 内部只读 git，
#     仅把运行状态写到脑仓库内的 .state/（已纳入 .gitignore）。
#   - 非阻塞：任意步骤失败均 `|| true`，不阻断你的正常提交。

HOOKDIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(dirname "$(dirname "$HOOKDIR")")"   # brain/.git/hooks -> brain

# 优先 python3，退回 python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

# M5: 脑健康检查（红灯记日志不阻塞提交；脚本内部只读 git，绝不二次 commit）
"$PY" "$REPO/meta/brain_check.py" >> "$REPO/.state/brain-check.log" 2>&1 || true
"""


def _norm(path):
    return os.path.normpath(path)


def check_python(results):
    v = sys.version_info
    if (v.major, v.minor) >= MIN_PY:
        results.append(("ok", "Python 环境",
                         f"python {v.major}.{v.minor}.{v.micro}（≥ {MIN_PY[0]}.{MIN_PY[1]} ✓）"))
    else:
        results.append(("red", "Python 环境",
                         f"当前 {v.major}.{v.minor}，框架要求 ≥ {MIN_PY[0]}.{MIN_PY[1]}"))


def check_git_integrity(results, do_fix, brain_root):
    git_dir = os.path.join(brain_root, ".git")
    if not os.path.isdir(brain_root):
        results.append(("yellow", "Git 完整性",
                        f"脑根目录不存在：{brain_root}；请先按 SKILL.md 初始化大脑（记忆目录）"))
        return
    if os.path.isdir(git_dir):
        results.append(("ok", "Git 完整性", f"脑根 .git 存在，仓库完整（{brain_root}）"))
        return
    # .git 丢失/损坏 —— 不自动重建（需你的远程 URL，且涉及重写历史）
    results.append(("red", "Git 完整性",
                    f"脑根 .git 不存在或已损坏：仓库失去版本控制（工作区文件仍在，数据未丢）"))
    recipe = (
        f"cd {brain_root} && "
        "git init -b main && "
        "git remote add origin <你的远程URL> && "
        "git fetch origin main && "
        "git reset --mixed FETCH_HEAD && "
        "git checkout -- ."
    )
    results.append(("fix", "自愈配方（请确认远程 URL 后手动执行）", recipe))


def check_connectivity(results):
    import urllib.request
    probes = {
        "github.com:443": "https://github.com",
        "api.github.com": "https://api.github.com",
    }
    any_ok = False
    blocked = []
    for name, url in probes.items():
        try:
            urllib.request.urlopen(url, timeout=8)
            any_ok = True
        except Exception:
            blocked.append(name)
    if not blocked:
        results.append(("ok", "远程连通性", "github.com 与 api.github.com 均可达"))
    elif any_ok:
        # 至少一个通：指出哪个通道可用（写操作走 API 通道兜底）
        live = [n for n in probes if n not in blocked]
        results.append(("yellow", "远程连通性",
                        f"{'、'.join(blocked)} 暂时连不上（间歇性，常发生）；"
                        f"{'、'.join(live)} 仍可用，写操作可走 API 通道兜底"))
    else:
        results.append(("yellow", "远程连通性",
                        "全部连不上（网络/代理问题），稍后重试；"
                        "本地工作不受影响"))


def check_brain_state(results, do_fix, brain_root):
    missing = [f for f in BRAIN_STATE_FILES
               if not os.path.exists(os.path.join(brain_root, f))]
    if not missing:
        results.append(("ok", "脑状态文件", "index.md / ledger.md / VERSION.json 齐全"))
        return
    for f in missing:
        tpl = os.path.join(REPO, "templates", f)
        if do_fix and os.path.exists(tpl):
            try:
                import shutil
                os.makedirs(brain_root, exist_ok=True)
                shutil.copy(tpl, os.path.join(brain_root, f))
                results.append(("fix", f"补全 {f}",
                                f"已从框架 templates/{f} 生成到脑根 {brain_root} ✓"))
                continue
            except Exception as e:
                results.append(("red", f"补全 {f}", f"复制失败：{e}"))
        elif os.path.exists(tpl):
            results.append(("yellow", f"缺失 {f}",
                            f"可从模板生成：cp templates/{f} {brain_root}/{f}"))
        else:
            results.append(("yellow", f"缺失 {f}",
                            "无对应模板；请按 SKILL.md 的脑文件规范手动创建"))


def check_hook(results, do_fix, brain_root):
    hook = os.path.join(brain_root, ".git", "hooks", "post-commit")
    if os.path.exists(hook):
        results.append(("ok", "健康检查钩子",
                        f"脑根 .git/hooks/post-commit 已安装（{brain_root}）"))
        return
    if do_fix:
        try:
            os.makedirs(os.path.dirname(hook), exist_ok=True)
            with open(hook, "w", encoding="utf-8") as f:
                f.write(HOOK_CONTENT)
            try:
                os.chmod(hook, 0o755)
            except Exception:
                pass
            results.append(("fix", "安装钩子",
                            f"已装脑根 .git/hooks/post-commit（每次提交自动跑脑健康检查）✓"))
        except Exception as e:
            results.append(("red", "安装钩子", f"写入失败：{e}"))
    else:
        results.append(("yellow", "健康检查钩子",
                        "未安装；运行 `python tools/doctor.py --fix` 可一键安装"))


def check_skill_links(results):
    skill_md = os.path.join(REPO, "skill", "SKILL.md")
    if not os.path.exists(skill_md):
        return  # 非框架/技能仓库，跳过
    base = os.path.dirname(skill_md)
    text = open(skill_md, encoding="utf-8").read()
    links = re.findall(r"\]\(([^)]+)\)", text)
    broken = []
    for lnk in links:
        if lnk.startswith(("http://", "https://", "mailto:")):
            continue
        if lnk.startswith("#"):
            continue
        cand = _norm(os.path.join(base, lnk))
        if not os.path.exists(cand):
            broken.append(lnk)
    if not broken:
        results.append(("ok", "SKILL.md 引用链接", "所有 references/ docs/ 链接均真实存在"))
    else:
        detail = "；".join(broken[:8])
        results.append(("yellow", "SKILL.md 引用链接",
                        f"发现断裂链接 {len(broken)} 处（前8）：{detail}；"
                        f"请补齐对应文件或修正路径"))


def check_scrub(results):
    try:
        from scrub import check_tree
    except Exception:
        return
    hits = check_tree(REPO, exclude_dirs={"tools", ".git", ".build", "__pycache__"})
    if not hits:
        results.append(("ok", "脱敏残留", "未发现私人标识残留"))
    else:
        toks = "、".join(list(hits.keys())[:8])
        results.append(("yellow", "脱敏残留",
                        f"发现疑似私人标识：{toks}；"
                        f"跑 `python tools/assemble.py --check-only` 看明细，"
                        f"并把新标识加入 tools/scrub.py 的 SCRUB_MAP 后重跑"))


def print_report(results, as_json, brain_root):
    reds = [r for r in results if r[0] == "red"]
    yellows = [r for r in results if r[0] in ("yellow", "fix")]
    if as_json:
        out = {
            "tool": "doctor", "version": "1.0",
            "checked_at": NOW.strftime("%Y-%m-%d %H:%M"),
            "framework_root": REPO,
            "brain_root": brain_root,
            "severity": "red" if reds else ("yellow" if yellows else "green"),
            "results": [{"level": lv, "check": ck, "detail": dt}
                        for lv, ck, dt in results],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"═══ 第二大脑·环境诊断与自愈 v1.0 ═══  {NOW.strftime('%Y-%m-%d %H:%M')}")
        print(f"框架根（发布源）：{REPO}")
        print(f"脑根（你的记忆）：{brain_root}")
        print(f"严重度：{'红(需处理)' if reds else ('黄(建议)' if yellows else '绿(正常)')}")
        print("─" * 54)
        for lv, ck, dt in results:
            icon = {"ok": "✅", "yellow": "⚠️ ", "fix": "🔧", "red": "❌"}.get(lv, "·")
            # fix/red 详情可能本身是命令配方，单独成行更清晰
            print(f"  [{icon}] {ck}")
            for line in dt.split("\n"):
                print(f"        {line}")
        print("─" * 54)
        if reds:
            print("有红色项需先处理（见上方 ❌ / 🔧 配方）。")
        elif yellows:
            print("仅黄色建议项；加 --fix 可自动处理安全的补全项。")
        else:
            print("一切正常。")
    return 2 if reds else (1 if yellows else 0)


def main():
    ap = argparse.ArgumentParser(description="第二大脑·环境诊断与故障自愈")
    ap.add_argument("--fix", action="store_true", help="自动修复可自愈项（安全补全）")
    ap.add_argument("--brain-root", default=None,
                    help="指定脑根目录（默认 ~/.workbuddy/brain，或环境变量 SB_BRAIN）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 报告")
    args = ap.parse_args()

    brain_root = os.path.expanduser(args.brain_root) if args.brain_root else BRAIN_ROOT

    results = []
    check_python(results)
    check_git_integrity(results, args.fix, brain_root)
    check_connectivity(results)
    check_brain_state(results, args.fix, brain_root)
    check_hook(results, args.fix, brain_root)
    check_skill_links(results)
    check_scrub(results)

    return print_report(results, args.json, brain_root)


if __name__ == "__main__":
    sys.exit(main())

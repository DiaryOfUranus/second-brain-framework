#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assemble.py — 构建第二大脑开源纯净版（复制 + 脱敏编排）

把一份**私人第二大脑实例**的"框架部分"复制并脱敏到干净包，供开源。
本脚本是 `second-brain-opensource` 仓库的构建编排；也是他人 fork 自己脑时的入口。

它**只处理需要复制+脱敏的内容**（方法论 skill 树、机器可读 schema、定位白皮书）。
通用模板（templates/）、可移植治理脚本（meta/）、README/LICENSE/.gitignore 已由
仓库维护者直接维护，不在此脚本范围。

处理的源（可用环境变量覆盖，默认指向作者机器）：
  SB_SOURCE_BRAIN  : 私人脑仓库根（默认 ~/.workbuddy/brain）
  SB_SOURCE_SKILL  : 私人 second-brain skill 根（默认 ~/.workbuddy/skills/second-brain）

处理内容：
  skill/SKILL.md + references/*（剔除 base-*.md 理论 seed）+ scripts/* + skills/*（递归）
  两个机器可读 schema（GIR / CRL）
  定位白皮书 → docs/positioning.md

用法：
  python tools/assemble.py                       # 构建到本仓库根
  python tools/assemble.py --git                 # 构建并 git init + 初始提交
  python tools/assemble.py --check-only          # 仅校验无残留私人标识
"""

import os
import sys
import argparse
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scrub import scrub_file, scrub_tree, check_tree  # noqa: E402

SRC_BRAIN = os.environ.get("SB_SOURCE_BRAIN") or os.path.expanduser("~/.workbuddy/brain")
SRC_SKILL = os.environ.get("SB_SOURCE_SKILL") or os.path.expanduser("~/.workbuddy/skills/second-brain")
OUT = os.path.dirname(HERE)  # second-brain-opensource/

# skill 中需剔除的"理论 seed"（属私人理论原文，不进开源框架版）
SKILL_EXCLUDE_FILES = {"base-编译论.md", "base-共振理论.md", "base-文明秩序演进理论.md"}


def copy_scrub_skill():
    n = 0
    # SKILL.md
    src_skill_md = os.path.join(SRC_SKILL, "SKILL.md")
    if os.path.exists(src_skill_md):
        scrub_file(src_skill_md, os.path.join(OUT, "skill", "SKILL.md"))
        n += 1
    # references（剔除 base-*.md）
    ref_src = os.path.join(SRC_SKILL, "references")
    if os.path.isdir(ref_src):
        for fn in sorted(os.listdir(ref_src)):
            if not fn.endswith(".md"):
                continue
            if fn in SKILL_EXCLUDE_FILES:
                print(f"  [skip] references/{fn}（理论 seed，不进框架版）")
                continue
            scrub_file(os.path.join(ref_src, fn),
                       os.path.join(OUT, "skill", "references", fn))
            n += 1
    # scripts
    scr_src = os.path.join(SRC_SKILL, "scripts")
    if os.path.isdir(scr_src):
        for fn in sorted(os.listdir(scr_src)):
            if not fn.endswith(".py"):
                continue
            scrub_file(os.path.join(scr_src, fn),
                       os.path.join(OUT, "skill", "scripts", fn))
            n += 1
    # skills（子技能树，递归）
    sub_src = os.path.join(SRC_SKILL, "skills")
    if os.path.isdir(sub_src):
        cnt = scrub_tree(sub_src, os.path.join(OUT, "skill", "skills"))
        n += cnt
    return n


def copy_scrub_schemas():
    n = 0
    pairs = [
        ("kb/文明与认知/知识卡/卡-第二大脑_代际传承序列化格式_v0.1.schema.json",
         "schemas/gir_v0.1.schema.json"),
        ("kb/文明与认知/知识卡/卡-第二大脑_编译权分布台账_schema_v0.1.schema.json",
         "schemas/crl_v0.1.schema.json"),
    ]
    for src_rel, dst_rel in pairs:
        s = os.path.join(SRC_BRAIN, src_rel)
        if os.path.exists(s):
            scrub_file(s, os.path.join(OUT, dst_rel))
            n += 1
        else:
            print(f"  [warn] 源不存在：{s}")
    return n


def copy_scrub_whitepaper():
    src = os.path.join(SRC_BRAIN, "kb/文明与认知/第二大脑_vs_开源同类_定位与差异化白皮书.md")
    if os.path.exists(src):
        scrub_file(src, os.path.join(OUT, "docs", "positioning.md"))
        return 1
    print(f"  [warn] 白皮书源不存在：{src}")
    return 0


def git_init_commit():
    import subprocess
    if os.path.exists(os.path.join(OUT, ".git")):
        print("[git] 已存在 .git，跳过 init（仅提交）")
    else:
        subprocess.run(["git", "init"], cwd=OUT, check=True)
        print("[git] init 完成")
    subprocess.run(["git", "add", "-A"], cwd=OUT, check=True)
    msg = f"chore: initial open-source clean export of second-brain framework ({datetime.date.today().isoformat()})"
    r = subprocess.run(
        ["git", "-c", "user.email=second-brain@local", "-c", "user.name=second-brain",
         "commit", "-q", "-m", msg],
        cwd=OUT, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"[git] 已提交：{msg}")
    else:
        print(f"[git] 提交失败：{r.stderr}")


def main():
    ap = argparse.ArgumentParser(description="构建第二大脑开源纯净版")
    ap.add_argument("--git", action="store_true", help="构建后 git init + 初始提交")
    ap.add_argument("--check-only", action="store_true", help="仅校验无残留私人标识")
    args = ap.parse_args()

    if args.check_only:
        hits = check_tree(OUT, exclude_dirs={"tools", ".git", ".build"})
        if not hits:
            print("[check] 未发现残留私人标识 ✓")
            return 0
        for tok, files in hits.items():
            print(f"[check] 残留「{tok}」: {files[:10]}")
        return 1

    print(f"源·脑：{SRC_BRAIN}")
    print(f"源·skill：{SRC_SKILL}")
    print(f"目标：{OUT}")
    print("── 复制 + 脱敏 ──")
    ns = copy_scrub_skill()
    print(f"  skill: {ns} 文件")
    nsc = copy_scrub_schemas()
    print(f"  schemas: {nsc} 文件")
    nw = copy_scrub_whitepaper()
    print(f"  whitepaper: {nw} 文件")

    print("── 校验残留 ──")
    # 跳过 tools/（脱敏工具自身的定义文件会"点名"这些 token，属正常工作内容，非泄露）
    hits = check_tree(OUT, exclude_dirs={"tools", ".git", ".build"})
    if hits:
        print("[check] ⚠ 发现残留私人标识：")
        for tok, files in hits.items():
            print(f"  「{tok}」: {files[:10]}")
        print("请检查 SCRUB_MAP 后重跑；未清零前不要公开。")
        return 1
    print("[check] ✓ 无残留私人标识")

    if args.git:
        git_init_commit()
    else:
        print("（未加 --git，跳过 git 初始化；需要时重跑 `python tools/assemble.py --git`）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

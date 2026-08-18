#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrub.py — 第二大脑·脱敏工具（开源纯净版配套）

把一份**私人第二大脑**导出为不含私人标识的干净副本：把所有实例专属标识
（身份 / 平行实例名 / 雇主 / 城市 / 操作系统用户 / 私人路径）替换为 `{{占位符}}`。

本脚本是「开源撒种」流程的可复用件：你可以用它把自己的脑（或任何第二大脑实例）
脱敏后贡献给开源仓库，而不泄露私人数据。

用法：
  python tools/scrub.py --check <dir>          扫描目录，列出残留的私人标识
  python tools/scrub.py --in <file> --out <f>  脱敏单个文件
  python tools/scrub.py --tree <src> --dst <d> 递归脱敏整棵树（仅文本类文件）

文本类扩展名：.md .py .json .sh .txt .yaml .yml .toml .cfg .ini
"""

import os
import sys
import argparse

# ── 私人标识 → 占位符（顺序：最长/最具体优先）─────────────────────────────
# 注意：不做全局反斜杠归一（会破坏正则转义 `\.` 等合法反斜杠）。
# 故 Windows 路径同时覆盖正斜杠与反斜杠两种写法。
SCRUB_MAP = [
    ("天王星日记", "{{SOVEREIGN}}"),
    ("南京证券", "{{EMPLOYER}}"),
    ("衡枢", "{{SIBLING_A}}"),
    ("鉴枢", "{{SIBLING_B}}"),
    ("元枢", "{{INSTANCE_NAME}}"),
    ("Kimi", "{{REFERENCE_INSTANCE}}"),
    ("南京", "{{CITY}}"),
    # 路径（正斜杠与反斜杠两种都覆盖）
    ("C:/Users/Administrator/.workbuddy/brain", "{{BRAIN_ROOT}}"),
    ("C:/Users/Administrator/.workbuddy", "{{WORKBUDDY_HOME}}"),
    ("C:/Users/Administrator", "{{HOME}}"),
    ("C:\\Users\\Administrator\\.workbuddy\\brain", "{{BRAIN_ROOT}}"),
    ("C:\\Users\\Administrator\\.workbuddy", "{{WORKBUDDY_HOME}}"),
    ("C:\\Users\\Administrator", "{{HOME}}"),
    ("C:/PublicResources/SecondBrain/WorkBuddy元枢", "{{SHARED_WORKSPACE}}/SecondBrain/WorkBuddy{{INSTANCE_NAME}}"),
    ("C:/PublicResources/SecondBrain", "{{SHARED_WORKSPACE}}/SecondBrain"),
    ("C:/PublicResources/OriginalTheory", "{{THEORY_CANONICAL}}"),
    ("C:/PublicResources", "{{SHARED_WORKSPACE}}"),
    ("C:\\PublicResources\\SecondBrain\\WorkBuddy元枢", "{{SHARED_WORKSPACE}}/SecondBrain/WorkBuddy{{INSTANCE_NAME}}"),
    ("C:\\PublicResources\\SecondBrain", "{{SHARED_WORKSPACE}}/SecondBrain"),
    ("C:\\PublicResources\\OriginalTheory", "{{THEORY_CANONICAL}}"),
    ("C:\\PublicResources", "{{SHARED_WORKSPACE}}"),
    ("E:/twx", "{{THEORY_SOURCE}}"),
    ("E:\\twx", "{{THEORY_SOURCE}}"),
    ("D:/南京证券", "{{EMPLOYER_PATH}}"),
    ("D:\\南京证券", "{{EMPLOYER_PATH}}"),
    ("OriginalTheory", "{{THEORY_CANONICAL}}"),
    ("KnowledgeBase", "{{KNOWLEDGE_BASE}}"),
    ("SecondBrain", "{{SECOND_BRAIN_PKG}}"),
    ("C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe", "{{PYTHON}}"),
    ("C:\\Users\\Administrator\\.workbuddy\\binaries\\python\\versions\\3.13.12\\python.exe", "{{PYTHON}}"),
    ("WorkBuddy元枢", "WorkBuddy{{INSTANCE_NAME}}"),
    ("PublicResources", "{{SHARED_WORKSPACE_NAME}}"),
    ("Administrator", "{{OS_USER}}"),
]

TEXT_EXTS = {".md", ".py", ".json", ".sh", ".txt", ".yaml", ".yml",
             ".toml", ".cfg", ".ini", ".rst", ".markdown"}


def scrub_text(text):
    # 不做全局反斜杠归一（会破坏正则转义 `\.` 等合法反斜杠）；
    # Windows 路径的两种斜杠写法由 SCRUB_MAP 显式覆盖。
    for old, new in SCRUB_MAP:
        if old in text:
            text = text.replace(old, new)
    return text


def scrub_file(src, dst):
    with open(src, encoding="utf-8", errors="replace") as f:
        text = f.read()
    text = scrub_text(text)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)


def scrub_tree(src_root, dst_root):
    count = 0
    for root, dirs, files in os.walk(src_root):
        # 跳过不应复制的目录
        dirs[:] = [d for d in dirs if d not in {
            ".git", "__pycache__", "tmp", "inbox", "code-maps", "sessions", "UPGRADES", ".state"}]
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXTS:
                continue
            if fn in {".DS_Store", "export_sb.log"} or fn.endswith(".pyc"):
                continue
            s = os.path.join(root, fn)
            rel = os.path.relpath(s, src_root)
            d = os.path.join(dst_root, rel)
            scrub_file(s, d)
            count += 1
    return count


# 用于 --check 的"残留私人标识"原始词（脱敏后应全部为 0）
RAW_TOKENS = ["天王星日记", "南京证券", "元枢", "衡枢", "鉴枢", "Kimi",
              "C:/Users/Administrator", "C:/PublicResources", "E:/twx", "D:/南京证券",
              "Administrator"]


def check_tree(root, exclude_dirs=None):
    exclude_dirs = exclude_dirs or set()
    hits = {}
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXTS:
                continue
            p = os.path.join(r, fn)
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for tok in RAW_TOKENS:
                if tok in t:
                    hits.setdefault(tok, []).append(os.path.relpath(p, root))
    return hits


def main():
    ap = argparse.ArgumentParser(description="第二大脑·脱敏工具")
    ap.add_argument("--check", metavar="DIR", help="扫描目录，列出残留私人标识")
    ap.add_argument("--in", dest="inp", metavar="FILE", help="输入文件")
    ap.add_argument("--out", metavar="FILE", help="输出文件")
    ap.add_argument("--tree", metavar="SRC", help="递归脱敏的源目录")
    ap.add_argument("--dst", metavar="DIR", help="递归脱敏的目标目录")
    args = ap.parse_args()

    if args.check:
        hits = check_tree(args.check)
        if not hits:
            print(f"[scrub] 未发现残留私人标识 ✓ ({args.check})")
            return 0
        for tok, files in hits.items():
            print(f"[scrub] 残留「{tok}」({len(files)} 处):")
            for f in files[:10]:
                print(f"    {f}")
        return 1

    if args.inp and args.out:
        scrub_file(args.inp, args.out)
        print(f"[scrub] 已脱敏：{args.inp} → {args.out}")
        return 0

    if args.tree and args.dst:
        n = scrub_tree(args.tree, args.dst)
        print(f"[scrub] 已递归脱敏 {n} 个文件：{args.tree} → {args.dst}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

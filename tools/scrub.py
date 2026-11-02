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

私人标识映射（SCRUB_MAP/RAW_TOKENS）**不入库**：放在 tools/scrub_local.json
（已被 .gitignore 排除；可用环境变量 SB_SCRUB_CONFIG 指向其他路径）。
首次使用先 `cp tools/scrub_local.example.json tools/scrub_local.json` 再填入
你自己的标识——工具本身若硬编码映射，等于把"脱敏钥匙"连仓库一起公开。

文本类扩展名：.md .py .json .sh .txt .yaml .yml .toml .cfg .ini
"""

import os
import sys
import json
import argparse

CONFIG_NAME = "scrub_local.json"


class ScrubConfigMissing(RuntimeError):
    """私人标识配置缺失/非法（tools/scrub_local.json）。"""


def _config_path():
    return (os.environ.get("SB_SCRUB_CONFIG")
            or os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_NAME))


def load_private_config():
    """载入私人标识映射（tools/scrub_local.json·gitignore 不入库）。

    fail-closed：缺失/缺键/空映射 ⇒ 抛 ScrubConfigMissing——
    裸跑（空映射）会把「没脱」伪装成「已脱净」，比报错危险得多。
    """
    path = _config_path()
    if not os.path.isfile(path):
        raise ScrubConfigMissing(
            f"缺私人标识配置: {path}\n"
            f"  复制 tools/scrub_local.example.json → tools/scrub_local.json，"
            f"填入你自己的标识（该文件已被 .gitignore 排除，不会入库）。")
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
        scrub_map = [(str(old), str(new)) for old, new in cfg["scrub_map"]]
        raw_tokens = [str(t) for t in cfg["raw_tokens"]]
    except Exception as e:
        raise ScrubConfigMissing(
            f"配置格式错误（须含 scrub_map:[[旧,新],...] 与 raw_tokens:[...]，均非空）: {e}")
    if not scrub_map or not raw_tokens:
        raise ScrubConfigMissing("配置为空映射（scrub_map/raw_tokens 均不得为空——裸跑=假净）")
    # 排序：最长/最具体优先（路径前缀必须先于其短前缀替换）
    scrub_map.sort(key=lambda p: len(p[0]), reverse=True)
    return scrub_map, raw_tokens


_SCRUB_MAP = None
_RAW_TOKENS = None


def _ensure_config():
    # 惰性加载：import 本模块（doctor/assemble）不要求配置存在，
    # 只有真正执行脱敏/检查动作时才 fail-closed。
    global _SCRUB_MAP, _RAW_TOKENS
    if _SCRUB_MAP is None:
        _SCRUB_MAP, _RAW_TOKENS = load_private_config()

TEXT_EXTS = {".md", ".py", ".json", ".sh", ".txt", ".yaml", ".yml",
             ".toml", ".cfg", ".ini", ".rst", ".markdown"}


def scrub_text(text):
    # 不做全局反斜杠归一（会破坏正则转义 `\.` 等合法反斜杠）；
    # Windows 路径的两种斜杠写法由配置显式覆盖（最长/最具体优先）。
    _ensure_config()
    for old, new in _SCRUB_MAP:
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


# 用于 --check 的"残留私人标识"原始词（脱敏后应全部为 0）——同出自 scrub_local.json
def _raw_tokens():
    _ensure_config()
    return _RAW_TOKENS


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
            for tok in _raw_tokens():
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

    try:
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
    except ScrubConfigMissing as e:
        print(f"[scrub] {e}")
        return 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

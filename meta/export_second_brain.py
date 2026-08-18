#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_second_brain.py — 把本机第二大脑导出为干净交换包

零依赖（stdlib only）。设计目的：
  把持久脑内容复制为一个"干净包"，便于与其他本地工具 / 平行实例 / 外部审阅者
  交换（不含 sessions/audits/tmp/inbox/code-maps/.git 等会话级或派生内容，
  也不含 self-model.md 等含私人身份/本地配置的敏感文件）。

流程：
  1. 从脑仓库根复制**持久**脑内容到暂存 .build 目录；
     排除：.git / sessions / audits / tmp / inbox / code-maps / __pycache__ / .state /
           self-model.md / *.pyc。
  2. 生成 MANIFEST.json（对齐 second-brain-upgrade v1；contains_local_config 按实际
     导出内容动态判定、embeds_theory=false、theory_pointer 指向外部 canonical）。
  3. 生成 STATE.md（当前脑状态/变更/时间/原因/排除清单）。
  4. 原子交换：.build → 正式目录（防读到半成品）。

便携性：
  - 包名通过环境变量 SB_PACKAGE 指定，默认 "second-brain"。
  - 输出目录通过环境变量 SB_PUB_DIR 指定，默认 ~/second-brain-export。
  - self_name 为占位符 {{INSTANCE_NAME}}（由接收方实例化时替换）。
"""

import os
import re
import sys
import json
import shutil
import hashlib
import datetime

PKG = os.environ.get("SB_PACKAGE") or "second-brain"
PUB_DIR = os.environ.get("SB_PUB_DIR") or os.path.expanduser("~/second-brain-export")
PUB_ROOT = os.path.join(PUB_DIR, PKG)

EXCLUDE_DIRS = {".git", "sessions", "audits", "tmp", "inbox", "code-maps", "__pycache__", ".state", "logs"}
EXCLUDE_FILES = {".DS_Store", "export_sb.log", "self-model.md"}
EXCLUDE_SUFFIXES = (".pyc",)

# 用于 MANIFEST.contains_local_config 动态判定与 --audit 报告的敏感模式
SENSITIVE_DIRS = {"sessions", "audits"}
SENSITIVE_FILES = {"self-model.md"}
# 简单启发式：检测常见凭证/密钥/token 残留（仅前 8KB，避免大文件慢扫）
TOKEN_PATTERNS = [
    re.compile(rb"gh[pousr]_[A-Za-z0-9_]{36,}", re.IGNORECASE),   # GitHub PAT
    re.compile(rb"sk-[a-zA-Z0-9]{48,}", re.IGNORECASE),           # OpenAI/类 API key
    re.compile(rb"[a-zA-Z0-9_-]*(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"']?[\w\-./+=]{16,}", re.IGNORECASE),
]
TOKEN_PREVIEW_BYTES = 8192

SCHEMA = "1.0"

# 脑仓库根：脚本位置自动推导；可用 SB_BRAIN 覆盖
BRAIN = os.environ.get("SB_BRAIN") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


def ts():
    return datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=8))
    ).isoformat()


def should_skip(name):
    if name in EXCLUDE_DIRS or name in EXCLUDE_FILES:
        return True
    if name.endswith(EXCLUDE_SUFFIXES):
        return True
    return False


def copy_tree(src, dst):
    for entry in os.scandir(src):
        if should_skip(entry.name):
            continue
        s = entry.path
        d = os.path.join(dst, entry.name)
        if entry.is_dir():
            copy_tree(s, d)
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)


def scan_tree(src, rel_prefix=""):
    """返回 (included, excluded) 两个相对路径列表，与 copy_tree 使用同一跳过规则。"""
    included, excluded = [], []
    try:
        entries = list(os.scandir(src))
    except OSError as e:
        return included, [f"{rel_prefix or src} (无法读取: {e})"]
    for entry in entries:
        rel = os.path.join(rel_prefix, entry.name).replace("\\", "/")
        if should_skip(entry.name):
            excluded.append(rel)
            continue
        if entry.is_dir():
            inc, exc = scan_tree(entry.path, rel)
            included.extend(inc)
            excluded.extend(exc)
        else:
            included.append(rel)
    return included, excluded


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _force_remove(path):
    if not os.path.exists(path):
        return
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for fn in files:
                try:
                    os.remove(os.path.join(root, fn))
                except OSError:
                    pass
            for dn in dirs:
                try:
                    os.rmdir(os.path.join(root, dn))
                except OSError:
                    pass
        try:
            os.rmdir(path)
        except OSError:
            pass
    else:
        try:
            os.remove(path)
        except OSError:
            pass


def _rename_with_retry(src, dst, tries=6, delay=0.5):
    last = None
    for _ in range(tries):
        try:
            os.rename(src, dst)
            return
        except OSError as e:
            last = e
            time_sleep(delay)
    if os.path.exists(dst):
        _force_remove(dst)
    copy_tree(src, dst)
    _force_remove(src)


def time_sleep(d):
    import time
    time.sleep(d)


def load_version():
    vf = os.path.join(BRAIN, "VERSION.json")
    if os.path.exists(vf):
        with open(vf, encoding="utf-8") as f:
            return json.load(f)
    return {"current_version": None, "current_commit": None}


def latest_changelog_summary(n=1):
    cf = os.path.join(BRAIN, "CHANGELOG.md")
    if not os.path.exists(cf):
        return ""
    with open(cf, encoding="utf-8") as f:
        txt = f.read()
    blocks = re.split(r"\n##\s+", txt)
    out = []
    for b in blocks[1: 1 + n + 1]:
        out.append("## " + b.strip())
    return "\n".join(out)[:2000]


def _is_sensitive_path(rel):
    """判断相对路径是否属于会话级/本地敏感内容（用于动态判定与审计）。"""
    parts = rel.split("/")
    if any(p in SENSITIVE_DIRS for p in parts):
        return True
    if rel in SENSITIVE_FILES or any(p in SENSITIVE_FILES for p in parts):
        return True
    return False


def _scan_token_leak(path):
    """扫描文件前 TOKEN_PREVIEW_BYTES 字节是否含常见凭证/token 模式。"""
    try:
        with open(path, "rb") as f:
            head = f.read(TOKEN_PREVIEW_BYTES)
    except OSError:
        return False
    for pat in TOKEN_PATTERNS:
        if pat.search(head):
            return True
    return False


def _contains_local_config(artifacts, root=None):
    """MANIFEST.contains_local_config 动态判定：
    只要导出产物里仍含 sessions/audits/self-model.md 或扫描到 token/PAT 残留，就标 true。
    root: 用于内容扫描的根目录（dry-run 时用 BRAIN，实际导出后用 files_dir）。
    """
    for rel in artifacts:
        if _is_sensitive_path(rel):
            return True
        if root is not None and _scan_token_leak(os.path.join(root, rel)):
            return True
    return False


def _list_sensitive_hits(artifacts, root=None):
    """返回触发 contains_local_config=true 的具体依据列表。"""
    hits = []
    for rel in artifacts:
        if _is_sensitive_path(rel):
            hits.append(f"敏感路径: {rel}")
        if root is not None:
            full = os.path.join(root, rel)
            if _scan_token_leak(full):
                hits.append(f"疑似凭证残留: {full}")
    return hits


def _print_audit(included, excluded, sensitive_hits, contains_local_config):
    print("\n=== 导出审计报告 ===")
    print(f"包含文件数: {len(included)}")
    print(f"排除路径数: {len(excluded)}")
    print(f"MANIFEST.contains_local_config: {contains_local_config}")
    if sensitive_hits:
        print("敏感内容依据:")
        for h in sensitive_hits:
            print(f"  ⚠️  {h}")
    else:
        print("敏感内容依据: 未发现")
    print("====================")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="导出第二大脑干净交换包")
    parser.add_argument("--dry-run", action="store_true",
                        help="只扫描并报告会包含/排除哪些文件，不生成包")
    parser.add_argument("--audit", action="store_true",
                        help="导出完成后打印审计报告")
    args = parser.parse_args()

    if not os.path.isdir(BRAIN):
        print(f"❌ 脑目录不存在：{BRAIN}")
        sys.exit(1)

    # 先扫描源目录，用于 dry-run 和预判敏感内容
    included, excluded = scan_tree(BRAIN)

    if args.dry_run:
        print(f"DRY-RUN: 源目录 = {BRAIN}")
        print(f"  将包含 {len(included)} 个文件")
        for p in sorted(included):
            print(f"    + {p}")
        print(f"  将排除 {len(excluded)} 个路径")
        for p in sorted(excluded):
            print(f"    - {p}")
        pred = _contains_local_config(included, root=BRAIN)
        print(f"  MANIFEST.contains_local_config 将判定为: {pred}")
        return

    build = PUB_ROOT + ".build"
    if os.path.exists(build):
        _force_remove(build)
    files_dir = os.path.join(build, "files")
    os.makedirs(files_dir, exist_ok=True)
    copy_tree(BRAIN, files_dir)

    ver = load_version()
    v = ver.get("current_version")
    commit = ver.get("current_commit")

    artifacts = []
    checksums = {}
    for root, dirs, fns in os.walk(files_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in fns:
            if fn in EXCLUDE_FILES or fn.endswith(EXCLUDE_SUFFIXES):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, files_dir).replace("\\", "/")
            artifacts.append(rel)
            checksums[rel] = "sha256:" + sha256(full)

    # 动态判定：如果导出产物里仍含敏感路径/token 残留，诚实标 true
    contains_local_config = _contains_local_config(artifacts, root=files_dir)
    sensitive_hits = _list_sensitive_hits(artifacts, root=files_dir)

    manifest = {
        "format": "second-brain-upgrade",
        "format_version": SCHEMA,
        "package": "second-brain-upgrade",
        "tool_name": "WorkBuddy",
        "self_name": "{{INSTANCE_NAME}}",
        "version": v or "unknown",
        "commit": commit,
        "exported_at": ts(),
        "contains_local_config": contains_local_config,
        "embeds_theory": False,
        "theory_pointer": "{{THEORY_CANONICAL}}",
        "files": [{"path": p, "sha256": checksums[p]} for p in sorted(artifacts)],
        "capability_map": {
            "declaration_gate": True,
            "command_guard": True,
            "upgrade_pack": True,
            "brain_commit": True,
            "brain_check": True,
            "offline_drill": True,
        },
        "interop": {
            "import_mode": "staged",
            "note": "脑内容（派生 seed + meta/DNA + 状态账）。理论原文不在本包，指针见 theory_pointer。",
        },
    }
    with open(os.path.join(build, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    state = [
        f"# 第二大脑状态卡（{PKG}）",
        f"- 实例：{{{{INSTANCE_NAME}}}}（本地独立演进的第二大脑实例）",
        f"- 当前版本：{v}",
        f"- 对齐 git commit：{commit}",
        f"- 导出时间：{ts()}",
        f"- 本次导出原因：生成干净交换包",
        f"- 已排除：.git / sessions / audits / tmp / inbox / code-maps / logs / self-model.md / *.pyc",
        f"- 包含文件数：{len(artifacts)}",
        f"- MANIFEST.contains_local_config：{contains_local_config}",
        f"- 理论：本包 embeds_theory=false，指针 → {manifest['theory_pointer']}（canonical 由接收方配置）",
        f"",
        f"## 最近变更（CHANGELOG 摘）",
        latest_changelog_summary(1) or "（无）",
    ]
    with open(os.path.join(build, "STATE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(state))

    final = PUB_ROOT
    backup = PUB_ROOT + ".prev"
    if os.path.exists(final):
        if os.path.exists(backup):
            _force_remove(backup)
        os.rename(final, backup)
    _rename_with_retry(build, final)
    print(f"exported → {final} ({len(artifacts)} files, version {v}, contains_local_config={contains_local_config})")

    if args.audit:
        _print_audit(included, excluded, sensitive_hits, contains_local_config)


if __name__ == "__main__":
    main()

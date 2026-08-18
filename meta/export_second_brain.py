#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_second_brain.py — 把本机第二大脑导出为干净交换包

零依赖（stdlib only）。设计目的：
  把持久脑内容复制为一个"干净包"，便于与其他本地工具 / 平行实例 / 外部审阅者
  交换（不含 tmp/inbox/code-maps/.git 等会话级或派生内容）。

流程：
  1. 从脑仓库根复制**持久**脑内容到暂存 .build 目录；
     排除：.git / tmp / inbox / code-maps / __pycache__ / .state / *.pyc。
  2. 生成 MANIFEST.json（对齐 second-brain-upgrade v1；contains_local_config=false、
     embeds_theory=false、theory_pointer 指向外部 canonical）。
  3. 生成 STATE.md（当前脑状态/变更/时间/原因）。
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

EXCLUDE_DIRS = {".git", "tmp", "inbox", "code-maps", "__pycache__", ".state"}
EXCLUDE_FILES = {".DS_Store", "export_sb.log"}
EXCLUDE_SUFFIXES = (".pyc",)

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


def main():
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

    manifest = {
        "format": "second-brain-upgrade",
        "format_version": SCHEMA,
        "package": "second-brain-upgrade",
        "tool_name": "WorkBuddy",
        "self_name": "{{INSTANCE_NAME}}",
        "version": v or "unknown",
        "commit": commit,
        "exported_at": ts(),
        "contains_local_config": False,
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
        f"- 本次导出原因：生成干净交换包（剔除 tmp/inbox/code-maps/.git）",
        f"- 包含文件数：{len(artifacts)}",
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
    print(f"exported → {final} ({len(artifacts)} files, version {v})")


if __name__ == "__main__":
    main()

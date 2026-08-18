#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_pack.py — 第二大脑升级包管理（可与其他管理工具交换，开源便携版）

零依赖（stdlib only）。设计目的：
  第二大脑从初版演进到当前，需要一套可追溯、可交换的升级管理机制，便于与
  平行实例或其他管理工具互通能力。本脚本是这套机制的"引擎"。

命令：
  list                         列出 VERSION.json 中登记的所有版本
  changelog [--ver vX.Y.Z]    打印升级说明（默认读 brain/CHANGELOG.md）
  snapshot <ver>              在 VERSION.json 指明的 git 边界 commit 快照 meta/ → UPGRADES/<ver>/
  gen-all                     依次 snapshot 所有 git_backed 版本
  export <ver> [--out p.zip]  把 UPGRADES/<ver>/ 打成 zip（可传输升级包）
  import <pkg.json>           把外部升级包暂存到 brain/inbox/<id>/ 待接收方审核（不自动覆盖）

交换格式：manifest.json 遵循 "second-brain-upgrade" v1 schema
（见 skill/references/upgrade-manager.md）。

便携性：脑仓库根通过环境变量 SB_BRAIN 指定，默认 ~/.workbuddy/brain。
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
import datetime
import argparse

BRAIN = os.environ.get("SB_BRAIN") or os.path.expanduser("~/.workbuddy/brain")
META = os.path.join(BRAIN, "meta")
UPG = os.path.join(BRAIN, "UPGRADES")
INBOX = os.path.join(BRAIN, "inbox")
VERSION_FILE = os.path.join(BRAIN, "VERSION.json")
CHANGELOG = os.path.join(BRAIN, "CHANGELOG.md")
SCHEMA = "1.0"

# 能力映射：脚本路径 -> 该能力对另一实例的"可获得价值"（交换时让对方知道得到什么）。
# 仅列出本开源包随附的治理脚本；各实例可按自身布局自行扩充。
CAP_MAP = {
    "meta/brain_check.py": "脑健康检查器：结构/台账/过期/日志/备份/脱脑 六项硬检查，post-commit 自动触发",
    "meta/brain_offline_drill.py": "脱脑依赖度演练：无脑状态跑基准任务，把对脑的依赖变为可观测量",
    "meta/brain_commit.py": "脑库代谢后自动提交：任何代谢后把脑目录变更提交进 Git，无变更跳过",
    "meta/export_second_brain.py": "脑导出：把持久脑内容复制为干净交换包（剔除 tmp/inbox/code-maps）",
    "meta/upgrade_pack.py": "升级包引擎：snapshot/gen-all/export/import，能力可交换",
}


def git(*args, check=True):
    r = subprocess.run(["git", "-C", BRAIN, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    return r.stdout.strip()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"format_version": SCHEMA, "current_version": None, "current_commit": None, "versions": []}


def snapshot_meta(commit, dest):
    """在 <commit> 处快照 meta/ 到 dest/files/，返回 (artifacts, changes)。"""
    files_dir = os.path.join(dest, "files")
    if os.path.exists(files_dir):
        shutil.rmtree(files_dir)
    os.makedirs(files_dir, exist_ok=True)
    out = git("ls-tree", "-r", "--name-only", commit, "meta/")
    artifacts = []
    for rel in out.splitlines():
        if not rel.startswith("meta/"):
            continue
        if "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        blob = git("show", f"{commit}:{rel}")
        rest = rel[len("meta/"):]
        target = os.path.join(files_dir, rest)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(blob)
        artifacts.append(rel)
    return artifacts


def diff_changes(prev_commit, commit):
    changes = []
    if prev_commit:
        out = git("diff", "--name-status", prev_commit, commit, "meta/")
        for line in out.splitlines():
            if not line.strip():
                continue
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            status, path = parts
            t = {"A": "add", "M": "modify", "D": "remove", "R": "rename"}.get(status[0], "modify")
            changes.append({"type": t, "path": path, "capability": CAP_MAP.get(path, "")})
    return changes


def build_manifest(ver, vinfo, prev_commit):
    commit = vinfo["commit"]
    dest = os.path.join(UPG, ver)
    artifacts = snapshot_meta(commit, dest)
    changes = diff_changes(prev_commit, commit)
    # 仅首个版本（无前驱 commit）在无 diff 时回退为"全新增"；其余版本空 diff 如实留空
    if not changes and prev_commit is None and artifacts:
        changes = [{"type": "add", "path": a, "capability": CAP_MAP.get(a, "")} for a in artifacts]
    manifest = {
        "format": "second-brain-upgrade",
        "format_version": SCHEMA,
        "package_id": f"{ver}-{commit}",
        "from_version": vinfo.get("from_version"),
        "to_version": ver,
        "generated_at": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
        "source_instance": {
            "name": "{{INSTANCE_NAME}}",
            "brain_root": BRAIN,
            "owner": "{{SOVEREIGN}}",
            "note": "WorkBuddy 本地第二大脑实例；与平行实例各自独立演进",
        },
        "summary": vinfo.get("summary", ver),
        "git_commit": commit,
        "changes": changes,
        "artifacts": artifacts,
        "interop": {
            "compatible_targets": ["其他 WorkBuddy 第二大脑实例",
                                   "任意支持 second-brain-upgrade v1 的管理工具"],
            "import_mode": "staged",
            "import_instructions": "用 `upgrade_pack.py import <manifest.json>` 把包暂存到 <target_brain>/inbox/<id>/；接收方审核 files/ 后手动并入自身 meta/ 并按自身 skill 布局重注册（SKILL.md 注册为实例特有，不自动覆盖）",
            "registration_note": "meta/ 脚本为可移植 DNA；second-brain/SKILL.md 的受管登记为实例特有，导入方须自行重注册",
        },
        "checksum": {},
    }
    for a in artifacts:
        fp = os.path.join(dest, "files", a[len("meta/"):])
        if os.path.exists(fp):
            manifest["checksum"][a] = "sha256:" + sha256(fp)
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


def cmd_list(args):
    d = load_version()
    print(f"当前版本: {d.get('current_version')} @ {d.get('current_commit')}")
    print(f"{'版本':10} {'日期':12} {'git':10} {'摘要'}")
    for v in d.get("versions", []):
        print(f"{v['version']:10} {v.get('date','-'):12} {(v.get('commit') or '-'):10} {v.get('summary','')}")


def cmd_changelog(args):
    if args.ver:
        d = load_version()
        for v in d.get("versions", []):
            if v["version"] == args.ver:
                print(json.dumps(v, ensure_ascii=False, indent=2))
                return
        print(f"未找到版本 {args.ver}")
        return
    if os.path.exists(CHANGELOG):
        with open(CHANGELOG, encoding="utf-8") as f:
            print(f.read())
    else:
        print("CHANGELOG.md 不存在")


def cmd_snapshot(args):
    d = load_version()
    vinfo = next((v for v in d["versions"] if v["version"] == args.version), None)
    if not vinfo:
        print(f"VERSION.json 中无 {args.version}")
        sys.exit(1)
    if not vinfo.get("git_backed"):
        print(f"{args.version} 非 git 支撑版本，无法快照 meta/")
        sys.exit(1)
    prev = None
    for v in d["versions"]:
        if v["version"] == args.version:
            break
        if v.get("git_backed"):
            prev = v.get("commit")
    m = build_manifest(args.version, vinfo, prev)
    print(f"snapshot {args.version}: {len(m['artifacts'])} artifacts, {len(m['changes'])} changes → UPGRADES/{args.version}/")


def cmd_gen_all(args):
    d = load_version()
    for v in d["versions"]:
        if v.get("git_backed"):
            prev = None
            for pv in d["versions"]:
                if pv["version"] == v["version"]:
                    break
                if pv.get("git_backed"):
                    prev = pv.get("commit")
            m = build_manifest(v["version"], v, prev)
            print(f"  {v['version']}: {len(m['artifacts'])} artifacts")


def cmd_export(args):
    src = os.path.join(UPG, args.version)
    if not os.path.isdir(src):
        print(f"UPGRADES/{args.version} 不存在，先 snapshot")
        sys.exit(1)
    out = args.out or os.path.join(UPG, f"{args.version}.zip")
    if os.path.exists(out):
        os.remove(out)
    shutil.make_archive(out[:-4], "zip", src)
    print(f"exported → {out}")


def cmd_import(args):
    pkg = args.package
    with open(pkg, encoding="utf-8") as f:
        m = json.load(f)
    pid = m.get("package_id", "unknown")
    dest = os.path.join(INBOX, pid)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    src_files = os.path.join(os.path.dirname(os.path.abspath(pkg)), "files")
    if os.path.isdir(src_files):
        shutil.copytree(src_files, os.path.join(dest, "files"))
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    report = [
        f"# 升级包导入暂存报告",
        f"- 包ID: {pid}",
        f"- 来源实例: {m.get('source_instance', {}).get('name', '?')}（owner={m.get('source_instance', {}).get('owner', '?')}）",
        f"- 版本: {m.get('from_version')} → {m.get('to_version')}",
        f"- 摘要: {m.get('summary')}",
        f"- 产物数: {len(m.get('artifacts', []))}",
        f"- 变更数: {len(m.get('changes', []))}",
        f"",
        f"## 下一步（接收方手动）",
        f"1. 审阅 inbox/{pid}/files/ 中脚本",
        f"2. 按自身 meta/ 布局并入（注意：不要覆盖本实例已有同名文件的差异）",
        f"3. 按自身 second-brain/SKILL.md 布局重注册受管能力",
        f"4. 如接受，记录到本实例 CHANGELOG 与 audit-log",
    ]
    with open(os.path.join(dest, "IMPORT-REPORT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"已暂存到 {dest}（未自动应用，请审核 IMPORT-REPORT.md）")


def main():
    ap = argparse.ArgumentParser(description="第二大脑升级包管理")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("list")
    p_cl = sub.add_parser("changelog")
    p_cl.add_argument("--ver", default=None)
    p_sn = sub.add_parser("snapshot")
    p_sn.add_argument("version")
    sub.add_parser("gen-all")
    p_ex = sub.add_parser("export")
    p_ex.add_argument("version")
    p_ex.add_argument("--out", default=None)
    p_im = sub.add_parser("import")
    p_im.add_argument("package")

    args = ap.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "changelog":
        cmd_changelog(args)
    elif args.cmd == "snapshot":
        cmd_snapshot(args)
    elif args.cmd == "gen-all":
        cmd_gen_all(args)
    elif args.cmd == "export":
        cmd_export(args)
    elif args.cmd == "import":
        cmd_import(args)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()

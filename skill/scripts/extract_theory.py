#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_theory.py — 超长理论文献的脚本化提取工具（theory-extract-formalize 子技能）

设计目标：
  处理数十万字级的专著/多卷理论时，避免把全文灌入 AI 上下文窗口。
  本脚本只做「只读扫描 + 命中摘录 + 索引」，产出的小文件由 AI 定点读取合成。

用法：
  python extract_theory.py --source <目录或文件...> --terms <术语表> --out <项目目录> [--context 3]

  --source  源文献：一个目录（递归扫描指定扩展名）或用空格分隔的多个文件。
  --terms   术语表：逗号分隔的关键词，或用 @词表文件 指定（每行一个，# 开头为注释）。
  --out     项目输出目录（自动创建 01_原文提取 / 05_命中索引.md / 06_章节大纲.md）。
  --context 命中行上下文字数（行），默认 3。重叠窗口自动合并。
  --ext     扫描扩展名，默认 .md（多值用逗号，如 .md,.txt）。

输出：
  01_原文提取/<源文件基名>_<术语>.md   每段摘录含 `源文件:行号` 锚点
  05_命中索引.md                       每术语×每文件的命中计数 + 明细
  06_章节大纲.md                       每源文件的 Markdown 标题大纲

注意：本脚本只读，不修改任何源文件。
"""

import argparse
import os
import re
import sys

# ---------- 工具函数 ----------

def sanitize(name: str) -> str:
    """把术语/文件名变成安全片段。"""
    s = re.sub(r'[^\w一-鿿]+', '_', name)
    return s.strip('_') or 'term'

def load_terms(spec: str):
    """从逗号串或 @文件 载入术语表。"""
    if spec.startswith('@'):
        path = spec[1:]
        terms = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    terms.append(line)
        return terms
    return [t.strip() for t in spec.split(',') if t.strip()]

def collect_sources(source_args, exts):
    sources = []
    for s in source_args:
        if os.path.isdir(s):
            for root, _, files in os.walk(s):
                for fn in files:
                    if any(fn.lower().endswith(e) for e in exts):
                        sources.append(os.path.join(root, fn))
        elif os.path.isfile(s):
            sources.append(s)
        else:
            print(f"[warn] 跳过不存在的源：{s}", file=sys.stderr)
    # 去重保序
    seen = set()
    uniq = []
    for p in sources:
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            uniq.append(p)
    return uniq

def extract_file_hits(path, terms, context):
    """返回 {term: [(lineno, [context_lines])]}。"""
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    results = {t: [] for t in terms}
    compiled = [(t, re.compile(re.escape(t), re.IGNORECASE)) for t in terms]
    for i, line in enumerate(lines, start=1):
        for t, rx in compiled:
            if rx.search(line):
                # 合并上下文窗口：记录 (start, end, hit_lineno)
                results[t].append(i)
    return lines, results

def merge_windows(hit_lines, total, context):
    """把命中的行号合并成不重叠的上下文窗口列表 [(start,end)]。"""
    if not hit_lines:
        return []
    windows = []
    cur_start = max(1, hit_lines[0] - context)
    cur_end = min(total, hit_lines[0] + context)
    for hl in hit_lines[1:]:
        ns = max(1, hl - context)
        ne = min(total, hl + context)
        if ns <= cur_end + 1:  # 重叠或相邻，合并
            cur_end = max(cur_end, ne)
        else:
            windows.append((cur_start, cur_end))
            cur_start, cur_end = ns, ne
    windows.append((cur_start, cur_end))
    return windows

def write_extract_files(out_dir, src_path, terms, lines, results, context):
    """为每个 (源文件, 术语) 写出摘录文件，返回该源文件的命中统计。"""
    base = sanitize(os.path.splitext(os.path.basename(src_path))[0])
    extract_root = os.path.join(out_dir, '01_原文提取')
    os.makedirs(extract_root, exist_ok=True)
    total = len(lines)
    stat = {}  # term -> count
    for t in terms:
        hits = results[t]
        if not hits:
            stat[t] = 0
            continue
        stat[t] = len(hits)
        windows = merge_windows(hits, total, context)
        fname = f"{base}_{sanitize(t)}.md"
        fpath = os.path.join(extract_root, fname)
        with open(fpath, 'w', encoding='utf-8') as out:
            out.write(f"# 原文提取 · {os.path.basename(src_path)} · 术语「{t}」\n\n")
            out.write(f"> 源文件：`{src_path}` ｜ 命中 {len(hits)} 处 ｜ 上下文 ±{context} 行\n\n")
            for wi, (s, e) in enumerate(windows, 1):
                out.write(f"## 摘录 {wi}（行 {s}–{e}）\n\n")
                for ln in range(s, e + 1):
                    marker = '▶' if (ln in hits) else ' '
                    out.write(f"{marker} {ln}: {lines[ln-1].rstrip()}\n")
                out.write("\n")
    return stat

def write_outline(out_dir, src_path, lines):
    """提取 Markdown 标题作为章节大纲。"""
    outline = []
    for i, line in enumerate(lines, 1):
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            outline.append((level, i, m.group(2).strip()))
    return outline

def main():
    ap = argparse.ArgumentParser(description='超长理论文献脚本化提取工具')
    ap.add_argument('--source', nargs='+', required=True, help='源目录或文件（可多个）')
    ap.add_argument('--terms', required=True, help='术语表：逗号分隔，或 @词表文件')
    ap.add_argument('--out', required=True, help='项目输出目录')
    ap.add_argument('--context', type=int, default=3, help='上下文字数（行），默认 3')
    ap.add_argument('--ext', default='.md', help='扫描扩展名，逗号分隔，默认 .md')
    args = ap.parse_args()

    exts = tuple(e if e.startswith('.') else '.' + e for e in args.ext.split(','))
    terms = load_terms(args.terms)
    sources = collect_sources(args.source, exts)
    if not sources:
        print('[error] 没有找到任何源文件。', file=sys.stderr)
        sys.exit(1)
    os.makedirs(args.out, exist_ok=True)

    all_stats = {}      # src_path -> {term: count}
    all_outlines = {}   # src_path -> [(level, lineno, title)]

    for src in sources:
        try:
            lines, results = extract_file_hits(src, terms, args.context)
        except Exception as e:
            print(f"[warn] 读取失败 {src}: {e}", file=sys.stderr)
            continue
        stat = write_extract_files(args.out, src, terms, lines, results, args.context)
        all_stats[src] = stat
        all_outlines[src] = write_outline(src, lines)

    # 05_命中索引.md
    idx_path = os.path.join(args.out, '05_命中索引.md')
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write('# 命中索引\n\n')
        f.write('| 源文件 | ' + ' | '.join(terms) + ' | 合计 |\n')
        f.write('|---' * (len(terms) + 2) + '|\n')
        grand = 0
        for src, stat in all_stats.items():
            row = [f'{os.path.basename(src)}']
            tot = 0
            for t in terms:
                row.append(str(stat.get(t, 0)))
                tot += stat.get(t, 0)
            row.append(str(tot))
            grand += tot
            f.write('| ' + ' | '.join(row) + ' |\n')
        f.write(f'\n**总命中数：{grand}**\n')

    # 06_章节大纲.md
    ol_path = os.path.join(args.out, '06_章节大纲.md')
    with open(ol_path, 'w', encoding='utf-8') as f:
        f.write('# 章节大纲\n\n')
        for src, outline in all_outlines.items():
            f.write(f'## {os.path.basename(src)}\n\n')
            if not outline:
                f.write('（未检测到 Markdown 标题）\n\n')
            for level, ln, title in outline:
                f.write(f'{"  " * (level-1)}- L{ln} {title}\n')
            f.write('\n')

    print(f"[ok] 提取完成：{len(sources)} 个源文件，{len(terms)} 个术语，{grand} 处命中")
    print(f"     输出目录：{args.out}")
    print(f"     摘录：{os.path.join(args.out, '01_原文提取')}")
    print(f"     索引：{idx_path}")
    print(f"     大纲：{ol_path}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-guardrails — 生成后 QA 校验层
====================================
捕获 agent 生成 PPT / HTML / H5 的三类通病（来自 PowerPoint Skill Review 实证）：

  P0  占位符残留   模板标记 / TODO / 未替换字段残留在最终产物里
  P1  对比度失效   文字与背景 WCAG 对比度过低（投影/手机上看不见）
  P2  溢出风险     固定高度容器内塞入过长文本（需人工最终确认）

不依赖任何第三方包（纯标准库），便于在托管 Python 环境直接跑。

用法:
  python qa_guardrails.py <file_or_dir> [--json]
支持扩展名: .html .htm .md .txt .pptx
"""
import sys, os, re, json, zipfile, glob

# ---------- 占位符残留规则 ----------
# 注意：TODO/FIXME 必须大写且带边界（如 [TODO] / TODO:），避免误伤
# 合法标识符里的 todo 状态（data-status="todo" / class="s-todo" / 待启动）。
# 大小写不敏感的只限少数英文词，故去掉全局 re.I，按需用 (?i:)。
PLACEHOLDER_RE = re.compile(
    r'\[必填\]'
    r'|替换为'
    r'|未替换'
    r'|占位'
    r'|(?i:placeholder)'
    r'|(?i:lorem ipsum)'
    r'|待填|待补'
    r'|____{2,}'
    r'|XXXX'
    r'|\{\{|\}\}'          # 双花括号模板
    r'|\{[a-zA-Z_][a-zA-Z0-9_]*\}'  # 单花括号变量 {var}
    r'|(?<![\w"\'])(?:TODO|FIXME)(?![\w"\'])'  # 仅大写+边界，排除 todo 状态
)

# ---------- 颜色解析 ----------
HEX_RE = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b')
RGB_RE = re.compile(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', re.I)

def parse_color(token: str):
    token = token.strip()
    m = HEX_RE.search(token)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = RGB_RE.search(token)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None

def rel_luminance(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(rgb1, rgb2):
    l1, l2 = rel_luminance(rgb1), rel_luminance(rgb2)
    lo, hi = min(l1, l2), max(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

# ---------- 提取内联样式里的颜色对 ----------
INLINE_STYLE_RE = re.compile(r'style\s*=\s*["\']([^"\']*)["\']', re.I)

def inline_color_pairs(style: str):
    fg = bg = None
    cm = re.search(r'(?:^|;)\s*color\s*:\s*([^;]+)', style, re.I)
    if cm:
        fg = parse_color(cm.group(1))
    bm = re.search(r'(?:^|;)\s*background(?:-color)?\s*:\s*([^;]+)', style, re.I)
    if bm:
        bg = parse_color(bm.group(1))
    if fg and bg:
        return [(fg, bg)]
    return []

# ---------- 各格式读取 ----------
def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_pptx_text(path: str) -> str:
    """解包 pptx（zip）抽取所有 XML 文本，无需 markitdown。"""
    out = []
    try:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.endswith('.xml'):
                    try:
                        data = z.read(name).decode('utf-8', 'ignore')
                        out.append(data)
                    except Exception:
                        pass
    except Exception as e:
        return f'__PPTX_OPEN_ERROR__ {e}'
    return '\n'.join(out)

# ---------- 检查逻辑 ----------
def check_placeholder(text: str):
    hits = []
    for m in PLACEHOLDER_RE.finditer(text):
        s, e = m.start(), m.end()
        snippet = text[max(0, s - 15):e + 15].replace('\n', ' ')
        hits.append(snippet.strip())
    return hits

def check_contrast(html_text: str):
    issues = []
    for style in INLINE_STYLE_RE.findall(html_text):
        for fg, bg in inline_color_pairs(style):
            ratio = contrast(fg, bg)
            if ratio < 3.0:
                sev = 'P1-严重(<3:1)'
            elif ratio < 4.5:
                sev = 'P1-偏低(<4.5:1)'
            else:
                continue
            issues.append(f'{sev} 对比度={ratio:.2f} 前景{rgb_hex(fg)}/背景{rgb_hex(bg)}')
    return issues

def check_overflow(html_text: str):
    """启发式：固定高度(<80px)容器 + 内文过长(>60字) → 风险，需人工确认。"""
    risks = []
    # 匹配 <tag ... style="...height:<=80px...">长文本</tag>
    tag_re = re.compile(r'<(\w+)([^>]*style\s*=\s*["\'][^"\']*height\s*:\s*(\d+)px[^"\']*["\'][^>]*)>(.*?)</\1>', re.I | re.S)
    for m in tag_re.finditer(html_text):
        h = int(m.group(3))
        inner = re.sub(r'<[^>]+>', '', m.group(4)).strip()
        # 过滤掉纯空白/纯标签
        if h < 80 and len(inner) > 60:
            risks.append(f'P2-疑似溢出 高度={h}px 文本{len(inner)}字: {inner[:30]}...')
    return risks

def rgb_hex(rgb):
    return '#' + ''.join(f'{c:02X}' for c in rgb)

# ---------- 主流程 ----------
def scan_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pptx':
        text = read_pptx_text(path)
        html_text = ''
    else:
        text = read_text(path)
        html_text = text if ext in ('.html', '.htm') else ''

    result = {
        'file': path,
        'placeholder': check_placeholder(text),
        'contrast': check_contrast(html_text) if html_text else [],
        'overflow': check_overflow(html_text) if html_text else [],
    }
    return result

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    as_json = '--json' in args
    targets = [a for a in args if not a.startswith('--')]

    files = []
    for t in targets:
        if os.path.isdir(t):
            for ext in ('*.html', '*.htm', '*.md', '*.txt', '*.pptx'):
                files.extend(glob.glob(os.path.join(t, '**', ext), recursive=True))
        else:
            files.append(t)

    all_res = [scan_file(f) for f in files]
    if as_json:
        print(json.dumps(all_res, ensure_ascii=False, indent=2))
        return 0

    total_p0 = total_p1 = total_p2 = 0
    for r in all_res:
        p0, p1, p2 = r['placeholder'], r['contrast'], r['overflow']
        total_p0 += len(p0); total_p1 += len(p1); total_p2 += len(p2)
        print(f'\n=== {r["file"]} ===')
        if p0:
            print(f'  [P0 占位符残留] {len(p0)} 处:')
            for h in p0[:8]:
                print(f'    · {h}')
        else:
            print('  [P0 占位符残留] 无')
        if p1:
            print(f'  [P1 对比度失效] {len(p1)} 处:')
            for h in p1[:8]:
                print(f'    · {h}')
        else:
            print('  [P1 对比度失效] 无')
        if p2:
            print(f'  [P2 溢出风险] {len(p2)} 处(需人工确认):')
            for h in p2[:8]:
                print(f'    · {h}')
        else:
            print('  [P2 溢出风险] 无')

    print('\n------------------------')
    print(f'合计: P0={total_p0}  P1={total_p1}  P2={total_p2}')
    verdict = '通过(可交付)' if total_p0 == 0 and total_p1 == 0 else '需修复后交付'
    print(f'结论: {verdict}')
    return 0

if __name__ == '__main__':
    sys.exit(main())

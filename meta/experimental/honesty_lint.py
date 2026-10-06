#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[EXPERIMENTAL - 尚未转正，见 docs/experimental.md 转正判据]
已知边界（2026-10-06 实测）：判据面比预想窄——W1 对裸百分比数字不命中
（E3 为段级判据，须"据实测统计"类断言句式触发）；漏报可能，终判在人。

honesty_lint.py — 诚实与数字纪律静态机检 (deterministic, stdlib-only)

来源与射程（诚实边界，务必先读）：
  上游 BootLoops-ai/skills @ ca892277 的 `prose-lint`（42,763 B）自标：
    「A pass that runs every grep and skips this question is NOT a lint.」
  故本件**不自称 prose-lint**，只做其**可机械判定的那两个子集**：
    §E 诚实类 E3（出处失真）/ E5（自信的模糊）  → 规则 E3 / E5
    §N 数字纪律 N1–N13 中可算术/可坐标判定者     → 规则 N2 / W1 / W3
  ★ **不覆盖**上游 §A 词表 / §B 句式 / §C 节奏 / §D 格式 ——
    那部分中文侧已由既有 `prose_deslop_guard.py` 覆盖，**本件不重复造**。
  ★ **不覆盖**需语义理解的一切判据（上游 §A3.4 colleague test / §F 段 4 内部一致性）。
    本件是**模式匹配**，不是语义理解；漏报与误报都可能，**终判在人**。

我方纪律映射（每条规则的「立法依据」，皆为在册条款，非本件新造）：
  W1  无源不判    —— 判据须附「取数字段名 + 取样命令」；无源之判＝无效判
  W3  跨集不比    —— 凡率须指名分母集合；跨集合之差禁作趋势
  E3  引文失真    —— 事实断言须可回指坐标（承 `W-1` 家族）
  E5  自信的模糊  ——  contested/约略事实平直陈述即病灶
  N2  减法一致    —— 读者会相减的数字必须自洽

误杀防护（整行/整段豁免）：
  · 围栏代码块 ``` 内不扫
  · 含反引号内联坐标（路径 / 文件名 / 章节锚 / 行号锚）时，E3 与 W1 视为已给源
  · 含口径标签（活区/全档/唯一/去重/分母/集合…）时，W3 视为已指名分母集合

退出码：0 = 无 Tier1 命中；1 = 有 Tier1 命中（须处置或显式标注豁免）；2 = 用法/IO 错。
用法：
  python honesty_lint.py <file> [<file> ...] [--json] [--rule W1,E3] [--quiet]
  python honesty_lint.py --stdin
"""
import sys
import re
import json
import argparse

# ── 围栏代码块剥离（渲染面纪律：源码里的示例不该被当 prose 扫）──────────
_FENCE = re.compile(r"^\s*(```|~~~)")


def strip_fences(text):
    """返回 [(line_no, line_text)]；围栏内行**保留行号但内容置空**。

    ★★ 接口契约（接线实测所逼，2026-10-05）：**行号必须与原文一致**。
       首版用「删除围栏行」实现，导致其后所有行号前移 ⇒ brain_check 报出的
       行号指向错误原文（把 `〔fp:…〕` 指纹行报成违规）。
       其它维度（[11]/[11b]）皆用原文行号 ⇒ 本件必须同口径，否则门给的坐标不可回指。
    ★★ 占位用 **None** 而非 "" 标记（与真实空行区分）：若并作 ""，段聚合会
       把真实段落边界一并抹掉（实测：围栏两侧文本被并成一段，行号落到段首）。
    """
    out = []
    inside = False
    fence = None
    for i, ln in enumerate(text.splitlines(), 1):
        m = _FENCE.match(ln)
        if m:
            if not inside:
                inside, fence = True, m.group(1)
            elif m.group(1) == fence:
                inside, fence = False, None
            out.append((i, None))          # 围栏标记行：占位保号
            continue
        out.append((i, None if inside else ln))   # 围栏内：占位保号
    return out


def paragraphs(lines):
    """把 [(no, line)] 聚成空行分隔的段，返回 [(start_no, 段文本, 是否含表格行)]。

    ★ 表格行单独标出：markdown 表格里出现的率值/数字属**元描述**（如规则表里
      列举「召回率」是在说"本规则治什么"），不是作者的**事实断言**。
      接线实测假报根因即此 ⇒ W3/W1 判据面排除表格行。
    ★ 占位空行（围栏剥离所致，内容为 ""）**不切段** —— 否则围栏会把前后文本
      切成两段，破坏段级判据。
    """
    paras, buf, start, has_tbl = [], [], None, False
    for no, ln in lines:
        if ln is None:         # 围栏占位：不追加、不切段（但保行号）
            continue
        if ln.strip() == "":
            if buf:
                paras.append((start, "\n".join(buf), has_tbl))
                buf, start, has_tbl = [], None, False
        else:
            if start is None:
                start = no
            if ln.lstrip().startswith("|"):
                has_tbl = True
            buf.append(ln)
    if buf:
        paras.append((start, "\n".join(buf), has_tbl))
    return paras


# ── 证据/坐标/口径 的识别面（“已给源”即豁免）────────────────────────
# 取样命令或可回指文件名（写在反引号里）
SRC_RE = re.compile(
    r"`[^`]*(?:grep|wc\b|git\b|find\b|awk|sed\b|rg\b|python\b|sha256sum|md5sum|"
    r"rev-list|numstat|Get-ChildItem|Measure-Object|brain_check|"
    r"[\w./\\-]+\.(?:py|sh|ps1|json|txt|csv))[^`]*`"
)
# 裸坐标（不在反引号里也算）：文件路径 / commit hash / 行锚 / 章节锚 / 日期
COORD_RE = re.compile(
    r"(?:[A-Za-z]:\\[\w.\\\-]+|/[\w./\-]+|[\w\-]+\.(?:md|py|sh|json|txt)"
    r"|\b[0-9a-f]{7,40}\b|\bL\d{3,}\b|§\s*\d|\d{4}-\d{2}-\d{2})"
)
# 取数字段名
FIELD_RE = re.compile(r"(字段|取样命令|field\b|stat\b|列名|口径)")

# 口径标签：凡比较/率值须指名分母集合（W-3）
CALIBER_RE = re.compile(
    r"(口径|分母|全量|首投|重投|子样|子样窗|活区|全档|去重|唯一编号|最大号|"
    r"出现次数|行次|条目数|样本集|集合|同一分母)"
)

# 判据性数字：数量/比率/占比，带单位
# ★ 后顾排除时间量词（接线实测假报）：「3 个月」「3 天」里的「个/天」不构成
#   计数单位 ⇒ 单位后若紧跟时间量词字则该匹配不成立。
#   ★ 取证记录：负向断言放在**数字前**是错的（时间量词在数字**后**），
#     曾致「3 个月」被读成「3 个」（KB index.md L294 假报）。
_NUM = r"(\d[\d,]*(?:\.\d+)?)"
_UNIT = r"(%|条|件|次|个|项|张|页|行|万|亿|倍|轮)"
_TIME_AFTER = r"(?![年月日周秒])"          # 单位后不得紧跟时间量词
NUM_UNIT_RE = re.compile(
    r"(?<![\w.])" + _NUM + r"\s*" + _UNIT + _TIME_AFTER
)
# 裸百分比（无单位后缀形式）
PCT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*%")

# 跨集合比较词（“多/少/高/低/增/降/超/倍”类，作用于集合间）
# ★ 收窄：去掉裸 `提升/降低`（中文里也指「能力提升」等非比较义），
#   保留**必须带数量语境**的强比较词。
XSET_RE = re.compile(
    r"(更多|更少|多出|多于|少于|超过|超出|增加|下降|上升|相差|差距|"
    r"多\s*\d|少\s*\d|高出|高出)"
)
# 率/占比（须分母）——★ 收窄（两轮实测逼出来的）：
#   ① `比例` 裸用常指「按比例分配」而非率值 ⇒ 移除；
#   ② `召回率/命中率/成功率/…` 作为**普通名词**极常见（"可用性与召回率同等重要"
#      讲的是检出能力，不是率值）⇒ 复合词须**紧邻数字**才成立（率值必有量）。
_RATE_WORD = r"(?:占比|比率|成功率|命中率|通过率|准确率|召回率|漏检率|误报率)"
RATE_RE = re.compile(
    _RATE_WORD + r"\s*(?:为|是|达|＝|=)?\s*[\d(（]"   # 复合词紧邻数字
    r"|占\s*[\d(（]"
    r"|率\s*[是为约]\s*[\d(（]"
)

# 跨代/跨集借用的高危表述（我方 W-2/W-3 的字面锚）
BORROW_RE = re.compile(r"(旧尺|上一代|之前(?:的)?口径|历史数据(?:的)?口径)")

# 引证式事实断言：据/按 + 实测/统计/显示/证明
CITE_RE = re.compile(
    r"(?:据|按|依|根据|见|详见|引|参见)[^。；\n]{0,8}"
    r"(?:实测|统计|报告|记录|显示|证明|表明)|"
    r"实测(?:表明|显示|证明)|(?:统计|计数)(?:表明|显示)"
)
# 无源断言动词（未带引证词也可能宣称事实）
BARE_FACT_RE = re.compile(r"(?:已(?:全部|全部)?完成|全部(?:通过|完成|就绪)|(?:零|无)(?:必须处置|违规|残留))")

# 绝对化断言（E5）——★ 词表刻意收紧：`所有/全部/首次/第一个/100%` 在纪律语料里
#   是正常表述（我方在册纪律大量使用），纳入即噪声源 ⇒ 只收**不可对冲的强断言**。
# ★★ 二次收紧（真实脑内件反向对照实测）：`必然/从未/永远` 在我方语料里
#   **绝大多数出现在引号内**（作为被讨论的词被引用），不是作者断言
#   ⇒ 判定前先剥除引号/反引号内容（见 strip_quoted）。
ABS_RE = re.compile(
    r"(必然|一定会|无一例外|从未|永远|史上首次|全球首次|完全杜绝|彻底解决|"
    r"彻底杜绝|永久失效|绝无可能|完全一致|丝毫不差)"
)

# ── 引号/反引号内容剥离（E5/W1 的证据面）───────────────────────────
# ★ 判据面收窄的关键：作者**引用**一个词 ≠ 作者**断言**它。
#   故 E5 判定前剥除 `"..."` `“...”` `「...」` `『...』` `''...''` `...` 内内容。
QUOTED_RE = re.compile(r"``[^`]*``|`[^`]*`|\"[^\"\n]*\"|“[^”\n]*”|「[^」\n]*」|『[^』\n]*』|''[^'\n]*''")


def strip_quoted(s):
    """把引号/反引号包裹的内容替换为等长空格（保列位）。"""
    return QUOTED_RE.sub(lambda m: " " * len(m.group(0)), s)
# 对冲词（与绝对化同行即视为已对冲）
HEDGE_RE = re.compile(
    r"(可能|也许|或许|据称|推测|初步|尚未|待验证|未验证|待核|倾向于|看似|或可|"
    r"约|近似|区间|范围内|倾向于认为|存疑|未排除|不排除)"
)

# 减法一致：形如「A − B = C」「A 减 B 得 C」「A-B，相差 C」
# ★ 第三组「结果数」**必须存在**（承首跑取证：`569 减 520` 若允许 C 缺省，
#   `c` 会取到 0 而恒假报 —— 判据不可与「无结果数」同形）。
# ★ 减号族须齐全：`-`(ASCII) `−`(U+2212 减号) `–`(U+2013) `—`(U+2014)。
#   接线实测漏报根因：日志里写「`2026 − 10 = 05`」用的是 U+2212，
#   而日期剔除正则只认 ASCII `-` ⇒ 剔除失效、假报复现。
SUB_RE = re.compile(
    r"(?<![\w.\-/])(\d[\d,]*(?:\.\d+)?)\s*(?:-|−|–|—|减|减去)\s*(\d[\d,]*(?:\.\d+)?)"
    r"\s*(?:=)?\s*(?:得|为|＝|=)\s*(\d[\d,]*(?:\.\d+)?)"
)
SUB2_RE = re.compile(
    r"(?<![\w.\-/])(\d[\d,]*(?:\.\d+)?)\s*(?:-|−|–|—)\s*(\d[\d,]*(?:\.\d+)?)"
    r"\s*[,，]?\s*(?:相差|差|多|少)\s*(\d[\d,]*(?:\.\d+)?)"
)
# 形如 2026-10-05 / 2026-10 / 2026−10−05 的日期段先行剔除（N2 判据面收窄）
# ★ 连字符族须与 SUB 同族，否则「日期被读成减法」会在 Unicode 连字符下复现。
DATE_SPAN_RE = re.compile(
    r"(?<![\w.])(\d{4})\s*(?:-|−|–|—)\s*(\d{2})(?:\s*(?:-|−|–|—)\s*(\d{2}))?(?![\w.])"
)


def _f(x):
    return float(x.replace(",", ""))


RULES = {
    "W1": "无源之判：出现判据性数字但同行无取样命令/字段名/坐标",
    "W3": "跨集不比：出现集合间比较或率值但未指名分母集合（口径）",
    "E3": "引文失真：出现「据…实测/统计/显示」类事实断言但无可回指坐标",
    "E5": "自信的模糊：绝对化断言且同行无对冲词",
    "N2": "减法不一致：同句给出的减法关系与算术真值不符",
}

# 每条规则的严重度：1 = 必须处置；2 = 提示
SEV = {"W1": 1, "W3": 1, "E3": 1, "E5": 2, "N2": 1}

CURE = {
    "W1": "补「取数字段名 + 取样命令」（反引号内写命令），或删该数字",
    "W3": "指名分母集合（活区/全档/去重/子样窗…），或改述为不跨集的比较",
    "E3": "补可回指坐标（文件路径 / commit hash / L#### / § / 日期）",
    "E5": "加精确对冲（初步/尚未/约/待验证），或降为可核范围表述",
    "N2": "核对三个数字；读者会相减，故须自洽（承 N2 减法一致）",
}


def _has_source(s):
    return bool(SRC_RE.search(s) or FIELD_RE.search(s) or COORD_RE.search(s))


def _has_enum_support(paras, i):
    """本段是否落在某个表格段的**连续正文区段**内（即被该枚举支撑）。

    ★ 根因修法（2026-10-05 接线批次**三次**假报后改弦）：
      前两版按「紧邻 ±1 段」打补丁，仍漏 —— 作者引用表格的写法远比邻接复杂：
      「结论段 + 表」「段标题 + 表」「表 + 结论段」「正文串 → …→ 表」皆可。
      局部打补丁 = 判据面**永远追不上**证据面（W1 由行→段那次已犯同族错）。
    ★ 现行口径：**表格段前后的连续非表格段组成的整个区段，一律视作被该表支撑**
      —— 理由：表格是一份**完整枚举**，其描述范围由表自身界定，读者由表即得
      取数依据；这些正文段里的数字正是对该枚举的引用。
    ★ 边界（防放宽过头 ⇒ 漏报）：**遇到下一个表格段即截断**，不跨越；
      且**必须真有表格邻接**（无表 ⇒ 不构成支撑）。
    ★ 诚实边界：这仍非语义理解 ⇒ 隔很远的表格会被误当支撑（本批已实证）。
      W1 的立意是「逼作者给取数依据」；若正文确实引的是另一处的数，
      作者应把该数就近标注来源（如本节两处修法所示）。
    """
    if i < 0 or i >= len(paras):
        return False
    if paras[i][2]:                      # 本段即表格
        return True
    # 向两侧扩张，直到撞到另一个表格段或文档两端
    for j in range(i - 1, -1, -1):
        if paras[j][2]:
            return True
    for j in range(i + 1, len(paras)):
        if paras[j][2]:
            return True
    return False


def scan_text(text, only=None):
    """返回 findings = [ {rule, line, sev, matched, cure} ]"""
    lines = strip_fences(text)
    paras = paragraphs(lines)
    findings = []

    def add(rule, line, matched):
        if only and rule not in only:
            return
        findings.append({
            "rule": rule, "line": line, "sev": SEV[rule],
            "matched": matched[:60], "cure": CURE[rule],
        })

    for no, ln in lines:
        if ln is None:            # 围栏占位行：跳过内容判定（行号已保）
            continue
        # ── E5 自信的模糊：剥引号后判（引用 ≠ 断言）──
        bare = strip_quoted(ln)
        for m in ABS_RE.finditer(bare):
            if not HEDGE_RE.search(bare):
                add("E5", no, m.group(0))

        # ── N2 减法一致 ──
        # 日期段先行剔除（`2026-10-05` 不是减法式）
        nline = DATE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), ln)
        for rx in (SUB_RE, SUB2_RE):
            for m in rx.finditer(nline):
                a, b, c = _f(m.group(1)), _f(m.group(2)), _f(m.group(3))
                if abs((a - b) - c) > 1e-9:
                    add("N2", no, m.group(0))

    for pi, (start, para, has_tbl) in enumerate(paras):
        # ── W1 无源之判：**段级**判据（承真实件反向对照：坐标常在上一行，
        #   行级判据面比证据面窄 ⇒ 噪声爆炸。整段无源才报。）
        #   ★ 表格行排除（接线实测假报：表内「默认 15%」是**描述脚本默认值**
        #     的元描述，不是作者的事实断言）。
        #   ★ 前邻枚举支撑（接线批次实测假报）：「结论段 + 紧随其后的表」是
        #     惯用序 ⇒ 判据面须含前一段表格，否则「5 个假报」类句恒假报。
        if not only or "W1" in only:
            if not has_tbl and not _has_source(para) and not _has_enum_support(paras, pi):
                m = NUM_UNIT_RE.search(para) or PCT_RE.search(para)
                if m and not re.search(r"(?:19|20)\d{2}-\d{2}-\d{2}", m.group(0)):
                    add("W1", start, m.group(0))

        # ── W3 跨集不比：段级判据（比较词与被比较数常跨行）；表格行属元描述，排除
        if not only or "W3" in only:
            if not has_tbl and not CALIBER_RE.search(para):
                m = XSET_RE.search(para)
                if m and re.search(r"\d", para):
                    add("W3", start, m.group(0))
                else:
                    m2 = RATE_RE.search(para)
                    if m2 and re.search(r"\d", para):
                        add("W3", start, m2.group(0))

        # ── E3 引文失真：段级判据（引证词与坐标常跨行）；表格行排除
        if not only or "E3" in only:
            if not has_tbl and (CITE_RE.search(para) or BARE_FACT_RE.search(para)):
                if not _has_source(para):
                    m = CITE_RE.search(para) or BARE_FACT_RE.search(para)
                    add("E3", start, m.group(0))

    findings.sort(key=lambda f: (f["line"], f["rule"]))
    return findings


def _report(paths, findings, as_json, quiet):
    if as_json:
        print(json.dumps(
            {"scanned": paths, "count": len(findings), "findings": findings},
            ensure_ascii=False, indent=2))
        return
    t1 = [f for f in findings if f["sev"] == 1]
    if not quiet:
        print("===== 诚实与数字纪律机检 (honesty_lint) =====")
        print("扫描面: %s" % (", ".join(paths) if paths else "<stdin>"))
        print("规则 5 条（W1/W3/E3/E5/N2）· 本件只做可机械判定者，"
              "不含语义判据；终判在人。")
    if not findings:
        print("命中 0 条。")
        return
    by = {}
    for f in findings:
        by.setdefault(f["rule"], 0)
        by[f["rule"]] += 1
    print("命中 %d 条（Tier1 %d / Tier2 %d）: %s"
          % (len(findings), len(t1), len(findings) - len(t1),
             " ".join("%s=%d" % (k, by[k]) for k in sorted(by))))
    for f in findings:
        print("  L%-5d [%s:%d] %-14s 命中「%s」 → %s"
              % (f["line"], f["rule"], f["sev"], RULES[f["rule"]][:14],
                 f["matched"], f["cure"]))


def main():
    ap = argparse.ArgumentParser(description="诚实与数字纪律静态机检 (deterministic)")
    ap.add_argument("files", nargs="*", help="要扫描的文本文件")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--rule", help="只跑指定规则，逗号分隔（如 W1,E3）")
    ap.add_argument("--quiet", "-q", action="store_true", help="只出计数")
    args = ap.parse_args()

    if not args.files and not args.stdin:
        ap.error("须给文件或 --stdin")

    only = None
    if args.rule:
        only = {r.strip().upper() for r in args.rule.split(",") if r.strip()}
        bad = only - set(RULES)
        if bad:
            print("未知规则: %s（可用: %s）" % (",".join(sorted(bad)),
                                              ",".join(sorted(RULES))),
                  file=sys.stderr)
            return 2

    findings = []
    try:
        if args.stdin:
            findings += scan_text(sys.stdin.read(), only)
        else:
            for p in args.files:
                with open(p, "rb") as fh:
                    findings += scan_text(fh.read().decode("utf-8", "replace"), only)
    except OSError as e:
        print("IO 错: %s" % e, file=sys.stderr)
        return 2

    _report(args.files, findings, args.json, args.quiet)
    return 1 if any(f["sev"] == 1 for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())

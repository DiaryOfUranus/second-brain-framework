# -*- coding: utf-8 -*-
"""ledger_writer.py —— 衡枢侧固退写器公共件本体（写器P-1/P-2 机械落形）

《固退写器公共件纪律》生效件（2026-10-11·作者拍板）之衡枢本体。
各席写器本体到位后改传参调用本件，不另造第二套（写器P-3·一面一秤）。

用法（嵌入固退写器脚本）：
    from ledger_writer import append_ledger_entry, proof, find_anchor, next_number
    st = append_ledger_entry(LEDGER_PATH, BLOCK, fp=FP)   # 'OK' | 'SKIP'
    proof(LEDGER_PATH, before_active, expect_delta=1)
    n = next_number(LEDGER_PATH)                          # 号位现读（附三③）
    # 无「## 归档」物理节的册（活跃直排 EOF 形制）：anchor_line=None ⇒ EOF 追加
    st = append_ledger_entry(LEDGER_PATH, BLOCK, fp=FP, anchor_line=None)
    # v1.4：非台账条形追加（共享登记簿行等）——append_plain
    st = append_plain(REGISTRY_PATH, "- 2026-10-14｜席作：……", fp="fp:xxx")

行为标签（v1.4·承问枢 10-13 basic-memory 扫描建议·机器可读）：
    _BEHAVIOR = {
      "append_ledger_entry": "append-only · idempotent(fp) · constructive(tmp+os.replace)",
      "append_plain":        "append-only · idempotent(fp/逐行去重) · constructive(tmp+os.replace)",
      "next_number":         "read-only",
      "find_anchor":         "pure",
      "active_count":        "pure",
      "entry_id_exists":     "pure",
      "proof":               "read-only · assertive",
    }

v1.1（2026-10-12·附三项差异备忘链认通过·本体侧升级）：
  ① 附三①：写后校验失败自动回滚——写盘后计数增量/行尾断言失败时，
     恢复原文本后再抛异常（写后校验失败不留半态）。
  ② 附三②：内容派生指纹幂等键——fp=None 时自动派生
     fp = "fp:autoderive-" + sha256(block)[:16]，与写入文本构造性绑定。
     （显式 fp 仍须在 block 内恰 1 次；派生 fp 不要求在块内。）
  ③ 附三③：next_number() 号位现读——写前实测全档最大条目号 +1，
     禁按印象/邻近段落推断（乐观并发协议第①步）。

v1.2（2026-10-13·问枢窗内异议三缺核备为真〔鉴枢受理〕·本体侧升级）：
  ④ EOF 模式：anchor_line=None ⇒ 条目追加至文件尾（活跃直排 EOF 形制之册可直调）；
     锚写了但文件无此锚 ⇒ 仍 AssertionError（fail-closed，禁静默降级）。
  ⑤ anchor_line 契约收紧：None ⇒ EOF 追加；非 str（int 等）⇒ AssertionError
     （禁 AttributeError 逃出 fail-closed 契约——调用方按 AssertionError 兜异常不漏接）。
  ⑥ BOM 保型：_read 以 utf-8-sig 剥 BOM ⇒ 号位面（next_number／entry_id_exists／
     active_count）覆盖 BOM 件首行条目（撞号断言不再漏首行）；写回时按原文件
     BOM 在位与否保型回写（utf-8-sig），不静默吞 BOM。

v1.3（2026-10-14·问枢「第四缺」核备为真〔鉴枢 10-13 §四〕·本体侧升级）：
  ⑦ 主体行尾按多数判：CRLF 数 > 裸 LF 数才算 CRLF 件（禁「任一 CRLF 即判型」）；
     混行尾共享件按主体走，少数派行尾原样保留。
  ⑧ 只对本次新增行套主体行尾：禁全文 replace（splitlines 保端点直拼，
     既存字节零改动——v1.2 对混行尾件整件静默转 CRLF 之根因拔除）。
  ⑨ 行尾门改 delta：写前/写后记 (CRLF, 裸LF, 孤立CR, CRCRLF) 四值，
     断言「本次引入的异种行尾＝0」——既存少数派行尾不得算本次责任，
     也不得被本次抹平（恒绿门族之 delta 正法·问枢 §一.3 修法三步）。
  负控 +⑮⑯⑰（混行尾 LF 主体保型／CRLF 主体保型／delta 门 fail-closed）。

v1.4（2026-10-14·问枢 P-3 换秤当场逮出「plain_append 能力面缺失」〔鉴枢 §四 采〕·本体侧升级）：
  ⑩ 新增 append_plain(path, line, fp=None)：非台账条形之追加（共享登记簿行
     「- 日期｜席作…」／表行等）。台账形断言（「- [」起行／触发栏／号位）不适用——
     「只增载体的追加」与「台账条目追加」分设两门（选 append_plain 方案，
     不给 append_ledger_entry 加 require_entry_shape 旁路——一门一形，防双旗混用）。
     行尾与落盘全复用公共件自有量具（_majority_eol／_eol_delta_gate／_write：
     tmp＋os.replace∥BOM 保型∥只对新增行套 EOL），并加一条比行尾规则更硬的
     不变式：写前字节必须是写后字节的严格前缀（原件区零改动）。
     幂等：fp 已在 ⇒ SKIP；fp=None ⇒ 逐行去重 guard（同文行已在 ⇒ SKIP）。
  ⑪ 行为标签 _BEHAVIOR 落模块（read-only／append-only／destructive 声明面）。
  负控 +⑱⑲⑳（plain 追加混行尾保型＋前缀不变式／逐行去重 SKIP／BOM 件 plain 保型）。
  注：问枢适配器例外面 append_plain 在本版本落册后，其「上游补齐后本函数即删除」
  承诺可兑现（其漂移门第⑤能力项探针应由 WARN 转 PASS）。

纪律来源：patterns/reusable-patterns.md「固退写器公共件纪律（写器P-1～P-4）」。
自检：python ledger_writer.py --selftest
"""
import hashlib
import os
import re
import sys
import tempfile

ENTRY_RE = re.compile(r"^- \[\d{4}-\d\d-\d\d\] #(\d+)", re.M)
EXCLUDE_MARKS = ("[已核销", "[已归档")
_BOM = "﻿"

_BEHAVIOR = {
    "append_ledger_entry": "append-only · idempotent(fp) · constructive(tmp+os.replace)",
    "append_plain": "append-only · idempotent(fp/逐行去重) · constructive(tmp+os.replace)",
    "next_number": "read-only",
    "find_anchor": "pure",
    "active_count": "pure",
    "entry_id_exists": "pure",
    "proof": "read-only · assertive",
}


def _read(path):
    """读文件并剥 UTF-8 BOM（v1.2⑥：号位面覆盖 BOM 件首行条目）。"""
    return open(path, "rb").read().decode("utf-8-sig")


def _read_with_bom(path):
    """读文件并返回 (text, had_bom)——写回保型用。"""
    raw = open(path, "rb").read()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def _write(path, text, bom=False):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(text.encode("utf-8-sig" if bom else "utf-8"))
    os.replace(tmp, path)


def _eol_stats(text):
    """行尾四值统计（v1.3⑨ delta 门量具）。

    crlf=CRLF 对数；bare_lf=不配对的裸 LF；lone_cr=未跟 LF 的孤立 CR
    （含 CRCRLF 之首 CR）；crcrc=CRCRLF 双重转换数。
    """
    crlf = text.count("\r\n")
    lf_total = text.count("\n")
    cr_total = text.count("\r")
    return {
        "crlf": crlf,
        "bare_lf": lf_total - crlf,
        "lone_cr": cr_total - crlf,
        "crcrc": text.count("\r\r\n"),
    }


def _majority_eol(text):
    """v1.3⑦ 主体行尾按多数判：CRLF > 裸 LF ⇒ CRLF 件；否则 LF 件。"""
    s = _eol_stats(text)
    return "\r\n" if s["crlf"] > s["bare_lf"] else "\n"


def _check_lineend(text):
    """行尾健全性（v1.3 口径）。

    均质 CRLF 件：CR==LF==CRLF 且无 CRCRLF；均质 LF 件：CR==0；
    混行尾件（v1.3 起合法既存态·共享件不背锅）：只查无 CRCRLF/孤立 CR。
    """
    s = _eol_stats(text)
    if s["crlf"] > 0 and s["bare_lf"] > 0:
        assert s["crcrc"] == 0 and s["lone_cr"] == 0, (
            f"混行尾件含 CRCRLF={s['crcrc']} 或孤立 CR={s['lone_cr']}"
        )
    elif s["crlf"] > 0:
        assert s["crcrc"] == 0, f"CRCRLF={s['crcrc']}（双重转换坑）"
        assert text.count("\r") == text.count("\n") == s["crlf"], "CRLF 件混行尾"
    else:
        assert s["lone_cr"] == 0, f"LF 件含孤立 CR: {s['lone_cr']}"


def _eol_delta_gate(before_stats, after_stats, eol):
    """v1.3⑨ delta 门：本次引入的异种行尾必＝0（fail-closed）。

    主体 EOL 恰 +1（新增 1 行）；少数派四值零增量（既存字节不被抹平）。
    ★ 门不信 eol 参数——从写前统计重算主体比对（防「门随被检对象自调」
    恒绿门族：判型被劫持时门仍能拦，负控 ⑰ 即此形态）。
    """
    real_majority = "\r\n" if before_stats["crlf"] > before_stats["bare_lf"] else "\n"
    assert eol == real_majority, (
        f"判型不符：传入 eol={eol!r} ≠ 写前重算主体 {real_majority!r}"
    )
    if eol == "\r\n":
        assert after_stats["crlf"] - before_stats["crlf"] == 1, (
            f"CRLF 增量 {after_stats['crlf'] - before_stats['crlf']} ≠ 1"
        )
        assert after_stats["bare_lf"] == before_stats["bare_lf"], (
            f"混行尾伤害：既存裸 LF {before_stats['bare_lf']}→{after_stats['bare_lf']} 被抹平"
        )
    else:
        assert after_stats["bare_lf"] - before_stats["bare_lf"] == 1, (
            f"裸 LF 增量 {after_stats['bare_lf'] - before_stats['bare_lf']} ≠ 1"
        )
        assert after_stats["crlf"] == before_stats["crlf"], (
            f"混行尾伤害：既存 CRLF {before_stats['crlf']}→{after_stats['crlf']} 被抹平"
        )
    assert after_stats["crcrc"] == before_stats["crcrc"], "本次引入 CRCRLF"
    assert after_stats["lone_cr"] == before_stats["lone_cr"], "本次引入孤立 CR"


def _split_keepends(text):
    """按 \\n 拆行并保端点（splitlines 会吃 \\v/\\f 等，禁用）。

    CRLF 行的 \\r 留在行内容尾，"".join 还原即逐字节等价。
    """
    parts = text.split("\n")
    lines = [p + "\n" for p in parts[:-1]]
    if parts[-1] != "":
        lines.append(parts[-1])
    return lines


def find_anchor(lines, target):
    """写器P-1：整行 strip() 相等锚，断言恰 1 处，返回行号。禁裸 find／子串 count。

    兼容保端点行（strip() 会剥行尾 \\r\\n）与裸内容行两种形态。
    """
    assert isinstance(target, str), "锚须为 str（None 请走 anchor_line=None EOF 模式）"
    hits = [i for i, l in enumerate(lines) if l.strip() == target.strip()]
    assert len(hits) == 1, f"锚「{target.strip()[:40]}」命中 {len(hits)} 处（须恰 1）"
    return hits[0]


def active_count(text, anchor_line="## 归档"):
    """活跃区条目数（brain_check [2] 同族口径：行首条目正则 ∧ 排除已核销/已归档行）。

    锚按整行相等定位；文件无锚时视全档为活跃区。
    """
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.strip() == anchor_line.strip()]
    region = lines[: hits[0]] if hits else lines
    n = 0
    for l in region:
        if ENTRY_RE.match(l) and not any(m in l for m in EXCLUDE_MARKS):
            n += 1
    return n


def entry_id_exists(text, entry_id):
    """写器P-1 附则（鉴枢收紧）：ID 唯一性断言面覆盖全档（活跃＋归档区）。"""
    pat = re.compile(r"^- \[\d{4}-\d\d-\d\d\] #%s(?!\d)" % re.escape(str(entry_id)), re.M)
    if pat.search(text):
        return True
    # 归档区 ### 标题式历史形态同查
    return re.search(r"^#{1,3}\s*#%s\b" % re.escape(str(entry_id)), text, re.M) is not None


def next_number(path):
    """附三③ 号位现读：全档最大条目号 +1（乐观并发协议①·写前实测）。

    空档/无条目 ⇒ 返回 1。调用方：写入前现读，缩短测量-写入窗口；
    撞号由 append_ledger_entry 全档唯一性断言兜底（fail-closed）。
    """
    ids = [int(m.group(1)) for m in ENTRY_RE.finditer(_read(path))]
    return (max(ids) + 1) if ids else 1


def append_ledger_entry(path, block, fp=None, anchor_line="## 归档"):
    """向台账件锚前插入一条目（幂等：fp 已在 ⇒ SKIP）。

    anchor_line=None ⇒ v1.2④ EOF 追加模式（活跃直排 EOF 形制之册）；
    anchor_line 为其他非 str 值 ⇒ AssertionError（v1.2⑤ 契约收紧）。

    fp=None ⇒ 附三② 内容派生指纹幂等键（sha256(block) 前 16 hex）。
    block 硬断言（fail-closed，写盘前零副作用）：
      ① 以「- [」起行；② 含「触发:」或「触发：」栏；
      ③ 显式 fp 在块内恰 1 次（派生 fp 豁免——键与内容构造性绑定）；
      ④ 条目 ID 全档唯一（新条号不得与既有任何条目撞；BOM 件首行条目同在断言面）。
    附三① 写后校验（计数增量＋行尾 delta）失败 ⇒ 自动回滚原文本后再抛异常。
    v1.2⑥ BOM 保型：原文件带 BOM ⇒ 写回仍带 BOM。
    v1.3⑦⑧⑨：主体行尾多数判／只对新增行套 EOL／行尾门 delta（既存行尾零改动）。
    返回 'OK' 或 'SKIP'。
    """
    if anchor_line is not None:
        assert isinstance(anchor_line, str), (
            "anchor_line 须为 str 或 None（EOF 模式）；收到 %r" % type(anchor_line).__name__
        )
    text, had_bom = _read_with_bom(path)
    if fp is None:
        # 附三② 内容派生指纹：键由 block 派生 ＋ 拼入 block 尾落盘
        # （键与写入文本构造性一致且为落盘文本子串 ⇒ 幂等 guard 可查）
        fp = "fp:autoderive-" + hashlib.sha256(block.encode("utf-8")).hexdigest()[:16]
        block = block.rstrip("\n") + "〔" + fp + "〕"
    if fp and fp in text:
        return "SKIP"  # 幂等 guard：fp 即内容指纹
    # —— 写前断言（fail-closed，零副作用）——
    assert block.lstrip().startswith("- ["), "条目须以「- [」起行"
    assert ("触发:" in block) or ("触发：" in block), "缺触发栏"
    if not fp.startswith("fp:autoderive-"):
        assert fp and block.count(fp) == 1, "fp 须在块内恰 1 次（幂等键唯一）"
    m = ENTRY_RE.match(block)
    assert m, "条目行须含「- [日期] #N」号位"
    entry_id = m.group(1)
    assert not entry_id_exists(text, entry_id), f"条目号 #{entry_id} 全档撞号·停机"
    # —— v1.3：主体行尾多数判 ＋ 只对新增行套 EOL（既存字节零改动）——
    eol = _majority_eol(text)
    before_stats = _eol_stats(text)
    new_line = block.rstrip("\r\n") + eol
    if anchor_line is None:
        # v1.2④ EOF 追加模式
        out = text
        if out and not out.endswith("\n"):
            out += eol
        out = out + new_line
    else:
        lines = _split_keepends(text)
        idx = find_anchor(lines, anchor_line)
        lines.insert(idx, new_line)
        out = "".join(lines)
    _eol_delta_gate(before_stats, _eol_stats(out), eol)  # v1.3⑨ 写前 delta 门
    before = active_count(text, anchor_line or "## 归档不可达哨兵-EOF模式全档活跃")
    _write(path, out, bom=had_bom)
    # —— 写器P-2：写后自证 ＋ 附三① 失败自动回滚 ——
    try:
        after_text = _read(path)
        after = active_count(after_text, anchor_line or "## 归档不可达哨兵-EOF模式全档活跃")
        assert after - before == 1, f"活跃计数增量 {after - before} ≠ 1（写入成功≠门禁可见）"
        _eol_delta_gate(before_stats, _eol_stats(after_text), eol)  # v1.3⑨ 写后 delta 门
    except AssertionError:
        _write(path, text, bom=had_bom)  # 附三①：回滚到写入前原文本（字节级），再抛
        raise
    return "OK"


def append_plain(path, line, fp=None):
    """v1.4⑩：非台账条形之追加（共享登记簿行「- 日期｜席作…」／表行等）。

    与 append_ledger_entry 分设两门（一门一形）：台账形断言（「- [」起行／
    触发栏／号位／撞号）此处**不适用**；行尾与落盘全复用公共件自有量具——
    _majority_eol 判型／只对新增行套 EOL／_eol_delta_gate delta 门／
    _write（tmp＋os.replace∥BOM 保型）。

    额外硬不变式（比行尾规则更硬）：**写前字节必须是写后字节的严格前缀**
    （原件区零改动·问枢适配器同款不变式）。

    幂等（双 guard）：
      ① fp 给出且已在文件 ⇒ SKIP；
      ② fp=None ⇒ 逐行去重 guard（strip() 后同文行已在 ⇒ SKIP）。
    line 须为非空 str（去掉行尾换行后仍有内容），否则 AssertionError（fail-closed）。
    返回 'OK' 或 'SKIP'。
    """
    assert isinstance(line, str), "line 须为 str；收到 %r" % type(line).__name__
    core = line.rstrip("\r\n").strip()
    assert core, "plain 行去行尾后为空（拒写空行）"
    text, had_bom = _read_with_bom(path)
    # 幂等 guard ①：显式 fp
    if fp is not None:
        assert isinstance(fp, str) and fp, "fp 须为非空 str 或 None"
        if fp in text:
            return "SKIP"
    # 幂等 guard ②：逐行去重（strip 后同文行已在）
    if any(l.strip() == core for l in text.splitlines()):
        return "SKIP"
    eol = _majority_eol(text)
    before_stats = _eol_stats(text)
    new_line = line.rstrip("\r\n") + eol
    out = text
    if out and not out.endswith("\n"):
        out += eol
    out = out + new_line
    # 硬不变式：写前字节是写后字节的严格前缀（原件区零改动）
    assert out.startswith(text), "plain 追加前缀不变式破口：原件区被改动"
    _eol_delta_gate(before_stats, _eol_stats(out), eol)
    _write(path, out, bom=had_bom)
    # 写后自证 ＋ 失败自动回滚（附三① 同款）
    try:
        after_text = _read(path)
        assert after_text.startswith(text), "写后前缀不变式破口"
        _eol_delta_gate(before_stats, _eol_stats(after_text), eol)
    except AssertionError:
        _write(path, text, bom=had_bom)
        raise
    return "OK"


def proof(path, before_active, expect_delta=1, anchor_line="## 归档"):
    """写器P-2 独立自证入口：计数增量＋行尾保型。返回 (delta, ok)。"""
    text = _read(path)
    delta = active_count(text, anchor_line) - before_active
    assert delta == expect_delta, f"计数增量 {delta} ≠ 预期 {expect_delta}"
    _check_lineend(text)
    return delta, True


def _selftest():
    """负控夹具 20 条：全过打 PASS 并 rc=0（v1.4 +⑱⑲⑳ plain 追加族）。"""
    n_pass = 0
    # ① 锚不唯一 → 拒绝
    try:
        find_anchor(["## 归档", "x", "## 归档"], "## 归档")
        raise SystemExit("① fail")
    except AssertionError:
        n_pass += 1
    # ② 裸子串负控：正文行含「## 归档」子串 → find_anchor 不命中（整行相等防线）
    lines = ["- [2026-10-11] #1 正文提到 ## 归档 字样", "tail"]
    try:
        find_anchor(lines, "## 归档")
        raise SystemExit("② fail")
    except AssertionError:
        n_pass += 1
    # ③ CRLF 件插入：增量 1＋行尾保型＋无 CRCRLF
    d = tempfile.mkdtemp()
    p = os.path.join(d, "ledger_crlf.md")
    open(p, "wb").write(("- [2026-10-10] #900 旧条 ｜ 方向: x ｜ 触发: y\r\n## 归档\r\n- [2026-09-01] #800 旧档\r\n").encode("utf-8"))
    before = active_count(_read(p))
    b1 = "- [2026-10-11] #901 新条 ｜ 方向: a ｜ 触发: b 〔fp:t-selftest-1〕"
    st = append_ledger_entry(p, b1, "fp:t-selftest-1")
    assert st == "OK"
    proof(p, before, 1)
    t = _read(p)
    assert t.count("\r\n") == t.count("\n") == t.count("\r") and t.count("\r\r\n") == 0
    assert "## 归档" in t and t.index("#901") < t.index("## 归档")
    n_pass += 1
    # ④ 幂等：fp 已在 ⇒ SKIP（不重复插入）
    st2 = append_ledger_entry(p, b1, "fp:t-selftest-1")
    assert st2 == "SKIP" and len(re.findall(r"#901(?!\d)", t)) == 1
    n_pass += 1
    # ⑤ 缺触发栏 → 拒绝
    p5 = os.path.join(d, "l5.md")
    open(p5, "wb").write("- [2026-10-10] #900 x\r\n## 归档\r\n".encode("utf-8"))
    try:
        append_ledger_entry(p5, "- [2026-10-11] #901 无触发栏 〔fp:t-5〕", "fp:t-5")
        raise SystemExit("⑤ fail")
    except AssertionError:
        n_pass += 1
    # ⑥ 撞号 → 拒绝（全档含归档区）
    try:
        append_ledger_entry(p5, "- [2026-10-11] #900 撞号 ｜ 触发: y 〔fp:t-6〕", "fp:t-6")
        raise SystemExit("⑥ fail")
    except AssertionError:
        n_pass += 1
    # ⑦ LF 件插入：CR==0 保持
    p7 = os.path.join(d, "l7.md")
    open(p7, "wb").write("- [2026-10-10] #900 x\n## 归档\n".encode("utf-8"))
    append_ledger_entry(p7, "- [2026-10-11] #901 lf ｜ 触发: y 〔fp:t-7〕", "fp:t-7")
    assert _read(p7).count("\r") == 0
    n_pass += 1
    # ⑧ fp 双落 → 拒绝（幂等键须唯一）
    try:
        append_ledger_entry(p7, "- [2026-10-11] #902 双fp ｜ 触发: y 〔fp:t-8〕\n〔fp:t-8〕", "fp:t-8")
        raise SystemExit("⑧ fail")
    except AssertionError:
        n_pass += 1
    # ⑨ 附三① 写后校验失败自动回滚（负控：注入计数失真使写后断言失败）
    p9 = os.path.join(d, "l9.md")
    open(p9, "wb").write("- [2026-10-10] #900 x ｜ 触发: y\n## 归档\n".encode("utf-8"))
    orig = _read(p9)
    g = globals()  # __main__ 下 import ledger_writer 会另载独立实例 ⇒ 须 patch 当前命名空间
    real_active_count = g["active_count"]
    g["active_count"] = lambda *a, **k: 0  # 写后读数恒 0 ⇒ 增量断言必败
    try:
        append_ledger_entry(p9, "- [2026-10-11] #901 回滚负控 ｜ 触发: y 〔fp:t-9〕", "fp:t-9")
        raise SystemExit("⑨ fail（未抛异常）")
    except AssertionError:
        pass
    finally:
        g["active_count"] = real_active_count
    assert _read(p9) == orig, "⑨ 回滚失败：文件与写入前不一致"
    n_pass += 1
    # ⑩ 附三② fp=None 内容派生指纹：首跑 OK，二跑 SKIP，文件仅一条
    p10 = os.path.join(d, "l10.md")
    open(p10, "wb").write("- [2026-10-10] #900 x ｜ 触发: y\n## 归档\n".encode("utf-8"))
    b10 = "- [2026-10-11] #901 派生键 ｜ 触发: y"
    assert append_ledger_entry(p10, b10) == "OK"
    assert append_ledger_entry(p10, b10) == "SKIP"
    assert len(re.findall(r"#901(?!\d)", _read(p10))) == 1
    n_pass += 1
    # ⑪ 附三③ next_number 号位现读：全档 max+1（含归档区）
    assert next_number(p) == 902          # p 含 #901/#900/#800
    open(p5, "wb").write("## 归档\n".encode("utf-8"))  # 空档 ⇒ 1
    assert next_number(p5) == 1
    n_pass += 1
    # ⑫ v1.2⑥ BOM 件：首行条目在号位面（撞号停机）＋ 写入后 BOM 保型
    p12 = os.path.join(d, "l12.md")
    open(p12, "wb").write("﻿- [2026-10-10] #900 首行条目 ｜ 触发: y\n".encode("utf-8"))
    assert _read(p12).startswith("- ["), "⑫ BOM 未剥"
    assert next_number(p12) == 901, "⑫ BOM 件首行条目逃出号位面"
    assert active_count(_read(p12)) == 1, "⑫ BOM 件首行条目漏计"
    try:
        append_ledger_entry(p12, "- [2026-10-11] #900 BOM撞号 ｜ 触发: y 〔fp:t-12〕", "fp:t-12", anchor_line=None)
        raise SystemExit("⑫ fail（撞号未停机）")
    except AssertionError:
        pass
    b12 = "- [2026-10-11] #901 BOM件追加 ｜ 触发: y 〔fp:t-12b〕"
    assert append_ledger_entry(p12, b12, "fp:t-12b", anchor_line=None) == "OK"
    raw12 = open(p12, "rb").read()
    assert raw12.startswith(b"\xef\xbb\xbf"), "⑫ 写回丢失 BOM"
    assert raw12.decode("utf-8-sig").startswith("- [2026-10-10] #900"), "⑫ 首行条目受损"
    assert active_count(_read(p12)) == 2, "⑫ 追加后计数应为 2"
    n_pass += 1
    # ⑬ v1.2④ EOF 模式：无锚册 anchor_line=None ⇒ OK 且条目在尾；二跑 SKIP
    p13 = os.path.join(d, "l13.md")
    open(p13, "wb").write("- [2026-10-10] #900 尾条 ｜ 触发: y\n".encode("utf-8"))
    b13 = "- [2026-10-11] #901 EOF追加 ｜ 触发: y 〔fp:t-13〕"
    assert append_ledger_entry(p13, b13, "fp:t-13", anchor_line=None) == "OK"
    t13 = _read(p13)
    assert t13.index("#901") > t13.index("#900"), "⑬ EOF 追加未落尾"
    assert append_ledger_entry(p13, b13, "fp:t-13", anchor_line=None) == "SKIP"
    n_pass += 1
    # ⑭ v1.2⑤ 非 str 锚 → AssertionError（禁 AttributeError 逃出契约）
    try:
        append_ledger_entry(p13, "- [2026-10-11] #902 坏锚 ｜ 触发: y 〔fp:t-14〕", "fp:t-14", anchor_line=123)
        raise SystemExit("⑭ fail")
    except AssertionError:
        pass
    except AttributeError:
        raise SystemExit("⑭ fail：AttributeError 逃出 fail-closed 契约")
    n_pass += 1
    # ⑮ v1.3⑧ 混行尾件·LF 主体（问枢实证反向）：既存 CRLF 3 行保留＋新增行落 LF
    p15 = os.path.join(d, "l15.md")
    body15 = "- [2026-10-10] #900 a ｜ 触发: y\n" * 12 + "- [2026-10-09] #899 b ｜ 触发: y\r\n" * 3 + "## 归档\n"
    open(p15, "wb").write(body15.encode("utf-8"))
    before15 = _eol_stats(_read(p15))
    assert before15["crlf"] == 3 and before15["bare_lf"] == 13
    assert append_ledger_entry(p15, "- [2026-10-11] #901 混行尾LF主体 ｜ 触发: y 〔fp:t-15〕", "fp:t-15") == "OK"
    after15 = _eol_stats(_read(p15))
    assert after15["crlf"] == 3, f"⑮ 既存 CRLF 被抹平: {before15['crlf']}→{after15['crlf']}"
    assert after15["bare_lf"] == before15["bare_lf"] + 1, "⑮ 新增行未落主体 EOL"
    n_pass += 1
    # ⑯ v1.3⑦ 混行尾件·CRLF 主体：既存裸 LF 保留＋新增行落 CRLF
    p16 = os.path.join(d, "l16.md")
    body16 = "- [2026-10-10] #900 a ｜ 触发: y\r\n" * 5 + "- [2026-10-09] #899 b ｜ 触发: y\n" * 2 + "## 归档\r\n"
    open(p16, "wb").write(body16.encode("utf-8"))
    before16 = _eol_stats(_read(p16))
    assert before16["crlf"] == 6 and before16["bare_lf"] == 2
    assert append_ledger_entry(p16, "- [2026-10-11] #901 混行尾CRLF主体 ｜ 触发: y 〔fp:t-16〕", "fp:t-16") == "OK"
    after16 = _eol_stats(_read(p16))
    assert after16["bare_lf"] == 2, f"⑯ 既存裸 LF 被抹平: {before16['bare_lf']}→{after16['bare_lf']}"
    assert after16["crlf"] == before16["crlf"] + 1, "⑯ 新增行未落主体 EOL"
    n_pass += 1
    # ⑰ v1.3⑨ delta 门 fail-closed（负控：patch 主体判型为错误 EOL ⇒ 写前门拦截·零写入）
    p17 = os.path.join(d, "l17.md")
    open(p17, "wb").write(body15.encode("utf-8"))  # 同 ⑮ 之 LF 主体混行尾件
    orig17 = _read(p17)
    real_meol = g["_majority_eol"]
    g["_majority_eol"] = lambda *a, **k: "\r\n"  # 错误判型 ⇒ 新增行落 CRLF ⇒ delta 门必炸
    try:
        append_ledger_entry(p17, "- [2026-10-11] #901 delta门负控 ｜ 触发: y 〔fp:t-17〕", "fp:t-17")
        raise SystemExit("⑰ fail（delta 门未拦截）")
    except AssertionError:
        pass
    finally:
        g["_majority_eol"] = real_meol
    assert _read(p17) == orig17, "⑰ fail-closed 失效：写前门未拦住却已写盘"
    n_pass += 1
    # ⑱ v1.4⑩ plain 追加·登记簿行形（非台账条形）：混行尾件既存 CRLF 12 行保留
    #    ＋新增行落主体 LF＋前缀不变式（原件区零改动）＋幂等 fp SKIP
    p18 = os.path.join(d, "l18.md")
    body18 = "- 2026-10-13｜甲作：x\n" * 124 + "- 2026-10-12｜乙作：y\r\n" * 12
    open(p18, "wb").write(body18.encode("utf-8"))
    before18 = _eol_stats(_read(p18))
    assert before18["crlf"] == 12 and before18["bare_lf"] == 124
    raw18_before = open(p18, "rb").read()
    line18 = "- 2026-10-14｜丙作：plain 追加 〔fp:t-18〕"
    assert append_plain(p18, line18, "fp:t-18") == "OK"
    raw18_after = open(p18, "rb").read()
    assert raw18_after.startswith(raw18_before), "⑱ 前缀不变式破口：原件区被改动"
    after18 = _eol_stats(_read(p18))
    assert after18["crlf"] == 12, f"⑱ 既存 CRLF 被抹平: 12→{after18['crlf']}"
    assert after18["bare_lf"] == before18["bare_lf"] + 1, "⑱ 新增行未落主体 EOL"
    assert append_plain(p18, line18, "fp:t-18") == "SKIP", "⑱ fp 幂等失效"
    n_pass += 1
    # ⑲ v1.4⑩ plain 追加·fp=None 逐行去重：同文行二跑 SKIP；行尾非 str 值拒写
    p19 = os.path.join(d, "l19.md")
    open(p19, "wb").write("- 2026-10-13｜丁作：a\n".encode("utf-8"))
    line19 = "- 2026-10-14｜戊作：b"
    assert append_plain(p19, line19) == "OK"
    assert append_plain(p19, line19) == "SKIP", "⑲ 逐行去重失效"
    try:
        append_plain(p19, "   \r\n  ")
        raise SystemExit("⑲ fail（空行未拒）")
    except AssertionError:
        pass
    n_pass += 1
    # ⑳ v1.4⑩ plain 追加·BOM 件保型＋delta 门 fail-closed 负控（patch 判型）
    p20 = os.path.join(d, "l20.md")
    open(p20, "wb").write("﻿- 2026-10-13｜己作：a\n".encode("utf-8"))
    line20 = "- 2026-10-14｜庚作：b 〔fp:t-20〕"
    assert append_plain(p20, line20, "fp:t-20") == "OK"
    raw20 = open(p20, "rb").read()
    assert raw20.startswith(b"\xef\xbb\xbf"), "⑳ BOM 丢失"
    assert raw20.decode("utf-8-sig").startswith("- 2026-10-13｜己作：a"), "⑳ 首行受损"
    orig20 = _read(p20)
    real_meol2 = g["_majority_eol"]
    g["_majority_eol"] = lambda *a, **k: "\r\n"  # LF 件错误判型 ⇒ delta 门必炸
    try:
        append_plain(p20, "- 2026-10-14｜辛作：c 〔fp:t-20c〕", "fp:t-20c")
        raise SystemExit("⑳ fail（delta 门未拦截）")
    except AssertionError:
        pass
    finally:
        g["_majority_eol"] = real_meol2
    assert _read(p20) == orig20, "⑳ fail-closed 失效：写前门未拦住却已写盘"
    n_pass += 1
    print(f"selftest {n_pass}/20 PASS")
    assert n_pass == 20


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit(0)
    if "--next-number" in sys.argv:
        i = sys.argv.index("--next-number")
        print(next_number(sys.argv[i + 1]))
        sys.exit(0)
    print(__doc__)

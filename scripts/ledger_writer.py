# -*- coding: utf-8 -*-
"""ledger_writer.py —— 衡枢侧固退写器公共件本体（写器P-1/P-2 机械落形）

《固退写器公共件纪律》生效件（2026-10-11·作者拍板）之衡枢本体。
各席写器本体到位后改传参调用本件，不另造第二套（写器P-3·一面一秤）。

用法（嵌入固退写器脚本）：
    from ledger_writer import append_ledger_entry, proof, find_anchor
    st = append_ledger_entry(LEDGER_PATH, BLOCK, fp=FP)   # 'OK' | 'SKIP'
    proof(LEDGER_PATH, before_active, expect_delta=1)

纪律来源：patterns/reusable-patterns.md「固退写器公共件纪律（写器P-1～P-4）」。
自检：python ledger_writer.py --selftest
"""
import os
import re
import sys
import tempfile

ENTRY_RE = re.compile(r"^- \[\d{4}-\d\d-\d\d\] #(\d+)", re.M)
EXCLUDE_MARKS = ("[已核销", "[已归档")


def _read(path):
    return open(path, "rb").read().decode("utf-8")


def _write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(text.encode("utf-8"))
    os.replace(tmp, path)


def _is_crlf(text):
    return "\r\n" in text


def _check_lineend(text):
    """行尾不变量：CRLF 件 CR==LF==CRLF 且 CRCRLF==0；LF 件 CR==0。违者 AssertionError。"""
    crlf = text.count("\r\n")
    lf = text.count("\n")
    cr = text.count("\r")
    crcrc = text.count("\r\r\n")
    if _is_crlf(text):
        assert crcrc == 0, f"CRCRLF={crcrc}（双重转换坑）"
        assert cr == lf == crlf, f"混行尾: CR={cr} LF={lf} CRLF={crlf}"
    else:
        assert cr == 0, f"LF 件含孤立 CR: {cr}"


def find_anchor(lines, target):
    """写器P-1：整行 strip() 相等锚，断言恰 1 处，返回行号。禁裸 find／子串 count。"""
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


def append_ledger_entry(path, block, fp, anchor_line="## 归档"):
    """向台账件锚前插入一条目（幂等：fp 已在 ⇒ SKIP）。

    block 硬断言（fail-closed·写盘前）：
      ① 以「- [」起行；② 含「触发:」或「触发：」栏；③ fp 在块内恰 1 次；
      ④ 条目 ID 全档唯一（新条号不得与既有任何条目撞）。
    返回 'OK' 或 'SKIP'。
    """
    text = _read(path)
    if fp and fp in text:
        return "SKIP"  # 幂等 guard：fp 即内容指纹
    # —— 写前断言（fail-closed，零副作用）——
    assert block.lstrip().startswith("- ["), "条目须以「- [」起行"
    assert ("触发:" in block) or ("触发：" in block), "缺触发栏"
    assert fp and block.count(fp) == 1, "fp 须在块内恰 1 次（幂等键唯一）"
    m = ENTRY_RE.match(block)
    assert m, "条目行须含「- [日期] #N」号位"
    entry_id = m.group(1)
    assert not entry_id_exists(text, entry_id), f"条目号 #{entry_id} 全档撞号·停机"
    # —— 归一 → 插入 → 还原 ——
    crlf = _is_crlf(text)
    norm = text.replace("\r\n", "\n") if crlf else text
    lines = norm.split("\n")
    idx = find_anchor(lines, anchor_line)
    lines.insert(idx, block.rstrip("\n"))
    out = "\n".join(lines)
    if crlf:
        out = out.replace("\n", "\r\n")
    _check_lineend(out)
    before = active_count(text, anchor_line)
    _write(path, out)
    # —— 写器P-2：写后自证 ——
    after_text = _read(path)
    after = active_count(after_text, anchor_line)
    assert after - before == 1, f"活跃计数增量 {after - before} ≠ 1（写入成功≠门禁可见）"
    _check_lineend(after_text)
    return "OK"


def proof(path, before_active, expect_delta=1, anchor_line="## 归档"):
    """写器P-2 独立自证入口：计数增量＋行尾保型。返回 (delta, ok)。"""
    text = _read(path)
    delta = active_count(text, anchor_line) - before_active
    assert delta == expect_delta, f"计数增量 {delta} ≠ 预期 {expect_delta}"
    _check_lineend(text)
    return delta, True


def _selftest():
    """负控夹具 8 条：全过打 PASS 并 rc=0。"""
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
    assert st2 == "SKIP" and t.count("#901") - t.count("#9011") == len(re.findall(r"#901(?!\d)", t)) == 1
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
    print(f"selftest {n_pass}/8 PASS")
    assert n_pass == 8


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit(0)
    print(__doc__)

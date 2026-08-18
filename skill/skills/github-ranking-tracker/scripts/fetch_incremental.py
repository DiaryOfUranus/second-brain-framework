# -*- coding: utf-8 -*-
"""增量抓取：先抓主页提取 Top100 链接，再逐页抓取解析写盘。
产出 2026-08-10-<label>.md，label 命名与基线一致（all-stars/all-forks/lang-<L>）。
"""
import urllib.request, ssl, re, os, time, datetime

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
MAIN = "https://evanli.github.io/Github-Ranking/"
BASE = "https://evanli.github.io/Github-Ranking/Top100/"
OUT = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/ranking-snapshots"
DATE = "2026-08-10"
os.makedirs(OUT, exist_ok=True)

def fetch(url, tries=4):
    last=None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=30, context=ctx).read().decode("utf-8","ignore")
        except Exception as e:
            last=e
            if t==tries-1:
                print(f"   [dbg] last err {type(e).__name__}: {e}")
                return None
            time.sleep(1.5)

# 1) 抓主页提取所有 Top100 链接
main = fetch(MAIN)
if not main:
    print("[FATAL] main page fetch failed"); raise SystemExit(1)
hrefs = re.findall(r'href="([^"]*Top100/[^"]+\.html)"', main)
SITE = "https://evanli.github.io/"
urls = []
seen=set()
for h in hrefs:
    if h.startswith("http"):
        full = h
    elif h.startswith("/"):
        full = SITE.rstrip("/")+h
    else:
        full = SITE+h.lstrip("/")
    if full in seen: continue
    seen.add(full); urls.append(full)
print(f"[INFO] main page extracted {len(urls)} Top100 links")
print("[INFO] sample urls:", urls[:2])

def label_of(url):
    fn = url.rsplit("/",1)[-1]
    name = fn[:-5] if fn.endswith(".html") else fn  # strip .html
    if name=="Top-100-stars": return "all-stars"
    if name=="Top-100-forks": return "all-forks"
    return "lang-"+name

def parse(html):
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.S)
    out=[]
    for r in rows:
        if '<th>' in r: continue
        cells = re.findall(r'<td>(.*?)</td>', r, re.S)
        if len(cells)<8: continue
        rank=cells[0].strip()
        m=re.search(r'href="https://github\.com/([^"]+)"', cells[1])
        repo=m.group(1) if m else re.sub(r'<[^>]+>','',cells[1]).strip()
        stars=re.sub(r'<[^>]+>','',cells[2]).strip()
        forks=re.sub(r'<[^>]+>','',cells[3]).strip()
        lang=re.sub(r'<[^>]+>','',cells[4]).strip()
        issues=re.sub(r'<[^>]+>','',cells[5]).strip()
        desc=re.sub(r'<[^>]+>','',cells[6]).strip()
        lastc=re.sub(r'<[^>]+>','',cells[7]).strip()
        lastc=lastc[:10] if lastc else ""
        out.append((rank,repo,lang,stars,forks,issues,lastc,desc))
    return out

def write_file(label, url, rows):
    path=os.path.join(OUT, f"{DATE}-{label}.md")
    title = label.replace("lang-","Lang=").replace("all-","All-")
    lines=[f"# GitHub Ranking Top100 — {title} ({DATE})",
           f"> source: {url}",
           f"> fetched: {DATE} | entries: {len(rows)}",
           "",
           "| Rank | Project | Lang | Stars | Forks | OpenIssues | LastCommit | Description |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        rank,repo,lang,stars,forks,issues,lastc,desc=r
        d=desc.replace("|","/").replace("\n"," ")
        lines.append(f"| {rank} | {repo} | {lang} | {stars} | {forks} | {issues} | {lastc} | {d} |")
    open(path,"w",encoding="utf-8").write("\n".join(lines)+"\n")
    return path

ok=0; fail=0; labels=[]
for url in urls:
    label=label_of(url)
    html=fetch(url)
    if not html:
        print(f"[FAIL] {label}: fetch None"); fail+=1; continue
    rows=parse(html)
    if not rows:
        print(f"[FAIL] {label}: parse 0 rows"); fail+=1; continue
    p=write_file(label,url,rows)
    labels.append(label)
    print(f"[OK] {label}: {len(rows)} rows -> {os.path.basename(p)}"); ok+=1
    time.sleep(0.3)

# 写 file-index
idx=os.path.join(OUT, f"{DATE}-file-index.md")
open(idx,"w",encoding="utf-8").write(
    f"# 快照文件索引 {DATE}\n\n> 共 {len(labels)} 个 Top100 页\n\n" +
    "\n".join(f"- `{DATE}-{l}.md`" for l in sorted(labels)) + "\n")
print(f"DONE ok={ok} fail={fail} total={len(urls)}")

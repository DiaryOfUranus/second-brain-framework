import urllib.request, ssl, re, os, time, datetime

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
BASE = "https://evanli.github.io/Github-Ranking/Top100/"
OUT = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/ranking-snapshots"
DATE = "2026-08-03"
os.makedirs(OUT, exist_ok=True)

# (filename, label)
pages = [
    ("Top-100-stars.html", "all-stars"),
    ("Top-100-forks.html", "all-forks"),
]
langs = ["ActionScript","C","CSharp","CPP","Clojure","CoffeeScript","CSS","Dart","DM",
"Elixir","Go","Groovy","Haskell","HTML","Java","JavaScript","Julia","Kotlin","Lua",
"MATLAB","Objective-C","Perl","PHP","PowerShell","Python","R","Ruby","Rust","Scala",
"Shell","Swift","TeX","TypeScript","Vim-script"]
for L in langs:
    pages.append((L+".html", "lang-"+L))

def fetch(url, tries=3):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=25, context=ctx).read().decode("utf-8","ignore")
        except Exception as e:
            if t==tries-1: return None
            time.sleep(1.5)

def parse(html):
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.S)
    out=[]
    for r in rows:
        if '<th>' in r: continue  # header
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

def write_file(fname, label, url, rows):
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

ok=0; fail=0
for fname,label in pages:
    url=BASE+fname
    html=fetch(url)
    if not html:
        print(f"[FAIL] {label}: fetch None"); fail+=1; continue
    rows=parse(html)
    if not rows:
        print(f"[FAIL] {label}: parse 0 rows"); fail+=1; continue
    p=write_file(fname,label,url,rows)
    print(f"[OK] {label}: {len(rows)} rows -> {os.path.basename(p)}"); ok+=1
    time.sleep(0.3)

print(f"DONE ok={ok} fail={fail} total={len(pages)}")

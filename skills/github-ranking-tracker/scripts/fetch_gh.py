import urllib.request, ssl, json, time, os

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
OUT = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/projects/_gh_meta.md"
DATE = "2026-08-10"

repos = [
 # existing 8
 "openclaw/openclaw","NousResearch/hermes-agent","Significant-Gravitas/AutoGPT",
 "ollama/ollama","langgenius/dify","n8n-io/n8n","langchain-ai/langchain","anthropics/claude-code",
 # new 12
 "ultraworkers/claw-code","obra/superpowers","affaan-m/ECC","mattpocock/skills",
 "farion1231/cc-switch","msitarzewski/agency-agents","openai/symphony","openai/codex",
 "ggml-org/llama.cpp","infiniflow/ragflow","open-webui/open-webui","langflow-ai/langflow",
]

def fetch(repo, tries=3):
    url=f"https://api.github.com/repos/{repo}"
    for t in range(tries):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.github+json"})
            data=json.loads(urllib.request.urlopen(req, timeout=20, context=ctx).read().decode("utf-8","ignore"))
            return data
        except Exception as e:
            if t==tries-1: return {"__err__":f"{type(e).__name__}: {e}"}
            time.sleep(2)

meta={}
for r in repos:
    d=fetch(r)
    meta[r]=d
    if "__err__" in d:
        print(f"[ERR] {r}: {d['__err__']}")
    else:
        print(f"[OK] {r}: stars={d.get('stargazers_count')} lang={d.get('language')} pushed={d.get('pushed_at')}")
    time.sleep(0.5)

# write concise markdown table
lines=[f"# GitHub 实测元数据（{DATE}）","> 来源 api.github.com/repos/<repo>，未鉴权（60/min 限额内）。","",
 "| 项目 | Stars | Forks | Lang | OpenIssues | Created | Pushed | Topics | Description |",
 "|---|---|---|---|---|---|---|---|---|"]
for r in repos:
    d=meta[r]
    if "__err__" in d:
        lines.append(f"| {r} | ERR | | | | | | | {d['__err__']} |"); continue
    topics=", ".join(d.get("topics",[])[:8])
    desc=(d.get("description") or "").replace("|","/")
    lines.append(f"| {r} | {d.get('stargazers_count')} | {d.get('forks_count')} | {d.get('language')} | {d.get('open_issues_count')} | {d.get('created_at','')[:10]} | {d.get('pushed_at','')[:10]} | {topics} | {desc} |")

open(OUT,"w",encoding="utf-8").write("\n".join(lines)+"\n")
print(f"\nwrote {OUT}")
# also dump raw json for card generation
open(OUT.replace("_gh_meta.md","_gh_meta.json"),"w",encoding="utf-8").write(json.dumps(meta, ensure_ascii=False, indent=1))

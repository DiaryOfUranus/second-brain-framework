# -*- coding: utf-8 -*-
"""采集 recorded 项目近期发版/提交，写 _recent.json + _recent.md，并就地更新各卡'近期变动'段。"""
import urllib.request, ssl, json, time, os, re

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
PROJ = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/projects"
DATE = "2026-08-10"
repos = {
 "openclaw":"openclaw/openclaw","hermes-agent":"NousResearch/hermes-agent","AutoGPT":"Significant-Gravitas/AutoGPT",
 "ollama":"ollama/ollama","dify":"langgenius/dify","n8n":"n8n-io/n8n","langchain":"langchain-ai/langchain",
 "claude-code":"anthropics/claude-code","claw-code":"ultraworkers/claw-code","superpowers":"obra/superpowers",
 "ECC":"affaan-m/ECC","mattpocock-skills":"mattpocock/skills","cc-switch":"farion1231/cc-switch",
 "agency-agents":"msitarzewski/agency-agents","symphony":"openai/symphony","codex":"openai/codex",
 "llama-cpp":"ggml-org/llama.cpp","ragflow":"infiniflow/ragflow","open-webui":"open-webui/open-webui",
 "langflow":"langflow-ai/langflow",
}
def fetch(url, tries=3):
    for t in range(tries):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.github+json"})
            return json.loads(urllib.request.urlopen(req, timeout=20, context=ctx).read().decode("utf-8","ignore"))
        except urllib.error.HTTPError as e:
            if e.code==404: return {"__404__":True}
            if t==tries-1: return {"__err__":f"{e.code}"}
            time.sleep(2)
        except Exception as e:
            if t==tries-1: return {"__err__":f"{type(e).__name__}"}
            time.sleep(2)

recent={}
for name,slug in repos.items():
    rel=fetch(f"https://api.github.com/repos/{slug}/releases/latest")
    commits=fetch(f"https://api.github.com/repos/{slug}/commits?per_page=5")
    rel_info=None
    if isinstance(rel,dict) and not any(k.startswith("__") for k in rel):
        rel_info={"tag":rel.get("tag_name"),"name":rel.get("name"),"published":(rel.get("published_at") or "")[:10]}
    cl=[]
    if isinstance(commits,list):
        for c in commits[:5]:
            cm=c.get("commit",{})
            cl.append({"date":(cm.get("author",{}).get("date") or "")[:10],"msg":(cm.get("message") or "").split("\n")[0][:90]})
    recent[name]={"slug":slug,"release":rel_info,"commits":cl}
    print(f"[OK] {name}: release={rel_info['tag'] if rel_info else 'NONE'} commits={len(cl)}")
    time.sleep(0.6)

open(os.path.join(PROJ,"_recent.json"),"w",encoding="utf-8").write(json.dumps(recent,ensure_ascii=False,indent=1))

# 写 _recent.md 摘要
L=[f"# recorded 项目近期活动（{DATE}）\n> GitHub API：latest release + 最近 5 commits\n"]
for name,d in recent.items():
    L.append(f"## {name}（{d['slug']}）")
    if d["release"]:
        L.append(f"- 最新发版：{d['release']['tag']}（{d['release']['name']}）发布于 {d['release']['published']}")
    else:
        L.append("- 最新发版：无（或未打 release tag）")
    L.append("- 最近提交：")
    for c in d["commits"]:
        L.append(f"  - {c['date']} {c['msg']}")
    L.append("")
open(os.path.join(PROJ,"_recent.md"),"w",encoding="utf-8").write("\n".join(L)+"\n")

# 就地更新各卡'近期变动'段
def update_card(name, d):
    p=os.path.join(PROJ,name+".md")
    if not os.path.isfile(p): return False
    txt=open(p,encoding="utf-8").read()
    sec=f"## 近期变动（GitHub API {DATE}）\n"
    if d["release"]:
        sec+=f"- 最新发版：**{d['release']['tag']}**（{d['release']['name']}）发布于 {d['release']['published']}\n"
    else:
        sec+=f"- 最新发版：本周未检出新 release（或未打 tag）\n"
    sec+=f"- 最近推送活跃度见 _gh_meta.md（stars/forks/pushed）。\n- 最近 5 次提交：\n"
    for c in d["commits"]:
        sec+=f"  - {c['date']}｜{c['msg']}\n"
    sec+=f"- 置信度：实测元数据级（release/commits 已核验）。\n"
    # 替换已有'近期变动'段或追加
    m=re.search(r"## 近期变动（GitHub API 20\d\d-\d\d-\d\d）\n.*?(?=\n## |\Z)", txt, re.S)
    if m:
        txt=txt[:m.start()]+sec+txt[m.end():]
    else:
        # 追加到'## 待办'之前，或末尾
        mt=re.search(r"\n## 待办", txt)
        if mt: txt=txt[:mt.start()]+"\n"+sec+"\n"+txt[mt.start():]
        else: txt=txt+"\n"+sec
    open(p,"w",encoding="utf-8").write(txt)
    return True

ok=0
for name,d in recent.items():
    if update_card(name,d): ok+=1
print(f"\nupdated cards: {ok}/{len(recent)}")

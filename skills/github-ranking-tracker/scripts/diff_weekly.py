# -*- coding: utf-8 -*-
"""周环比 diff：对比 2026-08-03 与 2026-08-10 两套快照。
产出 weeklies/2026-08-10.md。
方法：纯快照对比（同为 evanli 站点 stars，apples-to-apples）。
"""
import os, re, glob

SNAP = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/ranking-snapshots"
WEEK = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/weeklies"
OLD = "2026-08-03"
NEW = "2026-08-10"

def parse_snap(date):
    """返回 (universe: {repo_lower: [(label,rank,stars,forks)]}, stars_top100: set, forks_top100: set)"""
    universe = {}
    stars_top100 = set(); forks_top100 = set()
    for path in glob.glob(os.path.join(SNAP, f"{date}-*.md")):
        fn = os.path.basename(path)
        if fn.endswith("file-index.md") or fn.endswith("AI-cluster-index.md"): continue
        label = fn[len(date)+1:-3]  # strip date- and .md
        for line in open(path, encoding="utf-8"):
            if not line.startswith("| "): continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5: continue
            if cells[0] == "Rank" or not cells[0].isdigit(): continue
            rank = int(cells[0])
            repo = cells[1]
            stars_s = cells[3].replace(",", "")
            forks_s = cells[4].replace(",", "")
            try: stars = int(stars_s)
            except: stars = 0
            try: forks = int(forks_s)
            except: forks = 0
            universe.setdefault(repo.lower(), []).append((label, rank, stars, forks))
            if label == "all-stars": stars_top100.add(repo.lower())
            if label == "all-forks": forks_top100.add(repo.lower())
    return universe, stars_top100, forks_top100

ou, ost, oft = parse_snap(OLD)
nu, nst, nft = parse_snap(NEW)

def best_rank(u, repo):
    rows = u.get(repo.lower())
    if not rows: return None, None, None
    # 优先 all-stars，否则最小 rank
    asrows = [r for r in rows if r[0]=="all-stars"]
    pick = min(asrows if asrows else rows, key=lambda r: r[1])
    return pick[1], pick[2], pick[0]

# recorded 项目（slug 小写用于匹配快照 Project 列）
recorded = {
 "openclaw/openclaw":"openclaw","nousresearch/hermes-agent":"hermes-agent",
 "significant-gravitas/autogpt":"AutoGPT","ollama/ollama":"ollama",
 "langgenius/dify":"dify","n8n-io/n8n":"n8n","langchain-ai/langchain":"langchain",
 "anthropics/claude-code":"claude-code","ultraworkers/claw-code":"claw-code",
 "obra/superpowers":"superpowers","affaan-m/ecc":"ECC","mattpocock/skills":"mattpocock-skills",
 "farion1231/cc-switch":"cc-switch","msitarzewski/agency-agents":"agency-agents",
 "openai/symphony":"symphony","openai/codex":"codex","ggml-org/llama.cpp":"llama-cpp",
 "infiniflow/ragflow":"ragflow","open-webui/open-webui":"open-webui",
 "langflow-ai/langflow":"langflow","qwen-code-dev-bot/oh-my-cli":"oh-my-cli",
}

# tracked 未深分析候选
tracked = ["firecrawl","awesome-llm-apps","spec-kit","system-prompts-and-models-of-ai-tools",
 "gstack","ui-ux-pro-max-skill","andrej-karpathy-skills","nextchat","comfyui",
 "transformers","stable-diffusion-webui"]

lines = []
lines.append(f"# 周报 · {NEW}（周环比 {OLD} → {NEW}）\n")
lines.append("> 数据源：https://evanli.github.io/Github-Ranking/ ｜ 方法：子 skill `github-ranking-tracker`")
lines.append("> 对比口径：同为站点快照 stars，apples-to-apples；本周 star 绝对值另以 GitHub API 复核（见 projects/_gh_meta.md）。\n")

# ---- A. 全站 Stars Top100 进出榜 ----
new_in = sorted(nst - ost)
dropped = sorted(ost - nst)
lines.append("## 一、全站 Stars Top100 进出榜\n")
if new_in:
    lines.append(f"**新进榜（{len(new_in)}）**：")
    for r in new_in:
        rank, stars, _ = best_rank(nu, r)
        lines.append(f"- {r} — 现排名 #{rank}，stars≈{stars:,}")
else:
    lines.append("- 新进榜：无")
if dropped:
    lines.append(f"\n**出榜（{len(dropped)}）**：")
    for r in dropped:
        rank, stars, _ = best_rank(ou, r)
        lines.append(f"- {r} — 上周排名 #{rank}，stars≈{stars:,}")
else:
    lines.append("\n- 出榜：无")

# ---- B/C. recorded 项目 rank + star 变动 ----
lines.append("\n## 二、recorded 项目周变动（rank 取各页最佳；star 取快照值）\n")
lines.append("| 项目 | 上周rank | 本周rank | rankΔ | 上周stars | 本周stars | starΔ | starΔ% | 备注 |")
lines.append("|---|---|---|---|---|---|---|---|---|")
notable = []
for slug, name in recorded.items():
    orank, ostars, olabel = best_rank(ou, slug)
    nrank, nstars, nlabel = best_rank(nu, slug)
    if orank is None and nrank is None:
        lines.append(f"| {name} | - | - | - | - | - | - | - | 未在任一 Top100 快照（如 oh-my-cli） |")
        continue
    rd = "" if (orank is None or nrank is None) else (nrank-orank)
    sd = "" if (ostars is None or nstars is None) else (nstars-ostars)
    sd_pct = "" if (ostars in (None,0) or sd=="") else f"{sd/ostars*100:.1f}%"
    note=""
    if orank is None and nrank is not None: note="↑新入榜"
    if orank is not None and nrank is None: note="↓出榜"
    if isinstance(sd, int) and ostars and sd/ostars > 0.05: note += " ⚡star>+5%"
    if isinstance(nrank, int) and nrank<=50 and (orank is None or orank>50): note += " ⭐进前50"
    lines.append(f"| {name} | {orank} | {nrank} | {rd} | {ostars:,} | {nstars:,} | {sd:,} | {sd_pct} | {note.strip()} |")
    if (isinstance(sd,int) and ostars and sd/ostars>0.05) or (isinstance(nrank,int) and nrank<=50 and (orank is None or orank>50)):
        notable.append(name)

# ---- D. tracked 候选状态 ----
lines.append("\n## 三、tracked 候选（未深分析）本周快照状态\n")
lines.append("| 候选 | 是否在任一 Top100 快照 | 本周最佳rank | 本周stars |")
lines.append("|---|---|---|---|")
for t in tracked:
    present = [r for r in nu if t.lower() in r]
    if present:
        ranks=[best_rank(nu,r) for r in present]
        best=min([x for x in ranks if x[0]], key=lambda x:x[0])
        lines.append(f"| {t} | 是（{', '.join(present)}） | #{best[0]} | {best[1]:,} |")
    else:
        lines.append(f"| {t} | 否 | - | - |")

# ---- E. 新 AI 集群扫描 ----
lines.append("\n## 四、本周新浮现 AI 集群项目（建议扩编深分析）\n")
KW = ["agent","llm","ai-","gpt","claude","langchain","rag","mcp","skill","copilot","chatbot","prompt","transformer","diffusion","autonomous","workflow ai"]
baseline_repos = set(ou.keys())
new_ai = []
for repo, rows in nu.items():
    if repo in baseline_repos: continue
    # 只在全站 stars/forks top100 或语言 top 前30 关注
    top = min(rows, key=lambda r:r[1])
    if top[1] > 30: continue
    desc = ""
    # 取描述：从任一快照行（已无 desc 保存，跳过）
    hit = any(k in repo.lower() for k in KW) or top[1]<=20
    if hit:
        new_ai.append((repo, top[0], top[1], top[2]))
new_ai.sort(key=lambda x:x[2], reverse=True)
if new_ai:
    lines.append("| 项目 | 所在榜 | rank | stars |")
    lines.append("|---|---|---|---|")
    for repo,label,rank,stars in new_ai[:40]:
        lines.append(f"| {repo} | {label} | #{rank} | {stars:,} |")
else:
    lines.append("- 无显著新浮现（或全在基线宇宙内）")

lines.append("\n## 五、待办（本周 action）\n")
lines.append("- [ ] 见任务 4：对 tracked 候选 + 新浮现 AI 项目扩编深分析卡")
lines.append("- [ ] 见任务 1：以 GitHub API 复核 recorded 项目近期发版，更新各卡\"近期变动\"段")

out = os.path.join(WEEK, f"{NEW}.md")
open(out,"w",encoding="utf-8").write("\n".join(lines)+"\n")
print("wrote", out)
print("notable star jumps:", notable)
print("new AI candidates:", len(new_ai))

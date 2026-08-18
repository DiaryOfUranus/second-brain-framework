# -*- coding: utf-8 -*-
import json, os, re
PROJ = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/projects"
DATE = "2026-08-10"
recent = json.load(open(os.path.join(PROJ, "_recent.json"), encoding="utf-8"))
limited = [k for k, v in recent.items()
           if v.get("release") is None and (not isinstance(v.get("commits"), list) or len(v["commits"]) == 0)]
print("limited repos:", limited)

pending = (
    "## 近期变动（GitHub API " + DATE + "）\n"
    "- 最新发版：**本周未核验**——GitHub API 未鉴权限额（60/小时）已在上轮采集用尽，"
    "release/commits 详情待下周日 API 复位后补（避免限流假阴性误判为无发版）。\n"
    "- 最近推送活跃度（stars/forks/pushed）见 projects/_gh_meta.md（" + DATE + " 已核验）。\n"
    "- 置信度：实测元数据级（stars/forks/pushed 已核验）；release/commits 待补，标 pending-release。\n"
)

for name in limited:
    p = os.path.join(PROJ, name + ".md")
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"## 近期变动（GitHub API 20\d\d-\d\d-\d\d）\n.*?(?=\n## |\Z)", txt, re.S)
    if m:
        txt = txt[:m.start()] + pending + txt[m.end():]
        open(p, "w", encoding="utf-8").write(txt)
        print("[修正] " + name + ".md")
    else:
        print("[跳过-无段] " + name)
print("DONE")

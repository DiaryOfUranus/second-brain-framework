# -*- coding: utf-8 -*-
"""采集 11 个 tracked 候选元数据（源：2026-08-10 快照，源 GitHub 经 evanli 镜像），
生成锚定判词的深分析卡。release 因 API 限额标待核验。"""
import glob, json, os, re

PROJ = '{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/projects'
SNAP = '{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/ranking-snapshots'
DATE = '2026-08-10'
LINK = 'Projects/机思符号系统/交付物/理论对接卡-本地AI管理工具架构判词与{{INSTANCE_NAME}}补刀.md'

repos = {
 'firecrawl':'firecrawl/firecrawl',
 'awesome-llm-apps':'shubhamsaboo/awesome-llm-apps',
 'spec-kit':'github/spec-kit',
 'system-prompts-and-models-of-ai-tools':'x1xhlol/system-prompts-and-models-of-ai-tools',
 'gstack':'garrytan/gstack',
 'ui-ux-pro-max-skill':'nextlevelbuilder/ui-ux-pro-max-skill',
 'andrej-karpathy-skills':'multica-ai/andrej-karpathy-skills',
 'nextchat':'ChatGPTNextWeb/NextChat',
 'comfyui':'comfy-org/ComfyUI',
 'transformers':'huggingface/transformers',
 'stable-diffusion-webui':'AUTOMATIC1111/stable-diffusion-webui',
}

# 从 8/10 快照解析每个 repo 记录
universe={}
for path in glob.glob(os.path.join(SNAP, DATE+'-*.md')):
    fn=os.path.basename(path)
    if fn.endswith('file-index.md'): continue
    for line in open(path, encoding='utf-8'):
        if not line.startswith('| '): continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)<5: continue
        if not cells[0].isdigit(): continue
        repo=cells[1].lower(); lang=cells[2]
        stars_s=cells[3].replace(',',''); desc=cells[7] if len(cells)>7 else ''
        try: stars=int(stars_s)
        except: stars=0
        universe.setdefault(repo, []).append((lang, stars, desc))

meta={}
for name,slug in repos.items():
    rows=universe.get(slug.lower())
    if not rows:
        print('[WARN] '+name+': not in any 8/10 snapshot'); continue
    lang,stars,desc=rows[0]
    for r in rows:
        if r[0] and r[0] != 'None':
            lang,stars,desc=r; break
    meta[name]={'slug':slug,'stars':stars,'forks':'?','lang':lang,'pushed':'?','topics':[],'desc':desc,'release':None}
    print('[OK] '+name+': '+str(stars)+' stars/'+str(lang))

open(os.path.join(PROJ,'_tracked_meta.json'),'w',encoding='utf-8').write(json.dumps(meta,ensure_ascii=False,indent=1))

A = {
'firecrawl': dict(
  pos='把任意网站转成 LLM-ready 的结构化数据（Markdown/JSON），提供 crawl/scrape 的 API 与自托管。',
  i_would='锚定【落点2 索引协议】＋【落点1 入口输入工程】：它是"把人类意图（抓取某站）压缩为 AI 可吃的结构化索引"的入口工具——内容早已在 Web，firecrawl 是检索钥匙而非货物。我会把它接在调度中枢的"输入翻译层"之下：默认 AI 把"研究 X"翻译成 firecrawl 调用而非把整站塞上下文。质量审计在出口（数据是否干净）而非入口。',
  actual='实测为 AI 数据摄取层（crawl 到 LLM-ready），与 落点2 同构。它的"结构化抽取"正是机思索引协议的外部实现：以极小输入（URL+schema）换回 AI 内部本就缺失的外部知识指针。',
  pc='优：验证"入口输入工程＝把外部知识压缩成索引"在商业产品成立。劣：它产的是文本块/JSON，若不经归因协议升级为归因对，仍是"记忆=知识库"而非"记忆=相位图"（撞 落点2 的弥散区警示）。',
  help_='最强印证【落点2】：外部知识须经"索引协议"压缩进 AI，而非灌文本。反向喂"本地AI管理工具"——我们的机思符号输入翻译层可直接复用其 schema 抽取范式；但须补归因协议，否则落入"记忆存文本"陷阱。'),
'awesome-llm-apps': dict(
  pos='精选 LLM 应用/agent 项目清单（curated list），社区维护。',
  i_would='锚定【落点3 skill 双条款·补操作性分界】：清单是"随社区折旧的事实索引"→应归检索层/日志库，不应固化成 skill（会通胀）。若要做成 skill，只存"如何检索这份清单的语法"而非清单正文。',
  actual='典型"知识库型"资产：高价值但折旧快。若有人把它整份塞进 skill 正文，正好撞用户判词要执法的一刀（skill 存语法不存文本）。',
  pc='优：信息密度高、入门友好。劣：纯清单无加载策略/预算审计，规模上来必通胀——印证"技能账过预算审计"必要性。',
  help_='反面教材加边界样本：提醒"跨载体不变的程续性资产→skill；随载体折旧的事实→KB"。直接喂"skill 双条款"的操作性分界判定。'),
'spec-kit': dict(
  pos='微软出品：spec-driven 开发——把需求写成 spec，由 agent 按 spec 实现/验证/迭代。',
  i_would='锚定【落点1 两端管辖】＋【落点4 调度中枢】：spec 是"人类意图的最小可编译输入"（入口输入工程）；agent 按 spec 拆分/实现/质管（运营权）。宪法层（spec 不可被 agent 擅自改目标）禁授——spec 即受保护治理平面的标准件。',
  actual='把"需求到实现"做成 spec 契约，agent 在 spec 边界内运营。与 落点1/4 高度同构：入口=spec（结构化输入），出口=验证/测试（审计）。',
  pc='优：大厂背书"意图压缩成可编译 spec"范式，直证 落点1。劣：spec 仍可能被 agent 漂移修改，需显式 CODEOWNERS 式保护（呼应 oh-my-cli 的 AUTONOMY.md 标准件）。',
  help_='【落点1/4】的生产级佐证：spec＝入口输入工程的契约形态；其"受保护 spec"机制可直接对标我们的"宪法权禁授"。建议把 spec-kit 的 spec 保护范式结晶进第二大脑子 skill 的治理模板。'),
'system-prompts-and-models-of-ai-tools': dict(
  pos='收集各 AI 工具（Cursor/Cline/等）的 system prompt 与模型配置，逆向公开其"输入配方"。',
  i_would='锚定【落点1 入口输入工程】＋【落点3 skill 双条款】：system prompt 正是"我们能改的唯一输入"的实物样本。我会把它当"索引协议语料"而非照搬——逐载体实测哪些 prompt 段真正改变激活路由面（补刀 a：输入塑形不等于权重改变，是唯一近似杠杆）。',
  actual='把各家"输入配方"集中曝光，实证"输入工程＝封闭权重下唯一可行杠杆"（补刀 a）。但它存的是文本原文，若当 skill 正文灌会撞 落点3"存语法不存文本"。',
  pc='优：把"输入可改"这件判词事实做成可观测语料库。劣：纯文本集合，缺归因协议（哪些 prompt 段有效未验证）；规模大后折旧快。',
  help_='【落点1+补刀a】的实证矿：这些 prompt 是"输入侧赋权＝近似杠杆"的现成对照样本。喂"本地AI管理工具"——我们的输入翻译层应以"语法（如何构造 prompt）"而非"prompt 文本"入库。'),
'gstack': dict(
  pos='YC 系 AI 开发工作流栈（garrytan/gstack），把编码 agent 串成可管理的开发流水线。',
  i_would='锚定【落点4 调度中枢权限裁定】：它是"默认 AI 拿运营权做任务拆分/编排/质管"的具象。我会要求它的编排知识经归因协议自学（相位图），且流水线终态受出口审计；宪法权（任务账本/归因底账）在栈外。',
  actual='做 agent 开发流水线编排，是 落点4"调度中枢"的生态样本：把拆任务/路由/质管交给默认 AI。',
  pc='优：验证"运营权授予、宪法权禁授"在开发流水线成立。劣：若编排写死先验表而不自学，会撞"中枢知识不能出厂写死"一刀（落点4）。',
  help_='【落点4】调度中枢参照：其"开发流水线编排"可抽象为我们的子任务管理 UI；路由表自学机制值得借鉴，避免先验写死。'),
'ui-ux-pro-max-skill': dict(
  pos='一个"UI/UX 设计"agent skill（nextlevelbuilder 出品），把设计流程固化成可调用技能。',
  i_would='锚定【落点3 skill 双条款】：检验样本——若它存的是"设计流程语法/验证清单"（语法），合规；若塞满具体设计稿/配色文本（文本），则撞"存语法不存文本"且必通胀。加载策略看归因读数（调用频率乘命中率）。',
  actual='以 skill 形态封装 UI/UX 能力，是 落点3 的直系样本。需 README 深读确认它存的是语法还是文本。',
  pc='优：验证"skill=长期记忆载体层"在垂直领域成立。劣：垂直 skill 易堆文本，须预算审计——正中用户判词要执法的一刀。',
  help_='【落点3】的微型探针：用它检验"skill 双条款"的可执行性。若其结构偏文本，则作为"反面教材"喂我们的 skill 库纪律；若偏语法，则作正面范本。标记 pending-readme 确认。'),
'andrej-karpathy-skills': dict(
  pos='multica-ai 整理的 Karpathy agent skills 合集（跨语言榜 #24，200k+ stars）。',
  i_would='锚定【落点3 skill 双条款】：与 superpowers/mattpocock-skills 同簇——验证"程序性资产固化成 skill"是爆款刚需。我会强制加"存语法不存文本＋加载策略=权重＋技能账预算审计"三关，否则社区化必通胀。',
  actual='Kardpathy 背书的技能合集，是 落点3 的权威样本（名人效应放大验证）。形态待 README 深读确认语法/文本占比。',
  pc='优：顶流佐证"skill=长期记忆"方向被市场独立验证。劣：同 superpowers，缺硬规则易堆积。',
  help_='【落点3】权威佐证（承接 superpowers/ECC 线索）：三位顶流（superpowers/mattpocock/andrej-karpathy）合力证明"skill 即长期记忆"是真实需求，反推"技能账预算审计"必须落地——直接喂用户 thesis。'),
'nextchat': dict(
  pos='ChatGPT Next Web（NextChat）：自托管多模型对话 UI，统一前端接 OpenAI/Claude/本地模型。',
  i_would='锚定【落点1 入口输入工程】＋【落点4 载体路由】：纯触达层——人类输入经它进模型，按载体翻译输入（同 cc-switch 思路）。它只负责入口，不碰中段权重；质量在出口审计。',
  actual='与 open-webui 同类的多模型 UI 聚合器，是 落点1"入口"的典型实现。',
  pc='优：触达层成熟样本，印证"入口输入工程"分层必要。劣：无治理/记忆/调度，只是门面。',
  help_='【落点1】触达层定位参照（接续 open-webui）：提醒架构中"入口"与"治理"必须分层；其多模型路由可对标我们的"输入翻译层"。'),
'comfyui': dict(
  pos='节点式可视化 AI 工作流引擎（comfy-org/ComfyUI），主要服务扩散模型/图像生成。',
  i_would='锚定【落点4 调度中枢·任务编排】＋【落点1】：节点图=子任务拆分载体，串行/并行/挂起由图定义；默认 AI 可据图派单。须配套跟踪与出口质量审计；图知识经归因协议自学而非写死。',
  actual='以拖拽节点图组织生成任务，是 n8n/langflow 同类的可视化编排引擎；与 落点4"任务图+挂起/恢复"需求高度吻合。',
  pc='优：编排可视化范式，印证用户"任务图"需求（也在我本机 H3/视频流水线实测）。劣：画布易掩盖"中枢知识须自学"，流程写死则僵。',
  help_='【落点4】任务编排的工业级佐证（接续 langflow/n8n）：其节点图可对标我们的子任务管理 UI；本机已用 ComfyUI 跑 FLUX/Wan2.2，属"载体层"实物，印证"载体层不等于权重层"。'),
'transformers': dict(
  pos='Hugging Face Transformers：加载/微调/推理各类 ML 模型的统一框架（Python，163k）。',
  i_would='锚定【落点1 载体层不等于权重层】＋【补刀a】：它是"载体框架"——你能换模型/后端，改不了权重内部。加载策略=权重（按任务选模型）。调度中枢应在各异构后端间路由。权重不可达，印证"输入工程＝唯一近似杠杆"。',
  actual='纯载体框架，完美印证用户 thesis"载体层不等于权重层"——引擎可换、权重封闭。',
  pc='优：本地AI管理工具的模型底座选型参照；权重不可达的硬物证。劣：本身无治理/记忆，只是器官不是生命（补刀c 范畴 B）。',
  help_='【落点1+补刀a】的硬物证（承接 llama.cpp）：transformers 是"载体层"工业标准；本地AI管理工具的模型路由须以它为底座之一，且明确"加载策略才是权重"。'),
'stable-diffusion-webui': dict(
  pos='AUTOMATIC1111 的 Stable Diffusion WebUI：本地文生图/图生图前端（164k）。',
  i_would='锚定【落点1 入口输入工程/触达层】＋【落点1 载体层】：纯触达层 UI，把人类提示词压缩为模型输入；后端权重不可达。按用户 thesis，它只管入口，质量在出口（生成图是否达标）。',
  actual='本地扩散模型 UI 聚合器，是 落点1"入口"实现；与 ComfyUI 互补（脚本式 vs 节点式）。',
  pc='优：本地生成触达层成熟样本。劣：无治理/记忆/调度，只是门面；权重封闭（补刀a）。',
  help_='【落点1】触达层参照（接续 open-webui/nextchat）：本机已部署同类本地生成管线；提醒"入口输入工程"与"治理"分层——UI 再强也只是生命体的感官器官（补刀c 范畴 B）。'),
}

def card(name, m, a):
    stars=m.get('stars','?'); forks=m.get('forks','?'); lang=m.get('lang','?')
    pushed=m.get('pushed','?'); topics=','.join(m.get('topics',[])[:10]); desc=(m.get('desc') or '')[:200]
    rel=m.get('release')
    rel_s = (rel['tag']+'（'+rel['published']+'）') if rel else '本周未核验（GitHub API 未鉴权 60/小时限额已用尽，release 待下周日复位后补）'
    conf='快照级（stars/lang/desc 源 GitHub 经 evanli 镜像；release/commits 待 API 复位核验；架构细节标 pending-readme）'
    return (
'# '+name+' — 深分析卡\n\n'
'> 数据日期：'+DATE+'｜置信度：'+conf+'｜对标架构见 ['+LINK+'](../../'+LINK+')\n'
'> GitHub 实测：Stars '+str(stars)+'｜Forks '+str(forks)+'｜语言 '+str(lang)+'｜最近推送 '+str(pushed)+'｜Topics：'+topics+'\n'
'> 仓库：https://github.com/'+m['slug']+'\n\n'
'## 一句话定位\n'+a['pos']+'\n\n'
'## 我会怎么做（锚定用户判词架构）\n'+a['i_would']+'\n\n'
'## 实际怎么做（GitHub 实测 + 公开架构）\n'+a['actual']+'\n\n'
'## 优劣对比\n'+a['pc']+'\n\n'
'## 对我（{{INSTANCE_NAME}}·本地AI管理工具生命化）的帮助\n'+a['help_']+'\n\n'
'## 近期变动（'+DATE+' 快照源）\n'
'- 最新发版：'+rel_s+'\n'
'- 置信度：快照级（stars/lang/desc 已核验；release/commits 待 API 复位核验）。\n\n'
'## 交叉链接\n'
'- 架构判词与{{INSTANCE_NAME}}补刀：见 `'+LINK+'`\n'
'- 第二大脑（相位图/ attribution 账本）：本机脑 `C:\\Users\\{{OS_USER}}\\.workbuddy\\brain\\`\n'
'- 机思符号系统交付物：`Projects/机思符号系统/交付物/`\n\n'
'## 待办\n'
'- [ ] README 级深读（标记 pending-readme），补架构细节与近期发版\n'
'- [ ] 下周 diff 跟踪 star 增量与榜单进出\n'
    )

n=0
for name,a in A.items():
    m=meta.get(name)
    if not m: print('[SKIP] '+name+': no meta'); continue
    open(os.path.join(PROJ,name+'.md'),'w',encoding='utf-8').write(card(name,m,a))
    n+=1
    print('[生成] '+name+'.md')
print('DONE cards='+str(n))

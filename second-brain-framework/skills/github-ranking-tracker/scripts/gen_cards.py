# -*- coding: utf-8 -*-
import json, os

PROJ = "{{SHARED_WORKSPACE}}/{{KNOWLEDGE_BASE}}/github-ranking-tracker/projects"
meta = json.load(open(os.path.join(PROJ, "_gh_meta.json"), encoding="utf-8"))
DATE = "2026-08-03"
LINK = "Projects/机思符号系统/交付物/理论对接卡-本地AI管理工具架构判词与{{INSTANCE_NAME}}补刀.md"

def m(repo):
    d = meta.get(repo, {})
    return d

# ---- 1) 给 8 张旧卡追加"近期实测"段 ----
existing = {
 "openclaw/openclaw":"openclaw.md",
 "NousResearch/hermes-agent":"hermes-agent.md",
 "Significant-Gravitas/AutoGPT":"AutoGPT.md",
 "ollama/ollama":"ollama.md",
 "langgenius/dify":"dify.md",
 "n8n-io/n8n":"n8n.md",
 "langchain-ai/langchain":"langchain.md",
 "anthropics/claude-code":"claude-code.md",
}
for repo, fn in existing.items():
    d = m(repo)
    if "__err__" in d: continue
    sec = (f"\n\n## 近期实测（GitHub API {DATE}）\n"
           f"- Stars：{d.get('stargazers_count')}｜Forks：{d.get('forks_count')}｜语言：{d.get('language')}\n"
           f"- Open Issues：{d.get('open_issues_count')}｜创建：{d.get('created_at','')[:10]}｜最近推送：{d.get('pushed_at','')[:10]}\n"
           f"- Topics：{', '.join(d.get('topics',[])[:10])}\n"
           f"- 官方描述：{(d.get('description') or '')[:200]}\n"
           f"- 置信度：由\"描述级\"升级为\"实测元数据级\"（星标/活跃度已核验；架构细节仍待 README 级深读，标记 pending-readme）。\n")
    p = os.path.join(PROJ, fn)
    if os.path.isfile(p):
        open(p,"a",encoding="utf-8").write(sec)
        print(f"[追加] {fn}")

# ---- 2) 生成 12 张新高相关卡 ----
analyses = {
 "ultraworkers/claw-code": dict(
   name="claw-code", title="ultraworkers/claw-code",
   pos="Rust 编写的\"agent 托管博物馆展品\"，声明由 agent 在无人工干预下开发维护。",
   i_would="若我来造：把它定位为\"调度中枢\"管辖下的一个自治触达单元，仍受宪法层（时钟/账本/归因底账）约束——自治≠脱离审计。无人工干预可成立，但必须保留可追因日志，否则违反\"裁判与选手分离\"。",
   actual="实测为一场自治仓库 stunt（pushed 2026-06-26 已停更，37 open issues 极少）——更像是营销式\"AI 自管\"演示，而非可持续生命体。它跳过的是治理层，不是补全它。",
   pc="优：把\"无人工干预\"推到极致，是生命化直觉探针。劣：停更暴露\"无宪法层的自治=短暂表演\"；缺相位图/记忆传承，死亡即失忆。",
   help_="反向印证用户判词：治理脚手架≠生命。claw-code 只有\"触达层自治\"没有\"宪法层+记忆传承\"，故不能算生命——正好支撑范畴 B（工具是生命的器官，不是生命本身）。"),
 "obra/superpowers": dict(
   name="superpowers", title="obra/superpowers",
   pos="agentic 技能框架 + 软件开发方法论（Shell，265k stars，爆红）。",
   i_would="正合\"skill=长期记忆载体层\"：把高权重程序性资产（编译协议/验证流程/域分辨力）固化成 skill；加载策略=权重（高频进默认上下文、低频进检索层）；技能账过预算审计。",
   actual="以\"skills + subagent-driven-development\"组织 agent 能力，本质是体外固退库。它没有区分语法/文本——把事实也往 skill 塞就会折旧通胀，正是用户判词要执法的一刀。",
   pc="优：验证\"skill 即长期记忆\"在真实生态成立且刚需。劣：缺\"存语法不存文本\"的硬规则，易技能堆积。",
   help_="最强对标样本。建议把 superpowers 的 skill 组织方式映射进第二大脑子 skill 体系，并强制加\"技能账预算审计\"关卡——直接喂养用户 thesis。"),
 "affaan-m/ECC": dict(
   name="ECC", title="affaan-m/ECC",
   pos="\"agent harness 性能优化系统：Skills, instincts, memory, security, research-first\"，面向 Claude Code/Codex/OpenCode/Cursor 等（237k stars）。",
   i_would="这就是用户\"本地AI管理工具\"thesis 的孪生体：入口输入工程（instincts/memory）+ 出口审计（security）+ 调度（harness）。我会把 memory 做成相位图（载体×任务×输入→质量读数）而非知识库。",
   actual="把 skills/instincts/memory/security 打包成\"harness 优化层\"，跨多种 agent 宿主。它的\"memory\"若存的是文本而非归因对，会撞用户判词的\"记忆存文本\"警示。",
   pc="优：首次出现把\"技能+本能+记忆+安全\"统一为一个 harness 的商业级项目，证明用户架构方向被市场独立验证。劣：未公开其 memory 是知识库还是相位图，待 README 深读。",
   help_="最高价值对标。ECC 的\"harness 优化\"=用户\"调度中枢+输入工程\"；其成功说明\"管理工具生命化\"是真实需求而非空想。标记 pending-readme 深挖其 memory 形态。"),
 "mattpocock/skills": dict(
   name="mattpocock-skills", title="mattpocock/skills",
   pos="\"Skills for Real Engineers，来自 .agents 目录\"（Shell，199k stars）。",
   i_would="作为\"程序性资产库\"样本：每个 skill 应是编译协议/验证流程（语法），不是事实。加载策略按归因读数晋升。",
   actual="个人 .agents 目录的技能集合，偏实战工程技能。社区化后易变成\"技能堆积\"，需预算审计。",
   pc="优：草根验证\"工程师需要可复用 skill\"。劣：无加载策略/预算审计，规模上来必通胀。",
   help_="佐证\"技能账过预算审计\"的必要性；可作为第二大脑 skill 库的民间形态参考。"),
 "farion1231/cc-switch": dict(
   name="cc-switch", title="farion1231/cc-switch",
   pos="跨平台桌面 All-in-One 助手，统一 Claude Code / Codex / OpenCode / OpenClaw / Grok Build / Hermes Agent（Rust，123k）。",
   i_would="这正是\"调度中枢\"的载体路由岗位：把一句人类意图翻译成目标 agent 可编译域的索引语言（机思符号运行岗）。路由表须经归因协议自学，不是写死。",
   actual="做\"多 agent 切换/统一前端\"，是触达层聚合器。它解决\"哪个 agent 干哪活\"的路由，但路由质量是否过相位图复测未知。",
   pc="优：验证\"默认AI 按载体翻译输入\"是真实痛点。劣：若路由写死先验表而不自学，会撞用户\"中枢知识不能出厂写死\"一刀。",
   help_="调度中枢的现成样本——其\"统一多 agent 前端\"可抽象为我们的\"输入翻译层\"；路由表自学机制值得借鉴。"),
 "msitarzewski/agency-agents": dict(
   name="agency-agents", title="msitarzewski/agency-agents",
   pos="\"完整 AI 代理公司：每个 agent 是带人格/流程/交付物的专精专家\"（Shell，138k）。",
   i_would="\"共同体编译体最小实例\"的具象：多专精 agent 协作。关键是宪法层（账本/审计）在 agent 之外，且每个 agent 的路由过归因协议。",
   actual="以\"人格+流程+交付物\"组织 specialist agents，偏角色扮演式分工。缺显式治理/记忆传承设计。",
   pc="优：多 agent 分工直觉清晰。劣：人格化易掩盖\"无宪法层\"风险；记忆/归因对未建模。",
   help_="\"共同体编译体\"的生态佐证；提醒我们分工易、治理难——治理才是生命化门槛。"),
 "openai/symphony": dict(
   name="symphony", title="openai/symphony",
   pos="\"把项目工作变成隔离的自主实现运行，让团队管理工作而非监督编码 agent\"（Elixir，26k）。",
   i_would="纯粹的\"管理/调度中枢\"：人类退到管理位、agent 跑实现。必须配套出口审计（质量读数）与归因底账——否则管理盲飞。",
   actual="OpenAI 官方的 agent 编排/管理层，定位\"管 agent 而非监督 agent\"。是调度中枢的权威样本。",
   pc="优：大厂背书\"调度中枢\"范式。劣：Elixir 小众、生态未起；未公开审计/记忆机制。",
   help_="调度中枢的权威参照；验证\"运营权授予、宪法权禁授\"在商业产品也成立。"),
 "openai/codex": dict(
   name="codex", title="openai/codex",
   pos="\"终端运行的轻量编码 agent\"（Rust，103k）。",
   i_would="作为触达层的一个载体：受调度中枢派单、受出口审计。它的代码库上下文即机思符号索引协议的验证场。",
   actual="OpenAI 官方编码 agent，定位轻量终端工具。是\"输入工程=索引协议\"的最佳实测载体之一。",
   pc="优：官方加持、轻量。劣：闭源权重不可达（印证载体层≠权重层）；能力边界由 OpenAI 定。",
   help_="触达层载体样本；其代码上下文供给方式可对标我们的\"机思符号索引协议\"验证策略。"),
 "ggml-org/llama.cpp": dict(
   name="llama-cpp", title="ggml-org/llama.cpp",
   pos="C/C++ LLM 推理引擎（122k）。",
   i_would="作为\"载体层\"：权重不可达，引擎可换。调度中枢应按任务在 llama.cpp/各异构后端间路由，加载策略=权重。",
   actual="纯推理引擎，不碰权重。完美印证用户 thesis\"载体层≠权重层\"——你能换引擎，改不了模型内部。",
   pc="优：本地推理基石，验证载体可替换。劣：本身无治理/记忆，只是器官不是生命。",
   help_="\"载体层≠权重层\"的硬物证；本地AI管理工具的推理底座选型参照。"),
 "infiniflow/ragflow": dict(
   name="ragflow", title="infiniflow/ragflow",
   pos="RAG 引擎，融合 RAG 与 Agent，打造 LLM 的\"context layer\"（Go，86k；Topics 直写 context-engineering）。",
   i_would="\"记忆=相位图/检索层，不是知识库\"——RAGFlow 的 context layer 正是检索层实现；但它存的是文本块，须经归因协议升级为归因对才算相位图。",
   actual="把\"context engineering\"产品化，Topics 明示 context-engineering。是\"输入工程=索引协议\"的工程化样本。",
   pc="优：context-engineering 工业级落地，直证用户输入工程 thesis。劣：检索召回≠归因对，记忆形态仍偏文本。",
   help_="\"输入工程/索引协议\"与\"记忆=检索层\"双重佐证；其 context layer 可对标我们的相位图检索侧。"),
 "open-webui/open-webui": dict(
   name="open-webui", title="open-webui/open-webui",
   pos="用户友好 AI 界面，支持 Ollama/OpenAI API 等（Python，147k）。",
   i_would="纯触达层：人类输入经它进模型。按用户 thesis，它只负责入口输入工程，不碰中段权重；质量管理在出口审计。",
   actual="LLM 的 UI 聚合器，把多后端统一为人类可对话界面。是\"入口\"的典型实现。",
   pc="优：触达层成熟样本。劣：无治理/记忆/调度，只是门面。",
   help_="触达层定位参照；提醒我们工具架构中\"入口\"与\"治理\"要分层。"),
 "langflow-ai/langflow": dict(
   name="langflow", title="langflow-ai/langflow",
   pos="可视化构建/部署 AI agent 与工作流（Python，152k）。",
   i_would="\"任务编排=调度中枢一等能力\"：可视化任务图+串行/并行/挂起。其节点即子任务拆分载体，须配套跟踪与质量管理。",
   actual="以拖拽画布组织 agent/工作流，是 n8n/dify 同类的编排引擎。可视化降低编排门槛。",
   pc="优：编排可视化样本，印证用户\"任务图+挂起/恢复\"需求。劣：画布易掩盖\"中枢知识须自学\"，流程写死则僵。",
   help_="调度中枢\"任务编排\"能力的现成实现；其可视化范式可借鉴进我们的子任务管理 UI。"),
}

tpl = """# {title} — 深分析卡

> 数据日期：{DATE}｜置信度：{conf}｜对标架构见 [{LINK}](../../{LINK})
> GitHub 实测：Stars {stars}｜Forks {forks}｜语言 {lang}｜最近推送 {pushed}｜Topics：{topics}

## 一句话定位
{pos}

## 我会怎么做（锚定用户判词架构）
{i_would}

## 实际怎么做（实测 + 公开架构）
{actual}

## 优劣对比
{pc}

## 对我（{{INSTANCE_NAME}}·本地AI管理工具生命化）的帮助
{help_}

## 交叉链接
- 架构判词与{{INSTANCE_NAME}}补刀：见 `{LINK}`
- 第二大脑（相位图/ attribution 账本）：本机脑 `C:\\Users\\{{OS_USER}}\\.workbuddy\\brain\\`
- 机思符号系统交付物：`Projects/机思符号系统/交付物/`

## 待办
- [ ] README 级深读（标记 pending-readme），补架构细节与近期发版
- [ ] 下周 diff 跟踪 star 增量与榜单进出
"""

for repo, a in analyses.items():
    d = m(repo)
    stars = d.get('stargazers_count','?'); forks=d.get('forks_count','?')
    lang=d.get('language','?'); pushed=(d.get('pushed_at') or '')[:10]
    topics=", ".join(d.get('topics',[])[:10])
    conf = "实测元数据级（星标/活跃度已核验；架构 pending-readme）"
    text = tpl.format(title=a['title'], DATE=DATE, conf=conf, LINK=LINK,
        stars=stars, forks=forks, lang=lang, pushed=pushed, topics=topics,
        pos=a['pos'], i_would=a['i_would'], actual=a['actual'], pc=a['pc'], help_=a['help_'])
    p = os.path.join(PROJ, a['name']+".md")
    open(p,"w",encoding="utf-8").write(text)
    print(f"[生成] {a['name']}.md")
print("DONE cards")

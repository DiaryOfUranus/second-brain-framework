#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capability_briefing.py — 第二大脑·零学习自扫描能力简报器（v0.3.3 新增）

设计目标（对应评测短板「开箱即用 4.2 / 触发方式」）：
  用户**永远不需要读本框架的任何文档**。装了第二大脑的 AI 在首次唤醒（或用户
  问「你能做什么」）时运行本脚本，自扫描框架结构，产出一段可直接转述给用户的
  能力简报——这就是「第二大脑不用学」的机械落形：AI 替用户学，学完主动报告。

用法：
    python capability_briefing.py            # 人类可读简报（AI 直接转述）
    python capability_briefing.py --json     # 机读（供 AI 二次加工）
    python capability_briefing.py --root X   # 指定框架根目录（默认自动定位）

只依赖标准库；只读扫描，零配置，任何目录可跑。
"""
import argparse
import json
import os
import sys

# 组件 → (能力一句话[面向用户], 触发示范[用户可以直接这样说])
CAPABILITIES = {
    "SKILL.md": ("第二大脑总开关：五层协议与工程纪律的入口", "什么都不用说，正常给我派活即可"),
    "references/layer1-dialogue-management.md": ("对话级管理：每次任务自动走『加载-确认-执行-验收-沉淀』五步", "直接派活就行"),
    "references/layer2-project-management.md": ("项目管理：多步骤大任务自动切片、里程碑、中断恢复", "『帮我跟进这个项目』"),
    "references/layer3-knowledge-skill-management.md": ("自成长：发现重复劳动会自动结晶成可复用技能", "『这类活以后按固定流程做』"),
    "references/ai-division-governance.md": ("多模型编排：把不同难度的活分给性价比合适的模型，省成本", "『用便宜的模型把这事办了』"),
    "references/second-brain.md": ("跨会话持久记忆：决定、偏好、失败教训长期保留不丢", "『记住这个偏好』『上次我们聊到哪了』"),
    "references/engineering-axioms.md": ("工程公理约束：先列不能做什么、每步可验收，减少 AI 翻车", "自动生效，无需触发"),
    "references/theory-hindcast-empirics.md": ("理论实证：把抽象概念落成可测量指标做回测", "『给这套方案做实证检验』"),
    "references/tef-skill.md": ("超长文献提取：从几百页材料里抽取概念并形式化", "『读完这堆文档，帮我提炼 X』"),
    "references/mu-language-v2-ref.md": ("复合符号系统：长链推理的防漂移记法", "长任务自动启用"),
    "references/ai-native-symbol-system.md": ("复合符号系统（同上，详细手册）", "长任务自动启用"),
    "references/code-map.md": ("代码地图：陌生代码库一键生成导航视图", "『帮我摸清这个代码库』"),
    "references/upgrade-manager.md": ("版本演进管理：脑的升级可追溯、可交换、可回滚", "『把我的脑升级/导出』"),
    "references/loop-governance-dna.md": ("循环治理 DNA：自治执行的安全护栏", "自动生效"),
    "references/conversation-protocol.md": ("对话协议细节（五步流程展开）", "自动生效"),
    "references/skill-lifecycle.md": ("技能生命周期管理", "自动生效"),
    "scripts/ledger_writer.py": ("台账安全写入：写前四断言+写后自证，杜绝错插/重复/撞号", "自动生效 · AI 记台账时"),
    "scripts/extract_theory.py": ("文献脚本化提取：不灌全文、只读命中点", "『从这些论文里找关于 X 的论述』"),
    "scripts/capability_briefing.py": ("本简报：自扫描并报告能力", "『你能做什么？』"),
    "docs/quickstart.md": ("5 分钟上手指南（想看再看，不看也行）", "『怎么开始？』"),
    "docs/FAQ.md": ("常见问题速答", "『这是个啥？』"),
    "docs/避坑指南.md": ("反模式清单+故障自恢复表：出错时 AI 按它自愈", "出问题时 AI 自动查"),
    "docs/experimental.md": ("实验性功能与诚实边界说明", "进阶"),
    "docs/positioning.md": ("定位说明（与 PKM 等工具的区别）", "进阶"),
    "meta/brain_check.py": ("脑健康体检：结构/台账/过期/备份自动巡检，红黄绿灯", "自动生效"),
    "meta/run_all_selftests.py": ("机检单一入口：一条命令跑完全部自检", "自动生效"),
    "meta/brain_commit.py": ("一键提交：把脑的变更落进 Git", "自动生效"),
    "meta/export_second_brain.py": ("干净导出：把脑脱敏打包分享", "『把我的脑导出备份』"),
    "tools/scrub.py": ("脱敏检查：开源/分享前扫掉私人标识", "『我想开源/分享』"),
    "tools/assemble.py": ("脱敏打包组装", "同上"),
    "templates": ("实例化模板：建你自己的私人脑", "『帮我装一个』"),
}

GROUPS = [
    ("🧠 记忆与沉淀", ["跨会话", "持久记忆", "台账安全", "版本演进"]),
    ("🛡 纪律与治理", ("对话级管理", "项目管理", "工程公理", "循环治理", "对话协议", "健康体检", "机检单一入口", "一键提交")),
    ("🔧 加工与生成", ("自成长", "理论实证", "超长文献", "文献脚本化", "代码地图", "复合符号")),
    ("📦 分享与运维", ("干净导出", "脱敏", "组装", "实例化模板", "本简报", "5 分钟上手", "常见问题", "反模式", "总开关", "多模型编排", "实验性", "定位")),
]


def find_root(explicit):
    if explicit:
        return explicit
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (here, os.path.dirname(here), os.getcwd()):
        if os.path.isfile(os.path.join(cand, "SKILL.md")):
            return cand
    return None


def scan(root):
    found = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "__pycache__", "node_modules", ".build")]
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/")
            for key, (cap, trig) in CAPABILITIES.items():
                if key in ("templates",):
                    if rel.startswith("templates/"):
                        found.setdefault(key, (cap, trig))
                elif rel == key or rel.endswith("/" + key):
                    found.setdefault(key, (cap, trig))
    return found


def _group_for(name):
    for label, needles in GROUPS:
        for n in needles:
            if n in name:
                return label
    return "🧩 其他能力"


def brief(root, found):
    lines = ["【第二大脑已就绪 · 能力简报（AI 请把这段转述给用户）】", ""]
    grouped = {}
    for key, (cap, trig) in sorted(found.items()):
        grouped.setdefault(_group_for(cap), []).append((cap, trig))
    for label, _ in GROUPS:
        if label in grouped:
            lines.append(f"{label}")
            for cap, trig in grouped[label]:
                lines.append(f"  • {cap}（{trig}）")
            lines.append("")
    # 未识别组件：如实告知 AI 自读补报（不冒充已知）
    known_keys = set(CAPABILITIES)
    extras = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "__pycache__", "node_modules", ".build")]
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/")
            if not any(rel.endswith(k) or (k == "templates" and rel.startswith("templates/")) for k in known_keys):
                if rel.endswith((".md", ".py")):
                    extras.append(rel)
    if extras:
        lines.append(f"  • 另有 {len(extras)} 个组件未在简报表中：请 AI 自行阅读后向用户补充说明")
        lines.append("")
    lines.append("你只需要用自然语言说需求——何时读哪份文档、跑哪个脚本、怎么编排，")
    lines.append("全部由装了第二大脑的 AI 自动决定。你不用学它的任何内部机制。")
    return "\n".join(lines), extras


def main():
    ap = argparse.ArgumentParser(description="第二大脑·零学习自扫描能力简报")
    ap.add_argument("--root", default=None, help="框架根目录（含 SKILL.md）")
    ap.add_argument("--json", action="store_true", help="机读输出")
    a = ap.parse_args()
    root = find_root(a.root)
    if not root or not os.path.isfile(os.path.join(root, "SKILL.md")):
        print("【发生了什么】未找到 SKILL.md（不像是装好的第二大脑框架）。\n"
              "【下一步】请确认路径，或在框架目录里运行本脚本；\n"
              "【逃生口】也可用 --root 明确指定框架根目录。")
        sys.exit(2)
    found = scan(root)
    if a.json:
        text, extras = brief(root, found)
        print(json.dumps({"root": root, "components": len(found),
                          "unmapped": extras, "brief": text}, ensure_ascii=False, indent=2))
        return
    text, _ = brief(root, found)
    print(text)


if __name__ == "__main__":
    main()

---
name: theory-version-fracture-audit
description: 多版本理论 corpus 的概念断裂审计——当理论在版本迭代中丢失/泛化操作化定义、概念间断裂时，用脚本抽取概念登记 + 跨版本存在矩阵 + 逐项实读纠偏定位断裂。触发词：用户说"做概念断裂审计/版本迭代审计/检查版本丢失/对照多版找缺口"，或理论作者每次出新版本后要防止操作化回退。agent_created: true
---

# 理论版本断裂审计（Theory Version Fracture Audit）

## 一、何时用

- 用户持有一套**多版本理论 corpus**（如 `文明秩序演进理论` 的 1128/2.0/2.1/canonical 3.0 线），且指出"新版本丢了旧版操作化定义、概念泛化、概念间断裂"。
- 用户每次发布新理论版本后，要**防操作化回退**跑 diff。
- 要做某理论的**全量概念断裂审计**。

## 二、核心方法（5 步，已实测）

### 步骤 1｜清点版本文件
列出所有版本路径、编码、行数、体积，建立版本清单表。区分"基准操作化版本"（专项优化版，如 2.0 测 CS-5D、2.1 测物质基底、1128 重连贯）与"退化目标"（canonical 泛化版）。

### 步骤 2｜抽取概念登记
用脚本从每个版本抽取**章节标题**＋**定义/定理/公式/操作化锚点**（匹配模式：定义/定理/公式/＝/称之为/操作化/测量/代理指标/量化/阈值/量表/KPI）。
- 同时跑一个**自动发现的缩写采集器**（正则 `[A-Z]{2,8}` 连续大写）捕捉各版独有术语（注意会混入 HTML 残余词如 `nbsp/br` 与跨框架术语，步骤 4 清洗）。

### 步骤 3｜跨版本存在矩阵
维护一张 curated 候选概念表（来自审计经验，见 §四），对每版做"在场/缺失"布尔判定（子串匹配）。输出每概念 × 每版的矩阵，标记疑似 LOST（参考版有、目标版无）。

### 步骤 4｜逐项实读纠偏（最关键，不可省）
子串匹配**必有误报**，必须实读原文确认：
- **误报类型 A**：canon 实际含该概念但脚本因"整章拆分存储"漏检——先确认文件是单体还是按章拆分（`find … -name "*.md"` 数文件）。
- **误报类型 B**：候选词属**另一独立框架**（如 COD 秩序创造理论 vs 文明秩序主链），误报成"丢失的文明秩序测量项"。需实读确认归属。
- **误报类型 C**：候选词是**用户分析术语**（如 `能形基底/能量基底`），corpus 各版均无，非断裂，是待并入贡献词。
- **误报类型 D**：HTML 残余（nbsp/br/Authorization）混入自动发现缩写，清洗掉。

### 步骤 5｜落成审计 KB
输出：版本清单表 + 断裂清单（分级 A 结构性/B 降级/C 局部）+ 在场证明（纠正过度概括）+ 连带风险 + 修复路径（归作者-owned 版本迭代，AI 不擅改 canonical）。

## 三、可执行脚本（自包含核心）

将以下 Python 存为 `audit_concepts.py`，传入版本文件路径即可跑步骤 2–3：

```python
import os, re, sys

ANCHOR_PATTERNS = [r'^#+\s*.+', r'定义', r'定理', r'公式', r'＝', r'称之为',
                   r'操作化', r'测量指标', r'代理指标', r'量化', r'阈值',
                   r'量表', r'KPI', r'评分']
CURATED = ['PCE','CGT','CCE','ICM','ECO','OGP-I','OGP-E','OGP','CS-5D','SIM',
           'IMP','EPM','GAP','EOA','RPB','NOC','OCU','MPB*','SLA','ER','EROI',
           'CRM','ε','η','φ_distrib','Gini','RCRI']

def scan(path):
    hits = {c: [] for c in CURATED}
    found_anchors = 0
    with open(path, encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if any(re.search(p, line) for p in ANCHOR_PATTERNS):
                found_anchors += 1
            for c in CURATED:
                if re.search(r'(?<![A-Za-z])'+re.escape(c)+r'(?![A-Za-z])', line):
                    hits[c].append(i)
    return found_anchors, hits

def main():
    paths = sys.argv[1:]
    print(f"{'CONCEPT':<12}" + "".join(f"{os.path.basename(p)[:14]:>16}" for p in paths))
    matrix = {c: [] for c in CURATED}
    for p in paths:
        _, hits = scan(p)
        for c in CURATED:
            matrix[c].append('Y' if hits[c] else '·')
    for c in CURATED:
        row = "".join(f"{v:>16}" for v in matrix[c])
        # 标红：参考版有但最后一个(canonical)无
        print(f"{c:<12}{row}")
    print("\n提示：Y=在场 ·=缺失；最后列若为 · 而前面有 Y = 疑似断裂，须实读步骤4纠偏。")

if __name__ == '__main__':
    main()
```

用法：`python audit_concepts.py 1128.md 2.0.md 2.1.md canonical_成稿.md`

## 四、curated 候选概念（审计经验表，可扩展）

- **传承机制（A1 级，结构缺失）**：PCE 前序文明体 / CGT 基因传递 / CCE 嵌合体 / ICM 继承-批判 / ECO 欧洲基督教秩序体。
- **CS-5D 与物质基底（B 级降级）**：OGP-I/E、CS-5D、SIM、IMP、EPM、GAP、EOA、RPB、NOC、OCU、MPB*、SLA、ER、EROI。
- **COD 框架（A2 级，范围分工非丢失）**：GCRS、GCA-5D、OCU-HI、CGP、CLI、NEB、VNL、PAC、DGU、GA-LHF、IC-LHF、LNI。

## 五、关键纪律（必守，否则产出假断裂）

1. **canonical ≠ 完整权威**：迭代中常丢失早期版操作化并泛化定义。测量类查专项版（2.0/2.1）、传承/连贯查 1128、引用带**版本＋L 行号**。
2. **能形基底/能量基底 是 RPB/MPB\* 的口语别名**（作者表达习惯）：`能形基底`≈`RPB 资源-人口基底`（"支撑社会运转的所有资源总和"之操作化对应）、`能量基底`≈`MPB* 物质许可边界`（"可被技术顶高的扩张杠杆"之操作化对应）。corpus 各版无此二词但**有对应操作化概念**——**非新概念、非断裂**，勿误报为缺漏；引用时定位 RPB/MPB\*（带版本＋L）。
3. **COD 层缺于 canon 是范围分工**（canon 第0章"W-COD 回写·待回补"显式标注），**非意外丢失**，报告时严禁误述成"丢失"。
4. **禁反向覆盖**：用户离线备份（如 `{{THEORY_SOURCE}}`）只读不写；修复正文回补属作者-owned 版本迭代，AI 仅建候选补丁（新建增量版、不改写原版）。
5. **纠正过度概括**：脚本显示"22/25 子构造仍在场"时，结论应为"局部断裂"而非"整体塌方"。
6. **COET（文明秩序演进理论）版本断裂须联动应用栈**：做 COET 版本断裂审计时，并行参照 `civilization-order-country-analysis` 的 **乙5 版本断裂纪律**——baseline＝**1128 ＋ 编译论 V7**（非简化泛化的 v3.1 正式稿，否则会把"版本迭代内容丢失"误判为"框架本体盲区"）；canonical（v3.1）/ `{{THEORY_SOURCE}}` 各版**全程只读**；判某机制"缺失"前**先追跨章指针**（如 Ch1 §1.4 文明八维 → V7 §1.7），二阶误判（未追指针）比版本断裂更前置。COET 的 **v3.21** 是派生扩展版（保护带扩展：多层级共同体 / 元基因非唯一 / AS 方案 A ＋ 方法论澄清·倾向vs表现四层），**非 canonical**；进 canonical 须走 COET 成卷管线、由用户拍板。

## 六、输出物

- `理论概念断裂审计_全量_<日期>.md`（分级断裂＋在场证明＋修复路径）
- 如需回补：新建 `理论_操作化回补增量版_v0.1_<日期>.md`（汇集各补丁、标注来源版＋L、不改写原版）

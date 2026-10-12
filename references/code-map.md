# 代码地图常驻 μ 视图（code-map）· 子 Skill 使用手册

> **本文件是第二大脑（second-brain）受管子 Skill 之一**，由总管在「代码库理解 / 导航 / 常驻地图」类任务中按需加载。
> 它不是独立工具，是第二大脑 index / v0 μ 哲学在代码库上的工程落地——把全量源码压成**静态充分统计量 μ**（CODE_MAP.md），让 agent 不必全量读码即可定位改动点，补 agent 默认只看到光标处文件、缺全局观的洞（易局部改坏全局）。
>
> **源真相在 brain/meta**：本手册只描述调用与边界，提取器 / 落盘脚本以 `~/.workbuddy/brain/meta/` 下文件为准（不重复造）。

---

## 一、何时启用本子 Skill（甜区与诚实边界）

### ✅ 甜区
1. 进入陌生 / 大型代码库前，先生成导航地图（补 agent 只看到光标处、缺全局观的洞）。
2. 要「代码变更即重算」的常驻 μ 视图（根治「地图过期」——比没有地图更危险的坑）。
3. 需要模块职责 / 依赖 / 覆盖率的**确定性摘要**（非 LLM、可重现、可版本化）。

### ⚠️ 非优势 / 边界（诚实标注）
- 调用链是**静态 import 图，非运行时真实链路**（动态分派 / DI / 反射不覆盖）——生态通病，未假装解决。
- 其他语言（js / ts / go / rs / java / rb / c / cpp / bash）是**正则结构嗅探**（给 import / export / def 名，非语义），不保证全覆盖装饰器糖 / 宏。
- 不自动做 LLM 语义合成（「为何存在 / 业务边界」），避免非确定性污染确定性工程层；语义层是可叠加选项，默认关。

## 二、实现（已落位，源真相在 brain/meta）
- `~/.workbuddy/brain/meta/code_map.py` — 提取器：`build_map(repo) -> dict`，生成目录树(截断) + 模块清单 + 外部依赖 Top。Python 用 stdlib `ast` **精确**；其他语言正则降级。**不调 LLM、纯确定性可重现**。
- `~/.workbuddy/brain/meta/update_code_map.py <repo> [--no-commit]` — 落盘 `brain/code-maps/<repo>/CODE_MAP.md`（常驻、可版本化、跨 Session 持久）+ 自动 git add / commit brain。
- `~/.workbuddy/brain/meta/hooks/post-commit-code-map` — 可装目标仓库，commit 即重算（同构 self-model 常驻压缩，根治过期）。

## 三、用法
```bash
python ~/.workbuddy/brain/meta/update_code_map.py <仓库路径>                # 生成并落盘 brain
python ~/.workbuddy/brain/meta/update_code_map.py <仓库路径> --no-commit    # 仅生成
# 装常驻重算（目标仓库 commit 即更新地图）：
cp ~/.workbuddy/brain/meta/hooks/post-commit-code-map <目标仓库>/.git/hooks/post-commit
chmod +x <目标仓库>/.git/hooks/post-commit
# ⚠️ 若目标仓库已有 post-commit，请把逻辑并入而非覆盖
```

## 四、与基座耦合
- 本子 Skill = 代码库的**编译期静态 μ**（v0 μ 哲学：确定性工程层提供「不能出错的结构认知」）。
- 地图 tracked（持久脑视图），用时即重算；非 gitignored 中间产物。
- EVALUATION 元结论：地图 = μ 视图，融入基座而非复刻独立「项目地图」轮子。

## 五、来源说明
本子 Skill 原为独立用户级 skill（`~/.workbuddy/skills/code-map`），已并入第二大脑成为受管子 Skill；其全部内容随本次整合归入 `references/code-map.md`，不再单独注册。原 standalone 备份于 `~/.workbuddy/_skill_backup/code-map-20260730`。

# 5 分钟上手（Quickstart）

> 目标：从空目录到一个能跑的「私人第二大脑」最小实例。读完约 5 分钟，操作后约 5 分钟。

## 你会得到什么

一个**本地 Git 仓库**作为你的「脑」：里面是结构化记忆文件（脑图、自我模型、台账、错题本），配合几个**零依赖 Python 脚本**（只用标准库，无需 `pip install`）做健康检查、自动提交、脱敏导出。全程不联网、不上传。

## 前置条件

- **Python 3.8+**：脚本只用标准库，不需要安装任何第三方包。
- **Git**：用来让「大脑的演进」可 diff / 可回滚。
- **一个本地目录**：默认 `~/.workbuddy/brain`，也可任意路径（用 `SB_BRAIN` 环境变量覆盖）。

## 步骤 1：把框架复制为你的脑

```bash
# 从 GitHub 克隆（或把本仓库目录复制一份）
git clone https://github.com/DiaryOfUranus/second-brain-framework.git ~/.workbuddy/brain
cd ~/.workbuddy/brain

# 初始化为你的私人脑仓库（本仓库自带的 .git 历史可保留或丢弃，不影响使用）
git init && git add -A && git commit -m "init my second brain"
```

> 你克隆到的这份是「框架 + 治理工具」的纯净版，不含任何私人数据，可放心作为起点。

## 步骤 2：用模板建出状态文件

模板里所有私人字段都是 `{{占位符}}`，**按本机实际情况填写，不要照搬示例值**——这正是本框架的「实例化守卫」纪律：结构可复制，内容必须你亲手写。

```bash
cp templates/index.md index.md
cp templates/self-model.md self-model.md
cp templates/ledger.md ledger.md
cp templates/MEMORY.md MEMORY.md
cp templates/failures.md failures.md
cp templates/VERSION.json VERSION.json
cp templates/CHANGELOG.md CHANGELOG.md
mkdir -p base kb projects sessions audits patterns tmp inbox
cp templates/base/骨架.md base/骨架.md   # 把 {{理论名}} 换成你自己的基座名（或留空）
```

打开 `index.md` 和 `self-model.md`，把里面的 `{{...}}` 占位符换成你的真实信息（名字、职业、脑的用途）。这一步就是「实例化」。

## 步骤 3：装上自动健康检查钩子

```bash
cp meta/hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

装好后，**每次 `git commit` 会自动跑 `meta/brain_check.py`**（六检查项：结构完整性 / 台账违规 / 过期条目 / 日志间隙 / 备份新鲜度 / 脱脑演练），用红黄绿灯告诉你哪里不对。它只报检、不阻塞提交。

## 步骤 4：跑一次健康检查，认识红黄绿灯

```bash
python meta/brain_check.py
```

第一次跑大概率会亮几个**黄灯**（比如还没填日志、备份目录未配置）——这是正常的。
**黄灯 = 提示，红灯 = 必须处理**。重点是：你现在有了一个会「体检」的脑。

## 步骤 5：体验一次完整日常循环

假设你在一次对话里做了一个决定「下周开始用第二大脑管理读书笔记」：

1. **开场声明**（可选但推荐）：在对话开头写一句「第二大脑 已启动｜脑图已读｜台账活跃 N 条」。
2. **工作**：正常做事。
3. **收尾**：把这条决定写进 `ledger.md` 或 `MEMORY.md`，然后：
   ```bash
   python meta/brain_commit.py   # 把脑的变更提交进 Git
   ```
4. 下次对话，先读 `index.md` 就能立刻想起「上周决定做读书笔记管理」——**记忆跨会话延续了**。

## 环境变量（可选）

| 变量 | 默认 | 含义 |
|---|---|---|
| `SB_BRAIN` | 脚本位置推导 | 脑仓库根目录 |
| `SB_EXPORT_DIR` | 未设（跳过副本检查） | 导出副本目录，用于「备份新鲜度」检查 |
| `SB_PACKAGE` | `second-brain` | 导出包名 |
| `SB_PUB_DIR` | `~/second-brain-export` | 导出输出目录 |

## 下一步

- 想系统了解五层协议与治理纪律 → 读 `skill/SKILL.md`（较长，按需下潜）
- 想把自己的脑**安全脱敏后开源/分享** → 看 `tools/scrub.py` + `tools/assemble.py`，先跑 `python tools/assemble.py --check-only` 自检有无残留私人标识
- 想导出给别的工具用 → `python meta/export_second_brain.py`
- 常见问题与踩坑 → [docs/FAQ.md](FAQ.md)

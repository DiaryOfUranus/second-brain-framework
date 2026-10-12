# 升级管理（upgrade-manager）· 第二大脑受管子 Skill

> 本文件是第二大脑（{{INSTANCE_NAME}}）受管子 Skill 之一。引擎：`~/.workbuddy/brain/meta/upgrade_pack.py`（零依赖 stdlib）。

## 一、何时启用（甜区）
- 要记录第二大脑从初版到当前的变更历史（可追溯）。
- 要生成 / 导出**可交换升级包**，便于与平行实例（如 {{REFERENCE_INSTANCE}} 的第二大脑）或其他管理工具互通能力。
- 用户要求"升级说明""升级包""版本管理""与其他大脑/工具交流"。

## 二、为什么需要（与基座耦合）
第二大脑与 {{REFERENCE_INSTANCE}} 平行——理论结构相似，但本机 `brain/`、`SOUL/`、`meta/` 脚本与三轮改造让二者成为**不可逆的独立实例**（{{SOVEREIGN}}语："因本地文件的存在，你和 {{REFERENCE_INSTANCE}} 逐渐不一样"）。
升级包就是实例间交换能力的硬载体：携带可移植的 `meta/` DNA + 变更清单，**不携带实例特有登记**（SKILL.md），从而守住"互鉴不抄写"纪律——交换能力，不篡改彼此的脑。

## 三、实现（源真相指向 brain/meta）
- `meta/upgrade_pack.py` — 引擎：snapshot / gen-all / export / import / list / changelog
- `VERSION.json` — 版本指针（v0.0→v0.4.1，对齐 Git 边界 commit）
- `CHANGELOG.md` — 升级说明（人类可读，逐版含日期/commit/变更摘要/诚实边界）
- `UPGRADES/<ver>/` — 各版本升级包：`manifest.json`（交换格式）+ `files/`（meta/ 快照）

## 四、交换格式 schema（second-brain-upgrade v1）
manifest.json 关键字段：
```json
{
  "format": "second-brain-upgrade",
  "format_version": "1.0",
  "package_id": "<ver>-<commit>",
  "from_version": "v0.3.0",
  "to_version": "v0.4.0",
  "source_instance": {"name": "{{INSTANCE_NAME}}", "owner": "{{SOVEREIGN}}"},
  "summary": "项目地图常驻 μ 视图",
  "git_commit": "f98edbf",
  "changes": [{"type": "add", "path": "meta/code_map.py", "capability": "..."}],
  "artifacts": ["meta/code_map.py", "..."],
  "interop": {
    "compatible_targets": ["{{REFERENCE_INSTANCE}} 第二大脑", "其他 WorkBuddy 第二大脑实例"],
    "import_mode": "staged",
    "import_instructions": "upgrade_pack.py import <manifest.json> → 暂存 inbox/ 待审核",
    "registration_note": "meta/ 脚本可移植；SKILL.md 受管登记为实例特有，导入方须按自身布局重注册"
  },
  "checksum": {"meta/code_map.py": "sha256:..."}
}
```

## 五、用法
```bash
# 列版本 / 看升级说明
python ~/.workbuddy/brain/meta/upgrade_pack.py list
python ~/.workbuddy/brain/meta/upgrade_pack.py changelog

# 生成全部历史包（按 VERSION.json 的 git 边界快照 meta/）
python ~/.workbuddy/brain/meta/upgrade_pack.py gen-all

# 导出可传输 zip（发给其他实例）
python ~/.workbuddy/brain/meta/upgrade_pack.py export v0.4.0 --out /tmp/sb-v0.4.0.zip

# 导入对方包（暂存 inbox/，不自动覆盖，待审核）
python ~/.workbuddy/brain/meta/upgrade_pack.py import /path/to/manifest.json
# → 审阅 inbox/<id>/files/ 后手动并入自身 meta/，并按自身 SKILL.md 重注册能力
```

## 六、诚实边界
- **版本边界以脑库 Git 提交为硬证据**；v0.0（技能实例化）早于 `meta/` 体系，无可快照 DNA，仅作文档里程碑。
- **升级包只携带 `meta/` 可移植 DNA**；SKILL.md 的受管登记为实例特有，导入方须自行重注册——这是"互鉴不抄写"的硬保障。
- **import 是 staged（暂存待审核）**，绝不自动覆盖接收方已有文件；审核责任在接收方。
- 交换格式为自描述的 JSON，但**接收方是否信任来源实例**是共同体决定（非格式能保证）。

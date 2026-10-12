# slidep / tencent-pptx 执行指南（PPT 生成 + 讲解词）

> 本文件是 `neixin-trainer-method` 技能的执行层：把 Layer A 的课程设计（3.0 骨架）变成干净 PPTX，
> 并加上演讲者备注。记录生产环境实测过的失败模式与正确写法。

---

## A. 技术栈与入口

- **slidep / tencent-pptx**：将 `pages/*.jsx`（受限 JSX DSL）编译为 OOXML `.pptx`。
  组件：`<Slide>` `<Box>`(仅 flex，禁止 grid/calc) `<Text>`(文本节点内用 `<span>` 改样式)
  `<svg>` `<FAIcon>`(必须 fill) `<Table>`(cells 为二维数组)。无 `import/export`，文件末表达式须为 `<Slide>`。
- **画布**：1280×720；A/B/C 三区母版（标题 0–120 / 内容 120–660 / 页脚 660–720）。
- **tencent-local-office-edit**（editor_sdk）：本地 Office 实时编辑，用于给已生成的 pptx 加备注等。

---

## B. slidep 守护进程启动（关键坑）

slidep 以守护进程运行，监听 `pages/` 变化并增量编译进目标 `.pptx`。

- 启动器在 node 版本根目录（**不是** `bin/`）：`…/node/versions/22.22.2/slidep-start.cmd`。
- **必须用 PowerShell 调 `*.cmd` 启动器**（`.cmd` 用 `%dp0%` 原生 Windows 路径）。
  ❌ 禁止在 Git Bash 里直接 `node.exe …/slidep-start.js`——MSYS 会给 `$HOME` 前置 `/c`，
  报 `MODULE_NOT_FOUND`（`c:\c\Users\…`）。
- 命令（PowerShell）：
  ```powershell
  & "{{WORKBUDDY_HOME}}\binaries\node\versions\22.22.2\slidep-start.cmd" `
     --project "C:\path\to\pptx" --filename "输出.pptx"
  ```
- 重启前先 `slidep-stop.cmd`。日志/状态在 `<project>/.slidep/logs.log` 与 `state.json`
  （`revisionId` 条数 = 已编译页数）。
- 单页语法校验：`slidep-validate.cmd <file.jsx> --project <dir>`，输出
  `{"success":true,"status":"ready"}` 即通过。reconcile 失败时**只报第一个出错页**，需逐页
  validate 其余页定位全部错误。

---

## C. SWC JSX 解析器必知（生产实测失败模式）

slidep 用 SWC 解析 JSX；以下写法会报 `Syntax Error` / `Expression expected` 并导致整批编译中止：

1. **SVG `d` 属性含 JS 表达式必须包 `{}`**
   - ❌ `<path d='M240,' + (b.y+48) + '…' />`（字符串字面量后接 `+` 运算符，非法）
   - ✅ `<path d={'M240,' + (b.y+48) + '…'} />`
2. **JSX 文本节点禁止裸特殊符号** `→` `≥` `<`：
   - ❌ `<Text>客户 ≥ 业务</Text>`、`<Text>a < b</Text>`
   - ✅ 用 HTML 实体 `&gt;` `&lt;` `&gt;=`（`&gt;`/`&lt;` 在 JSX 文本节点**可用**，已验证编译通过）。
     或把符号放进 JS 字符串字面量再 `{…}` 包裹。
   - 注：单独圈码①②③④⑤⑥⑦⑧、`「」`、中文标点等 Unicode 文本**安全**，可直写。
3. `<Text>` 内改样式用 `<span style={{…}}>…</span>`，不要给 `<Text>` 嵌套非 span 结构。
4. `Box` 只支持 flex 布局；`width:'calc(50% - 6px)'` 在 slidep 允许，但 grid/`calc` 复杂表达式慎用。
5. `FAIcon` 必须提供 `fill` 与 `width`/`height`。

---

## D. 加演讲者备注（讲解词）

已生成 pptx 后，用 `tencent-local-office-edit` 的 `slide_add_notes` 逐页写入。

- **路由**：本地 pptx 编辑走 `tencent-docs-routing` → `tencent-local-office-edit`。
- **file_id 来源**：用 `get_pool_status` 按文件路径匹配已打开实例的真实 `file_id`
  （形如 `sid_xxx`）。⚠️ Tencent Docs 预览注入的 `file_id` GUID 与 editor_sdk 的 `sid_xxx` 是两套，
  **不能直接混用**——必须用 `get_pool_status` 拿到的。
- **page_index 为 0 基**：0→第1页 … 20→第21页。顺序与 slidep 插入顺序一致。
- **工具**：`slide_add_notes`（创建备注页，notes 不存在时用）；若已存在须用 `slide_set_notes_text`
  （替换全文）。`slide_append_notes_text` 会重置字符级样式，仅保留纯文本+语言标签。
- 讲解词结构见 `assets/notes-template.md`（【勾】【讲】【练】【化】）。每页 90–170 字为宜。
- 写完后 `save_file`（省略 file_path 覆盖原文件）。
- 校验：`slide_get_notes_text file_id=… page_index=N` 返回 `{"ok":true,"text":"…"}`。
- 解包核验：`ppt/notesSlides/notesSlideN.xml` 数量 = 页数，zip 合法。

---

## E. 推荐产物结构

```
<project>/pptx/
  STORY.md            # 课程叙事 / 21页大纲（用 assets/story-template.md）
  DESIGN.md           # 设计系统（用 assets/design-template.md）
  pages/slide_01_*.jsx … slide_21_*.jsx
  输出.pptx
```

---

## F. 已验证的配色（{{EMPLOYER}}金融主题示例）

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| 主色 primary | `#1E40AF` | 标题、页眉色条、主色块、节点主线 |
| 辅色 secondary | `#0EA5E9` | 卡片底、第二系列、分隔线 |
| 强调 accent | `#DC2626` | 「立即办理」CTA、合规红线、关键警示 |
| 文本 | `#1E293B` / `#64748B` | 主文 / 次要 |
| 背景 | `#FFFFFF` / `#F1F5F9` | 页面 / 浅底块 |

字体：`'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif`。所有 L1/L2 视觉用内联 `<svg>`
绘制，不依赖外部图片素材。

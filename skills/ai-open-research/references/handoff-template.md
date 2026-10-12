# HANDOFF — <日期>
> 这是跨上下文连续性的充分统计量（μ）。下次会话只读本文件 + question-graph，不重读全部历史。
> 对应 oh-my-cli 的"会话可重放 / Session Replay"思想。

## frontier（开放问题 + 为何重要）
- [Q-id] <问题> — 重要因：<它卡住了哪个更高层 claim / 它分裂出了什么>
- ...

## deltas（本次会话变化）
- 新增问题：<Q-id 列表，增殖来源>
- 状态推进：<Q-id: open→claimed 等>
- 降级/剪枝：<Q-id: claimed→challenged / closed 及原因>
- 新 claim（带归因对）：<Q-id → (证据指针, 结论, 置信)>

## next-leases（下次接手哪几个，限 1–3）
- [Q-id] <为何先租它>
- ...

## 收敛度量快照
- 开放数:__（趋势：上次__ → 本次__，净增/净减__）
- claimed 数:__ 跨链接数:__ 剪枝死路数:__
- 判读：<本次是否增加确定性 / 是否剪掉分支 / 是否发散失控>

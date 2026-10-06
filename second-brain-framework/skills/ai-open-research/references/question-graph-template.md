# QUESTION GRAPH — <主题>
> 节点=问题/假设；回答一个会 spawn 子问题（增殖正常）
> 状态机：open → investigating → evidenced → claimed → challenged → (closed | reopened)
> 每条 claimed 必须带归因对：(问题 × 证据源指针 × 结论 × 置信度 × 复测次数)

## open（待租赁，P1 每次只 lease 1–3 个）
- [Q1] open | <问题表述> | 父Q:— | 证据:— | 结论:— | 置信:— | 复测:0

## investigating（已租赁，探究中）
- [Q2] investigating | <问题> | 父Q:Q1 | 证据:<指针> | 结论:— | 置信:— | 复测:0

## evidenced（有证据未达 claimed）
- [Q3] evidenced | <问题> | 父Q:Q1 | 证据:<指针列表> | 结论:<初步> | 置信:0.5 | 复测:1

## claimed（已达置信阈值，带归因对）
- [Q4] claimed | <问题> | 父Q:Q2 | 证据:<指针> | 结论:<断言> | 置信:0.85 | 复测:2

## challenged（被反证/无法复现）
- [Q5] challenged | <问题> | 父Q:Q4 | 证据:<反证指针> | 结论:原 claimed 降级 | 置信:0.3 | 复测:1

## closed（合并入更高层 claim / 剪枝死路）
- [Q6] closed | <问题> | 父Q:— | 证据:<合并目标 Q-id> | 结论:并入 Q4 | 置信:— | 复测:—

## 统计快照（每次 handoff 更新）
- 开放数:__ 探究中:__ evidenced:__ claimed:__ challenged:__ closed:__
- 跨链接数:__ 剪枝死路数:__

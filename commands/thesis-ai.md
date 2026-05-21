---
name: thesis-ai
description: 仅降AI检测率 — 针对AI高风险段落执行优化
---

# /thesis-ai

仅执行降AI检测率优化，不处理查重和润色。

## 前置条件

必须先执行 `/thesis-init` 初始化项目。

## 执行流程

1. 读取 `thesis_overview.md` 中标记的AI高风险段落
2. 询问用户优化范围：
   - 全文优化
   - 仅高风险段落
   - 指定章节
3. 调用 `agents/ai_reduction_agent.md` 执行优化
4. 生成修订日志
5. 更新章节任务文档状态

## 可选参数

- `--chapter N` — 仅优化第N章
- `--level high` — 仅优化高风险段落（默认）
- `--level all` — 优化所有风险等级的段落

## 输出文件

- 章节任务文档更新
- `revision_log_ai.md` — AI优化修订日志

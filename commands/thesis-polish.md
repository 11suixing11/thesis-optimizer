---
name: thesis-polish
description: 仅学术润色 — 提升表达精准度、学术规范性、可读性
---

# /thesis-polish

仅执行学术润色优化。

## 前置条件

必须先执行 `/thesis-init` 初始化项目。

## 执行流程

1. 询问用户润色范围：
   - 全文润色
   - 指定章节
2. 询问润色重点：
   - 表达精准化
   - 学术规范性
   - 可读性优化
   - 全部（默认）
3. 调用 `agents/polishing_agent.md` 执行润色
4. 生成修订日志
5. 更新章节任务文档状态

## 可选参数

- `--chapter N` — 仅润色第N章
- `--focus precision` — 仅关注表达精准化
- `--focus规范` — 仅关注学术规范性
- `--focus readability` — 仅关注可读性

## 输出文件

- 章节任务文档更新
- `revision_log_polish.md` — 润色修订日志

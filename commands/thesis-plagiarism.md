---
name: thesis-plagiarism
description: 仅降查重率 — 针对查重高风险段落执行深度语义改写
---

# /thesis-plagiarism

仅执行降查重率优化。

## 前置条件

必须先执行 `/thesis-init` 初始化项目。

## 执行流程

1. 读取 `thesis_overview.md` 中标记的查重高风险段落
2. 询问用户优化范围：
   - 全文优化
   - 仅高风险段落
   - 指定章节
3. 调用 `agents/plagiarism_agent.md` 执行改写
4. 生成修订日志
5. 更新章节任务文档状态

## 可选参数

- `--chapter N` — 仅优化第N章
- `--level high` — 仅优化高风险段落（默认）
- `--level all` — 优化所有风险等级的段落

## 输出文件

- 章节任务文档更新
- `revision_log_plagiarism.md` — 查重优化修订日志

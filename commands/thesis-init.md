---
name: thesis-init
description: 初始化论文优化项目 — 分析论文结构，生成总揽文档
---

# /thesis-init

初始化论文优化项目。读取用户提供的论文文件，进行全面分析，生成项目总揽文档。

## 执行流程

1. 询问用户以下信息：
   - 论文文件路径（支持 .tex 和 .md 格式）
   - 目标学科（计算机科学 / 电子工程 / 机械工程 / 通用）
   - 目标院校（可选，用于格式规范检查）
   - 引用格式（IEEE / GB/T 7714 / APA）

2. 加载对应的学科画像：`references/discipline_profiles/[学科]_profile.md`

3. 调用 `agents/analyzer_agent.md` 对论文进行全面扫描

4. 生成 `thesis_overview.md` 总揽文档，包含：
   - 论文基本信息
   - 章节结构
   - 风险评估结果
   - 优化计划和优先级

5. 为每个章节生成 `chapter_[XX]_[名称].md` 任务文档

6. 向用户报告初始化结果，确认是否开始优化

## 输出文件

- `thesis_overview.md` — 总揽文档
- `chapter_01_*.md` 到 `chapter_N_*.md` — 各章节任务文档

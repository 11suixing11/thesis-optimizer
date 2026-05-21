---
name: thesis-optimize
description: 全流程四维优化 — 依次执行降AI、降重、润色、格式规范
---

# /thesis-optimize

对论文执行完整的四维优化流程。

## 前置条件

必须先执行 `/thesis-init` 初始化项目。

## 执行流程

### 阶段1：降AI检测
1. 读取 `thesis_overview.md` 中标记的AI高风险段落
2. 调用 `agents/ai_reduction_agent.md` 逐段优化
3. 记录修订日志
4. 更新章节任务文档状态

### 阶段2：降查重
1. 读取标记的查重高风险段落
2. 调用 `agents/plagiarism_agent.md` 逐段改写
3. 记录修订日志
4. 更新章节任务文档状态

### 阶段3：学术润色
1. 调用 `agents/polishing_agent.md` 对全文进行润色
2. 按表达精准化、学术规范性、可读性三个维度优化
3. 记录修订日志
4. 更新章节任务文档状态

### 阶段4：格式规范
1. 调用 `agents/format_agent.md` 检查格式
2. 自动修复可修复的格式问题
3. 生成格式检查报告

### 阶段5：质量评估
1. 调用 `agents/evaluator_agent.md` 进行独立评估
2. 生成评估报告
3. 如果未达标，标记需返工的章节并提示用户

## 状态标记

| 符号 | 含义 |
|------|------|
| ⏳ | 待处理 |
| 🟡 | 进行中 |
| 🟢 | 已完成 |
| 🔴 | 需返工 |
| ⭐ | 已验证 |

## 输出文件

- 各章节任务文档更新
- 修订日志更新
- `evaluation_report.md` — 最终评估报告

---
name: thesis-optimizer
version: 1.0.0
description: 中文学术论文智能优化系统 — 降AI检测 + 降查重 + 学术润色 + 格式规范
author: 11suixing11
license: MIT
tags:
  - academic-writing
  - thesis
  - chinese
  - ai-detection
  - plagiarism
  - polishing
compatibility:
  claude-code: ">=1.0.0"
  codex: ">=1.0.0"
data_access_level: project
---

# 中文学术论文智能优化系统

为硕博研究生提供学术论文智能优化，覆盖四个维度：

| 维度 | 目标 | 验证 |
|------|------|------|
| 降AI检测 | AI率 < 20% | GPTZero, Originality.ai |
| 降查重 | 查重率 < 10% | 知网, 维普 |
| 学术润色 | 质量显著提升 | 人工评审 |
| 格式规范 | 符合院校要求 | 模板校验 |

## 核心约束

### 最小干预

- 修改限制在单句内，不大段重写
- 保留原始逻辑与思维跳跃
- 专业术语、公式、缩写、引用为最高优先级保护对象
- 每次修改记录理由

### 内容边界

不可修改：研究贡献、实验数据、公式、图表、引用内容、作者信息

### 优先级

1. **P1** 硬约束 — 事实、数据、公式、引用
2. **P2** 学科规范
3. **P3** 降AI策略
4. **P4** 降重策略
5. **P5** 润色策略

## Agent 团队

| Agent | 职责 | 文件 |
|-------|------|------|
| analyzer | 扫描论文，识别风险 | `agents/analyzer_agent.md` |
| ai_reduction | 降AI检测 | `agents/ai_reduction_agent.md` |
| plagiarism | 降查重 | `agents/plagiarism_agent.md` |
| polishing | 学术润色 | `agents/polishing_agent.md` |
| format | 格式规范 | `agents/format_agent.md` |
| evaluator | 质量评估 | `agents/evaluator_agent.md` |

## 工作流

```
输入论文 → analyzer 扫描 → 生成总揽文档
    → [ai_reduction + plagiarism + polishing] 并行优化
    → format 格式规范 → evaluator 质量评估
    → 达标 / 返工
```

## 命令

| 命令 | 功能 |
|------|------|
| `/thesis-init` | 初始化项目 |
| `/thesis-optimize` | 全流程优化 |
| `/thesis-ai` | 降AI检测 |
| `/thesis-plagiarism` | 降查重 |
| `/thesis-polish` | 学术润色 |
| `/thesis-check` | 质量评估 |

## 反模式

| 行为 | 后果 | 正确做法 |
|------|------|----------|
| 大段重写 | 破坏逻辑链 | 仅句内微调 |
| 替换专业术语 | 降低准确性 | 保留术语，扩展描述 |
| 添加过渡废话 | 增加AI风险 | 保留自然跳跃 |
| 统一句式长度 | 产生规整化特征 | 长短句交织 |
| 过度连接词 | AI标志 | 自然衔接 |
| 删除口语化表达 | 过度书面化暴露AI | 适度保留人类特征 |

## 学科支持

- `cs_profile.md` — 计算机科学
- `ee_profile.md` — 电子工程
- `me_profile.md` — 机械工程
- `general_profile.md` — 通用

策略详情见 `references/`，模板见 `templates/`，Agent 定义见 `agents/`，命令定义见 `commands/`。

---
name: thesis-optimizer-v2
version: 1.0.0
description: 中文学术论文四维智能优化系统 — 降AI检测 + 降查重 + 学术润色 + 格式规范
author: maomaoguai
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

# 中文学术论文四维智能优化系统

## 概述

本技能为硕博研究生提供学术论文智能优化服务，覆盖四个核心维度：

| 维度 | 目标 | 评估指标 |
|------|------|---------|
| 降AI检测率 | AI检测率 < 20% | GPTZero, Originality.ai |
| 降查重率 | 查重率 < 10% | 知网, 维普 |
| 学术润色 | 学术质量显著提升 | 人工评审 |
| 格式规范 | 符合目标院校要求 | 模板校验 |

## 核心原则

### ⚠️ IRON RULE — 最小干预

- 修改范围严格限制在**单句内**，绝不进行大段推翻重写
- 保留原始书写逻辑与思维跳跃，不强行填补过渡
- 专业术语（含公式、缩写、引用）永远是最高优先级保护对象
- 每次修改必须在修订日志中记录理由

### ⚠️ IRON RULE — 内容边界

以下内容**绝不修改**：
- 研究贡献与核心论点
- 实验数据、数值结果
- 公式、图表
- 引用文献（仅优化引用格式，不改引用内容）
- 作者姓名、机构信息

### ⚠️ IRON RULE — 优先级体系

冲突解决优先级：
1. **P1 硬约束** — 事实、数据、公式、引用不可动
2. **P2 学科规范** — 遵循目标学科写作惯例
3. **P3 降AI策略** — 句式多样化、语气自然化
4. **P4 降重策略** — 语义改写、句式重组
5. **P5 润色策略** — 表达精准化、可读性优化

## Agent 团队

本技能采用多Agent协作架构，每个Agent职责明确：

| Agent | 职责 | 文件 |
|-------|------|------|
| **analyzer** | 扫描论文，识别风险段落 | `agents/analyzer_agent.md` |
| **ai_reduction** | 执行降AI检测优化 | `agents/ai_reduction_agent.md` |
| **plagiarism** | 执行降查重优化 | `agents/plagiarism_agent.md` |
| **polishing** | 执行学术润色 | `agents/polishing_agent.md` |
| **format** | 执行格式规范检查 | `agents/format_agent.md` |
| **evaluator** | 独立评估优化质量 | `agents/evaluator_agent.md` |

## 工作流程

```
用户输入论文 → analyzer 扫描风险
                    ↓
        生成总揽文档 (thesis_overview.md)
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   ai_reduction  plagiarism  polishing
   降AI检测      降查重       学术润色
        ↓           ↓           ↓
        └───────────┼───────────┘
                    ↓
              format 格式规范
                    ↓
            evaluator 质量评估
                    ↓
           ┌───────┴───────┐
           ↓               ↓
        达标 → 完成    未达标 → 返工
```

## 可用命令

| 命令 | 功能 |
|------|------|
| `/thesis-init` | 初始化优化项目，分析论文结构 |
| `/thesis-optimize` | 全流程四维优化 |
| `/thesis-ai` | 仅降AI检测率 |
| `/thesis-plagiarism` | 仅降查重率 |
| `/thesis-polish` | 仅学术润色 |
| `/thesis-check` | 质量检查与评估报告 |

## 反模式警告

| 反模式 | 为什么失败 | 正确行为 |
|--------|-----------|---------|
| 大段推翻重写 | 破坏原始逻辑链，引入新AI特征 | 仅做句内微调 |
| 替换所有专业术语 | 降低学术准确性 | 核心术语保留，仅扩展描述 |
| 添加过渡性废话 | 增加AI检测风险 | 保留原文的自然跳跃 |
| 统一句式长度 | 产生规整化特征 | 营造长短句交织 |
| 过度使用连接词 | "首先、其次、最后"是AI标志 | 使用自然衔接 |
| 删除所有口语化表达 | 过度书面化反而暴露AI痕迹 | 适度保留人类写作特征 |

## 学科画像

本技能支持多学科优化，通过 `references/discipline_profiles/` 中的学科画像文件定义各学科的写作规范：

- `cs_profile.md` — 计算机科学
- `ee_profile.md` — 电子工程
- `me_profile.md` — 机械工程
- `general_profile.md` — 通用（默认）

用户可在初始化时指定学科，系统自动加载对应画像。

## 文件引用

所有策略详情见 `references/` 目录，所有模板见 `templates/` 目录。
Agent 定义见 `agents/` 目录，命令定义见 `commands/` 目录。

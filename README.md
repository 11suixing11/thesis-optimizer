<div align="center">

# Thesis Optimizer

**中文学术论文智能优化系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Codex-lightgrey.svg)]()

面向硕博研究生的学术论文多维智能优化 Agent Skill

[快速开始](#快速开始) · [功能特性](#功能特性) · [系统架构](#系统架构) · [使用指南](#使用指南)

</div>

---

## 功能特性

<table>
<tr>
<td width="50%">

### AI 检测降痕
消除 AI 写作痕迹，通过 GPTZero / Originality.ai 检测
- 句式重组与多样化
- 打破规整化结构
- 语气自然化处理

</td>
<td width="50%">

### 查重降重
深度语义改写，查重率降至 10% 以下
- 同义替换与句式重组
- 引用规范化处理
- 专业术语完整保留

</td>
</tr>
<tr>
<td>

### 学术润色
提升表达精准度与学术规范性
- 量化模糊表述
- 术语一致性检查
- 可读性优化

</td>
<td>

### 格式规范
符合目标院校与学科要求
- 多学科画像支持
- 文档结构检查
- 引用格式统一

</td>
</tr>
</table>

## 系统架构

```
论文输入
   │
   ▼
┌─────────────────────────────────────────────────────────┐
│  analyzer          全文扫描 → 风险识别 → 总揽文档        │
└─────────────────────────────────────────────────────────┘
   │
   ▼
┌──────────────┬──────────────┬──────────────┐
│ ai_reduction │  plagiarism  │   polishing  │
│   降AI检测   │    降查重    │    学术润色   │
└──────────────┴──────────────┴──────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────┐
│  format            格式检查 → 自动修复                   │
└─────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────┐
│  evaluator         独立评估 → 质量报告                   │
│  (含反逢迎机制，不因用户期望降低标准)                     │
└─────────────────────────────────────────────────────────┘
   │
   ▼
  达标 ✓ / 返工 ↺
```

## Agent 团队

| Agent | 职责 | 核心能力 |
|:------|:-----|:---------|
| `analyzer` | 论文分析 | 全文扫描，识别 AI 高风险、查重风险、格式问题 |
| `ai_reduction` | 降 AI 检测 | 句内重组、打破规整化、语气自然化 |
| `plagiarism` | 降查重 | 深度语义改写、引用规范化、术语处理 |
| `polishing` | 学术润色 | 表达精准化、学术规范性、可读性优化 |
| `format` | 格式规范 | 多学科画像加载、文档结构检查 |
| `evaluator` | 质量评估 | 四维评分、反逢迎机制、独立判定 |

## 快速开始

### 安装

```bash
# Claude Code
git clone https://github.com/11suixing11/thesis-optimizer.git ~/.claude/skills/thesis-optimizer

# Codex
git clone https://github.com/11suixing11/thesis-optimizer.git ~/.codex/skills/thesis-optimizer
```

### 使用

```bash
# 1. 在论文目录启动 Agent
cd /path/to/your/thesis

# 2. 初始化项目
/thesis-init

# 3. 执行全流程优化
/thesis-optimize

# 4. 查看评估报告
/thesis-check
```

## 可用命令

| 命令 | 功能 | 参数 |
|:-----|:-----|:-----|
| `/thesis-init` | 初始化项目 | 论文路径、学科、引用格式 |
| `/thesis-optimize` | 全流程优化 | — |
| `/thesis-ai` | 仅降 AI | `--chapter N`, `--level high\|all` |
| `/thesis-plagiarism` | 仅降重 | `--chapter N`, `--level high\|all` |
| `/thesis-polish` | 仅润色 | `--chapter N`, `--focus precision\|readability` |
| `/thesis-check` | 质量检查 | `--quick`, `--full`, `--chapter N` |

## 评分体系

| 等级 | 分数 | 判定 |
|::---:|:----:|:-----|
| **A** | ≥ 85 | 达标，可提交 |
| **B** | 70-84 | 基本达标，建议微调 |
| **C** | 55-69 | 未达标，需返工 |
| **D** | < 55 | 严重不达标，需大幅返工 |

## 设计约束

本系统遵循三条不可违反的铁律：

**最小干预** — 修改范围严格限制在单句内，不大段推翻重写，保留原始逻辑与思维跳跃

**内容边界** — 研究贡献、实验数据、公式、图表、引用文献、作者信息绝不修改

**优先级体系** — 事实/数据 > 学科规范 > 降 AI > 降重 > 润色

## 适用范围

- **用户** — 硕博研究生
- **格式** — LaTeX (.tex) / Markdown (.md)
- **语言** — 中文论文
- **学科** — 计算机科学、电子工程、机械工程、通用

## Python 工具

```bash
# 文本统计（句长标准差、TTR）
python scripts/text_stats.py <file>

# AI 高频词扫描
python scripts/ai_vocab_checker.py <file>

# 改写对比报告
python scripts/diff_viewer.py <original> <revised>
```

## 许可证

[MIT License](LICENSE)

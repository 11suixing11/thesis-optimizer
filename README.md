# Thesis Optimizer V2 — 中文学术论文四维智能优化系统

> 面向硕博研究生的学术论文智能优化 Agent Skill 套件

## 核心功能

| 维度 | 目标 | 评估指标 |
|------|------|---------|
| 降AI检测率 | AI检测率 < 20% | GPTZero, Originality.ai |
| 降查重率 | 查重率 < 10% | 知网, 维普 |
| 学术润色 | 学术质量显著提升 | 人工评审 |
| 格式规范 | 符合目标院校要求 | 模板校验 |

## 架构设计

### 多Agent协作

| Agent | 职责 |
|-------|------|
| **analyzer** | 扫描论文，识别风险段落 |
| **ai_reduction** | 执行降AI检测优化 |
| **plagiarism** | 执行降查重优化 |
| **polishing** | 执行学术润色 |
| **format** | 执行格式规范检查 |
| **evaluator** | 独立评估优化质量 |

### 项目结构

```
thesis-optimizer-v2/
├── SKILL.md                          # 技能入口定义
├── README.md                         # 项目文档
├── USAGE_GUIDE.md                    # 使用指南
├── agents/                           # 6个Agent定义
│   ├── analyzer_agent.md
│   ├── ai_reduction_agent.md
│   ├── plagiarism_agent.md
│   ├── polishing_agent.md
│   ├── format_agent.md
│   └── evaluator_agent.md
├── commands/                         # 6个Slash命令
│   ├── thesis-init.md
│   ├── thesis-optimize.md
│   ├── thesis-ai.md
│   ├── thesis-plagiarism.md
│   ├── thesis-polish.md
│   └── thesis-check.md
├── templates/                        # 文档模板
│   ├── master_overview_template.md
│   ├── chapter_task_template.md
│   └── revision_log_template.md
├── references/                       # 策略知识库
│   ├── ai_pattern_taxonomy.md
│   ├── ai_vocabulary_blacklist.md
│   ├── perplexity_burstiness.md
│   ├── strategy_ai_reduction.md
│   ├── strategy_plagiarism.md
│   ├── strategy_polishing.md
│   ├── evaluation_criteria.md
│   └── discipline_profiles/          # 学科画像
│       ├── cs_profile.md
│       ├── ee_profile.md
│       ├── me_profile.md
│       └── general_profile.md
├── shared/                           # 共享资源
│   ├── contracts/
│   └── schemas/
├── scripts/                          # Python辅助脚本
│   ├── text_stats.py
│   ├── ai_vocab_checker.py
│   └── diff_viewer.py
├── hooks/                            # 生命周期钩子
│   └── hooks.json
└── tests/                            # 测试
    └── fixtures/
        └── sample_thesis.md
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

## 安装方式

### Claude Code

```bash
# 克隆到 skills 目录
git clone <repo-url> ~/.claude/skills/thesis-optimizer-v2
```

### Codex

```bash
# 克隆到 skills 目录
git clone <repo-url> ~/.codex/skills/thesis-optimizer-v2
```

### 其他Agent

```bash
# 克隆到通用 skills 目录
git clone <repo-url> ~/.agent/skills/thesis-optimizer-v2
```

## 快速开始

1. 安装技能到对应Agent的skills目录
2. 在论文项目目录中启动Agent
3. 执行 `/thesis-init` 初始化项目
4. 执行 `/thesis-optimize` 开始全流程优化
5. 执行 `/thesis-check` 查看评估报告

## 适用范围

- **目标用户**：硕博研究生
- **论文格式**：LaTeX (.tex) 和 Markdown (.md)
- **语言**：中文论文（英文支持计划中）
- **学科**：计算机科学、电子工程、机械工程、通用

## 核心设计原则

### ⚠️ IRON RULE — 最小干预

- 修改范围严格限制在单句内
- 绝不大段推翻重写
- 保留原始逻辑和思维跳跃
- 专业术语永远保护原文

### ⚠️ IRON RULE — 内容边界

以下内容绝不修改：
- 研究贡献与核心论点
- 实验数据、数值结果
- 公式、图表
- 引用文献
- 作者姓名、机构信息

### ⚠️ IRON RULE — 优先级体系

冲突解决优先级：
1. P1 硬约束 — 事实、数据、公式、引用不可动
2. P2 学科规范 — 遵循目标学科写作惯例
3. P3 降AI策略 — 句式多样化、语气自然化
4. P4 降重策略 — 语义改写、句式重组
5. P5 润色策略 — 表达精准化、可读性优化

## 许可证

MIT License

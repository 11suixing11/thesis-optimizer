# Thesis Optimizer — 中文学术论文智能优化系统

> 面向硕博研究生的学术论文多维智能优化 Agent Skill

## 核心能力

| 优化维度 | 目标 | 验证方式 |
|----------|------|----------|
| AI检测降痕 | AI检测率 < 20% | GPTZero / Originality.ai |
| 查重降重 | 查重率 < 10% | 知网 / 维普 |
| 学术润色 | 表达质量显著提升 | 人工评审 |
| 格式规范 | 符合院校要求 | 模板校验 |

## 系统架构

采用多 Agent 协作架构，各 Agent 职责独立、互相制约：

```
论文输入 → [analyzer] 风险扫描
                ↓
        生成总揽文档
                ↓
     ┌──────────┼──────────┐
     ↓          ↓          ↓
 [ai_reduction] [plagiarism] [polishing]
  降AI检测      降查重       学术润色
     ↓          ↓          ↓
     └──────────┼──────────┘
                ↓
          [format] 格式规范
                ↓
        [evaluator] 质量评估
                ↓
         达标 → 完成
         未达标 → 返工
```

## Agent 列表

| Agent | 职责 |
|-------|------|
| analyzer | 全文扫描，识别风险段落 |
| ai_reduction | 消除AI写作痕迹 |
| plagiarism | 深度语义改写降重 |
| polishing | 学术表达润色 |
| format | 格式规范检查 |
| evaluator | 独立质量评估（含反逢迎机制） |

## 可用命令

| 命令 | 功能 |
|------|------|
| `/thesis-init` | 初始化项目，分析论文结构 |
| `/thesis-optimize` | 全流程四维优化 |
| `/thesis-ai` | 仅降AI检测率 |
| `/thesis-plagiarism` | 仅降查重率 |
| `/thesis-polish` | 仅学术润色 |
| `/thesis-check` | 质量检查与评估报告 |

## 项目结构

```
├── SKILL.md                  # 技能入口
├── README.md                 # 项目文档
├── USAGE_GUIDE.md            # 使用指南
├── agents/                   # Agent 定义
├── commands/                 # 命令定义
├── templates/                # 文档模板
├── references/               # 策略知识库
│   └── discipline_profiles/  # 学科画像
├── shared/                   # 共享资源
├── scripts/                  # Python 辅助工具
├── hooks/                    # 生命周期钩子
└── tests/                    # 测试
```

## 安装

```bash
# Claude Code
git clone <repo-url> ~/.claude/skills/thesis-optimizer

# Codex
git clone <repo-url> ~/.codex/skills/thesis-optimizer
```

## 快速开始

1. 安装技能到 Agent 的 skills 目录
2. 在论文项目目录中启动 Agent
3. 执行 `/thesis-init` 初始化
4. 执行 `/thesis-optimize` 开始优化
5. 执行 `/thesis-check` 查看评估报告

## 适用范围

- **用户**：硕博研究生
- **格式**：LaTeX (.tex) / Markdown (.md)
- **语言**：中文论文
- **学科**：计算机科学、电子工程、机械工程、通用

## 设计约束

### 最小干预原则

- 修改范围严格限制在单句内
- 不大段推翻重写
- 保留原始逻辑和思维跳跃
- 专业术语始终保护原文

### 内容边界

以下内容绝不修改：研究贡献、实验数据、公式、图表、引用文献、作者信息

### 优先级体系

1. P1 — 事实、数据、公式、引用不可动
2. P2 — 学科写作规范
3. P3 — 降AI策略
4. P4 — 降重策略
5. P5 — 润色策略

## 许可证

MIT License

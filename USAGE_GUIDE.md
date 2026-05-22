# 使用指南

## 快速开始

### 1. 安装

```bash
git clone <repo-url> ~/.claude/skills/thesis-optimizer
```

### 2. 初始化

在论文目录启动 Agent，执行：

```
/thesis-init
```

系统会询问：论文路径、学科、目标院校、引用格式。

### 3. 优化

```
/thesis-optimize
```

自动执行：降AI → 降重 → 润色 → 格式 → 评估。

### 4. 查看报告

```
/thesis-check
```

## 命令详解

### /thesis-init

| 参数 | 说明 | 必填 |
|------|------|------|
| 论文路径 | .tex 或 .md | 是 |
| 学科 | CS / EE / ME / 通用 | 是 |
| 目标院校 | 格式检查用 | 否 |
| 引用格式 | IEEE / GB/T 7714 / APA | 是 |

输出：`thesis_overview.md` + 各章节任务文档。

### /thesis-optimize

按顺序执行五个阶段，使用状态标记追踪进度：

| 标记 | 含义 |
|------|------|
| ⏳ | 待处理 |
| 🟡 | 进行中 |
| 🟢 | 已完成 |
| 🔴 | 需返工 |

### /thesis-ai — 仅降AI

- `--chapter N` — 指定章节
- `--level high` — 仅高风险（默认）
- `--level all` — 全部

### /thesis-plagiarism — 仅降重

参数同 `/thesis-ai`。

### /thesis-polish — 仅润色

- `--chapter N` — 指定章节
- `--focus precision` — 表达精准化
- `--focus readability` — 可读性

### /thesis-check — 质量检查

- `--quick` — 快速检查
- `--full` — 完整检查（默认）
- `--chapter N` — 指定章节

评分体系：

| 分数 | 等级 | 判定 |
|------|------|------|
| ≥ 85 | A | 达标 |
| 70-84 | B | 建议微调 |
| 55-69 | C | 需返工 |
| < 55 | D | 需大幅返工 |

## Python 工具

```bash
# 文本统计
python scripts/text_stats.py <file> [--format json|text]

# AI高频词扫描
python scripts/ai_vocab_checker.py <file> [--format json|text]

# 改写对比
python scripts/diff_viewer.py <original> <revised> [--format markdown|html]
```

## 常见问题

**支持什么格式？** LaTeX (.tex) 和 Markdown (.md)。

**支持什么学科？** CS、EE、ME、通用，可扩展。

**优化要多久？** 硕士论文约 2-4 小时，单章 20-40 分钟。

**会改核心内容吗？** 不会。仅优化表达，不改研究贡献、数据、公式、引用。

**怎么验证效果？** 用 `/thesis-check`，建议用外部工具二次验证。

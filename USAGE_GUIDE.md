# 使用指南

## 目录

1. [快速开始](#快速开始)
2. [初始化项目](#初始化项目)
3. [全流程优化](#全流程优化)
4. [单项优化](#单项优化)
5. [质量检查](#质量检查)
6. [Python工具](#python工具)
7. [常见问题](#常见问题)

## 快速开始

### 第一步：安装技能

将本项目克隆到Agent的skills目录：

```bash
# Claude Code
git clone <repo-url> ~/.claude/skills/thesis-optimizer-v2

# Codex
git clone <repo-url> ~/.codex/skills/thesis-optimizer-v2
```

### 第二步：启动Agent

在你的论文项目目录中启动Agent（Claude Code / Codex 等）。

### 第三步：初始化项目

```
/thesis-init
```

系统会询问：
- 论文文件路径（.tex 或 .md）
- 目标学科（计算机科学 / 电子工程 / 机械工程 / 通用）
- 目标院校（可选）
- 引用格式（IEEE / GB/T 7714 / APA）

### 第四步：开始优化

```
/thesis-optimize
```

系统会自动执行：
1. 降AI检测
2. 降查重
3. 学术润色
4. 格式规范
5. 质量评估

### 第五步：查看报告

```
/thesis-check
```

## 初始化项目

### 命令

```
/thesis-init
```

### 参数

| 参数 | 说明 | 必填 |
|------|------|------|
| 论文文件路径 | .tex 或 .md 文件 | 是 |
| 目标学科 | 计算机科学 / 电子工程 / 机械工程 / 通用 | 是 |
| 目标院校 | 用于格式规范检查 | 否 |
| 引用格式 | IEEE / GB/T 7714 / APA | 是 |

### 输出文件

- `thesis_overview.md` — 总揽文档
- `chapter_01_*.md` 到 `chapter_N_*.md` — 各章节任务文档

## 全流程优化

### 命令

```
/thesis-optimize
```

### 执行流程

```
阶段1：降AI检测 → 阶段2：降查重 → 阶段3：学术润色 → 阶段4：格式规范 → 阶段5：质量评估
```

### 状态标记

| 符号 | 含义 |
|------|------|
| ⏳ | 待处理 |
| 🟡 | 进行中 |
| 🟢 | 已完成 |
| 🔴 | 需返工 |
| ⭐ | 已验证 |

## 单项优化

### 仅降AI检测

```
/thesis-ai
```

可选参数：
- `--chapter N` — 仅优化第N章
- `--level high` — 仅优化高风险段落（默认）
- `--level all` — 优化所有风险等级的段落

### 仅降查重

```
/thesis-plagiarism
```

可选参数：
- `--chapter N` — 仅优化第N章
- `--level high` — 仅优化高风险段落（默认）
- `--level all` — 优化所有风险等级的段落

### 仅学术润色

```
/thesis-polish
```

可选参数：
- `--chapter N` — 仅润色第N章
- `--focus precision` — 仅关注表达精准化
- `--focus规范` — 仅关注学术规范性
- `--focus readability` — 仅关注可读性

## 质量检查

### 命令

```
/thesis-check
```

### 可选参数

- `--quick` — 快速检查，仅评估高风险段落
- `--full` — 完整检查，评估全文（默认）
- `--chapter N` — 仅检查第N章

### 评分体系

| 总分 | 等级 | 判定 |
|------|------|------|
| ≥ 85 | A | 达标，可提交 |
| 70-84 | B | 基本达标，建议微调 |
| 55-69 | C | 未达标，需返工 |
| < 55 | D | 严重不达标，需大幅返工 |

## Python工具

### 文本统计工具

计算句长标准差、TTR（词汇丰富度）等指标。

```bash
python scripts/text_stats.py <file_path> [--format json|text]
```

示例：
```bash
python scripts/text_stats.py thesis.tex
python scripts/text_stats.py thesis.tex --format json
```

### AI高频词扫描工具

扫描文本中的AI高频词汇并标记风险等级。

```bash
python scripts/ai_vocab_checker.py <file_path> [--format json|text]
```

示例：
```bash
python scripts/ai_vocab_checker.py chapter_01.md
python scripts/ai_vocab_checker.py chapter_01.md --format json
```

### 改写对比生成工具

生成优化前后的可视化对比报告。

```bash
python scripts/diff_viewer.py <original_file> <revised_file> [--format markdown|html]
```

示例：
```bash
python scripts/diff_viewer.py original.tex revised.tex
python scripts/diff_viewer.py original.tex revised.tex --format html > diff_report.html
```

## 常见问题

### Q: 支持哪些文件格式？

A: 目前支持 LaTeX (.tex) 和 Markdown (.md) 格式。Word (.docx) 支持计划中。

### Q: 支持哪些学科？

A: 目前支持计算机科学、电子工程、机械工程和通用学科。可通过添加学科画像扩展。

### Q: 优化需要多长时间？

A: 硕士论文约2-4小时，单章节约20-40分钟，取决于论文长度和问题严重程度。

### Q: 会修改论文的核心内容吗？

A: 不会。本技能严格遵循"最小干预"原则，仅优化表达方式，不修改研究贡献、实验数据、公式、图表、引用文献。

### Q: 如何验证优化效果？

A: 使用 `/thesis-check` 命令进行独立质量评估。建议使用外部工具（GPTZero、知网等）进行二次验证。

### Q: 如果优化效果不达标怎么办？

A: 系统会标记需返工的章节并给出具体建议。可使用 `/thesis-ai`、`/thesis-plagiarism`、`/thesis-polish` 针对性优化。

### Q: 如何添加新的学科画像？

A: 在 `references/discipline_profiles/` 目录下创建新的画像文件，参考现有画像的格式。

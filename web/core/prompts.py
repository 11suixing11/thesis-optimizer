"""Agent prompt 加载器 — 从 agents/ 和 references/ 目录加载 prompt"""

import re
from pathlib import Path


# 项目根目录（web/ 的上级）
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _read_md(path: Path) -> str:
    """读取 markdown 文件，去除 YAML frontmatter"""
    text = path.read_text(encoding="utf-8")
    # 去除 frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    return text.strip()


def _read_full_md(path: Path) -> str:
    """读取 markdown 文件，保留 frontmatter"""
    return path.read_text(encoding="utf-8").strip()


def load_agent_prompt(agent_name: str) -> str:
    """加载指定 agent 的 prompt"""
    path = PROJECT_ROOT / "agents" / f"{agent_name}_agent.md"
    if not path.exists():
        raise FileNotFoundError(f"Agent prompt not found: {path}")
    return _read_md(path)


def load_reference(name: str) -> str:
    """加载参考文档"""
    path = PROJECT_ROOT / "references" / f"{name}.md"
    if not path.exists():
        return ""
    return _read_md(path)


def load_discipline_profile(discipline: str) -> str:
    """加载学科画像"""
    profile_map = {
        "cs": "cs_profile",
        "ee": "ee_profile",
        "me": "me_profile",
        "general": "general_profile",
    }
    filename = profile_map.get(discipline, "general_profile")
    path = PROJECT_ROOT / "references" / "discipline_profiles" / f"{filename}.md"
    if not path.exists():
        return ""
    return _read_md(path)


def get_analyzer_system_prompt(discipline: str) -> str:
    """构建 analyzer agent 的完整 system prompt"""
    agent = load_agent_prompt("analyzer")
    profile = load_discipline_profile(discipline)
    taxonomy = load_reference("ai_pattern_taxonomy")
    blacklist = load_reference("ai_vocabulary_blacklist")

    return f"""{agent}

## 学科画像

{profile}

## AI 写作模式分类

{taxonomy}

## AI 高频词汇参考

{blacklist}"""


def get_ai_reduction_system_prompt() -> str:
    """构建 ai_reduction agent 的完整 system prompt"""
    agent = load_agent_prompt("ai_reduction")
    strategy = load_reference("strategy_ai_reduction")
    return f"""{agent}

## 详细策略

{strategy}"""


def get_plagiarism_system_prompt() -> str:
    """构建 plagiarism agent 的完整 system prompt"""
    agent = load_agent_prompt("plagiarism")
    strategy = load_reference("strategy_plagiarism")
    return f"""{agent}

## 详细策略

{strategy}"""


def get_polishing_system_prompt() -> str:
    """构建 polishing agent 的完整 system prompt"""
    agent = load_agent_prompt("polishing")
    strategy = load_reference("strategy_polishing")
    return f"""{agent}

## 详细策略

{strategy}"""


def get_format_system_prompt(discipline: str) -> str:
    """构建 format agent 的完整 system prompt"""
    agent = load_agent_prompt("format")
    profile = load_discipline_profile(discipline)
    return f"""{agent}

## 学科画像

{profile}"""


def get_evaluator_system_prompt() -> str:
    """构建 evaluator agent 的完整 system prompt"""
    agent = load_agent_prompt("evaluator")
    criteria = load_reference("evaluation_criteria")
    return f"""{agent}

## 评估标准

{criteria}"""

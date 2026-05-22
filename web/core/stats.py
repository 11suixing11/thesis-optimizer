"""统计函数封装 — 从 scripts/ 目录复用"""

import sys
from pathlib import Path

# 将项目根目录加入 path 以导入 scripts
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from text_stats import analyze_text as text_stats_analyze
from ai_vocab_checker import analyze_text as vocab_analyze


def get_text_stats(text: str) -> dict:
    """获取文本统计信息"""
    return text_stats_analyze(text)


def get_vocab_stats(text: str) -> dict:
    """获取 AI 高频词统计"""
    return vocab_analyze(text)


def get_combined_stats(text: str) -> dict:
    """获取综合统计信息"""
    text_result = text_stats_analyze(text)
    vocab_result = vocab_analyze(text)

    return {
        "text_stats": {
            "total_chars": text_result["total_chars"],
            "total_sentences": text_result["total_sentences"],
            "avg_sentence_length": text_result["avg_sentence_length"],
            "sentence_length_std_dev": text_result["sentence_length_std_dev"],
            "ttr": text_result["ttr"],
            "risk_assessment": text_result["risk_assessment"],
        },
        "vocab_stats": {
            "risk_level": vocab_result["risk_level"],
            "high_risk_count": vocab_result["summary"]["high_risk_count"],
            "medium_risk_count": vocab_result["summary"]["medium_risk_count"],
            "low_risk_count": vocab_result["summary"]["low_risk_count"],
            "total_matches": vocab_result["summary"]["total_matches"],
        },
    }

#!/usr/bin/env python3
"""
文本统计工具 — 计算句长标准差、TTR（词汇丰富度）等指标
用法: python text_stats.py <file_path> [--format json|text]
"""

import sys
import json
import re
import argparse
from pathlib import Path


def split_sentences(text: str) -> list[str]:
    """中英文分句"""
    sentences = re.split(r'[。！？.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def split_words_chinese(text: str) -> list[str]:
    """简单中文分词（基于字符类型）"""
    words = []
    current_word = ""
    for char in text:
        if '一' <= char <= '鿿':
            if current_word:
                words.append(current_word)
                current_word = ""
            words.append(char)
        elif char.isalnum():
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
    if current_word:
        words.append(current_word)
    return words


def calc_sentence_lengths(text: str) -> list[int]:
    """计算每个句子的长度（字符数）"""
    sentences = split_sentences(text)
    return [len(s) for s in sentences]


def calc_std_dev(values: list[float]) -> float:
    """计算标准差"""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return variance ** 0.5


def calc_ttr(text: str) -> float:
    """计算词汇丰富度（Type-Token Ratio）"""
    words = split_words_chinese(text)
    if not words:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(words)


def analyze_text(text: str) -> dict:
    """分析文本并返回统计结果"""
    sentence_lengths = calc_sentence_lengths(text)
    words = split_words_chinese(text)
    unique_words = set(words)
    std_dev = calc_std_dev(sentence_lengths)
    ttr = calc_ttr(text)

    return {
        "total_chars": len(text),
        "total_sentences": len(sentence_lengths),
        "total_words": len(words),
        "unique_words": len(unique_words),
        "avg_sentence_length": round(sum(sentence_lengths) / max(len(sentence_lengths), 1), 2),
        "sentence_length_std_dev": round(std_dev, 2),
        "ttr": round(ttr, 4),
        "sentence_lengths": sentence_lengths,
        "risk_assessment": {
            "sentence_diversity": "高风险" if std_dev < 3 else
                                  "中风险" if std_dev < 5 else
                                  "低风险" if std_dev < 8 else "安全",
            "vocabulary_richness": "高风险" if ttr < 0.4 else
                                   "中风险" if ttr < 0.5 else
                                   "低风险" if ttr < 0.6 else "安全"
        }
    }


def format_output(result: dict, fmt: str) -> str:
    """格式化输出"""
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    lines = [
        "=" * 50,
        "文本统计报告",
        "=" * 50,
        f"总字符数：{result['total_chars']}",
        f"总句数：{result['total_sentences']}",
        f"总词数：{result['total_words']}",
        f"不同词数：{result['unique_words']}",
        "",
        "核心指标：",
        f"  平均句长：{result['avg_sentence_length']} 字符",
        f"  句长标准差：{result['sentence_length_std_dev']}",
        f"  词汇丰富度（TTR）：{result['ttr']}",
        "",
        "风险评估：",
        f"  句式多样性：{result['risk_assessment']['sentence_diversity']}",
        f"  词汇丰富度：{result['risk_assessment']['vocabulary_richness']}",
        "",
        "句长分布：",
        f"  最短句：{min(result['sentence_lengths'])} 字符",
        f"  最长句：{max(result['sentence_lengths'])} 字符",
        "=" * 50,
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="文本统计工具")
    parser.add_argument("file_path", help="要分析的文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="text",
                        help="输出格式")
    args = parser.parse_args()

    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"错误：文件不存在 {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"错误：无法读取文件 {e}", file=sys.stderr)
        sys.exit(1)

    result = analyze_text(text)
    print(format_output(result, args.format))


if __name__ == "__main__":
    main()

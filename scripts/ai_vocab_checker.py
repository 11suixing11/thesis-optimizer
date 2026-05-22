#!/usr/bin/env python3
"""
AI高频词扫描工具 — 扫描文本中的AI高频词汇并标记风险等级
用法: python ai_vocab_checker.py <file_path> [--format json|text]
"""

import sys
import json
import re
import argparse
from pathlib import Path


HIGH_RISK_WORDS = [
    "值得注意的是", "综上所述", "不难发现", "显而易见", "毋庸置疑",
    "众所周知", "在当今社会", "随着", "具有重要意义", "取得了显著成果",
    "首先", "其次", "再次", "最后",
    "不仅", "而且", "一方面", "另一方面",
    "总而言之", "概括来说", "综合来看",
]

MEDIUM_RISK_WORDS = [
    "本文提出", "本文认为", "实验结果表明", "该方法具有",
    "通过分析可以发现", "在此基础上", "然而", "但是", "尽管如此",
    "研究表明", "文献指出", "理论上",
]

LOW_RISK_WORDS = [
    "因此", "所以", "由此", "基于此",
    "具有", "能够", "可以", "采用",
    "分析", "研究", "方法", "结果",
]


def find_matches(text: str, word_list: list[str]) -> list[dict]:
    """查找匹配的词汇"""
    matches = []
    for word in word_list:
        count = text.count(word)
        if count > 0:
            matches.append({
                "word": word,
                "count": count,
                "positions": [m.start() for m in re.finditer(re.escape(word), text)]
            })
    return matches


def analyze_text(text: str) -> dict:
    """分析文本中的AI高频词"""
    high_matches = find_matches(text, HIGH_RISK_WORDS)
    medium_matches = find_matches(text, MEDIUM_RISK_WORDS)
    low_matches = find_matches(text, LOW_RISK_WORDS)

    total_high = sum(m["count"] for m in high_matches)
    total_medium = sum(m["count"] for m in medium_matches)
    total_low = sum(m["count"] for m in low_matches)

    risk_level = "安全"
    if total_high > 5:
        risk_level = "高风险"
    elif total_high > 2 or total_medium > 5:
        risk_level = "中风险"
    elif total_high > 0 or total_medium > 2:
        risk_level = "低风险"

    return {
        "risk_level": risk_level,
        "summary": {
            "high_risk_count": total_high,
            "medium_risk_count": total_medium,
            "low_risk_count": total_low,
            "total_matches": total_high + total_medium + total_low
        },
        "details": {
            "high_risk": high_matches,
            "medium_risk": medium_matches,
            "low_risk": low_matches
        }
    }


def format_output(result: dict, fmt: str) -> str:
    """格式化输出"""
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    lines = [
        "=" * 50,
        "AI高频词扫描报告",
        "=" * 50,
        f"总体风险等级：{result['risk_level']}",
        "",
        "匹配统计：",
        f"  高风险词：{result['summary']['high_risk_count']} 次",
        f"  中风险词：{result['summary']['medium_risk_count']} 次",
        f"  低风险词：{result['summary']['low_risk_count']} 次",
        f"  总匹配数：{result['summary']['total_matches']} 次",
        "",
    ]

    for level in ["high_risk", "medium_risk", "low_risk"]:
        if result["details"][level]:
            label = {"high_risk": "高风险", "medium_risk": "中风险", "low_risk": "低风险"}[level]
            lines.append(f"{label}词汇详情：")
            for match in result["details"][level]:
                lines.append(f"  「{match['word']}」出现 {match['count']} 次")
            lines.append("")

    lines.append("=" * 50)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI高频词扫描工具")
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

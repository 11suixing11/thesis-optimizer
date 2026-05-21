#!/usr/bin/env python3
"""
改写前后对比生成工具 — 生成优化前后的可视化对比报告
用法: python diff_viewer.py <original_file> <revised_file> [--format markdown|html]
"""

import sys
import argparse
from pathlib import Path
import difflib


def read_file(file_path: str) -> list[str]:
    """读取文件并按行返回"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"错误：无法读取文件 {e}", file=sys.stderr)
        sys.exit(1)


def generate_diff(original_lines: list[str], revised_lines: list[str]) -> list[str]:
    """生成统一格式的diff"""
    return list(difflib.unified_diff(
        original_lines,
        revised_lines,
        fromfile='原文',
        tofile='优化后',
        lineterm='',
        n=3
    ))


def generate_side_by_side(original_lines: list[str], revised_lines: list[str]) -> list[tuple]:
    """生成并排对比"""
    diff = list(difflib.ndiff(original_lines, revised_lines))

    pairs = []
    current_original = []
    current_revised = []

    for line in diff:
        if line.startswith('- '):
            current_original.append(line[2:])
        elif line.startswith('+ '):
            current_revised.append(line[2:])
        elif line.startswith('  '):
            if current_original or current_revised:
                pairs.append(('\n'.join(current_original), '\n'.join(current_revised)))
                current_original = []
                current_revised = []
            pairs.append((line[2:], line[2:]))

    if current_original or current_revised:
        pairs.append(('\n'.join(current_original), '\n'.join(current_revised)))

    return pairs


def format_markdown(original_lines: list[str], revised_lines: list[str]) -> str:
    """生成Markdown格式的对比报告"""
    pairs = generate_side_by_side(original_lines, revised_lines)

    lines = [
        "# 改写对比报告",
        "",
        "## 统计信息",
        "",
        f"- 原文行数：{len(original_lines)}",
        f"- 优化后行数：{len(revised_lines)}",
        "",
        "## 逐段对比",
        "",
    ]

    for i, (orig, rev) in enumerate(pairs, 1):
        if orig != rev:
            lines.append(f"### 对比 {i}")
            lines.append("")
            lines.append("**原文：**")
            lines.append(f"```")
            lines.append(orig.strip())
            lines.append(f"```")
            lines.append("")
            lines.append("**优化后：**")
            lines.append(f"```")
            lines.append(rev.strip())
            lines.append(f"```")
            lines.append("")

    # 统计修改数量
    changed_count = sum(1 for o, r in pairs if o != r)
    lines.extend([
        "## 总结",
        "",
        f"- 共 {len(pairs)} 个段落",
        f"- 修改 {changed_count} 个段落",
        f"- 未修改 {len(pairs) - changed_count} 个段落",
        "",
    ])

    return "\n".join(lines)


def format_html(original_lines: list[str], revised_lines: list[str]) -> str:
    """生成HTML格式的对比报告"""
    pairs = generate_side_by_side(original_lines, revised_lines)

    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>改写对比报告</title>",
        "<style>",
        "body { font-family: 'Microsoft YaHei', sans-serif; margin: 20px; }",
        ".pair { margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }",
        ".original { background-color: #fff3f3; padding: 10px; margin: 5px 0; border-radius: 3px; }",
        ".revised { background-color: #f3fff3; padding: 10px; margin: 5px 0; border-radius: 3px; }",
        ".label { font-weight: bold; margin-bottom: 5px; }",
        "h1 { color: #333; }",
        "h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 5px; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>改写对比报告</h1>",
        "<h2>逐段对比</h2>",
    ]

    for i, (orig, rev) in enumerate(pairs, 1):
        if orig != rev:
            html.append(f"<div class='pair'>")
            html.append(f"<h3>对比 {i}</h3>")
            html.append(f"<div class='label'>原文：</div>")
            html.append(f"<div class='original'><pre>{orig.strip()}</pre></div>")
            html.append(f"<div class='label'>优化后：</div>")
            html.append(f"<div class='revised'><pre>{rev.strip()}</pre></div>")
            html.append(f"</div>")

    changed_count = sum(1 for o, r in pairs if o != r)
    html.extend([
        "<h2>总结</h2>",
        f"<p>共 {len(pairs)} 个段落，修改 {changed_count} 个段落</p>",
        "</body>",
        "</html>",
    ])

    return "\n".join(html)


def main():
    parser = argparse.ArgumentParser(description="改写对比生成工具")
    parser.add_argument("original_file", help="原文文件路径")
    parser.add_argument("revised_file", help="优化后文件路径")
    parser.add_argument("--format", choices=["markdown", "html"], default="markdown",
                        help="输出格式")
    args = parser.parse_args()

    original_lines = read_file(args.original_file)
    revised_lines = read_file(args.revised_file)

    if args.format == "markdown":
        output = format_markdown(original_lines, revised_lines)
    else:
        output = format_html(original_lines, revised_lines)

    print(output)


if __name__ == "__main__":
    main()

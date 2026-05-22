"""优化流水线 — 编排 6 个 Agent 的执行"""

import asyncio
from typing import Callable, Awaitable

from core.claude_client import call_claude
from core.prompts import (
    get_analyzer_system_prompt,
    get_ai_reduction_system_prompt,
    get_plagiarism_system_prompt,
    get_polishing_system_prompt,
    get_format_system_prompt,
    get_evaluator_system_prompt,
)

ProgressCallback = Callable[[str, int, str], Awaitable[None]]

STAGES = [
    "analyze",
    "reduce_ai",
    "reduce_plagiarism",
    "polish",
    "check_format",
    "evaluate",
]


async def run_pipeline(
    thesis_text: str,
    api_key: str,
    discipline: str = "general",
    citation_format: str = "gb/t 7714",
    on_progress: ProgressCallback | None = None,
) -> dict:
    """
    执行完整优化流水线，返回结果字典。
    """

    async def progress(stage: str, pct: int, msg: str):
        if on_progress:
            await on_progress(stage, pct, msg)

    results = {}
    revision_logs = []
    current_text = thesis_text

    # --- Stage 1: 分析 ---
    await progress("analyze", 5, "正在分析论文...")
    system_prompt = get_analyzer_system_prompt(discipline)
    user_msg = f"""请分析以下论文，学科类别：{discipline}，引用格式：{citation_format}

---

{current_text}

---

请按照输出格式要求，生成完整的分析报告。"""
    results["analysis"] = await _call(system_prompt, user_msg, api_key, max_tokens=8192)
    await progress("analyze", 15, "分析完成")

    # --- Stage 2: 降AI ---
    await progress("reduce_ai", 20, "正在降低AI检测率...")
    system_prompt = get_ai_reduction_system_prompt()
    user_msg = f"""请对以下论文执行降AI优化。学科：{discipline}

分析报告（供参考）：

{results['analysis']}

---

论文原文：

{current_text}

---

请逐段优化高AI风险段落，输出修改后的完整论文文本，并在末尾附上修订日志。"""
    ai_result = await _call(system_prompt, user_msg, api_key, max_tokens=16384)
    current_text, log = _split_text_and_log(ai_result)
    results["ai_reduction"] = current_text
    if log:
        revision_logs.append(("降AI", log))
    await progress("reduce_ai", 40, "降AI完成")

    # --- Stage 3: 降重 ---
    await progress("reduce_plagiarism", 45, "正在降低查重率...")
    system_prompt = get_plagiarism_system_prompt()
    user_msg = f"""请对以下论文执行降重优化。学科：{discipline}，引用格式：{citation_format}

分析报告（供参考）：

{results['analysis']}

---

论文文本：

{current_text}

---

请优化高查重风险段落，输出修改后的完整论文文本，并在末尾附上修订日志。"""
    plag_result = await _call(system_prompt, user_msg, api_key, max_tokens=16384)
    current_text, log = _split_text_and_log(plag_result)
    results["plagiarism"] = current_text
    if log:
        revision_logs.append(("降重", log))
    await progress("reduce_plagiarism", 60, "降重完成")

    # --- Stage 4: 润色 ---
    await progress("polish", 65, "正在润色...")
    system_prompt = get_polishing_system_prompt()
    user_msg = f"""请对以下论文执行学术润色。学科：{discipline}

---

{current_text}

---

请润色全文，提升学术表达质量，输出修改后的完整论文文本，并在末尾附上修订日志。"""
    polish_result = await _call(system_prompt, user_msg, api_key, max_tokens=16384)
    current_text, log = _split_text_and_log(polish_result)
    results["polished"] = current_text
    if log:
        revision_logs.append(("润色", log))
    await progress("polish", 80, "润色完成")

    # --- Stage 5: 格式检查 ---
    await progress("check_format", 82, "正在检查格式...")
    system_prompt = get_format_system_prompt(discipline)
    user_msg = f"""请检查以下论文的格式规范。学科：{discipline}，引用格式：{citation_format}

---

{current_text}

---

请生成格式检查报告，列出所有格式问题并给出修改建议。"""
    results["format_report"] = await _call(system_prompt, user_msg, api_key, max_tokens=8192)
    await progress("check_format", 88, "格式检查完成")

    # --- Stage 6: 评估 ---
    await progress("evaluate", 90, "正在生成评估报告...")
    system_prompt = get_evaluator_system_prompt()
    user_msg = f"""请对以下优化后的论文进行综合评估。学科：{discipline}

优化前分析报告：

{results['analysis']}

---

优化后论文：

{current_text}

---

请从AI检测率、查重率、学术表达、格式规范、内容完整性五个维度进行评估，给出综合评分和改进建议。"""
    results["evaluation"] = await _call(system_prompt, user_msg, api_key, max_tokens=8192)
    await progress("evaluate", 100, "全部完成")

    results["revision_logs"] = revision_logs
    return results


async def _call(system_prompt: str, user_message: str, api_key: str, max_tokens: int = 8192) -> str:
    """在线程池中调用 Claude API，避免阻塞事件循环"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, call_claude, system_prompt, user_message, api_key, max_tokens
    )


def _split_text_and_log(result: str) -> tuple[str, str]:
    """将 Claude 返回的结果拆分为正文和修订日志"""
    markers = ["## 修订日志", "### 修订日志", "修订日志：", "---\n## 修订"]
    for marker in markers:
        idx = result.find(marker)
        if idx != -1:
            text = result[:idx].strip()
            log = result[idx:].strip()
            return text, log
    return result.strip(), ""

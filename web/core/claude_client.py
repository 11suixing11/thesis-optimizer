"""Claude API 客户端封装"""

import anthropic


def call_claude(system_prompt: str, user_message: str, api_key: str, max_tokens: int = 8192) -> str:
    """调用 Claude API，返回文本响应"""
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text

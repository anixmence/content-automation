from __future__ import annotations

import json
import os
from urllib import error, request

from app.models import GenerationRequest

OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4.1-mini"


class OpenAIConfigError(Exception):
    """Raised when OpenAI related settings are invalid."""


class OpenAIGenerationError(Exception):
    """Raised when OpenAI generation fails."""


def _extract_output_text(response_json: dict) -> str:
    output = response_json.get("output", [])
    for item in output:
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                return text

    output_text = response_json.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    raise OpenAIGenerationError("OpenAI API 回傳內容為空，請稍後重試。")


def generate_content_with_openai(
    request_data: GenerationRequest,
    moments_count: int,
    tone: str,
    sections: list[str],
) -> tuple[list[str], str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise OpenAIConfigError(
            "缺少 OPENAI_API_KEY。請先設定環境變數，例如：\n"
            "export OPENAI_API_KEY='your_api_key'"
        )

    prompt = f"""
你是中文內容行銷編輯，請依照以下條件產出內容，並且只輸出 JSON。

主題：{request_data.topic}
語氣：{tone}
朋友圈文案條數：{moments_count}
公眾號文章段落方向：{", ".join(sections)}

請輸出以下 JSON 結構：
{{
  "moments": ["文案1", "文案2", "...共 {moments_count} 條"],
  "article_title": "文章標題",
  "article_body": "完整文章內容（使用 Markdown，包含導言、至少 {len(sections)} 個對應段落、小結）"
}}

要求：
1) 每條朋友圈文案都要完整可直接發佈。
2) 文章要完整、可閱讀、非提綱。
3) 不要輸出 JSON 以外內容。
""".strip()

    payload = {
        "model": DEFAULT_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    }
                ],
            }
        ],
    }

    req = request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise OpenAIGenerationError(f"OpenAI API 請求失敗（HTTP {exc.code}）：{detail}") from exc
    except error.URLError as exc:
        raise OpenAIGenerationError(f"無法連線至 OpenAI API：{exc.reason}") from exc

    try:
        response_json = json.loads(body)
        output_text = _extract_output_text(response_json)
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise OpenAIGenerationError(f"OpenAI 回傳內容解析失敗：{exc}") from exc

    moments = parsed.get("moments")
    article_title = parsed.get("article_title")
    article_body = parsed.get("article_body")

    if not isinstance(moments, list) or len(moments) != moments_count or not all(isinstance(i, str) for i in moments):
        raise OpenAIGenerationError("OpenAI 回傳的 moments 欄位格式錯誤。")

    if not isinstance(article_title, str) or not article_title.strip():
        raise OpenAIGenerationError("OpenAI 回傳的 article_title 欄位格式錯誤。")

    if not isinstance(article_body, str) or not article_body.strip():
        raise OpenAIGenerationError("OpenAI 回傳的 article_body 欄位格式錯誤。")

    return moments, article_title, article_body

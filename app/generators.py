from __future__ import annotations

from openai import OpenAI

from app.models import GenerationRequest


def _extract_lines(text: str) -> list[str]:
    cleaned = text.strip()
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]

    result = []
    for line in lines:
        normalized = line
        if line[0:2].isdigit() and "." in line:
            normalized = line.split(".", 1)[1].strip()
        elif line.startswith(("-", "•")):
            normalized = line[1:].strip()
        result.append(normalized)
    return result


def generate_moments_copies(
    client: OpenAI,
    model: str,
    request: GenerationRequest,
    moments_count: int,
    tone: str,
) -> list[str]:
    prompt = (
        "你是一位資深中文社群編輯。"
        f"請針對主題「{request.topic}」寫 {moments_count} 條朋友圈文案，"
        f"語氣為「{tone}」。每條都要完整可直接發佈，不要模板感，不要重複。"
        "請只輸出條列內容，每行一條，不要額外說明。"
    )

    response = client.responses.create(model=model, input=prompt)
    text = response.output_text
    candidates = _extract_lines(text)
    copies = candidates[:moments_count]

    if len(copies) < moments_count:
        missing_count = moments_count - len(copies)
        copies.extend([f"（生成不足，請重試）主題：{request.topic}"] * missing_count)

    return copies


def generate_article(
    client: OpenAI,
    model: str,
    request: GenerationRequest,
    sections: list[str],
    tone: str,
) -> tuple[str, str]:
    section_hint = "、".join(sections)
    prompt = (
        "你是一位資深中文內容策劃與公眾號主編。"
        f"請以主題「{request.topic}」撰寫一篇完整可發佈的公眾號文章，語氣為「{tone}」。"
        f"文章請自然涵蓋這些段落方向：{section_hint}。"
        "要求：有吸引人的標題、開頭引入、清楚分段、小標、結尾總結與行動呼籲。"
        "輸出格式：第一行為標題；從第二行開始為文章正文。不要額外解釋。"
    )

    response = client.responses.create(model=model, input=prompt)
    text = response.output_text.strip()
    lines = [line for line in text.splitlines()]

    if not lines:
        return f"{request.topic}：完整實戰指南", "生成失敗，請重試。"

    title = lines[0].lstrip("# ").strip() or f"{request.topic}：完整實戰指南"
    body = "\n".join(lines[1:]).strip()
    if not body:
        body = "生成失敗，請重試。"

    return title, body

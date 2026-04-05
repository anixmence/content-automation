from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from app.config import OUTPUT_DIR, load_model_name, load_openai_api_key, load_settings
from app.generators import generate_article, generate_moments_copies
from app.models import GenerationRequest, GenerationResult


def run_generation(topic: str) -> GenerationResult:
    settings = load_settings()
    api_key = load_openai_api_key()
    model = load_model_name(settings)

    client = OpenAI(api_key=api_key)
    request = GenerationRequest(topic=topic)

    moments = generate_moments_copies(
        client=client,
        model=model,
        request=request,
        moments_count=int(settings["moments_count"]),
        tone=str(settings["default_tone"]),
    )
    title, body = generate_article(
        client=client,
        model=model,
        request=request,
        sections=list(settings["article_sections"]),
        tone=str(settings["default_tone"]),
    )

    return GenerationResult(
        topic=topic,
        moments_copies=moments,
        article_title=title,
        article_body=body,
    )


def save_outputs(result: GenerationResult) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    moments_path = OUTPUT_DIR / "moments.txt"
    article_path = OUTPUT_DIR / "article.md"

    moments_content = "\n".join(
        [f"主題：{result.topic}", "", "=== 5條朋友圈文案 ===", *[f"{i + 1}. {text}" for i, text in enumerate(result.moments_copies)]]
    )
    moments_path.write_text(moments_content, encoding="utf-8")

    article_content = "\n".join([f"# {result.article_title}", "", result.article_body])
    article_path.write_text(article_content, encoding="utf-8")

    return moments_path, article_path

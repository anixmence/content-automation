from __future__ import annotations

from app.models import GenerationRequest


def generate_moments_copies(request: GenerationRequest, moments_count: int, tone: str) -> list[str]:
    templates = [
        "{topic} 不是一時的熱度，而是值得長期投入的方向。今天先行動一小步。",
        "如果你也在關注 {topic}，歡迎一起交流，我先把這週的心得整理好了。",
        "做 {topic} 最大的收穫：看見自己每天都在變得更穩、更清晰。",
        "把複雜的 {topic} 變簡單，才是能真正落地的開始。",
        "關於 {topic}，我整理了 3 個可直接上手的方法，留言我發你。",
        "最近在深挖 {topic}，越研究越確定：先開始，比完美更重要。",
        "{topic} 這件事，我用一個小流程把效率提升了不少，之後分享細節。",
        "很多人問我 {topic} 怎麼入門：先選一個場景，今天就做第一版。",
    ]

    copies = []
    for i in range(moments_count):
        text = templates[i % len(templates)].format(topic=request.topic)
        copies.append(f"[{tone}] {text}")

    return copies


def generate_article(request: GenerationRequest, sections: list[str], tone: str) -> tuple[str, str]:
    title = f"從 0 到 1 做好「{request.topic}」：一套可落地的方法"

    intro = (
        f"在討論 {request.topic} 時，很多人會先追求完整方案，但真正有效的方式通常是先跑出最小閉環。"
        f"這篇文章會用 {tone} 的方式，帶你快速建立可執行的路線。"
    )

    paragraphs = [intro]
    for idx, section in enumerate(sections, start=1):
        paragraphs.append(
            f"## {idx}. {section}\n"
            f"以「{request.topic}」為核心，先設定一個可在 1 週內完成的小目標，"
            "並把輸入、執行、輸出三步固定下來。重點不是一次到位，而是可重複與可優化。"
        )

    closing = (
        f"最後，請記住：{request.topic} 的關鍵不是知道更多，而是每週持續產出可驗證成果。"
        "當你有了第一個可運作版本，後面的優化自然會變得簡單。"
    )
    paragraphs.append(closing)

    body = "\n\n".join(paragraphs)
    return title, body

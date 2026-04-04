from dataclasses import dataclass


@dataclass
class GenerationRequest:
    topic: str


@dataclass
class GenerationResult:
    topic: str
    moments_copies: list[str]
    article_title: str
    article_body: str

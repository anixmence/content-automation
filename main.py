from __future__ import annotations

import argparse
import sys

from app.generators import OpenAIConfigError, OpenAIGenerationError
from app.pipeline import run_generation, save_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="內容生成系統 MVP")
    parser.add_argument("topic", type=str, help="輸入主題，例如：AI 內容營銷")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        result = run_generation(args.topic)
    except OpenAIConfigError as exc:
        print(f"設定錯誤：{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except OpenAIGenerationError as exc:
        print(f"生成失敗：{exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    moments_path, article_path = save_outputs(result)

    print("生成完成！")
    print(f"- 朋友圈文案：{moments_path}")
    print(f"- 公眾號文章：{article_path}")


if __name__ == "__main__":
    main()

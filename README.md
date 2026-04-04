# content-automation

最小可行版本（MVP）：輸入一個主題，輸出 5 條朋友圈文案與 1 篇公眾號文章。

## 專案結構

```text
content-automation/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── generators.py
│   ├── models.py
│   └── pipeline.py
├── config/
│   └── settings.json
├── output/
│   └── .gitkeep
└── main.py
```

## 功能

- 輸入：一個主題（CLI 參數）
- 輸出：
  - `output/moments.txt`（5 條朋友圈文案）
  - `output/article.md`（1 篇公眾號文章）

## 如何在本機執行

### 1) 環境需求

- Python 3.10+

### 2) 執行指令

```bash
python3 main.py "AI 內容生成"
```

### 3) 查看輸出

```bash
cat output/moments.txt
cat output/article.md
```

## 可調整設定

可在 `config/settings.json` 調整：

- `moments_count`: 朋友圈文案條數（MVP 預設 5）
- `default_tone`: 文案語氣
- `article_sections`: 公眾號文章段落主題

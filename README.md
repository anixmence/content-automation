# content-automation

正式可用版（基礎版）：輸入一個主題，透過 OpenAI API 輸出 5 條朋友圈文案與 1 篇完整公眾號文章。

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
├── main.py
└── requirements.txt
```

## 安裝

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 設定 API Key

請先設定環境變數：

```bash
export OPENAI_API_KEY="your_api_key"
```

可選：自訂模型（不設時使用 `config/settings.json` 的 `model`）

```bash
export OPENAI_MODEL="gpt-5-mini"
```

## 執行

```bash
python main.py "AI 內容生成"
```

## 輸出檔案

- `output/moments.txt`：5 條完整可用朋友圈文案
- `output/article.md`：1 篇完整可用公眾號文章

## 錯誤處理

若未設定 API key，程式會顯示清楚錯誤並結束：

```text
錯誤：OPENAI_API_KEY 未設定。請先在環境變數設定 API key...
```

## 可調整設定（config/settings.json）

- `moments_count`: 文案數量（目前預設 5）
- `default_tone`: 內容語氣
- `model`: 預設模型名稱
- `article_sections`: 文章段落方向

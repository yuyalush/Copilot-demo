# Copilot-demo
Pythonを用いて東京の天気情報を取得するAPIクライアント

## 概要 (Overview)

このプロジェクトは、OpenWeatherMap APIを使用して東京の天気情報を取得するPythonクライアントです。

This project provides a Python client to fetch weather information for Tokyo using the OpenWeatherMap API.

## 機能 (Features)

- 東京の現在の天気情報を取得 (Fetch current weather information for Tokyo)
- 気温、湿度、風速などの詳細情報 (Detailed information including temperature, humidity, wind speed)
- 摂氏・華氏の単位選択 (Support for Celsius and Fahrenheit units)
- 日本語・英語などの多言語対応 (Multi-language support including Japanese and English)

## セットアップ (Setup)

### 1. 必要なパッケージのインストール (Install required packages)

```bash
pip install -r requirements.txt
```

### 2. APIキーの取得 (Get API Key)

1. [OpenWeatherMap](https://openweathermap.org/api)にアクセス
2. 無料アカウントを作成
3. APIキーを取得

### 3. 環境変数の設定 (Set environment variables)

`.env.example`をコピーして`.env`ファイルを作成:

```bash
cp .env.example .env
```

`.env`ファイルを編集してAPIキーを設定:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## 使い方 (Usage)

### 基本的な使用方法 (Basic Usage)

```python
from tokyo_weather import TokyoWeatherClient

# クライアントを作成 (Create client)
client = TokyoWeatherClient()

# 整形された天気情報を取得 (Get formatted weather information)
print(client.get_formatted_weather())

# 生のJSONデータを取得 (Get raw JSON data)
weather_data = client.get_current_weather()
print(weather_data)
```

### コマンドラインから実行 (Run from command line)

```bash
python tokyo_weather.py
```

### 単位と言語の指定 (Specify units and language)

```python
# 華氏と英語で取得 (Get in Fahrenheit and English)
weather = client.get_formatted_weather(units="imperial", lang="en")
print(weather)

# 摂氏と日本語で取得（デフォルト）(Get in Celsius and Japanese - default)
weather = client.get_formatted_weather(units="metric", lang="ja")
print(weather)
```

## テスト (Testing)

```bash
python -m unittest test_tokyo_weather.py
```

または (or):

```bash
python test_tokyo_weather.py
```

## プロジェクト構成 (Project Structure)

```
.
├── tokyo_weather.py      # メインの天気APIクライアント (Main weather API client)
├── test_tokyo_weather.py # ユニットテスト (Unit tests)
├── requirements.txt      # 依存パッケージ (Dependencies)
├── .env.example          # 環境変数のサンプル (Environment variables template)
├── .gitignore           # Gitの除外設定 (Git ignore configuration)
└── README.md            # このファイル (This file)
```

## ライセンス (License)

MIT License

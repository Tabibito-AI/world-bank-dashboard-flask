# World Bank Economic Dashboard (Flask/Python版)

## 概要

このリポジトリは、World Bankの公開データを利用して、主要12カ国の経済指標を可視化・分析するダッシュボードアプリケーションのFlask/Python実装です。

元のNode.js/GitHub Actionsベースのプロジェクトを、Manusサーバーへのフルスタックデプロイを目的としてPython/Flaskに変換しました。

### 特徴

*   **データソース**: World Bank Open Data
*   **対象国**: 日本、アメリカ、中国、ドイツ、イギリス、フランス、インド、ブラジル、カナダ、オーストラリア、インドネシア、ペルーの12カ国
*   **主要指標**: GDP、成長率、失業率、インフレ率、一人当たりGDP、貿易、政府債務、総人口、人口増減率、外国直接投資
*   **アーキテクチャ**: Python/Flaskによるバックエンド、HTML/CSS/JavaScriptによるフロントエンド
*   **AI分析**: Google Gemini APIを利用した経済トレンドの自動分析機能（デプロイ環境の制約により、現在はダミーデータで無効化されています）

## 最終デプロイURL

このリポジトリのコードベースでデプロイされたアプリケーションのURLは以下の通りです。

**URL**: [https://nghki1cmmplv.manus.space/](https://nghki1cmmplv.manus.space/)

## メイン画面

![ダッシュボードのメイン画面](/home/ubuntu/upload/18-11-20252.15の画像.jpeg)

## アーキテクチャ

| コンポーネント | 技術 | 役割 |
| :--- | :--- | :--- |
| **バックエンド** | Python / Flask | データ収集、AI分析（無効化）、ダッシュボード生成、静的ファイル配信 |
| **データ収集** | Python / `aiohttp` | World Bank APIから非同期でデータを取得 |
| **AI分析** | Python / `google-generativeai` (ダミー) | 経済トレンドの分析とサマリー生成 |
| **フロントエンド** | HTML / CSS / JavaScript | データの可視化（Chart.js）、ユーザーインターフェース |

### ファイル構成

```
world-bank-dashboard-flask/
├── src/
│   ├── data_collector.py       # World Bank APIからデータを取得するモジュール
│   ├── gemini_analyzer.py      # AI分析モジュール (現在はダミー実装)
│   ├── dashboard_generator.py  # HTML/CSS/JSファイルを生成するモジュール
│   ├── main.py                 # Flaskアプリケーションのエントリーポイント
│   ├── routes/
│   │   └── api.py              # APIエンドポイントの定義
│   └── static/                 # 静的ファイル (index.html, style.css, script.js)
├── venv/                       # 仮想環境
├── requirements.txt            # Pythonの依存関係リスト
└── README.md                   # このファイル
```

## デプロイ方法 (Manusサーバー向け)

このアプリケーションは、Manusサーバーの`service_deploy_backend`ツールを使用してデプロイすることを想定しています。

### 1. 依存関係のインストール

```bash
# 仮想環境を有効化
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

### 2. デプロイ

Flaskアプリケーションのルートディレクトリ（`world-bank-flask-backend`）から以下のコマンドを実行します。

```bash
service_deploy_backend --framework flask --project_dir /path/to/world-bank-flask-backend
```

**注意**: `google-generativeai`が依存する`grpcio`の環境問題により、AI分析機能は現在無効化されています。再デプロイ時も同様のエラーが発生する可能性があるため、このリポジトリの`gemini_analyzer.py`はダミー実装のままにしてあります。

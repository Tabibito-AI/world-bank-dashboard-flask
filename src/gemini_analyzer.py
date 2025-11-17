
import asyncio
from typing import Any, Dict

# AI分析機能を無効化するためのダミーモジュール

def initialize_gemini():
    # 何もしない
    pass

async def analyze_data(economic_data: Dict[str, Any]) -> Dict[str, Any]:
    """AI分析をスキップし、ダミーの分析結果を返す"""
    print("🤖 Gemini AI分析は無効化されています。ダミーの結果を返します。")
    
    # ダミーの概要分析
    overview = {
        "title": "経済指標ダッシュボード概要",
        "summary": "AI分析機能は現在無効化されています。データはWorld Bankから正常に取得されています。",
        "keyFindings": [
            "AI分析機能は現在無効化されています。",
            "データはWorld Bankから正常に取得されています。",
            "主要な経済指標のトレンドをチャートで確認できます。"
        ],
        "methodology": "AI分析無効",
        "dataQuality": "World Bank公式データを使用"
    }

    # ダミーの国別分析
    dummy_country_analysis = {
        "overview": "AI分析機能は現在無効化されています。",
        "strengths": ["データ表示"],
        "challenges": ["AI分析無効"],
        "outlook": "データは最新です"
    }
    by_country = {
        code: {
            "country": data["name"],
            "countryCode": code,
            **dummy_country_analysis
        }
        for code, data in economic_data["byCountry"].items()
    }

    # ダミーの指標別分析
    dummy_indicator_analysis = {
        "analysis": "AI分析機能は現在無効化されています。",
        "insights": ["データ表示"],
        "globalTrends": "データは最新です"
    }
    by_indicator = {
        code: {
            "indicator": data["name"],
            "indicatorCode": code,
            **dummy_indicator_analysis
        }
        for code, data in economic_data["byIndicator"].items()
    }

    # ダミーの世界経済総括
    global_economic_summary = {
        "mainTrends": ["AI分析機能は現在無効化されています。"],
        "keyPoints": ["データは最新です"]
    }

    return {
        "overview": overview,
        "byCountry": by_country,
        "byIndicator": by_indicator,
        "globalEconomicSummary": global_economic_summary,
    }

if __name__ == "__main__":
    # テスト用のダミーデータ
    dummy_economic_data = {
        "byCountry": {
            "JPN": {"name": "日本", "data": []}
        },
        "byIndicator": {
            "NY.GDP.MKTP.CD": {"name": "GDP（現在価格、米ドル）", "data": []}
        },
        "summary": {
            "countries": ["JPN"],
            "indicators": ["NY.GDP.MKTP.CD"],
            "yearRange": {"min": 2010, "max": 2020},
            "totalRecords": 10
        }
    }
    async def main():
        analysis = await analyze_data(dummy_economic_data)
        print(analysis)
    
    asyncio.run(main())



import asyncio
import os
import json
from datetime import datetime

import aiohttp

# 対象国のコード
COUNTRIES = {
    "JPN": "日本",
    "USA": "アメリカ",
    "CHN": "中国",
    "DEU": "ドイツ",
    "GBR": "イギリス",
    "FRA": "フランス",
    "IND": "インド",
    "BRA": "ブラジル",
    "CAN": "カナダ",
    "AUS": "オーストラリア",
    "IDN": "インドネシア",
    "PER": "ペルー",
}

# 経済指標のコード
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP（現在価格、米ドル）",
    "NY.GDP.MKTP.KD.ZG": "GDP成長率（年率）",
    "SL.UEM.TOTL.ZS": "失業率（%）",
    "FP.CPI.TOTL.ZG": "インフレ率（%）",
    "NY.GDP.PCAP.CD": "一人当たりGDP（米ドル）",
    "NE.TRD.GNFS.ZS": "貿易（GDP比%）",
    "GC.DPT.TOTL.GD.ZS": "政府債務（GDP比%）",
    "SP.POP.TOTL": "総人口",
    "SP.POP.GROW": "人口増減率（年率%）",
    "BX.KLT.DINV.CD.WD": "外国直接投資（米ドル）",
}

# World Bank API基本URL
BASE_URL = "https://api.worldbank.org/v2"


async def fetch_indicator_data(
    session,
    country_code,
    indicator_code,
    end_year=datetime.now().year,
    start_year=datetime.now().year - 19,
):
    """指定された国と指標のデータを取得"""
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"
    params = {"format": "json", "date": f"{start_year}:{end_year}", "per_page": 100}

    print(f"  📈 {COUNTRIES[country_code]} - {INDICATORS[indicator_code]} を取得中...")

    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data and data[1]:
                    return [
                        {
                            "country": item["country"]["value"],
                            "countryCode": item["countryiso3code"],
                            "indicator": INDICATORS[indicator_code],
                            "indicatorCode": indicator_code,
                            "year": int(item["date"]),
                            "value": item["value"],
                            "unit": get_unit(indicator_code),
                        }
                        for item in data[1]
                        if item["value"] is not None
                    ]
    except Exception as e:
        print(f"  ❌ {country_code} - {indicator_code} の取得に失敗:", e)
    return []


def get_unit(indicator_code):
    """指標コードに基づいて単位を返す"""
    units = {
        "NY.GDP.MKTP.CD": "米ドル",
        "NY.GDP.MKTP.KD.ZG": "%",
        "SL.UEM.TOTL.ZS": "%",
        "FP.CPI.TOTL.ZG": "%",
        "NY.GDP.PCAP.CD": "米ドル",
        "NE.TRD.GNFS.ZS": "%",
        "GC.DPT.TOTL.GD.ZS": "%",
        "SP.POP.TOTL": "人",
        "SP.POP.GROW": "%",
        "BX.KLT.DINV.CD.WD": "米ドル",
    }
    return units.get(indicator_code, "")


async def collect_all_data():
    """全ての国と指標のデータを取得"""
    all_data = []
    countries = list(COUNTRIES.keys())
    indicators = list(INDICATORS.keys())

    print(f"📊 {len(countries)}カ国 × {len(indicators)}指標のデータを取得開始...")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for country_code in countries:
            print(f"🌍 {COUNTRIES[country_code]} のデータを取得中...")
            for indicator_code in indicators:
                tasks.append(
                    fetch_indicator_data(session, country_code, indicator_code)
                )
        results = await asyncio.gather(*tasks)
        for result in results:
            all_data.extend(result)

    return all_data


def organize_data(raw_data):
    """データを国別・指標別に整理"""
    organized = {
        "byCountry": {},
        "byIndicator": {},
        "summary": {
            "totalRecords": len(raw_data),
            "countries": list(COUNTRIES.keys()),
            "indicators": list(INDICATORS.keys()),
            "yearRange": {
                "min": min(d["year"] for d in raw_data) if raw_data else 0,
                "max": max(d["year"] for d in raw_data) if raw_data else 0,
            },
            "lastUpdated": datetime.now().isoformat(),
        },
    }

    for country_code in COUNTRIES:
        organized["byCountry"][country_code] = {
            "name": COUNTRIES[country_code],
            "data": [d for d in raw_data if d["countryCode"] == country_code],
        }

    for indicator_code in INDICATORS:
        organized["byIndicator"][indicator_code] = {
            "name": INDICATORS[indicator_code],
            "data": [d for d in raw_data if d["indicatorCode"] == indicator_code],
        }

    return organized


def save_data(data, filename):
    """データをファイルに保存"""
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 データを保存しました: {filename}")

    except Exception as error:
        print(f"❌ データ保存に失敗: {filename}", error)
        raise error


async def collect_data():
    """メイン関数：データ収集の実行"""
    try:
        print("🚀 World Bank データ収集開始...")

        raw_data = await collect_all_data()

        if not raw_data:
            raise Exception("データが取得できませんでした")

        organized_data = organize_data(raw_data)

        # JSON形式で保存するように修正
        save_data(raw_data, "raw-data.json")
        save_data(organized_data, "organized-data.json")
        save_data(organized_data, "economic-data.json")

        print(f"✅ データ収集完了: {len(raw_data)}件のレコードを取得")
        print(
            f"📅 期間: {organized_data['summary']['yearRange']['min']}-{organized_data['summary']['yearRange']['max']}"
        )

        return organized_data

    except Exception as error:
        print("❌ データ収集でエラーが発生:", error)
        raise error


if __name__ == "__main__":
    asyncio.run(collect_data())


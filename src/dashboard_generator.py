
import os
import json
from datetime import datetime


def generate_dashboard(economic_data, analysis):
    """HTMLダッシュボードを生成"""
    try:
        print("🎨 HTMLダッシュボードを生成中...")
        generate_html(economic_data, analysis)
        generate_css()
        generate_js(economic_data, analysis)
        print("✅ ダッシュボード生成完了")
    except Exception as e:
        print(f"❌ ダッシュボード生成でエラーが発生: {e}")
        raise


def generate_html(economic_data, analysis):
    """HTMLファイルを生成"""
    overview_summary = (analysis.get("overview", {}) or {}).get("summary", "データを読み込み中...")
    overview_key_findings = (analysis.get("overview", {}) or {}).get("keyFindings", ["分析中..."])

    key_findings_html = "".join([f"<li>{finding}</li>" for finding in overview_key_findings])

    country_options = "".join(
        [
            f'<option value="{code}">{data["name"]}</option>'
            for code, data in (economic_data.get("byCountry") or {}).items()
        ]
    )

    indicator_options = "".join(
        [
            f'<option value="{code}">{data["name"]}</option>'
            for code, data in (economic_data.get("byIndicator") or {}).items()
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World Bank Economic Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/date-fns@2.29.3/index.min.js"></script>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1 class="title">
                    <span class="title-icon">📊</span>
                    World Bank Economic Dashboard
                </h1>
                <p class="subtitle">主要12カ国の経済指標分析 - AI powered by Gemini</p>
                <div class="last-updated">
                    最終更新: <span id="lastUpdated">{ datetime.now().strftime("%Y-%m-%d %H:%M:%S") }</span>
                </div>
            </div>
        </header>

        <section class="overview-section">
            <div class="overview-card">
                <h2>📈 概要</h2>
                <div class="overview-content">
                    <p class="overview-text" id="overviewText">
                        {overview_summary}
                    </p>
                    <div class="key-findings">
                        <h3>主要な発見</h3>
                        <ul id="keyFindings">
                            {key_findings_html}
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section class="countries-section">
            <h2>🌍 国別分析</h2>
            <div class="countries-grid" id="countriesGrid">
            </div>
        </section>

        <section class="indicators-section">
            <h2>📊 指標別比較</h2>
            <div class="indicators-tabs">
                <div class="tab-buttons" id="indicatorTabs">
                </div>
                <div class="tab-content" id="indicatorContent">
                </div>
            </div>
        </section>

        <section class="charts-section">
            <h2>📈 データ可視化</h2>
            <div class="charts-grid">
                <div class="chart-card">
                    <h3>GDP比較（最新年）</h3>
                    <canvas id="gdpChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>GDP成長率トレンド</h3>
                    <canvas id="gdpGrowthChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>失業率比較</h3>
                    <canvas id="unemploymentChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>一人当たりGDP比較</h3>
                    <canvas id="gdpPerCapitaChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>インフレ率トレンド</h3>
                    <canvas id="inflationChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>貿易トレンド</h3>
                    <canvas id="tradeChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>総人口トレンド</h3>
                    <canvas id="populationChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>外国直接投資トレンド</h3>
                    <canvas id="fdiChart"></canvas>
                </div>
            </div>
        </section>

        <section class="data-section">
            <h2>📋 詳細データ</h2>
            <div class="data-controls">
                <select id="countrySelect">
                    <option value="">国を選択</option>
                    {country_options}
                </select>
                <select id="indicatorSelect">
                    <option value="">指標を選択</option>
                    {indicator_options}
                </select>
            </div>
            <div class="data-table-container">
                <table id="dataTable" class="data-table">
                    <thead>
                        <tr>
                            <th>年</th>
                            <th>国</th>
                            <th>指標</th>
                            <th>値</th>
                            <th>単位</th>
                        </tr>
                    </thead>
                    <tbody id="dataTableBody">
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="footer">
            <div class="footer-content">
                <p>
                    データソース: <a href="https://data.worldbank.org/" target="_blank">World Bank Open Data</a> | 
                    AI分析: <a href="https://ai.google.dev/" target="_blank">Google Gemini</a> | 
                    更新: GitHub Actions
                </p>
                <p class="footer-note">
                    このダッシュボードは自動更新されます。最新のデータと分析をお楽しみください。
                </p>
            </div>
        </footer>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>"""

    public_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(public_dir, exist_ok=True)
    file_path = os.path.join(public_dir, "index.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("💾 HTMLファイルを生成しました: index.html")


def generate_css():
    """CSSファイルを生成"""
    css = """
    /* World Bank Economic Dashboard Styles */

    /* Reset and base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Header */
    .header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }

    .title-icon {
        font-size: 3rem;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 15px;
    }

    .last-updated {
        font-size: 0.9rem;
        color: #95a5a6;
        padding: 8px 16px;
        background: rgba(52, 152, 219, 0.1);
        border-radius: 20px;
        display: inline-block;
    }

    /* Section common */
    section {
        margin-bottom: 40px;
    }

    section h2 {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Overview section */
    .overview-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    .overview-text {
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 25px;
        color: #34495e;
    }

    .key-findings h3 {
        color: #e74c3c;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }

    .key-findings ul {
        list-style: none;
    }

    .key-findings li {
        padding: 10px 0;
        padding-left: 25px;
        position: relative;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }

    .key-findings li:before {
        content: "💡";
        position: absolute;
        left: 0;
        top: 10px;
    }

    /* Country analysis grid */
    .countries-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 20px;
    }

    .country-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .country-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }

    .country-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }

    .country-flag {
        font-size: 2rem;
    }

    .country-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
    }

    .country-overview {
        font-size: 1rem;
        line-height: 1.6;
        color: #555;
        margin-bottom: 20px;
    }

    .country-metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }

    .metric-item {
        text-align: center;
        padding: 15px;
        background: rgba(52, 152, 219, 0.1);
        border-radius: 10px;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }

    /* AI analysis section */
    .ai-analysis-section {
        background: rgba(52, 152, 219, 0.05);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border-left: 4px solid #3498db;
    }

    .ai-analysis-section h4 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }

    .ai-analysis-content {
        font-size: 1rem;
        line-height: 1.6;
        color: #34495e;
        margin-bottom: 15px;
    }

    .ai-analysis-trends {
        font-size: 0.95rem;
        color: #7f8c8d;
        font-style: italic;
    }

    .ai-analysis-trends strong {
        color: #2c3e50;
    }

    /* Indicator tabs */
    .indicators-tabs {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    .tab-buttons {
        display: flex;
        flex-wrap: wrap;
        background: rgba(52, 152, 219, 0.1);
    }

    .tab-button {
        flex: 1;
        min-width: 200px;
        padding: 15px 20px;
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        color: #7f8c8d;
        transition: all 0.3s ease;
        border-bottom: 3px solid transparent;
    }

    .tab-button:hover {
        background: rgba(52, 152, 219, 0.2);
        color: #2c3e50;
    }

    .tab-button.active {
        background: rgba(52, 152, 219, 0.3);
        color: #2c3e50;
        border-bottom-color: #3498db;
    }

    .tab-content {
        padding: 30px;
    }

    .tab-panel {
        display: none;
    }

    .tab-panel.active {
        display: block;
    }

    /* Charts section */
    .charts-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 25px;
    }

    .chart-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    }

    .chart-card h3 {
        text-align: center;
        margin-bottom: 20px;
        color: #34495e;
    }

    /* Data table section */
    .data-controls {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }

    .data-controls select {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 1rem;
    }

    .data-table-container {
        overflow-x: auto;
        background: #fff;
        border-radius: 15px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
    }

    .data-table th, .data-table td {
        padding: 15px;
        text-align: left;
        border-bottom: 1px solid #eee;
    }

    .data-table th {
        background: #f7f9fc;
        font-weight: 600;
        color: #2c3e50;
    }

    .data-table tbody tr:hover {
        background-color: #f1f5f9;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 30px 0;
        color: rgba(255, 255, 255, 0.8);
    }

    .footer a {
        color: #fff;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    .footer a:hover {
        color: #ddd;
    }

    .footer-note {
        font-size: 0.9rem;
        margin-top: 10px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .title {
            font-size: 2rem;
        }

        .charts-grid {
            grid-template-columns: 1fr;
        }

        .tab-button {
            flex-basis: 100%;
        }
    }
    """
    public_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(public_dir, exist_ok=True)
    file_path = os.path.join(public_dir, "style.css")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("💾 CSSファイルを生成しました: style.css")


def generate_js(economic_data, analysis):
    """JavaScriptファイルを生成"""
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const economicData = {economic_data};
    const analysis = {analysis};

    if (economicData && analysis) {{
        renderCountryCards(economicData, analysis);
        renderIndicatorTabs(economicData, analysis);
        renderCharts(economicData);
        setupDataFilters(economicData);
    }}

    // 最終更新日時を更新
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {{
        lastUpdatedElement.textContent = new Date(economicData.summary.lastUpdated).toLocaleString('ja-JP');
    }}
}});

function renderCountryCards(economicData, analysis) {{
    const grid = document.getElementById('countriesGrid');
    if (!grid) return;

    const countryOrder = ['JPN', 'USA', 'CHN', 'DEU', 'GBR', 'FRA', 'IND', 'BRA', 'CAN', 'AUS', 'IDN', 'PER'];

    for (const countryCode of countryOrder) {{
        const country = economicData.byCountry[countryCode];
        const countryAnalysis = analysis.byCountry[countryCode];
        if (!country || !countryAnalysis) continue;

        const latestData = getLatestData(country.data);

        const card = document.createElement('div');
        card.className = 'country-card';
        card.innerHTML = `
            <div class="country-header">
                <span class="country-flag">${{getFlag(countryCode)}}</span>
                <h3 class="country-name">${{country.name}}</h3>
            </div>
            <p class="country-overview">${{countryAnalysis.economicOverview || ''}}</p>
            <div class="country-metrics">
                ${{renderMetric('GDP', latestData['NY.GDP.MKTP.CD'])}}
                ${{renderMetric('成長率', latestData['NY.GDP.MKTP.KD.ZG'])}}
                ${{renderMetric('失業率', latestData['SL.UEM.TOTL.ZS'])}}
                ${{renderMetric('インフレ率', latestData['FP.CPI.TOTL.ZG'])}}
            </div>
            <div class="ai-analysis-section">
                <h4>🤖 AI分析コメント</h4>
                <div class="ai-analysis-content">
                    <strong>強み:</strong> ${{countryAnalysis.strengths?.join(', ') || '分析中...'}}<br>
                    <strong>課題:</strong> ${{countryAnalysis.challenges?.join(', ') || '分析中...'}}
                </div>
                <div class="ai-analysis-trends">
                    <strong>今後の見通し:</strong> ${{countryAnalysis.outlook || '分析中...'}}
                </div>
            </div>
        `;
        grid.appendChild(card);
    }}
}}

// ... (The rest of the JS code will be similar to the original file)

"""
    public_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(public_dir, exist_ok=True)
    file_path = os.path.join(public_dir, "script.js")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("💾 JavaScriptファイルを生成しました: script.js")


if __name__ == "__main__":
    # This is a placeholder for testing
    dummy_data = {"byCountry": {}, "byIndicator": {}, "summary": {}}
    dummy_analysis = {"overview": {}, "byCountry": {}, "byIndicator": {}}
    generate_dashboard(dummy_data, dummy_analysis)


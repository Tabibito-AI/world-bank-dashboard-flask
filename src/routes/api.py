
from flask import Blueprint, jsonify, request
from src.data_collector import collect_data
from src.gemini_analyzer import analyze_data
from src.dashboard_generator import generate_dashboard

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@api_bp.route("/update", methods=["POST"])
async def update_dashboard():
    try:
        # データ収集
        economic_data = await collect_data()

        # AI分析（無効化）
        # analysis_results = await analyze_data(economic_data)
        analysis_results = await analyze_data(economic_data) # ダミー分析を呼び出す

        # ダッシュボード生成
        generate_dashboard(economic_data, analysis_results)

        # 結果を返す
        return jsonify({
            "economic_data": economic_data,
            "analysis": analysis_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


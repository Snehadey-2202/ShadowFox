"""
app.py
Flask Web Dashboard application for India vs England 3rd T20I (2017) Fielding Analysis.
"""

import os
import sqlite3
from flask import Flask, render_template, jsonify, send_from_directory, send_file, Response, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CHARTS_DIR = os.path.join(DATASET_DIR, "charts")
DB_PATH = os.path.join(DATASET_DIR, "india_england_2017_t20_fielding.db")

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "static"))

def get_db_connection():
    """Connects to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_charts_exist():
    """Guarantees that database and all 5 chart PNGs exist in dataset/charts/."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    required_charts = [
        "team_performance_scores.png",
        "target_player_comparison.png",
        "fielding_zone_analysis.png",
        "runs_saved_analysis.png",
        "dismissal_breakdown.png"
    ]
    
    all_exist = all(os.path.exists(os.path.join(CHARTS_DIR, f)) for f in required_charts)
    db_exists = os.path.exists(DB_PATH)

    if not all_exist or not db_exists:
        print("[+] Generating missing database and chart images for dashboard...")
        from data_collector import T20FieldingDataCollector
        from analyzer import FieldingAnalyzer
        from visualizer import FieldingVisualizer
        from exporter import DatasetExporter

        collector = T20FieldingDataCollector()
        events = collector.generate_ball_by_ball_logs()
        analyzer = FieldingAnalyzer(events)
        matrix = analyzer.get_performance_matrix()
        zone_summary = analyzer.get_zone_summary()
        
        exporter = DatasetExporter(output_dir=DATASET_DIR)
        exporter.export_all(events, matrix)

        visualizer = FieldingVisualizer(charts_dir=CHARTS_DIR)
        visualizer.generate_all_charts(matrix, zone_summary, events)

@app.route("/")
def index():
    """Renders main dashboard layout."""
    ensure_charts_exist()
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    """Returns Executive KPIs, Leaderboard, Delivery Logs, and Scouting data as JSON."""
    ensure_charts_exist()

    conn = get_db_connection()
    try:
        matrix_rows = conn.execute("SELECT * FROM player_performance_matrix ORDER BY performance_score DESC").fetchall()
        logs_rows = conn.execute("SELECT * FROM ball_by_ball_fielding ORDER BY over ASC, ball ASC").fetchall()

        matrix = [dict(row) for row in matrix_rows]
        logs = [dict(row) for row in logs_rows]

        top_fielder = matrix[0]['player_name'] if matrix else "N/A"
        top_ps = matrix[0]['performance_score'] if matrix else 0
        total_runs_saved = sum(p['runs_saved'] for p in matrix)
        total_dismissals = sum(p['catches'] + p['stumpings'] + p['run_outs'] for p in matrix)
        total_deliveries = len(logs)

        from analyzer import FieldingAnalyzer, FieldingEvent
        events_objs = []
        for l in logs:
            events_objs.append(FieldingEvent(
                match_number=l.get('match_number', '3rd T20I'),
                innings=l.get('innings', 2),
                team=l.get('team', 'India'),
                over=l['over'], ball=l['ball'],
                batter=l.get('batter', 'Batter'), bowler=l.get('bowler', 'Bowler'),
                fielder=l['fielder'], position=l['position'],
                short_description=l['short_description'],
                pick=l.get('pick', l.get('clean_picks', 0)),
                throw=l.get('throw', l.get('good_throws', 0)),
                catches=l['catches'], dropped_catches=l['dropped_catches'],
                stumpings=l['stumpings'], run_outs=l['run_outs'],
                missed_run_outs=l['missed_run_outs'], direct_hits=l['direct_hits'],
                runs_saved=l['runs_saved'], venue=l.get('venue', 'Bengaluru'),
                zone=l.get('zone', 'Infield')
            ))
        analyzer = FieldingAnalyzer(events_objs)
        
        scouting = {
            "Dhoni": analyzer.get_scouting_report("MS Dhoni (WK)"),
            "Kohli": analyzer.get_scouting_report("Virat Kohli (C)"),
            "Pandya": analyzer.get_scouting_report("Hardik Pandya")
        }

        return jsonify({
            "kpis": {
                "top_fielder": top_fielder,
                "top_ps": top_ps,
                "total_runs_saved": total_runs_saved,
                "total_dismissals": total_dismissals,
                "total_deliveries": total_deliveries
            },
            "leaderboard": matrix,
            "logs": logs,
            "scouting": scouting
        })
    finally:
        conn.close()

@app.route("/charts/<filename>")
def serve_chart(filename):
    """Serves chart images from dataset/charts/."""
    ensure_charts_exist()
    chart_file_path = os.path.join(CHARTS_DIR, filename)
    if not os.path.exists(chart_file_path):
        ensure_charts_exist()
    return send_from_directory(CHARTS_DIR, filename)

@app.route("/api/download/<file_type>")
def download_file(file_type):
    """Browser download route for dataset CSVs or SQLite database."""
    ensure_charts_exist()
    if file_type == "log_csv":
        path = os.path.join(DATASET_DIR, "India_England_2017_Ball_By_Ball_Fielding.csv")
        as_name = "India_England_2017_Ball_By_Ball_Fielding.csv"
    elif file_type == "player_csv" or file_type == "matrix_csv":
        path = os.path.join(DATASET_DIR, "India_England_2017_Player_Performance.csv")
        as_name = "India_England_2017_Player_Performance.csv"
    elif file_type == "sqlite_db":
        path = DB_PATH
        as_name = "india_england_2017_t20_fielding.db"
    else:
        return jsonify({"error": "Invalid download file type."}), 400

    if not os.path.exists(path):
        return jsonify({"error": "Requested file does not exist."}), 404

    return send_file(path, as_attachment=True, download_name=as_name)

@app.route("/favicon.ico")
def favicon():
    """Serves inline SVG cricket favicon to prevent console 404 logs."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <text y=".9em" font-size="90">🏏</text>
    </svg>'''
    return Response(svg, mimetype="image/svg+xml")

def run_server(port=5000, debug=False):
    """Entry point to launch Flask dev server."""
    ensure_charts_exist()
    app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    run_server(debug=True)

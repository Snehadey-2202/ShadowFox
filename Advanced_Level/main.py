"""
main.py
CLI entrypoint for ShadowFox Advanced Level Python Development Internship Task 3: Cricket Fielding Performance Analysis.
"""

import sys
import os
import argparse
import unittest

from data_collector import T20FieldingDataCollector
from analyzer import FieldingAnalyzer
from exporter import DatasetExporter
from visualizer import FieldingVisualizer

def run_pipeline(quiet: bool = False) -> dict:
    """Executes full analytics pipeline: simulation, matrix calculation, SQLite/CSV export, and chart generation."""
    if not quiet:
        print("=" * 75)
        print(" SHADOWFOX SPORTS ANALYTICS ENGINE: INDIA VS ENGLAND 3RD T20I (2017) ")
        print(" Match: England Innings | Venue: M. Chinnaswamy Stadium, Bengaluru ")
        print("=" * 75)
        print("\n[+] Step 1: Simulating 120 Legal Delivery Fielding Events (England Innings)...")

    collector = T20FieldingDataCollector()
    events = collector.generate_ball_by_ball_logs()

    if not quiet:
        print("[+] Step 2: Computing Performance Matrix & Scouting Evaluations...")

    analyzer = FieldingAnalyzer(events)
    matrix = analyzer.get_performance_matrix()
    zone_summary = analyzer.get_zone_summary()

    if not quiet:
        print("[+] Step 3: Persisting Datasets to SQLite DB & CSV Tables...")

    exporter = DatasetExporter(output_dir="dataset")
    exporter.export_all(events, matrix)

    if not quiet:
        print("[+] Step 4: Generating High-Res Matplotlib & Seaborn Analytics Charts...")

    visualizer = FieldingVisualizer(charts_dir="dataset/charts")
    chart_paths = visualizer.generate_all_charts(matrix, zone_summary, events)

    if not quiet:
        print("[SUCCESS] Pipeline executed cleanly!")
        print(f" -> SQLite Database: {exporter.db_path}")
        print(f" -> Ball Logs CSV: {exporter.log_csv_path}")
        print(f" -> Performance Matrix CSV: {exporter.matrix_csv_path}")
        print(f" -> Generated Charts: {len(chart_paths)} images saved in dataset/charts/\n")

    return {
        "events": events,
        "matrix": matrix,
        "zone_summary": zone_summary,
        "exporter": exporter,
        "chart_paths": chart_paths
    }

def print_player_scouting_card(player_name: str):
    """Prints qualitative scouting report for target player to ASCII terminal."""
    collector = T20FieldingDataCollector()
    events = collector.generate_ball_by_ball_logs()
    analyzer = FieldingAnalyzer(events)
    report = analyzer.get_scouting_report(player_name)

    if not report.get("stats"):
        print(f"[-] Player '{player_name}' not found. Available target players: 'MS Dhoni', 'Virat Kohli', 'Hardik Pandya'")
        return

    stats = report["stats"]
    print("\n" + "=" * 65)
    print(f" SCOUTING CARD: {report['player_name'].upper()} (Rank #{report['match_rank']}) ")
    print("=" * 65)
    print(f" Role: {report['role']}")
    print(f" Performance Score: {stats['performance_score']} PS")
    print(f" Metrics: {stats['clean_picks']} CP | {stats['good_throws']} GT | {stats['catches']} C | {stats['stumpings']} ST | {stats['run_outs']} RO | +{stats['runs_saved']} RS")
    print(f"\n Match Highlight:\n   {report['match_highlight']}")
    print("\n Key Tactical Strengths:")
    for s in report.get('key_strengths', []):
        print(f"   • {s}")
    print("\n Coaching Directives:")
    for c in report.get('coaching_points', []):
        print(f"   • {c}")
    print("=" * 65 + "\n")

def run_tests():
    """Runs automated unit test suite."""
    print("[+] Launching Automated Unit Test Suite (tests/test_fielding_engine.py)...\n")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

def launch_dashboard(port: int = 5000):
    """Launches interactive Flask web dashboard."""
    run_pipeline(quiet=True)
    web_dir = os.path.join(os.path.dirname(__file__), "web_dashboard")
    sys.path.insert(0, web_dir)
    from app import run_server
    print(f"\n[+] Starting Interactive Flask Web Dashboard Server on http://127.0.0.1:{port}...")
    print("[+] Press Ctrl+C to terminate server.")
    run_server(port=port)

def main():
    parser = argparse.ArgumentParser(description="Cricket Fielding Performance Analysis Engine (ShadowFox Task 3)")
    parser.add_argument("-d", "--dashboard", action="store_true", help="Launch interactive Flask web dashboard")
    parser.add_argument("-p", "--player", type=str, help="Print terminal scouting card for target player (e.g. 'MS Dhoni')")
    parser.add_argument("-t", "--test", action="store_true", help="Run automated unit test suite")
    parser.add_argument("-q", "--quiet", action="store_true", help="Execute pipeline quietly without verbose logs")

    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.dashboard:
        launch_dashboard()
    elif args.player:
        print_player_scouting_card(args.player)
    else:
        run_pipeline(quiet=args.quiet)

if __name__ == "__main__":
    main()

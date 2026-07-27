"""
main.py
Master CLI driver incorporating argparse for India vs England 3rd T20I (2017) Fielding Analytics Engine.
"""
import sys
import os
import argparse
import unittest

from data_collector import T20FieldingDataCollector
from analyzer import FieldingAnalyzer
from exporter import DatasetExporter
from visualizer import FieldingVisualizer

def print_ascii_header():
    """Prints clean ASCII header for terminal output."""
    print("=" * 75)
    print(" SHADOWFOX SPORTS ANALYTICS ENGINE: INDIA VS ENGLAND 3RD T20I (2017) ")
    print(" Match: England Innings | Venue: M. Chinnaswamy Stadium, Bengaluru ")
    print("=" * 75)

def run_pipeline(quiet=False):
    """Executes full data collection, analysis, export, and chart visualization pipeline."""
    if not quiet:
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
    paths = exporter.export_all(events, matrix)

    if not quiet:
        print("[+] Step 4: Generating High-Res Matplotlib & Seaborn Analytics Charts...")
    visualizer = FieldingVisualizer(charts_dir="dataset/charts")
    chart_paths = visualizer.generate_all_charts(matrix, zone_summary, events)

    if not quiet:
        print(f"[SUCCESS] Pipeline executed cleanly!")
        print(f" -> SQLite Database: {paths['db_path']}")
        print(f" -> Ball Logs CSV: {paths['log_csv']}")
        print(f" -> Performance Matrix CSV: {paths['matrix_csv']}")
        print(f" -> Generated Charts: {len(chart_paths)} images saved in dataset/charts/\n")

    return analyzer, matrix

def print_player_scouting_card(analyzer: FieldingAnalyzer, player_name: str):
    """Prints elegant terminal scouting card for specified player using clean ASCII text."""
    report = analyzer.get_scouting_report(player_name)
    
    if "error" in report:
        print(f"\n[!] ERROR: {report['error']}\n")
        return

    stats = report['stats']
    print("\n" + "=" * 70)
    print(f" PLAYER SCOUTING REPORT: {stats['player_name'].upper()}")
    print("=" * 70)
    print(f" Match Rank      : #{report['match_rank']}")
    print(f" Role            : {report['role']}")
    print(f" Primary Position: {stats['primary_position']}")
    print(f" Performance Score: {stats['performance_score']} PS")
    print("-" * 70)
    print(" METRIC STATISTICAL BREAKDOWN:")
    print(f"  - Total Deliveries Monitored: {stats['total_deliveries']}")
    print(f"  - Clean Picks (+1)         : {stats['clean_picks']}")
    print(f"  - Good Throws (+1)         : {stats['good_throws']}")
    print(f"  - Catches Taken (+3)       : {stats['catches']}")
    print(f"  - Stumpings (+3)           : {stats['stumpings']}")
    print(f"  - Direct Hits (+2)         : {stats['direct_hits']}")
    print(f"  - Run Outs (+3)            : {stats['run_outs']}")
    print(f"  - Net Runs Saved           : +{stats['runs_saved']}")
    print("-" * 70)
    print(" MATCH HIGHLIGHT:")
    print(f"  * {report['match_highlight']}")
    print("-" * 70)
    print(" KEY TACTICAL STRENGTHS:")
    for s in report['key_strengths']:
        print(f"  [+] {s}")
    print("-" * 70)
    print(" COACHING DIRECTIVES:")
    for c in report['coaching_points']:
        print(f"  [-] {c}")
    print("=" * 70 + "\n")

def run_tests():
    """Runs automated unit test suite."""
    print("\n[+] Launching Automated Unit Test Suite (tests/test_fielding_engine.py)...\n")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="India vs England 3rd T20I (2017) Cricket Fielding Performance Analytics Engine"
    )
    parser.add_argument("-d", "--dashboard", action="store_true",
                        help="Execute pipeline and boot up Flask Web Dashboard server")
    parser.add_argument("-p", "--player", type=str, metavar="NAME",
                        help="Query database and print terminal scouting card for player (e.g., 'MS Dhoni')")
    parser.add_argument("-t", "--test", action="store_true",
                        help="Launch automated unit test suite")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Run database generation silently without console logs")

    args = parser.parse_args()

    if args.test:
        run_tests()
        return

    if not args.quiet:
        print_ascii_header()
    analyzer, matrix = run_pipeline(quiet=args.quiet)

    if args.player:
        query = args.player.lower()
        matched_name = None
        for p in matrix:
            if query in p.player_name.lower():
                matched_name = p.player_name
                break
        
        if matched_name:
            print_player_scouting_card(analyzer, matched_name)
        else:
            print(f"\n[!] Player matching '{args.player}' not found. Available fielders:")
            for p in matrix:
                print(f" - {p.player_name}")
            print()

    if args.dashboard:
        print("[+] Starting Interactive Flask Web Dashboard Server on http://127.0.0.1:5000...")
        print("[+] Press Ctrl+C to terminate server.")
        from web_dashboard.app import run_server
        run_server(port=5000)

if __name__ == "__main__":
    main()

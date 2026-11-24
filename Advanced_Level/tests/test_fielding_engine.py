"""
test_fielding_engine.py
Automated unit test suite for ShadowFox Cricket Fielding Performance Analytics Engine.
"""

import unittest
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from models import PlayerFieldingStats, FieldingWeights
from data_collector import T20FieldingDataCollector
from analyzer import FieldingAnalyzer
from exporter import DatasetExporter

class TestFieldingEngine(unittest.TestCase):
    """Unit test cases verifying formula math, dataset integrity, SQLite DB schema, and Flask API."""

    def test_01_performance_formula(self):
        """Verify PS formula computation with known positive and negative inputs."""
        stats = PlayerFieldingStats(
            player_name="Test Player",
            primary_position="Cover",
            role="Fielder",
            clean_picks=10,       # 10 * 1 = 10
            good_throws=8,        # 8 * 1 = 8
            catches=2,            # 2 * 3 = 6
            dropped_catches=1,    # 1 * -3 = -3
            stumpings=1,          # 1 * 3 = 3
            run_outs=1,           # 1 * 3 = 3
            missed_run_outs=1,    # 1 * -2 = -2
            direct_hits=2,        # 2 * 2 = 4
            runs_saved=5          # 5 * 1 = 5
        )
        # Expected PS = 10 + 8 + 6 - 3 + 3 + 3 - 2 + 4 + 5 = 34
        ps = stats.calculate_performance_score()
        self.assertEqual(ps, 34)

    def test_02_delivery_count(self):
        """Assert simulated dataset has 120 legal deliveries and schema columns."""
        collector = T20FieldingDataCollector()
        events = collector.generate_ball_by_ball_logs()
        self.assertEqual(len(events), 120)

    def test_03_player_count(self):
        """Assert exact 11-player count in matrix and top performers match elite subjects."""
        collector = T20FieldingDataCollector()
        events = collector.generate_ball_by_ball_logs()
        analyzer = FieldingAnalyzer(events)
        matrix = analyzer.get_performance_matrix()

        self.assertEqual(len(matrix), 11)
        self.assertEqual(matrix[0].player_name, "MS Dhoni (WK)")
        self.assertEqual(matrix[0].performance_score, 35)
        self.assertEqual(matrix[1].player_name, "Virat Kohli (C)")
        self.assertEqual(matrix[1].performance_score, 30)
        self.assertEqual(matrix[2].player_name, "Hardik Pandya")
        self.assertEqual(matrix[2].performance_score, 26)

    def test_04_database_integrity(self):
        """Assert SQLite db connection, table creation, and exact row matching."""
        collector = T20FieldingDataCollector()
        events = collector.generate_ball_by_ball_logs()
        analyzer = FieldingAnalyzer(events)
        matrix = analyzer.get_performance_matrix()

        test_dir = os.path.join(BASE_DIR, "dataset")
        exporter = DatasetExporter(output_dir=test_dir)
        exporter.export_all(events, matrix)

        db_path = exporter.db_path
        self.assertTrue(os.path.exists(db_path))

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM ball_by_ball_fielding")
        logs_count = cur.fetchone()[0]
        self.assertEqual(logs_count, 120)

        cur.execute("SELECT COUNT(*) FROM player_performance_matrix")
        matrix_count = cur.fetchone()[0]
        self.assertEqual(matrix_count, 11)
        conn.close()

    def test_05_dashboard_api(self):
        """Use Flask test client to verify HTTP 200 OK JSON responses on /api/data."""
        web_dir = os.path.join(BASE_DIR, "web_dashboard")
        sys.path.insert(0, web_dir)
        from app import app
        
        client = app.test_client()
        response = client.get("/api/data")
        self.assertEqual(response.status_code, 200)
        
        json_data = response.get_json()
        self.assertIn("kpis", json_data)
        self.assertIn("leaderboard", json_data)
        self.assertEqual(json_data["kpis"]["top_fielder"], "MS Dhoni (WK)")
        self.assertEqual(json_data["kpis"]["top_ps"], 35)

if __name__ == "__main__":
    unittest.main()

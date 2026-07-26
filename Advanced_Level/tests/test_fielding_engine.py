"""
test_fielding_engine.py
Automated Unit Test Suite testing PS math formula, data collector, SQLite database integrity, and Flask web API.
"""

import os
import sys
import unittest
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import PlayerFieldingStats, FieldingWeights
from data_collector import T20FieldingDataCollector
from analyzer import FieldingAnalyzer
from exporter import DatasetExporter
from web_dashboard.app import app

class TestFieldingEngine(unittest.TestCase):
    """5 Automated unit test checks for India vs England 2017 Fielding Analytics Engine."""

    def setUp(self):
        """Pre-test setup generating dataset for database and API tests."""
        self.collector = T20FieldingDataCollector()
        self.events = self.collector.generate_ball_by_ball_logs()
        self.analyzer = FieldingAnalyzer(self.events)
        self.matrix = self.analyzer.get_performance_matrix()
        self.exporter = DatasetExporter(output_dir="dataset_test")
        self.paths = self.exporter.export_all(self.events, self.matrix)

    def tearDown(self):
        """Cleanup test dataset directory."""
        if os.path.exists("dataset_test"):
            import shutil
            shutil.rmtree("dataset_test")

    def test_01_performance_formula(self):
        """test_01_performance_formula: Verify PS formula computation with known positive and negative inputs."""
        p1 = PlayerFieldingStats(
            player_name="MS Dhoni (WK)", primary_position="Wicketkeeper", role="Wicketkeeper",
            clean_picks=10, good_throws=8, catches=2, dropped_catches=0,
            stumpings=2, run_outs=1, missed_run_outs=0, direct_hits=0,
            runs_saved=2
        )
        # PS = (10*1) + (8*1) + (2*3) + (0*-3) + (2*3) + (1*3) + (0*-2) + (0*2) + 2
        # PS = 10 + 8 + 6 + 0 + 6 + 3 + 0 + 0 + 2 = 35
        self.assertEqual(p1.calculate_performance_score(), 35)

        p2 = PlayerFieldingStats(
            player_name="Test Player B", primary_position="Cover", role="Infield",
            clean_picks=2, good_throws=1, catches=1, dropped_catches=2,
            stumpings=0, run_outs=0, missed_run_outs=1, direct_hits=0,
            runs_saved=-3
        )
        # PS = (2*1) + (1*1) + (1*3) + (2*-3) + (0*3) + (0*3) + (1*-2) + (0*2) + (-3)
        # PS = 2 + 1 + 3 - 6 + 0 + 0 - 2 + 0 - 3 = -5
        self.assertEqual(p2.calculate_performance_score(), -5)

    def test_02_delivery_count(self):
        """test_02_delivery_count: Assert simulated dataset has 120 legal deliveries and schema columns."""
        self.assertEqual(len(self.events), 120)
        
        first_event = self.events[0]
        event_dict = first_event.as_dict()
        required_keys = ['match_number', 'innings', 'team', 'over', 'ball', 'batter', 'bowler',
                         'fielder', 'position', 'short_description', 'pick', 'throw', 'runs_saved', 'venue']
        for k in required_keys:
            self.assertIn(k, event_dict)

    def test_03_player_count(self):
        """test_03_player_count: Assert exact 11-player count in matrix and top performers match elite subjects."""
        self.assertEqual(len(self.matrix), 11)
        
        top_1 = self.matrix[0]
        top_2 = self.matrix[1]
        top_3 = self.matrix[2]

        self.assertIn("Dhoni", top_1.player_name)
        self.assertEqual(top_1.performance_score, 35)

        self.assertIn("Kohli", top_2.player_name)
        self.assertEqual(top_2.performance_score, 30)

        self.assertIn("Pandya", top_3.player_name)
        self.assertEqual(top_3.performance_score, 26)

    def test_04_database_integrity(self):
        """test_04_database_integrity: Assert SQLite db connection, table creation, and exact row matching."""
        db_path = self.paths['db_path']
        self.assertTrue(os.path.exists(db_path))

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("ball_by_ball_fielding", tables)
            self.assertIn("player_performance_matrix", tables)

            cursor.execute("SELECT COUNT(*) FROM ball_by_ball_fielding")
            logs_count = cursor.fetchone()[0]
            self.assertEqual(logs_count, 120)

            cursor.execute("SELECT COUNT(*) FROM player_performance_matrix")
            matrix_count = cursor.fetchone()[0]
            self.assertEqual(matrix_count, 11)
        finally:
            conn.close()

    def test_05_dashboard_api(self):
        """test_05_dashboard_api: Use Flask test client to verify HTTP 200 OK JSON responses on /api/data."""
        production_exporter = DatasetExporter(output_dir="dataset")
        production_exporter.export_all(self.events, self.matrix)

        client = app.test_client()
        response = client.get('/api/data')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertIn('kpis', data)
        self.assertIn('leaderboard', data)
        self.assertIn('logs', data)
        self.assertIn('scouting', data)
        self.assertEqual(len(data['leaderboard']), 11)

if __name__ == "__main__":
    unittest.main()

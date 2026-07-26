"""
exporter.py
DatasetExporter module persisting fielding analytics to SQLite database and CSV files.
"""

import os
import sqlite3
from typing import List
import pandas as pd
from models import FieldingEvent, PlayerFieldingStats

class DatasetExporter:
    """Exports fielding analysis datasets for India vs England 2017 3rd T20I."""

    def __init__(self, output_dir: str = "dataset"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.db_path = os.path.join(self.output_dir, "india_england_2017_t20_fielding.db")
        self.log_csv_path = os.path.join(self.output_dir, "India_England_2017_Ball_By_Ball_Fielding.csv")
        self.matrix_csv_path = os.path.join(self.output_dir, "India_England_2017_Player_Performance.csv")

    def export_all(self, events: List[FieldingEvent], player_matrix: List[PlayerFieldingStats]):
        """Exports both ball-by-ball logs and player matrix to CSV and SQLite database."""
        logs_df = pd.DataFrame([e.as_dict() for e in events])
        matrix_df = pd.DataFrame([p.as_dict() for p in player_matrix])

        # 1. Export CSV files
        logs_df.to_csv(self.log_csv_path, index=False)
        matrix_df.to_csv(self.matrix_csv_path, index=False)

        # 2. Export SQLite database tables
        conn = sqlite3.connect(self.db_path)
        try:
            logs_df.to_sql("ball_by_ball_fielding", conn, if_exists="replace", index=False)
            matrix_df.to_sql("player_performance_matrix", conn, if_exists="replace", index=False)
            conn.commit()
        finally:
            conn.close()

        return {
            "db_path": self.db_path,
            "log_csv": self.log_csv_path,
            "matrix_csv": self.matrix_csv_path
        }

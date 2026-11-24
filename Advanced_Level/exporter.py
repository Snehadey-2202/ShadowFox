"""
exporter.py
DatasetExporter module persisting ball-by-ball events and performance matrix into SQLite database and CSV files.
"""

import os
import sqlite3
import pandas as pd
from typing import List
from models import FieldingEvent, PlayerFieldingStats

class DatasetExporter:
    """Exports structured datasets into SQLite database tables and CSV files."""

    def __init__(self, output_dir: str = "dataset"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.db_path = os.path.join(self.output_dir, "india_england_2017_t20_fielding.db")
        self.log_csv_path = os.path.join(self.output_dir, "India_England_2017_Ball_By_Ball_Fielding.csv")
        self.matrix_csv_path = os.path.join(self.output_dir, "India_England_2017_Player_Performance.csv")

    def export_all(self, events: List[FieldingEvent], player_matrix: List[PlayerFieldingStats]):
        """Exports both SQLite relational database tables and CSV files."""
        self.export_to_csv(events, player_matrix)
        self.export_to_sqlite(events, player_matrix)

    def export_to_csv(self, events: List[FieldingEvent], player_matrix: List[PlayerFieldingStats]):
        """Saves CSV files for ball-by-ball logs and player matrix."""
        logs_df = pd.DataFrame([e.as_dict() for e in events])
        logs_df.to_csv(self.log_csv_path, index=False)

        matrix_df = pd.DataFrame([p.as_dict() for p in player_matrix])
        matrix_df.to_csv(self.matrix_csv_path, index=False)

    def export_to_sqlite(self, events: List[FieldingEvent], player_matrix: List[PlayerFieldingStats]):
        """Creates SQLite database with tables: ball_by_ball_fielding & player_performance_matrix."""
        logs_df = pd.DataFrame([e.as_dict() for e in events])
        matrix_df = pd.DataFrame([p.as_dict() for p in player_matrix])

        conn = sqlite3.connect(self.db_path)
        try:
            logs_df.to_sql("ball_by_ball_fielding", conn, if_exists="replace", index=False)
            matrix_df.to_sql("player_performance_matrix", conn, if_exists="replace", index=False)
            conn.commit()
        finally:
            conn.close()

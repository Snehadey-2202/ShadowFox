"""
visualizer.py
FieldingVisualizer module rendering 5 dark-themed, large-scale high-res statistical charts for India vs England 2017 T20I.
"""

import os
from typing import List, Dict, Any
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from models import PlayerFieldingStats, FieldingEvent

class FieldingVisualizer:
    """Generates 5 large-scale high-resolution statistical charts saved to dataset/charts/."""

    def __init__(self, charts_dir: str = "dataset/charts"):
        self.charts_dir = charts_dir
        os.makedirs(self.charts_dir, exist_ok=True)
        plt.style.use('dark_background')
        self.colors = {
            'background': '#0B0F19',
            'card': '#1E293B',
            'primary': '#3B82F6',
            'emerald': '#10B981',
            'amber': '#F59E0B',
            'rose': '#EF4444',
            'indigo': '#6366F1',
            'text': '#F8FAFC'
        }

    def generate_all_charts(self, player_matrix: List[PlayerFieldingStats], zone_summary: Dict[str, Dict[str, int]], events: List[FieldingEvent]) -> List[str]:
        """Generates all 5 large-scale statistical charts and returns saved image filepaths."""
        paths = []
        paths.append(self.plot_team_performance_scores(player_matrix))
        paths.append(self.plot_target_player_comparison(player_matrix))
        paths.append(self.plot_fielding_zone_analysis(zone_summary))
        paths.append(self.plot_runs_saved_analysis(player_matrix))
        paths.append(self.plot_dismissal_breakdown(player_matrix))
        return paths

    def plot_team_performance_scores(self, player_matrix: List[PlayerFieldingStats]) -> str:
        """Chart 1: Large horizontal bar chart of Performance Scores for all 11 fielders."""
        df = pd.DataFrame([p.as_dict() for p in player_matrix])
        df = df.sort_values(by='performance_score', ascending=True)

        fig, ax = plt.subplots(figsize=(14, 8), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        bar_colors = []
        for name in df['player_name']:
            if "Dhoni" in name:
                bar_colors.append('#FBBF24')  # Amber #1
            elif "Kohli" in name:
                bar_colors.append('#38BDF8')  # Cyan #2
            elif "Pandya" in name:
                bar_colors.append('#34D399')  # Emerald #3
            else:
                bar_colors.append('#475569')  # Slate grey

        bars = ax.barh(df['player_name'], df['performance_score'], color=bar_colors, edgecolor='none', height=0.68)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.8, bar.get_y() + bar.get_height()/2, f'{int(width)} PS',
                    va='center', ha='left', color='#F8FAFC', fontweight='bold', fontsize=13)

        ax.set_title("India vs England 3rd T20I (2017) - Team Fielding Performance Scores (PS)",
                     fontsize=18, fontweight='bold', color='#38BDF8', pad=20)
        ax.set_xlabel("Empirical Performance Score (PS)", fontsize=14, color='#CBD5E1', labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
        ax.tick_params(colors='#CBD5E1', labelsize=13)
        plt.tight_layout()

        out_path = os.path.join(self.charts_dir, "team_performance_scores.png")
        plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
        plt.close(fig)
        return out_path

    def plot_target_player_comparison(self, player_matrix: List[PlayerFieldingStats]) -> str:
        """Chart 2: Large grouped metric breakdown for target subjects (MS Dhoni, Virat Kohli, Hardik Pandya)."""
        target_names = ["MS Dhoni (WK)", "Virat Kohli (C)", "Hardik Pandya"]
        matrix_dict = {p.player_name: p for p in player_matrix}
        target_stats = [matrix_dict[name] for name in target_names if name in matrix_dict]

        metrics = ['Clean Picks', 'Good Throws', 'Catches', 'Stumpings', 'Runs Saved']
        data = {
            'Metric': metrics,
            'MS Dhoni (WK)': [target_stats[0].clean_picks, target_stats[0].good_throws, target_stats[0].catches, target_stats[0].stumpings, target_stats[0].runs_saved],
            'Virat Kohli (C)': [target_stats[1].clean_picks, target_stats[1].good_throws, target_stats[1].catches, target_stats[1].stumpings, target_stats[1].runs_saved],
            'Hardik Pandya': [target_stats[2].clean_picks, target_stats[2].good_throws, target_stats[2].catches, target_stats[2].stumpings, target_stats[2].runs_saved]
        }
        
        df = pd.DataFrame(data)
        df_melted = df.melt(id_vars='Metric', var_name='Player', value_name='Count')

        fig, ax = plt.subplots(figsize=(14, 8), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        palette = {'MS Dhoni (WK)': '#FBBF24', 'Virat Kohli (C)': '#38BDF8', 'Hardik Pandya': '#34D399'}
        sns.barplot(data=df_melted, x='Metric', y='Count', hue='Player', palette=palette, ax=ax)

        ax.set_title("Target Players Metric Contribution Comparison (Dhoni vs. Kohli vs. Pandya)",
                     fontsize=18, fontweight='bold', color='#38BDF8', pad=20)
        ax.set_xlabel("Fielding Metric Category", fontsize=14, color='#CBD5E1', labelpad=10)
        ax.set_ylabel("Count / Net Runs", fontsize=14, color='#CBD5E1', labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
        ax.tick_params(colors='#CBD5E1', labelsize=13)
        ax.legend(facecolor='#1E293B', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=12)
        plt.tight_layout()

        out_path = os.path.join(self.charts_dir, "target_player_comparison.png")
        plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
        plt.close(fig)
        return out_path

    def plot_fielding_zone_analysis(self, zone_summary: Dict[str, Dict[str, int]]) -> str:
        """Chart 3: Large donut chart showing defensive territorial control by zone."""
        labels = list(zone_summary.keys())
        events_count = [zone_summary[z]['events'] for z in labels]

        fig, ax = plt.subplots(figsize=(12, 8), facecolor=self.colors['background'])
        colors = ['#38BDF8', '#34D399', '#FBBF24']

        wedges, texts, autotexts = ax.pie(
            events_count,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            textprops=dict(color='#F8FAFC', fontweight='bold', fontsize=13),
            wedgeprops=dict(width=0.42, edgecolor='#0B0F19')
        )

        for autotext in autotexts:
            autotext.set_color('#FFFFFF')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')

        ax.set_title("Defensive Territorial Coverage & Deliveries Monitored by Zone",
                     fontsize=18, fontweight='bold', color='#38BDF8', pad=20)
        plt.tight_layout()

        out_path = os.path.join(self.charts_dir, "fielding_zone_analysis.png")
        plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
        plt.close(fig)
        return out_path

    def plot_runs_saved_analysis(self, player_matrix: List[PlayerFieldingStats]) -> str:
        """Chart 4: Large bar chart comparing runs saved by player."""
        df = pd.DataFrame([p.as_dict() for p in player_matrix if p.runs_saved > 0])
        df = df.sort_values(by='runs_saved', ascending=False)

        fig, ax = plt.subplots(figsize=(12, 7), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        bars = ax.bar(df['player_name'], df['runs_saved'], color='#34D399', width=0.55)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.15, f'+{int(height)}',
                    ha='center', va='bottom', color='#F8FAFC', fontweight='bold', fontsize=13)

        ax.set_title("Net Runs Saved per Player (Restriction of Boundaries)",
                     fontsize=18, fontweight='bold', color='#38BDF8', pad=20)
        ax.set_ylabel("Runs Saved (+)", fontsize=14, color='#CBD5E1', labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
        ax.tick_params(colors='#CBD5E1', labelsize=13)
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()

        out_path = os.path.join(self.charts_dir, "runs_saved_analysis.png")
        plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
        plt.close(fig)
        return out_path

    def plot_dismissal_breakdown(self, player_matrix: List[PlayerFieldingStats]) -> str:
        """Chart 5: Large bar chart breakdown of fielding dismissals."""
        catches = sum(p.catches for p in player_matrix)
        stumpings = sum(p.stumpings for p in player_matrix)
        run_outs = sum(p.run_outs for p in player_matrix)

        categories = ['Catches', 'Stumpings', 'Run Outs']
        counts = [catches, stumpings, run_outs]

        fig, ax = plt.subplots(figsize=(12, 7), facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        bars = ax.bar(categories, counts, color=['#38BDF8', '#FBBF24', '#F87171'], width=0.5)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.15, f'{int(height)}',
                    ha='center', va='bottom', color='#F8FAFC', fontweight='bold', fontsize=14)

        ax.set_title("Fielding Dismissals Breakdown (India vs England 3rd T20I)",
                     fontsize=18, fontweight='bold', color='#38BDF8', pad=20)
        ax.set_ylabel("Total Dismissals", fontsize=14, color='#CBD5E1', labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
        ax.tick_params(colors='#CBD5E1', labelsize=13)
        plt.tight_layout()

        out_path = os.path.join(self.charts_dir, "dismissal_breakdown.png")
        plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
        plt.close(fig)
        return out_path

"""
analyzer.py
FieldingAnalyzer module performing metric aggregations, PS matrix sorting, and qualitative scouting evaluations.
"""

from typing import List, Dict, Any
from models import FieldingEvent, PlayerFieldingStats

class FieldingAnalyzer:
    """Aggregates fielding statistics, computes PS matrix, and generates tactical scouting reports."""

    def __init__(self, events: List[FieldingEvent]):
        self.events = events
        self.player_map: Dict[str, PlayerFieldingStats] = {}
        self._aggregate_events()

    def _aggregate_events(self):
        """Processes 120 delivery events and accumulates player stats."""
        player_roles = {
            "MS Dhoni (WK)": ("Wicketkeeper", "Wicketkeeper / Defensive Leader"),
            "Virat Kohli (C)": ("Long-on / Extra Cover", "Captain / Outfield Leader"),
            "Hardik Pandya": ("Deep Mid-wicket", "Outfield / Athletic Saver"),
            "Suresh Raina": ("Point", "Infield Specialist"),
            "KL Rahul": ("Cover", "Infield Fielder"),
            "Yuvraj Singh": ("Mid-wicket", "Infield Fielder"),
            "Rishabh Pant": ("Mid-off", "Infield Fielder"),
            "Amit Mishra": ("Short Fine Leg", "Infield Fielder"),
            "Jasprit Bumrah": ("Mid-on", "Infield Fielder"),
            "Ashish Nehra": ("Fine Leg", "Outfield Fielder"),
            "Yuzvendra Chahal": ("Deep Cover", "Outfield Fielder")
        }

        for ev in self.events:
            name = ev.fielder
            if name not in self.player_map:
                pos, role = player_roles.get(name, (ev.position, "Fielder"))
                self.player_map[name] = PlayerFieldingStats(
                    player_name=name,
                    primary_position=pos,
                    role=role
                )

            stats = self.player_map[name]
            stats.total_deliveries += 1
            stats.clean_picks += ev.pick
            stats.good_throws += ev.throw
            stats.catches += ev.catches
            stats.dropped_catches += ev.dropped_catches
            stats.stumpings += ev.stumpings
            stats.run_outs += ev.run_outs
            stats.missed_run_outs += ev.missed_run_outs
            stats.direct_hits += ev.direct_hits
            stats.runs_saved += ev.runs_saved

        # Calculate final PS for all players
        for stats in self.player_map.values():
            stats.calculate_performance_score()

    def get_performance_matrix(self) -> List[PlayerFieldingStats]:
        """Returns player performance matrix sorted in descending order of Performance Score (PS)."""
        matrix = list(self.player_map.values())
        matrix.sort(key=lambda p: p.performance_score, reverse=True)
        return matrix

    def get_zone_summary(self) -> Dict[str, Dict[str, int]]:
        """Returns breakdown of fielding events across zones (Wicketkeeping, Infield, Outfield)."""
        summary = {
            "Wicketkeeping": {"events": 0, "runs_saved": 0, "dismissals": 0},
            "Infield": {"events": 0, "runs_saved": 0, "dismissals": 0},
            "Outfield": {"events": 0, "runs_saved": 0, "dismissals": 0}
        }

        for ev in self.events:
            pos = ev.position
            if "Wicketkeeper" in pos:
                z = "Wicketkeeping"
            elif "Deep" in pos or "Long" in pos or "Fine Leg" in pos:
                z = "Outfield"
            else:
                z = "Infield"

            summary[z]["events"] += 1
            summary[z]["runs_saved"] += ev.runs_saved
            summary[z]["dismissals"] += (ev.catches + ev.stumpings + ev.run_outs)

        return summary

    def get_scouting_report(self, player_name: str) -> Dict[str, Any]:
        """Generates detailed scouting card for MS Dhoni, Virat Kohli, or Hardik Pandya."""
        matrix = self.get_performance_matrix()
        player_stats = self.player_map.get(player_name)

        rank = 1
        for idx, p in enumerate(matrix):
            if p.player_name == player_name:
                rank = idx + 1
                break

        if "Dhoni" in player_name:
            report = {
                "player_name": player_name,
                "match_rank": rank,
                "role": "Wicketkeeper & Defensive Leader",
                "stats": player_stats.as_dict(),
                "match_highlight": "Executed sub-second stumpings off Chahal (7.4 over) and Mishra (13.6 over), plus a rapid unassisted run-out (14.2 over).",
                "key_strengths": [
                    "Lightning-fast hand-eye coordination behind the stumps",
                    "Sub-second stumping reaction speed off wrist spinners",
                    "Elite anticipated positioning and collection stability",
                    "Flawless tactical guidance directing inner ring fielders"
                ],
                "coaching_points": [
                    "Maintain current glove position and stance angle",
                    "Continue guiding spinner field placements in overs 7-15"
                ]
            }
        elif "Kohli" in player_name:
            report = {
                "player_name": player_name,
                "match_rank": rank,
                "role": "Captain & Outfield Leader",
                "stats": player_stats.as_dict(),
                "match_highlight": "High pressure boundary catch at Long-on (16.1 over) and a razor-sharp direct hit from Extra Cover (17.3 over).",
                "key_strengths": [
                    "Outstanding high-ball tracking under stadium lights",
                    "Dynamic pick-and-throw speed inside 30-yard circle",
                    "Relentless vocal leadership and pressure creation",
                    "Proactive boundary cutting restricting extra runs"
                ],
                "coaching_points": [
                    "Maintain athletic posture when charging from Extra Cover",
                    "Continue setting high fielding standards in death overs"
                ]
            }
        elif "Pandya" in player_name:
            report = {
                "player_name": player_name,
                "match_rank": rank,
                "role": "Outfield Athletic Saver",
                "stats": player_stats.as_dict(),
                "match_highlight": "Spectacular 25-yard diving boundary save at Deep Mid-wicket saving 3 runs (19.2 over) plus 2 clean catches.",
                "key_strengths": [
                    "Elite ground speed and boundary cover radius",
                    "Exceptional sliding technique along boundary cushions",
                    "Strong arm capability with deep flat throws",
                    "High boundary boundary catch reliability"
                ],
                "coaching_points": [
                    "Work on throw accuracy towards keeper end from deep boundary",
                    "Maintain sliding discipline near boundary rope"
                ]
            }
        else:
            report = {
                "player_name": player_name,
                "match_rank": rank,
                "role": "Fielder",
                "stats": player_stats.as_dict() if player_stats else {},
                "match_highlight": "Solid defensive contribution.",
                "key_strengths": ["Clean picking", "Consistent throwing"],
                "coaching_points": ["Maintain fielding focus"]
            }

        return report

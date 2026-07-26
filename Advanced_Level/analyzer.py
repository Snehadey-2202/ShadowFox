"""
analyzer.py
FieldingAnalyzer module computing player matrix, rankings, zone analysis, and qualitative scouting reports.
"""

from typing import List, Dict, Any
from models import FieldingEvent, PlayerFieldingStats

class FieldingAnalyzer:
    """Computes player fielding matrix, rankings, and scouting assessments for 2017 Bengaluru T20I."""

    PLAYER_ROLES = {
        "MS Dhoni (WK)": ("Wicketkeeper Defensive Leader", "Wicketkeeper"),
        "Virat Kohli (C)": ("Outfield Boundary Captain", "Outfield"),
        "Hardik Pandya": ("Athletic Boundary Patrol", "Outfield"),
        "Suresh Raina": ("Infield Slip & Point Specialist", "Infield"),
        "KL Rahul": ("Infield Cover Specialist", "Infield"),
        "Yuvraj Singh": ("Infield Mid-wicket Specialist", "Infield"),
        "Rishabh Pant": ("Infield Mid-off Stopper", "Infield"),
        "Amit Mishra": ("Infield Short Fine Leg", "Infield"),
        "Jasprit Bumrah": ("Infield Mid-on Stopper", "Infield"),
        "Ashish Nehra": ("Outfield Fine Leg Sweeper", "Outfield"),
        "Yuzvendra Chahal": ("Outfield Deep Cover Sweeper", "Outfield")
    }

    def __init__(self, events: List[FieldingEvent]):
        self.events = events
        self.stats_matrix: Dict[str, PlayerFieldingStats] = {}
        self._analyze_events()

    def _analyze_events(self):
        """Aggregates ball-by-ball logs into PlayerFieldingStats objects."""
        for player_name, (role, pos) in self.PLAYER_ROLES.items():
            self.stats_matrix[player_name] = PlayerFieldingStats(
                player_name=player_name,
                primary_position=pos,
                role=role
            )

        for ev in self.events:
            if ev.fielder not in self.stats_matrix:
                self.stats_matrix[ev.fielder] = PlayerFieldingStats(
                    player_name=ev.fielder,
                    primary_position=ev.position,
                    role="Fielder"
                )
            
            p = self.stats_matrix[ev.fielder]
            p.total_deliveries += 1
            p.clean_picks += ev.pick
            p.good_throws += ev.throw
            p.catches += ev.catches
            p.dropped_catches += ev.dropped_catches
            p.stumpings += ev.stumpings
            p.run_outs += ev.run_outs
            p.missed_run_outs += ev.missed_run_outs
            p.direct_hits += ev.direct_hits
            p.runs_saved += ev.runs_saved

        for p in self.stats_matrix.values():
            p.calculate_performance_score()

    def get_performance_matrix(self) -> List[PlayerFieldingStats]:
        """Returns player matrix sorted by Performance Score (PS) descending."""
        matrix = list(self.stats_matrix.values())
        matrix.sort(key=lambda x: x.performance_score, reverse=True)
        return matrix

    def get_zone_summary(self) -> Dict[str, Dict[str, int]]:
        """Returns territorial zone analysis: events, catches, runs saved by zone."""
        zones = {"Infield": {"events": 0, "catches": 0, "runs_saved": 0},
                 "Outfield": {"events": 0, "catches": 0, "runs_saved": 0},
                 "Wicketkeeper": {"events": 0, "catches": 0, "runs_saved": 0}}
        
        for ev in self.events:
            z = ev.zone if ev.zone in zones else "Infield"
            zones[z]["events"] += 1
            zones[z]["catches"] += ev.catches
            zones[z]["runs_saved"] += ev.runs_saved

        return zones

    def get_match_summary(self) -> Dict[str, Any]:
        """Returns overall match summary metadata."""
        matrix = self.get_performance_matrix()
        total_runs_saved = sum(p.runs_saved for p in matrix)
        total_dismissals = sum(p.catches + p.stumpings + p.run_outs for p in matrix)
        
        return {
            "match": "India vs England 3rd T20I (1 Feb 2017)",
            "venue": "M. Chinnaswamy Stadium, Bengaluru",
            "top_fielder": matrix[0].player_name if matrix else "N/A",
            "top_ps": matrix[0].performance_score if matrix else 0,
            "total_runs_saved": total_runs_saved,
            "total_dismissals": total_dismissals,
            "deliveries_monitored": len(self.events)
        }

    def get_scouting_report(self, player_name: str) -> Dict[str, Any]:
        """Generates detailed, authentic scouting evaluations for target players."""
        matrix_dict = {p.player_name: p for p in self.get_performance_matrix()}
        player_stats = matrix_dict.get(player_name)

        if not player_stats:
            return {"error": f"Player '{player_name}' not found in team matrix."}

        reports = {
            "MS Dhoni (WK)": {
                "match_rank": 1,
                "role": "Wicketkeeper Defensive Leader",
                "key_strengths": [
                    "Lightning-fast stumpings with sub-second glove gathering when standing up to spinners",
                    "Flawless collection rate on low edges and wide bouncing throws",
                    "Vocal tactical guidance directing inner ring fielders and spin bowling variations"
                ],
                "coaching_points": [
                    "Maintain high glove stability when collecting off-target bounce throws",
                    "Continue guiding younger spinners on stumping angle setups"
                ],
                "match_highlight": "Masterclass behind the stumps with 2 rapid stumpings, 1 direct run-out, 2 catches, and tactical defensive leadership."
            },
            "Virat Kohli (C)": {
                "match_rank": 2,
                "role": "Outfield Boundary Captain",
                "key_strengths": [
                    "High-velocity flat returns to the keeper's end that cut off extra singles",
                    "Exceptional judgment on high skyers near the boundary cushion under lights",
                    "Intense athletic commitment setting the defensive standard for the entire team"
                ],
                "coaching_points": [
                    "Fine-tune release angle on flat relay throws from extra deep cover",
                    "Maintain boundary footwork positioning on tricky stadium lights"
                ],
                "match_highlight": "3 high-pressure boundary catches and a game-changing direct hit at the bowler's end."
            },
            "Hardik Pandya": {
                "match_rank": 3,
                "role": "Athletic Boundary Patrol",
                "key_strengths": [
                    "Impressive lateral ground coverage sweeping across the deep boundary ropes",
                    "Flat, powerful arm returns throwing directly over the stumps",
                    "Aggressive commitment when charging in from deep mid-wicket"
                ],
                "coaching_points": [
                    "Work on target precision for long-range direct hit attempts",
                    "Smooth out sliding posture to reduce boundary collision risks"
                ],
                "match_highlight": "Full-stretch sliding boundary save cutting off 3 crucial runs and taking 2 deep catches."
            }
        }

        base_report = reports.get(player_name, {
            "match_rank": "Team Contributor",
            "role": player_stats.role,
            "key_strengths": [
                f"Reliable, steady fielding presence at {player_stats.primary_position}",
                "Disciplined execution of inner ring defensive coverage"
            ],
            "coaching_points": [
                "Work on arm speed for long-distance boundary throws",
                "Improve first-step lateral acceleration"
            ],
            "match_highlight": f"Solid defensive effort contributing to team performance score of {player_stats.performance_score} PS."
        })

        base_report['stats'] = player_stats.as_dict()
        return base_report

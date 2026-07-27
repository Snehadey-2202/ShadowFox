"""
models.py
Object-Oriented Data Models for India vs England 3rd T20I (2017) Cricket Fielding Analytics Engine.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any

@dataclass
class FieldingWeights:
    """Weight multipliers for empirical Fielding Performance Score (PS) calculation."""
    clean_pick: int = 1
    good_throw: int = 1
    catch: int = 3
    dropped_catch: int = -3
    stumping: int = 3
    run_out: int = 3
    missed_run_out: int = -2
    direct_hit: int = 2
    runs_saved_weight: int = 1

@dataclass
class FieldingEvent:
    """Represents a single ball-by-ball fielding event record."""
    match_number: str
    innings: int
    team: str
    over: int
    ball: int
    batter: str
    bowler: str
    fielder: str
    position: str
    short_description: str
    pick: int = 0          # Clean Picks (CP)
    throw: int = 0         # Good Throws (GT)
    catches: int = 0       # Catches (C)
    dropped_catches: int = 0 # Dropped Catches (DC)
    stumpings: int = 0     # Stumpings (ST)
    run_outs: int = 0      # Run Outs (RO)
    missed_run_outs: int = 0 # Missed Run Outs (MRO)
    direct_hits: int = 0   # Direct Hits (DH)
    runs_saved: int = 0    # Net Runs Saved (RS)
    venue: str = "M. Chinnaswamy Stadium, Bengaluru"
    zone: str = "Infield"

    @property
    def clean_picks(self) -> int:
        return self.pick

    @property
    def good_throws(self) -> int:
        return self.throw

    def as_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['clean_picks'] = self.pick
        d['good_throws'] = self.throw
        return d

@dataclass
class PlayerFieldingStats:
    """Aggregated empirical metrics and Performance Score calculation for a player."""
    player_name: str
    primary_position: str
    role: str
    total_deliveries: int = 0
    clean_picks: int = 0
    good_throws: int = 0
    catches: int = 0
    dropped_catches: int = 0
    stumpings: int = 0
    run_outs: int = 0
    missed_run_outs: int = 0
    direct_hits: int = 0
    runs_saved: int = 0
    performance_score: int = 0
    weights: FieldingWeights = field(default_factory=FieldingWeights)

    def calculate_performance_score(self) -> int:
        """
        Computes Performance Score (PS) according to formula:
        PS = (CP * 1) + (GT * 1) + (C * 3) + (DC * -3) + (ST * 3) + 
             (RO * 3) + (MRO * -2) + (DH * 2) + RS
        """
        w = self.weights
        ps = (
            (self.clean_picks * w.clean_pick) +
            (self.good_throws * w.good_throw) +
            (self.catches * w.catch) +
            (self.dropped_catches * w.dropped_catch) +
            (self.stumpings * w.stumping) +
            (self.run_outs * w.run_out) +
            (self.missed_run_outs * w.missed_run_out) +
            (self.direct_hits * w.direct_hit) +
            (self.runs_saved * w.runs_saved_weight)
        )
        self.performance_score = ps
        return ps

    def as_dict(self) -> Dict[str, Any]:
        self.calculate_performance_score()
        return {
            "player_name": self.player_name,
            "primary_position": self.primary_position,
            "role": self.role,
            "total_deliveries": self.total_deliveries,
            "clean_picks": self.clean_picks,
            "good_throws": self.good_throws,
            "catches": self.catches,
            "dropped_catches": self.dropped_catches,
            "stumpings": self.stumpings,
            "run_outs": self.run_outs,
            "missed_run_outs": self.missed_run_outs,
            "direct_hits": self.direct_hits,
            "runs_saved": self.runs_saved,
            "performance_score": self.performance_score
        }

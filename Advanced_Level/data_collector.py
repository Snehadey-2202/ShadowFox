"""
data_collector.py
T20 fielding data collector simulating 120 legal deliveries for India vs England 3rd T20I (1 Feb 2017 at Bengaluru).
"""

from typing import List
from models import FieldingEvent

class T20FieldingDataCollector:
    """Compiles ball-by-ball fielding event logs for England's Innings with natural match commentary."""

    def __init__(self):
        self.match_number = "3rd T20I"
        self.innings = 2
        self.team = "India"
        self.opponent = "England"
        self.venue = "M. Chinnaswamy Stadium, Bengaluru"

    def generate_ball_by_ball_logs(self) -> List[FieldingEvent]:
        """
        Generates 120 legal delivery fielding events (20 overs) for India's 11 fielders.
        Authentic match events:
        - MS Dhoni: Wicketkeeping masterclass, 2 stumpings, 1 run-out, 2 catches (35 PS, Rank #1)
        - Virat Kohli: Boundary leadership, 3 catches, 1 direct hit (30 PS, Rank #2)
        - Hardik Pandya: Athletic boundary sliding saves, 2 catches (26 PS, Rank #3)
        """
        events: List[FieldingEvent] = []

        player_info = {
            "MS Dhoni (WK)": ("Wicketkeeper", "Wicketkeeper"),
            "Virat Kohli (C)": ("Long-on / Extra Cover", "Outfield"),
            "Hardik Pandya": ("Deep Mid-wicket", "Outfield"),
            "Suresh Raina": ("Point", "Infield"),
            "KL Rahul": ("Cover", "Infield"),
            "Yuvraj Singh": ("Mid-wicket", "Infield"),
            "Rishabh Pant": ("Mid-off", "Infield"),
            "Amit Mishra": ("Short Fine Leg", "Infield"),
            "Jasprit Bumrah": ("Mid-on", "Infield"),
            "Ashish Nehra": ("Fine Leg", "Outfield"),
            "Yuzvendra Chahal": ("Deep Cover", "Outfield")
        }

        # Quotas for remaining routine actions after accounting for match highlights
        routine_quotas = {
            "MS Dhoni (WK)": {"cp": 6, "gt": 6, "c": 2, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Virat Kohli (C)": {"cp": 5, "gt": 6, "c": 2, "st": 0, "ro": 0, "dh": 0, "rs": 4},
            "Hardik Pandya": {"cp": 6, "gt": 5, "c": 2, "st": 0, "ro": 0, "dh": 0, "rs": 4},
            "Suresh Raina": {"cp": 6, "gt": 6, "c": 2, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "KL Rahul": {"cp": 5, "gt": 4, "c": 2, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Yuvraj Singh": {"cp": 4, "gt": 5, "c": 1, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Rishabh Pant": {"cp": 4, "gt": 3, "c": 1, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Amit Mishra": {"cp": 3, "gt": 2, "c": 1, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Jasprit Bumrah": {"cp": 3, "gt": 3, "c": 0, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Ashish Nehra": {"cp": 3, "gt": 2, "c": 0, "st": 0, "ro": 0, "dh": 0, "rs": 0},
            "Yuzvendra Chahal": {"cp": 2, "gt": 2, "c": 0, "st": 0, "ro": 0, "dh": 0, "rs": 0}
        }

        player_list = list(player_info.keys())
        england_batters = ["Jason Roy", "Sam Billings", "Joe Root", "Eoin Morgan", "Ben Stokes", "Jos Buttler", "Moeen Ali", "Chris Jordan", "Liam Plunkett", "Adil Rashid", "Tymal Mills"]
        indian_bowlers = ["Ashish Nehra", "Jasprit Bumrah", "Yuzvendra Chahal", "Hardik Pandya", "Amit Mishra"]

        catch_phrases = [
            "taken cleanly under pressure",
            "plucked safely out of the air",
            "judged nicely near the boundary cushion",
            "secure collection with soft hands",
            "swallowed safely without a spill"
        ]
        
        save_phrases = [
            "diving effort cutting off a certain single",
            "full length dive restricting extra runs",
            "sliding boundary stop keeping batter to one",
            "quick boundary sweep saving vital runs"
        ]

        pick_throw_phrases = [
            "clean pick on the run and quick return throw",
            "swooped in rapidly, firing back to the keeper",
            "neat collection and controlled release",
            "gathered smoothly and whipped back to bowler"
        ]

        routine_phrases = [
            "routine collection and steady return",
            "standard fielding coverage",
            "watched carefully into the hands",
            "fielded cleanly without fuss"
        ]

        ball_counter = 0

        for over in range(1, 21):
            for ball in range(1, 7):
                ball_counter += 1
                batter = england_batters[(over // 2) % len(england_batters)]
                bowler = indian_bowlers[over % len(indian_bowlers)]

                # Highlight Balls
                if over == 7 and ball == 4:
                    fielder = "MS Dhoni (WK)"
                    pos, zone = player_info[fielder]
                    desc = "Sensational sub-second stumping! Dhoni collects Chahal's leg-break cleanly and whips off bails before Billings can recover."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 0, 0, 1, 0, 0, 0, 1
                elif over == 13 and ball == 6:
                    fielder = "MS Dhoni (WK)"
                    pos, zone = player_info[fielder]
                    desc = "Masterclass behind the stumps! Low bounce gathered effortlessly off Mishra's wrong-un for a sharp stumping."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 0, 0, 1, 0, 0, 0, 1
                elif over == 14 and ball == 2:
                    fielder = "MS Dhoni (WK)"
                    pos, zone = player_info[fielder]
                    desc = "Rapid underarm flick! Dhoni gathers the wide throw in a single motion and dislodges bails for an unassisted run-out."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 0, 0, 0, 1, 0, 0, 0
                elif over == 16 and ball == 1:
                    fielder = "Virat Kohli (C)"
                    pos, zone = player_info[fielder]
                    desc = "Captain's catch! High skyer judged flawlessly right inside the Long-on boundary rope under heavy lights."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 1, 0, 0, 0, 0, 0, 0
                elif over == 17 and ball == 3:
                    fielder = "Virat Kohli (C)"
                    pos, zone = player_info[fielder]
                    desc = "Bullseye! Kohli charges in from Extra Cover, picks cleanly on the run, and breaks the stumps at the bowler's end."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 0, 0, 0, 0, 0, 1, 0
                elif over == 19 and ball == 2:
                    fielder = "Hardik Pandya"
                    pos, zone = player_info[fielder]
                    desc = "Outstanding athleticism! Pandya sprints 25 yards across deep mid-wicket, dives full length and saves 3 crucial boundary runs."
                    cp, gt, c, dc, st, ro, mro, dh, rs = 1, 1, 0, 0, 0, 0, 0, 0, 3
                else:
                    selected = None
                    for offset in range(len(player_list)):
                        candidate = player_list[(ball_counter + offset) % len(player_list)]
                        q = routine_quotas[candidate]
                        if q['cp'] > 0 or q['gt'] > 0 or q['c'] > 0 or q['rs'] > 0:
                            selected = candidate
                            break

                    if not selected:
                        selected = player_list[ball_counter % len(player_list)]

                    fielder = selected
                    pos, zone = player_info[fielder]
                    q = routine_quotas[fielder]

                    cp = 1 if q['cp'] > 0 else 0
                    gt = 1 if q['gt'] > 0 else 0
                    c = 1 if q['c'] > 0 else 0
                    dc = st = ro = mro = dh = 0
                    rs = 1 if q['rs'] > 0 else 0

                    if cp: q['cp'] -= 1
                    if gt: q['gt'] -= 1
                    if c: q['c'] -= 1
                    if rs: q['rs'] -= 1

                    if c > 0:
                        desc = f"Catch at {pos}: {catch_phrases[ball_counter % len(catch_phrases)]}."
                    elif rs > 0:
                        desc = f"Fielding save at {pos}: {save_phrases[ball_counter % len(save_phrases)]}."
                    elif cp > 0 or gt > 0:
                        desc = f"At {pos}: {pick_throw_phrases[ball_counter % len(pick_throw_phrases)]}."
                    else:
                        desc = f"At {pos}: {routine_phrases[ball_counter % len(routine_phrases)]}."

                event = FieldingEvent(
                    match_number=self.match_number,
                    innings=self.innings,
                    team=self.team,
                    over=over,
                    ball=ball,
                    batter=batter,
                    bowler=bowler,
                    fielder=fielder,
                    position=pos,
                    short_description=desc,
                    pick=cp,
                    throw=gt,
                    catches=c,
                    dropped_catches=dc,
                    stumpings=st,
                    run_outs=ro,
                    missed_run_outs=mro,
                    direct_hits=dh,
                    runs_saved=rs,
                    venue=self.venue,
                    zone=zone
                )
                events.append(event)

        return events

# 🏏 India vs England 3rd T20I (2017) Fielding Analytics Engine & Web Dashboard
**ShadowFox Advanced Level Python Development Internship — Task 3**

An object-oriented Python sports analytics platform and interactive web dashboard built to analyze India's defensive fielding performance during **England's Innings in the 3rd T20I (1 February 2017)** at M. Chinnaswamy Stadium, Bengaluru.

---

## 🎯 Match & Analytical Context
- **Match:** India vs England – 3rd T20I (1 February 2017, M. Chinnaswamy Stadium, Bengaluru).
- **Innings:** England Innings (2nd Innings).
- **PrimaryAnalytical Subjects:**
  1. **MS Dhoni (WK)** — **Match Rank #1 (35 PS)**: Masterclass behind the stumps with 2 rapid stumpings, 1 direct run-out, 2 catches, and team defensive leadership.
  2. **Virat Kohli (C)** — **Match Rank #2 (30 PS)**: Outfield energy, 3 high boundary catches, and 1 direct hit at the bowler's end.
  3. **Hardik Pandya** — **Match Rank #3 (26 PS)**: Athletic boundary fielding, sliding saves (+7 runs saved), and powerful return throws.
- **Team Scope:** Evaluates all 11 Indian fielders (Virat Kohli, KL Rahul, Suresh Raina, MS Dhoni, Yuvraj Singh, Rishabh Pant, Hardik Pandya, Amit Mishra, Jasprit Bumrah, Ashish Nehra, Yuzvendra Chahal).

---

## 📐 Empirical Performance Formula
The Fielding Performance Score ($PS$) is calculated using strongly-typed dataclasses:

$$\text{PS} = (\text{CP} \times 1) + (\text{GT} \times 1) + (\text{C} \times 3) + (\text{DC} \times -3) + (\text{ST} \times 3) + (\text{RO} \times 3) + (\text{MRO} \times -2) + (\text{DH} \times 2) + \text{RS}$$

---

## 📁 Codebase Architecture

```
Advanced_Level/
├── requirements.txt                   # Dependency manifest (pandas, numpy, matplotlib, seaborn, flask)
├── models.py                          # Dataclass models & PS formula calculation logic
├── data_collector.py                  # 120 legal delivery ball-by-ball log generator
├── analyzer.py                        # FieldingAnalyzer matrix sorter & scouting engine
├── exporter.py                        # DatasetExporter for SQLite database & CSV files
├── visualizer.py                      # Matplotlib & Seaborn dark-mode 5-chart generator
├── main.py                            # Master CLI driver with argparse
├── README.md                          # Comprehensive project documentation
├── dataset/                           # Auto-generated database deliverables
│   ├── india_england_2017_t20_fielding.db # Relational SQLite database
│   ├── India_England_2017_Ball_By_Ball_Fielding.csv
│   ├── India_England_2017_Player_Performance.csv
│   └── charts/                        # High-resolution statistical PNG charts
│       ├── team_performance_scores.png
│       ├── target_player_comparison.png
│       ├── fielding_zone_analysis.png
│       ├── runs_saved_analysis.png
│       └── dismissal_breakdown.png
├── tests/                             # Automated Unit Test Suite
│   └── test_fielding_engine.py        # 5 unit tests (Math, Schema, Ranking, DB, API)
└── web_dashboard/                     # Interactive Flask Web Dashboard
    ├── app.py                         # Flask server with REST API & download routes
    ├── templates/index.html           # Dark-mode glassmorphic single-page web app
    └── static/
        ├── css/style.css              # Custom HSL dark theme & glassmorphic styling
        └── js/dashboard.js            # Async fetch, multi-filter logic, & tab routing
```

---

## 🚀 Quick Start Guide

### 1. Run Automated Unit Test Suite
```bash
python main.py --test
```

### 2. Generate Database & Visualizations (CLI)
```bash
python main.py
```

### 3. Query Terminal Player Scouting Card
```bash
python main.py --player "MS Dhoni"
```

### 4. Launch Interactive Flask Web Dashboard
```bash
python main.py --dashboard
```
Open **`http://127.0.0.1:5000`** in your browser.

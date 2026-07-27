# 🏏 Cricket Fielding Performance Analysis Engine & Interactive Web Dashboard

**ShadowFox Advanced Level Python Development Internship — Task 3**

A production-grade, Object-Oriented Python Sports Analytics Engine and interactive Flask Web Dashboard evaluating 11-player defensive fielding performance for **India vs England — 3rd T20I (1 February 2017 at M. Chinnaswamy Stadium, Bengaluru)** during England's 120-delivery chase.

---

## 🎯 Analytical Highlights & Player Rankings

The engine evaluates all 11 Indian fielders using an empirical Performance Score (PS) formula:

$$\text{PS} = (\text{CP} \times 1) + (\text{GT} \times 1) + (\text{C} \times 3) + (\text{DC} \times -3) + (\text{ST} \times 3) + (\text{RO} \times 3) + (\text{MRO} \times -2) + (\text{DH} \times 2) + \text{RS}$$

1. **MS Dhoni (WK) — Match Rank #1 (35 PS)**
   - Outstanding glove work: 2 stumpings, 1 run-out, 2 catches, 6 clean picks, 6 good throws.
2. **Virat Kohli (C) — Match Rank #2 (30 PS)**
   - Exceptional outfield leadership: 3 catches, 1 direct hit, +4 runs saved.
3. **Hardik Pandya — Match Rank #3 (26 PS)**
   - Athletic boundary diving saves: 2 catches, +4 runs saved.

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Interactive Web Dashboard
```bash
python main.py --dashboard
```
Open your browser to: **`http://127.0.0.1:5000`**

### 3. Run Automated Unit Test Suite
```bash
python main.py --test
```

### 4. Execute Full Pipeline (Database, CSVs, Charts)
```bash
python main.py
```

### 5. Query Player Scouting Card via CLI
```bash
python main.py -p "MS Dhoni"
```

---

## 📁 Repository Structure

```text
ShadowFox/Advanced_Level/
├── README.md                              # Portfolio documentation
├── requirements.txt                       # Dependencies
├── models.py                              # Dataclass models & PS formula
├── data_collector.py                      # 120-delivery simulator
├── analyzer.py                            # Matrix computation & scouting cards
├── exporter.py                            # SQLite & CSV persistence
├── visualizer.py                          # 5 Matplotlib/Seaborn charts
├── main.py                                # CLI entrypoint
├── tests/
│   └── test_fielding_engine.py            # Automated unit tests
├── dataset/                               # Output database & CSV deliverables
│   ├── india_england_2017_t20_fielding.db
│   ├── India_England_2017_Ball_By_Ball_Fielding.csv
│   ├── India_England_2017_Player_Performance.csv
│   └── charts/                            # 5 high-res PNG charts
└── web_dashboard/                         # Flask Web Dashboard
    ├── app.py                             # Server & API endpoints
    ├── templates/index.html               # Glassmorphic HTML template
    └── static/                            # CSS styles & JS client
```

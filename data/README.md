# SSA Mini Project — Conjunction Screening & Inspection Mission Design

Built for the Airbus D&S "Space Situational Awareness and Intelligence" internship application.
Goal: learn orbital mechanics *by implementing it*, using Orekit (the tool the JD names) instead
of a black-box library — every function below has a `# WHY:` comment explaining the physics,
not just the code. Fill in each `TODO` yourself; that's the point.

## Day-by-day (matches the original plan)

| Day | File | What you're learning |
|---|---|---|
| 1 | `src/setup_check.py` | Environment + pulling real TLE data from Celestrak |
| 2 | `src/propagate.py` | Orbit propagation — turning orbital elements into positions over time |
| 3-4 | `src/conjunction.py` | Closest-approach / collision-risk screening between two objects |
| 5 | `src/inspection_mission.py` | Hohmann transfer — designing a maneuver to reach a target object |
| 6 | `notebooks/visualize.ipynb` | Plotting your results (matplotlib) |
| 7 | — | Write the README summary + push to GitHub |

## Setup (Day 1)

```bash
conda install -c conda-forge orekit
python src/setup_check.py   # downloads orekit-data.zip and confirms it loads
```

## Why Orekit specifically

The JD names STK, Orekit, GMAT as accepted mission-analysis tools. STK and GMAT are GUI-first;
Orekit is the one you can actually drive from Python and put in a GitHub repo as working code —
that's what makes it a *demonstrable* skill rather than a claim on a resume.

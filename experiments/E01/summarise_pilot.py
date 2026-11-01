"""Write results/pilot_summary.md from results/pilot_final.csv (pilot split only)."""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
d = pd.read_csv(ROOT / "results" / "pilot_final.csv")
t = d.groupby(["level", "estimator"])["drift_pct"].median().unstack()[["B0", "B1", "B1g", "B2"]]
f = d.groupby(["level", "estimator"])["failure"].mean().unstack()[["B0", "B1", "B1g", "B2"]]
lines = ["# Pilot summary (pilot split only: families straight and meander, 12 trajectories, 10 seeds)", "",
         "Median drift ratio in percent of path length", "", t.round(2).to_markdown(), "",
         "Failure rate (drift ratio above threshold in config)", "", f.round(2).to_markdown(), "",
         f"Runs: {len(d)}"]
(ROOT / "results" / "pilot_summary.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))

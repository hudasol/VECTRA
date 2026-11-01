"""Pre specified analysis for the held out split. Unit of analysis: trajectory (mean over seeds). Writes results/e01_*.csv and e01_summary.md."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.evaluation import bootstrap_ci_median, paired_wilcoxon, holm, cliffs_delta_paired  # noqa: E402

LEVELS = ["D0", "D1", "D2", "D3", "D4"]
COMPARE = [("B2", "B1"), ("B2", "B0"), ("B2", "B1g")]

d = pd.read_csv(ROOT / "results" / "e01_heldout.csv")
d["traj_id"] = d["family"] + "_" + d["traj"].astype(str)
g = d.groupby(["level", "estimator", "traj_id"]).agg(drift=("drift_pct", "mean"), headrmse=("head_rmse_deg", "mean")).reset_index()
rows = []
for lv in LEVELS:
    for a, b in COMPARE:
        x = g[(g.level == lv) & (g.estimator == a)].sort_values("traj_id")["drift"].to_numpy()
        y = g[(g.level == lv) & (g.estimator == b)].sort_values("traj_id")["drift"].to_numpy()
        diff = x - y
        lo, hi = bootstrap_ci_median(diff, seed=1)
        rows.append({"level": lv, "A": a, "B": b, "n_traj": len(x), "median_A": np.median(x), "median_B": np.median(y),
                     "median_diff_pp": float(np.median(diff)), "ci_lo": lo, "ci_hi": hi, "p_raw": paired_wilcoxon(x, y),
                     "cliffs_delta": cliffs_delta_paired(x, y)})
t = pd.DataFrame(rows)
t["p_holm"] = holm(t["p_raw"].to_numpy())
t.to_csv(ROOT / "results" / "e01_primary_tests.csv", index=False)

sec = d.groupby(["level", "estimator"]).agg(
    drift_median=("drift_pct", "median"), drift_iqr_lo=("drift_pct", lambda s: s.quantile(.25)), drift_iqr_hi=("drift_pct", lambda s: s.quantile(.75)),
    ate_se2_median=("ate_se2", "median"), rpe10_median=("rpe10", "median"), head_rmse_median=("head_rmse_deg", "median"),
    failure_rate=("failure", "mean"), nees_pos_median=("nees_pos_mean", "median"), cover95_mean=("cover95_pos", "mean"),
    nees_head_median=("nees_head_mean", "median"), n_runs=("drift_pct", "size")).reset_index()
sec.to_csv(ROOT / "results" / "e01_secondary.csv", index=False)
print(t.round(4).to_string())
print(sec.round(3).to_string())

"""E02 analysis: prespecified families F1 (drift), F2 (heading RMSE), F3 (B3a against B3), plus descriptive tables.
Usage: python analyze_e02.py results/e02_heldout.csv"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.evaluation import bootstrap_ci_median, paired_wilcoxon, holm, cliffs_delta_paired   # noqa: E402

LEVELS = ["D0", "D1", "D2", "D3", "D4"]


def family(per, metric, pairs):
    rows = []
    for lv in LEVELS:
        t = per[per.level == lv].pivot(index="traj", columns="estimator", values=metric)
        for a, b in pairs:
            d = t[a] - t[b]
            lo, hi = bootstrap_ci_median(d.values)
            rows.append({"level": lv, "A": a, "B": b, "n_traj": len(d), "median_A": t[a].median(),
                         "median_B": t[b].median(), "median_diff": float(np.median(d)), "ci_lo": lo, "ci_hi": hi,
                         "p_raw": paired_wilcoxon(t[a].values, t[b].values),
                         "delta": cliffs_delta_paired(t[a].values, t[b].values)})
    out = pd.DataFrame(rows)
    out["p_holm"] = holm(out.p_raw.values)
    return out


def main(path):
    df = pd.read_csv(path)
    stem = Path(path).stem
    per = df.groupby(["traj", "level", "estimator"]).agg(drift=("drift_pct", "mean"), head=("head_rmse_deg", "mean"),
                                                         cover=("cover95_pos", "mean")).reset_index()
    pairs = [("B3", "B1g"), ("B3", "B2"), ("B3", "B0")]
    f1 = family(per, "drift", pairs)
    f2 = family(per, "head", pairs)
    f3 = pd.concat([family(per, "drift", [("B3a", "B3")]).assign(metric="drift"),
                    family(per, "cover", [("B3a", "B3")]).assign(metric="cover")])
    f3["p_holm"] = holm(f3.p_raw.values)
    f1.to_csv(ROOT / "results" / f"{stem}_F1.csv", index=False)
    f2.to_csv(ROOT / "results" / f"{stem}_F2.csv", index=False)
    f3.to_csv(ROOT / "results" / f"{stem}_F3.csv", index=False)
    sec = df.groupby(["level", "estimator"]).agg(
        drift_median=("drift_pct", "median"), drift_iqr_lo=("drift_pct", lambda x: x.quantile(.25)),
        drift_iqr_hi=("drift_pct", lambda x: x.quantile(.75)), ate_se2_median=("ate_se2", "median"),
        rpe10_median=("rpe10", "median"), head_rmse_median=("head_rmse_deg", "median"),
        failure_rate=("failure", "mean"), nees_pos_median=("nees_pos_mean", "median"),
        cover95_mean=("cover95_pos", "mean"), h_gated_mean=("h_gated", "mean"), n_runs=("drift_pct", "size")).reset_index()
    sec.to_csv(ROOT / "results" / f"{stem}_secondary.csv", index=False)
    env = df.groupby(["date", "time", "sky", "estimator"]).agg(drift_median=("drift_pct", "median"),
                                                                zen_min=("zen_min", "mean"),
                                                                head_rmse_median=("head_rmse_deg", "median")).reset_index()
    env.to_csv(ROOT / "results" / f"{stem}_envelope.csv", index=False)
    pd.set_option("display.width", 200)
    for f in (f1, f2, f3, sec):
        print(f.round(4).to_string())


if __name__ == "__main__":
    main(sys.argv[1])

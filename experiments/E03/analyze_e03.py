"""Study 3 analysis.

  python analyze_e03.py select  results/e03/dev.csv.gz            -> results/e03/dev_selection.json
  python analyze_e03.py confirm results/e03/confirm.csv.gz        -> results/e03/confirm_tests.csv, confirm_summary.json
  python analyze_e03.py describe <csv.gz> <tag>                   -> results/e03/<tag>_by_level.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.evaluation import paired_wilcoxon, holm     # noqa: E402

OUT = ROOT / "results" / "e03"
PRIMARY_LEVELS = ["D0", "D2", "D4"]
VO_SYSTEMS = ["B0", "B1", "B1g", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B3L", "B3C", "B3R", "B4R"]
SELECT_ORDER = ["B4", "B6", "B5", "B7", "B8"]


def per_traj(df, metric, levels=PRIMARY_LEVELS):
    d = df[df.level.isin(levels)]
    lv = d.groupby(["env", "traj", "level", "estimator"])[metric].mean().reset_index()
    return lv.groupby(["env", "traj", "estimator"])[metric].mean().unstack("estimator")


def cluster_boot_median(diff, env, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    envs = np.unique(env)
    groups = [diff[env == e] for e in envs]
    stats = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.integers(0, len(envs), len(envs))
        vals = np.concatenate([groups[i][rng.integers(0, len(groups[i]), len(groups[i]))] for i in pick])
        stats[b] = np.median(vals)
    return float(np.quantile(stats, 0.025)), float(np.quantile(stats, 0.975))


def compare(t, a, b, kind, margin=0.0):
    d = (t[a] - t[b]).values
    env = t.index.get_level_values("env").values
    lo, hi = cluster_boot_median(d, env)
    p = paired_wilcoxon(t[a].values, t[b].values)
    if kind == "lower":          # a lower than b, one sided from the two sided test
        p1 = p / 2 if np.median(d) < 0 else 1 - p / 2
        ok = hi < 0
    elif kind == "higher":
        p1 = p / 2 if np.median(d) > 0 else 1 - p / 2
        ok = lo > 0
    else:                        # non inferiority with margin on the upper bound
        p1 = np.nan
        ok = hi < margin
    return {"A": a, "B": b, "kind": kind, "margin": margin, "n_traj": len(d), "median_A": float(t[a].median()),
            "median_B": float(t[b].median()), "median_diff": float(np.median(d)), "ci_lo": lo, "ci_hi": hi,
            "p_one_sided": float(p1), "criterion_met": bool(ok)}


def select(path):
    df = pd.read_csv(path)
    lv = df[df.level.isin(PRIMARY_LEVELS)].groupby(["traj", "level", "estimator"]).head_rmse_deg.mean().reset_index()
    med = lv.groupby(["level", "estimator"]).head_rmse_deg.median().unstack("level")
    score = med[PRIMARY_LEVELS].mean(1)
    cands = score.loc[SELECT_ORDER]
    best = cands.min()
    chosen = next(e for e in SELECT_ORDER if cands[e] <= best + 0.05)
    rank = score.loc[[e for e in VO_SYSTEMS if e in score.index]].sort_values()
    res = {"rule": "lowest mean over D0, D2, D4 of the median trajectory heading RMSE among B4 to B8; ties within "
                   "0.05 degrees go to the first of B4, B6, B5, B7, B8", "scores": cands.round(4).to_dict(),
           "selected": chosen, "dev_ranking": list(rank.index), "dev_scores_all": score.round(4).to_dict()}
    (OUT / "dev_selection.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return res


def confirm(path):
    df = pd.read_csv(path)
    sel = json.loads((OUT / "dev_selection.json").read_text())
    S = sel["selected"]
    h = per_traj(df, "head_rmse_deg")
    h_d0 = per_traj(df, "head_rmse_deg", ["D0"])
    dr_d4 = per_traj(df, "drift_pct", ["D4"])
    tests = [dict(compare(h, "B3", "B0", "lower"), H="H1", metric="head_rmse_deg", levels="D0,D2,D4"),
             dict(compare(h_d0, "B1", "B0", "higher"), H="H2", metric="head_rmse_deg", levels="D0"),
             dict(compare(h, S, "B2", "noninf", 0.5), H="H3", metric="head_rmse_deg", levels="D0,D2,D4"),
             dict(compare(h, "B4", "B2", "noninf", 0.5), H="H3b", metric="head_rmse_deg", levels="D0,D2,D4"),
             dict(compare(h, "B4R", "B4", "lower"), H="H4", metric="head_rmse_deg", levels="D0,D2,D4"),
             dict(compare(dr_d4, "W3", "B0", "lower"), H="H5", metric="drift_pct", levels="D4")]
    t = pd.DataFrame(tests)
    sup = t.kind != "noninf"
    t["p_holm"] = np.nan
    t.loc[sup, "p_holm"] = holm(t.loc[sup, "p_one_sided"].values)
    t["supported"] = np.where(sup, (t.p_holm < 0.05) & t.criterion_met, t.criterion_met)
    t.to_csv(OUT / "confirm_tests.csv", index=False)
    # H6 consistency of B3C
    lvl = df[df.level.isin(PRIMARY_LEVELS)]
    cons = {}
    for e in ["B3", "B3C", "B4", "B0"]:
        g = lvl[lvl.estimator == e]
        cons[e] = {"median_nees_pos": float(g.nees_pos_mean.median()), "mean_cover95": float(g.cover95_pos.mean()),
                   "median_nees_head": float(g.nees_head_mean.median())}
    h6 = 1 <= cons["B3C"]["median_nees_pos"] <= 4 and 0.8 <= cons["B3C"]["mean_cover95"] <= 0.99
    # H7 ranking transfer
    from scipy.stats import kendalltau
    dev = sel["dev_scores_all"]
    lv = lvl.groupby(["traj", "level", "estimator"]).head_rmse_deg.mean().reset_index()
    cs = lv.groupby(["level", "estimator"]).head_rmse_deg.median().unstack("level")[PRIMARY_LEVELS].mean(1)
    common = [e for e in VO_SYSTEMS if e in dev and e in cs.index]
    tau = kendalltau([dev[e] for e in common], [cs[e] for e in common]).statistic
    summary = {"selected_S": S, "H6_consistency": cons, "H6_met": bool(h6), "H7_kendall_tau": float(tau),
               "H7_met": bool(tau >= 0.6), "confirm_ranking": list(cs.loc[common].sort_values().index),
               "confirm_scores": cs.loc[common].round(4).to_dict(), "n_rows": int(len(df)),
               "n_traj": int(df.traj.nunique())}
    (OUT / "confirm_summary.json").write_text(json.dumps(summary, indent=1))
    print(t.round(4).to_string())
    print(json.dumps(summary, indent=1))


def describe(path, tag):
    df = pd.read_csv(path)
    g = df.groupby(["traj", "level", "estimator"]).agg(head=("head_rmse_deg", "mean"), drift=("drift_pct", "mean"),
                                                      fail=("failure", "mean"), nees=("nees_pos_mean", "median"),
                                                      cover=("cover95_pos", "mean"), gated=("h_gated", "mean"),
                                                      maxrun=("max_run_gated", "mean")).reset_index()
    out = g.groupby(["level", "estimator"]).agg(head_med=("head", "median"), drift_med=("drift", "median"),
                                                fail=("fail", "mean"), nees_med=("nees", "median"),
                                                cover=("cover", "mean"), gated=("gated", "mean"),
                                                maxrun=("maxrun", "mean")).reset_index()
    out.to_csv(OUT / f"{tag}_by_level.csv", index=False)
    noon = df.assign(noon=df.time.isin(["11:45", "12:30"]) & df.date.isin(["2026-06-21"]))
    nn = noon.groupby(["noon", "estimator"]).head_rmse_deg.mean().unstack("noon")
    nn.to_csv(OUT / f"{tag}_noon.csv")
    print(out.pivot(index="estimator", columns="level", values="head_med").round(2).to_string())
    print(out.pivot(index="estimator", columns="level", values="drift_med").round(2).to_string())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "select":
        select(sys.argv[2])
    elif cmd == "confirm":
        confirm(sys.argv[2])
    else:
        describe(sys.argv[2], sys.argv[3])

"""Every Study 2 number quoted in the paper text, as LaTeX macros, computed from results files."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[1] / "results"
O = Path(__file__).resolve().parent / "numbers.tex"
d = pd.read_csv(R / "e02_heldout.csv" if (R / "e02_heldout.csv").exists() else R / "e02_heldout.csv.gz")
x = pd.read_csv(R / "e02_heldout_explore_B4.csv" if (R / "e02_heldout_explore_B4.csv").exists() else R / "e02_heldout_explore_B4.csv.gz")
sec = pd.read_csv(R / "e02_heldout_secondary.csv").set_index(["level", "estimator"])
F1 = pd.read_csv(R / "e02_heldout_F1.csv"); F2 = pd.read_csv(R / "e02_heldout_F2.csv"); F3 = pd.read_csv(R / "e02_heldout_F3.csv")
vo = pd.read_csv(R / "e02_heldout_vo_stats.csv")
sky = json.loads((R / "e02_sky_envelope.json").read_text())
M = {}


def put(k, v, nd=2):
    M[k] = f"{v:.{nd}f}" if isinstance(v, (float, np.floating)) else str(v)


put("nTraj", d.traj.nunique()); put("nRuns", len(d)); put("nRunsCell", int(sec.loc[("D0", "B0"), "n_runs"]))
for lv in ["D0", "D4"]:
    put(f"voOk{lv}", vo[vo.level == lv].ok_frac.median())
put("voSigWDzero", vo[vo.level == "D0"].sig_w.median(), 4); put("voSigWDfour", vo[vo.level == "D4"].sig_w.median(), 4)
L = {"D0": "zero", "D1": "one", "D2": "two", "D3": "three", "D4": "four"}
for lv in L:
    for e in ["B0", "B1", "B1g", "B2", "B3", "B3a"]:
        put(f"dr{e}{L[lv]}", sec.loc[(lv, e), "drift_median"]); put(f"hd{e}{L[lv]}", sec.loc[(lv, e), "head_rmse_median"])
        put(f"cv{e}{L[lv]}", sec.loc[(lv, e), "cover95_mean"]); put(f"ne{e}{L[lv]}", sec.loc[(lv, e), "nees_pos_median"], 1)
        put(f"fr{e}{L[lv]}", sec.loc[(lv, e), "failure_rate"], 3)
# by time of day, June, all skies, all levels (mean over runs)
J = d[d.date == "2026-06-21"]
tm = J.groupby(["time", "estimator"]).agg(h=("head_rmse_deg", "mean"), dr=("drift_pct", "mean")).reset_index()
for t, tag in [("12:30", "noon"), ("11:45", "near"), ("09:30", "morn")]:
    for e in ["B0", "B1", "B1g", "B2", "B3", "B3a"]:
        r = tm[(tm.time == t) & (tm.estimator == e)].iloc[0]
        put(f"h{tag}{e}", r.h); put(f"d{tag}{e}", r.dr)
D = d[d.date == "2026-12-21"].groupby("estimator").agg(h=("head_rmse_deg", "mean"), dr=("drift_pct", "mean"))
for e in D.index:
    put(f"hdec{e}", D.loc[e, "h"]); put(f"ddec{e}", D.loc[e, "dr"])
S = d.groupby(["sky", "estimator"]).head_rmse_deg.mean()
for s in ["clear", "cloud", "dust", "haze"]:
    for e in ["B1", "B1g", "B2", "B3", "B3a"]:
        put(f"sky{s}{e}", S.loc[(s, e)])
for e in ["B1g", "B3"]:
    put(f"gated{e}", d[d.estimator == e].h_gated.mean(), 0)
# stuck heading: share of runs with final heading error above 3 deg, cloud scenarios outside the noon window
C = d[(d.sky == "cloud") & (~((d.date == "2026-06-21") & d.time.isin(["11:45", "12:30"])))]
for e in ["B1", "B1g", "B2", "B3"]:
    put(f"stuck{e}", 100 * (C[C.estimator == e].head_final_deg > 3).mean(), 1)
# exploratory B4
X = x.groupby(["sky", "estimator"]).head_rmse_deg.mean()
put("skycloudBfour", X.loc[("cloud", "B4")])
per = x.groupby(["traj", "level", "estimator"]).head_rmse_deg.mean().unstack()
for lv in ["D0", "D2"]:
    p = per.xs(lv, level="level"); put(f"bfourShare{L[lv]}", 100 * (p.B4 < p.B2).mean(), 0)
    put(f"bfourMed{L[lv]}", p.B4.median(), 3); put(f"btwoMed{L[lv]}", p.B2.median(), 3)

# trajectory level medians (median over trajectories of per trajectory means): the prespecified unit
per2 = d.groupby(["traj", "level", "estimator"]).agg(dr=("drift_pct", "mean"), h=("head_rmse_deg", "mean")).reset_index()
for lv in L:
    for e in ["B0", "B1", "B1g", "B2", "B3", "B3a"]:
        q = per2[(per2.level == lv) & (per2.estimator == e)]
        put(f"tdr{e}{L[lv]}", q.dr.median()); put(f"thd{e}{L[lv]}", q.h.median())
ow = d[~((d.date == "2026-06-21") & d.time.isin(["11:45", "12:30"]))]
per3 = ow.groupby(["traj", "level", "estimator"]).head_rmse_deg.mean().reset_index()
for lv in L:
    for e in ["B1", "B1g", "B2", "B3"]:
        put(f"owhd{e}{L[lv]}", per3[(per3.level == lv) & (per3.estimator == e)].head_rmse_deg.median())
G = d.assign(cl=d.sky == "cloud").groupby(["cl", "estimator"]).h_gated.mean()
for e in ["B1g", "B3"]:
    put(f"gatedcloud{e}", G.loc[(True, e)], 0); put(f"gatedother{e}", G.loc[(False, e)], 0)
from scipy import stats as _st
pv = []
for lv in L:
    q = per2[per2.level == lv].pivot(index="traj", columns="estimator", values="h")
    pv.append(_st.wilcoxon(q["B2"] - q["B1g"]).pvalue)
put("maxpBtwoBgate", max(pv), 4)
for lv in L:
    p = per.xs(lv, level="level"); put(f"bfourShare{L[lv]}", 100 * (p.B4 < p.B2).mean(), 0)
    put(f"bfourMed{L[lv]}", p.B4.median(), 2); put(f"btwoMed{L[lv]}", p.B2.median(), 2)
for e in ["B0", "B3"]:
    put(f"ate{e}three", sec.loc[("D3", e), "ate_se2_median"]); put(f"rpe{e}three", sec.loc[("D3", e), "rpe10_median"])
put("distinctBzero", int(d[(d.estimator == "B0")].groupby(["traj", "level"]).drift_pct.nunique().max()))
# example trajectory in the figure (held out run, level D3, clear sky, filter seed 0)
q = d[(d.traj == "MiddleEast__Data_omni__P0000") & (d.level == "D3") & (d.date == "2026-06-21") & (d.sky == "clear") & (d.fseed == 0)]
for tm, tag in [("09:30", "morn"), ("12:30", "noon")]:
    for e in ["B0", "B1", "B1g", "B3"]:
        put(f"ex{tag}{e}", float(q[(q.time == tm) & (q.estimator == e)].drift_pct.iloc[0]))
# reduction ranges for the weighted schemes against B0 at D3 and D4 (trajectory level)
W = ["B1g", "B2", "B3", "B3a"]
for lv in ["D3", "D4"]:
    q = per2[per2.level == lv].groupby("estimator")[["dr", "h"]].median()
    hr = [q.loc["B0", "h"] / q.loc[e, "h"] for e in W]; dr_ = [100 * (1 - q.loc[e, "dr"] / q.loc["B0", "dr"]) for e in W]
    put(f"hratioMin{L[lv]}", min(hr), 1); put(f"hratioMax{L[lv]}", max(hr), 1)
    put(f"dredMin{L[lv]}", min(dr_), 0); put(f"dredMax{L[lv]}", max(dr_), 0)
# tests
for name, F in [("Fone", F1), ("Ftwo", F2)]:
    for _, r in F.iterrows():
        k = f"{name}{L[r.level]}{r.B}"
        put(k + "diff", r.median_diff, 3 if name == "Fone" else 2); put(k + "p", r.p_holm, 4)
        put(k + "lo", r.ci_lo, 3 if name == "Fone" else 2); put(k + "hi", r.ci_hi, 3 if name == "Fone" else 2)
for _, r in F3.iterrows():
    put(f"Fthree{L[r.level]}{r.metric}diff", r.median_diff, 3); put(f"Fthree{L[r.level]}{r.metric}p", r.p_holm, 4)
    put(f"Fthree{L[r.level]}{r.metric}A", r.median_A, 3); put(f"Fthree{L[r.level]}{r.metric}B", r.median_B, 3)
y = sky["year_2026"]; j = sky["days"]["2026-06-21"]
put("blindDays", y["days_with_sigma_gt_10"]); put("blindMax", y["max_minutes"]); put("juneTen", j["minutes_sigma_gt_10"])
put("juneTwo", j["minutes_sigma_gt_2"]); put("juneTenDouble", sky["june21_if_dop_doubled"]["minutes_sigma_gt_10"])
put("dopSeventy", 100 * sky["model_zenith_dop_at_elevation"]["70"], 1); put("dopThirtyFive", 100 * sky["model_zenith_dop_at_elevation"]["35"], 1)
import re
EN = {"D0": "Dzero", "D4": "Dfour", "B3a": "Bthreea", "B1g": "Bgate", "B0": "Bzero", "B1": "Bone", "B2": "Btwo", "B3": "Bthree", "B4": "Bfour"}


def clean(k):
    for a, b in EN.items():
        k = k.replace(a, b)
    assert re.fullmatch(r"[A-Za-z]+", k), k
    return k


M = {clean(k): v for k, v in M.items()}
O.write_text("\n".join(f"\\newcommand{{\\n{k}}}{{{v}}}" for k, v in sorted(M.items())) + "\n")
print(len(M), "macros")

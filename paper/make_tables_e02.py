"""E02 LaTeX tables from results/e02_heldout_*.csv only."""
from pathlib import Path
import pandas as pd

R = Path(__file__).resolve().parents[1] / "results"
O = Path(__file__).resolve().parent
LV = ["D0", "D1", "D2", "D3", "D4"]
ES = ["B0", "B1", "B1g", "B2", "B3", "B3a"]


def f(v, d=2):
    t = f"{v:.{d}f}"
    return t[1:] if t.startswith("-") and float(t) == 0 else t


def pf(v):
    return "$<$0.001" if v < 0.001 else f(v, 3)


sec = pd.read_csv(R / "e02_heldout_secondary.csv")
_h = R / "e02_heldout.csv"
D = pd.read_csv(_h if _h.exists() else R / "e02_heldout.csv.gz")
per = D.groupby(["traj", "level", "estimator"]).agg(dr=("drift_pct", "mean"), h=("head_rmse_deg", "mean")).reset_index()
tdr = per.groupby(["level", "estimator"]).dr.median()
th = per.groupby(["level", "estimator"]).h.median()
L = ["\\begin{tabular}{l" + "r" * len(ES) + "}", "\\toprule",
     "Level & " + " & ".join(ES) + " \\\\", "\\midrule", "\\multicolumn{7}{l}{\\emph{Drift ratio (\\%), trajectory level}} \\\\"]
for lv in LV:
    L.append(lv + " & " + " & ".join(f(tdr.loc[(lv, e)]) for e in ES) + " \\\\")
L += ["\\midrule", "\\multicolumn{7}{l}{\\emph{Heading RMSE (deg), trajectory level}} \\\\"]
for lv in LV:
    L.append(lv + " & " + " & ".join(f(th.loc[(lv, e)]) for e in ES) + " \\\\")
L += ["\\midrule", "\\multicolumn{7}{l}{\\emph{Failure rate (share of runs with drift above 10\\%)}} \\\\"]
for lv in LV:
    r = sec[sec.level == lv].set_index("estimator")
    L.append(lv + " & " + " & ".join(f(r.loc[e, "failure_rate"]) for e in ES) + " \\\\")
L += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_e02_main.tex").write_text("\n".join(L))

rows = ["\\begin{tabular}{llrrrr}", "\\toprule", "Level & Pair & Diff & 95\\% CI & $\\delta$ & $p_{\\mathrm{Holm}}$ \\\\"]
for fam, title, d in [("F1", "F1: drift ratio (percentage points)", 2), ("F2", "F2: heading RMSE (deg)", 2)]:
    t = pd.read_csv(R / f"e02_heldout_{fam}.csv")
    rows += ["\\midrule", f"\\multicolumn{{6}}{{l}}{{\\emph{{{title}}}}} \\\\"]
    for lv in LV:
        for i, b in enumerate(["B1g", "B2", "B0"]):
            r = t[(t.level == lv) & (t.B == b)].iloc[0]
            rows.append(f"{lv if i == 0 else ''} & B3 vs {b} & {f(r.median_diff, d)} & [{f(r.ci_lo, d)}, {f(r.ci_hi, d)}] & {f(r.delta)} & {pf(r.p_holm)} \\\\")
rows += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_e02_tests.tex").write_text("\n".join(rows))

t = pd.read_csv(R / "e02_heldout_F3.csv")
rows = ["\\begin{tabular}{llrrrr}", "\\toprule", "Level & Metric & Diff & 95\\% CI & $\\delta$ & $p_{\\mathrm{Holm}}$ \\\\", "\\midrule"]
for _, r in t.iterrows():
    dd = 3 if r.metric == "cover" else 2
    rows.append(f"{r.level} & {'coverage' if r.metric == 'cover' else 'drift'} & {f(r.median_diff, dd)} & [{f(r.ci_lo, dd)}, {f(r.ci_hi, dd)}] & {f(r.delta)} & {pf(r.p_holm)} \\\\")
rows += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_e02_f3.tex").write_text("\n".join(rows))
print("ok")

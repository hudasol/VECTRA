"""LaTeX tables generated from results/*.csv only."""
import pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[1] / "results"; O = Path(__file__).resolve().parent
s = pd.read_csv(R / "e01_secondary.csv"); p = pd.read_csv(R / "e01_primary_tests.csv")
lv = ["D0", "D1", "D2", "D3", "D4"]; es = ["B0", "B1", "B1g", "B2"]
def f(v, d=2):
    t = f"{v:.{d}f}"
    return t[1:] if t.startswith("-") and float(t) == 0 else t
L = ["\\begin{tabular}{llrrrr}", "\\toprule", "Level & System & Drift \\% & IQR & Fail & NEES \\\\", "\\midrule"]
for l in lv:
    for e in es:
        r = s[(s.level == l) & (s.estimator == e)].iloc[0]
        L.append(f"{l if e=='B0' else ''} & {e} & {f(r.drift_median)} & {f(r.drift_iqr_lo,1)} to {f(r.drift_iqr_hi,1)} & {f(r.failure_rate)} & {f(r.nees_pos_median,1)} \\\\")
    if l != "D4": L.append("\\midrule")
L += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_main.tex").write_text("\n".join(L))
def pf(v): return "$<$0.001" if v < 0.001 else f(v, 3)
L = ["\\begin{tabular}{llrrrr}", "\\toprule", "Level & Pair & Median diff (pp) & 95\\% CI & $\\delta$ & $p_{\\mathrm{Holm}}$ \\\\", "\\midrule"]
for l in lv:
    for i, b in enumerate(["B1", "B0", "B1g"]):
        r = p[(p.level == l) & (p.B == b)].iloc[0]
        L.append(f"{l if i==0 else ''} & B2 vs {b} & {f(r.median_diff_pp)} & [{f(r.ci_lo)}, {f(r.ci_hi)}] & {f(r.cliffs_delta)} & {pf(r.p_holm)} \\\\")
    if l != "D4": L.append("\\midrule")
L += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_tests.tex").write_text("\n".join(L))
print("ok")

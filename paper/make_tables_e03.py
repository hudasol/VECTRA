"""Study 3 LaTeX tables from result files only."""
from pathlib import Path
import pandas as pd

R = Path(__file__).resolve().parents[1] / "results"
O = Path(__file__).resolve().parent


def f(v, d=2):
    t = f"{v:.{d}f}"
    return t[1:] if t.startswith("-") and float(t) == 0 else t


dw = pd.read_csv(R / "e03_sky/desert_windows.csv")
order = ["Thar", "Abu Dhabi", "Sahara, central", "Rub al Khali", "Sahara, Sahel edge", "Great Sandy", "Kalahari",
         "Namib", "Atacama", "Simpson"]
L = ["\\begin{tabular}{lrrrr}", "\\toprule", "Desert & Lat. & Zenith & Ring & Days \\\\", "\\midrule"]
for n in order:
    g = dw[dw.desert == n].set_index("geometry")
    L.append(f"{n} & {g.loc['zenith', 'lat_used']:.0f} & {g.loc['zenith', 'max_minutes']} & "
             f"{g.loc['zenith_ring', 'max_minutes']} & {g.loc['zenith', 'days_per_year_with_window']} \\\\")
L += ["\\bottomrule", "\\end{tabular}"]
(O / "tab_e03_deserts.tex").write_text("\n".join(L))

ct = R / "e03/confirm_tests.csv"
if ct.exists():
    t = pd.read_csv(ct)
    L = ["\\begin{tabular}{llrrrrl}", "\\toprule", "H & Pair & $A$ & $B$ & Diff [95\\% CI] & $p_{\\mathrm{Holm}}$ & Result \\\\",
         "\\midrule"]
    for _, r in t.iterrows():
        p = "--" if pd.isna(r.p_holm) else ("$<$0.001" if r.p_holm < 0.001 else f(r.p_holm, 3))
        unit = "\\%" if r.metric == "drift_pct" else "$^\\circ$"
        L.append(f"{r.H} & {r.A}$-${r.B} ({r.levels}) & {f(r.median_A)} & {f(r.median_B)} & {f(r.median_diff)}{unit} "
                 f"[{f(r.ci_lo)}, {f(r.ci_hi)}] & {p} & {'yes' if r.supported else 'no'} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    (O / "tab_e03_tests.tex").write_text("\n".join(L))
    cb = pd.read_csv(R / "e03/confirm_by_level.csv")
    es = ["B0", "B1", "B1g", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B3L", "B3C", "B3R", "B4R", "SUN", "MAG", "W0", "W3", "W4R"]
    L = ["\\begin{tabular}{lrrrrrrr}", "\\toprule",
         " & \\multicolumn{3}{c}{Heading RMSE (deg)} & \\multicolumn{3}{c}{Drift (\\%)} & NEES \\\\",
         "System & D0 & D2 & D4 & D0 & D2 & D4 & D2 \\\\", "\\midrule"]
    for e in es:
        g = cb[cb.estimator == e].set_index("level")
        if g.empty:
            continue
        L.append(e + " & " + " & ".join(f(g.loc[lv, "head_med"]) for lv in ["D0", "D2", "D4"]) + " & "
                 + " & ".join(f(g.loc[lv, "drift_med"]) for lv in ["D0", "D2", "D4"]) + f" & {g.loc['D2', 'nees_med']:.0f} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    (O / "tab_e03_main.tex").write_text("\n".join(L))
print("ok")

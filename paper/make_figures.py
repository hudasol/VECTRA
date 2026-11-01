"""Figures for the paper. Reads only results/*.csv. Greyscale safe (marker and line style carry identity)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
R = Path(__file__).resolve().parents[1] / "results"; O = Path(__file__).resolve().parent / "figs"
plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6, "pdf.fonttype": 42})
sty = {"B0": ("0.55", "s", ":"), "B1": ("0.0", "o", "--"), "B1g": ("tab:blue", "^", "-"), "B2": ("tab:red", "D", "-")}
lab = {"B0": "B0 no heading", "B1": "B1 heading", "B1g": "B1g heading + gate", "B2": "B2 adaptive"}
s = pd.read_csv(R / "e01_secondary.csv"); lv = ["D0", "D1", "D2", "D3", "D4"]

fig, ax = plt.subplots(figsize=(3.4, 2.5))
for e in sty:
    d = s[s.estimator == e].set_index("level").loc[lv]; c, m, l = sty[e]
    x = np.arange(5) + {"B0": -.09, "B1": -.03, "B1g": .03, "B2": .09}[e]
    ax.errorbar(x, d.drift_median, yerr=[d.drift_median - d.drift_iqr_lo, d.drift_iqr_hi - d.drift_median],
                color=c, marker=m, ls=l, ms=3.5, lw=1, capsize=1.5, label=lab[e])
ax.set_yscale("log"); ax.set_xticks(range(5)); ax.set_xticklabels(lv)
ax.set_xlabel("Degradation level"); ax.set_ylabel("Final drift (% of path)")
ax.grid(alpha=.25, lw=.4); ax.legend(fontsize=6.5, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(O / "fig_drift.pdf"); plt.close(fig)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(3.4, 2.1))
for e in sty:
    d = s[s.estimator == e].set_index("level").loc[lv]; c, m, l = sty[e]
    a1.plot(range(5), d.nees_pos_median, color=c, marker=m, ls=l, ms=3, lw=1)
    a2.plot(range(5), d.cover95_mean, color=c, marker=m, ls=l, ms=3, lw=1, label=lab[e])
a1.axhline(2, color="k", lw=.6); a1.set_yscale("log"); a1.set_ylabel("Median position NEES")
a2.axhline(.95, color="k", lw=.6); a2.set_ylabel("95% coverage"); a2.set_ylim(0, 1)
for a in (a1, a2): a.set_xticks(range(5)); a.set_xticklabels(lv); a.grid(alpha=.25, lw=.4)
a1.text(0.1, 2.3, "ideal = 2", fontsize=6); a2.text(0.1, .91, "ideal = 0.95", fontsize=6)
fig.tight_layout(); fig.savefig(O / "fig_nees.pdf"); plt.close(fig)

x = pd.read_csv(R / "e01_sensitivity.csv")
from matplotlib.ticker import ScalarFormatter, NullFormatter
P = [("noise_sigma_deg", "Cue noise (deg)"), ("bias_rw_deg_per_sqrt_s", "Bias walk (deg/$\\sqrt{s}$)"),
     ("contamination_start_rate_per_s", "Contamination rate (1/s)"), ("dropout_frac", "Cue dropout fraction")]
fig, axs = plt.subplots(1, 4, figsize=(7.1, 2.3), sharey=True)
for a, (p, t) in zip(axs, P):
    g = x[x.param == p].groupby(["value", "estimator"]).drift_pct.median().unstack()
    for e in sty:
        c, m, l = sty[e]; a.plot(g.index, g[e], color=c, marker=m, ls=l, ms=3, lw=1, label=lab[e])
    a.set_yscale("log"); a.set_xlabel(t); a.grid(alpha=.25, lw=.4)
    a.set_yticks([1, 2, 5, 10]); a.yaxis.set_major_formatter(ScalarFormatter()); a.yaxis.set_minor_formatter(NullFormatter())
    a.set_xticks(g.index); a.set_xticklabels([f"{v:g}" for v in g.index], fontsize=6.5)
    a.minorticks_off() if False else None
axs[0].set_ylabel("Median drift (%), D2")
h, l_ = axs[0].get_legend_handles_labels()
fig.legend(h, l_, loc="upper center", ncol=4, fontsize=6.5, frameon=False)
fig.tight_layout(rect=(0, 0, 1, 0.9)); fig.savefig(O / "fig_sens.pdf"); plt.close(fig)
print("ok")

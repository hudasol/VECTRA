"""Study 3 figures from result files only (pink theme). Usage: python make_figures_e03.py [sky|results|all]"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "E03"))
R = ROOT / "results"
F = Path(__file__).resolve().parent / "figs"
PINK = ["#5c1a3a", "#b0306a", "#e0609a", "#f2a7c3", "#f9d5e3"]
GREY = "#6b6b6b"
SAKURA = LinearSegmentedColormap.from_list("sakura", ["#fff7fa", "#f9d5e3", "#f2a7c3", "#e0609a", "#b0306a", "#5c1a3a"])
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "font.family": "serif"})


def sky():
    import sky_v2 as S
    z = np.load(R / "e03_sky" / "dop_tables.npz")
    dop, zen, aod = z["dop"], z["zen"], z["aod"]
    fig, ax = plt.subplots(1, 3, figsize=(7.16, 2.3))
    a = ax[0]
    zz = np.linspace(0, 80, 200)
    g = np.radians(zz)
    a.plot(zz, 0.6 * np.sin(g) ** 2 / (1 + np.cos(g) ** 2), color=GREY, ls="--", lw=1, label="Study 2 law")
    for i, (k, c) in enumerate(zip([0, 2, 4, 6, 8], PINK)):
        a.plot(zen, dop[k, :, 0], color=c, lw=1.2, label=f"RT, AOD {aod[k]:g}")
    a.add_patch(plt.Rectangle((53, 0.24), 4, 0.06, color="k", alpha=0.25, lw=0))
    a.plot([20], [0.08], "k^", ms=4, label="measured [desert]")
    a.set_xlabel("solar zenith (deg)")
    a.set_ylabel("zenith DoP")
    a.legend(frameon=False, fontsize=5.5, loc="upper left")
    a.set_title("(a) zenith degree of polarisation", fontsize=8)
    # (b) heading noise through 21 June
    clim = json.loads((R / "e03_sky" / "power_24.45_54.38.json").read_text())
    cv = S.sigma_curves(dop, z["ring_az"], clim["AOD_55"]["JUN"])
    h = np.arange(6 * 60, 18 * 60) / 60.0
    zs = S.sun_zen_vec(S.LAT, S.LON, 172, h - S.UTC)
    a = ax[1]
    s2 = np.degrees(S.sigma_point(0.6 * np.sin(np.radians(zs)) ** 2 / (1 + np.cos(np.radians(zs)) ** 2)))
    a.semilogy(h, s2, color=GREY, ls="--", lw=1, label="zenith, Study 2 law")
    for k, (lab, c) in enumerate(zip(["zenith, RT", "zenith and ring, RT", "sun sensor (assumed)"], PINK[1:4])):
        a.semilogy(h, np.interp(zs, S.ZF, cv[:, k]), color=c, lw=1.2, label=lab)
    a.axhline(2.0, color="k", lw=0.6, ls=":", label="magnetometer (assumed)")
    a.axhline(10, color="k", lw=0.4)
    a.set_ylim(0.1, 200)
    a.set_xlabel("local time, 21 June")
    a.set_ylabel("heading noise (deg)")
    a.legend(frameon=False, fontsize=5.5, loc="upper left")
    a.set_title("(b) Abu Dhabi, June aerosol", fontsize=8)
    # (c) global map
    m = np.load(R / "e03_sky" / "global_blind_map.npz")
    a = ax[2]
    im = a.pcolormesh(m["doy"], m["lat"], m["minutes"][:, :, 0], cmap=SAKURA, shading="auto")
    a.contour(m["doy"], m["lat"], m["minutes"][:, :, 1], levels=[1], colors=[PINK[0]], linewidths=0.8)
    for la, name in [(24.45, "Abu Dhabi"), (23.44, None), (-23.44, None)]:
        a.axhline(la, color="k", lw=0.4, ls=":" if name is None else "-")
    a.text(5, 25.5, "Abu Dhabi", fontsize=5.5)
    a.set_xlabel("day of year")
    a.set_ylabel("latitude (deg)")
    a.set_title("(c) minutes per day above 10 deg", fontsize=8)
    plt.colorbar(im, ax=a, fraction=0.05, pad=0.02)
    fig.tight_layout()
    fig.savefig(F / "fig_e03_sky.pdf")
    print("sky figure")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("sky", "all"):
        sky()

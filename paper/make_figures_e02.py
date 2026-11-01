"""E02 figures. Sky figures use only the model; result figures read results/e02_*.csv."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vectra.sky import sun_position, zenith_dop, aop_sigma   # noqa: E402
from vectra.config import load_config                        # noqa: E402
O = Path(__file__).resolve().parent / "figs"
plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6, "pdf.fonttype": 42})
cfg = load_config(ROOT / "configs" / "e02.yaml")
LOC = cfg["sky"]["location"]; CO = cfg["compass"]


def sun_local(s):
    t = datetime.fromisoformat(s) - timedelta(hours=LOC["utc_offset_h"])
    return sun_position(LOC["lat_deg"], LOC["lon_deg"], t)


def vec(zen, az):
    z, a = np.radians(zen), np.radians(az)
    return np.stack([np.sin(z) * np.sin(a), np.sin(z) * np.cos(a), np.cos(z)], -1)   # east, north, up


def sky_panel(ax, s, title):
    zs, azs = sun_local(s)
    r = np.linspace(0, 90, 181); th = np.linspace(0, 360, 361)
    R, T = np.meshgrid(r, th)
    P = vec(R, T); S = vec(np.array(zs), np.array(azs))
    cg = np.clip(P @ S, -1, 1)
    dop = CO["d_max"] * (1 - cg ** 2) / (1 + cg ** 2)
    X = R * np.sin(np.radians(T)); Y = R * np.cos(np.radians(T))
    m = ax.pcolormesh(X, Y, dop, cmap="RdPu", vmin=0, vmax=CO["d_max"], shading="auto", rasterized=True)
    # e-vectors on a coarse grid: perpendicular to the scattering plane, e = p x s
    for rr in [0, 20, 40, 60, 80]:
        for tt in (np.arange(0, 360, 30) if rr else [0]):
            p = vec(np.array(rr), np.array(tt)); e = np.cross(p, S)
            if np.linalg.norm(e) < 1e-6: continue
            e /= np.linalg.norm(e)
            a = np.radians(tt); zr = np.radians(rr)
            if rr == 0:
                u, v = e[0], e[1]
            else:
                dz = np.array([np.cos(zr) * np.sin(a), np.cos(zr) * np.cos(a), -np.sin(zr)])
                da = np.array([np.cos(a), -np.sin(a), 0.0])
                cr, ca = e @ dz, e @ da
                u = cr * np.sin(a) + ca * np.cos(a); v = cr * np.cos(a) - ca * np.sin(a)
            x0, y0 = rr * np.sin(a), rr * np.cos(a); L = 6
            ax.plot([x0 - L * u, x0 + L * u], [y0 - L * v, y0 + L * v], color="k", lw=0.7)
    ax.plot(zs * np.sin(np.radians(azs)), zs * np.cos(np.radians(azs)), marker="*", color="#e0a000", ms=9, mec="k", mew=0.4)
    ax.add_patch(plt.Circle((0, 0), 90, fill=False, lw=0.6))
    ax.text(0, 93, "N", ha="center", fontsize=7); ax.text(93, 0, "E", va="center", fontsize=7)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-100, 100); ax.set_ylim(-100, 100)
    ax.set_title(f"{title}\nsun zenith {zs:.0f} deg, zenith DoP {zenith_dop(zs, CO['d_max']):.3f}", fontsize=6.5)
    return m


def fig_sky():
    fig = plt.figure(figsize=(7.1, 2.25))
    a1 = fig.add_axes([0.0, 0.2, 0.25, 0.68]); a2 = fig.add_axes([0.25, 0.2, 0.25, 0.68])
    a3 = fig.add_axes([0.6, 0.2, 0.37, 0.65])
    sky_panel(a1, "2026-06-21T08:00", "21 June, 08:00")
    m = sky_panel(a2, "2026-06-21T12:30", "21 June, 12:30")
    cb = fig.colorbar(m, ax=[a1, a2], orientation="horizontal", fraction=0.05, pad=0.02, shrink=0.6)
    cb.set_label("Rayleigh degree of linear polarisation", fontsize=7); cb.ax.tick_params(labelsize=6)
    hrs = np.arange(6.0, 18.01, 0.05)
    for d, ls in [("2026-06-21", "-"), ("2026-12-21", "--")]:
        base = datetime.fromisoformat(d) - timedelta(hours=LOC["utc_offset_h"])
        zz = np.array([sun_position(LOC["lat_deg"], LOC["lon_deg"], base + timedelta(hours=float(h)))[0] for h in hrs])
        sig = np.degrees(aop_sigma(zenith_dop(zz, CO["d_max"]), np.radians(CO["floor_deg"]), np.radians(CO["c_deg"])))
        sig = np.where(zz < 90, sig, np.nan)
        a3.plot(hrs, sig, ls=ls, color="#8a3b5c", lw=1.1, label=("21 June" if ls == "-" else "21 December"))
    a3.set_yscale("log"); a3.set_xlabel("Local time, Abu Dhabi (h)"); a3.set_ylabel("Compass noise, clear sky (deg)")
    a3.axhline(CO["floor_deg"], color="0.5", lw=0.6, ls=":"); a3.grid(alpha=.25, lw=.4); a3.legend(fontsize=6.5, frameon=False)
    a3.set_xlim(6, 18)
    fig.savefig(O / "fig_sky.pdf", dpi=300); fig.savefig(O / "fig_sky.png", dpi=200); plt.close(fig)




def fig_frames():
    """Pilot frame at every level with the visual odometry inliers marked."""
    import cv2
    from vectra.degrade import Degrader, level_params
    from vectra.vo import StereoVO
    L = np.load("/home/claude/data/pilot_L.npy", mmap_mode="r"); R = np.load("/home/claude/data/pilot_R.npy", mmap_mode="r")
    D = np.load("/home/claude/data/pilot_D.npy", mmap_mode="r"); g = np.load("/home/claude/data/pilot_meta.npz")["gyro"]
    k = 250
    fig, axs = plt.subplots(1, 5, figsize=(7.1, 1.75))
    for ax, lv in zip(axs, cfg["levels"]):
        p = level_params(cfg["levels"], lv); rng = np.random.default_rng(3)
        dl = Degrader(p, cfg["camera"], rng, 320); dr = Degrader(p, cfg["camera"], np.random.default_rng(3), 320); dr.glare_map = dl.glare_map
        vo = StereoVO(160, 159.5, 159.5, 0.25)
        for j in (k - 1, k):
            a = dl(np.ascontiguousarray(L[j]), np.asarray(D[j], np.float32), g[10 * j], rng)
            b = dr(np.ascontiguousarray(R[j]), np.asarray(D[j], np.float32), g[10 * j], rng)
            res = vo.step(a, b, 0.1)
        ax.imshow(a, cmap="gray", vmin=0, vmax=255)
        pts = vo.prev_pts.reshape(-1, 2) if vo.prev_pts is not None else np.zeros((0, 2))
        ax.scatter(pts[:, 0], pts[:, 1], s=1.2, c="#e0408a", lw=0)
        ax.set_title(f"{lv}: {int(res[4])} inliers" if res[0] else f"{lv}: VO failed", fontsize=7)
        ax.axis("off")
    fig.tight_layout(pad=0.2); fig.savefig(O / "fig_frames.pdf", dpi=300); fig.savefig(O / "fig_frames.png", dpi=200); plt.close(fig)



STY = {"B0": ("0.55", "s", ":"), "B1": ("0.0", "o", "--"), "B1g": ("tab:blue", "^", "-"),
       "B2": ("tab:green", "v", "-."), "B3": ("tab:red", "D", "-"), "B3a": ("#8a3b5c", "P", "--")}
LV = ["D0", "D1", "D2", "D3", "D4"]


def _held():
    import pandas as pd
    return pd.read_csv(ROOT / "results" / "e02_heldout.csv" if (ROOT / "results" / "e02_heldout.csv").exists() else ROOT / "results" / "e02_heldout.csv.gz")


def fig_e02_main():
    df = _held()
    per = df.groupby(["traj", "level", "estimator"]).agg(dr=("drift_pct", "mean"), h=("head_rmse_deg", "mean")).reset_index()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.1, 2.1))
    for e, (c, m, l) in STY.items():
        x = np.arange(5) + (list(STY).index(e) - 2.5) * 0.06
        for ax, col in ((a1, "dr"), (a2, "h")):
            g = per[per.estimator == e].groupby("level")[col]
            med = g.median().loc[LV]; lo = g.quantile(.25).loc[LV]; hi = g.quantile(.75).loc[LV]
            ax.errorbar(x, med, yerr=[med - lo, hi - med], color=c, marker=m, ls=l, ms=3, lw=1, capsize=1.2, label=e)
    from matplotlib.ticker import ScalarFormatter, NullFormatter
    for a in (a1, a2):
        a.set_xticks(range(5)); a.set_xticklabels(LV); a.set_xlabel("Degradation level"); a.grid(alpha=.25, lw=.4); a.set_yscale("log")
        a.yaxis.set_major_formatter(ScalarFormatter()); a.yaxis.set_minor_formatter(NullFormatter())
    a1.set_yticks([0.5, 1, 2, 5, 10]); a2.set_yticks([0.2, 0.5, 1, 2, 5, 10])
    a1.set_ylabel("Drift ratio (%)"); a2.set_ylabel("Heading RMSE (deg)")
    a1.legend(fontsize=6.5, frameon=False, ncol=3, loc="upper left")
    fig.tight_layout(); fig.savefig(O / "fig_e02_main.pdf"); fig.savefig(O / "fig_e02_main.png", dpi=200); plt.close(fig)


def fig_envelope():
    df = _held()
    times = cfg["sky"]["start_times"]
    fig, axs = plt.subplots(1, 4, figsize=(7.1, 2.05), sharey=True)
    for ax, sky in zip(axs, ["clear", "haze", "dust", "cloud"]):
        for e in ["B0", "B1", "B1g", "B2", "B3", "B3a"]:
            c, m, l = STY[e]
            g = df[(df.sky == sky) & (df.date == "2026-06-21") & (df.estimator == e)].groupby("time").head_rmse_deg.mean()
            ax.plot(range(len(times)), g.loc[times].values, color=c, marker=m, ls=l, ms=3, lw=1, label=e)
        ax.set_xticks(range(len(times))); ax.set_xticklabels(times, rotation=60, fontsize=6)
        ax.set_yscale("log"); ax.grid(alpha=.25, lw=.4); ax.set_title(f"21 June, {sky}", fontsize=7.5)
    axs[0].set_ylabel("Mean heading RMSE (deg)")
    h, l_ = axs[0].get_legend_handles_labels()
    fig.legend(h, l_, loc="upper center", ncol=6, fontsize=6.5, frameon=False)
    fig.tight_layout(pad=0.3, rect=(0, 0, 1, 0.9)); fig.savefig(O / "fig_envelope.pdf"); fig.savefig(O / "fig_envelope.png", dpi=200); plt.close(fig)


def fig_traj():
    """One held out trajectory at level D3, June 12:30 and 09:30, clear sky, filter seed 0."""
    sys.path.insert(0, str(ROOT / "experiments" / "E02"))
    import run_filters as rf
    from vectra.filter2 import run_filter
    from vectra.sky import compass_cue
    f = sorted(rf.VO_DIR.glob("MiddleEast__Data_omni__*.npz"))[0]
    z = np.load(f); x, y, yaw = z["x"], z["y"], z["yaw"]
    nimu = min(len(z["gyro"]), 10 * len(x)); nfr = nimu // 10; dt = 0.01
    im, co, fl = cfg["imu"], cfg["compass"], cfg["filter"]
    vo = z["D3_s0"][:nfr]
    cue_idx = np.arange(0, nimu, 20); t_cue = cue_idx * dt
    yaw_i = np.interp(t_cue, np.arange(nfr) * 0.1, np.unwrap(yaw[:nfr]))
    g, a = rf.noisy_imu(z["gyro"][:nimu], z["acc"][:nimu], im, dt, np.random.default_rng(rf.seed_of("imu", f.stem, "D3_s0", 0)))
    p0 = np.array([1e-4, 1e-4, 1e-6, 4.0, 4.0, im["gyro_bias_init_sigma"] ** 2] + [im["accel_bias_init_sigma"] ** 2] * 2)
    x0 = np.array([x[0], y[0], yaw[0], (x[1] - x[0]) / 0.1, (y[1] - y[0]) / 0.1, 0.0, 0.0, 0.0])
    scen = rf.scenarios(cfg)
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 2.35))
    for ax, tm in zip(axs, ["09:30", "12:30"]):
        sc = {"local_start": f"2026-06-21T{tm}", "sky": "clear"}
        si = next(i for i, s in enumerate(scen) if s["date"] == "2026-06-21" and s["time"] == tm and s["sky"] == "clear")
        cue = compass_cue(t_cue, yaw_i, sc, cfg["sky"], co, np.random.default_rng(rf.seed_of("cue", f.stem, "D3_s0", si, 0)))
        ax.plot(x[:nfr], y[:nfr], color="k", lw=1.6, label="Ground truth")
        for e in ["B0", "B1", "B1g", "B3"]:
            out, _, _, _ = run_filter(rf.ESTIMATORS[e], dt, g, a, np.arange(nfr) * 10, vo[:, 0] > 0, vo[:, 1], vo[:, 2], vo[:, 3],
                                      cue_idx, cue["valid"], cue["z"], cue["d_meas"], x0, p0, im["gyro_noise_density"],
                                      im["accel_noise_density"], im["gyro_bias_rw"], im["accel_bias_rw"], np.array(fl["vo_sigma"]) ** 2,
                                      fl["vo_gate_chi2_3dof"], np.radians(fl["heading_nominal_sigma_deg"]), fl["heading_gate_chi2_1dof"],
                                      int(fl["b2_window"]), np.radians(co["c_deg"]), np.radians(co["floor_deg"]), int(fl["vo_nis_window"]))
            c, m, l = STY[e]
            ax.plot(out[:, 0], out[:, 1], color=c, ls=l, lw=1, label=e)
        ax.set_aspect("equal", adjustable="datalim"); ax.grid(alpha=.25, lw=.4)
        ax.set_title(f"D3, 21 June {tm}, clear sky (sun zenith {np.mean(cue['zen']):.0f} deg)", fontsize=7.5)
        ax.set_xlabel("North (m)"); ax.set_ylabel("East (m)")
    axs[0].legend(fontsize=6, frameon=False)
    fig.tight_layout(); fig.savefig(O / "fig_traj.pdf"); fig.savefig(O / "fig_traj.png", dpi=200); plt.close(fig)


if __name__ == "__main__":
    which = sys.argv[1:] or ["sky"]
    for w in which:
        globals()["fig_" + w]()
    print("ok")

"""E02 step 2: run every estimator on the saved visual odometry measurements, under every
sky scenario, and write one row per run.

IMU noise is added to the noise free dataset IMU. The compass cue comes from the sky model.
Every random stream is seeded from (stream, trajectory name, VO run key, scenario, seed).

Usage: python run_filters.py --split pilot|heldout --out results/e02_<split>.csv [--set key=value ...]
"""
import argparse
import copy
import csv
import hashlib
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config          # noqa: E402
from vectra.filter2 import run_filter          # noqa: E402
from vectra.sky import compass_cue             # noqa: E402
from vectra.evaluation import run_metrics      # noqa: E402

ESTIMATORS = {"B0": 0, "B1": 1, "B2": 2, "B1g": 3, "B3": 4, "B3a": 5}
VO_DIR = ROOT / "results" / "e02_vo"


def seed_of(*parts):
    h = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return int.from_bytes(h[:8], "little")


def scenarios(cfg):
    out = []
    for d in cfg["sky"]["dates"]:
        for t in cfg["sky"]["start_times"]:
            for s in cfg["sky"]["conditions"]:
                out.append({"local_start": f"{d}T{t}", "date": d, "time": t, "sky": s})
    return out


def noisy_imu(gyro, acc, im, dt, rng):
    n = len(gyro)
    bg = rng.normal(0, im["gyro_bias_init_sigma"]) + np.cumsum(rng.normal(0, im["gyro_bias_rw"] * np.sqrt(dt), n))
    ba = rng.normal(0, im["accel_bias_init_sigma"], 2) + np.cumsum(rng.normal(0, im["accel_bias_rw"] * np.sqrt(dt), (n, 2)), 0)
    g = gyro + bg + rng.normal(0, im["gyro_noise_density"] / np.sqrt(dt), n)
    a = acc + ba + rng.normal(0, im["accel_noise_density"] / np.sqrt(dt), (n, 2))
    return g, a


def split_files(cfg, split):
    envs = cfg["data"][split]
    excl = set(cfg["data"].get("excluded", []))
    return sorted(f for f in VO_DIR.glob("*.npz") if f.stem.split("__")[0] in envs
                  and f.stem.replace("__", "/") not in excl)


def process(args):
    path, cfg, split, estimators = args
    z = np.load(path)
    name = path.stem
    x, y, yaw = z["x"], z["y"], z["yaw"]
    n = len(x)
    dt = 1.0 / cfg["imu"]["rate_hz"]
    gyro, acc = z["gyro"], z["acc"]
    nimu = min(len(gyro), 10 * n)
    gyro, acc = gyro[:nimu], acc[:nimu]
    nfr = nimu // 10
    traj = {"x": x[:nfr], "y": y[:nfr], "theta": yaw[:nfr], "dt": 0.1,
            "path_length": float(np.sum(np.hypot(np.diff(x[:nfr]), np.diff(y[:nfr]))))}
    f = cfg["filter"]
    co = cfg["compass"]
    im = cfg["imu"]
    rvo = np.array(f["vo_sigma"]) ** 2
    vo_idx = np.arange(nfr) * 10
    cue_step = int(round(cfg["imu"]["rate_hz"] / co["rate_hz"]))
    cue_idx = np.arange(0, nimu, cue_step)
    t_cue = cue_idx * dt
    yaw_imu = np.interp(t_cue, np.arange(nfr) * 0.1, np.unwrap(yaw[:nfr]))
    p0 = np.array([1e-4, 1e-4, 1e-6, 4.0, 4.0, im["gyro_bias_init_sigma"] ** 2] + [im["accel_bias_init_sigma"] ** 2] * 2)
    v0 = np.array([(x[1] - x[0]) / 0.1, (y[1] - y[0]) / 0.1])
    x0 = np.array([x[0], y[0], yaw[0], v0[0], v0[1], 0.0, 0.0, 0.0])
    rows = []
    vo_keys = [k for k in z.files if k.startswith("D")]
    for key in vo_keys:
        level, dseed = key.split("_")
        vo = z[key][:nfr]
        for si, sc in enumerate(scenarios(cfg)):
            for fs in range(cfg["filter_seeds"]):
                g, a = noisy_imu(gyro, acc, im, dt, np.random.default_rng(seed_of("imu", name, key, fs)))
                cue = compass_cue(t_cue, yaw_imu, sc, cfg["sky"], co, np.random.default_rng(seed_of("cue", name, key, si, fs)))
                for e in estimators:
                    out, oxy, nu, ng = run_filter(
                        ESTIMATORS[e], dt, g, a, vo_idx, vo[:, 0] > 0, vo[:, 1], vo[:, 2], vo[:, 3],
                        cue_idx, cue["valid"], cue["z"], cue["d_meas"], x0, p0,
                        im["gyro_noise_density"], im["accel_noise_density"], im["gyro_bias_rw"], im["accel_bias_rw"],
                        rvo, f["vo_gate_chi2_3dof"], np.radians(f["heading_nominal_sigma_deg"]),
                        f["heading_gate_chi2_1dof"], int(f["b2_window"]), np.radians(co["c_deg"]),
                        np.radians(co["floor_deg"]), int(f["vo_nis_window"]))
                    est = {"x": out[:, 0], "y": out[:, 1], "theta": out[:, 2], "Pxx": out[:, 3], "Pyy": out[:, 4],
                           "Ptt": out[:, 5], "Pxy": oxy, "h_used": int(nu), "h_gated": int(ng)}
                    m = run_metrics(traj, est, f["failure_drift_ratio_pct"])
                    rows.append({"split": split, "traj": name, "env": name.split("__")[0], "level": level,
                                 "dseed": dseed, "date": sc["date"], "time": sc["time"], "sky": sc["sky"],
                                 "fseed": fs, "estimator": e, "zen_mean": float(np.mean(cue["zen"])),
                                 "zen_min": float(np.min(cue["zen"])),
                                 "cue_dop_med": float(np.median(cue["d_true"])),
                                 "vo_ok_frac": float(np.mean(vo[1:, 0] > 0)), **m})
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["pilot", "heldout"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--estimators", nargs="*", default=list(ESTIMATORS))
    a = ap.parse_args()
    cfg = load_config(ROOT / "configs" / "e02.yaml")
    for item in a.set:
        k, v = item.split("=", 1)
        d = cfg
        ks = k.split(".")
        for p in ks[:-1]:
            d = d[p]
        d[ks[-1]] = eval(v)
    files = split_files(cfg, a.split)
    print(len(files), "trajectories", flush=True)
    rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(process, [(f, cfg, a.split, a.estimators) for f in files]):
            rows += r
            print(len(rows), flush=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", a.out, len(rows))

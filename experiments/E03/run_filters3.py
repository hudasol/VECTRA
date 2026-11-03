"""Study 3 step 2: run the Study 3 estimators on saved VO measurements with the Study 3 compass simulator.
One row per run. Every random stream is seeded from (stream, trajectory, VO key, scenario, draw).

Usage: python run_filters3.py --split dev|confirm|pilot|nondesert --out results/e03/<file>.csv.gz
       [--estimators ...] [--coupling 1|0] [--draws N] [--keys D0_s0 D2_s0 ...] [--max-traj N]"""
import argparse
import gzip
import csv
import hashlib
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "E02"))
from vectra.config import load_config                    # noqa: E402
from vectra.filter3 import run_filter3                   # noqa: E402
from vectra.compass3 import (SkyTable, compass_cue3, sun_sensor_cue, magnetometer_cue,   # noqa: E402
                             wheel_odometry)
from vectra.evaluation import run_metrics                # noqa: E402
from run_filters import noisy_imu                        # noqa: E402

DEG = np.pi / 180
# name: (h_mode, cue source, odometry, calibrated, lockout)
ESTIMATORS = {
    "B0": (0, "zenith", "vo", 0, 0), "B1": (1, "zenith", "vo", 0, 0), "B1g": (3, "zenith", "vo", 0, 0),
    "B2": (2, "zenith", "vo", 0, 0), "B3": (4, "zenith", "vo", 0, 0), "B4": (6, "zenith", "vo", 0, 0),
    "B5": (7, "zenith", "vo", 0, 0), "B6": (8, "zenith", "vo", 0, 0), "B7": (9, "zenith", "vo", 0, 0),
    "B8": (10, "zenith", "vo", 0, 0), "B3L": (4, "zenith", "vo", 0, 1), "B3C": (4, "zenith", "vo", 1, 0),
    "B3R": (4, "ring", "vo", 0, 0), "B4R": (6, "ring", "vo", 0, 0), "SUN": (4, "sun", "vo", 0, 0),
    "MAG": (4, "mag", "vo", 0, 0), "W0": (0, "zenith", "wo", 0, 0), "W3": (4, "zenith", "wo", 0, 0),
    "W4R": (6, "ring", "wo", 0, 0),
    # diagnostics: oracle heading (true yaw, 0.01 degree) and oracle translation (true body velocity, no compass)
    "ORH": (4, "oracle", "vo", 0, 0), "ORT": (0, "zenith", "votrue", 0, 0),
}
VIS = {"D0": None, "D1": 1000.0, "D2": 200.0, "D3": 60.0, "D4": 20.0}
SKY_TABLE = None
ASSUME_TILT = False
DIRS = {"dev": "e02_vo", "pilot": "e02_vo", "confirm": "e03_vo", "nondesert": "e03_vo"}
ENVS = {"pilot": ["WesternDesertTown"], "dev": ["DesertGasStation", "MiddleEast", "EndofTheWorld"],
        "confirm": ["Ruins", "AncientTowns", "HQWesternSaloon"], "nondesert": ["Gascola"]}


def seed_of(*parts):
    return int.from_bytes(hashlib.sha256("|".join(map(str, parts)).encode()).digest()[:8], "little")


def scenarios(s3, clim):
    out = []
    for d in s3["dates"]:
        mo = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][int(d[5:7]) - 1]
        for t in s3["start_times"]:
            rng = np.random.default_rng(seed_of("scenario", d, t))
            aod = clim["AOD_55"][mo] * float(np.exp(rng.normal(0, s3["aod_lognormal_sigma"])))
            cloud = bool(rng.random() < clim["CLOUD_AMT"][mo] / 100.0)
            out.append({"local_start": f"{d}T{t}", "date": d, "time": t, "month": mo, "aod_bg": aod, "cloud": cloud})
    return out


def b8_prob(model, d_meas, zen, z, dyaw_gyro):
    """Learned reliability (logistic regression fitted on the pilot split)."""
    if model is None:
        return np.zeros(len(z))
    dz = np.r_[0.0, np.diff(z)]
    incons = np.abs((dz - dyaw_gyro + np.pi / 2) % np.pi - np.pi / 2)
    X = np.c_[np.log(np.maximum(d_meas, 1e-4)), np.cos(zen * DEG), np.log(incons + 1e-4)]
    Xs = (X - np.array(model["mean"])) / np.array(model["scale"])
    return 1 / (1 + np.exp(-(Xs @ np.array(model["coef"]) + model["intercept"])))


def features(cue, gyro_int_cue):
    dz = np.r_[0.0, np.diff(cue["z"])]
    incons = np.abs((dz - gyro_int_cue + np.pi / 2) % np.pi - np.pi / 2)
    return np.c_[np.log(np.maximum(cue["d_meas"], 1e-4)), np.cos(cue["zen"] * DEG), np.log(incons + 1e-4)]


def process(args):
    path, cfg, split, estimators, coupling, draws, keys, dump_features = args
    s3 = cfg["s3"]
    clim = json.loads((ROOT / s3["power_climatology"]).read_text())
    table = SkyTable(ROOT / (SKY_TABLE or s3["sky_table"]))
    pf = json.loads((ROOT / "results" / "e03" / "pilot_fit.json").read_text())
    b8p = ROOT / "results" / "e03" / "b8_model.json"
    b8 = json.loads(b8p.read_text()) if b8p.exists() else None
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
    f, co, im, fl = cfg["filter"], s3["compass"], cfg["imu"], s3["filter"]
    rvo = np.array(f["vo_sigma"]) ** 2
    vo_idx = np.arange(nfr) * 10
    cue_step = int(round(cfg["imu"]["rate_hz"] / co["rate_hz"]))
    cue_idx = np.arange(0, nimu, cue_step)
    t_cue = cue_idx * dt
    tf = np.arange(nfr) * 0.1
    yaw_cue = np.interp(t_cue, tf, np.unwrap(yaw[:nfr]))
    roll = pitch = None
    ASSUME_TILT = bool(s3.get("assume_tilt", False))
    tilt_src = "gauss_markov_assumed"
    if "roll" in z.files and not ASSUME_TILT:
        roll = np.interp(t_cue, tf, np.unwrap(z["roll"][:nfr]))
        pitch = np.interp(t_cue, tf, np.unwrap(z["pitch"][:nfr]))
        tilt_src = "rendered_terrain"
    _c, _s = np.cos(yaw[:nfr]), np.sin(yaw[:nfr])
    _vx, _vy = np.gradient(x[:nfr], 0.1), np.gradient(y[:nfr], 0.1)
    vtrue = (_c * _vx + _s * _vy, -_s * _vx + _c * _vy)
    x0 = np.array([x[0], y[0], yaw[0], (x[1] - x[0]) / 0.1, (y[1] - y[0]) / 0.1, 0, 0, 0, 0, 0.0])
    rows, feats = [], []
    vo_keys = [k for k in z.files if k.startswith("D") and (not keys or k in keys)]
    scen = scenarios(s3, clim)
    for key in vo_keys:
        level, dseed = key.split("_")
        vo = z[key][:nfr]
        dust = 0.0 if (not coupling or VIS[level] is None) else 3.912 / VIS[level] * s3["dust_layer_m"]
        for si, sc in enumerate(scen):
            scd = dict(sc, aod=sc["aod_bg"] + dust, lat=cfg["sky"]["location"]["lat_deg"],
                       lon=cfg["sky"]["location"]["lon_deg"], utc=cfg["sky"]["location"]["utc_offset_h"])
            for fs in range(draws):
                g, a = noisy_imu(gyro, acc, im, dt, np.random.default_rng(seed_of("imu", name, key, fs)))
                gint = np.r_[0.0, np.diff((np.cumsum(g) * dt)[cue_idx])]
                cues = {}
                for geo in ("zenith", "ring"):
                    cues[geo] = compass_cue3(t_cue, yaw_cue, scd, table, co,
                                             np.random.default_rng(seed_of("cue", name, key, si, fs)),
                                             roll, pitch, geometry=geo)
                zc = cues["zenith"]
                cues["sun"] = sun_sensor_cue(zc["zen"], zc["az"], yaw_cue, co,
                                             np.random.default_rng(seed_of("sun", name, key, si, fs)))
                cues["oracle"] = {"z": yaw_cue, "r_est": np.full(len(yaw_cue), (0.01 * DEG) ** 2),
                                  "err": np.zeros(len(yaw_cue))}
                cues["mag"] = magnetometer_cue(yaw_cue, co, np.random.default_rng(seed_of("mag", name, key, si, fs)))
                if dump_features:
                    lab = np.abs(zc["err"]) > 3 * np.sqrt(zc["r_est"])
                    feats.append(np.c_[features(zc, gint), lab])
                p_b8 = b8_prob(b8, zc["d_meas"], zc["zen"], zc["z"], gint)
                wo = wheel_odometry(x[:nfr], y[:nfr], yaw[:nfr], 0.1, s3["wheel_odometry"],
                                    np.random.default_rng(seed_of("wo", name, key, fs)))
                for e in estimators:
                    hm, src, odo, cal, lock = ESTIMATORS[e]
                    cue = cues[src]
                    if odo == "vo":
                        ok, vf, vr, vw = vo[:, 0] > 0, vo[:, 1], vo[:, 2], vo[:, 3]
                        r_odo = rvo
                    elif odo == "votrue":
                        ok, vf, vr, vw = np.ones(nfr, bool), vtrue[0], vtrue[1], vo[:, 3]
                        r_odo = np.array([1e-4, 1e-4, rvo[2]])
                    else:
                        ok, vf, vr, vw = np.ones(nfr, bool), wo[0], wo[1], wo[2]
                        wcfg = s3["wheel_odometry"]
                        r_odo = np.array([wcfg["speed_sigma"] ** 2 + (0.15 * 1.0) ** 2 * wcfg["slip_frac"],
                                          wcfg["speed_sigma"] ** 2 + (0.15 * 1.0) ** 2 * wcfg["slip_frac"],
                                          wcfg["yaw_rate_sigma"] ** 2 + 0.05 ** 2])
                    p0 = np.array([1e-4, 1e-4, 1e-6, 4.0, 4.0, im["gyro_bias_init_sigma"] ** 2,
                                   im["accel_bias_init_sigma"] ** 2, im["accel_bias_init_sigma"] ** 2,
                                   (fl["bias_init_deg"] * DEG) ** 2 if hm == 9 else 0.0,
                                   pf["sv_sigma"] ** 2 if cal else 0.0])
                    out, nu, ng, mrg = run_filter3(
                        hm, dt, g, a, vo_idx, ok, vf, vr, vw, cue_idx, zc["valid"], np.mod(cue["z"], np.pi),
                        cue["r_est"], p_b8, x0, p0, im["gyro_noise_density"], im["accel_noise_density"],
                        im["gyro_bias_rw"], im["accel_bias_rw"], fl["bias_rw_deg_sqrt_s"] * DEG if hm == 9 else 0.0,
                        pf["sv_sigma"] if cal else 0.0, pf["sv_tau_s"], r_odo, pf["rgm_extra"] if cal else 0.0,
                        f["vo_gate_chi2_3dof"], np.radians(f["heading_nominal_sigma_deg"]),
                        f["heading_gate_chi2_1dof"], int(f["b2_window"]), (fl["r_bad_deg"] * DEG) ** 2,
                        fl["prior_bad"], fl["huber_k"], fl["lockout_samples"] if lock else 0)
                    est = {"x": out[:, 0], "y": out[:, 1], "theta": out[:, 2], "Pxx": out[:, 3], "Pyy": out[:, 4],
                           "Ptt": out[:, 5], "Pxy": out[:, 6], "h_used": int(nu), "h_gated": int(ng)}
                    m = run_metrics(traj, est, f["failure_drift_ratio_pct"])
                    rows.append({"split": split, "traj": name, "env": name.split("__")[0], "level": level,
                                 "dseed": dseed, "date": sc["date"], "time": sc["time"], "cloud": int(sc["cloud"]),
                                 "aod": round(scd["aod"], 4), "fseed": fs, "estimator": e, "coupling": int(coupling),
                                 "tilt_src": tilt_src, "zen_min": float(np.min(zc["zen"])),
                                 "cue_dop_med": float(np.median(zc["d_true"])),
                                 "cue_err_rms_deg": float(np.degrees(np.sqrt(np.mean(((cue["err"] + np.pi / 2) % np.pi - np.pi / 2) ** 2)))),
                                 "max_run_gated": int(mrg), "vo_ok_frac": float(np.mean(vo[1:, 0] > 0)), **m})
    return rows, (np.vstack(feats) if feats else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=list(ENVS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--estimators", nargs="*", default=[e for e in ESTIMATORS if e not in ("ORH", "ORT")])
    ap.add_argument("--coupling", type=int, default=1)
    ap.add_argument("--draws", type=int, default=None)
    ap.add_argument("--keys", nargs="*", default=[])
    ap.add_argument("--max-traj", type=int, default=0)
    ap.add_argument("--dump-features", default="")
    ap.add_argument("--sky-table", default="")
    ap.add_argument("--assume-tilt", type=int, default=0)
    a = ap.parse_args()
    cfg = load_config(ROOT / "configs" / "e03.yaml")
    if a.sky_table:
        cfg["s3"]["sky_table"] = a.sky_table
    if a.assume_tilt:
        cfg["s3"]["assume_tilt"] = True
    draws = a.draws or (cfg["s3"]["imu_draws_confirm"] if a.split == "confirm" else cfg["s3"]["imu_draws_dev"])
    excl = set(cfg["data"].get("excluded", []))
    files = sorted(p for p in (ROOT / "results" / DIRS[a.split]).glob("*.npz")
                   if p.stem.split("__")[0] in ENVS[a.split] and p.stem.replace("__", "/") not in excl)
    if a.max_traj:
        files = files[:a.max_traj]
    print(len(files), "trajectories", flush=True)
    rows, feats = [], []
    with Pool(a.workers) as pool:
        for r, fe in pool.imap_unordered(process, [(p, cfg, a.split, a.estimators, a.coupling, draws, a.keys,
                                                     bool(a.dump_features)) for p in files]):
            rows += r
            if fe is not None:
                feats.append(fe)
            print(len(rows), flush=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(a.out, "wt", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    if a.dump_features:
        np.save(a.dump_features, np.vstack(feats))
    print("wrote", a.out, len(rows))


if __name__ == "__main__":
    main()

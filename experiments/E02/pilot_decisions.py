"""E02 pilot decisions, computed on the pilot split only.

1. Nominal visual noise: 1.4826 times the median absolute deviation of the D0 visual
   odometry errors (forward speed, right speed, yaw rate), pooled over pilot trajectories.
2. Visual odometry statistics per level (success fraction, robust error), to check that the
   levels are graded and D4 is not fully saturated.
Writes results/e02_pilot_vo_stats.csv and prints the values to copy into configs/e02.yaml.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
VO = ROOT / "results" / "e02_vo"
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config     # noqa: E402


def truth_body(x, y, yaw):
    dp = np.diff(np.c_[x, y], axis=0)
    th = yaw[:-1]
    vf = (np.cos(th) * dp[:, 0] + np.sin(th) * dp[:, 1]) / 0.1
    vr = (-np.sin(th) * dp[:, 0] + np.cos(th) * dp[:, 1]) / 0.1
    w = np.diff(np.unwrap(yaw)) / 0.1
    return vf, vr, w


def mad_sigma(e):
    return 1.4826 * np.median(np.abs(e - np.median(e)))


if __name__ == "__main__":
    cfg = load_config(ROOT / "configs" / "e02.yaml")
    split = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    envs = cfg["data"][split]
    rows, d0 = [], {"vf": [], "vr": [], "w": []}
    for f in sorted(VO.glob("*.npz")):
        if f.stem.split("__")[0] not in envs:
            continue
        z = np.load(f)
        vf, vr, w = truth_body(z["x"], z["y"], z["yaw"])
        for k in [k for k in z.files if k.startswith("D")]:
            r = z[k]
            ok = r[1:, 0] > 0
            ef, er, ew = (r[1:, 1] - vf)[ok], (r[1:, 2] - vr)[ok], (r[1:, 3] - w)[ok]
            rows.append({"traj": f.stem, "run": k, "level": k.split("_")[0], "ok_frac": ok.mean(),
                         "sig_vf": mad_sigma(ef), "sig_vr": mad_sigma(er), "sig_w": mad_sigma(ew),
                         "p90_speed_err": np.percentile(np.hypot(ef, er), 90) if ok.any() else np.nan})
            if k.startswith("D0"):
                d0["vf"].append(ef); d0["vr"].append(er); d0["w"].append(ew)
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results" / f"e02_{split}_vo_stats.csv", index=False)
    print(df.groupby("level")[["ok_frac", "sig_vf", "sig_vr", "sig_w", "p90_speed_err"]].median().round(4))
    if split == "pilot":
        s = [round(float(mad_sigma(np.concatenate(d0[k]))), 4) for k in ["vf", "vr", "w"]]
        print("vo_sigma (pilot rule):", s)

"""Descriptive (post hoc, development split): forward speed scale bias and lag one autocorrelation of the VO errors.
Output results/e03/vo_bias_dev.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
rows = []
for f in sorted((ROOT / "results/e02_vo").glob("*.npz")):
    if f.stem.startswith("WesternDesertTown"):
        continue
    z = np.load(f)
    n = len(z["x"])
    yaw = z["yaw"]
    vf = np.cos(yaw) * np.gradient(z["x"], 0.1) + np.sin(yaw) * np.gradient(z["y"], 0.1)
    for lv in ["D0", "D2", "D4"]:
        vo = z[f"{lv}_s0"][:n]
        ok = (vo[:, 0] > 0) & (np.abs(vf) > 0.3)
        if ok.sum() < 50:
            continue
        r = vo[ok, 1] / vf[ok]
        e = vo[ok, 1] - vf[ok]
        rows.append({"traj": f.stem, "level": lv, "scale_median": float(np.median(r)),
                     "err_mean": float(np.mean(e)), "err_sd": float(np.std(e)),
                     "lag1": float(np.corrcoef(e[:-1], e[1:])[0, 1])})
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results/e03/vo_bias_dev.csv", index=False)
print(df.groupby("level")[["scale_median", "err_mean", "err_sd", "lag1"]].median().round(3))

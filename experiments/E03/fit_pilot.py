"""Study 3 pilot fits (pilot split only, WesternDesertTown): coloured visual noise (AR(1) on the forward speed
scale error) and the extra variance of the averaged gyro in the bias measurement. Output results/e03/pilot_fit.json"""
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
files = sorted((ROOT / "results" / "e02_vo").glob("WesternDesertTown__*.npz"))
rows = {}
for lv in ["D0", "D1", "D2", "D3", "D4"]:
    rho, sd, wsd = [], [], []
    for f in files:
        z = np.load(f)
        x, y, yaw = z["x"], z["y"], z["yaw"]
        vf_true = np.cos(yaw) * np.gradient(x, 0.1) + np.sin(yaw) * np.gradient(y, 0.1)
        vo = z[f"{lv}_s0"]
        ok = (vo[:, 0] > 0) & (np.abs(vf_true) > 0.3)
        e = np.where(ok, vo[:, 1] / np.where(ok, vf_true, 1) - 1, np.nan)
        e = e[np.isfinite(e)]
        e = e[np.abs(e) < 1.0]
        if len(e) < 50:
            continue
        # low pass part (coloured) by a 2 s moving average; AR(1) fitted to it
        k = 20
        m = np.convolve(e, np.ones(k) / k, mode="valid")
        r1 = np.corrcoef(m[:-1], m[1:])[0, 1]
        rho.append(r1)
        sd.append(np.std(m))
        wsd.append(np.std(e - np.convolve(e, np.ones(k) / k, mode="same")))
    tau = float(-0.1 / np.log(np.clip(np.median(rho), 1e-3, 0.9999)))
    rows[lv] = {"sv_sigma": float(np.median(sd)), "sv_tau_s": tau, "white_sd": float(np.median(wsd)), "n_traj": len(sd)}
fit = {"levels": rows,
       "sv_sigma": float(np.median([r["sv_sigma"] for r in rows.values()])),
       "sv_tau_s": float(np.median([r["sv_tau_s"] for r in rows.values()])),
       "rgm_extra": 0.002 ** 2 / 0.01 / 10,
       "note": "rgm_extra is the variance of the mean of ten gyro samples (noise density 0.002 rad/s/sqrt(Hz), 100 Hz)"}
(ROOT / "results" / "e03" / "pilot_fit.json").write_text(json.dumps(fit, indent=1))
print(json.dumps(fit, indent=1))

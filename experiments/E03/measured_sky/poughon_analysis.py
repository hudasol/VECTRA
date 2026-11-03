"""MEASURED check of the zenith model with the open Marseille skylight polarisation images (Poughon et al.)."""
import json, sys
import numpy as np
from datetime import datetime, timedelta
ROOT = __import__("pathlib").Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from vectra.sky import sun_position
from vectra.compass3 import SkyTable
R = json.load(open(sys.argv[1]))
out_path = sys.argv[2]
tab = SkyTable(ROOT / "results/e03_sky/dop_tables.npz")
rows = []
for r in R:
    t = datetime.strptime(r["t"], "%Y-%m-%dT%H-%M-%S") - timedelta(hours=2)
    z, az = sun_position(43.296, 5.394, t)
    if z > 85 or r["max"] < 1000:
        continue
    p = r["p_40"]
    I = dict(zip((90, 45, 135, 0), p))
    S0 = (I[0] + I[45] + I[90] + I[135]) / 2
    S1, S2 = I[0] - I[90], I[45] - I[135]
    rows.append((z, az, np.hypot(S1, S2) / S0, 0.5 * np.arctan2(S2, S1), r["label"], r["t"]))
z = np.array([x[0] for x in rows]); az = np.radians([x[1] for x in rows]); d = np.array([x[2] for x in rows])
aop = np.array([x[3] for x in rows]); lab = np.array([x[4] for x in rows])
best = None
for sgn in (1, -1):
    pred0 = sgn * az + np.pi / 2
    # circular mean of the offset on the doubled angle
    off = 0.5 * np.angle(np.mean(np.exp(2j * (aop - pred0))))
    res = (aop - pred0 - off + np.pi / 2) % np.pi - np.pi / 2
    rms = np.sqrt(np.mean(res ** 2))
    if best is None or rms < best[0]:
        best = (rms, sgn, off, res)
rms, sgn, off, res = best
# per label summary and a fit of sigma^2 = floor^2 + (c/d)^2 on samples with |res| < 30 deg (robust)
from scipy.optimize import least_squares
bins = np.quantile(d, np.linspace(0, 1, 9))
bin_rows = []
for i in range(8):
    m = (d >= bins[i]) & (d <= bins[i + 1])
    bin_rows.append({"d_lo": float(bins[i]), "d_hi": float(bins[i + 1]), "n": int(m.sum()),
                     "d_med": float(np.median(d[m])), "res_rms_deg": float(np.degrees(np.sqrt(np.mean(res[m] ** 2)))),
                     "res_mad_deg": float(np.degrees(1.4826 * np.median(np.abs(res[m]))))})
dm = np.array([b["d_med"] for b in bin_rows]); sm = np.radians([b["res_mad_deg"] for b in bin_rows])
f = least_squares(lambda q: np.log(np.sqrt(q[0] ** 2 + (q[1] / dm) ** 2)) - np.log(sm), [0.01, 0.001], bounds=([1e-5, 1e-6], [1, 1]))
model = {}
for aod in (0.15, 0.3, 0.45):
    model[str(aod)] = [float(tab(aod, zz)[0]) for zz in (30, 45, 60, 75)]
meas = {}
for zz in (30, 45, 60, 75):
    m = np.abs(z - zz) < 3
    meas[str(zz)] = {"median_dop": float(np.median(d[m])) if m.any() else None, "n": int(m.sum())}
summary = {"source": "Poughon et al. 2024, 1 month skylight polarisation images, doi:10.57745/610QTS, CC BY-SA 4.0, day 2022-07-29, MEASURED",
           "n_images_daylight": int(len(d)), "time_zone_fit": "UTC+2 (DoP versus sin^2 of solar zenith, r = 0.98)",
           "aop_sign": int(sgn), "aop_offset_deg": float(np.degrees(off)), "aop_residual_rms_deg": float(np.degrees(rms)),
           "aop_residual_mad_deg": float(np.degrees(1.4826 * np.median(np.abs(res)))),
           "per_label_median_dop": {l: float(np.median(d[lab == l])) for l in np.unique(lab)},
           "per_label_res_mad_deg": {l: float(np.degrees(1.4826 * np.median(np.abs(res[lab == l])))) for l in np.unique(lab)},
           "bins": bin_rows, "fit_floor_deg": float(np.degrees(abs(f.x[0]))), "fit_c_deg": float(np.degrees(abs(f.x[1]))),
           "frozen_law": {"floor_deg": 0.5, "c_deg": 0.05},
           "zenith_dop_measured_by_sun_zenith": meas, "zenith_dop_model_rt_by_aod": model,
           "corr_dop_sin2": float(np.corrcoef(d, np.sin(np.radians(z)) ** 2)[0, 1])}
json.dump(summary, open(out_path, "w"), indent=1)
np.savez_compressed(out_path.replace(".json", "_series.npz"), sun_zen=z, sun_az=np.degrees(az), dop=d, aop_res_deg=np.degrees(res), label=lab)
print(json.dumps(summary, indent=1))

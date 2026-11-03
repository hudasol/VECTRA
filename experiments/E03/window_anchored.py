"""Blind window on 21 June with the measured anchored DoP table (clear sky law fitted to the Marseille images,
aerosol attenuation from radiative transfer). Output results/e03_sky/blind_window_anchored.json"""
import json
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "E03"))
sys.path.insert(0, str(ROOT / "src"))
import sky_v2 as S
out = {}
clim = json.loads((ROOT / "results/e03_sky/power_24.45_54.38.json").read_text())
for name, f in [("radiative_transfer", "dop_tables.npz"), ("measured_anchored", "dop_tables_anchored.npz")]:
    z = np.load(ROOT / "results/e03_sky" / f)
    for lab, mult in [("low", 0.5), ("mean", 1.0), ("high", 1.5)]:
        cv = S.sigma_curves(z["dop"], z["ring_az"], clim["AOD_55"]["JUN"] * mult)
        for thr in (2.0, 5.0, 10.0):
            m, _ = S.day_minutes(cv, S.LAT, S.LON, S.UTC, 172, thr)
            out[f"{name}|{lab}|gt{int(thr)}"] = dict(zip(["zenith", "zenith_ring", "sun_sensor"], map(int, m)))
# Study 2 law for reference
zz = S.ZF
d2 = 0.6 * np.sin(np.radians(zz)) ** 2 / (1 + np.cos(np.radians(zz)) ** 2)
cv2 = np.stack([np.degrees(S.sigma_point(d2))] * 3, 1)
out["study2_law|gt10"] = int(S.day_minutes(cv2, S.LAT, S.LON, S.UTC, 172, 10.0)[0][0])
(ROOT / "results/e03_sky/blind_window_anchored.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))

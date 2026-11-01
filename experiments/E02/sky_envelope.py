"""Model only: when is the zenith compass blind over Abu Dhabi? Writes results/e02_sky_envelope.json."""
import json, sys
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config                      # noqa: E402
from vectra.sky import sun_position, zenith_dop, aop_sigma  # noqa: E402

cfg = load_config(ROOT / "configs" / "e02.yaml")
loc, co = cfg["sky"]["location"], cfg["compass"]


def sigma_deg(z, dop_scale=1.0):
    return np.degrees(aop_sigma(dop_scale * zenith_dop(z, co["d_max"]), np.radians(co["floor_deg"]), np.radians(co["c_deg"])))


def day(d, h0=5, h1=19):
    base = d - timedelta(hours=loc["utc_offset_h"])
    hrs = np.arange(h0, h1, 1 / 60)
    z = np.array([sun_position(loc["lat_deg"], loc["lon_deg"], base + timedelta(hours=float(h)))[0] for h in hrs])
    return hrs, z, sigma_deg(z)


out = {"days": {}}
for d in ["2026-03-20", "2026-06-21", "2026-09-22", "2026-12-21"]:
    hrs, z, s = day(datetime.fromisoformat(d))
    rec = {"min_zenith_deg": float(z.min()), "time_min_zenith_h": float(hrs[z.argmin()])}
    for th in (2, 5, 10):
        m = (s > th) & (z < 90)
        rec[f"minutes_sigma_gt_{th}"] = int(m.sum())
        rec[f"window_sigma_gt_{th}"] = [float(hrs[m].min()), float(hrs[m].max())] if m.any() else None
    out["days"][d] = rec
blind = []
for k in range(365):
    d = datetime(2026, 1, 1) + timedelta(days=k)
    hrs, z, s = day(d, 11, 14)
    m = int((s > 10).sum())
    if m:
        blind.append((d.strftime("%Y-%m-%d"), m))
# sensitivity: the measured zenith DoP at 70 degrees solar elevation in a desert was about twice the model value
base = datetime(2026, 6, 21) - timedelta(hours=loc["utc_offset_h"])
hrs = np.arange(11, 14, 1 / 60)
z = np.array([sun_position(loc["lat_deg"], loc["lon_deg"], base + timedelta(hours=float(h)))[0] for h in hrs])
out["june21_if_dop_doubled"] = {f"minutes_sigma_gt_{th}": int((sigma_deg(z, 2.0) > th).sum()) for th in (2, 5, 10)}
out["model_zenith_dop_at_elevation"] = {"35": float(zenith_dop(55.0, co["d_max"])), "70": float(zenith_dop(20.0, co["d_max"]))}
out["year_2026"] = {"days_with_sigma_gt_10": len(blind), "first": blind[0][0], "last": blind[-1][0],
                    "max_minutes": max(b[1] for b in blind)}
(ROOT / "results" / "e02_sky_envelope.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["year_2026"]), json.dumps(out["days"]["2026-06-21"]))

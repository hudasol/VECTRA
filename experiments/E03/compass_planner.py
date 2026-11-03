"""Mission scheduling helper (SIMULATED model output): for a site and a date range, list the local times when a
sky polarisation compass is expected to be unreliable (heading noise above a threshold).

Example: python compass_planner.py --lat 24.45 --lon 54.38 --utc 4 --start 2026-06-01 --days 30 --aod 0.56
Options: --table anchored|rt (default anchored, the measured anchored DoP table), --threshold 10 (degrees),
--geometry zenith|zenith_ring. Output: one line per day with the unreliable interval, or 'usable all day'."""
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "E03"))
sys.path.insert(0, str(ROOT / "src"))
import sky_v2 as S   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--utc", type=float, required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--aod", type=float, default=0.4)
    ap.add_argument("--threshold", type=float, default=10.0)
    ap.add_argument("--geometry", choices=["zenith", "zenith_ring"], default="zenith")
    ap.add_argument("--table", choices=["anchored", "rt"], default="anchored")
    a = ap.parse_args()
    z = np.load(ROOT / "results/e03_sky" / ("dop_tables_anchored.npz" if a.table == "anchored" else "dop_tables.npz"))
    cv = S.sigma_curves(z["dop"], z["ring_az"], a.aod)
    col = 0 if a.geometry == "zenith" else 1
    h = np.arange(0, 24 * 60) / 60.0
    d0 = date.fromisoformat(a.start)
    print(f"site {a.lat:.2f}, {a.lon:.2f}, UTC{a.utc:+g}; AOD {a.aod}; {a.geometry}; noise above {a.threshold} deg; "
          f"{a.table} table (SIMULATED)")
    for k in range(a.days):
        day = d0 + timedelta(days=k)
        zs = S.sun_zen_vec(a.lat, a.lon, day.timetuple().tm_yday, h - a.utc)
        s = np.interp(zs, S.ZF, cv[:, col])
        bad = (zs < 85) & (s > a.threshold)
        if bad.any():
            t = h[bad]
            print(f"{day}  unreliable {int(t.min()):02d}:{int(round(60 * (t.min() % 1))):02d} to "
                  f"{int(t.max()):02d}:{int(round(60 * (t.max() % 1))):02d} local ({bad.sum()} min)")
        else:
            print(f"{day}  usable all day")


if __name__ == "__main__":
    main()

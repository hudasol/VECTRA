"""Study 3, sky model v2: radiative transfer tables, validation, climatology, compass geometries, Cramer Rao bound,
blind window with uncertainty and a global latitude by day of year map. All outputs are SIMULATED except the
climatology inputs, which are MEASURED or reanalysis values from NASA POWER (fetched, cached with the access date).

Usage: python sky_v2.py [--photons 100000]
Outputs in results/e03_sky/."""
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timedelta, date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.sky_rt import simulate, view_dirs, single_scatter_rayleigh_dop, observer_ref   # noqa: E402
from vectra.sky import sun_position                                                       # noqa: E402

OUT = ROOT / "results" / "e03_sky"
LAT, LON, UTC = 24.4539, 54.3773, 4
FLOOR, C = np.radians(0.5), np.radians(0.05)          # frozen E02 sensor law (assumed)
ZEN_GRID = np.array([0, 1, 2, 3, 4, 5, 6, 8, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80.0])
AOD_GRID = np.array([0.15, 0.3, 0.45, 0.6, 0.8, 1.2, 2.0, 3.5, 6.0, 10.0])
RING_EL, RING_N = 60.0, 12
POWER_URL = ("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=AOD_55,CLOUD_AMT"
             "&community=RE&longitude={lon}&latitude={lat}&format=JSON")


def views():
    az = np.arange(RING_N) * 360.0 / RING_N
    return np.vstack([view_dirs(90.0, 0.0)[None], view_dirs(RING_EL, az)]), az


def rt_tables(n_ph, g=0.7, p_a=0.2, albedo=0.3, tag="base"):
    v, az = views()
    dop = np.zeros((len(AOD_GRID), len(ZEN_GRID), len(v)))
    aop = np.zeros_like(dop)
    for i, a in enumerate(AOD_GRID):
        for j, z in enumerate(ZEN_GRID):
            r = simulate(z, v, tau_a=a, g=g, p_a=p_a, albedo=albedo, n_photons=n_ph if a < 1 else n_ph // 2,
                         sun_az_deg=180.0, max_orders=40 if a < 1 else 300,
                         rng=np.random.default_rng(1000 * i + j))
            dop[i, j] = r["dop"]
            aop[i, j] = r["aop"]
        print(tag, "aod", a, "zenith DoP", np.round(dop[i, :, 0], 3), flush=True)
    return dop, aop


def aop_pattern(sun_vec, v):
    """Angle of polarisation (rad, mod pi) at upward views v, referenced to observer_ref, E normal to the sun plane."""
    E = np.cross(sun_vec[None, :], v)
    E /= np.linalg.norm(E, axis=-1, keepdims=True) + 1e-15
    e1 = observer_ref(v)
    e2 = np.cross(-v, e1)
    return np.arctan2(np.sum(E * e2, -1), np.sum(E * e1, -1)) % np.pi


def sigma_point(d):
    return np.sqrt(FLOOR ** 2 + (C / np.maximum(d, 1e-6)) ** 2)


def crb_geometry(sun_zen, dop_zen, dop_ring, ring_az, use_zenith=True, use_ring=True):
    """Cramer Rao bound (rad) on heading from AoP only. Derivative of the ring AoP from the single scattering
    plane geometry (exact by symmetry for the zenith point), magnitudes from the radiative transfer DoP."""
    sun = view_dirs(90 - sun_zen, 180.0)
    info = 0.0
    if use_zenith:
        info += 1.0 / sigma_point(dop_zen) ** 2
    if use_ring:
        h = 1e-4
        va = view_dirs(RING_EL, ring_az + np.degrees(h))
        vb = view_dirs(RING_EL, ring_az - np.degrees(h))
        da = (aop_pattern(sun, va) - aop_pattern(sun, vb) + np.pi / 2) % np.pi - np.pi / 2
        deriv = da / (2 * h)
        info += np.sum(deriv ** 2 / sigma_point(dop_ring) ** 2)
    return 1.0 / np.sqrt(max(info, 1e-12))


def mc_check(sun_zen, dop_zen, dop_ring, ring_az, n=1500, rng=None):
    """Monte Carlo check of the bound: least squares heading from noisy zenith and ring AoP."""
    rng = rng or np.random.default_rng(5)
    sun = view_dirs(90 - sun_zen, 180.0)
    psi_grid = np.radians(np.arange(-20, 20.01, 0.05))
    pred = np.stack([np.concatenate([[(np.pi / 2 - p) % np.pi],      # zenith AoP in body frame
                                     aop_pattern(sun, view_dirs(RING_EL, ring_az + np.degrees(p)))]) for p in psi_grid])
    sig = np.concatenate([[sigma_point(dop_zen)], sigma_point(dop_ring)])
    truth = pred[len(psi_grid) // 2]
    est = np.empty(n)
    for k in range(n):
        z = truth + rng.normal(0, sig)
        r = (z[None, :] - pred + np.pi / 2) % np.pi - np.pi / 2
        cost = np.sum((r / sig) ** 2, 1)
        est[k] = psi_grid[np.argmin(cost)]
    return float(np.std(est))


def climatology(lat, lon):
    cache = OUT / f"power_{lat:.2f}_{lon:.2f}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    raw = json.load(urllib.request.urlopen(POWER_URL.format(lat=lat, lon=lon), timeout=60))
    p = raw["properties"]["parameter"]
    out = {"url": POWER_URL.format(lat=lat, lon=lon), "accessed": date.today().isoformat(),
           "source": raw["header"].get("sources"), "AOD_55": p["AOD_55"], "CLOUD_AMT": p["CLOUD_AMT"]}
    cache.write_text(json.dumps(out, indent=1))
    return out


def interp_dop(dop_tab, aod, zen):
    """Bilinear interpolation of the table in AOD and solar zenith, per view."""
    ia = np.clip(np.searchsorted(AOD_GRID, aod) - 1, 0, len(AOD_GRID) - 2)
    fa = np.clip((aod - AOD_GRID[ia]) / (AOD_GRID[ia + 1] - AOD_GRID[ia]), 0, 1)
    row = (1 - fa) * dop_tab[ia] + fa * dop_tab[ia + 1]
    return np.array([np.interp(zen, ZEN_GRID, row[:, k]) for k in range(row.shape[1])])


ZF = np.arange(0.0, 85.01, 0.25)


def sigma_curves(dop_tab, ring_az, aod, sun_sigma=np.radians(0.5)):
    """Heading noise (deg) against solar zenith on a fine grid for the zenith sensor, zenith plus ring, sun sensor."""
    out = np.zeros((len(ZF), 3))
    for i, z in enumerate(ZF):
        d = interp_dop(dop_tab, aod, z)
        out[i] = (np.degrees(sigma_point(d[0])), np.degrees(crb_geometry(z, d[0], d[1:], ring_az)),
                  np.degrees(sun_sigma / max(np.sin(np.radians(z)), 1e-6)))
    return out


def sun_zen_vec(lat_deg, lon_deg, doy, hour_utc, ndays=365):
    """Vectorised form of vectra.sky.sun_position (same NOAA equations), zenith only."""
    g = 2 * np.pi / ndays * (doy - 1 + (hour_utc - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                       - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    ha = np.radians((hour_utc * 60 + eqtime + 4 * lon_deg) / 4 - 180)
    lat = np.radians(lat_deg)
    cz = np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(ha)
    return np.degrees(np.arccos(np.clip(cz, -1, 1)))


def day_minutes(curves, lat, lon, utc, doy, thr):
    """Minutes per day (1 minute steps, sun above 5 degrees) with noise above thr, for each geometry."""
    h = np.arange(0, 24 * 60) / 60.0
    z = sun_zen_vec(lat, lon, doy, h - utc)
    z = z[z < 85]
    s = np.stack([np.interp(z, ZF, curves[:, k]) for k in range(curves.shape[1])], 1)
    return (s > thr).sum(0), float(z.min()) if len(z) else 90.0


def minutes_above(rows, col, thr):
    return 2 * int(np.sum(rows[:, col] > thr))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photons", type=int, default=100000)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    v, ring_az = views()
    val = {}
    # 1. single scattering limit against the analytic Rayleigh law
    err = []
    for z in [10, 30, 50, 70]:
        r = simulate(z, v, tau_r=0.01, tau_a=0.0, albedo=0.0, n_photons=20000, single_only=True, sun_az_deg=180.0)
        gam = np.degrees(np.arccos(np.clip(v @ view_dirs(90 - z, 180.0), -1, 1)))
        err.append(float(np.max(np.abs(r["dop"] - single_scatter_rayleigh_dop(gam)))))
        err.append(float(abs((np.degrees(r["aop"][0]) - 90 + 90) % 180 - 90)))
    val["single_scatter_max_abs_error"] = max(err)
    # 2. tables
    tab, aop_tab = rt_tables(a.photons)
    # sign of the zenith polarisation: E normal to the solar meridian (positive) or along it (negative, a 90 degree flip)
    flip = np.abs(((np.degrees(aop_tab[:, :, 0]) - 90) + 90) % 180 - 90) > 45
    val["zenith_aop_flipped_cells"] = [[float(AOD_GRID[i]), float(ZEN_GRID[j])] for i, j in zip(*np.nonzero(flip))]
    np.savez_compressed(OUT / "dop_tables.npz", dop=tab, aop=aop_tab, zen=ZEN_GRID, aod=AOD_GRID, ring_el=RING_EL, ring_az=ring_az)
    sens = {}
    for tag, kw in {"g0.6_pa0.1": dict(g=0.6, p_a=0.1), "g0.8_pa0.3": dict(g=0.8, p_a=0.3),
                    "albedo0.15": dict(albedo=0.15), "albedo0.45": dict(albedo=0.45)}.items():
        v1 = views()[0][:1]
        sens[tag] = [float(simulate(z, v1, tau_a=0.45, n_photons=a.photons // 2, rng=np.random.default_rng(7),
                                    **kw)["dop"][0]) for z in [20.0, 55.0]]
    val["sensitivity_zenith_dop_at_sun_zen_20_55_aod0.45"] = sens
    # 3. comparison with the measured desert band (zenith DoP at solar elevation 35 and 70 degrees)
    val["model_zenith_dop_elev35"] = {f"{x:.2f}": float(interp_dop(tab, x, 55.0)[0]) for x in AOD_GRID}
    val["model_zenith_dop_elev70"] = {f"{x:.2f}": float(interp_dop(tab, x, 20.0)[0]) for x in AOD_GRID}
    val["measured_band"] = {"elev35": [0.24, 0.30], "elev70": 0.08}
    # 4. Cramer Rao bound against Monte Carlo
    crb = []
    for z in [3.0, 6.0, 10.0, 20.0, 40.0]:
        d = interp_dop(tab, 0.45, z)
        crb.append({"sun_zen": z, "crb_zenith_deg": float(np.degrees(crb_geometry(z, d[0], d[1:], ring_az, True, False))),
                    "crb_zen_ring_deg": float(np.degrees(crb_geometry(z, d[0], d[1:], ring_az))),
                    "mc_zen_ring_deg": float(np.degrees(mc_check(z, d[0], d[1:], ring_az)))})
    val["crb_vs_mc"] = crb
    # 5. climatology and blind window in Abu Dhabi
    clim = climatology(LAT, LON)
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    rows_out = []
    curves_cache = {}
    for mi, mo in enumerate(months):
        aod = clim["AOD_55"][mo]
        doy = date(2026, mi + 1, 21).timetuple().tm_yday
        for lab, aod_x in [("low", 0.5 * aod), ("mean", aod), ("high", 1.5 * aod)]:
            cv = sigma_curves(tab, ring_az, aod_x)
            res = {thr: day_minutes(cv, LAT, LON, UTC, doy, thr) for thr in (2.0, 5.0, 10.0)}
            for gi, gname in enumerate(["zenith", "zenith_ring", "sun_sensor"]):
                rows_out.append({"month": mo, "doy": doy, "aod_case": lab, "aod": aod_x, "geometry": gname,
                                 "min_sun_zen": res[2.0][1], "min_gt2": int(res[2.0][0][gi]),
                                 "min_gt5": int(res[5.0][0][gi]), "min_gt10": int(res[10.0][0][gi])})
    # 21 June with the measured June AOD: the headline window
    cvj = sigma_curves(tab, ring_az, clim["AOD_55"]["JUN"])
    val["june21_minutes_gt10"] = dict(zip(["zenith", "zenith_ring", "sun_sensor"],
                                          map(int, day_minutes(cvj, LAT, LON, UTC, 172, 10.0)[0])))
    import csv
    with open(OUT / "blind_window_abudhabi.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0]))
        w.writeheader()
        w.writerows(rows_out)
    # 6. global map: minutes per day with zenith compass noise above 10 degrees, AOD 0.3
    lats = np.arange(-40, 40.1, 1.0)
    doys = np.arange(1, 366, 2)
    cv3 = sigma_curves(tab, ring_az, 0.3)
    gm = np.zeros((len(lats), len(doys), 3))
    for i, la in enumerate(lats):
        for j, dy in enumerate(doys):
            gm[i, j] = day_minutes(cv3, la, 0.0, 0.0, dy, 10.0)[0]
    np.savez_compressed(OUT / "global_blind_map.npz", lat=lats, doy=doys, minutes=gm, geometries=["zenith", "zenith_ring", "sun_sensor"])
    val["climatology"] = {"url": clim["url"], "accessed": clim["accessed"], "source": clim["source"]}
    (OUT / "validation.json").write_text(json.dumps(val, indent=1))
    print(json.dumps(val, indent=1))


if __name__ == "__main__":
    main()

"""Study 3, SIMULATED: ant style homing and the growth of position error with path length.

A rover drives a correlated random outbound path (0.5 m/s) and integrates wheel odometry distance with a heading
from one of: gyro only; gyro plus zenith compass; gyro plus zenith and ring compass; gyro plus magnetometer (ASSUMED).
The homing error is the position error at checkpoints along the path (100 m to 3 km). Heading uses a two state
(heading, gyro bias) Kalman filter at 1 Hz with the compass gated as B3. Compass truth error: radiative transfer DoP
noise, bias random walk and Gauss Markov tilt error (2 degrees, 20 s). No images are involved.

Output: results/e03/homing.csv and results/e03/homing_fit.json"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from numba import njit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.compass3 import SkyTable, point_sigma, _ring_deriv, tilt_heading_error   # noqa: E402
from vectra.sky import sun_position                                                  # noqa: E402

DEG = np.pi / 180
CHECK = np.array([100, 300, 1000, 3000.0])
SPEED = 0.5


@njit(cache=True)
def run_paths(n_paths, T, sig_true, sig_est, tilt_scale, mode, seed, gyro_bias0, gyro_rw, gyro_noise, scale_sig,
              slip_frac, bias_rw, mag_sig, mag_bias):
    np.random.seed(seed)
    nchk = 4
    out = np.zeros((n_paths, nchk))
    chk = np.array([100.0, 300.0, 1000.0, 3000.0])
    for p in range(n_paths):
        th = np.random.uniform(-np.pi, np.pi)
        x = 0.0; y = 0.0; xe = 0.0; ye = 0.0
        bg = np.random.normal(0, gyro_bias0)
        the = th
        be = 0.0
        P00 = 1e-6; P01 = 0.0; P11 = gyro_bias0 ** 2
        scale = 1 + np.random.normal(0, scale_sig)
        cbias = np.random.normal(0, DEG)
        tilt_r = np.random.normal(0, 2 * DEG); tilt_p = np.random.normal(0, 2 * DEG)
        a = np.exp(-1.0 / 20.0)
        mb = np.random.normal(0, mag_bias)
        dist = 0.0
        ci = 0
        slip = False
        for k in range(T):
            om = np.random.normal(0, 0.03)            # wander of the outbound path (persistence about 1 km)
            th += om
            bg += np.random.normal(0, gyro_rw)
            wm = om + bg + np.random.normal(0, gyro_noise)
            # filter predict
            the += wm - be
            P00 += -2 * P01 + P11 + gyro_noise ** 2
            P01 += -P11
            P11 += gyro_rw ** 2
            # odometry
            if slip:
                slip = np.random.random() > 0.5
            else:
                slip = np.random.random() < slip_frac * 0.5 / (1 - slip_frac)
            d = SPEED
            dm = d * scale * (1.15 if slip else 1.0)
            x += d * np.sin(th); y += d * np.cos(th)
            xe += dm * np.sin(the); ye += dm * np.cos(the)
            dist += d
            # compass
            if mode > 0:
                cbias += np.random.normal(0, bias_rw)
                tilt_r = a * tilt_r + np.random.normal(0, 2 * DEG * np.sqrt(1 - a * a))
                tilt_p = a * tilt_p + np.random.normal(0, 2 * DEG * np.sqrt(1 - a * a))
                if mode == 3:
                    z = th + np.random.normal(0, mag_sig) + mb
                    r = mag_sig ** 2
                    nu = (z - the + np.pi) % (2 * np.pi) - np.pi
                else:
                    terr = tilt_scale[k] * np.sqrt(tilt_r ** 2 + tilt_p ** 2) / (2 * DEG) * np.sign(tilt_r)
                    z = th + np.random.normal(0, sig_true[k]) + cbias + terr
                    r = sig_est[k] ** 2
                    nu = (z - the + np.pi / 2) % np.pi - np.pi / 2
                S = P00 + r
                if nu * nu / S < 6.63:
                    K0 = P00 / S; K1 = P01 / S
                    the += K0 * nu; be += K1 * nu
                    P11 -= K1 * P01; P01 -= K0 * P01; P00 -= K0 * P00
            if ci < nchk and dist >= chk[ci]:
                out[p, ci] = np.hypot(xe - x, ye - y)
                ci += 1
    return out


def sigma_series(table, start, aod, T, geometry):
    t0 = datetime.fromisoformat(start) - timedelta(hours=4)
    zen = np.array([sun_position(24.4539, 54.3773, t0 + timedelta(seconds=float(s)))[0] for s in range(0, T, 30)])
    zen = np.interp(np.arange(T), np.arange(0, T, 30), zen)
    d = table(aod, zen)
    sz = point_sigma(d[:, 0], 0.5 * DEG, 0.05 * DEG)
    if geometry == "ring":
        g = _ring_deriv(np.round(zen, 1), table.ring_el, table.ring_az)
        s = 1 / np.sqrt(1 / sz ** 2 + np.sum(g ** 2 / point_sigma(d[:, 1:], 0.5 * DEG, 0.05 * DEG) ** 2, 1))
    else:
        s = sz
    # tilt error magnitude for a 2 degree tilt at this solar zenith
    tilt = np.abs(tilt_heading_error(zen, 180 + 0 * zen, 0 * zen, 2 * DEG + 0 * zen, 0 * zen))
    return s, tilt, zen


def main():
    table = SkyTable(ROOT / "results" / "e03_sky" / "dop_tables.npz")
    T = int(CHECK[-1] / SPEED) + 10
    rows = []
    for start, label in [("2026-03-21T08:00", "march_morning"), ("2026-06-21T11:00", "june_noon")]:
        for src, mode, geo, aware in [("gyro_only", 0, "zenith", 0), ("zenith", 1, "zenith", 0),
                                      ("zenith_ring", 2, "ring", 0), ("zenith_tilt_aware", 1, "zenith", 1),
                                      ("zenith_ring_tilt_aware", 2, "ring", 1), ("magnetometer", 3, "zenith", 0)]:
            s, tilt, zen = sigma_series(table, start, 0.45, T, geo)
            s_est = np.sqrt(s ** 2 + tilt ** 2) if aware else s      # tilt aware: noise model includes a 2 degree tilt
            err = run_paths(300, T, s, s_est, tilt, mode, 7, 0.002, 1e-4, 0.002, 0.02, 0.1, 0.01 * DEG, 2 * DEG, 3 * DEG)
            for ci, L in enumerate(CHECK):
                rows.append({"scenario": label, "heading": src, "path_m": L, "median_err_m": float(np.median(err[:, ci])),
                             "p90_err_m": float(np.quantile(err[:, ci], 0.9)),
                             "median_err_pct": float(100 * np.median(err[:, ci]) / L)})
    import pandas as pd
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "e03"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "homing.csv", index=False)
    fit = {}
    for (sc, h), g in df.groupby(["scenario", "heading"]):
        b, a = np.polyfit(np.log(g.path_m), np.log(g.median_err_m), 1)
        fit[f"{sc}|{h}"] = {"exponent": float(b), "err_at_10km_m_extrapolated": float(np.exp(a) * 10000 ** b)}
    (out / "homing_fit.json").write_text(json.dumps(fit, indent=1))
    print(df.round(2).to_string())
    print(json.dumps(fit, indent=1))


if __name__ == "__main__":
    main()

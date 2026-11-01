"""Layer 2: sun position and a zenith polarisation compass model for E02.

Sun position follows the NOAA General Solar Position Calculations. The zenith degree of
linear polarisation follows the single scattering Rayleigh model,
    d = d_max * sin^2(gamma) / (1 + cos^2(gamma)),
where gamma is the scattering angle, equal to the solar zenith angle for a zenith view.
The zenith e-vector is perpendicular to the scattering plane, so it is perpendicular to
the solar meridian. The compass therefore measures heading modulo 180 degrees, and the
filter resolves the ambiguity with its prior.

Sensor noise: the angle of polarisation error has a floor and a term that grows as the
degree of polarisation falls, sigma^2 = floor^2 + (c / d)^2. Sky conditions scale d
(aerosol depolarisation) and, for broken cloud, add cloud epochs over the zenith where d
drops and the angle gains an extra error. All sky parameters are assumptions, listed in
configs/e02.yaml.
"""
import numpy as np
from datetime import datetime, timedelta


def sun_position(lat_deg, lon_deg, t_utc):
    """Solar zenith and azimuth (degrees, azimuth clockwise from north) for a UTC datetime."""
    doy = t_utc.timetuple().tm_yday
    hour = t_utc.hour + t_utc.minute / 60 + t_utc.second / 3600 + t_utc.microsecond / 3.6e9
    ndays = 366 if (t_utc.year % 4 == 0 and (t_utc.year % 100 != 0 or t_utc.year % 400 == 0)) else 365
    g = 2 * np.pi / ndays * (doy - 1 + (hour - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                       - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    tst = hour * 60 + eqtime + 4 * lon_deg          # UTC, so the timezone term is zero
    ha = np.radians(tst / 4 - 180)
    lat = np.radians(lat_deg)
    cz = np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(ha)
    zen = np.arccos(np.clip(cz, -1, 1))
    az = np.degrees(np.arctan2(np.sin(ha), np.cos(ha) * np.sin(lat) - np.tan(decl) * np.cos(lat))) + 180.0
    return np.degrees(zen), az % 360.0


def zenith_dop(zen_deg, d_max):
    g = np.radians(zen_deg)
    return d_max * np.sin(g) ** 2 / (1 + np.cos(g) ** 2)


def aop_sigma(d, floor_rad, c_rad):
    return np.sqrt(floor_rad ** 2 + (c_rad / np.maximum(d, 1e-6)) ** 2)


def markov_epochs(n, frac, mean_s, dt, rng):
    if frac <= 0:
        return np.zeros(n, bool)
    p_end = min(1.0, dt / mean_s)
    p_start = p_end * frac / max(1e-9, 1 - frac)
    out = np.zeros(n, bool)
    s = rng.random() < frac
    for k in range(n):
        s = (rng.random() >= p_end) if s else (rng.random() < p_start)
        out[k] = s
    return out


def compass_cue(t_s, yaw_true, scen, skycfg, sensor, rng):
    """Simulate the zenith compass.

    Returns dict with z (heading measurement modulo pi, radians, in [0, pi)),
    d_meas (measured degree of polarisation), sigma_true (true angle noise, rad),
    zen (solar zenith, deg) and valid (bool). Heading is NED yaw, clockwise from north.
    """
    loc = skycfg["location"]
    t0 = datetime.fromisoformat(scen["local_start"]) - timedelta(hours=loc["utc_offset_h"])
    n = len(t_s)
    zen = np.empty(n)
    az = np.empty(n)
    # sun moves slowly: evaluate every 10 s and interpolate
    tg = np.arange(0, t_s[-1] + 10.0, 10.0)
    zg, ag = zip(*[sun_position(loc["lat_deg"], loc["lon_deg"], t0 + timedelta(seconds=float(s))) for s in tg])
    zen[:] = np.interp(t_s, tg, zg)
    az[:] = np.degrees(np.unwrap(np.radians(np.interp(t_s, tg, np.degrees(np.unwrap(np.radians(ag)))))))
    sky = skycfg["conditions"][scen["sky"]]
    d = zenith_dop(zen, sensor["d_max"]) * sky["dop_factor"]
    extra = np.zeros(n)
    dt = float(np.median(np.diff(t_s)))
    cloud = markov_epochs(n, sky.get("cloud_frac", 0.0), sky.get("cloud_mean_s", 30.0), dt, rng)
    if cloud.any():
        d = np.where(cloud, d * rng.uniform(*sky["cloud_dop_scale"], n), d)
        extra = np.where(cloud, np.radians(sky["cloud_aop_extra_deg"]), 0.0)
    floor = np.radians(sensor["floor_deg"])
    c = np.radians(sensor["c_deg"])
    sig = np.sqrt(aop_sigma(d, floor, c) ** 2 + extra ** 2)
    # zenith e-vector is perpendicular to the solar meridian, so heading = sun azimuth + 90 deg - AoP_body
    err = rng.normal(0.0, 1.0, n) * sig
    z = np.mod(yaw_true + err, np.pi)
    d_meas = np.abs(d + rng.normal(0.0, 1.0, n) * sensor["dop_meas_sigma"])
    valid = (zen < 90.0) & (rng.random(n) >= sensor.get("sample_loss", 0.0))
    return {"z": z, "d_meas": d_meas, "d_true": d, "sigma_true": sig, "zen": zen, "az": az % 360, "valid": valid,
            "cloud": cloud}

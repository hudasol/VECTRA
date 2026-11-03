"""Study 3 compass simulator (SIMULATED): radiative transfer DoP, climatology driven aerosol, dust coupled to the
image degradation level, broken cloud, a heading bias with a random walk, platform tilt and two sensor geometries
(zenith point; zenith plus a ring of twelve points at 60 degrees elevation). Also a sun sensor and a magnetometer
(both ASSUMED error models) and simulated wheel odometry.

The filter side noise estimate r_est uses only what a real sensor knows: the measured zenith DoP, the solar zenith
angle from the ephemeris and the frozen Study 2 sensor law. The truth side error contains terms the filter does not
model (multiple scattering DoP, aerosol, bias, tilt, cloud), so the B3 weighting is no longer matched to the simulator.
"""
from datetime import datetime, timedelta

import numpy as np

from vectra.sky import sun_position, markov_epochs

DEG = np.pi / 180


class SkyTable:
    """Interpolates the radiative transfer DoP tables from experiments/E03/sky_v2.py."""

    def __init__(self, path):
        z = np.load(path)
        self.dop, self.zen, self.aod = z["dop"], z["zen"], z["aod"]
        self.ring_az = z["ring_az"]
        self.ring_el = float(z["ring_el"])

    def __call__(self, aod, zen):
        a = np.clip(aod, self.aod[0], self.aod[-1])
        ia = int(np.clip(np.searchsorted(self.aod, a) - 1, 0, len(self.aod) - 2))
        fa = (a - self.aod[ia]) / (self.aod[ia + 1] - self.aod[ia])
        row = (1 - fa) * self.dop[ia] + fa * self.dop[ia + 1]
        return np.stack([np.interp(zen, self.zen, row[:, k]) for k in range(row.shape[1])], -1)


def _ring_deriv(sun_zen_deg, ring_el, ring_az):
    """|d AoP_k / d heading| for the ring points (single scattering plane geometry), shape (n, K)."""
    from vectra.sky_rt import view_dirs, observer_ref
    out = np.zeros((len(sun_zen_deg), len(ring_az)))
    h = 1e-3
    for i, z in enumerate(sun_zen_deg):
        s = view_dirs(90 - z, 180.0)
        vals = []
        for dd in (h, -h):
            v = view_dirs(ring_el, ring_az + np.degrees(dd))
            E = np.cross(s[None, :], v)
            E /= np.linalg.norm(E, axis=-1, keepdims=True) + 1e-15
            e1 = observer_ref(v)
            e2 = np.cross(-v, e1)
            vals.append(np.arctan2(np.sum(E * e2, -1), np.sum(E * e1, -1)))
        out[i] = np.abs(((vals[0] - vals[1]) + np.pi / 2) % np.pi - np.pi / 2) / (2 * h)
    return out


def point_sigma(d, floor, c):
    return np.sqrt(floor ** 2 + (c / np.maximum(d, 1e-6)) ** 2)


def tilt_heading_error(sun_zen, sun_az, yaw, roll, pitch):
    """Exact heading error of a zenith AoP compass that assumes it is level (single scattering plane geometry)."""
    A, e = sun_az * DEG, (90 - sun_zen) * DEG
    s = np.stack([np.sin(A) * np.cos(e), np.cos(A) * np.cos(e), np.sin(e)], -1)
    cy, sy = np.cos(yaw), np.sin(yaw)
    f0 = np.stack([sy, cy, 0 * yaw], -1)
    r0 = np.stack([cy, -sy, 0 * yaw], -1)
    u0 = np.stack([0 * yaw, 0 * yaw, 1 + 0 * yaw], -1)

    def rot(v, axis, ang):
        axis = axis / np.linalg.norm(axis, axis=-1, keepdims=True)
        ca, sa = np.cos(ang)[:, None], np.sin(ang)[:, None]
        return v * ca + np.cross(axis, v) * sa + axis * np.sum(axis * v, -1, keepdims=True) * (1 - ca)
    # pitch about the right axis, then roll about the (pitched) forward axis
    f1, u1 = rot(f0, r0, pitch), rot(u0, r0, pitch)
    r2, u2 = rot(r0, f1, roll), rot(u1, f1, roll)
    E = np.cross(s, u2)
    alpha = np.arctan2(np.sum(E * r2, -1), np.sum(E * f1, -1))
    z = (A + np.pi / 2 - alpha)
    return ((z - yaw) + np.pi / 2) % np.pi - np.pi / 2


def compass_cue3(t_s, yaw_true, scen, table, sensor, rng, roll=None, pitch=None, geometry="zenith"):
    """scen: local_start, aod, cloud (bool), lat, lon, utc. sensor: floor_deg, c_deg, dop_meas_sigma,
    bias_sigma_deg, bias_rw_deg_sqrt_s, tilt_sigma_deg (used when roll and pitch are not given), tilt_tau_s,
    cloud_frac, cloud_mean_s, cloud_dop_scale, cloud_aop_extra_deg."""
    t0 = datetime.fromisoformat(scen["local_start"]) - timedelta(hours=scen["utc"])
    n = len(t_s)
    tg = np.arange(0, t_s[-1] + 10.0, 10.0)
    zg, ag = zip(*[sun_position(scen["lat"], scen["lon"], t0 + timedelta(seconds=float(s))) for s in tg])
    zen = np.interp(t_s, tg, zg)
    az = np.degrees(np.interp(t_s, tg, np.unwrap(np.radians(ag)))) % 360
    floor, c = sensor["floor_deg"] * DEG, sensor["c_deg"] * DEG
    dops = table(scen["aod"], zen)                       # (n, 1 + K)
    dt = float(np.median(np.diff(t_s)))
    cloud = np.zeros(n, bool)
    extra = np.zeros(n)
    att = np.ones(n)
    if scen["cloud"]:
        cloud = markov_epochs(n, sensor["cloud_frac"], sensor["cloud_mean_s"], dt, rng)
        att = np.where(cloud, rng.uniform(*sensor["cloud_dop_scale"], n), 1.0)
        extra = np.where(cloud, sensor["cloud_aop_extra_deg"] * DEG, 0.0)
    d_zen = dops[:, 0] * att
    d_meas = np.abs(d_zen + rng.normal(0, sensor["dop_meas_sigma"], n))
    sig_zen = point_sigma(d_zen, floor, c)
    r_zen_est = point_sigma(d_meas, floor, c) ** 2
    if geometry == "zenith":
        sig = sig_zen
        r_est = r_zen_est
    else:
        g = _ring_deriv(np.round(zen, 1), table.ring_el, table.ring_az)
        ring_d = dops[:, 1:] * att[:, None]
        info = 1 / sig_zen ** 2 + np.sum(g ** 2 / point_sigma(ring_d, floor, c) ** 2, 1)
        sig = 1 / np.sqrt(info)
        scale = d_meas / np.maximum(d_zen, 1e-6)       # the sensor sees the attenuation through its zenith DoP
        info_e = 1 / r_zen_est + np.sum(g ** 2 / point_sigma(dops[:, 1:] * scale[:, None], floor, c) ** 2, 1)
        r_est = 1 / info_e
    sig = np.sqrt(sig ** 2 + extra ** 2)
    bias = rng.normal(0, sensor["bias_sigma_deg"] * DEG) + np.cumsum(
        rng.normal(0, sensor["bias_rw_deg_sqrt_s"] * DEG * np.sqrt(dt), n))
    if roll is None:
        a = np.exp(-dt / sensor["tilt_tau_s"])
        roll = np.zeros(n)
        pitch = np.zeros(n)
        q = sensor["tilt_sigma_deg"] * DEG * np.sqrt(1 - a * a)
        roll[0], pitch[0] = rng.normal(0, sensor["tilt_sigma_deg"] * DEG, 2)
        e = rng.normal(0, q, (n, 2))
        for k in range(1, n):
            roll[k] = a * roll[k - 1] + e[k, 0]
            pitch[k] = a * pitch[k - 1] + e[k, 1]
    tilt_err = tilt_heading_error(zen, az, yaw_true, roll, pitch)
    if geometry != "zenith":
        tilt_err = tilt_err * (sig / np.maximum(sig_zen, 1e-9)) ** 0      # same tilt geometry assumed for the ring
    err = rng.normal(0, 1, n) * sig + bias + tilt_err
    z = np.mod(yaw_true + err, np.pi)
    return {"z": z, "r_est": r_est, "d_meas": d_meas, "d_true": d_zen, "sigma_true": sig, "zen": zen, "az": az,
            "bias": bias, "tilt_err": tilt_err, "cloud": cloud, "valid": zen < 90.0, "err": err}


def sun_sensor_cue(zen, az, yaw_true, sensor, rng):
    """Sun direction sensor (ASSUMED): azimuth error sigma_dir / sin(zenith), plus a constant bias."""
    sig = sensor["sun_sigma_deg"] * DEG / np.maximum(np.sin(zen * DEG), 1e-3)
    err = rng.normal(0, 1, len(zen)) * sig + rng.normal(0, sensor["sun_bias_deg"] * DEG)
    return {"z": yaw_true + err, "r_est": (sensor["sun_sigma_deg"] * DEG / np.maximum(np.sin(zen * DEG), 1e-3)) ** 2,
            "err": err}


def magnetometer_cue(yaw_true, sensor, rng):
    """Magnetometer heading (ASSUMED): white noise plus an uncalibrated hard iron bias and a slow disturbance."""
    n = len(yaw_true)
    err = (rng.normal(0, sensor["mag_sigma_deg"] * DEG, n) + rng.normal(0, sensor["mag_bias_deg"] * DEG)
           + np.cumsum(rng.normal(0, sensor["mag_rw_deg_sqrt_s"] * DEG * np.sqrt(0.2), n)))
    return {"z": yaw_true + err, "r_est": np.full(n, (sensor["mag_sigma_deg"] * DEG) ** 2), "err": err}


def wheel_odometry(x, y, yaw, dt, wo, rng):
    """Simulated wheel odometry body velocity (forward, right) and yaw rate at the frame rate (SIMULATED):
    a scale error, white noise and slip epochs on sand in which the measured speed exceeds the true speed."""
    vx, vy = np.gradient(x, dt), np.gradient(y, dt)
    c, s = np.cos(yaw), np.sin(yaw)
    vf = c * vx + s * vy
    vr = -s * vx + c * vy                     # omnidirectional platforms move sideways as well
    n = len(x)
    slip = markov_epochs(n, wo["slip_frac"], wo["slip_mean_s"], dt, rng)
    scale = 1 + rng.normal(0, wo["scale_sigma"])
    fac = scale * np.where(slip, 1 + wo["slip_excess"], 1.0)
    meas = vf * fac + rng.normal(0, wo["speed_sigma"], n)
    meas_r = vr * fac + rng.normal(0, wo["speed_sigma"], n)
    wrate = np.gradient(np.unwrap(yaw), dt) * (1 + rng.normal(0, wo["yaw_scale_sigma"])) + rng.normal(0, wo["yaw_rate_sigma"], n)
    return meas, meas_r, wrate

"""Layer 2: synthetic sensors derived from truth. Every random draw uses an explicit seed stream."""
import numpy as np

STREAM = {"imu": 1, "visual": 2, "heading": 3}


def rng_for(stream, family_idx, traj_idx, seed, level_idx=0):
    ss = np.random.SeedSequence([STREAM[stream], int(family_idx), int(traj_idx), int(seed), int(level_idx)])
    return np.random.default_rng(ss)


def _markov_mask(rng, n_steps, frac, mean_burst_steps):
    """True where the sensor is DROPPED. Two state chain with stationary dropped fraction `frac`."""
    if frac <= 0:
        return np.zeros(n_steps, dtype=bool)
    p_stay = 1.0 - 1.0 / max(mean_burst_steps, 1.0)
    p_enter = frac / (1.0 - frac) * (1.0 - p_stay)
    p_enter = min(p_enter, 1.0)
    m = np.zeros(n_steps, dtype=bool)
    cur = rng.random() < frac
    u = rng.random(n_steps)
    for i in range(n_steps):
        m[i] = cur
        cur = (u[i] < p_stay) if cur else (u[i] < p_enter)
    return m


def simulate_imu(traj, rng, p):
    dt = traj["dt"]
    n = len(traj["t"])
    bg = rng.normal(0, p["gyro_bias_init_sigma"]) + np.cumsum(np.r_[0, rng.standard_normal(n - 1)]) * p["gyro_bias_rw"] * np.sqrt(dt)
    ba = rng.normal(0, p["accel_bias_init_sigma"]) + np.cumsum(np.r_[0, rng.standard_normal(n - 1)]) * p["accel_bias_rw"] * np.sqrt(dt)
    w_m = traj["omega"] + bg + rng.standard_normal(n) * p["gyro_noise_density"] / np.sqrt(dt)
    a_m = traj["a"] + ba + rng.standard_normal(n) * p["accel_noise_density"] / np.sqrt(dt)
    return {"w_m": w_m, "a_m": a_m, "bg_true": bg, "ba_true": ba}


def simulate_visual(traj, rng, vis, level, timing):
    """Visual front end abstracted at the measurement level: forward speed and yaw rate at the visual rate."""
    dt = traj["dt"]
    n = len(traj["t"])
    step = int(round(1.0 / (timing["visual_rate_hz"] * dt)))
    idx = np.arange(0, n, step)
    m = level["noise_mult"]
    drop = _markov_mask(rng, len(idx), level["dropout_frac"], vis["dropout_mean_burst_s"] * timing["visual_rate_hz"])
    scale = 1.0 + rng.normal(0, vis["scale_error_sigma"])
    v_meas = traj["v"][idx] * scale + rng.standard_normal(len(idx)) * vis["speed_sigma"] * m
    w_meas = traj["omega"][idx] + rng.standard_normal(len(idx)) * vis["yawrate_sigma"] * m
    out = rng.random(len(idx)) < level["outlier_prob"]
    v_meas = v_meas + out * rng.choice([-1.0, 1.0], len(idx)) * vis["outlier_speed_error"]
    w_meas = w_meas + out * rng.standard_normal(len(idx)) * 10 * vis["yawrate_sigma"]
    valid = np.zeros(n, dtype=bool)
    vv = np.zeros(n)
    ww = np.zeros(n)
    valid[idx] = ~drop
    vv[idx] = v_meas
    ww[idx] = w_meas
    return {"valid": valid, "v": vv, "w": ww}


def simulate_heading(traj, rng, h, timing_dt_unused=None):
    """Synthetic heading cue from ground truth yaw: white noise, bias, bias random walk, dropout, contamination."""
    dt = traj["dt"]
    n = len(traj["t"])
    step = int(round(1.0 / (h["rate_hz"] * dt)))
    idx = np.arange(0, n, step)
    k = len(idx)
    dts = step * dt
    drop = _markov_mask(rng, k, h["dropout_frac"], h["dropout_mean_burst_s"] * h["rate_hz"])
    b0 = np.deg2rad(rng.normal(0, h["bias_init_sigma_deg"]))
    brw = np.cumsum(np.r_[0, rng.standard_normal(k - 1)]) * np.deg2rad(h["bias_rw_deg_per_sqrt_s"]) * np.sqrt(dts)
    noise = rng.standard_normal(k) * np.deg2rad(h["noise_sigma_deg"])
    contam = np.zeros(k)
    t = 0
    lam = h["contamination_start_rate_per_s"]
    while t < k:
        if rng.random() < lam * dts:
            dur = int(rng.uniform(*h["contamination_duration_s"]) * h["rate_hz"])
            off = np.deg2rad(rng.uniform(*h["contamination_offset_deg"])) * rng.choice([-1.0, 1.0])
            contam[t:t + dur] = off
            t += dur
        t += 1
    z = np.zeros(n)
    valid = np.zeros(n, dtype=bool)
    reliable = np.ones(n, dtype=bool)
    z[idx] = traj["theta"][idx] + b0 + brw + noise + contam
    valid[idx] = ~drop
    reliable[idx] = contam == 0
    return {"valid": valid, "z": z, "reliable": reliable}

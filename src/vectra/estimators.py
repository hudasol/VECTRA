"""Layer 3: planar EKF with state [x, y, theta, v, bias_gyro, bias_accel].
Modes: 0 = B0 (no heading), 1 = B1 (heading, fixed noise), 2 = B2 (heading, adaptive noise), 3 = B1g (heading, fixed noise, chi2 gate).
All modes share the same code path except the heading update."""
import numpy as np
from numba import njit


@njit(cache=True)
def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


@njit(cache=True)
def _ekf(mode, dt, w_m, a_m, vis_valid, vis_v, vis_w, head_valid, head_z,
         qg, qa, qbg, qba, rv, rw, vis_gate, h_sigma, h_gate, window, p0diag, x0):
    n = w_m.shape[0]
    x = x0.copy()
    P = np.zeros((6, 6))
    for i in range(6):
        P[i, i] = p0diag[i]
    out_x = np.zeros((n, 6))
    out_P = np.zeros((n, 4))      # Pxx, Pxy, Pyy, Ptt
    hist_nu2 = np.zeros(window)
    hist_hph = np.zeros(window)
    hcount = 0
    n_h_used = 0
    n_h_gated = 0
    Rh_nom = h_sigma * h_sigma
    I6 = np.eye(6)
    for k in range(n):
        if k > 0:
            th = x[2]
            w = w_m[k - 1] - x[4]
            a = a_m[k - 1] - x[5]
            thn = th + w * dt
            thm = th + 0.5 * w * dt
            vm = x[3] + 0.5 * a * dt
            F = np.eye(6)
            F[0, 2] = -vm * np.sin(thm) * dt
            F[0, 3] = np.cos(thm) * dt
            F[0, 4] = 0.5 * vm * np.sin(thm) * dt * dt
            F[0, 5] = -0.5 * np.cos(thm) * dt * dt
            F[1, 2] = vm * np.cos(thm) * dt
            F[1, 3] = np.sin(thm) * dt
            F[1, 4] = -0.5 * vm * np.cos(thm) * dt * dt
            F[1, 5] = -0.5 * np.sin(thm) * dt * dt
            F[2, 4] = -dt
            F[3, 5] = -dt
            x[0] += vm * np.cos(thm) * dt
            x[1] += vm * np.sin(thm) * dt
            x[2] = thn
            x[3] += a * dt
            Q = np.zeros((6, 6))
            Q[2, 2] = qg * qg * dt
            Q[3, 3] = qa * qa * dt
            Q[4, 4] = qbg * qbg * dt
            Q[5, 5] = qba * qba * dt
            Q[0, 0] = 1e-8 * dt
            Q[1, 1] = 1e-8 * dt
            P = F @ P @ F.T + Q
        # visual update: z = [v_vis, w_m - w_vis] ; h = [v, bias_gyro]
        if vis_valid[k]:
            z = np.array([vis_v[k], w_m[k] - vis_w[k]])
            H = np.zeros((2, 6))
            H[0, 3] = 1.0
            H[1, 4] = 1.0
            R = np.diag(np.array([rv, rw + qg * qg / dt]))
            nu = z - np.array([x[3], x[4]])
            S = H @ P @ H.T + R
            Si = np.linalg.inv(S)
            if nu @ Si @ nu < vis_gate:
                K = P @ H.T @ Si
                x = x + K @ nu
                IKH = I6 - K @ H
                P = IKH @ P @ IKH.T + K @ R @ K.T
        # heading update
        if mode > 0 and head_valid[k]:
            nu_h = _wrap(head_z[k] - x[2])
            hph = P[2, 2]
            Rh = Rh_nom
            if mode == 2:
                hist_nu2[hcount % window] = nu_h * nu_h
                hist_hph[hcount % window] = hph
                hcount += 1
                m = min(hcount, window)
                cov = np.mean(hist_nu2[:m]) - np.mean(hist_hph[:m])
                if cov > Rh_nom:
                    Rh = cov
            S_h = hph + Rh
            use = True
            if mode == 3 and nu_h * nu_h / S_h > h_gate:
                use = False
            if use:
                K = P[:, 2] / S_h
                x = x + K * nu_h
                x[2] = _wrap(x[2])
                IKH = I6.copy()
                IKH[:, 2] -= K
                P = IKH @ P @ IKH.T + np.outer(K, K) * Rh
                n_h_used += 1
            else:
                n_h_gated += 1
        out_x[k] = x
        out_P[k, 0] = P[0, 0]
        out_P[k, 1] = P[0, 1]
        out_P[k, 2] = P[1, 1]
        out_P[k, 3] = P[2, 2]
    return out_x, out_P, n_h_used, n_h_gated


MODES = {"B0": 0, "B1": 1, "B2": 2, "B1g": 3}


def run_estimator(name, traj, imu, vis, head, cfg):
    f = cfg["filter"]
    im = cfg["imu"]
    v = cfg["visual"]
    dt = traj["dt"]
    p0 = np.array([1e-4, 1e-4, 1e-6, 0.05 ** 2, im["gyro_bias_init_sigma"] ** 2, im["accel_bias_init_sigma"] ** 2])
    x0 = np.array([traj["x"][0], traj["y"][0], traj["theta"][0], traj["v"][0], 0.0, 0.0])
    hv = head["valid"] if name != "B0" else np.zeros_like(head["valid"])
    ox, oP, nu, ng = _ekf(MODES[name], dt, imu["w_m"], imu["a_m"], vis["valid"], vis["v"], vis["w"], hv, head["z"],
                          im["gyro_noise_density"], im["accel_noise_density"], im["gyro_bias_rw"], im["accel_bias_rw"],
                          v["speed_sigma"] ** 2, v["yawrate_sigma"] ** 2, v["gate_chi2_2dof"],
                          np.deg2rad(f["heading_nominal_sigma_deg"]), f["heading_gate_chi2_1dof"],
                          int(f["b2_window"]), p0, x0)
    return {"x": ox[:, 0], "y": ox[:, 1], "theta": ox[:, 2], "v": ox[:, 3], "Pxx": oP[:, 0], "Pxy": oP[:, 1],
            "Pyy": oP[:, 2], "Ptt": oP[:, 3], "h_used": int(nu), "h_gated": int(ng)}

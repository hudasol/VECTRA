"""Layer 3: planar loosely coupled filter for E02.

State [x, y, theta, vx, vy, bg, bax, bay]: world position, yaw (NED, clockwise from
north), world velocity, gyro bias and the two horizontal accelerometer biases.
IMU at 100 Hz drives the prediction. Stereo visual odometry at 10 Hz measures the body
velocity (forward, right) and the yaw rate, which observes the gyro bias. The zenith
compass at 5 Hz measures yaw modulo pi. A visual update whose NIS exceeds the gate is
not rejected; its noise is inflated so that the NIS equals the gate (bounded influence).

Heading modes: 0 B0 no cue, 1 B1 fixed noise, 2 B2 covariance matching, 3 B1g fixed noise
with a chi square gate, 4 B3 noise from the measured degree of polarisation with a gate,
5 B3a which is B3 plus a visual noise scale adapted from the visual NIS, 6 B4 (exploratory,
added after the held out run) which uses the DoP based noise as the floor of covariance
matching with no gate.
"""
import numpy as np
from numba import njit

NX = 8


@njit(cache=True)
def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


@njit(cache=True)
def _wrap_half(a):
    return (a + 0.5 * np.pi) % np.pi - 0.5 * np.pi


@njit(cache=True)
def run_filter(mode, dt, gyro, acc, vo_idx, vo_ok, vo_vf, vo_vr, vo_w, cue_idx, cue_ok, cue_z, cue_d,
               x0, p0, qg, qa, qbg, qba, rvo, vo_gate, h_sigma, h_gate, w_b2, c_rad, floor_rad, w_vo):
    n = gyro.shape[0]
    x = x0.copy()
    P = np.diag(p0)
    I = np.eye(NX)
    nf = vo_idx.shape[0]
    out = np.zeros((nf, 6))       # x, y, theta, Pxx, Pyy, Ptt (Pxy dropped below)
    outxy = np.zeros(nf)
    vi = 0
    ci = 0
    h_nu2 = np.zeros(w_b2)
    h_hph = np.zeros(w_b2)
    hc = 0
    nis_hist = np.zeros(w_vo)
    nc = 0
    vo_scale = 1.0
    n_used = 0
    n_gated = 0
    gsum = 0.0
    gcount = 0
    Rh0 = h_sigma * h_sigma
    for k in range(n):
        # prediction with IMU sample k
        th = x[2]
        w = gyro[k] - x[5]
        ab0 = acc[k, 0] - x[6]
        ab1 = acc[k, 1] - x[7]
        c = np.cos(th)
        s = np.sin(th)
        ax = c * ab0 - s * ab1
        ay = s * ab0 + c * ab1
        F = np.eye(NX)
        F[0, 3] = dt
        F[1, 4] = dt
        F[2, 5] = -dt
        F[3, 2] = (-s * ab0 - c * ab1) * dt
        F[4, 2] = (c * ab0 - s * ab1) * dt
        F[3, 6] = -c * dt
        F[3, 7] = s * dt
        F[4, 6] = -s * dt
        F[4, 7] = -c * dt
        x[0] += x[3] * dt + 0.5 * ax * dt * dt
        x[1] += x[4] * dt + 0.5 * ay * dt * dt
        x[3] += ax * dt
        x[4] += ay * dt
        x[2] = _wrap(th + w * dt)
        Q = np.zeros((NX, NX))
        Q[2, 2] = qg * qg * dt
        Q[3, 3] = qa * qa * dt
        Q[4, 4] = qa * qa * dt
        Q[5, 5] = qbg * qbg * dt
        Q[6, 6] = qba * qba * dt
        Q[7, 7] = qba * qba * dt
        P = F @ P @ F.T + Q
        gsum += gyro[k]
        gcount += 1
        # visual update at frame boundaries
        if vi < nf and vo_idx[vi] == k:
            if vo_ok[vi]:
                th = x[2]
                c = np.cos(th)
                s = np.sin(th)
                hv0 = c * x[3] + s * x[4]
                hv1 = -s * x[3] + c * x[4]
                gm = gsum / max(gcount, 1)
                z = np.array([vo_vf[vi], vo_vr[vi], gm - vo_w[vi]])
                hz = np.array([hv0, hv1, x[5]])
                H = np.zeros((3, NX))
                H[0, 2] = -s * x[3] + c * x[4]
                H[0, 3] = c
                H[0, 4] = s
                H[1, 2] = -c * x[3] - s * x[4]
                H[1, 3] = -s
                H[1, 4] = c
                H[2, 5] = 1.0
                R = np.diag(rvo) * vo_scale
                nu = z - hz
                S = H @ P @ H.T + R
                Si = np.linalg.inv(S)
                nis = nu @ Si @ nu
                if mode == 5:
                    nis_hist[nc % w_vo] = nis / vo_scale
                    nc += 1
                    m = min(nc, w_vo)
                    vo_scale = max(1.0, np.mean(nis_hist[:m]) / 3.0)
                if nis > vo_gate:
                    # robust update: inflate the visual noise so the normalised innovation sits on the gate,
                    # which bounds the influence of an outlier without locking the filter out
                    R = R * (nis / vo_gate)
                    S = H @ P @ H.T + R
                    Si = np.linalg.inv(S)
                K = P @ H.T @ Si
                x = x + K @ nu
                x[2] = _wrap(x[2])
                IKH = I - K @ H
                P = IKH @ P @ IKH.T + K @ R @ K.T
            gsum = 0.0
            gcount = 0
            out[vi, 0] = x[0]
            out[vi, 1] = x[1]
            out[vi, 2] = x[2]
            out[vi, 3] = P[0, 0]
            out[vi, 4] = P[1, 1]
            out[vi, 5] = P[2, 2]
            outxy[vi] = P[0, 1]
            vi += 1
        # compass update
        if mode > 0 and ci < cue_idx.shape[0] and cue_idx[ci] == k:
            if cue_ok[ci]:
                nu_h = _wrap_half(cue_z[ci] - x[2])
                hph = P[2, 2]
                Rh = Rh0
                if mode == 2:
                    h_nu2[hc % w_b2] = nu_h * nu_h
                    h_hph[hc % w_b2] = hph
                    hc += 1
                    m = min(hc, w_b2)
                    cv = np.mean(h_nu2[:m]) - np.mean(h_hph[:m])
                    if cv > Rh0:
                        Rh = cv
                elif mode == 4 or mode == 5:
                    dm = max(cue_d[ci], 1e-6)
                    Rh = floor_rad * floor_rad + (c_rad / dm) ** 2
                elif mode == 6:
                    # exploratory B4: DoP based noise as the floor of covariance matching, no gate
                    dm = max(cue_d[ci], 1e-6)
                    Rd = floor_rad * floor_rad + (c_rad / dm) ** 2
                    h_nu2[hc % w_b2] = nu_h * nu_h
                    h_hph[hc % w_b2] = hph
                    hc += 1
                    m = min(hc, w_b2)
                    cv = np.mean(h_nu2[:m]) - np.mean(h_hph[:m])
                    Rh = max(Rd, cv)
                Sh = hph + Rh
                use = True
                if (mode == 3 or mode == 4 or mode == 5) and nu_h * nu_h / Sh > h_gate:
                    use = False
                if use:
                    K = P[:, 2] / Sh
                    x = x + K * nu_h
                    x[2] = _wrap(x[2])
                    IKH = I.copy()
                    IKH[:, 2] -= K
                    P = IKH @ P @ IKH.T + np.outer(K, K) * Rh
                    n_used += 1
                else:
                    n_gated += 1
            ci += 1
    return out, outxy, n_used, n_gated

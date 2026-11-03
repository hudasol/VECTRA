"""Study 3 planar filter: the Study 2 filter (filter2.py, unchanged) extended with a compass bias state, a
coloured (Gauss Markov) visual speed scale state, robust and two mode compass weighting, a learned reliability
input and a gate lock out rule.

State [x, y, theta, vx, vy, bg, bax, bay, bh, sv]: as in Study 2 plus the compass heading bias bh (rad) and the
visual forward speed scale error sv. States that a mode does not use have zero initial variance and zero process
noise, so they stay at zero and the mode reduces exactly to its Study 2 form.

Compass modes (h_mode):
 0 none (B0); 1 fixed noise (B1); 2 covariance matching (B2); 3 fixed noise with gate (B1g);
 4 per sample noise r_est with gate (B3); 6 r_est as floor of covariance matching, no gate (B4);
 7 two mode moment matched IMM approximation, good mode r_est, bad mode r_bad (B5);
 8 Huber weighting of the r_est innovation (B6); 9 B3 with the bias state (B7);
 10 learned reliability p_bad per sample: r_est / (1 - p_bad), reject if p_bad > 0.9 (B8).
lockout > 0: after that many consecutive gated samples the next sample is used with its noise inflated so that its
normalised innovation sits on the gate (bounded influence, as for the visual update).
"""
import numpy as np
from numba import njit

NX = 10


@njit(cache=True)
def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


@njit(cache=True)
def _wrap_half(a):
    return (a + 0.5 * np.pi) % np.pi - 0.5 * np.pi


@njit(cache=True)
def run_filter3(h_mode, dt, gyro, acc, vo_idx, vo_ok, vo_vf, vo_vr, vo_w, cue_idx, cue_ok, cue_z, cue_r, cue_p,
                x0, p0, qg, qa, qbg, qba, qbh, sv_sigma, sv_tau, rvo, rgm_extra, vo_gate, h_sigma, h_gate, w_b2,
                r_bad, prior_bad, huber_k, lockout):
    n = gyro.shape[0]
    x = x0.copy()
    P = np.diag(p0)
    I = np.eye(NX)
    nf = vo_idx.shape[0]
    out = np.zeros((nf, 7))
    vi = 0
    ci = 0
    h_nu2 = np.zeros(w_b2)
    h_hph = np.zeros(w_b2)
    hc = 0
    n_used = 0
    n_gated = 0
    run_gated = 0
    max_run_gated = 0
    gsum = 0.0
    gcount = 0
    Rh0 = h_sigma * h_sigma
    p_bad = prior_bad
    phi_sv = np.exp(-dt / sv_tau) if sv_tau > 0 else 1.0
    for k in range(n):
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
        F[9, 9] = phi_sv
        x[0] += x[3] * dt + 0.5 * ax * dt * dt
        x[1] += x[4] * dt + 0.5 * ay * dt * dt
        x[3] += ax * dt
        x[4] += ay * dt
        x[2] = _wrap(th + w * dt)
        x[9] *= phi_sv
        Q = np.zeros((NX, NX))
        Q[2, 2] = qg * qg * dt
        Q[3, 3] = qa * qa * dt
        Q[4, 4] = qa * qa * dt
        Q[5, 5] = qbg * qbg * dt
        Q[6, 6] = qba * qba * dt
        Q[7, 7] = qba * qba * dt
        Q[8, 8] = qbh * qbh * dt
        Q[9, 9] = sv_sigma * sv_sigma * (1 - phi_sv * phi_sv)
        P = F @ P @ F.T + Q
        gsum += gyro[k]
        gcount += 1
        if vi < nf and vo_idx[vi] == k:
            if vo_ok[vi]:
                th = x[2]
                c = np.cos(th)
                s = np.sin(th)
                hv0 = c * x[3] + s * x[4]
                hv1 = -s * x[3] + c * x[4]
                gm = gsum / max(gcount, 1)
                z = np.array([vo_vf[vi], vo_vr[vi], gm - vo_w[vi]])
                hz = np.array([hv0 * (1 + x[9]), hv1, x[5]])
                H = np.zeros((3, NX))
                H[0, 2] = (-s * x[3] + c * x[4]) * (1 + x[9])
                H[0, 3] = c * (1 + x[9])
                H[0, 4] = s * (1 + x[9])
                H[0, 9] = hv0
                H[1, 2] = -c * x[3] - s * x[4]
                H[1, 3] = -s
                H[1, 4] = c
                H[2, 5] = 1.0
                R = np.diag(rvo)
                R[2, 2] += rgm_extra
                nu = z - hz
                S = H @ P @ H.T + R
                Si = np.linalg.inv(S)
                nis = nu @ Si @ nu
                if nis > vo_gate:
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
            out[vi, 6] = P[0, 1]
            vi += 1
        if h_mode > 0 and ci < cue_idx.shape[0] and cue_idx[ci] == k:
            if cue_ok[ci]:
                hb = x[8] if h_mode == 9 else 0.0
                nu_h = _wrap_half(cue_z[ci] - x[2] - hb)
                hph = P[2, 2]
                if h_mode == 9:
                    hph = P[2, 2] + 2 * P[2, 8] + P[8, 8]
                Rh = Rh0
                gate_on = h_mode == 3 or h_mode == 4 or h_mode == 9 or h_mode == 10
                if h_mode == 2:
                    h_nu2[hc % w_b2] = nu_h * nu_h
                    h_hph[hc % w_b2] = hph
                    hc += 1
                    m = min(hc, w_b2)
                    cv = np.mean(h_nu2[:m]) - np.mean(h_hph[:m])
                    if cv > Rh0:
                        Rh = cv
                elif h_mode == 4 or h_mode == 9:
                    Rh = cue_r[ci]
                elif h_mode == 6:
                    h_nu2[hc % w_b2] = nu_h * nu_h
                    h_hph[hc % w_b2] = hph
                    hc += 1
                    m = min(hc, w_b2)
                    cv = np.mean(h_nu2[:m]) - np.mean(h_hph[:m])
                    Rh = max(cue_r[ci], cv)
                elif h_mode == 7:
                    # two mode: Markov prior on the bad mode, Bayes update from the innovation likelihoods
                    pb = 0.95 * p_bad + 0.05 * (1 - p_bad) * prior_bad / max(1 - prior_bad, 1e-9)
                    pb = min(max(pb, 1e-4), 1 - 1e-4)
                    sg = hph + cue_r[ci]
                    sb = hph + r_bad
                    lg = np.exp(-0.5 * nu_h * nu_h / sg) / np.sqrt(sg)
                    lb = np.exp(-0.5 * nu_h * nu_h / sb) / np.sqrt(sb)
                    p_bad = pb * lb / (pb * lb + (1 - pb) * lg + 1e-300)
                    # moment matched single update: effective noise from the mode mixture
                    Rh = cue_r[ci] / max(1 - p_bad, 1e-3)
                elif h_mode == 8:
                    Rh = cue_r[ci]
                    r = abs(nu_h) / np.sqrt(hph + Rh)
                    if r > huber_k:
                        Rh = (hph + Rh) * r / huber_k - hph
                elif h_mode == 10:
                    Rh = cue_r[ci] / max(1 - cue_p[ci], 0.05)
                Sh = hph + Rh
                use = True
                if gate_on and nu_h * nu_h / Sh > h_gate:
                    use = False
                if h_mode == 10 and cue_p[ci] > 0.9:
                    use = False
                if (not use) and lockout > 0 and run_gated >= lockout:
                    Rh = Rh * (nu_h * nu_h / Sh) / h_gate
                    Sh = hph + Rh
                    use = True
                if use:
                    Hh = np.zeros(NX)
                    Hh[2] = 1.0
                    if h_mode == 9:
                        Hh[8] = 1.0
                    PH = P @ Hh
                    Sh = Hh @ PH + Rh
                    K = PH / Sh
                    x = x + K * nu_h
                    x[2] = _wrap(x[2])
                    IKH = I - np.outer(K, Hh)
                    P = IKH @ P @ IKH.T + np.outer(K, K) * Rh
                    n_used += 1
                    run_gated = 0
                else:
                    n_gated += 1
                    run_gated += 1
                    if run_gated > max_run_gated:
                        max_run_gated = run_gated
            ci += 1
    return out, n_used, n_gated, max_run_gated

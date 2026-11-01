"""Layer 4: metrics and statistics. Depends only on arrays, never on estimators or sensors."""
import numpy as np
from scipy import stats


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def _align_se2(est_xy, gt_xy):
    mu_e, mu_g = est_xy.mean(0), gt_xy.mean(0)
    E, G = est_xy - mu_e, gt_xy - mu_g
    H = E.T @ G
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, d])
    R = Vt.T @ D @ U.T
    return (R @ E.T).T + mu_g


def run_metrics(traj, est, fail_pct=10.0, nees_stride=20):
    gt = np.c_[traj["x"], traj["y"]]
    es = np.c_[est["x"], est["y"]]
    err = es - gt
    pe = np.linalg.norm(err, axis=1)
    L = traj["path_length"]
    drift = 100.0 * pe[-1] / L
    rmse = float(np.sqrt(np.mean(pe ** 2)))
    ate_al = float(np.sqrt(np.mean(np.sum((_align_se2(es, gt) - gt) ** 2, axis=1))))
    dt = traj["dt"]
    w = int(round(10.0 / dt))
    rel_e = (es[w:] - es[:-w]) - (gt[w:] - gt[:-w])
    rpe = float(np.sqrt(np.mean(np.sum(rel_e ** 2, axis=1))))
    he = _wrap(est["theta"] - traj["theta"])
    idx = np.arange(0, len(pe), nees_stride)
    nees = np.empty(len(idx))
    for j, k in enumerate(idx):
        P = np.array([[est["Pxx"][k], est["Pxy"][k]], [est["Pxy"][k], est["Pyy"][k]]])
        e = err[k]
        try:
            nees[j] = e @ np.linalg.solve(P, e)
        except np.linalg.LinAlgError:
            nees[j] = np.inf
    nees_h = (he[idx] ** 2) / np.maximum(est["Ptt"][idx], 1e-12)
    return {"drift_pct": float(drift), "pos_rmse": rmse, "ate_se2": ate_al, "rpe10": rpe,
            "head_rmse_deg": float(np.rad2deg(np.sqrt(np.mean(he ** 2)))), "head_final_deg": float(np.rad2deg(abs(he[-1]))),
            "nees_pos_mean": float(np.mean(nees[1:])), "cover95_pos": float(np.mean(nees[1:] < 5.991)),
            "nees_head_mean": float(np.mean(nees_h[1:])), "failure": bool(drift > fail_pct),
            "path_length": float(L), "h_used": est["h_used"], "h_gated": est["h_gated"]}


def bootstrap_ci_median(x, n_boot=10000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    b = np.median(x[rng.integers(0, len(x), (n_boot, len(x)))], axis=1)
    return float(np.quantile(b, alpha / 2)), float(np.quantile(b, 1 - alpha / 2))


def paired_wilcoxon(a, b):
    d = np.asarray(a) - np.asarray(b)
    if np.allclose(d, 0):
        return 1.0
    return float(stats.wilcoxon(d, zero_method="wilcox", alternative="two-sided").pvalue)


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj


def cliffs_delta_paired(a, b):
    d = np.asarray(a) - np.asarray(b)
    return float((np.sum(d > 0) - np.sum(d < 0)) / len(d))

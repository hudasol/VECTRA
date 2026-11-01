"""Layer 1: planar ground truth trajectories for a wheeled rover. Deterministic given (family, index)."""
import numpy as np

FAMILIES = ["straight", "meander", "loops", "stopgo", "slalom", "mixed"]


def _ou(rng, n, dt, sigma, tau):
    x = np.zeros(n)
    a = np.exp(-dt / tau)
    s = sigma * np.sqrt(1 - a * a)
    for k in range(1, n):
        x[k] = a * x[k - 1] + s * rng.standard_normal()
    return x


def _speed_profile(rng, n, dt, stopgo):
    t = np.arange(n) * dt
    v0 = rng.uniform(0.8, 1.4)
    if not stopgo:
        return v0 * (1 + 0.15 * np.sin(2 * np.pi * t / rng.uniform(30, 60) + rng.uniform(0, 6.28)))
    target = np.zeros(n)
    k = 0
    go = True
    while k < n:
        L = int(rng.uniform(10, 25) / dt) if go else int(rng.uniform(3, 8) / dt)
        target[k:k + L] = v0 if go else 0.0
        k += L
        go = not go
    v = np.zeros(n)
    amax = 0.5 * dt
    for i in range(1, n):
        v[i] = v[i - 1] + np.clip(target[i] - v[i - 1], -amax, amax)
    return v


def _curvature(rng, family, n, dt):
    t = np.arange(n) * dt
    if family == "straight":
        return _ou(rng, n, dt, 0.01, 20.0)
    if family in ("meander", "stopgo"):
        return _ou(rng, n, dt, 0.06 if family == "meander" else 0.04, 10.0)
    if family == "loops":
        k = np.zeros(n)
        i, sign = 0, 1.0
        while i < n:
            L = int(rng.uniform(20, 40) / dt)
            R = rng.uniform(8, 15)
            k[i:i + L] = sign / R
            i += L
            sign = -sign
        kern = np.ones(int(2.0 / dt)) / int(2.0 / dt)
        return np.convolve(k, kern, mode="same")
    if family == "slalom":
        A = rng.uniform(0.08, 0.15)
        P = rng.uniform(25, 40)
        return A * np.sin(2 * np.pi * t / P + rng.uniform(0, 6.28))
    if family == "mixed":
        k = np.zeros(n)
        i = 0
        while i < n:
            L = int(40 / dt)
            choice = rng.integers(0, 3)
            seg = min(L, n - i)
            if choice == 0:
                k[i:i + seg] = _ou(rng, seg, dt, 0.01, 20.0)
            elif choice == 1:
                k[i:i + seg] = _ou(rng, seg, dt, 0.08, 8.0)
            else:
                k[i:i + seg] = rng.choice([-1, 1]) / rng.uniform(8, 20)
            i += seg
        return k
    raise ValueError(family)


def make_trajectory(family, index, duration_s=200.0, dt=0.05):
    """Return dict of truth arrays. Start pose is the origin with heading zero."""
    if family not in FAMILIES:
        raise ValueError(family)
    rng = np.random.default_rng(np.random.SeedSequence([1000 + FAMILIES.index(family), int(index)]))
    n = int(round(duration_s / dt)) + 1
    v = _speed_profile(rng, n, dt, family == "stopgo")
    kappa = _curvature(rng, family, n, dt)
    w = v * kappa
    th = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)
    for i in range(1, n):
        th[i] = th[i - 1] + 0.5 * (w[i - 1] + w[i]) * dt
        thm = 0.5 * (th[i - 1] + th[i])
        vm = 0.5 * (v[i - 1] + v[i])
        x[i] = x[i - 1] + vm * np.cos(thm) * dt
        y[i] = y[i - 1] + vm * np.sin(thm) * dt
    a = np.gradient(v, dt)
    return {"t": np.arange(n) * dt, "dt": dt, "x": x, "y": y, "theta": th, "v": v, "omega": w, "a": a,
            "path_length": float(np.sum(0.5 * (v[1:] + v[:-1]) * dt)), "family": family, "index": int(index)}

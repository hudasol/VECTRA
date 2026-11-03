"""Sky model v2 (Study 3): vector Monte Carlo radiative transfer for skylight polarisation.

Plane parallel, horizontally homogeneous atmosphere with Rayleigh molecules and one aerosol type, a Lambertian
(depolarising) ground and full multiple scattering. Stokes vectors (I, Q, U) are carried with explicit reference
vectors and rotated at every scattering event. Radiance toward a set of upward viewing directions is estimated with
the local estimate (peel off) method. Everything here is SIMULATED.

Assumptions (labelled in the paper):
- Rayleigh phase matrix with depolarisation ignored.
- Aerosol: Henyey Greenstein intensity phase function with asymmetry g and single scattering albedo w, and a
  Rayleigh shaped linear polarisation of maximum p_a (P12 = -p_a sin^2/(1+cos^2) P11). This is a simplified matrix,
  not a Mie computation; p_a and g are varied in the sensitivity runs.
- Aerosol and molecules are well mixed in one layer (vertical profile does not change the zenith pattern much for
  a ground observer, but it is an assumption).
Circular polarisation (V) is neglected; it is below 1 percent for skylight.
"""
import numpy as np


def _norm(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def _perp_ref(d):
    """A reference unit vector perpendicular to each direction d."""
    a = np.where(np.abs(d[:, 2:3]) < 0.9, np.array([[0.0, 0.0, 1.0]]), np.array([[1.0, 0.0, 0.0]]))
    return _norm(np.cross(np.cross(d, a), d))


def _rotate(Q, U, e_old, e_new, d):
    """Rotate linear Stokes components from reference e_old to e_new (both perpendicular to d)."""
    e2 = np.cross(d, e_old)
    c = np.sum(e_new * e_old, -1)
    s = np.sum(e_new * e2, -1)
    phi2 = 2 * np.arctan2(s, c)
    c2, s2 = np.cos(phi2), np.sin(phi2)
    return Q * c2 + U * s2, -Q * s2 + U * c2


def _phase(cos_t, f_r, g, p_a):
    """Mixture phase matrix elements (P11 normalised over the sphere, ratios P12/P11 and P33/P11)."""
    pr = 3.0 / (16 * np.pi) * (1 + cos_t ** 2)
    ph = (1 - g * g) / (4 * np.pi * (1 + g * g - 2 * g * cos_t) ** 1.5)
    ray12 = -(1 - cos_t ** 2) / (1 + cos_t ** 2)
    ray33 = 2 * cos_t / (1 + cos_t ** 2)
    p11 = f_r * pr + (1 - f_r) * ph
    p12 = f_r * pr * ray12 + (1 - f_r) * ph * p_a * ray12
    p33 = (f_r * pr + (1 - f_r) * ph) * ray33
    return p11, p12, p33


def _scatter_stokes(I, Q, U, e_in, d_in, d_out, f_r, g, p_a):
    """Apply the mixture phase matrix for scattering d_in -> d_out. Returns (I,Q,U) and the outgoing reference."""
    n = np.cross(d_in, d_out)
    nn = np.linalg.norm(n, axis=-1, keepdims=True)
    bad = nn[:, 0] < 1e-9
    n = np.where(bad[:, None], np.cross(d_in, _perp_ref(d_in)), n)
    n = _norm(n)
    e_par_in = np.cross(n, d_in)
    e_par_out = np.cross(n, d_out)
    Qs, Us = _rotate(Q, U, e_in, e_par_in, d_in)
    ct = np.clip(np.sum(d_in * d_out, -1), -1, 1)
    p11, p12, p33 = _phase(ct, f_r, g, p_a)
    I2 = p11 * I + p12 * Qs
    Q2 = p12 * I + p11 * Qs
    U2 = p33 * Us
    return I2, Q2, U2, e_par_out


def _sample_dir(d, f_r, g, rng):
    """Sample a new direction from the mixture intensity phase function (polarisation is handled by weights)."""
    n = len(d)
    ray = rng.random(n) < f_r
    mu = np.empty(n)
    # Rayleigh by rejection on 1+mu^2
    m = ray.copy()
    out = np.empty(n)
    while m.any():
        k = m.sum()
        x = rng.uniform(-1, 1, k)
        acc = rng.random(k) * 2 < 1 + x * x
        idx = np.flatnonzero(m)
        out[idx[acc]] = x[acc]
        m[idx[acc]] = False
    mu[ray] = out[ray]
    if (~ray).any():
        u = rng.random((~ray).sum())
        if abs(g) < 1e-6:
            mu[~ray] = 2 * u - 1
        else:
            mu[~ray] = (1 + g * g - ((1 - g * g) / (1 - g + 2 * g * u)) ** 2) / (2 * g)
    phi = rng.uniform(0, 2 * np.pi, n)
    e1 = _perp_ref(d)
    e2 = np.cross(d, e1)
    st = np.sqrt(np.clip(1 - mu * mu, 0, 1))
    return _norm(mu[:, None] * d + st[:, None] * (np.cos(phi)[:, None] * e1 + np.sin(phi)[:, None] * e2))


def view_dirs(elev_deg, az_deg):
    """Upward viewing unit vectors (x east, y north, z up) for elevation and azimuth (from north toward east)."""
    el, az = np.broadcast_arrays(np.radians(elev_deg), np.radians(az_deg))
    return np.stack([np.cos(el) * np.sin(az), np.cos(el) * np.cos(az), np.sin(el)], -1)


def observer_ref(v):
    """Local reference for a sky point: the direction of increasing elevation toward the zenith (north at zenith)."""
    p = -v                                    # propagation direction toward the observer
    up = np.array([0.0, 0.0, 1.0])
    e = up - np.outer(np.sum(p * up, -1), np.ones(3)) * p
    nz = np.linalg.norm(e, axis=-1) < 1e-9
    e[nz] = np.array([0.0, 1.0, 0.0])
    return _norm(e)


def simulate(sun_zen_deg, views, tau_r=0.17, tau_a=0.3, g=0.7, w_a=0.92, p_a=0.2, albedo=0.3,
             n_photons=200000, max_orders=40, rng=None, sun_az_deg=180.0, single_only=False):
    """Return Stokes (I, Q, U) toward each upward viewing direction, the AoP referenced to observer_ref, and DoP.

    views: (K,3) upward unit vectors. AoP is measured from the observer reference toward p x e (p = -v)."""
    rng = rng or np.random.default_rng(0)
    K = len(views)
    acc = np.zeros((K, 3))
    tau_s = tau_r + tau_a
    sun = view_dirs(90 - sun_zen_deg, sun_az_deg)[None, :]
    d = np.repeat(-sun, n_photons, 0)
    e = _perp_ref(d)
    I = np.ones(n_photons); Q = np.zeros(n_photons); U = np.zeros(n_photons)
    w = np.ones(n_photons)
    tau = np.zeros(n_photons)                       # optical depth from the top
    alive = np.ones(n_photons, bool)
    p_obs = -views
    e_obs = observer_ref(views)
    mu_v = views[:, 2]
    for order in range(max_orders):
        idx = np.flatnonzero(alive)
        if len(idx) == 0:
            break
        dz = d[idx, 2]
        s = -np.log(rng.random(len(idx)))
        tnew = tau[idx] - s * dz
        hit_ground = tnew >= tau_s
        escape = tnew <= 0
        scat = ~(hit_ground | escape)
        # ground: Lambertian, depolarising, upward cosine weighted
        gi = idx[hit_ground]
        if len(gi):
            w[gi] *= albedo
            u1, u2 = rng.random(len(gi)), rng.random(len(gi))
            mu = np.sqrt(u1)
            ph = 2 * np.pi * u2
            st = np.sqrt(1 - mu * mu)
            d[gi] = np.stack([st * np.cos(ph), st * np.sin(ph), mu], -1)
            e[gi] = _perp_ref(d[gi])
            I[gi], Q[gi], U[gi] = 1.0, 0.0, 0.0
            tau[gi] = tau_s
        alive[idx[escape]] = False
        si = idx[scat]
        if len(si) == 0:
            continue
        tau[si] = tnew[scat]
        f_sca = tau_r + tau_a * w_a
        w[si] *= f_sca / tau_s                        # single scattering albedo of the mixture
        f_r = tau_r / f_sca
        # peel off toward each view (radiance at the ground, arbitrary common scale)
        for k in range(K):
            dk = np.repeat(p_obs[k][None, :], len(si), 0)
            I2, Q2, U2, eo = _scatter_stokes(I[si], Q[si], U[si], e[si], d[si], dk, f_r, g, p_a)
            Q2, U2 = _rotate(Q2, U2, eo, np.repeat(e_obs[k][None, :], len(si), 0), dk)
            att = np.exp(-(tau_s - tau[si]) / mu_v[k]) / mu_v[k] * w[si]
            acc[k] += [np.sum(att * I2), np.sum(att * Q2), np.sum(att * U2)]
        if single_only:
            break
        # new direction and Stokes, weight carries the polarisation dependent intensity
        dn = _sample_dir(d[si], f_r, g, rng)
        I2, Q2, U2, eo = _scatter_stokes(I[si], Q[si], U[si], e[si], d[si], dn, f_r, g, p_a)
        ct = np.clip(np.sum(d[si] * dn, -1), -1, 1)
        p11, _, _ = _phase(ct, f_r, g, p_a)
        w[si] *= I2 / (p11 * I[si])
        I[si], Q[si], U[si] = 1.0, Q2 / I2, U2 / I2
        d[si], e[si] = dn, eo
        # Russian roulette
        low = si[w[si] < 0.02]
        if len(low):
            kill = rng.random(len(low)) > 0.5
            alive[low[kill]] = False
            w[low[~kill]] *= 2
    I_, Q_, U_ = acc.T
    dop = np.hypot(Q_, U_) / I_
    aop = 0.5 * np.arctan2(U_, Q_)
    return dict(I=I_, Q=Q_, U=U_, dop=dop, aop=aop)


def single_scatter_rayleigh_dop(gamma_deg):
    """Analytic single scattering Rayleigh degree of polarisation at scattering angle gamma."""
    c = np.cos(np.radians(gamma_deg))
    return (1 - c * c) / (1 + c * c)

"""Unit tests for the Study 3 modules: radiative transfer, compass geometry and the ten state filter."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vectra.sky_rt import simulate, view_dirs, single_scatter_rayleigh_dop   # noqa: E402
from vectra.compass3 import tilt_heading_error                               # noqa: E402
from vectra.filter2 import run_filter                                        # noqa: E402
from vectra.filter3 import run_filter3                                       # noqa: E402


def test_rt_single_scattering_matches_rayleigh_and_zenith_aop():
    v = np.vstack([view_dirs(90.0, 0.0)[None], view_dirs(60.0, np.array([0.0, 90.0, 180.0, 270.0]))])
    for z in (20.0, 50.0):
        r = simulate(z, v, tau_r=0.01, tau_a=0.0, albedo=0.0, n_photons=5000, single_only=True, sun_az_deg=120.0)
        gam = np.degrees(np.arccos(v @ view_dirs(90 - z, 120.0)))
        assert np.max(np.abs(r["dop"] - single_scatter_rayleigh_dop(gam))) < 1e-6
        assert abs(np.degrees(r["aop"][0]) % 180 - 30.0) < 1e-6


def test_rt_multiple_scattering_depolarises_and_keeps_symmetry():
    v = np.vstack([view_dirs(90.0, 0.0)[None], view_dirs(60.0, np.array([90.0, 270.0]))])
    r = simulate(50.0, v, tau_a=0.4, n_photons=20000, sun_az_deg=180.0)
    assert r["dop"][0] < single_scatter_rayleigh_dop(50.0)
    assert abs(r["dop"][1] - r["dop"][2]) < 0.03


def test_tilt_error_zero_when_level_and_grows_near_zenith():
    yaw = np.linspace(-3, 3, 9)
    z = np.zeros_like(yaw)
    assert np.max(np.abs(tilt_heading_error(30 + z, 100 + z, yaw, z, z))) < 1e-12
    e_low = np.abs(tilt_heading_error(60 + z, 100 + z, yaw, np.radians(3) + z, z)).max()
    e_high = np.abs(tilt_heading_error(10 + z, 100 + z, yaw, np.radians(3) + z, z)).max()
    assert e_high > 3 * e_low


def test_filter3_reduces_to_filter2_when_extra_states_are_inert():
    n, dt = 3000, 0.01
    rng = np.random.default_rng(0)
    gyro = rng.normal(0, 0.01, n)
    acc = rng.normal(0, 0.05, (n, 2))
    nf = n // 10
    vo_idx = np.arange(nf) * 10
    ok = np.ones(nf, bool)
    vf = 1 + rng.normal(0, 0.05, nf)
    vr = rng.normal(0, 0.05, nf)
    vw = rng.normal(0, 0.005, nf)
    ci = np.arange(0, n, 20)
    cz = np.mod(rng.normal(0, 0.02, len(ci)), np.pi)
    cd = np.full(len(ci), 0.3)
    floor, c = np.radians(0.5), np.radians(0.05)
    x0 = np.array([0, 0, 0, 1.0, 0, 0, 0, 0])
    p0 = np.array([1e-4, 1e-4, 1e-6, 4, 4, 4e-6, 4e-4, 4e-4])
    rvo = np.array([0.003, 0.0017, 2.4e-5])
    o2, _, nu2, ng2 = run_filter(4, dt, gyro, acc, vo_idx, ok, vf, vr, vw, ci, np.ones(len(ci), bool), cz, cd,
                                 x0, p0, 0.002, 0.02, 1e-4, 1e-3, rvo, 11.34, np.radians(1.0), 6.63, 3, c, floor, 10)
    r = np.full(len(ci), floor ** 2 + (c / 0.3) ** 2)
    o3, nu3, ng3, _ = run_filter3(4, dt, gyro, acc, vo_idx, ok, vf, vr, vw, ci, np.ones(len(ci), bool), cz, r,
                                  np.zeros(len(ci)), np.r_[x0, 0, 0], np.r_[p0, 0, 0], 0.002, 0.02, 1e-4, 1e-3, 0.0,
                                  0.0, 5.0, rvo, 0.0, 11.34, np.radians(1.0), 6.63, 3, 1.0, 0.1, 1.345, 0)
    assert nu2 == nu3 and ng2 == ng3
    assert np.allclose(o2[:, :3], o3[:, :3], atol=1e-9)

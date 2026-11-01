"""Unit tests for the E02 modules: sun position, sky model, degradation and filter."""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vectra.sky import sun_position, zenith_dop, compass_cue        # noqa: E402
from vectra.degrade import Degrader, level_params, drop_mask        # noqa: E402
from vectra.filter2 import run_filter                               # noqa: E402

AD = (24.4539, 54.3773)


def test_sun_noon_june_near_zenith_and_december_low():
    z, _ = sun_position(*AD, datetime(2026, 6, 21, 12, 30) - timedelta(hours=4))
    assert z < 3.0
    z, _ = sun_position(*AD, datetime(2026, 12, 21, 12, 15) - timedelta(hours=4))
    assert 46.0 < z < 50.0


def test_sun_morning_is_east_and_afternoon_west():
    _, a = sun_position(*AD, datetime(2026, 6, 21, 8, 0) - timedelta(hours=4))
    assert 45 < a < 135
    _, a = sun_position(*AD, datetime(2026, 6, 21, 16, 30) - timedelta(hours=4))
    assert 225 < a < 315


def test_rayleigh_dop_limits():
    assert abs(zenith_dop(90.0, 0.6) - 0.6) < 1e-12
    assert zenith_dop(0.0, 0.6) < 1e-12


def test_compass_is_reproducible_and_modulo_pi():
    sky = {"location": {"lat_deg": AD[0], "lon_deg": AD[1], "utc_offset_h": 4},
           "conditions": {"clear": {"dop_factor": 1.0}}}
    sensor = {"d_max": 0.6, "floor_deg": 0.5, "c_deg": 0.05, "dop_meas_sigma": 0.002}
    t = np.arange(0, 60, 0.2)
    yaw = np.linspace(-3, 3, len(t))
    sc = {"local_start": "2026-12-21T09:30", "sky": "clear"}
    a = compass_cue(t, yaw, sc, sky, sensor, np.random.default_rng(3))
    b = compass_cue(t, yaw, sc, sky, sensor, np.random.default_rng(3))
    assert np.array_equal(a["z"], b["z"])
    assert np.all((a["z"] >= 0) & (a["z"] < np.pi))
    err = (a["z"] - yaw + np.pi / 2) % np.pi - np.pi / 2
    assert np.std(err) < np.radians(2.0)


def test_degradation_identity_at_d0_and_darkening_adds_noise():
    cam = dict(airlight=0.6, max_range_m=2000, texp_base_s=0.005, texp_max_s=0.02, blur_base_px=1.0,
               full_well_e=4000, read_noise_e=6)
    img = (np.random.default_rng(0).random((64, 64)) * 200).astype(np.uint8)
    dep = np.full((64, 64), 10.0, np.float32)
    d0 = Degrader(level_params({"D0": {}}, "D0"), cam, np.random.default_rng(1), 64)
    assert np.array_equal(d0(img, dep, 0.0, np.random.default_rng(1)), img)
    d4 = Degrader(level_params({"D4": {"gain": 0.025}}, "D4"), cam, np.random.default_rng(1), 64)
    out = d4(img, dep, 0.0, np.random.default_rng(1))
    assert np.abs(out.astype(int) - img.astype(int)).mean() > 2.0


def test_drop_mask_fraction():
    m = drop_mask(20000, 0.2, 0.5, 0.1, np.random.default_rng(0))
    assert 0.15 < m.mean() < 0.25


def _straight(n=3000, dt=0.01):
    gyro = np.zeros(n)
    acc = np.zeros((n, 2))
    nf = n // 10
    vo_idx = np.arange(nf) * 10
    return gyro, acc, vo_idx, nf


def test_filter_noise_free_tracks_truth_and_b0_ignores_cue():
    gyro, acc, vo_idx, nf = _straight()
    ok = np.ones(nf, bool)
    vf = np.full(nf, 1.0)
    z0 = np.zeros(nf)
    ci = np.arange(0, len(gyro), 20)
    common = (ci, np.ones(len(ci), bool), np.full(len(ci), 0.3), np.full(len(ci), 0.3),
              np.array([0, 0, 0, 1.0, 0, 0, 0, 0]), np.full(8, 1e-6), 1e-4, 1e-3, 1e-6, 1e-5,
              np.array([1e-4, 1e-4, 1e-6]), 11.34, np.radians(1.0), 6.63, 3, np.radians(0.05),
              np.radians(0.5), 20)
    out, _, nu, _ = run_filter(0, 0.01, gyro, acc, vo_idx, ok, vf, z0, z0, *common)
    assert nu == 0
    assert abs(out[-1, 0] - 29.9) < 0.2 and abs(out[-1, 1]) < 0.05
    out4, _, nu4, ng4 = run_filter(4, 0.01, gyro, acc, vo_idx, ok, vf, z0, z0, *common)
    assert nu4 + ng4 == len(ci)


def test_sun_matches_independent_reference():
    """Solar zenith angles from the astral package (computed once, 2026-11-01) for Abu Dhabi, local time UTC+4."""
    ref = {"2026-06-21T08:00": 59.74, "2026-06-21T12:00": 5.64, "2026-06-21T12:30": 1.65, "2026-06-21T16:30": 55.63,
           "2026-12-21T08:00": 79.14, "2026-12-21T12:15": 47.89, "2026-12-21T16:00": 71.53}
    for s, z_ref in ref.items():
        z, _ = sun_position(*AD, datetime.fromisoformat(s) - timedelta(hours=4))
        assert abs(z - z_ref) < 0.2, (s, z, z_ref)

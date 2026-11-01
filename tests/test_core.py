import ast
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config                      # noqa: E402
from vectra.trajectory import make_trajectory, FAMILIES    # noqa: E402
from vectra.sensors import rng_for, simulate_imu, simulate_visual, simulate_heading  # noqa: E402
from vectra.estimators import run_estimator                # noqa: E402
from vectra.evaluation import run_metrics, holm            # noqa: E402

CFG = load_config(ROOT / "configs" / "e01_sim.yaml")


def _run(name, fam="meander", ti=0, seed=0, lv="D2"):
    tr = make_trajectory(fam, ti)
    fi = FAMILIES.index(fam)
    imu = simulate_imu(tr, rng_for("imu", fi, ti, seed), CFG["imu"])
    hd = simulate_heading(tr, rng_for("heading", fi, ti, seed), CFG["heading"])
    vis = simulate_visual(tr, rng_for("visual", fi, ti, seed, int(lv[1:])), CFG["visual"], CFG["levels"][lv], CFG["timing"])
    est = run_estimator(name, tr, imu, vis, hd, CFG)
    return tr, est


def test_same_seed_same_output():
    _, a = _run("B2")
    _, b = _run("B2")
    assert np.array_equal(a["x"], b["x"]) and np.array_equal(a["theta"], b["theta"])


def test_different_seed_differs():
    _, a = _run("B1", seed=0)
    _, b = _run("B1", seed=1)
    assert not np.array_equal(a["x"], b["x"])


def test_noise_free_estimator_tracks_truth():
    cfg = {k: (dict(v) if isinstance(v, dict) else v) for k, v in CFG.items()}
    cfg["imu"].update(gyro_noise_density=1e-9, accel_noise_density=1e-9, gyro_bias_init_sigma=1e-9, gyro_bias_rw=1e-12,
                      accel_bias_init_sigma=1e-9, accel_bias_rw=1e-12)
    tr = make_trajectory("meander", 0)
    imu = simulate_imu(tr, np.random.default_rng(0), cfg["imu"])
    n = len(tr["t"])
    vis = {"valid": np.zeros(n, bool), "v": np.zeros(n), "w": np.zeros(n)}
    hd = {"valid": np.zeros(n, bool), "z": np.zeros(n), "reliable": np.ones(n, bool)}
    est = run_estimator("B0", tr, imu, vis, hd, cfg)
    m = run_metrics(tr, est)
    assert m["drift_pct"] < 0.5


def test_b0_ignores_heading_cue():
    tr, a = _run("B0")
    n = len(tr["t"])
    fi = FAMILIES.index("meander")
    imu = simulate_imu(tr, rng_for("imu", fi, 0, 0), CFG["imu"])
    vis = simulate_visual(tr, rng_for("visual", fi, 0, 0, 2), CFG["visual"], CFG["levels"]["D2"], CFG["timing"])
    hd = simulate_heading(tr, rng_for("heading", fi, 0, 0), CFG["heading"])
    hd2 = dict(hd)
    hd2["z"] = hd["z"] + 1.0
    b = run_estimator("B0", tr, imu, vis, hd2, CFG)
    assert np.array_equal(a["x"], b["x"])


def test_split_has_no_family_overlap():
    d = CFG["data"]
    held = [f for f in d["families"] if f not in d["pilot_families"]]
    assert set(held).isdisjoint(d["pilot_families"]) and len(held) > 0


def test_path_length_positive_and_start_at_origin():
    for fam in FAMILIES:
        tr = make_trajectory(fam, 0)
        assert tr["path_length"] > 20 and tr["x"][0] == 0 and tr["y"][0] == 0


def test_holm_monotone_and_bounded():
    adj = holm([0.01, 0.04, 0.03, 0.5])
    assert np.all(adj <= 1) and adj[0] == 0.04


def test_layer_contract():
    order = ["config", "trajectory", "sensors", "estimators", "evaluation"]
    rank = {m: i for i, m in enumerate(order)}
    for m in order:
        tree = ast.parse((ROOT / "src" / "vectra" / f"{m}.py").read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("vectra"):
                names = [node.module.split(".")[1]] if "." in node.module else [a.name for a in node.names]
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[1] for a in node.names if a.name.startswith("vectra.")]
            for n in names:
                assert rank[n] < rank[m], f"{m} imports higher or same layer {n}"

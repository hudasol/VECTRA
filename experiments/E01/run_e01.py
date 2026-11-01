"""Run E01 simulation. Usage: python run_e01.py --config CFG --split pilot|heldout --out CSV [--override key=value ...]
Every random stream is seeded from (stream, family, trajectory, seed, level)."""
import argparse
import copy
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config                      # noqa: E402
from vectra.trajectory import make_trajectory, FAMILIES    # noqa: E402
from vectra.sensors import rng_for, simulate_imu, simulate_visual, simulate_heading  # noqa: E402
from vectra.estimators import run_estimator                # noqa: E402
from vectra.evaluation import run_metrics                  # noqa: E402

ESTIMATORS = ["B0", "B1", "B1g", "B2"]


def apply_override(cfg, item):
    key, val = item.split("=", 1)
    d = cfg
    parts = key.split(".")
    for p in parts[:-1]:
        d = d[p]
    d[parts[-1]] = type(d[parts[-1]])(eval(val)) if not isinstance(d[parts[-1]], str) else val


def run(cfg, split, out_csv, estimators=ESTIMATORS, levels=None, tag=""):
    d = cfg["data"]
    fams = d["pilot_families"] if split == "pilot" else [f for f in d["families"] if f not in d["pilot_families"]]
    levels = levels or list(cfg["levels"].keys())
    rows = []
    for fam in fams:
        fi = FAMILIES.index(fam)
        for ti in range(d["trajectories_per_family"]):
            traj = make_trajectory(fam, ti, cfg["timing"]["duration_s"], 1.0 / cfg["timing"]["imu_rate_hz"])
            for seed in range(d["seeds"]):
                imu = simulate_imu(traj, rng_for("imu", fi, ti, seed), cfg["imu"])
                head = simulate_heading(traj, rng_for("heading", fi, ti, seed), cfg["heading"])
                for lv in levels:
                    li = int(lv[1:])
                    vis = simulate_visual(traj, rng_for("visual", fi, ti, seed, li), cfg["visual"], cfg["levels"][lv], cfg["timing"])
                    for e in estimators:
                        est = run_estimator(e, traj, imu, vis, head, cfg)
                        m = run_metrics(traj, est, cfg["filter"]["failure_drift_ratio_pct"])
                        rows.append({"split": split, "family": fam, "traj": ti, "seed": seed, "level": lv, "estimator": e, "tag": tag, **m})
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--split", choices=["pilot", "heldout"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--override", nargs="*", default=[])
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    cfg = load_config(a.config)
    for o in a.override:
        apply_override(cfg, o)
    t0 = time.time()
    rows = run(cfg, a.split, a.out, tag=a.tag)
    print(f"{len(rows)} runs in {time.time()-t0:.1f}s -> {a.out}")

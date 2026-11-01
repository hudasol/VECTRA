"""Pilot only: VO error statistics per degradation level on pilot trajectories.
Used to set the level parameters and the nominal visual noise before the freeze."""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent)); sys.path.insert(0, str(ROOT / "src"))
from run_vo import fetch, load, run_vo, CACHE        # noqa: E402
from vectra.config import load_config                # noqa: E402

def truth_body(d):
    dp = np.diff(np.c_[d["x"], d["y"]], axis=0); th = d["yaw"][:-1]
    vf = (np.cos(th) * dp[:, 0] + np.sin(th) * dp[:, 1]) / 0.1
    vr = (-np.sin(th) * dp[:, 0] + np.cos(th) * dp[:, 1]) / 0.1
    w = np.diff(np.unwrap(d["yaw"])) / 0.1
    return vf, vr, w

if __name__ == "__main__":
    cfg = load_config(ROOT / "configs" / "e02.yaml")
    trajs = sys.argv[1:]
    rows = []
    for tr in trajs:
        work = CACHE / ("calib__" + tr.replace("/", "__")); work.mkdir(parents=True, exist_ok=True)
        fetch(cfg, tr, work); d = load(cfg, work)
        vf, vr, w = truth_body(d)
        for lv in cfg["levels"]:
            r = run_vo(cfg, d, lv, 5)
            ok = r[1:, 0] > 0
            ev = np.abs(np.c_[r[1:, 1] - vf, r[1:, 2] - vr])[ok]
            ew = np.abs(r[1:, 3] - w)[ok]
            row = dict(traj=tr, level=lv, ok_frac=float(ok.mean()), vel_err_med=float(np.median(ev)),
                       vel_err_p90=float(np.percentile(ev, 90)), vel_err_std_f=float(np.std((r[1:, 1] - vf)[ok])),
                       vel_err_std_r=float(np.std((r[1:, 2] - vr)[ok])), w_err_std=float(np.std((r[1:, 3] - w)[ok])),
                       w_err_med=float(np.median(ew)), inliers_med=float(np.median(r[1:, 4][ok])) if ok.any() else 0.0)
            rows.append(row); print(json.dumps(row), flush=True)
        import shutil; shutil.rmtree(work, ignore_errors=True)
    out = ROOT / "results" / "e02_pilot_levels.jsonl"
    with open(out, "a") as fh:
        for r in rows: fh.write(json.dumps(r) + "\n")

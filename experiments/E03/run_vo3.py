"""Study 3 step 1: stereo VO on confirmation trajectories never used before, with several degradation seeds.
Reuses the frozen E02 pipeline (run_vo.py) and also stores terrain roll, pitch and height for the tilt analysis.
Output: results/e03_vo/<env>__<traj>.npz  (RENDERED images, SIMULATED degradation)
Usage: python run_vo3.py --split confirmation [--workers 1]"""
import argparse
import shutil
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation as Rot

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "E02"))
sys.path.insert(0, str(ROOT / "src"))
import run_vo as E2                              # noqa: E402
from vectra.config import load_config            # noqa: E402

CFG = ROOT / "configs" / "e03.yaml"
OUT = ROOT / "results" / "e03_vo"


def process(traj):
    cfg = load_config(CFG)
    name = traj.replace("/", "__")
    out = OUT / f"{name}.npz"
    if out.exists():
        return name, "exists"
    work = E2.CACHE / name
    work.mkdir(parents=True, exist_ok=True)
    try:
        E2.fetch(cfg, traj, work)
        data = E2.load(cfg, work)
        pose = np.loadtxt(next(work.rglob("pose_lcam_front.txt")))[: len(data["x"])]
        eul = Rot.from_quat(pose[:, 3:]).as_euler("ZYX")
        shutil.rmtree(work, ignore_errors=True)
        runs = {}
        for li, level in enumerate(cfg["levels"]):
            seeds = [0] if level == "D0" else list(range(cfg["degradation_seeds"]))
            for s in seeds:
                runs[f"{level}_s{s}"] = E2.run_vo(cfg, data, level, 1000 * li + s + 17)
        OUT.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out, x=data["x"], y=data["y"], z=pose[:, 2], yaw=data["yaw"], pitch=eul[:, 1],
                            roll=eul[:, 2], gyro=data["gyro"], acc=data["acc"], **runs)
        return name, "ok"
    except Exception as e:      # recorded, never silently dropped
        return name, f"error: {e!r}"
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("traj", nargs="*")
    ap.add_argument("--split")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    cfg = load_config(CFG)
    trajs = a.traj or E2.list_trajectories(cfg, cfg["data"][a.split])
    print(len(trajs), "trajectories", flush=True)
    with Pool(a.workers) as pool:
        for name, status in pool.imap_unordered(process, trajs):
            print(name, status, flush=True)

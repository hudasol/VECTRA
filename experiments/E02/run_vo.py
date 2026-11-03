"""E02 step 1: download one TartanGround trajectory, degrade its stereo frames at every
level and seed, run the stereo visual odometry, and save the measurements with ground truth.

Images are deleted after processing. Only the measurement file is kept:
results/e02_vo/<env>__<traj>.npz

Usage: python run_vo.py <env/Data_x/Pxxxx> [<...>]  (or --split pilot|heldout --workers 2)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from scipy.spatial.transform import Rotation as Rot

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from vectra.config import load_config          # noqa: E402
from vectra.degrade import Degrader, level_params, drop_mask   # noqa: E402
from vectra.vo import StereoVO                  # noqa: E402

CACHE = Path(os.environ.get("VECTRA_CACHE", str(Path(__file__).resolve().parents[2] / "data" / "tg_cache")))
OUT = ROOT / "results" / "e02_vo"


def list_trajectories(cfg, envs):
    import urllib.request
    url = "https://huggingface.co/api/datasets/" + cfg["data"]["repo"]
    meta = json.load(urllib.request.urlopen(url, timeout=60))
    files = [s["rfilename"] for s in meta["siblings"]]
    out = []
    for e in envs:
        out += sorted({f.rsplit("/", 1)[0] for f in files if f.startswith(e + "/") and f.endswith("/imu.zip")})
    excl = set(cfg["data"].get("excluded", []))
    return [t for t in out if t not in excl]


def fetch(cfg, traj, work):
    base = cfg["data"]["base_url"] + "/" + traj
    for name in ["metadata", "imu", "image_lcam_front", "image_rcam_front", "depth_lcam_front"]:
        z = work / f"{name}.zip"
        if not z.exists():
            subprocess.run(["curl", "-sSL", "--retry", "3", "-m", "1200", "-o", str(z), f"{base}/{name}.zip"], check=True)
        with zipfile.ZipFile(z) as zz:
            zz.extractall(work)
        z.unlink()


def load(cfg, work):
    S = cfg["data"]["image_size"]
    pose = np.loadtxt(work / "pose_lcam_front.txt") if (work / "pose_lcam_front.txt").exists() \
        else np.loadtxt(next(work.rglob("pose_lcam_front.txt")))
    n = min(len(pose), cfg["data"]["max_frames"])
    imu_dir = next(work.rglob("imu_time.npy")).parent
    gyro = np.load(imu_dir / "gyro.npy")[: 10 * n, 2]
    acc = np.load(imu_dir / "acc_nograv_body.npy")[: 10 * n, :2]
    L = np.empty((n, S, S), np.uint8)
    R = np.empty((n, S, S), np.uint8)
    Dp = np.empty((n, S, S), np.float32)
    ld = next(work.rglob("image_lcam_front"))
    rd = next(work.rglob("image_rcam_front"))
    dd = next(work.rglob("depth_lcam_front"))
    for k in range(n):
        L[k] = cv2.resize(cv2.imread(str(ld / f"{k:06d}_lcam_front.png"), 0), (S, S), interpolation=cv2.INTER_AREA)
        R[k] = cv2.resize(cv2.imread(str(rd / f"{k:06d}_rcam_front.png"), 0), (S, S), interpolation=cv2.INTER_AREA)
        d = cv2.imread(str(dd / f"{k:06d}_lcam_front_depth.png"), cv2.IMREAD_UNCHANGED).view("<f4").squeeze(-1)
        Dp[k] = cv2.resize(d, (S, S), interpolation=cv2.INTER_NEAREST)
    yaw = Rot.from_quat(pose[:n, 3:]).as_euler("ZYX")[:, 0]
    return dict(x=pose[:n, 0], y=pose[:n, 1], yaw=yaw, gyro=gyro, acc=acc, L=L, R=R, D=Dp)


def run_vo(cfg, data, level, seed):
    S = cfg["data"]["image_size"]
    p = level_params(cfg["levels"], level)
    rng = np.random.default_rng(seed)
    degL = Degrader(p, cfg["camera"], rng, S)
    degR = Degrader(p, cfg["camera"], np.random.default_rng(seed), S)   # same glare geometry
    degR.glare_map = degL.glare_map
    n = len(data["x"])
    drop = drop_mask(n, p["drop_frac"], cfg["camera"]["drop_mean_burst_s"], 0.1, rng)
    vo = StereoVO(fx=S / 2, cx=S / 2 - 0.5, cy=S / 2 - 0.5, baseline=cfg["data"]["baseline_m"])
    res = np.zeros((n, 5))
    gap = 1
    for k in range(n):
        if drop[k]:
            gap += 1
            continue
        w = data["gyro"][min(10 * k, len(data["gyro"]) - 1)]
        li = degL(data["L"][k], data["D"][k], w, rng)
        ri = degR(data["R"][k], data["D"][k], w, rng)
        ok, vf, vr, wr, ninl = vo.step(li, ri, 0.1 * gap)
        res[k] = (ok, vf, vr, wr, ninl)
        gap = 1
    return res


def process(traj):
    cfg = load_config(ROOT / "configs" / "e02.yaml")
    name = traj.replace("/", "__")
    out = OUT / f"{name}.npz"
    if out.exists():
        return name, "exists"
    work = CACHE / name
    work.mkdir(parents=True, exist_ok=True)
    try:
        fetch(cfg, traj, work)
        data = load(cfg, work)
        shutil.rmtree(work, ignore_errors=True)
        runs = {}
        for li, level in enumerate(cfg["levels"]):
            seeds = [0] if level == "D0" else list(range(cfg["degradation_seeds"]))
            for s in seeds:
                runs[f"{level}_s{s}"] = run_vo(cfg, data, level, 1000 * li + s + 17)
        OUT.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out, x=data["x"], y=data["y"], yaw=data["yaw"], gyro=data["gyro"], acc=data["acc"],
                            **{k: v for k, v in runs.items()})
        return name, "ok"
    except Exception as e:      # recorded, never silently dropped
        return name, f"error: {e!r}"
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("traj", nargs="*")
    ap.add_argument("--split")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    cfg = load_config(ROOT / "configs" / "e02.yaml")
    trajs = a.traj or list_trajectories(cfg, cfg["data"][a.split])
    print(len(trajs), "trajectories", flush=True)
    with Pool(a.workers) as pool:
        for name, status in pool.imap_unordered(process, trajs):
            print(name, status, flush=True)

"""Pre specified sensitivity grid S1 on the held out split at level D2. One heading parameter changed at a time."""
import copy
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))
from vectra.config import load_config   # noqa: E402
from run_e01 import run                  # noqa: E402

GRID = {
    "noise_sigma_deg": [1.0, 2.0, 4.0, 8.0, 16.0],
    "contamination_start_rate_per_s": [0.0, 0.004, 0.012],
    "bias_rw_deg_per_sqrt_s": [0.05, 0.5, 2.0],
    "dropout_frac": [0.1, 0.5, 0.9],
}

if __name__ == "__main__":
    base = load_config(ROOT / "configs" / "e01_sim.yaml")
    frames = []
    for key, vals in GRID.items():
        for v in vals:
            cfg = copy.deepcopy(base)
            cfg["heading"][key] = v
            rows = run(cfg, "heldout", ROOT / "results" / "_tmp.csv", levels=["D2"], tag=f"{key}={v}")
            df = pd.DataFrame(rows)
            df["param"] = key
            df["value"] = v
            frames.append(df)
    out = pd.concat(frames)
    out.to_csv(ROOT / "results" / "e01_sensitivity.csv", index=False)
    (ROOT / "results" / "_tmp.csv").unlink(missing_ok=True)
    print(len(out), "runs")

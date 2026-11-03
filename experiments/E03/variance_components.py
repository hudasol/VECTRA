"""Variance components of log heading RMSE for B3 on the confirmation split (descriptive): environment,
trajectory, degradation seed within trajectory and level, scenario, and the residual (IMU draw and interactions).
Output results/e03/variance_components.json (shares of the total)."""
import json
import sys
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
d = pd.read_csv(sys.argv[1])
d = d[(d.estimator == "B3") & d.level.isin(["D2", "D4"])].copy()
d["y"] = np.log(d.head_rmse_deg)
d["scen"] = d.date + d.time
d["tseed"] = d.traj + d.level + d.dseed.astype(str)
md = smf.mixedlm("y ~ C(level)", d, groups="env", re_formula="1",
                 vc_formula={"traj": "0 + C(traj)", "tseed": "0 + C(tseed)", "scen": "0 + C(scen)"})
r = md.fit(reml=True)
comp = {"environment": float(r.cov_re.iloc[0, 0])}
for name, val in zip(r.model.exog_vc.names, r.vcomp):
    comp[name] = float(val)
comp["residual"] = float(r.scale)
tot = sum(comp.values())
share = {k: v / tot for k, v in comp.items()}
(ROOT / "results/e03/variance_components.json").write_text(json.dumps(share, indent=1))
print(json.dumps(share, indent=1))

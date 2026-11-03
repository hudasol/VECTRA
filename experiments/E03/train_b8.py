"""Fit the B8 learned reliability model (logistic regression) on pilot split compass samples only.
Input: features dumped by run_filters3.py --split pilot --dump-features. Output: results/e03/b8_model.json"""
import json
import sys
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
F = np.load(sys.argv[1])
X, y = F[:, :3], F[:, 3].astype(int)
rng = np.random.default_rng(0)
idx = rng.permutation(len(y))
tr, te = idx[: int(0.8 * len(y))], idx[int(0.8 * len(y)):]
sc = StandardScaler().fit(X[tr])
m = LogisticRegression(max_iter=1000, class_weight="balanced").fit(sc.transform(X[tr]), y[tr])
auc = roc_auc_score(y[te], m.predict_proba(sc.transform(X[te]))[:, 1])
out = {"features": ["log measured DoP", "cos solar zenith", "log gyro inconsistency of successive readings"],
       "label": "|compass error| > 3 sqrt(r_est)", "mean": sc.mean_.tolist(), "scale": sc.scale_.tolist(),
       "coef": m.coef_[0].tolist(), "intercept": float(m.intercept_[0]), "n_samples": int(len(y)),
       "positive_share": float(y.mean()), "holdout_auc_pilot": float(auc)}
(ROOT / "results" / "e03" / "b8_model.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))

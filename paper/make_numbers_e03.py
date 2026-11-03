"""Every Study 3 number quoted in the paper, as LaTeX macros (prefix \\s), computed from result files only."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[1] / "results"
O = Path(__file__).resolve().parent / "numbers_e03.tex"
M = {}
W = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
     "8": "eight", "9": "nine"}


def key(k):
    return "".join(W.get(ch, ch) for ch in k if ch.isalnum())


def put(k, v, nd=2):
    M[key(k)] = f"{v:.{nd}f}" if isinstance(v, (float, np.floating)) else str(v)


# sky
v = json.loads((R / "e03_sky/validation.json").read_text())
put("SSerr", "numerical precision")
clim = json.loads((R / "e03_sky/power_24.45_54.38.json").read_text())
put("AODann", clim["AOD_55"]["ANN"]); put("AODjun", clim["AOD_55"]["JUN"]); put("AODjul", clim["AOD_55"]["JUL"])
put("RTthirtyfiveLow", v["model_zenith_dop_elev35"]["0.15"]); put("RTthirtyfiveMean", v["model_zenith_dop_elev35"]["0.45"])
put("RTseventyLow", v["model_zenith_dop_elev70"]["0.15"], 3)
crb = v["crb_vs_mc"]
put("CRBdev", max(abs(c["mc_zen_ring_deg"] / c["crb_zen_ring_deg"] - 1) for c in crb) * 100, 0)
for c in crb:
    put(f"CRBzen{int(c['sun_zen'])}", c["crb_zenith_deg"], 1); put(f"CRBring{int(c['sun_zen'])}", c["crb_zen_ring_deg"], 1)
wa = json.loads((R / "e03_sky/blind_window_anchored.json").read_text())
put("WinRT", wa["radiative_transfer|mean|gt10"]["zenith"]); put("WinRTlo", wa["radiative_transfer|low|gt10"]["zenith"])
put("WinRThi", wa["radiative_transfer|high|gt10"]["zenith"]); put("WinAnch", wa["measured_anchored|mean|gt10"]["zenith"])
put("WinRing", wa["radiative_transfer|mean|gt10"]["zenith_ring"]); put("WinRingAnch", wa["measured_anchored|mean|gt10"]["zenith_ring"])
put("WinSun", wa["radiative_transfer|mean|gt10"]["sun_sensor"]); put("WinStudyTwo", wa["study2_law|gt10"])
put("WinRTtwo", wa["radiative_transfer|mean|gt2"]["zenith"]); put("WinRingtwo", wa["radiative_transfer|mean|gt2"]["zenith_ring"])
g = np.load(R / "e03_sky/global_blind_map.npz")
lat_any = g["lat"][(g["minutes"][:, :, 0] > 0).any(1)]
put("LatMax", int(max(abs(lat_any.min()), lat_any.max())))
dw = pd.read_csv(R / "e03_sky/desert_windows.csv")
# measured
m = json.loads((R / "e03/measured_marseille_0729.json").read_text())
put("MeasN", m["n_images_daylight"]); put("MeasCorr", m["corr_dop_sin2"]); put("MeasAopMad", m["aop_residual_mad_deg"], 1)
s = np.load(R / "e03/measured_marseille_0729_series.npz")
c = s["label"] == "c"
gg = np.radians(s["sun_zen"][c]); f = np.sin(gg) ** 2 / (1 + np.cos(gg) ** 2)
put("MeasDmax", float(np.sum(f * s["dop"][c]) / np.sum(f * f)), 3); put("MeasNclear", int(c.sum()))
# pilot fit
pf = json.loads((R / "e03/pilot_fit.json").read_text())
put("PilotSv", pf["sv_sigma"], 3); put("PilotTau", pf["sv_tau_s"], 1)
b8 = json.loads((R / "e03/b8_model.json").read_text())
put("BeightAuc", b8["holdout_auc_pilot"]); put("BeightPos", b8["positive_share"])
# homing
h = pd.read_csv(R / "e03/homing.csv")
hf = json.loads((R / "e03/homing_fit.json").read_text())
for sc, tag in [("march_morning", "M"), ("june_noon", "J")]:
    for hd, ht in [("gyro_only", "Gyro"), ("zenith", "Zen"), ("zenith_tilt_aware", "ZenTA"), ("zenith_ring_tilt_aware", "RingTA"),
                   ("zenith_ring", "Ring"), ("magnetometer", "Mag")]:
        for L in (1000, 3000):
            put(f"hom{tag}{ht}{L // 1000}k", h[(h.scenario == sc) & (h.heading == hd) & (h.path_m == L)].median_err_m.iloc[0], 0)
        put(f"homExp{tag}{ht}", hf[f"{sc}|{hd}"]["exponent"])
# development
dev = pd.read_csv(R / "e03/dev_by_level.csv").set_index(["level", "estimator"])
sel = json.loads((R / "e03/dev_selection.json").read_text())
put("Ssel", sel["selected"])
for e in ["B0", "B3", "B4", "ORH", "ORT", "B3C", "W3"]:
    for lv in ["D0", "D4"]:
        put(f"dev{e}{lv}dr", dev.loc[(lv, e), "drift_med"]); put(f"dev{e}{lv}hd", dev.loc[(lv, e), "head_med"])
        put(f"dev{e}{lv}nees", dev.loc[(lv, e), "nees_med"], 0); put(f"dev{e}{lv}cov", dev.loc[(lv, e), "cover"])
vb = pd.read_csv(R / "e03/vo_bias_dev.csv").groupby("level")[["scale_median", "err_sd", "lag1"]].median()
for lv in ["D0", "D4"]:
    put(f"voScale{lv}", vb.loc[lv, "scale_median"], 3); put(f"voSd{lv}", vb.loc[lv, "err_sd"])
# confirmation (if present)
ct = R / "e03/confirm_tests.csv"
if ct.exists():
    t = pd.read_csv(ct).set_index("H")
    for H in t.index:
        r = t.loc[H]
        nd = 2
        put(f"{H}diff", r.median_diff, nd); put(f"{H}lo", r.ci_lo, nd); put(f"{H}hi", r.ci_hi, nd)
        put(f"{H}A", r.median_A, nd); put(f"{H}B", r.median_B, nd)
        put(f"{H}p", "--" if pd.isna(r.p_holm) else ("$<$0.001" if r.p_holm < 0.001 else f"{r.p_holm:.3f}"))
        put(f"{H}res", "supported" if r.supported else "not supported")
    cs = json.loads((R / "e03/confirm_summary.json").read_text())
    put("Nconf", cs["n_traj"]); put("NrowsConf", cs["n_rows"])
    put("HsixNees", cs["H6_consistency"]["B3C"]["median_nees_pos"], 1); put("HsixCov", cs["H6_consistency"]["B3C"]["mean_cover95"])
    put("HsixNeesBthree", cs["H6_consistency"]["B3"]["median_nees_pos"], 1); put("HsixCovBthree", cs["H6_consistency"]["B3"]["mean_cover95"])
    put("HsixRes", "met" if cs["H6_met"] else "not met"); put("Hseventau", cs["H7_kendall_tau"]); put("HsevenRes", "met" if cs["H7_met"] else "not met")
    cb = pd.read_csv(R / "e03/confirm_by_level.csv").set_index(["level", "estimator"])
    for e in cb.index.get_level_values(1).unique():
        for lv in ["D0", "D2", "D4"]:
            if (lv, e) in cb.index:
                put(f"c{e}{lv}hd", cb.loc[(lv, e), "head_med"]); put(f"c{e}{lv}dr", cb.loc[(lv, e), "drift_med"])
for extra, tag in [("confirm_uncoupled_by_level.csv", "u"), ("confirm_anchored_by_level.csv", "a"), ("confirm_tilt_by_level.csv", "t")]:
    p = R / "e03" / extra
    if p.exists():
        cb = pd.read_csv(p).set_index(["level", "estimator"])
        for e in cb.index.get_level_values(1).unique():
            for lv in ["D0", "D2", "D4"]:
                if (lv, e) in cb.index:
                    put(f"{tag}{e}{lv}hd", cb.loc[(lv, e), "head_med"]); put(f"{tag}{e}{lv}dr", cb.loc[(lv, e), "drift_med"])
# like with like comparison for the dust coupling (seed s0, IMU draw 0 in both runs) and noon values
if ct.exists():
    cf = pd.read_csv(R / "e03/confirm.csv.gz")
    sub = cf[(cf.dseed == "s0") & (cf.fseed == 0) & (cf.level == "D4")]
    tm = sub.groupby(["traj", "estimator"]).head_rmse_deg.mean().groupby("estimator").median()
    put("cpsBzeroDfourhd", tm["B0"]); put("cpsBthreeDfourhd", tm["B3"])
    un = pd.read_csv(R / "e03/confirm_uncoupled.csv.gz")
    tu = un[un.level == "D4"].groupby(["traj", "estimator"]).head_rmse_deg.mean().groupby("estimator").median()
    put("unBzeroDfourhd", tu["B0"]); put("unBthreeDfourhd", tu["B3"])
    put("benefitUn", tu["B0"] - tu["B3"], 1); put("benefitCo", tm["B0"] - tm["B3"], 1)
    put("benefitRed", 100 * (1 - (tm["B0"] - tm["B3"]) / (tu["B0"] - tu["B3"])), 0)
    nn = cf[(cf.date == "2026-06-21") & cf.time.isin(["11:45", "12:30"]) & (cf.estimator == "B1")]
    put("noonBonePooled", nn.head_rmse_deg.mean(), 1); put("noonBoneDzero", nn[nn.level == "D0"].head_rmse_deg.mean(), 1)
    put("factorHone", float(pd.read_csv(ct).set_index("H").loc["H1", "median_B"] / pd.read_csv(ct).set_index("H").loc["H1", "median_A"]), 1)
for lab in ["c"]:
    put("MeasAopMadClear", m["per_label_res_mad_deg"]["c"], 1)
wa_lo = min(wa[f"measured_anchored|{c}|gt10"]["zenith"] for c in ("low", "mean", "high"))
wa_hi = max(wa[f"radiative_transfer|{c}|gt10"]["zenith"] for c in ("low", "mean", "high"))
put("WinMin", wa_lo); put("WinMax", wa_hi)
dor = R / "e03/dev_oracle.csv.gz"
if dor.exists():
    do = pd.read_csv(dor)
    g = do.groupby(["traj", "level", "estimator"]).nees_pos_mean.median().groupby(["level", "estimator"]).median()
    c2 = do.groupby(["traj", "level", "estimator"]).cover95_pos.mean().groupby(["level", "estimator"]).mean()
    for lv in ["D0", "D2", "D4"]:
        for e in ["ORX", "ORH", "ORT", "B0"]:
            put(f"or{e}{lv}nees", g.loc[(lv, e)], 0); put(f"or{e}{lv}cov", c2.loc[(lv, e)])
vc = R / "e03/variance_components.json"
if vc.exists():
    for k2, val in json.loads(vc.read_text()).items():
        put(f"vc{k2}", val * 100, 0)
O.write_text("\n".join(f"\\newcommand{{\\s{k}}}{{{v}}}" for k, v in sorted(M.items())) + "\n")
print(len(M), "macros")

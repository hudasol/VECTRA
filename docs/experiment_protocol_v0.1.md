# Experiment protocol, E01 simulation study (E01 sim), version 0.1

Status: FROZEN on 2026-11-01 before any held out run. Supersedes the draft v0 for the simulation study only. Any change after this point is logged as a deviation in docs/results_register.md.

## 1. What changed from draft v0 and why

1. Scope. The first study is a surrogate level simulation on synthetic planar rover trajectories. The visual front end is abstracted into speed and yaw rate measurements whose noise, dropout and outliers depend on the degradation level D0 to D4. No image is processed. The TartanGround stage (protocol v0) is not run in this study. The dataset host was not reachable from the analysis environment used here, and the team has so far downloaded only the metadata and IMU archives for one trajectory (docs/dataset_audit_A1.md). It remains the next stage.
2. Added system B1g, heading aided fusion with fixed noise and a fixed chi square gate. The novelty audit (docs/novelty_register.md) showed that gating is the standard reliability handling, so B2 must be compared against it.
3. Added a contamination model to the heading cue (offset epochs). Reliability awareness has no purpose if the cue is always equally reliable.
4. Unit of analysis is the trajectory, not the run. Seeds on the same trajectory are not independent. Per trajectory means over 10 seeds are paired across systems (n = 24).
5. Added NEES and 95 percent coverage to the reported results, and a pre specified sensitivity grid S1 (Section 8), following the audit recommendation.

## 2. Hypotheses

H0: with the same visual input and heading cue, B2 gives the same drift ratio as B0, B1 and B1g at every level.
H1: B2 gives a lower drift ratio than B0 and B1 at D2 to D4.
H2 (added after the pilot): B2 gives a lower drift ratio than B1g. The pilot shows near equal values, so we expect H0 to be retained for this comparison. We state this in advance.
The study may return negative results for any of these.

## 3. Systems

All share one planar extended Kalman filter with state (x, y, heading, speed, gyro bias, accelerometer bias), 20 Hz inertial input, 10 Hz visual update (speed and yaw rate, chi square gated at 99 percent, 2 degrees of freedom). They differ only in the heading update.

| ID | Heading update |
| --- | --- |
| B0 | None |
| B1 | Every available cue, fixed noise 3 degrees |
| B1g | As B1, rejected if normalised innovation squared exceeds 6.63 (99 percent, 1 degree of freedom) |
| B2 | Noise set by covariance matching over the last W innovations: R = max(R nominal, mean(innovation squared) minus mean(predicted heading variance)); W = 3 |

Rule used to choose W on the pilot split: lowest mean over levels of the median drift ratio; if all candidates (3, 5, 10, 20) lie within 1 percent of the best, take the smallest. All four were within 1 percent, so W = 3.

## 4. Degradation levels and heading cue

Values are in configs/e01_sim.yaml and are fixed by this protocol. Levels were adjusted once on the pilot split because the first draft saturated at D3 (the pilot B0 median drift reached 36 percent at D3 and 100 percent at D4). Final levels: noise multiplier 1, 1.5, 2.5, 4, 8; dropout fraction 0, 0.03, 0.10, 0.20, 0.35 (mean burst 1.5 s); outlier probability 0, 0.005, 0.01, 0.02, 0.05.

Heading cue: 2 Hz, white noise 2 degrees, initial bias with standard deviation 1 degree, bias random walk 0.05 degrees per square root second, dropout fraction 0.10 (mean burst 10 s), contamination epochs started at 0.004 per second lasting 5 to 20 s with offset 20 to 60 degrees of random sign. The cue is synthetic and idealised.

## 5. Data and splits

Six trajectory families (straight, meander, loops, stopgo, slalom, mixed), six trajectories each, 200 s, about 1 m/s. Pilot split: straight and meander (12 trajectories). Held out split: the other four families (24 trajectories). The held out split was not used to choose any parameter. Seeds 0 to 9 on every trajectory.

## 6. Metrics

Primary (unchanged from v0): drift ratio, final position error divided by path length in percent, no alignment, start pose known.
Secondary: position RMSE, absolute trajectory error after SE(2) alignment, relative pose error over 10 s windows, heading RMSE, failure rate (drift ratio above 10 percent), time averaged position NEES (expected value 2 for a consistent filter), 95 percent coverage of the position ellipse, heading NEES.
Runtime and memory are not measured in this study.

## 7. Statistics

For each level and each of three comparisons (B2 against B1, B0, B1g): paired Wilcoxon signed rank test on per trajectory mean drift ratio (n = 24), median paired difference in percentage points with 95 percent bootstrap interval (10,000 resamples), Cliff's delta. Holm correction over all 15 tests. No run is excluded. All results are reported.

## 8. Sensitivity grid S1 (pre specified, held out split, level D2)

One heading parameter varied at a time: noise 1, 2, 4, 8, 16 degrees (filter nominal stays 3 degrees); contamination rate 0, 0.004, 0.012 per second; bias random walk 0.05, 0.5, 2.0 degrees per square root second; dropout fraction 0.1, 0.5, 0.9. Descriptive medians only, no significance testing.

## 9. Freeze and deviations

Freeze point: the commit that adds this file. The held out and sensitivity results are produced only after it. Deviations are listed in the results register with a reason.

## 10. Threats to validity

Surrogate visual front end; synthetic heading cue; planar motion with no wheel odometry; one filter structure; parameter choices by the authors; four held out families only.

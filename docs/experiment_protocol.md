# Experiment protocol, E01: reliability aware heading fusion under visual degradation

Version: draft v0, 2026-10-20.
Status: NOT FROZEN. Nothing here is a commitment until the freeze date is set and recorded in the results register. Items marked "to set after pilot" are intentionally open.
Protocol review date: to be agreed with the faculty authors (proposed: Wednesday 28 October 2026).

## 1. Hypotheses

H0 (null): With the same visual input and the same heading cue, reliability aware fusion (B2) gives the same drift as fixed noise heading fusion (B1) and as visual inertial only (B0), at every degradation level.

H1 (alternative): At degradation levels D2 to D4, B2 gives lower drift than B1 and B0. At D0, B2 is not worse than B1 by more than a margin set after the pilot.

H2 (secondary alternative): B2 gives better uncertainty calibration than B1 at D2 to D4.

We state in advance that the result may be negative: B1 may match B2, or heading cues may help little when vision is good.

## 2. Systems compared

| ID | Description |
| --- | --- |
| B0 | Visual inertial estimate only. No heading update |
| B1 | B0 plus heading update with a fixed measurement noise |
| B2 | B0 plus heading update whose noise is adapted from a reliability estimate (for example innovation based gating or scaling) |

The estimator route (existing visual inertial system with a custom update, or a transparent planar estimator) is decided in docs/baseline_feasibility.md. The three systems must share the same code path except for the heading update, so that the comparison is fair.

## 3. Degradation levels

D0 clean, D1 mild, D2 moderate, D3 severe, D4 near blackout. Candidate operations: brightness scaling, blur, sensor noise, frame dropout. Numeric ranges: to set after pilot, so that D0 to D4 produce graded and not saturated difficulty. The ranges are recorded in configs/degradation.yaml before the main run and not changed afterwards.

## 4. Heading cue model

Synthetic cue from ground truth yaw with: white noise (sigma), constant bias, bias random walk, and dropout epochs (probability and duration). Values: to set after pilot. The cue is idealised, and this limitation is stated wherever results are reported.

## 5. Metrics

Primary metric (chosen now, before any result exists): drift ratio, defined as the Euclidean position error at the end of a trajectory divided by the path length travelled, in percent, with the estimate anchored at the known start pose and no further alignment.

Reason: our question is about accumulated drift when external position is unavailable, and a robot in the field does not get to align its trajectory to ground truth. Best fit alignment, as used in absolute trajectory error, can hide drift by redistributing it along the path. Normalising by path length makes trajectories of different length comparable. Its weakness is that it uses only the end point, so we report the secondary metrics below to show behaviour along the path.

Secondary metrics:
1. Absolute trajectory error (RMSE), with the alignment method stated.
2. Relative pose error over fixed distance windows.
3. Heading error over time and at the end.
4. Error versus distance travelled (curve).
5. Failure rate: share of runs whose drift ratio exceeds a threshold set after pilot. Recovery time after a degradation epoch.
6. Uncertainty calibration: normalised estimation error squared, and coverage of confidence intervals.
7. Runtime and memory per estimator.

## 6. Data and splits

Data: TartanGround subset, to be fixed after the dataset check (task A1). Trajectories are split by environment into a pilot set and a held out evaluation set before any tuning. The held out set is not used for choosing parameters. Split lists are saved in experiments/E01 and committed before the main run.

## 7. Seeds and repeats

Every stochastic step (degradation, heading noise, dropout) takes an integer seed. Each trajectory and degradation level is run with N seeds (N set after pilot, minimum 10). Same seed and config must reproduce the same output exactly; a test will check this.

## 8. Statistics

Comparisons are paired by trajectory and seed. For each degradation level we test B2 against B1 and B2 against B0 on the primary metric using a Wilcoxon signed rank test, report the median paired difference with a bootstrap 95 percent confidence interval, and correct for multiple comparisons with the Holm method. We report effect sizes and every comparison, including those that are not significant. We do not drop runs after seeing results; failed runs are counted as failures.

## 9. Freeze procedure

1. Pilot on the pilot split only, to set ranges and N.
2. Update the configs and the placeholders in this document.
3. Record the commit hash and date as the freeze point in the results register.
4. Run E01 on the held out split. Any change afterwards is logged as a deviation with a reason.

## 10. Threats to validity (draft)

Synthetic heading; simulation only; one dataset family; baseline implementation choices; possible overfitting if the pilot and held out splits leak.

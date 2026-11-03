# S3 Review D: statistics and experimental design

Scope: paper/vectra_paper.tex, docs/experiment_protocol_v0.2.md, docs/results_register.md, experiments/E02/analyze_e02.py, src/vectra/evaluation.py, results/e02_heldout_F1.csv, F2, F3. Two descriptive checks were computed read only from results/e02_heldout.csv.gz and are quoted where used.

## Weaknesses

**1. Small, clustered trajectory sample.** Claim: all F1 and F2 results. The 34 trajectories (at most 200 s) come from three environments (MiddleEast 14, DesertGasStation 11, EndofTheWorld 9), which share scenery and lighting; the effective sample for new desert scenes is nearer 3 than 34. Fix: at least 6 unused environments, analysed with random intercepts for environment and trajectory or a cluster bootstrap over environments. Direction: wider intervals; drift differences under 0.11 percentage points may lose significance.

**2. One degradation seed per level.** Claim: "levels are graded" and every level wise test. The seed is confounded with the trajectory and its variance is never estimated. Fix: at least 2 to 3 seeds per trajectory and level, nested random effect. Direction: larger residual variance at D3 and D4.

**3. Two IMU draws shared by all scenarios.** Claim: H1 (B3 against B0). B0 has two distinct runs per cell but is averaged as if it had 96. Fix: IMU noise drawn per run. Direction: H1 likely survives (large effects) with honest intervals.

**4. Scenarios crossed within trajectory.** Claim: the 97,920 run total and run level medians and failure shares. The 48 scenarios and 2 filter seeds reuse one visual odometry and IMU stream, so runs are pseudo replicates. At D2 the within trajectory variance of the B3 minus B2 heading difference (3.20) is about 14 times the between trajectory variance of trajectory means (0.23). Fix: crossed mixed model with trajectory, scenario and their interaction, reporting variance components. Direction: the scenario by system interaction becomes the main finding.

**5. Held out set already inspected.** Claim: any future confirmatory use, including B4. The set fed R-006, R-007 and the noon, cloud and lock out cuts. Fix: new frozen protocol on unseen environments; the current set becomes a second pilot. Direction: smaller effects for B3 and B4.

**6. Holm families split the primary hypotheses.** Claim: H1 to H3 verdicts. F1 and F2 are both primary but corrected separately, roughly doubling familywise error. H1 concerns D2 to D4, yet D0 and D1 sit in the family; F3 pools drift and coverage. Fix: one endpoint per hypothesis with a gatekeeping order. Direction: fewer, cleaner claims.

**7. H3 judged without a non inferiority margin.** Claim: "H3 is rejected". A two sided test against zero with n = 34 rejects any consistent tiny difference: B2 beats B3 by 0.008 to 0.087 percentage points of drift and 0.04 to 0.38 degrees of heading RMSE. Fix: prespecified margins (for example 0.25 percentage points, 0.5 degrees) tested one sided on the upper 95 percent cluster bootstrap bound. Direction: B3 likely non inferior on drift at all levels and on heading outside cloud.

**8. Small effects; mislabelled statistic.** Claim: H2 and the abstract. B3 minus B1g drift is 0.05 to 0.11 percentage points on a 0.9 to 3.3 percent base. cliffs_delta_paired computes a sign statistic, not Cliff's delta. Fix: prespecify a smallest effect of interest, report ratios of geometric means with intervals, rename the statistic. Direction: H2 holds on heading, near null on drift.

**9. Sky mix not weighted by climatology.** Claim: every pooled comparison, above all H3. Broken cloud is 25 percent of scenarios. Mean B3 minus B2 heading difference: +1.01 degrees under cloud against -0.045 to -0.026 under clear, haze and dust at D2; +1.79 against +0.02 to +0.05 at D4. H3 is driven by one sky condition whose frequency over Abu Dhabi is far below 25 percent; two dates and six times also do not represent a year. Fix: weight sky, date and time strata by a stated climatology (public reanalysis or airport records) and report stratified and weighted estimates. Direction: H3 likely becomes a tie or reverses.

**10. Exploratory B4 not confirmed.** Claim: the recommendation for DoP floored covariance matching. B4 was designed after seeing the cloud failure, on the same runs. Fix: prespecified B4 arm, non inferiority to B2 with the item 7 margin. Direction: a tie, now inferential.

**11. Intervals ignore discreteness and clustering.** Claim: Table 2 intervals and p values. A percentile bootstrap of a median on 34 points undercovers; p values near 1e-10 are the exact minimum at n = 34, not effect strength. Fix: BCa or cluster bootstrap of the Hodges Lehmann estimator. Direction: wider intervals.

**12. Missing variance components; noisy endpoint.** Claim: "levels are graded", coverage claims. Environment, trajectory, degradation seed, IMU draw and compass seed are never separated, and drift uses only the final position. Fix: report mixed model variance components and add a time averaged endpoint. Direction: sizes future studies correctly.

## Three most damaging issues, ranked

1. Item 9: the sky mix drives H3 and the pooled B3 against B2 conclusion.
2. Items 1 and 4: three environments plus pseudo replication overstate precision.
3. Item 7: H3 uses the wrong hypothesis structure.

## Minimal confirmation design (2 CPU cores, about two hours)

- Data: 12 unseen trajectories, 2 from each of 6 new environments, first 120 s; list frozen before processing.
- Arms: B0, B1g, B2, B3, B4. Levels D0, D2, D4.
- Seeds: 2 degradation seeds per trajectory and level (72 visual odometry runs, the main cost); IMU noise drawn per run.
- Scenarios: 21 June and 21 December; 09:30, 11:45, 12:30, 14:30; clear, dust, cloud; 1 filter seed. 24 scenarios, 72 x 24 x 5 = 8,640 filter runs.
- Budget check: time 2 visual odometry runs and 50 filter runs on the pilot split first; if the projection exceeds 110 minutes on 2 workers, drop D0 before cutting trajectories.
- Endpoints: heading RMSE at D2 and D4. Gatekeeping order: H1 B3 against B0 (superiority), H2 B3 against B1g (superiority), H3 B3 against B2 (non inferiority, margin 0.5 degrees), H5 B4 against B2 (non inferiority, same margin).
- Analysis: linear mixed model on log heading RMSE, fixed system, level, sky and interactions, random environment, trajectory and degradation seed; confirmed by a two stage cluster bootstrap (environments, then trajectories, 10,000 resamples). Report climatology weighted and unweighted estimates and all variance components.

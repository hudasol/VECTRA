# S3 Review B: estimator and evaluation

Scope: paper, filter2.py, vo.py, run_filters.py, configs/e02.yaml, compass_cue in sky.py, results/e02_heldout_secondary.csv, claims_and_limitations.md. No code was run.

## Weaknesses

**1. Planar state with privileged gravity removal.** Claim affected: drift reductions of a quarter to a half at D3 and D4. The filter consumes the dataset's gravity free body acceleration, which was produced with the true attitude, and only the vertical gyro. With a real IMU, roll or pitch error leaks g sin(error) into horizontal acceleration, often the dominant drift source on slopes. B0 drift is therefore understated and the share attributed to heading is unverified. Test: synthesise raw specific force from ground truth attitude plus gravity, add the same noise, and rerun B0 and B3 in a 15 state SE(3) error state filter. Expected direction: B0 and B3 drift both rise; the relative compass benefit probably shrinks, because tilt induced error is not corrected by a yaw aid.

**2. No established VIO baseline.** Claim affected: heading RMSE reduced by about an order of magnitude relative to B0. B0 is a loosely coupled frame to frame PnP front end with no window, mapping or first estimates Jacobian. OpenVINS reports position NEES of about 2 in simulation with FEJ and online calibration [1],. Test: run OpenVINS (or VINS Fusion) on the D0 to D4 image sequences with the synthesised IMU of item 1, with and without a yaw measurement. Expected direction: lower B0 drift and heading error, a smaller ratio of improvement, and fewer VO failures counted as outliers.

**3. Overconfidence that invalidates the gate and B2.** Claim affected: comparisons among B1g, B2 and B3, and the gate lock out explanation. Median position NEES spans 21 to 81 (ideal 2) and 95 percent coverage spans 0.09 to 0.27 in results/e02_heldout_secondary.csv. Every scheme that compares an innovation with P[2,2] uses a predicted covariance known to be too small, so rankings partly measure how each scheme tolerates a wrong P, not how it weights the compass. Test: report yaw NEES and compass NIS separately per system, then repeat F1 and F2 after scaling Q and R on the pilot split until pilot yaw NEES is near 1. Expected direction: the B1g deficit narrows and the B2 advantage over B3 may shrink.

**4. Unmodelled gyro noise in the bias measurement.** Claim affected: consistency section and B0 heading. The third VO row measures gyro mean minus VO yaw rate, but R uses only the VO MAD (0.0049 rad/s). The added gyro white noise is 0.02 rad/s per 100 Hz sample, so the 10 sample mean contributes about 0.0063 rad/s, which R omits; the same samples also drove the yaw prediction, a correlation the filter ignores. Test: set the third R entry to the sum of both variances, or remove the bias row and add a proper yaw rate state, then recompute yaw NEES. Expected direction: yaw and position NEES fall measurably for every system.

**5. White VO noise assumption.** Claim affected: overconfidence attributed to "likely" correlated VO errors. At 320 px and 90 degree field of view, fx is about 160 px, so disparity at the 40 m depth cap is 1 px, the minimum accepted; stereo depth and hence velocity scale are biased and correlated across frames sharing tracks. Test: from the saved results/e02_vo runs, compute VO residual mean, lag 1 to 10 autocorrelation and Allan deviation per level (cheap). Expected direction: positive autocorrelation and a nonzero scale bias growing with level; a shaping filter or scale bias state should raise coverage more than B3a.

**6. Fixed VO noise across levels.** Claim affected: H4 and drift at D3 and D4. R is the D0 pilot MAD at every level; MAD also understates heavy tails. B3a adapts one scalar. Test: an oracle run with per level R from held out residuals, isolating weighting from mistuning. Expected direction: B0 to B3 coverage rises sharply; the B3a coverage gain largely disappears.

**7. Robust VO inflation.** Claim affected: the pilot fix of bounded inflation. The code states that inflating R makes the NIS equal the gate, but only R is scaled, so the post inflation NIS remains above the gate; every VO outlier is still fused. Test: log the fraction of inflated VO updates per level and compare with Huber or Cauchy weighting and with hard rejection plus covariance inflation on recovery. Expected direction: inflation is frequent at D3 and D4, and drift changes for B0 more than for compass systems.

**8. Gate lock out has no recovery.** Claim affected: B3 losing to B2 under cloud. When a sample is gated, P[2,2] is not inflated and no counter forces reacceptance, so a heading error beyond about 2.6 sigma persists. The mechanism is stated but untested. Test: log consecutive rejections per run; add a rule that inflates P[2,2] after N rejections. Expected direction: B3 cloud heading RMSE falls toward B2, and the stuck run share drops.

**9. B3 circularity.** Claim affected: H2 and "DoP weighting used partial information best". compass_cue draws angle noise from sigma^2 = floor^2 + (c/d)^2 with the same floor and c that B3 uses, and d_meas has 0.002 noise, so B3 knows the true noise except under cloud, the only scenario where it loses. Test: rerun with mismatched laws (c doubled and halved, exponent 1.5, a bias random walk, and tilt from the ground truth roll and pitch already in TartanGround). Expected direction: B3's advantage over B1g shrinks and its gap to B2 widens.

**10. Known start pose and tiny initial yaw variance.** Claim affected: B0 heading and drift baselines over 200 s. Yaw variance starts at 1e-6 rad^2 and velocity is seeded from ground truth. Test: perturb the initial yaw by 5 degrees with matching P0. Expected direction: compass systems gain more and the 180 degree ambiguity resolution via the prior becomes testable.

**11. Short trajectories and endpoint drift.** Claim affected: drift ratios. Up to 200 s with one degradation seed; endpoint drift is noisy and dominated by the last seconds. Test: report drift versus distance curves and per segment RPE on yaw. Expected direction: compass benefit over B0 grows with duration.

**12. Tiny heading effects relative to sensor floor.** Claim affected: H2 support. In results/e02_heldout_secondary.csv the B1g minus B3 heading medians are 0.02 to 0.08 degrees, while the paper states paired differences of 0.14 to 0.37; this should be reconciled. Either way the gap is below the 0.5 degree sensor floor and rests on item 9. Test: equivalence bounds of 0.1 degree. Expected direction: several H2 cells become practically equivalent.

## Three most damaging issues, ranked

1. Item 9, B3 circularity: the central DoP weighting result is not separable from the simulator matching the filter.
2. Items 1 and 2, planar filter with privileged gravity removal and no established VIO baseline: the absolute and relative drift gains may not transfer to an SE(3) estimator.
3. Items 3 and 4, overconfidence of 10 to 40 times in NEES, partly from a demonstrable R error: every innovation based comparison rests on an invalid covariance.

## Reference

[1] P. Geneva, K. Eckenhoff, W. Lee, Y. Yang, G. Huang, "OpenVINS: A research platform for visual inertial estimation", https://udel.edu/~pgeneva/downloads/papers/c10.pdf

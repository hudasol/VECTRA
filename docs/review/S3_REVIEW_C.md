# S3 Review C: realism and relevance

Reviewer focus: field robotics in deserts and planetary analogues. Files read: paper/vectra_paper.tex, paper/numbers.tex, docs/claims_and_limitations.md, configs/e02.yaml, docs/literature/*.md. Sources below were opened by this reviewer.

## Weaknesses

**W1. Rendered data only.** Claim affected: abstract and conclusion that the compass is "a strong heading aid for a desert ground robot whose cameras degrade". Why weak: Unreal scenes lack real sand texture repetition, own shadow, sun flare and auto exposure behaviour that broke tracking in a real Sahara analogue. MADMAX offers 36 experiments, 9.2 km in total, with stereo, IMU and dual antenna RTK ground truth [1]. Test: run the frozen B0 to B3 pipeline on MADMAX stereo and IMU, with the compass simulated from the dual antenna heading and the logged sun position. Expected direction: higher B0 drift at D0, so a larger relative gain for heading aid, but more VO failures than the rendered pilot suggests.

**W2. No second real analogue.** Claim affected: generality across desert terrain. Why weak: one dataset family. The Katwijk beach dataset gives traverses above 1 km with stereo, IMU and wheel odometry, and RTK ground truth [2]. Test: repeat on Katwijk. Expected direction: rankings of B2 and B3 may change, since real VO errors are biased and correlated.

**W3. Trajectories capped at 200 s although longer ones exist.** Claim affected: drift ratio as the primary metric and the stated "practical lesson". Why weak: TartanGround trajectories contain 600 to 8000 samples at 10 Hz [3]; the cap (max_frames: 2000) discards the regime where heading error dominates position error. Test: rerun the held out split without the cap, reporting drift against distance. Expected direction: the gap between B0 and the compass systems grows roughly with distance; the B1 noon failure becomes more damaging.

**W4. No km scale or homing task.** Claim affected: the ant motivation and relevance to a GNSS denied mission. Why weak: no outbound and return, no home vector error, no window crossing. A 200 s run starting at 12:30 sits wholly inside the 64 minute window, so the transition into and out of blindness is never tested. Test: concatenate trajectories into 1 to 2 hour missions starting at 10:30 on 21 June and score homing error. Expected direction: all systems degrade; gated schemes may lock out after the window, as already seen under cloud.

**W5. No wheel odometry baseline.** Claim affected: that the compass is the relevant aid when vision degrades. Why weak: any wheeled rover carries encoders; Katwijk provides them [2]. A filter with wheel speed would bound translation drift at D4 independently of vision. Test: simulate encoder speed with slip noise proportional to slope and add B0w and B3w. Expected direction: the compass benefit on drift shrinks at D3 and D4; on heading it stays.

**W6. No magnetometer or sun sensor comparator.** Claim affected: contribution (i), that a zenith compass "needs another heading source around summer noon", stated but not evaluated. Why weak: the paper cannot say whether the polarisation compass is preferable to a cheap calibrated magnetometer, which has no noon window. Test: add a magnetometer model with hard iron bias and motor disturbance epochs, and a sun sensor model, each with the same weighting schemes. Expected direction: a magnetometer dominates at summer noon; a sun azimuth sensor shares the noon failure.

**W7. Zenith only sensor.** Claim affected: the 89 day, 65 minute blind window. Why weak: the window is a property of a single zenith pixel, not of skylight. Full sky imagers read the e vector pattern away from the zenith. Test: model a 60 degree field of view polarimeter fitting the Rayleigh pattern, and recompute the window. Expected direction: the window narrows substantially; the headline "never fuse with a fixed weight" weakens.

**W8. No platform tilt on dunes.** Claim affected: compass noise floor of 0.5 degrees and all heading results. Why weak: the filter is planar and the compass error has no tilt term. Tilt errors grow with tilt and solar altitude [4], so they are largest exactly in summer near noon. Test: take roll and pitch from the TartanGround ground truth (or MADMAX), inject tilt induced error in the compass, and run B3 with and without tilt compensation. Expected direction: B1 and B1g degrade first; B3 degrades because DoP does not signal tilt error.

**W9. Sky conditions not tied to climatology.** Claim affected: the 48 scenario design and the June results averaged equally over clear, haze, dust and cloud. Why weak: over the UAE the aerosol optical depth peaks in May to August (0.5 to 0.9) and dust is the dominant aerosol in spring and summer [5]. The blind window and the dust season coincide; clear June noon is not representative. Test: weight scenarios by monthly AERONET frequencies at a UAE site. Expected direction: compass benefit in June falls; differences between B2 and B3 under dust gain weight.

**W10. Image dust and sky dust are independent.** Claim affected: fusion results at D3 and D4. Why weak: D4 sets visibility to 20 m, yet it is crossed with a clear sky DoP factor of 1.0. Physically, such dust collapses sky DoP. Test: couple the sky DoP factor to the visibility of the level. Expected direction: compass benefit at D4 shrinks sharply; B3 tends to B0.

**W11. Single date per season and scene lighting mismatch.** Claim affected: the yearly window and time of day results. Why weak: only 21 June and 21 December are run; rendered sun position does not match the compass sun, so glare and shadow are not consistent with heading. Test: add May and August dates at the edges of the window; render or select scenes whose sun matches. Expected direction: shorter windows at the edges; small change to rankings.

**W12. Compass error model matches B3 and has no bias.** Claim affected: H2 and contribution (iii). Why weak: B3 uses the generating noise law; Study 1 showed a drifting bias defeats every heading aid. Test: add bias random walk and miscalibrated d_max in the compass only. Expected direction: B3 advantage over B1g shrinks or reverses.

## Three most damaging, ranked

1. W10 with W9: the physically impossible pairing of severe image dust with a clear polarised sky, during the season when dust is most frequent, inflates the compass benefit at exactly the levels used as the headline.
2. W3 with W4: truncating available longer trajectories to 200 s and omitting a homing task leaves the claimed relevance to GNSS denied desert missions untested.
3. W7 with W8: the blind window and noise floor rest on a zenith only, untilted sensor, so the central sky model result may not transfer to a real rover on dunes.

## Sources opened

[1] DLR, MADMAX data set page: https://www.dlr.de/en/rm/research/publications-and-downloads/datasets/marokko-navigations-tests
[2] ESA, Katwijk beach planetary rover dataset: https://robotics.estec.esa.int/datasets/?p=2
[3] Patel et al., TartanGround, arXiv:2505.10696: https://arxiv.org/pdf/2505.10696
[4] Liang et al., influence of sensor tilts, arXiv:2007.08987: https://arxiv.org/pdf/2007.08987
[5] Shalaby, Rappenglueck and Eltahir, climatology of dust aerosol over the Arabian Peninsula, ACPD 2015: https://acp.copernicus.org/preprints/15/1523/2015/acpd-15-1523-2015.pdf

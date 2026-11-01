# VECTRA: one page summary for faculty review

Updated 2026-11-01. Prepared by Huda Mueen for Dr. Rajesh Subramanian and Dr. Narina Thakur.

## Project

We are studying whether a compass like heading cue, in the manner of desert ant navigation, can reduce position drift of a ground rover when its camera becomes unreliable and satellite positioning is not available. The first stage is a simulation study on public data with a synthetic heading cue.

## Plan

1. Foundation (this week): repository, charter, registers, protocol draft, baseline feasibility note.
2. Pilot: set degradation and heading parameters on a pilot split only.
3. Freeze the protocol, then run experiment E01 on held out trajectories with three systems: visual inertial only, heading aided with fixed noise, reliability aware heading fusion.
4. Report all results, including negative ones.

## Status on 2026-11-01

- Done: repository, charter, registers, protocol v0 and the frozen protocol v0.1 (tag protocol-v0.1-frozen), a tested simulation of a planar rover with four estimators (no heading, fixed noise heading, fixed noise heading with a gate, covariance matching heading), a pilot, a held out run of 4,800 runs and a sensitivity grid of 13,440 runs.
- Chosen in advance: primary metric is end point drift ratio (final position error divided by path length).
- Main finding on the simulation: a heading cue lowers drift from the third degradation level onward. The reliability aware variant beats the plain fixed noise cue, but not a fixed noise cue with a simple gate. The sensitivity grid shows where this changes.
- Not done: no image based experiment, no TartanGround run, no real sensor. A draft paper exists. Novelty is judged narrow, and no new estimator is claimed.

## Proposed recommendation

Build a transparent planar estimator first so the comparison can start without external blockers, and add OpenVINS as a reference baseline once its inputs (IMU rate, calibration) and the laptop environment test are confirmed. This is a proposal pending the inputs listed above.

## Open risks

1. TartanGround licence and IMU details are not stated on its official page or in its paper.
2. The heading cue is synthetic, so conclusions cannot be extended to real sensors.
3. The novelty finding rests on the 14 opened works of 48 screened.
4. The OpenVINS route has not been tested on the lead author's machine. The simulation did not use it.

## Requested from faculty

Review of the frozen protocol v0.1, the results register and the draft paper, and agreement on the next stage.

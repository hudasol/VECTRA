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

- Study 1 (surrogate simulation, protocol v0.1): done. A heading cue helps once vision degrades; innovation based adaptation did not beat a simple gate.
- Study 2 (rendered TartanGround desert scenes, simulated sky compass, protocol v0.2): done on 34 held out trajectories. The compass cuts heading error by about an order of magnitude. A fixed weight compass fails around summer noon, when the sun is near the zenith over Abu Dhabi; weighting by the measured degree of polarisation beats a gated fixed weight, and covariance matching is slightly better overall.
- Manuscript: paper/vectra_paper.pdf, IEEE conference format, with every number generated from the results files.
- Not done: no real polarisation sensor, no field test, trajectories of at most 200 s.

## Proposed recommendation

Build a transparent planar estimator first so the comparison can start without external blockers, and add OpenVINS as a reference baseline once its inputs (IMU rate, calibration) and the laptop environment test are confirmed. This is a proposal pending the inputs listed above.

## Open risks

1. TartanGround licence and IMU details are not stated on its official page or in its paper.
2. The heading cue is synthetic, so conclusions cannot be extended to real sensors.
3. The novelty finding rests on the 14 opened works of 48 screened.
4. The OpenVINS route has not been tested on the lead author's machine. The simulation did not use it.

## Requested from faculty

Review of the frozen protocol v0.1, the results register and the draft paper, and agreement on the next stage.

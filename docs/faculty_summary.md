# VECTRA: one page summary for faculty review

Draft, 2026-10-20. Prepared by Huda Mueen for Dr. Rajesh Subramanian and Dr. Narina Thakur.

## Project

We are studying whether a compass like heading cue, in the manner of desert ant navigation, can reduce position drift of a ground rover when its camera becomes unreliable and satellite positioning is not available. The first stage is a simulation study on public data with a synthetic heading cue.

## Plan

1. Foundation (this week): repository, charter, registers, protocol draft, baseline feasibility note.
2. Pilot: set degradation and heading parameters on a pilot split only.
3. Freeze the protocol, then run experiment E01 on held out trajectories with three systems: visual inertial only, heading aided with fixed noise, reliability aware heading fusion.
4. Report all results, including negative ones.

## Status on 2026-10-20

- Done: repository with 11 documents in docs/, a README, a citation file and three configuration files, protocol draft v0, feasibility note.
- Chosen in advance: primary metric is end point drift ratio (final position error divided by path length), with the reason written in the protocol.
- Not done: no experiment, no baseline run, no novelty claim. The dataset check and the novelty audit are in progress with the student authors.

## Proposed recommendation

Build a transparent planar estimator first so the comparison can start without external blockers, and add OpenVINS as a reference baseline once its inputs (IMU rate, calibration) and the laptop environment test are confirmed. This is a proposal pending the inputs listed above.

## Open risks

1. TartanGround licence and IMU rate are not stated on its official page.
2. The heading cue is synthetic, so conclusions cannot be extended to real sensors.
3. The novelty of the gap is unverified until the audit returns.
4. The OpenVINS route has not been tested on the lead author's machine.

## Requested from faculty

Review of the protocol draft and agreement on a protocol review date (proposed: Wednesday 28 October 2026).

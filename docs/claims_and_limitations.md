# Claims and limitations

## Claims we may currently make

Statements about the simulation study E01 at the simulation tier only, each tied to a row in docs/results_register.md (R-002 and R-003): drift of the four systems under levels D0 to D4, the preregistered paired tests, the NEES and coverage values, and the sensitivity grid. Statements about what the public documentation of OpenVINS and TartanGround says (see docs/evidence_register.md and docs/source_log.md).

## Claims we may make after E01, if the evidence supports them

Each must be stated at the simulation tier and must cite a row in docs/results_register.md. After E01 the evidence does not support a claim that reliability weighting beats a gated fixed noise cue.

## Claims we may not make

- That a method works on a real robot.
- That a synthetic heading cue represents a real polarisation or magnetic sensor.
- That any organisation endorses or uses this work.
- Anything about performance before the protocol is frozen and the runs are done.

## Known limitations (current)

1. Simulation only in the first experiment.
2. The heading cue is derived from ground truth plus a noise model, so it is idealised.
3. TartanGround licence and IMU rate are not stated on the official page (open questions).
4. The feasibility check was done from documentation. OpenVINS has not been run.
5. The visual front end in E01 is a measurement level surrogate. There are no images.
6. In the simulation all filters are inconsistent (NEES far above 2).
7. The TartanAir documentation describes a noise free IMU derived from the pose. If TartanGround does the same, an image stage must add an IMU noise model.
8. A drifting cue bias defeated every heading aided system in the sensitivity grid.

# Novelty register

Purpose: list the closest prior work and state, for each, what it already does and what this project would add. No novelty claim is made until Maryam's audit (task M1) is complete and the register is filled.

| ID | Prior work | What it does | Overlap with VECTRA | Remaining difference | Opened? |
| --- | --- | --- | --- | --- | --- |
| N-001 | Sun-BCNN, arXiv 1609.05993 | Infers a sun direction from a single image and feeds it as a global orientation measurement into stereo visual odometry. Monte Carlo dropout gives an uncertainty used to weight the measurement. Reports up to 42 percent lower translational error on KITTI | High. A heading like cue with a per measurement uncertainty weighting inside visual odometry | Cue comes from a learned image model, not a compass. No IMU in the filter as read. No graded degradation protocol or consistency metric as read | Yes, abstract level |
| N-002 | Joshi and Rekleitis, arXiv 2409.09904 | Adds magnetometer relative orientation residuals to OKVIS style visual inertial odometry for underwater caves. Reduces yaw and ATE | High. A heading cue inside visual inertial odometry | Fixed calibration, no adaptation to cue reliability. Cave data, not a graded degradation study | Yes, summary |
| N-003 | Polarisation compass with MEMS INS, PMC10892783 | Loosely coupled Kalman filter, variational Bayes estimates time varying measurement noise, neural network bridges compass loss | High for the adaptive weighting idea | No camera. Not a visual degradation study | Yes, summary |
| N-004 | MIL-LC, arXiv 2606.25796 | Magnetometers with LiDAR and IMU. Scales magnetic residuals by LiDAR reliability, Huber kernel, degeneracy handling | Medium to high. Reliability dependent weighting of a heading related cue | LiDAR not camera. Indoor magnetic maps | Yes, summary |
| N-005 | Choi et al., arXiv 2510.01648 | Learns per measurement reliability in visual inertial optimisation. Lower error than fixed uncertainty on EuRoC | Medium. Reliability aware weighting inside visual inertial estimation | Weights visual landmarks, no heading aid. No graded degradation shown in the abstract | Yes, abstract |
| N-006 | Self supervised differentiable Kalman filter, arXiv 2203.07207 | Learned heteroscedastic covariance for the visual measurement, tested with synthetic brightness, blur and noise corruptions on EuRoC | Medium. Reliability aware weighting and synthetic degradation | No heading aid. No NEES or consistency metric | Yes, summary |
| N-007 | Adaptive covariance hybrid ESKF/UKF, arXiv 2512.17505 | Visual confidence score from entropy, intensity variation and blur scales the visual noise | Medium. Image quality scores driving the noise | No heading aid. UAV, EuRoC | Yes, abstract |
| N-008 | Failure or Drift?, arXiv 2608.30690 | Monocular SLAM under 115 synthetic corruption variants with five severity levels, and real conditions. Separates failure from drift | Medium. Graded degradation evaluation | Monocular, no IMU, no heading aid, driving data | Yes, summary |
| N-009 | Subterranean VIO benchmark, arXiv 2609.18628 | Four VIO systems under graded IMU, extrinsic, intrinsic and occlusion degradation, 11 levels | Medium. Graded degradation of visual inertial systems | Degrades calibration and occlusion, not image quality. No heading aid. No consistency metric | Yes, summary |
| N-010 | MSCEKF-MIO, arXiv 2505.12634 | Magnetometer array aided inertial odometry, magnetic constraint cuts heading error from 9.8 to 1.8 degrees | Low to medium. Heading constraint in a filter | No camera. Indoor | Yes, summary |
| N-011 | AntBot, Science Robotics 2019 (press release read) | Hexapod with a polarised light compass and optic flow sensor, homing to about 1 cm after 14 m outdoors | Medium for the biological premise | Hardware robot, no visual inertial baseline, sunlit conditions. Original paper not opened | Press release only |
| N-012 | Emulating insect brains, arXiv 2401.00473 | Path integration network on BrainScaleS 2, 1.0 percent return error after optimisation | Low. Same biological premise | Neuromorphic implementation in a virtual agent | Yes, summary |
| N-013 | Home vector direction learning, arXiv 2405.03827 | CNN learns home direction, odometry plus learned correction, assumes a heading source | Low. Assumes the heading cue we study | Visual homing, not drift reduction of estimator | Yes, summary |
| N-014 | Insect navigation as reinforcement learning, arXiv 2406.01501 | Survey style framework on insect navigation | Low | No fusion design | Yes, abstract |
| N-015 | AMO-HEAD, arXiv 2510.10979 | Adaptive heading estimation for UAVs. Inflates the magnetometer noise in two steps from a chi square test of the residual. Inflation factors tuned on a validation set from the test environment. No significance test found in the text | High for the adaptive weighting of a heading cue | Magnetometer and inertial only, no camera, no graded visual degradation, no consistency metric | Yes, full text |

Not opened, so no claim made about them: Stone et al. 2017 (bee path integration model), Dupeyroux et al. IROS 2017, QA-MSCKF, and the 34 works listed in docs/novelty_screening_log.md.

## Candidate gap (hypothesis, not a finding)

Reliability aware weighting of a heading cue inside a visual inertial filter, evaluated under controlled and graded visual degradation on a ground rover with a documented, reproducible protocol. This statement is a hypothesis to be tested by the audit. It may turn out to be already covered.

## Rule

A novelty claim requires a row for each of the closest works we opened, with the difference stated in one sentence.

## Audit result (task M1, reviewed by the lead author)

Status: proposed, not decided. The author who owns task M1 is asked to confirm or correct it.

Method: 48 works were screened (docs/novelty_screening_log.md). 14 were opened and 34 were not. A claim is made only about opened works.

Finding. No opened work combines all three of these: (a) a heading cue inside a visual inertial filter, (b) weighting of that cue by its estimated reliability, and (c) a graded visual degradation protocol with a fixed primary metric, paired statistics and a consistency metric. Parts (a) and (b) are covered separately by N-001, N-002, N-003, N-004 and N-015. Part (c) is covered separately by N-008 and N-009.

Narrowed gap statement: a preregistered, controlled comparison of a heading cue with and without reliability weighting, inside a visual inertial filter, under graded visual degradation, reported with drift ratio, paired tests and NEES.

What this does not support: a claim of a new estimator. Innovation based weighting of a heading cue is established practice (N-015, and the covariance matching literature in docs/literature/B_estimation.md). The contribution is the controlled evaluation.

Protocol changes proposed by the audit, and where they went: add a fixed noise baseline with an outlier gate (B1g) so that adaptation can be separated from outlier rejection (done in docs/experiment_protocol_v0.1.md); report NEES and coverage (done); tune nothing on the held out split (done).

Limit of the audit: 34 screened works were not opened, and a gap in the opened set does not prove a gap in the literature.

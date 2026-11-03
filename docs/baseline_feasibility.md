# Baseline feasibility note

Date: 2026-10-20. Author: Huda Mueen. Status: documentation based. No baseline has been run by us yet, and nothing in this note is a performance finding.

## 1. What OpenVINS requires (from its documentation, evidence E-001)

Read through a fetch tool summary; to be re-read directly before any figure is quoted.

- Input: the supported datasets are distributed as ROS bags (EuRoC, TUM VI, RPNG AR Table, UZH-FPV, KAIST VIO). KAIST Urban needs conversion to a bag first. A ROS 2 route exists but, for one dataset, goes through ROS 1 conversion first.
- Calibration: Kalibr style files are provided for some datasets. OpenVINS ships one configuration folder per supported dataset, which is the model for any new dataset we add.
- Time sync: for datasets that are not synchronised, online time offset estimation is recommended.
- Install routes: native ROS install, and a Docker route.
- Ground truth: used for evaluation by separate scripts, with logs exported as csv.

Not found in the pages we read: a statement of the minimum IMU rate. This must be confirmed on the page directly.

## 2. What TartanGround provides (evidence E-002, E-003)

- 63 environments, 878 trajectories (440 omni, 198 differential drive, 240 legged); 600 to 8,000 samples per trajectory.
- Stereo six camera rig, 90 degree field of view each, 640 by 640 pixels, collected at 10 Hz.
- Ground truth 6 DOF poses, depth, segmentation, 32 beam simulated LiDAR, IMU data.
- IMU rate: not stated. Licence: not stated on the official page.
- Raw download is zip archives with a python toolkit. ROS bags are provided for the legged (anymal) trajectories only.
- Size is about 15 to 16 TB in total, so we must use subsets.

## 3. Can TartanGround be converted for OpenVINS?

Likely in principle, with an adapter that writes a ROS bag with image and IMU topics plus a Kalibr style calibration file. Items we must confirm before this is a plan:

1. IMU rate, noise model and whether the IMU is simulated with noise at all (needed for the IMU noise parameters in the config).
2. Camera to IMU extrinsics (the transform OpenVINS needs).
3. Camera model. Assuming an ideal pinhole with a 90 degree field of view and 640 pixel width, the focal length would be 320 pixels (computed as 320 divided by tan 45 degrees). This is an assumption and must be checked against the dataset metadata.
4. Whether the 10 Hz image rate is workable for the tracking front end (risk, untested).
5. Which robot type (differential drive is the closest to a rover) has IMU data in the non bag format and how to read it.

## 4. Can it run on the lead author's laptop?

Not tested. The workspace used to prepare this note is a Linux VM and not her Windows laptop, so we cannot claim anything about her machine. Tests for her to run, recording every failing step in docs/baseline_feasibility_log.md (to create):

1. Check Windows version, free disk space, virtualisation enabled in firmware.
2. Install WSL2 with Ubuntu (free). Record the version and any error.
3. Option A, Docker: install Docker Desktop or run Docker inside WSL2, pull the OpenVINS image per the Docker page, and run the EuRoC example on one sequence. Record time and memory.
4. Option B, native: install ROS in WSL2 and build OpenVINS following the install page. Record the failing steps.
5. Run one supported dataset (EuRoC, small sequence) and confirm that a trajectory csv is produced.
Pass criterion: one supported sequence runs to completion and produces a trajectory file. Anything else is recorded as a failure with the error text.

## 5. Route comparison

| | (a) OpenVINS plus adapter plus custom heading update | (b) Transparent planar estimator prototype |
| --- | --- | --- |
| What it is | Existing filter based visual inertial system; we add a bag adapter and modify the update step for B1 and B2 | Our own small estimator (planar state, speed and yaw rate propagation, visual displacement input, heading update) |
| Effort (our estimate, not measured) | High: environment setup, adapter, calibration, C++ modification | Medium: pure python, but we write and validate the estimator |
| Risk | Environment failures on Windows; unknown IMU rate; calibration mismatch; tracking at 10 Hz; C++ changes | Weaker credibility as a "visual inertial" baseline; risk of an unfair or weak B0 |
| Fairness of B0 | Strong: B0 is a published, widely used system | Must be argued and validated; reviewers may see B0 as a straw man |
| Transparency and reproducibility | Heavier dependency stack | Light, fully inspectable, easy to seed and test |
| Fit to a single rover on a laptop | Doubtful until section 4 passes | Good |

## 6. Recommendation (proposed, for discussion; not a finding)

Start with route (b) to get a working, tested comparison of B0, B1 and B2 inside the first two weeks, because it has no external blockers and lets us validate the protocol, the metrics and the degradation code. In parallel, run the section 4 tests and the dataset audit check of the IMU rate and calibration. If both pass, add OpenVINS as an external reference baseline (route a) and report B0 against it, so that route (b) is not left as an unvalidated baseline. If they fail, report route (b) with its limitation stated openly.

Decision owner: lead author.

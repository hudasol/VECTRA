# Experiment protocol, E02 image based study, version 0.2

Status: FROZEN on 2026-11-01 before any held out trajectory was processed. Freeze point: the commit that sets this status, tagged protocol-v0.2-frozen. Deviations after the freeze are logged in docs/results_register.md.

## 1. Why E02 exists

E01 (protocol v0.1) used a surrogate visual front end and a synthetic heading cue. Its three main limits were: no images, a cue whose reliability had no physical cause, and a filter that was overconfident. E02 replaces the surrogate with stereo visual odometry on rendered desert scenes from TartanGround, replaces the synthetic cue with a zenith polarisation compass driven by the sun position over Abu Dhabi, and adds one estimator that takes its cue noise from the measured degree of polarisation. E01 stays frozen and is reported as it is.

## 2. Data

TartanGround, Hugging Face repository theairlabcmu/TartanGround, licence CC BY 4.0 as stated on the dataset card. The dataset was reachable from the analysis environment through the Hugging Face host, which was not the case when protocol v0.1 was written.

- Pilot split: WesternDesertTown (6 omni wheeled trajectories).
- Held out split: DesertGasStation, MiddleEast (omni wheeled and differential), EndofTheWorld.
- Excluded: DesertGasStation/Data_omni/P0000. Its frames were used to debug the visual odometry code before the pilot. No parameter was set from it, but it is excluded so the held out split is untouched.
- Per trajectory: front stereo pair (left and right), left depth, IMU (100 Hz), poses. The first 2,000 frames (200 s) at most.
- Images are converted to 8 bit grayscale and resized from 640 by 640 to 320 by 320 pixels.

## 3. Image degradation (levels D0 to D4)

Applied in linear intensity in this order: dust haze by Koschmieder attenuation along the rendered depth with visibility V (transmission exp(-3.912 r / V)) and airlight; veiling glare with one glare centre per sequence; auto exposure that lengthens the exposure time up to a cap and then loses light; motion blur from the yaw rate and exposure time; photon and read noise; gamma encoding and 8 bit quantisation; Markov frame drops. The same glare and haze apply to both cameras; noise is independent. Parameters are in configs/e02.yaml. Level values are set on the pilot split (Section 9).

## 4. Visual odometry

Stereo visual odometry with KLT feature tracking, forward backward check, stereo triangulation from left right KLT disparity and PnP with RANSAC. Output per frame: body velocity (forward, right) and yaw rate, or a failure flag when fewer than 15 inliers remain. No loop closure and no mapping.

## 5. Zenith polarisation compass

- Sun position: NOAA General Solar Position Calculations, Abu Dhabi (24.4539 N, 54.3773 E, UTC+4).
- Zenith degree of linear polarisation: Rayleigh single scattering, d = d_max sin^2(gamma) / (1 + cos^2(gamma)), gamma the solar zenith angle, d_max = 0.6.
- Zenith e-vector perpendicular to the solar meridian, so the compass measures heading modulo 180 degrees. The filter resolves the ambiguity with its prior.
- Angle noise: sigma^2 = floor^2 + (c / d)^2 with floor 0.5 degrees and c = 0.05 degrees. The sensor also reports a measured degree of polarisation with noise 0.002.
- Sky conditions: clear (d scale 1.0), haze (0.6), dust (0.3), broken cloud (clear sky with Markov cloud epochs over the zenith covering 35 percent of the time, mean 30 s, d scaled by 0.05 to 0.3 and an extra angle error of 10 degrees during an epoch).
- Scenarios: dates 21 June and 21 December 2026; start times 07:30, 09:30, 11:45, 12:30, 14:30, 16:30; four sky conditions. 48 scenarios, each with 2 filter seeds, on every visual odometry run.

All compass and sky parameters are modelling assumptions. They are not fitted to any data. The sources that motivate each are listed in the paper.

## 6. Systems

All share one 8 state extended Kalman filter (position, yaw, world velocity, gyro bias, two accelerometer biases), driven by the IMU at 100 Hz with added noise, and updated by visual odometry at 10 Hz (three measurements). A visual update whose NIS exceeds the chi square value 11.34 is kept with its noise inflated so that the NIS equals that value; this bounds outlier influence and prevents lock out. The start pose is known; the initial velocity has a variance of 4 (m/s) squared so that the first visual update sets it. They differ in the compass update.

| ID | Compass update |
| --- | --- |
| B0 | None |
| B1 | Fixed noise 1 degree, no gate |
| B1g | Fixed noise 1 degree, chi square gate 6.63 |
| B2 | Covariance matching over W = 3 innovations, floor 1 degree, no gate (as E01) |
| B3 | Noise from the measured degree of polarisation using the sensor model, chi square gate 6.63 |
| B3a | B3 plus a visual noise scale from the mean visual NIS over the last 20 updates (never below 1) |

## 7. Metrics

Primary: drift ratio (final position error divided by path length, percent, no alignment, start pose known). Secondary: position RMSE, ATE after SE(2) alignment, relative error over 10 s, heading RMSE, failure rate (drift above 10 percent), position NEES (time averaged, median over runs) and mean 95 percent coverage.

## 8. Statistics

Unit of analysis: the trajectory. For each trajectory, level and system, each metric is averaged over the degradation seed, the 48 sky scenarios and the 2 filter seeds (96 runs).

Each family uses paired Wilcoxon signed rank tests, the median paired difference with 10,000 bootstrap resamples and the paired dominance delta, with Holm correction within the family.

- Family F1 (primary, 15 tests): drift ratio, B3 against B1g, B2 and B0 at each level.
- Family F2 (primary for heading, 15 tests): heading RMSE, the same pairs. The compass acts on heading first, and E02 trajectories are at most 200 s, so heading is where an effect should appear first.
- Family F3 (secondary, 10 tests): B3a against B3 on drift ratio and on mean 95 percent coverage.

Descriptive only: drift and heading error by local start time and sky condition; visual odometry error and failure by level; compass updates accepted and rejected.

Hypotheses stated before the run:
- H1: B3 has a lower drift ratio and heading RMSE than B0 at D2 to D4.
- H2: B3 has a lower heading RMSE than B1g. The reason to expect it is the near noon June scenarios, where the compass noise exceeds the fixed 1 degree by orders of magnitude.
- H3: B3 is not worse than B2.
- H4: B3a has a lower drift ratio and a higher coverage than B3.
Any of these may be rejected.

## 9. Pilot decisions (pilot split only, results/e02_pilot*.csv)

1. Levels. The drafted levels were kept after one pilot check: the median visual odometry success fraction falls from 0.92 (D0) to 0.66, 0.62, 0.52 and 0.37 (D4), and the robust yaw rate error rises from 0.005 to 0.027 rad/s, so the levels are graded and D4 is not saturated. Values: gain 1, 0.5, 0.2, 0.07, 0.025; visibility none, 1000, 200, 60, 20 m; glare 0, 0.02, 0.05, 0.10, 0.20; frame drops 0, 2, 5, 10, 20 percent (mean burst 0.5 s).
2. Nominal visual noise: 1.4826 times the median absolute deviation of the D0 errors pooled over the pilot trajectories: 0.0548 m/s forward, 0.041 m/s right, 0.0049 rad/s yaw rate.
3. B3a window: candidates 10, 20 and 50 visual updates; rule: lowest mean over levels of the median drift ratio of B3a, the smallest if candidates lie within 1 percent of the best. Means were 6.77, 6.92 and 6.96 percent, so the window is 10.
4. Degradation seeds: one per level on the held out split (two were used on the first two pilot trajectories). Variation is carried by 48 sky scenarios and 2 filter seeds per visual odometry run.
5. Fixes made during the pilot, before any held out run: the initial velocity variance was raised to 4 (m/s) squared after the pilot showed a wrong initial velocity; the visual update was changed from rejection to bounded inflation after the pilot showed filter lock out with rejection.

## 10. Threats to validity

Rendered scenes, not real camera images. The scene lighting does not match the sun position of the compass scenario. The compass is simulated. The haze model uses a single airlight and the left depth for both cameras. The trajectories are short (up to 200 s). Planar filter on mostly planar motion.

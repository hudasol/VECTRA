# Experiment protocol, Study 3 (E03), version 0.3

Status: FROZEN before any estimator was run on the confirmation split. Freeze point: the commit that sets this status, tagged protocol-v0.3-frozen. Protocols v0.1 and v0.2 stay frozen and unchanged; Study 1 and Study 2 results are not edited. Deviations after the freeze are logged in docs/DECISIONS_S3.md and in the paper.

## 1. Why Study 3 exists

The Study 3 red team (docs/review/S3_REVIEW_A.md to D.md, merged in docs/STUDY3_RESPONSE.md) found that the Study 2 headline rests on: a single scattering sky with assumed sky factors; a compass with white error only (no bias, no tilt); a B3 estimator that uses the very law that generates the simulated compass noise; a sky condition that is independent of the image degradation, so a 20 m dust image can meet a clear polarised sky; an overconfident filter; 34 trajectories from three environments with one degradation seed; and held out data that have since been inspected. Study 3 changes the simulator, the estimators, the data split and the analysis so that each of these can fail.

## 2. Data and splits (RENDERED images, SIMULATED degradation)

TartanGround (CC BY 4.0), first 2,000 frames (200 s) per trajectory, 320 by 320 grayscale stereo, frozen Study 2 degradation and visual odometry code.

- Pilot (fitting only): WesternDesertTown, 6 trajectories, Study 2 VO files.
- Development (selection only): DesertGasStation, MiddleEast, EndofTheWorld, 34 trajectories, Study 2 VO files, degradation seed 0. These data were inspected in Study 2, so they are used only to choose, never to confirm.
- Confirmation (run once): Ruins, AncientTowns and HQWesternSaloon (Data_omni), 15 trajectories, chosen by environment name before any image was viewed and never processed before Study 3. Three degradation seeds per level D1 to D4 (fallback from five, compute), one at D0. Terrain roll and pitch come from the rendered poses.
- Non desert check (descriptive): Gascola (Data_omni), processed with the same pipeline if time allows.

## 3. Sky and compass model v2 (SIMULATED)

- Vector Monte Carlo radiative transfer (src/vectra/sky_rt.py): Rayleigh (optical depth 0.17, about 470 nm) plus one aerosol (Henyey Greenstein g 0.7, single scattering albedo 0.92, Rayleigh shaped polarisation of maximum 0.2), Lambertian ground albedo 0.3, full multiple scattering, peel off estimate at the zenith and at twelve points at 60 degrees elevation. Validated against the analytic single scattering law and compared with the measured desert band given in Section 10.
- MEASURED check (before the freeze): one day of open full sky polarisation images from Marseille (Poughon et al. 2024, CC BY-SA 4.0). Clear sky zenith DoP at solar zenith 49 to 83 degrees fits the Study 2 law with d_max 0.613, about 15 percent above the radiative transfer model at low aerosol. A measured anchored table (clear sky law from the measurement, aerosol and dust attenuation from radiative transfer) is therefore run as a secondary compass model; the radiative transfer table stays primary.
- Aerosol: NASA POWER monthly aerosol optical depth at 550 nm for Abu Dhabi (MERRA 2 based), times a lognormal day factor (sigma 0.3). AERONET was not reachable from the analysis environment.
- Dust coupling (primary): the image visibility V of a level adds a near ground dust layer of optical depth 3.912 H / V with H = 100 m (assumed), so a D4 image (V = 20 m) comes with a dust sky. The uncoupled Study 2 pairing is a secondary analysis.
- Cloud: each scenario is cloudy with the POWER monthly cloud amount as probability; within a cloudy scenario the Study 2 Markov cloud epochs apply.
- Error terms: point noise from the frozen Study 2 law (floor 0.5 degrees, c 0.05 degrees) on the radiative transfer DoP; heading bias (initial 1 degree, random walk 0.01 degrees per root second); tilt error computed exactly from the sun geometry and the platform roll and pitch (rendered terrain on the confirmation split, Gauss Markov 2 degrees with 20 s correlation on the development split, assumed); cloud angle error.
- The filter does not know the radiative transfer DoP, the bias, the tilt or the cloud term: its per sample noise estimate uses the measured zenith DoP and the frozen law only. This removes the Study 2 match between simulator and B3.
- Geometries: zenith point; zenith plus ring (heading information from the Cramer Rao bound of all thirteen points); sun direction sensor (0.5 degrees divided by the sine of the solar zenith, bias 0.3 degrees, assumed); magnetometer (2 degrees white, 3 degrees uncalibrated bias, slow disturbance, ASSUMED).
- Scenarios: 21 March, 21 June, 21 September, 21 December; start 09:30, 11:45, 12:30, 14:30 local time; 16 scenarios, each with its own aerosol and cloud draw. Equal weight on the four dates gives an annual mix.

## 4. Systems

One ten state filter (src/vectra/filter3.py): the Study 2 eight states plus a compass bias and a visual speed scale state, which are inert (zero variance) unless a system uses them.

| ID | Compass and odometry |
| --- | --- |
| B0 | No compass, stereo VO |
| B1 | Fixed 1 degree, no gate |
| B1g | Fixed 1 degree, gate 6.63 |
| B2 | Covariance matching, W = 3, floor 1 degree |
| B3 | Per sample noise from measured DoP, gate 6.63 |
| B4 | Per sample noise as the floor of covariance matching, no gate |
| B5 | Two mode (good, bad 45 degrees) moment matched IMM approximation, prior bad 0.1 |
| B6 | Huber weighting (k = 1.345) of the per sample noise |
| B7 | B3 with a compass bias state |
| B8 | Learned reliability: logistic regression on log measured DoP, cosine of solar zenith and the gyro consistency of successive compass readings, fitted on the pilot split; noise divided by (1 - p), reject if p > 0.9 |
| B3L | B3 with a lock out rule: after 25 consecutive gated samples the next is used with bounded inflation |
| B3C | B3 with the calibrated noise model: Gauss Markov visual speed scale state and the averaged gyro variance in the bias measurement, both fitted on the pilot split (results/e03/pilot_fit.json) |
| B3R, B4R | B3 and B4 with the zenith plus ring geometry |
| SUN, MAG | B3 style update with the sun sensor or the magnetometer |
| W0, W3, W4R | Simulated wheel odometry (scale 2 percent, slip epochs) instead of VO, with no compass, the zenith compass (B3) or the ring compass (B4) |

Selection on the development split (before the confirmation run): S is the system among B4 to B8 with the lowest mean over D0, D2 and D4 of the median trajectory heading RMSE. Ties within 0.05 degrees go to the simpler system in the order B4, B6, B5, B7, B8.

## 5. Metrics

Primary: heading RMSE (degrees). Co primary for odometry hypotheses: drift ratio (percent). Secondary: position NEES (time averaged), 95 percent coverage, failure rate, gated samples and the longest gated run.

## 6. Analysis

Unit: the trajectory. For each trajectory and system, the metric is averaged over levels D0, D2 and D4 (seeds, scenarios and IMU draws inside each level) unless a hypothesis names a level. Paired differences: median with a two stage cluster bootstrap (environments, then trajectories within environment, 10,000 resamples) and a paired Wilcoxon signed rank p value; Holm over the confirmatory family (H1 to H6). Variance components (environment, trajectory, degradation seed, scenario, IMU draw) from a linear mixed model on log heading RMSE, descriptive. Climatology weighting is built into the scenario design (Section 3).

## 7. Hypotheses (confirmation split, coupled sky)

- H1 (superiority): B3 has a lower heading RMSE than B0.
- H2 (harm): with bias and tilt, the ungated fixed weight B1 has a higher heading RMSE than B0 at D0 (clear images, where the compass dominates).
- H3 (non inferiority): S is not worse than B2 by more than 0.5 degrees heading RMSE (upper bound of the 95 percent cluster bootstrap interval of the median S minus B2 below 0.5).
- H3b (non inferiority, the Study 2 exploratory system): B4 is not worse than B2 by more than 0.5 degrees.
- H4 (geometry): B4R has a lower heading RMSE than B4.
- H5 (wheel odometry plus compass): W3 has a lower drift ratio than B0 at D4.
- H6 (consistency): B3C has a median position NEES in [1, 4] and a mean 95 percent coverage in [0.8, 0.99]. Criterion check, not part of the Holm family.
- H7 (ranking transfer): Kendall tau between the development and confirmation rankings of the VO based systems by median heading RMSE is at least 0.6. Criterion check.

Model results computed before the freeze and therefore not confirmatory: the blind window under radiative transfer, its uncertainty over the aerosol climatology, the geometry that shortens it and the global latitude by day map (experiments/E03/sky_v2.py).

## 8. Secondary and descriptive

Uncoupled sky on the confirmation split and the measured anchored compass model on the confirmation split (each with B0, B1, B1g, B2, B3, B4, S, one IMU draw); level wise results; noon versus morning scenarios; SUN and MAG; non desert check; gate lock out counts; drift decomposition with oracle heading and oracle translation; growth of position error with path length and a SIMULATED kilometre scale extrapolation; an ant style homing task with wheel odometry and compass.

## 9. Fallbacks

Planned size: levels D0 (seed 0), D2 and D4 (seeds 0 to 2), 16 scenarios, two IMU draws (fallback from five, compute: about 0.12 s per filter run on one core), 19 systems. If the confirmation compute still exceeds the budget: degradation seeds 0 and 1 only. Any fallback is logged with the reason.

## 10. Reference values used for comparison only

Measured zenith degree of linear polarisation in a desert under clear sky, as given in the study brief: 24 to 30 percent at 35 degrees solar elevation and about 8 percent at 70 degrees. These values are compared with the model; they are not fitted.

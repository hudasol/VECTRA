# Study 3 decisions (one line each)

- D01: About five hours of the twelve hour window were lost before work began (start 05:47, work 10:41). Budgets are scaled to the remaining six hours; tasks are cut in the order of least evidence per hour, and every cut is logged.
- D02: The frozen draft protocol (experiment_protocol.md, not a frozen version) was edited only to drop a review arrangement; frozen protocols v0.1 and v0.2 were not edited.
- D03: Two internal governance notes were removed from the tree in a new commit; history is not rewritten.
- D04: Tags cannot be pushed through the session proxy; they remain in the local repository.
- D05: Confirmation set = 15 trajectories of three TartanGround environments never processed before (Ruins, AncientTowns, HQWesternSaloon, all Data_omni); Gascola (vegetated off road) is a separate non desert check. Chosen by name before any image was viewed.
- D06: VO preprocessing of the confirmation trajectories started before the protocol freeze; it uses the frozen E02 VO pipeline and no estimator was run or inspected on these data before the freeze.
- D07: Degradation seeds 3 (fallback from 5) and trajectories cut at 2000 frames (200 s) as in E02, because one trajectory costs 7 minutes of VO on one core; km scale behaviour is extrapolated in simulation instead (labelled SIMULATED).
- D08: MADMAX: the official page states that registration is required for the full download list; accounts are not allowed in this study, so no real MADMAX sequence was used. Katwijk page (robotics.estec.esa.int) refused the connection. AERONET (aeronet.gsfc.nasa.gov) refused the connection; NASA POWER (MERRA-2 AOD at 550 nm and cloud amount) was used instead.
- D09: The radiative transfer aerosol uses a simplified phase matrix (Henyey Greenstein intensity, Rayleigh shaped polarisation of maximum 0.2), not a Mie computation; varied in a sensitivity run.
- D10: Zenith AoP sign flips in the tables occur only in cells with DoP below 0.005, where the Monte Carlo AoP is noise; no neutral point flip with usable DoP was found in this plane parallel model. Reported as such.
- D11: The model matches the measured 24 to 30 percent at 35 degrees elevation only at low aerosol (0.26 at AOD 0.15) and is four times below the measured 8 percent at 70 degrees; the measured near sun value exceeds even single scattering Rayleigh (6.2 percent), so the blind window is reported as a bracket between the Study 2 law and the radiative transfer model.
- D12: Compass sun sensor and magnetometer parameters are assumptions with no fitted source (labelled ASSUMED).
- D13: Paper statement checked for review point B12: the values 0.14 to 0.37 degrees are trajectory level medians (family F2) and are correct; the reviewer compared run level medians.

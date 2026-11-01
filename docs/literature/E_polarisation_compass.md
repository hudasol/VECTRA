# E. Polarisation compass: noise weighting, solar elevation, VO fusion, dynamic accuracy, dust

Search date: 2026-11-01. Tools: WebSearch + WebFetch only, free sources.

Reading levels: FULL means the fetch tool read the full article text, or most of it. ABSTRACT means only the abstract or landing page was read. SUMMARY means a press or summary page was read. Every quote below was returned by the fetch tool for the URL listed. The fetch tool returns a model summary of the page, so treat quotes as near verbatim and check them against the PDF before final citation.

---

## Q1. Polarisation compass noise weighted by DoP or another quality index inside a filter

### 1.1 Zhang, Wang, Li, Qiu (2022). Closest prior art for DoP based weighting
- Citation: Zhang, J.; Wang, S.; Li, W.; Qiu, Z. "A Multi-Mode Switching Variational Bayesian Adaptive Kalman Filter Algorithm for the SINS/PNS/GMNS Navigation System of Pelagic Ships." Sensors 2022, 22(9), 3372. DOI 10.3390/s22093372
- URL opened: https://www.mdpi.com/1424-8220/22/9/3372
- Reading level: FULL
- Facts:
  - DoP is used as a credibility measure. An interference factor ς_pol has upper and lower DoP thresholds (Eq. 21), giving three cases.
  - Above the upper threshold: "The weight of polarization navigation is equal to 1" (VBAKF then estimates the noise). Between the thresholds, the noise covariance blends the prior and the online estimate (Eq. 22). At or below the lower threshold, the polarisation system "is judged to be invalid" and is switched out for magnetometer only.
  - Simulation only: a ship at 39 N, 120 E. Multi mode VBAKF heading error is 0.147 deg against 0.293 deg for multi mode KF. No numeric DoP thresholds are given.
- Relevance: this is a piecewise DoP gate and weighting, not a continuous sigma(DoP) law. It does not consider the zenith sun.

### 1.2 Sun et al. (2025). Cites a DoP based noise adaptation (Dou et al.)
- Citation: Sun, Y.; Liu, X.; Liu, X.; Zhao, H.; Wang, C.; Cao, H.; Shen, C. "Variational Bayesian Innovation Saturation Kalman Filter for MEMS-INS/Polarization Compass Integrated Navigation." Micromachines 2025, 16(9), 1036. DOI 10.3390/mi16091036
- URL opened: https://pmc.ncbi.nlm.nih.gov/articles/PMC12472092
- Reading level: FULL (results section truncated)
- Facts:
  - Polarisation compass noise is modelled as Student's t. A VB auxiliary variable is "introduced as an auxiliary variable to dynamically adjust the covariance matrix", and an innovation saturation function with an adaptive boundary is added.
  - In its prior work review it says Dou et al. [26] defined "the degree of polarization ... as a deterministic factor to adaptively adjust the measurement noise matrix". The authors criticise that approach as not tracking noise variation accurately.
  - It also cites Zhao et al. [13] (VB cubature KF plus a residual chi squared outlier detector for INS/PC). Tests were "static and dynamic experiments ... on an unmanned vehicle". Reported dynamic improvements are 76.89% over AKF and 84.45% over ISRAKF; RMS in degrees was not in the fetched text.
  - Solar elevation and zenith are not mentioned.

### 1.3 Bai et al. (2024). Chi square adaptive KF for polarisation sensors
- Citation: Bai, H.; Yang, J.; Hu, P.; Qiu, Z.; Yu, X.; Wang, S.; Chi, X. "An Integrated Navigation System Using IMU/Multidirectional Polarization Sensors/Sun Sensor for Cloudy Environments." IEEE Sensors Journal 24(14), 2024. DOI not printed on the page opened.
- URL opened: https://agri.nais.net.cn/literature/agrinstl/J20241031000873.html
- Reading level: ABSTRACT
- Facts:
  - A chi square based KF is used to "adapt variable measurement noises of the polarization sensors and sun sensor"; an outlier detector selects the best polarisation sensors.
  - Tested in static ground tests and "unmanned aerial vehicle (UAV) flight tests" in cloudy conditions. No numbers in the abstract, and the abstract does not mention DoP.

### 1.4 Zhao et al. (2024). VB noise estimation plus NN bridging when the PC is unreliable
- Citation: Zhao, H.; Shen, C.; Cao, H.; Chen, X.; Wang, C.; Huang, H.; Li, J. "Seamless MEMS-INS/Polarization Compass Navigation Method with Data and Model Dual-Driven Approach." Micromachines 2024, 15(2), 237. DOI 10.3390/mi15020237
- URL opened: https://pmc.ncbi.nlm.nih.gov/articles/PMC10892783
- Reading level: FULL (results section not in the fetched excerpt)
- Facts:
  - Polarisation compass noise is treated as time varying because "the covariance matrix of the noise is usually unknown"; it is estimated by VB.
  - When the polarisation compass heading is abnormal (sky occluded), a neural network predicted heading increment replaces it. DoP is not used in the excerpt.

### 1.5 Ma et al. (2015). DoP as the accuracy indicator of the AoP measurement
- Citation: Ma, T.; Hu, X.; Zhang, L.; Lian, J.; He, X.; Wang, Y.; Xian, Z. "An Evaluation of Skylight Polarization Patterns for Navigation." Sensors 2015, 15(3), 5895-5913. DOI 10.3390/s150305895
- URL opened: https://www.mdpi.com/1424-8220/15/3/5895
- Reading level: FULL
- Facts:
  - "the DOP is a key parameter to indicate the accuracy of AOP measurements"
  - "the lower the DOP is, the larger the error of the AOP measurement will be"
  - Measurements were taken in Changsha in July 2014 at low sun only (solar elevations 2.27 to 6.87 deg). Solar meridian error was 0.27 deg (clear) and 0.41 deg (cloudy).
- Relevance: gives a physical justification for sigma rising as 1/DoP, but no filter is used.

### 1.6 Zhi, Chu, Li, Wang (2018). Baseline EKF with a fixed noise model
- Citation: Zhi, W.; Chu, J.; Li, J.; Wang, Y. "A Novel Attitude Determination System Aided by Polarization Sensor." Sensors 2018, 18(1), 158. DOI 10.3390/s18010158
- URL opened: https://doaj.org/article/197df0759191464b907bfd6a26c4b3b3
- Reading level: ABSTRACT
- Facts: an EKF in which "The covariance functions of filter process and measurement noises are deduced in detail"; quadrotor test. The abstract does not mention DoP adaptation.

---

## Q2. Heading accuracy versus solar elevation, sun near zenith

### 2.1 Horváth and Wehner (1999). Measured zenith DoP collapse at high sun in the Tunisian desert
- Citation: Horváth, G.; Wehner, R. "Skylight polarization as perceived by desert ants and measured by video polarimetry." Journal of Comparative Physiology A 184(1), 1-7, 1999. (DOI not printed in the PDF opened)
- URL opened: https://arago.elte.hu/sites/default/files/SkyPolDesertAnt_JCPA.pdf
- Reading level: FULL
- Facts:
  - Table 1, green channel, zenith window: DoP was 24.2 / 26.2 / 29.8% at sun elevation 35 deg (Tozeur, Metlaoui, Mahares) and fell to 8.1 / 7.5 / 7.6% at sun elevation 70 deg.
  - "The degree of polarization, however, is highly reduced even in the cloudless sky"; the maximum reached "only about 60%".
  - The DoP is "much more affected by atmospheric disturbances and surface reflections" than the AoP.
- Relevance: real desert data (about 34 N) showing zenith DoP below 10% at 70 deg sun elevation. This strongly supports the model's collapse near solar noon at 24.45 N in summer.

### 2.2 Han et al. (2017). Accuracy improves as the sun gets lower
- Citation: Han, G.; Hu, X.; Lian, J.; He, X.; Zhang, L.; Wang, Y.; Dong, F. "Design and Calibration of a Novel Bio-Inspired Pixelated Polarized Light Compass." Sensors 2017, 17(11), 2623. DOI 10.3390/s17112623
- URL opened: https://www.mdpi.com/1424-8220/17/11/2623
- Reading level: FULL (first 100k characters)
- Facts:
  - "The orientation accuracy of the sensor increases with the decrease of the solar elevation angle."
  - Orientation error standard deviation was 0.15 deg at sunset.

### 2.3 Liang, Bai, Zhou (arXiv 2012.09154). Yaw undefined at 90 deg solar altitude
- Citation: Liang, H.; Bai, H.; Zhou, T. "Exploration of Whether Skylight Polarization Patterns Contain Three-dimensional Attitude Information." arXiv:2012.09154 (venue and year not printed on the page opened; arXiv ID indicates Dec 2020)
- URL opened: https://arxiv.org/pdf/2012.09154
- Reading level: FULL
- Facts:
  - The yaw angle "cannot be estimated when solar altitude is 90°"; the maximum yaw error reaches 180 deg there.
  - Yaw estimation is usually restricted to solar altitudes of "0° ~ 60°".
  - When the sun is at the zenith the neutral points merge and "the orientation cannot be estimate[d]".

### 2.4 Hu et al. (2022). Projection of the sun vector vanishes near zenith
- Citation: Hu, P.; Huang, P.; Qiu, Z.; Yang, J.; Liu, X. "A 3D Attitude Estimation Method Based on Attitude Angular Partial Feedback for Polarization-Based Integrated Navigation System." Sensors 2022, 22(3), 710. DOI 10.3390/s22030710
- URL opened: https://pmc.ncbi.nlm.nih.gov/articles/PMC8840561
- Reading level: FULL
- Facts:
  - "when the sun is near the zenith, the projection decreases and approaches zero"
  - A "low-accuracy projection vector results in inaccurate correction information"
  - In simulation at small solar zenith angle, the all feedback INS/POL yaw RMSE was 8.55 deg, against 4.84 deg for their partial feedback method (APF).

### 2.5 Smith and Stewart (2014). Errors at very high solar elevation
- Citation: Smith, F. J.; Stewart, D. W. "Robot and Insect Navigation by Polarized Skylight." Proc. BIOSIGNALS 2014, pp. 183-188. DOI 10.5220/0004792101830188
- URL opened: https://scitepress.org/PublishedPapers/2014/47921/pdf/index.html
- Reading level: FULL
- Facts:
  - "Errors occur only at very low or high solar elevations"
  - "when the solar elevation is above the observation elevation there may be no zeros"
  - Simulation only, with a 1 deg tolerance in most cases.

### 2.6 Liang, Bai, Zhou, Shen (arXiv 2007.08987). Tilt errors depend on solar altitude
- Citation: Liang, H.; Bai, H.; Zhou, T.; Shen, K. "Influence of Sensor Tilts on Bio-inspired Polarized Skylight Orientation Determination." arXiv:2007.08987 (venue and year not printed on the page opened)
- URL opened: https://arxiv.org/abs/2007.08987
- Reading level: ABSTRACT
- Facts: the errors "are affected by not only the degree of inclination, but also the solar altitude angle". Existing methods "require polarization sensor pointing to the zenith". Relevant to a ground robot pitching on dunes.

### 2.7 Li, Zhang, Fan, Yu (2024). Direct sunlight compensation across solar zenith angles
- Citation: Li, G.; Zhang, Y.; Fan, S.; Yu, F. "An Improved Bio-Orientation Method Based on Direct Sunlight Compensation for Imaging Polarization Sensor." Journal of Imaging 2024, 10(4), 74. DOI 10.3390/jimaging10040074
- URL opened: https://www.mdpi.com/2313-433x/10/4/74
- Reading level: FULL (no per angle table found)
- Facts: reports "a 23% to 47% improvement in the polarization orientation accuracy under various solar zenith angles". For the near zenith sun case it notes "As γs tends towards 0, γx and γy are approaching 90°" (direct sunlight enters near normal).

---

## Q3. Polarisation compass fused with visual odometry or VIO

### 3.1 Steidle, Stürzl, Triebel (2019). Polarisation compass in a VIO EKF, MAV
- Citation: Steidle, F.; Stürzl, W.; Triebel, R. "Visual-inertial sensor fusion with a bio-inspired polarization compass for navigation of MAVs." IMAV 2019, Madrid.
- URL opened: https://elib.dlr.de/131074
- Reading level: ABSTRACT (full PDF is DLR internal only)
- Facts:
  - The polarisation compass, IMU and visual odometry (6 DoF pose changes) are fused in an indirect EKF, comparing two ways of feeding in the compass measurements.
  - "adding a compass to visual-inertial sensor fusion does not only eliminate the drift of yaw angle estimates" but also "improves overall state estimation of the system".
  - The platform is a MAV, not a ground vehicle.

### 3.2 Chu, Hu, Wan, Li (2023). Polarisation aided VINS on a vehicle
- Citation: Chu, J.; Hu, H.; Wan, Z.; Li, J. "Visual Inertial Navigation System Aided by Polarized Light." Laser & Optoelectronics Progress 60(7), 0726002, 2023. DOI 10.3788/LOP213411
- URL opened: https://m.researching.cn/articles/OJb6ab185ab96adddd
- Reading level: ABSTRACT
- Facts:
  - A polarisation orientation sensor, monocular camera and MEMS IMU are fused by least squares optimisation; "the observability of azimuth is achieved based on the polarization distribution of the sky".
  - In an outdoor vehicle mounted test over 2 km, "the heading angle accuracy is 23.4% greater than" the original VIO, and position error was 16.7% lower.
- Relevance: the closest ground vehicle polarisation plus VIO work found. Monocular, not stereo; noise weighting not described in the abstract.

### 3.3 Shan, Guo, Li, Tao (2025). LPVIMO-SAM: polarisation imagery for features, not for heading
- Citation: Shan, D.; Guo, P.; Li, W.; Tao, D. "LPVIMO-SAM: Tightly-coupled LiDAR/Polarization Vision/Inertial/Magnetometer/Optical Flow Odometry via Smoothing and Mapping." arXiv:2504.20380, 2025; DOI 10.1109/IROS60139.2025.11247522
- URL opened: https://arxiv.org/html/2504.20380v1
- Reading level: FULL
- Facts:
  - DoP and AoP images enhance visual features ("the Red channel represents the polarization degree image"); heading comes from a magnetometer factor.
  - The paper "replaces the Polarization Heading factor constraint with a magnetometer heading factor constraint" relative to the earlier PFLIO-SAM. This implies PFLIO-SAM used a polarisation heading factor in a factor graph; PFLIO-SAM itself is UNOPENED.
  - No sun elevation or DoP gating of the heading.

### 3.4 Serres et al. (2024). Review: polarised vision for autonomous vehicles
- Citation: Serres, J. R.; Lapray, P.-J.; Viollet, S.; Kronland-Martinet, T.; Moutenet, A.; Morel, O.; Bigué, L. "Passive Polarized Vision for Autonomous Vehicles: A Review." Sensors 2024, 24(11), 3312. DOI 10.3390/s24113312
- URL opened: https://www.mdpi.com/1424-8220/24/11/3312
- Reading level: FULL (first part only)
- Facts: fusing polarised sensors with an INS "could be a supplemental perceptive modality". It lists VIO as a method to complement, and describes a logistics droid with a stereo camera where polarised geolocation "will be the 4th redundancy" (planned, not demonstrated).

---

## Q4. Measured accuracy of real polarisation compasses on vehicles or robots

### 4.1 Dupeyroux, Serres, Viollet (2019). AntBot, Science Robotics (via CNRS press release)
- Citation: Dupeyroux, J.; Serres, J. R.; Viollet, S. "AntBot: a six-legged walking robot able to home like desert ants in outdoor environments." Science Robotics, 13 Feb 2019. DOI 10.1126/scirobotics.aau0307
- URL opened: https://www.cnrs.fr/en/press/first-walking-robot-moves-without-gps
- Reading level: SUMMARY (press release; paper UNOPENED)
- Facts: the UV compass measures heading with "0.4° precision by clear or cloudy weather". The homing error after 14 m was about 1 cm.

### 4.2 Dupeyroux, Viollet, Serres (2019). Two pixel UV sensor, outdoor
- Citation: Dupeyroux, J.; Viollet, S.; Serres, J. R. "Polarized skylight-based heading measurements: a bio-inspired approach." J. R. Soc. Interface 16(150), 2019. DOI 10.1098/rsif.2018.0878
- URL opened: https://ouci.dntb.gov.ua/works/406EwJy9
- Reading level: ABSTRACT
- Facts: "a mean angular error of only 0.62° ± 0.40° (median: 0.24°)" in outdoor field studies (static sensor, not a vehicle).

### 4.3 Hu et al. (2022). INS/POL, moving platform
- Citation and URL as in 2.4. Reading level FULL.
- Facts: in the real experiment the platform "moved around a rectangular trajectory" under "a clear blue sky". Yaw RMSE was 2.82 deg (APF) against 3.47 deg (all feedback).

### 4.4 Li, Wang, Zhang, Li, Sun (2024). Field tests in sandy and overcast conditions
- Citation: Li, Y.; Wang, X.; Zhang, M.; Li, R.; Sun, Q. "Bionic Compass Method Based on Atmospheric Polarization Optimization in Non-Ideal Clear Condition." Photonics 2024, 11(12), 1099. DOI 10.3390/photonics11121099
- URL opened: https://www.mdpi.com/2304-6732/11/12/1099
- Reading level: FULL (results section truncated)
- Facts:
  - Heading error is reduced "to within 2° under sunny, cloudy, overcast and sandy conditions".
  - Rayleigh theory is "applicable to high-altitude, dry, and clear weather conditions".

### 4.5 Lu et al. (2020). Imaging polarisation prototype on a car against GNSS
- Citation: Lu, H.; Xie, Y.; Zhang, K.; Zhang, H.; Zou, X. M.; Wang, J.; Zhao, K. C. "Construction and Test of Bio-Inspired Imaging Polarization Navigation Prototype." ISPRS Archives XLIII-B1-2020, 323-329. DOI 10.5194/isprs-archives-XLIII-B1-2020-323-2020
- URL opened: https://isprs-archives.copernicus.org/articles/XLIII-B1-2020/323/2020/
- Reading level: ABSTRACT
- Facts: "the prototype is installed on the top of a vehicle and its navigation performance is compared with GNSS". No numbers in the abstract.

### 4.6 Wang, Liang, Zhu, Zhang (2014). Camera based polarisation sensor
- Citation: Wang, D.; Liang, H.; Zhu, H.; Zhang, S. "A Bionic Camera-Based Polarization Navigation Sensor." Sensors 2014, 14(7), 13006-13023. DOI 10.3390/s140713006
- URL opened: https://discovery-pp.ucl.ac.uk/id/eprint/10189232
- Reading level: ABSTRACT
- Facts: indoor accuracy "can reach up to 0.3256°"; an outdoor test against GPS/INS (dynamic RMS not in the abstract).

### 4.7 Lambrinos et al. Sahabot (UZH project page)
- URL opened: https://mls.uzh.ch/en/research/fgrimls/Labhart/ModelsRobots/MobileRobot.html
- Reading level: SUMMARY
- Facts: "The navigational precision was comparable to that of the desert ant Cataglyphis bicolor"; the page gives no numbers. It lists Lambrinos et al. 1997 (Adaptive Behavior 6:131-161) and 2000 (Robotics and Autonomous Systems 30:39-64), both UNOPENED.

---

## Q5. Dust, aerosol, haze and skylight DoP

### 5.1 Pust and Shaw (2012). Desert site with moderate aerosol keeps DoP below 60%
- Citation: Pust, N. J.; Shaw, J. A. "Wavelength dependence of the degree of polarization in cloud-free skies: simulations of real environments." Optics Express 20(14), 15559-15568, 2012. (DOI not printed in the PDF text read)
- URL opened: https://www.montana.edu/jshaw/documents/Wavelength%20dependence%20of%20atmospheric%20DoP%20-%20PustShaw%20-%20Opt%20Express%202012.pdf
- Reading level: FULL
- Facts:
  - "For a desert surface with moderate aerosols, the DoP remains below 60% for most wavelengths" (Saada, Morocco case).
  - With low aerosol over dark ground, "sky DoPs that approach 90% in the NIR".
  - "urban areas with high aerosol loading will be even lower than this"; surface reflectance also matters.

### 5.2 Horváth and Wehner (1999). See 2.1
- The maximum DoP in a clear Tunisian desert sky was only about 60% (75% in single pixels), against 100% in an ideal Rayleigh atmosphere. The AoP still matched theory well.

### 5.3 Liang and Bai. PSNS dataset: DoP falls sharply with turbidity
- Citation: Liang, H.; Bai, H. "Polarized Skylight Navigation Simulation (PSNS) Dataset." arXiv:2007.13081 (venue and year not printed)
- URL opened: https://arxiv.org/abs/2007.13081
- Reading level: FULL
- Facts: "the DOP of the whole sky decreases sharply with the increase of atmospheric turbidity"; higher turbidity raises intensity and lowers DoP.

### 5.4 Zhao and Xu (2016). Mie and multiple scattering depolarise skylight
- Citation: Zhao, H.; Xu, W. "A Bionic Polarization Navigation Sensor and Its Calibration Method." Sensors 2016, 16(8), 1223. DOI 10.3390/s16081223
- URL opened: https://www.mdpi.com/1424-8220/16/8/1223
- Reading level: FULL (first 100k characters)
- Facts: "The Mie scattering and multiple scattering could depolarize the skylight and significantly reduce the DOP"; nevertheless "the direction of polarization can be stable under most conditions". Peak DoP depends on "the solar zenith angle and the conditions of atmosphere".

### 5.5 Ma et al. (2015). See 1.5
- With high concentrations of larger aerosols, Mie scattering dominates, so the AoP may not be perpendicular to the scattering plane and the method may fail (paraphrase, no exact quote captured).

### 5.6 Daskalopoulou et al. (2023). Dust and polarisation of direct sunlight (marginal)
- Citation: Daskalopoulou, V. et al. "Linear polarization signatures of atmospheric dust with the SolPol direct-sun polarimeter." Atmospheric Measurement Techniques 16(19), 4529-4550, 2023. DOI 10.5194/amt-16-4529-2023
- URL opened: https://uhra.herts.ac.uk/id/eprint/11150/
- Reading level: ABSTRACT
- Facts: polarisation of direct sunlight through dust rose by up to 700 ppm (Antikythera, Greece). This concerns transmitted sunlight, not skylight DoP, so its relevance is only that aligned dust adds a small polarisation signal of its own.

### 5.7 Li et al. (2024). See 4.4: field results include "sandy" conditions, with heading within 2 deg after optimisation.

---

## UNOPENED or failed
- Dou et al. (DoP as a "deterministic factor" to adjust R): cited as ref [26] in Sun et al. 2025. I could not identify the paper by search; locate it from the Sun et al. reference list before citing.
- Zhao et al. (VB cubature KF plus residual chi squared, ref [13] in Sun et al. 2025): not located.
- PFLIO-SAM (polarisation heading factor in LiDAR inertial factor graph): referenced inside LPVIMO-SAM; not opened.
- IEEE TIM DOI 10.1109/TIM.2023.3262253: the redirect to ieeexplore was not on the allowlist.
- Dupeyroux et al. IROS 2017 and HAL 01990800: blocked by Anubis bot protection.
- Karman et al. 2012 review (PMC3522911) and PMC4435192: reCAPTCHA (the Ma et al. content was read via MDPI instead). The MDPI review URL was not on the allowlist.
- SPIE "Effects of wildfire smoke on atmospheric polarization" (Proc. SPIE 9099) and SPIE OE 59(2) 027107 "Self-adaptive robust algorithm...": empty pages returned.
- Lambrinos et al. 1997 and 2000 (Sahabot) papers; AntBot Science Robotics full text.
- Li, S. et al. South China Sea marine skylight polarisation (opened but contained no numbers); Agarwal 2025 Queen's thesis (abstract had no elevation data).

---

## Synthesis (10 lines)
1. Q1: DoP based adaptation of the polarisation compass R is already published in a piecewise form. Zhang et al. 2022 (Sensors 22:3372) use upper and lower DoP thresholds to weight the measurement, blend it, or reject it and switch to magnetometer (simulation, ship). Sun et al. 2025 cite Dou et al. for using DoP "as a deterministic factor" to scale R.
2. Q1 continued: the rest of the literature adapts R statistically (VB, Student's t, innovation saturation, chi square KF: Sun 2025, Zhao 2024, Bai 2024). None of the opened works uses a continuous sigma² = floor² + (c/DoP)² law, combines it with a chi square gate, or ties DoP weighting to solar geometry. Claim novelty only for that specific combination, and cite Zhang 2022 and Dou as the closest works.
3. Q1 physical basis: Ma et al. 2015 state that lower DoP means larger AoP error, which supports a 1/DoP noise term.
4. Q2: near zenith failure is established in theory and simulation. Liang et al. say yaw "cannot be estimated when solar altitude is 90°" and limit use to 0 to 60 deg. Hu et al. 2022 say the sun vector projection "approaches zero" (8.55 deg yaw RMSE in simulation). Han et al. 2017 report accuracy improving as the sun gets lower. Smith and Stewart 2014 report errors at high elevation.
5. Q2 measured: Horváth and Wehner 1999 measured zenith DoP of about 8% at 70 deg sun elevation in the Tunisian desert, against 24 to 30% at 35 deg.
6. Q2 gap: no opened source reports a time resolved, low latitude (below about 25 N) summer noon outage window for a ground robot compass, nor its duration. The roughly one hour outage at 24.45 N appears unreported and is a reasonable contribution if framed carefully.
7. Q3: polarisation compass plus VIO has been done on a MAV (Steidle et al. 2019, EKF) and on a ground vehicle with monocular VINS (Chu et al. 2023, 23.4% heading gain over 2 km). Polarisation heading factors exist in LiDAR factor graphs (PFLIO-SAM, per LPVIMO-SAM). I found no stereo VO plus IMU plus polarisation EKF on a desert ground robot.
8. Q4: real compass accuracy ranges from about 0.2 to 0.6 deg on static or slow bio-inspired robots (AntBot 0.4 deg; Dupeyroux 2019 0.62 ± 0.40 deg) to about 2 to 3.5 deg yaw RMSE in dynamic INS/POL tests (Hu 2022: 2.82 deg) and within 2 deg in mixed weather including sandy conditions (Li 2024). A sigma floor of about 0.5 to 2 deg is therefore defensible.
9. Q5: aerosol and dust lower sky DoP. Pust and Shaw 2012 simulate desert DoP below 60% with moderate aerosol; Horváth and Wehner 1999 measured a maximum of only about 60% in a clear Tunisian desert sky; PSNS shows DoP "decreases sharply" with turbidity; Zhao and Xu 2016 show Mie scattering depolarises skylight while the AoP stays fairly stable. No opened source measured skylight DoP during a Gulf dust event.
10. Net: the paper should say its pure Rayleigh model overestimates DoP in Abu Dhabi dusty air (real maxima are about 60% or lower), so the real outage window around noon is likely wider than simulated. It should also present DoP weighting as an extension of Zhang 2022 and Dou et al., not as a first.

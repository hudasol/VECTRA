# B. Estimation theory and evaluation method: opened-source notes

Compiled 2026-11-01. Local copies of downloaded files were kept outside the repository.

## How to read the "READ" field

- FULL-TEXT (local): whole PDF or HTML downloaded and converted to text by me. I read the abstract, introduction and the sections named in the facts, using grep plus surrounding context. I did not read every page of the long papers.
- WEBFETCH-EXTRACT: the page was opened through the WebFetch tool, which returns a small-model extract of the document, not the raw text. Quotes marked this way come from that extract. Re-check them against the PDF before printing them. Direct download of these hosts (intra.ece.ucr.edu, www-users.cse.umn.edu) failed from the shell.
- METADATA-ONLY: DOI, pages and venue confirmed through the Crossref API, but I did not open the content. These are listed under UNOPENED.
- Quotes are under 25 words, with extraction whitespace normalised. "Venue" notes say where the venue was not printed in the extracted text.

---

## (1) Visual-inertial systems

### 1.1 MSCKF
- Citation: Mourikis, A. I. and Roumeliotis, S. I. (2007). A Multi-State Constraint Kalman Filter for Vision-aided Inertial Navigation. Proc. IEEE ICRA 2007, pp. 3565-3572. DOI 10.1109/ROBOT.2007.364024 (DOI and pages from Crossref; the opened text did not print venue).
- URL opened: https://intra.ece.ucr.edu/~mourikis/papers/MourikisRoumeliotis-ICRA07.pdf
- READ: WEBFETCH-EXTRACT (two separate fetches, both on the full PDF).
- Facts:
  1. Feature observations are used without putting features in the state. Quote: "This is achieved without including the feature position in the filter state vector."
  2. Feature errors are removed by a nullspace projection. Quote: "by projecting r(j) on the left nullspace of the matrix Hf".
  3. Outliers are gated by a Mahalanobis test, described only briefly, with no threshold or chi-square level given. Quote (as returned by the tool): "using a simple Mahalanobis distance test".
  4. The evaluation had no ground truth and no NEES. The paper reports a 3.2 km outdoor run with a final position error of about 10 m (about 0.31% of distance travelled) and 3-sigma bound plots. This is the earliest "percent of path length" style result in my set.
  5. There is no formal observability analysis in this paper. Observability and consistency for MSCKF-type filters came later (Hesch, Li and Mourikis, below).

### 1.2 OpenVINS (paper)
- Citation: Geneva, P., Eckenhoff, K., Lee, W., Yang, Y. and Huang, G. (2020). OpenVINS: A Research Platform for Visual-Inertial Estimation. Proc. IEEE ICRA 2020, pp. 4666-4672. DOI 10.1109/ICRA40945.2020.9196524 (from Crossref; the PDF text itself does not print the venue line).
- URL opened: https://udel.edu/~pgeneva/downloads/papers/c10.pdf
- READ: FULL-TEXT (local), 6.5k words; read the abstract, the simulator and consistency section, and the benchmark section.
- Facts:
  1. The system is an on-manifold sliding-window EKF with FEJ treatment. Abstract: "SLAM landmarks with different representations and consistent First-Estimates Jacobian (FEJ) treatments".
  2. Its toolbox covers evaluation. Quote: "trajectory alignment; plotting utilities for trajectory accuracy and consistency evaluation; Monte-Carlo evaluation of different accuracy metrics".
  3. Its consistency study uses simulation with repeated runs. Quote: "Average ATE and NEES over twenty runs" (Table I caption). Each Monte-Carlo run has different measurement noise and different initial calibration values.
  4. Benchmarks report both ATE and RPE for several algorithms. Quote: "We additionally compared the Relative Pose Error (RPE) of all methods."

### 1.3 OpenVINS documentation (supports 1.2, 2 and 3)
- Citation: OpenVINS documentation, "Filter Evaluation Metrics", "Filter Error Evaluation Methods", "First-Estimate Jacobian Estimators". University of Delaware RPNG. Web pages, accessed 2026-11-01.
- URLs opened: https://docs.openvins.com/eval-metrics.html , https://docs.openvins.com/eval-error.html , https://docs.openvins.com/fej.html
- READ: FULL-TEXT (local HTML to text).
- Facts:
  1. NEES is the standard consistency measure. Quote: "NEES is a standard way to characterize if the estimator is being consistent or not." The averaged NEES formula is taken over N runs at each timestep.
  2. The authors recommend RPE. Quote: "what we recommend all authors publish results for" (about RPE, which they say is less sensitive to jumps in error than ATE).
  3. The documentation quotes Bar-Shalom et al. (the book itself is unopened): "Wrong covariance yield wrong gain." It states that consistency is necessary for filter optimality.
  4. Alignment modes in ov_eval include `posyaw`, `se3`, `sim3` and `none`. A position-plus-yaw alignment mode exists, which matches the yaw gauge freedom in section 2.

### 1.4 VINS-Mono
- Citation: Qin, T., Li, P. and Shen, S. (2018). VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator. IEEE Transactions on Robotics 34(4). arXiv:1708.03852. DOI 10.1109/TRO.2018.2853729 (the DOI is in the arXiv metadata; I did not check volume or issue).
- URL opened: https://arxiv.org/pdf/1708.03852
- READ: FULL-TEXT (local), 12.8k words; read the abstract, introduction, pose graph and failure detection sections.
- Facts:
  1. Roll and pitch are observable from the IMU. Quote: "metric scale, as well as roll and pitch angles, all observable".
  2. Drift is confined to four degrees of freedom. Quote: "drift only occurs in 4 DOF, which is the 3D translation, and the rotation around the gravity direction (yaw angle)".
  3. It is optimisation based, not a filter. It marginalises old states into a prior and includes loop closure through a 4-DoF pose graph.
  4. Its failure detection uses hard rules, not a statistical test. Quote: "Large discontinuity in position or rotation between last two estimator outputs".

### 1.5 ORB-SLAM3
- Citation: Campos, C., Elvira, R., Gomez Rodriguez, J. J., Montiel, J. M. M. and Tardos, J. D. (2021). ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM. IEEE Transactions on Robotics. arXiv:2007.11898. DOI 10.1109/TRO.2021.3075644 (printed in the PDF).
- URL opened: https://arxiv.org/pdf/2007.11898
- READ: FULL-TEXT (local), 14.3k words; read the abstract, IMU initialisation and the evaluation protocol.
- Facts:
  1. Accuracy is reported as RMS ATE with a choice of alignment. Quote: "aligning the estimated trajectory with ground-truth using a Sim(3) transformation in the pure monocular case". The text says SE(3) alignment is used in the other sensor configurations.
  2. IMU initialisation is a MAP problem where gravity direction is estimated and the map is aligned to it. Quote: "rotated to align the z axis with the estimated gravity direction".
  3. Yaw is excluded from the gravity parameterisation. Quote: "rotation around gravity direction does not suppose a change in gravity".
  4. Loop closing and multi-map merging reset drift, so full ORB-SLAM3 is not a like-for-like baseline for a loop-free filter. This is my inference.

---

## (2) Observability of yaw and consistency

### 2.1 Hesch et al. (IJRR 2014)
- Citation: Hesch, J. A., Kottas, D. G., Bowman, S. L. and Roumeliotis, S. I. (2014). Camera-IMU-based localization: Observability analysis and consistency improvement. International Journal of Robotics Research 33(1): 182-201. DOI 10.1177/0278364913509675 (from Crossref; Crossref lists online year 2013).
- URL opened: https://www-users.cse.umn.edu/~stergios/papers/IJRR_2014_VINS_OC_Joel_Dimitris_Sean.pdf
- READ: WEBFETCH-EXTRACT only. Quotes below are from that extract and need a check against the PDF.
- Facts:
  1. VINS has four unobservable directions. Quote (Theorem 5.2): "corresponding to the IMU-camera global position and its rotation around the gravity vector".
  2. The standard EKF gains false yaw information. Quote (Sec. 6): "acquisition of nonexistent information about global rotations around the gravity vector (yaw)".
  3. The fix is a nullspace-preserving modification of the Jacobians. Quote (Sec. 6.1): "we maintain the nullspace, Nk, at each time step, and use it to enforce the unobservable directions".
  4. Overconfidence in yaw leaks into horizontal position. Figure 6 caption, as extracted: "because Std-VINS is overconfident in its yaw estimate, it also becomes overconfident along the x- and y-axes".

### 2.2 Huang, Mourikis, Roumeliotis: First-Estimates Jacobian EKF
- Citation: Huang, G. P., Mourikis, A. I. and Roumeliotis, S. I. (2009). A First-Estimates Jacobian EKF for Improving SLAM Consistency. In Experimental Robotics (Springer Tracts in Advanced Robotics), pp. 373-382. DOI 10.1007/978-3-642-00196-3_43 (Crossref). The file name indicates the ISER 2008 conference version; the venue is not printed in the extracted text.
- URL opened: https://people.csail.mit.edu/ghuang/paper/Huang2008ISER.pdf
- READ: FULL-TEXT (local), 3.9k words.
- Facts:
  1. Standard EKF-SLAM has too large an observable subspace. Quote: "observable subspace of dimension higher than that of the actual, nonlinear, SLAM system".
  2. The missing direction is global orientation. Quote: "the filter gains 'nonexistent' information about the robot's global orientation".
  3. The remedy: Jacobians are computed at the first-ever estimate of each variable, which restores the correct observable subspace dimension.
  4. It defines consistency (via Bar-Shalom) as errors that are zero-mean with covariance no larger than the filter's own. It evaluates with average RMS and average NEES over Monte Carlo runs.

### 2.3 Li and Mourikis (IJRR 2013)
- Citation: Li, M. and Mourikis, A. I. (2013). High-precision, consistent EKF-based visual-inertial odometry. International Journal of Robotics Research 32(6): 690-711. DOI 10.1177/0278364913481251 (from Crossref; the opened text did not show the venue).
- URL opened: https://intra.ece.ucr.edu/~mourikis/papers/Li2013IJRR.pdf
- READ: WEBFETCH-EXTRACT only.
- Facts:
  1. Spurious yaw observability. Quote (Sec. VI, as extracted): "the global yaw erroneously appears to be observable".
  2. Same first-estimate remedy. Quote (Sec. VII-A): "always use the first available estimate for each state".
  3. NEES benchmark. Quote (Sec. III-D): "the average pose NEES should be 6 (equal to the dimension of the pose error)".
  4. Evaluation uses Monte Carlo. Quote: "averaged over 50 Monte-Carlo trials". It reports RMSE alongside NEES.

### 2.4 Huang, Hendeby and Skog (magnetic-field-aided INS, observability constrained)
- Citation: Huang, C., Hendeby, G. and Skog, I. (2024). An Observability-Constrained Magnetic Field-Aided Inertial Navigation System, Extended Version. arXiv:2406.02161. arXiv comment: "Accepted to IPIN 2024".
- URL opened: https://arxiv.org/pdf/2406.02161
- READ: FULL-TEXT (local), 5.4k words; read the abstract, introduction and evaluation set-up.
- Relevance: it covers the same yaw-observability problem, for a magnetic-field-odometry-aided INS. It is not a compass-heading aid.
- Facts:
  1. Quote: "address the issue of erroneous yaw observability, which leads to inconsistent estimates of yaw uncertainty".
  2. Cause. Quote: "causes the yaw to be perceived as observable even though it is not".
  3. Evaluation uses Monte Carlo simulation (RMSE) plus real data.

### 2.5 Huang and Dissanayake (extra, optional)
- Citation: Huang, S. and Dissanayake, G. "Convergence and Consistency Analysis for Extended Kalman Filter based SLAM". University of Technology Sydney manuscript dated April 5, 2006; the journal venue is not shown in the extracted text, so I give no venue.
- URL opened: https://opus.lib.uts.edu.au/bitstream/10453/5819/3/2006013768.pdf
- READ: FULL-TEXT (local); abstract and introduction only.
- Fact: "robot orientation uncertainty at the instant when landmarks are first observed has a significant effect" on landmark uncertainty. I found this while searching for Bailey et al. (it is not the Bailey paper).

---

## (3) EKF consistency testing (NEES, NIS, chi-square gating)

The primary sources named in the brief (Bar-Shalom book, Bailey et al. 2006) are UNOPENED. What I could open is below.

### 3.1 NEES in practice: Li and Mourikis (2.3), Huang FEJ (2.2), OpenVINS (1.2, 1.3)
All three evaluate consistency by averaging NEES over Monte Carlo runs and comparing with the state dimension. Li and Mourikis give 6 for pose. The OpenVINS documentation gives "the degrees of freedoms of the state variables". These are secondary descriptions of Bar-Shalom's test.

### 3.2 Zhang et al. (2020), averaged NIS definition (see also 4.2)
- It defines the averaged NIS over n_MC Monte Carlo runs in its eq. (191): "The averaged normalized innovation squared (NIS) is also provided to measure the consistency of the Kalman filter".
- Citation and read status are in 4.2.

### 3.3 AMO-HEAD, chi-square gating of a heading sensor (see 4.3)
It applies a squared Mahalanobis distance of the magnetometer residual and compares it with chi-square quantiles. Quote: "d2 ∼ χ23" (three degrees of freedom).

### 3.4 Mourikis and Roumeliotis 2007 (1.1), Mahalanobis gating
Only a one-line mention, with no threshold.

---

## (4) Adaptive and robust Kalman filtering

### 4.1 Akhlaghi, Zhou and Huang (2017)
- Citation: Akhlaghi, S., Zhou, N. and Huang, Z. (2017). Adaptive Adjustment of Noise Covariance in Kalman Filter for Dynamic State Estimation. arXiv:1702.00884. The arXiv record carries no journal reference, and the PDF text does not print a venue; I treat it as a preprint.
- URL opened: https://arxiv.org/pdf/1702.00884
- READ: FULL-TEXT (local), 4.5k words; read the abstract, the adaptive EKF section and the references.
- Domain caution: the application is dynamic state estimation of a synchronous machine in a power system, not navigation.
- Facts:
  1. Covariance matching is one of Mehra's four classes. Quote: "Bayesian, correlation, covariance matching and maximum likelihood".
  2. The method estimates both Q (innovation based) and R (residual based) online. Abstract: "adaptively estimate Q and R based on innovation and residual".
  3. A naive R estimate can lose positive definiteness. Quote: "could not guarantee that the estimated Rk be a positive definite matrix".
  4. It uses a forgetting factor in (0, 1]: "forgetting factor 0 < α ≤ 1" for averaging.
  5. Its reference list cites Mehra, "Approaches to adaptive filtering", IEEE TAC AC-17(5), 1972, and not the 1970 paper in the brief.

### 4.2 Zhang et al. (2020), a review that describes Mehra 1970 (secondary)
- Citation: Zhang, L., Sidoti, D., Bienkowski, A., Pattipati, K. R., Bar-Shalom, Y. and Kleinman, D. L. (2020). On the Identification of Noise Covariances and Adaptive Kalman Filtering: A New Look at a 50 Year-Old Problem. IEEE Access 8: 59362-59388. DOI 10.1109/access.2020.2982407 (printed on the PMC page).
- URL opened: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8638515/
- READ: FULL-TEXT (local HTML to text); introduction, background, case set-up. Not every proof.
- Why I used it: it is open access and is co-authored by Bar-Shalom. It is the closest I could get to Mehra 1970 (IEEE TAC 15(2): 175-184, April 1970, reference [33] in this paper).
- Facts:
  1. Mehra's correlation method. Quote: "correlations of innovations from an arbitrary initial stabilizing filter gain was introduced by Mehra".
  2. Covariance matching. Quote: "sample covariance of the innovations should be consistent with its theoretical value".
  3. Adaptation rule. Quote: "if the estimated innovation covariance value is much larger than the theoretical value, then the process noise covariance is increased".
  4. Identifiability. Quote: "provided a counter-example wherein the system was observable and controllable, but the full Q matrix was not estimable". This contradicts the condition Mehra stated. It is a warning for any claim that innovation-based noise adaptation is well posed.
  5. Defines averaged NIS (eq. 191) for Monte Carlo consistency checks.

### 4.3 AMO-HEAD (closest prior art for B2: innovation-based covariance scaling of a heading aid)
- Citation: Guo, Q., Yang, S., Lyu, J., Sun, J., Lin, D. and He, S. (2025). AMO-HEAD: Adaptive MARG-Only Heading Estimation for UAVs under Magnetic Disturbances. arXiv:2510.10979 (13 Oct 2025, cs.RO). Preprint; no venue stated in the extracted text.
- URL opened: https://arxiv.org/pdf/2510.10979
- READ: FULL-TEXT (local), 11.1k words; read the adaptive covariance section (IV-B, IV-C), the observability section headers and the experiment section.
- Facts:
  1. A scaling factor is applied to the magnetometer noise based on a real-time deviation test. Abstract: "a scaling factor is applied based on real-time magnetic deviation detection".
  2. Gate: squared Mahalanobis distance of the magnetometer residual, "d2 ∼ χ23", with two thresholds at confidence levels "p1 = 0.95 for severe disturbances and p2 = 0.35 for moderate ones".
  3. Piecewise inflation: R_m is multiplied by λ1 (severe), λ2 (moderate), or 1. Quote: "λ1 and λ2, are empirically tuned using a validation dataset" collected in the same environment as the test.
  4. Reports heading RMSE and MAE: "RMSE of only 1.58° and an MAE of 1.42°". I found no significance test, confidence interval or repeated-run statistics in the text (searched for "signific", "p-value", "confidence interval").
  5. Includes a Lie-derivative observability analysis for heading. Design lesson for this paper: λ tuned in the test environment is a leakage risk.

### 4.4 Li et al. (2019), Huber-based robust filter (an application paper, not Huber's original)
- Citation: Li, Y., Li, J., Qi, J. and Chen, L. (2019). Robust Cubature Kalman Filter for Dynamic State Estimation of Synchronous Machines under Unknown Measurement Noise Statistics. IEEE Access 7: 29139-29148 (journal reference from the arXiv record). arXiv:1902.07213.
- URL opened: https://arxiv.org/pdf/1902.07213
- READ: FULL-TEXT (local), 5.8k words; read abstract, filter derivation and Huber section.
- Domain caution: power-system state estimation, not navigation.
- Facts:
  1. Huber M-estimation modifies the measurement noise covariance in the update. Quote: "obtain a revised covariance matrix of measurement noises".
  2. Huber cost is quadratic below a threshold and linear above. Quote: "c is a constant and is chosen as 1.5 in this paper".
  3. Claimed benefit. Abstract: "good adaptability to unknown measurement noise statistics characteristics including non-Gaussian measurement noise and outliers".

### 4.5 Wang et al. (2020), outlier-robust KF with Huber cost (skimmed)
- Citation: Wang, H., Liu, Y., Zhang, W. and Zuo, J. (2020). Outlier-robust Kalman Filter in the Presence of Correlated Measurements. arXiv:2011.13353 (stat.AP).
- URL opened: https://arxiv.org/pdf/2011.13353
- READ: abstract and introduction only.
- Fact: "the measurement fitting error is processed separately during the reweighting procedure". Useful only as a pointer that Huber reweighting can treat correlated measurement channels badly.

---

## (5) Trajectory evaluation

### 5.1 Zhang and Scaramuzza (IROS 2018)
- Citation: Zhang, Z. and Scaramuzza, D. (2018). A Tutorial on Quantitative Trajectory Evaluation for Visual(-Inertial) Odometry. Proc. IEEE/RSJ IROS 2018, pp. 7244-7251. DOI 10.1109/IROS.2018.8593941 (Crossref; the extracted text does not print the venue).
- URL opened: https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf
- READ: FULL-TEXT (local), 6.8k words; read the alignment and error-metric sections.
- Facts:
  1. The alignment type follows the unobservable freedoms. For inertial systems it is yaw-only plus translation. Quote: "corresponds to the four unobservable DoFs for visual-inertial systems".
  2. Relative error exists because there is no global reference. Quote: "do not have a global reference (global position and yaw)".
  3. ATE weakness. Quote: "ATE is sensitive to the time when the error occurs".
  4. Relative error gives a distribution over sub-trajectories (median, mean, percentiles) rather than one number. On which states to use for alignment they say "no gold standard".
- Implication for B1/B2 (my inference, not from the paper): once an absolute heading aid makes yaw observable, a 4-DoF yaw-and-translation alignment would remove the very error the aid is meant to fix. Report both aligned and position-only-aligned results, and say which is used.

### 5.2 Sturm et al. (IROS 2012), ATE and RPE
- Citation: Sturm, J., Engelhard, N., Endres, F., Burgard, W. and Cremers, D. (2012). A Benchmark for the Evaluation of RGB-D SLAM Systems. Proc. IEEE/RSJ IROS 2012, pp. 573-580. DOI 10.1109/IROS.2012.6385773 (Crossref).
- URL opened: https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf
- READ: FULL-TEXT (local), 7.1k words; read the metrics section.
- Facts:
  1. RPE measures drift over a fixed interval. Quote: "corresponds to the drift of the trajectory which is in particular useful for the evaluation of visual odometry systems".
  2. ATE needs alignment. Quote: "finds the rigid-body transformation S corresponding to the least-squares solution" (Horn's closed-form method).
  3. Do not compare start with end only. Quote: "a common (but poor) choice is to set ∆ = n".
  4. They report an RMSE of the translational part of the error, and mention mean or median as alternatives that reduce outlier influence.

### 5.3 Geiger, Lenz and Urtasun (CVPR 2012), KITTI
- Citation: Geiger, A., Lenz, P. and Urtasun, R. (2012). Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite. Proc. IEEE CVPR 2012, pp. 3354-3361. DOI 10.1109/CVPR.2012.6248074 (Crossref).
- URL opened: https://www.cvlibs.net/publications/Geiger2012CVPR.pdf
- READ: FULL-TEXT (local), 6.3k words; read the odometry metric paragraph and results.
- Facts:
  1. End-point error is misleading. Quote: "based on the error of the trajectory end-point can be misleading".
  2. Rotation and translation are reported separately and as a function of path length and speed. Quote: "we evaluate errors as a function of the trajectory length and velocity".
  3. Reported form is a percentage and deg/m. Quote: "average translation error of 2.2% and an average rotation error of 0.016 deg/m" (VISO2-S).
  4. The segment lengths used by the KITTI odometry devkit are not stated in this paper's text. I did not verify them; check the devkit documentation before citing numbers.

---

## (6) Statistics and experimental practice

### 6.1 Colas, Sigaud and Oudeyer (2018), How many random seeds?
- Citation: Colas, C., Sigaud, O. and Oudeyer, P.-Y. (2018). How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments. arXiv:1806.08295 (v2, 5 Jul 2018). Preprint.
- URL opened: https://arxiv.org/pdf/1806.08295
- READ: FULL-TEXT (local), 6.6k words; read the abstract, test descriptions, and the conclusions.
- Facts:
  1. Tests covered are Welch's t-test and the bootstrap confidence-interval test, with power analysis for the number of seeds.
  2. They assume independent measurements and say that is reasonable for independent training runs. Quote: "Measurements are independent from one another. This seems reasonable in RL." So they treat seeds as independent samples, which is the opposite of the claim in the brief. Seeds are only independent if each seed gives an independent draw for each algorithm; in a paired design with shared scenarios they are not (see synthesis 4).
  3. Multiple comparisons. Quote: "false positive rate grows linearly with the number of experiments". They suggest the Bonferroni correction.
  4. Small-sample warnings. Quote: "the bootstrap test should not be used with less than N = 20 samples". Recommended bootstrap resamples: "B should be chosen large (e.g. > 1000)".

### 6.2 Henderson et al. (AAAI 2018), Deep RL that matters
- Citation: Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D. and Meger, D. (2018). Deep Reinforcement Learning that Matters. AAAI 2018 (copyright line in the PDF). arXiv:1709.06560.
- URL opened: https://arxiv.org/pdf/1709.06560
- READ: FULL-TEXT (local), 12.1k words; read the seeds and trials section, the significance and bootstrap section.
- Facts:
  1. Same algorithm, same hyperparameters, two groups of 5 seeds gave significantly different results. Quote: "variance between runs is enough to create statistically different distributions just from varying random seeds" (t = -9.09, p = 0.0016 in the Figure 5 caption).
  2. Bootstrap confidence bounds. Quote: "Table 3 shows the bootstrap mean and 95% confidence bounds" (the table notes 10k bootstrap iterations).
  3. They say the right significance test is unsettled. Quote: "Further work is needed to investigate proper corrected significance tests for RL."
  4. Reporting small N or top-N runs is called misleading.

### 6.3 Derrac et al. (2011), nonparametric tests
- Citation: Derrac, J., Garcia, S., Molina, D. and Herrera, F. (2011). A practical tutorial on the use of nonparametric statistical tests as a methodology for comparing evolutionary and swarm intelligence algorithms. Swarm and Evolutionary Computation 1(1): 3-18. DOI 10.1016/j.swevo.2011.02.002 (printed in the PDF).
- URL opened: https://sci2s.ugr.es/sites/default/files/files/TematicWebSites/sicidm/2011-Derrac-SWEVO.pdf
- READ: FULL-TEXT (local), 15.4k words; read the Wilcoxon, FWER, Holm and recommendations sections.
- Facts:
  1. Wilcoxon signed ranks is the nonparametric analogue of the paired t-test. Quote: "analogous to the paired t-test in nonparametric statistical procedures".
  2. It is more robust to outliers. Quote: "more sensitive than the t-test", and it "does not assume normal distributions".
  3. Repeated pairwise tests lose error control. Quote: "such as Wilcoxon's test, should not be used to conduct various comparisons involving a set of algorithms".
  4. Holm step-down. Quote: "this adjusts the value of α in a step-down manner".
  5. Unit of analysis is one result per algorithm and problem, with repeated executions averaged first. Quote: "using average results from several executions when considering stochastic algorithms". So the sample size is the number of scenarios, not the number of seeds.

### 6.4 Nosek et al. (PNAS 2018), preregistration
- Citation: Nosek, B. A., Ebersole, C. R., DeHaven, A. C. and Mellor, D. T. (2018). The preregistration revolution. Proceedings of the National Academy of Sciences 115(11): 2600-2606. DOI 10.1073/pnas.1708274114 (DOI, volume, pages from Crossref; I did not check the issue number).
- What I opened: the author manuscript (OSF preprint version, DOI 10.31219/osf.io/2dxu5) at https://errorstatistics.com/wp-content/uploads/2017/07/nosek-et-al-preregistration-revolution.pdf. The PNAS site returned 403. Wording may differ from the published version.
- READ: FULL-TEXT (local), 7.6k words.
- Facts:
  1. Core idea. Quote: "committing to analytic steps without advance knowledge of the research outcomes".
  2. Deviations are allowed if reported. Quote: "Deviations do not necessarily rule out testing predictions effectively."
  3. Report all outcomes. Quote: "all outcomes of that analysis plan must be reported in order to avoid the problem of selective reporting".
  4. Pre-existing data is a named challenge: "Challenge #3: Data are pre-existing." Preregistration is still possible if nobody has yet looked at the data. For simulated results, fix the plan before running the final evaluation.

### 6.5 Ernst and Baldassarre (2023), registered reports
- Citation: Ernst, N. A. and Baldassarre, M. T. (2023). Registered Reports in Software Engineering. arXiv:2302.03649. Preprint (Empirical Software Engineering editorial context).
- URL opened: https://arxiv.org/pdf/2302.03649
- READ: abstract and introduction, with a keyword search for the stage structure.
- Facts:
  1. Stage 1 review gives acceptance before results. Quote: "in-principle acceptance" after a protocol is reviewed.
  2. Quote: "decouples publication from a focus on headline-worthy 'significant' results."
  3. Registered reports first appeared at the journal Cortex in 2013 (stated in the paper).
  4. This is a software engineering source, not robotics. I found no robotics or estimation registered-report source.

---

## UNOPENED (with reason)

| Source | Status |
|---|---|
| Bar-Shalom, Li and Kirubarajan (2001), Estimation with Applications to Tracking and Navigation (NEES, NIS, chi-square tests) | Book, paywalled. Only secondary statements opened (OpenVINS docs, FEJ paper, Zhang et al. 2020). |
| Bailey, Nieto, Guivant, Stevens and Nebot (2006), Consistency of the EKF-SLAM Algorithm, IROS 2006, pp. 3562-3568, DOI 10.1109/IROS.2006.281644 | Metadata checked via Crossref. IEEE Xplore page returned empty text via WebFetch. No open copy found. The UTS "opus" PDFs that matched the search were a different paper (Huang and Dissanayake), see 2.5. |
| Mehra (1970), On the identification of variances and adaptive Kalman filtering, IEEE TAC 15(2): 175-184, DOI 10.1109/TAC.1970.1099422 | Metadata via Crossref. Paywalled. Only secondary descriptions opened (4.2). |
| Mehra (1972), Approaches to adaptive filtering, IEEE TAC AC-17(5) | Only cited inside Akhlaghi et al.; not searched. |
| Sage and Husa (1969), Adaptive filtering with unknown prior statistics (JACC) | Not found. DTIC links returned 403. Crossref shows a different 1969 Sage and Husa item, "Algorithms for sequential adaptive estimation of prior statistics" (DOI 10.1109/SAP.1969.269927, 1969 Symposium on Adaptive Processes), that I could not open or confirm as the same work. |
| Huber (1964) and Durovic and Kovacevic style robust Kalman filters | Not opened. Only two application papers using Huber weights (4.4, 4.5). |
| Hesch et al. T-RO version (Consistency Analysis and Improvement of Vision-aided Inertial Navigation, DOI 10.1109/TRO.2013.2277549) | Crossref metadata only. Host not reachable from the shell (TLS certificate error). |
| Huang, Mourikis and Roumeliotis, Observability-based Rules for Designing Consistent EKF SLAM Estimators (IJRR 2010) | Appeared in search results only. |
| Li and Mourikis, Improving the Accuracy of EKF-Based VIO (ICRA 2012) | Search result only. |
| MSCKF technical report (TR_MSCKF) | UCR host reset the shell connection; WebFetch of the conference paper succeeded instead. |
| Chambers and Tzavella (2022), Registered Reports; Chambers (2013), Cortex | Cited inside 6.5, not opened. |
| Other hosts that blocked or failed | Semantic Scholar API (429 rate limit), IEEE Xplore (empty), github.com (403), PNAS site (403), Europe PMC (403), DTIC (403). |

---

## Synthesis (10 lines)

1. A filter that uses only relative information cannot observe global yaw or position. Four directions are unobservable in VINS (Hesch; Zhang and Scaramuzza; VINS-Mono says drift is confined to 4 DoF), so B0's heading will drift regardless of tuning.
2. Linearised EKFs gain false yaw information at estimated linearisation points, becoming overconfident in yaw and then in horizontal position (Hesch; Huang FEJ; Li and Mourikis). Any B0 baseline should use FEJ or observability-constrained Jacobians, or state that it does not.
3. An absolute heading aid makes yaw observable. This is my inference from the theory above, not a claim by any one paper. Fixed-noise fusion (B1) then relies on the heading noise being right, and an unmodelled bias would produce an overconfident, inconsistent filter.
4. Innovation-based covariance scaling is established practice. Covariance matching (Mehra class; Zhang et al. 2020) and chi-square-gated inflation of a magnetometer R (AMO-HEAD, with thresholds at 0.95 and 0.35 confidence and tuned λ) are the nearest prior art for B2. Mehra's identifiability condition is disputed (counter-example reported by Zhang et al.), so a reliability-adaptive R needs its own check.
5. Standard consistency evidence is average NEES over Monte Carlo runs against the state dimension, with 3-sigma plots and NIS (OpenVINS, Li and Mourikis, Huang FEJ, Zhang et al.). "Wrong covariance yield wrong gain" (Bar-Shalom, quoted by OpenVINS) is the argument for reporting it, so B1 versus B2 should be compared on NEES as well as error.
6. Trajectory error: report RPE or drift per path length (Sturm; KITTI; OpenVINS recommends RPE) with translation and rotation separate, plus ATE only with the alignment stated. For heading-aided runs, do not apply a 4-DoF yaw alignment without saying so, because it removes the benefit being tested (inference from Zhang and Scaramuzza).
7. Gating: MSCKF uses a Mahalanobis test, AMO-HEAD uses chi-square quantiles on a 3-DoF residual. The confidence level is a design parameter and should be fixed on data separate from the test scenarios (AMO-HEAD tunes λ in the test environment).
8. Seeds: Colas et al. and Henderson et al. use seeds as independent samples and show small N misleads (5 seeds can give p = 0.0016 between identical algorithms; bootstrap not below N = 20). In a paired comparison where B0, B1 and B2 share scenarios and noise draws, the unit is the scenario (Derrac: one averaged result per algorithm and problem). I did not find a source that uses the word pseudoreplication; this is my reading.
9. Test choice: paired Wilcoxon signed-rank per scenario, Holm across the family of comparisons (Derrac), bootstrap CI on the median paired difference with B above 1000 (Colas). By my arithmetic, a two-sided exact Wilcoxon cannot reach p below 0.05 with fewer than 6 scenarios, and with 3 Holm-corrected comparisons you need at least 7.
10. Preregistration: define metrics, alignment, gating levels, tuned parameters and the test list before the final runs, report all outcomes and deviations (Nosek; registered reports are a software engineering source only). I found no robotics source that makes this standard, and no estimation paper in this set (including AMO-HEAD) reports a significance test, so adaptive heading fusion papers in this set evaluate with RMSE on a handful of runs.

# F. Study 3 literature scan: polarisation compass, dusty skylight, open sky data, compass aided VO

Scan date: 3 November 2026. Scope: open access works, 2025 and 2026 first, then older key works. A work is listed only if its page or PDF was opened during this scan. "Read" records what was available: abstract (abstract page or abstract only) or full text (the full paper was opened). Quotes are short extracts taken from the opened page; where a page only gave a table, the table values are reported instead. Works already covered in `E_polarisation_compass.md` are cross referenced rather than repeated unless they were reopened here.

## 1. Polarisation compass and polarised light navigation for ground robots and UAVs (2025 to 2026 first)

### 1.1 Yuan, Wu, Wang, Liu (2025). Vision based tilt compensation
- Citation: Yuan, M.; Wu, X.; Wang, C.; Liu, X. (2025). Tilt Induced Error Compensation with Vision Based Method for Polarization Navigation. Applied Sciences 15(9), 5060. doi:10.3390/app15095060
- URL: https://www.mdpi.com/2076-3417/15/9/5060
- Read: abstract and article page.
- Facts: roll and pitch come from horizon detection in camera images, not from an IMU: "a method for compensating horizontal attitude angles based on horizon detection". Reported "the horizontal attitude angle estimation error remains within 0.3°" and "the heading accuracy after compensation is improved by approximately 77.4%". Preprocessing uses Retinex and a dark channel prior for low light and haze.
- Relevance to Study 3: confirms tilt is a first order error source for a compass on a moving platform; supports our use of VO or IMU attitude for tilt correction, but the paper does not fuse with VO for position.

### 1.2 Su, Zhang, Fu, Zhan, Li, Wang, Zhou (2026). Solar meridian from fused polarisation patterns, tested in dust
- Citation: Su, H.; Zhang, S.; Fu, Q.; Zhan, J.; Li, Y.; Wang, C.; Zhou, J. (2026). Solar meridian determination based on fused polarization patterns. Chinese Optics 19(4), 895 to 906. doi:10.37188/CO.2026-0044
- URL: https://chineseoptics.net.cn/en/article/doi/10.37188/CO.2026-0044
- Read: abstract.
- Facts: the authors "propose a dual-polarization mode fusion method" combining global and local polarisation features with temporal filtering using solar motion and a neutral point constraint. Evaluated under sunny, cloudy, foggy and dusty skies, with mean relative errors 0.02, 0.051, 0.053 and 0.017, "substantially outperforming single-feature methods".
- Relevance to Study 3: the only 2026 work found that reports compass performance explicitly in dust; it is a static meridian extraction study without VO or robot motion, and it does not weight by per sample DoP.

### 1.3 Wang, Li, Luo, Chu (2025). Error model for polarised skylight positioning
- Citation: Wang, Y.; Li, J.; Luo, Y.; Chu, J. (2025). Error Model for Autonomous Global Positioning Method Using Polarized Sky Light and True North Measurement Instrument. Applied Sciences 15(13), 7287. doi:10.3390/app15137287 (CC BY)
- URL: https://www.mdpi.com/2076-3417/15/13/7287
- Read: abstract and article page.
- Facts: simulation only; "the positioning error mostly remains less than 14 m" when the two measured angles deviate by up to 0.0001 degrees; some locations have errors "approaching positive infinity". No inertial or visual fusion in the method.
- Relevance to Study 3: background only; shows that skylight positioning (as opposed to heading) needs angular accuracy far beyond what a dusty sky allows, which supports restricting Study 3 to heading aiding.

### 1.4 Wang, Chi, Bai, Yang, Hu, Qiu, Yu (2024). Multidirectional polarisation sensors plus sun sensor for cloudy skies
- Citation: Wang, S.; Chi, X.; Bai, H.; Yang, J.; Hu, P.; Qiu, Z.; Yu, X. (2024). An Integrated Navigation System Using IμMultidirectional Polarization Sensors/Sun Sensor for Cloudy Environments. IEEE Sensors Journal 24(14), 21906 to 21915. doi:10.1109/JSEN.2023.3302405
- URL: https://research.buaa.edu.cn/zh/publications/an-integrated-navigation-system-using-i%CE%BCmultidirectional-polariza/
- Read: abstract.
- Facts: fuses several polarisation sensors, a sun sensor and an IMU, with outlier detection to select sensors and a chi square based Kalman filter to adapt measurement noise; claims "the proposed method can improve the navigation accuracy in cloudy weather conditions" from static ground and UAV tests. No visual odometry.
- Relevance to Study 3: closest multi directional and adaptive noise design; adaptation is innovation based (chi square), not a physically derived per sample DoP weight.

### 1.5 Yadala Chanchu, Zuidgeest, Stam, de Croon (2024). Learned heading from polarisation images
- Citation: Yadala Chanchu, L.; Zuidgeest, R. F. G.; Stam, D. M.; de Croon, G. C. H. E. (2024). Robust Heading Estimation from Polarization Images by Deep Neural Networks. IMAV 2024, Bristol, UK.
- URL: https://www.imavs.org/papers/2024/6.pdf
- Read: full text (PDF).
- Facts: ResNet 18 estimates solar azimuth from skylight polarisation images; "a median absolute error of 1.0 degrees on simulation data with cloud masks, and 4.3 degrees" on real images; the brightest spot baseline gives "a median absolute error of 10.9 degrees".
- Relevance to Study 3: a realistic real sky error scale (about 4 degrees median under mostly cloudy skies) for setting our compass noise priors; it shows the simulation to real gap that our unseen environment check must address.

### 1.6 Gkanias, Mitchell, Stankiewicz, Khan, Mitra, Webb (2023). Insect eye inspired celestial compass
- Citation: Gkanias, E.; Mitchell, R.; Stankiewicz, J.; Khan, S.; Mitra, S.; Webb, B. (2023). Celestial compass sensor mimics the insect eye for navigation under cloudy and occluded skies. Communications Engineering 2, 82. doi:10.1038/s44172-023-00132-w
- URL: https://www.research.ed.ac.uk/en/publications/celestial-compass-sensor-mimics-the-insect-eye-for-navigation-und/
- Read: abstract.
- Facts: a ring of eight photodiode pairs with two orthogonal polarisation orientations; performs better "especially under cloudy and occluded skies"; offers "an efficient and robust directional input for navigation".
- Relevance to Study 3: older key wide field, multi directional design; useful as a hardware reference for a low cost desert rover compass.

### 1.7 Stürzl (2017). Single camera polarisation compass with covariance
- Citation: Stürzl, W. (2017). A Lightweight Single Camera Polarization Compass with Covariance Estimation. Proceedings of the IEEE International Conference on Computer Vision (ICCV). doi:10.1109/ICCV.2017.572
- URL: https://mlanthology.org/iccv/2017/sturzl2017iccv-lightweight (PDF: https://openaccess.thecvf.com/content_ICCV_2017/papers/Sturzl_A_Lightweight_Single-Camera_ICCV_2017_paper.pdf)
- Read: abstract.
- Facts: "the sun direction and its covariance matrix can be estimated based on the polarization measured in the image plane"; field of view "approx. 56 degrees"; "combination with an IMU allows to determine all degrees" of orientation when the sensor is not levelled; because covariance is estimated, integration "in a multi-sensor navigation framework is straight forward".
- Relevance to Study 3: key prior art for per measurement uncertainty in a polarisation compass. Our DoP weighting must be positioned against this covariance approach, not presented as the first per sample uncertainty.

## 2. Measured skylight degree of polarisation in deserts and under dust or aerosol

### 2.1 Horváth and Wehner (1999). Video polarimetry in the Tunisian desert (target source found)
- Citation: Horváth, G.; Wehner, R. (1999). Skylight polarization as perceived by desert ants and measured by video polarimetry. Journal of Comparative Physiology A 184, 1 to 7.
- URL: https://www.imls.uzh.ch/static/CMS_publications/wehner/literatur/pdf99/wehner19992a.pdf
- Read: full text (PDF).
- Facts: Table 1 caption: "Sun elevation: 70°, local time 1400 hours; sun elevation: 35°, local time 1630 hours". Zenith window (20 by 15 degrees), green channel, mean plus or minus SD: at 35 degrees solar elevation 24.2 ± 6.9 % (Tozeur, chott), 26.2 ± 7.9 % (Metlaoui, mountains), 29.8 ± 9.0 % (Mahares, coast); at 70 degrees 8.1 ± 3.9 %, 7.5 ± 3.9 %, 7.6 ± 3.7 %. UV values are lower: 10.6 to 13.0 % at 35 degrees and 4.8 to 5.1 % at 70 degrees. Maximum DoP in the band through the zenith reached "only about 60%", and "the degree of polarization was always higher in the green than in the ultraviolet range". Measurements were taken 4 to 10 August 1996. Note: the table layout in the PDF text extraction is partly garbled and some cells hold a second day; values above should be checked against the printed table before final citation.
- Relevance to Study 3: this is the source for "zenith DoP of about 24 to 30 percent at 35 degrees and about 8 percent at 70 degrees". It is measured in a real desert and directly supports the claim that the zenith compass signal collapses at high sun, which motivates DoP weighting.

### 2.2 Pust and Shaw (2012). Desert site keeps DoP below 60 percent
- Citation: Pust, N. J.; Shaw, J. A. (2012). Wavelength dependence of the degree of polarization in cloud free skies: simulations of real environments. Optics Express 20(14), 15559 to 15568.
- URL: https://www.montana.edu/jshaw/documents/Wavelength%20dependence%20of%20atmospheric%20DoP%20-%20PustShaw%20-%20Opt%20Express%202012.pdf
- Read: full text (PDF).
- Facts: "For a desert surface with moderate aerosols, the DoP remains below 60% for most wavelengths (see Saada)"; the Saada (Morocco) cases have 550 nm AOD of 0.334 and 0.184 (Table 1); clean dark sites reach "sky DoPs that approach 90% in the NIR". The paper gives no zenith DoP versus solar elevation series.
- Relevance to Study 3: independent radiative transfer support that desert aerosol plus bright ground caps the maximum DoP well below Rayleigh, so a dusty sky model must include both aerosol and surface albedo.

### 2.3 Feng, Zhang, Zhan, Fu, Duan, Li, Lu (2024). Fog aerosol and sky polarisation, model plus measurement
- Citation: Feng, X.; Zhang, S.; Zhan, J.; Fu, Q.; Duan, J.; Li, Y.; Lu, S. (2024). Effect of Foggy Environments on Sky Polarization Distribution. Acta Optica Sinica 44(19), 1912004. doi:10.3788/AOS241212
- URL: https://m.researching.cn/articles/OJaac2dad2364c3cc5
- Read: abstract.
- Facts: adding doubling vector radiative transfer checked against a fisheye polarisation camera; "The DOP values across the entire sky decrease as the solar altitude increases"; higher AOD lowers DoP, "with sea fog consistently exhibiting higher DOP values"; agreement "minimum PPMCC of 71.25% and a maximum RMSE of 26.81%".
- Relevance to Study 3: shows the model to measurement gap that a vector RT sky model can have under heavy aerosol (RMSE up to about 27 percent); fog, not dust, so it is an analogue only.

Not found: no opened source reported zenith DoP in a dust storm or under a measured dust AOD as a time series. Dust specific measured values remain a gap.

## 3. Multiple scattering, aerosol effects, neutral points, vector radiative transfer

### 3.1 DeLeon, Espinosa, Long, Shaw, Kupinski (2025). Neutral point position versus turbidity
- Citation: DeLeon, C. M.; Espinosa, W. R.; Long, Y.; Shaw, J. A.; Kupinski, M. (2025). Observing and simulating the polarization neutral point dependence on atmospheric turbidity. Proc. SPIE 13615, Polarization Science and Remote Sensing XII, 1361505. doi:10.1117/12.3062931
- URL: https://smartfires.mtnsfepscor.org/?p=6372
- Read: abstract.
- Facts: neutral point zenith angle is "highly sensitive to atmospheric turbidity"; ULTRASIP observations compared with GRASP radiative transfer driven by AERONET inputs; simulations "systematically overestimate the zenith separation"; slope and intercept correlations ρ = 0.522 and 0.439, improving when high aerosol days are excluded.
- Relevance to Study 3: a 2025 measured validation of vector RT under varying aerosol; the systematic bias under high loading is a caution for our dusty sky model and should appear in the limitations.

### 3.2 Pereira et al. (2025). Moonlit sky polarisation, Rayleigh plus Mie plus multiple scattering model
- Citation: Pereira, B.; González Gaitán, S.; Mourão, A. M.; Rino Silvestre, J.; Paulino Afonso, A.; Anderson, J. P.; Cikota, A.; Morales Garoffolo, A. (2025). Moonlit sky polarization patterns from Cerro Paranal. arXiv:2510.27308.
- URL: https://arxiv.org/pdf/2510.27308
- Read: full text (PDF).
- Facts: model combines single Rayleigh (with depolarisation factor), single Mie from a log normal aerosol distribution, and an unpolarised multiple scattering term; four neutral points (Babinet, Brewster, Arago, second Brewster) described with "The Berry singularity theory"; DoP "peaks near a 90° angular separation", falling from about 60 percent in B to about 30 percent in I; "multiple scattering becomes more dominant at the reddest bands".
- Relevance to Study 3: a recent, fully described, lightweight sky model architecture (single scatter plus depolarising multiple scatter term) close to what a fast simulator for VECTRA can use; desert site but not dust laden.

### 3.3 Wu, Zhang, Fan, Gao (2014). Analytical skylight model with multiple scattering
- Citation: Wu, L.; Zhang, J.; Fan, Z.; Gao, J. (2014). An analytical model for skylight polarization pattern with multiple scattering. Acta Physica Sinica 63(11), 114201. doi:10.7498/aps.63.114201
- URL: https://wulixb.iphy.ac.cn/en/article/doi/10.7498/aps.63.114201
- Read: abstract.
- Facts: model "takes into consideration the multiple scattering properties of atmospheric particles, especially the aerosol"; uses OPAC aerosol phase functions and a Perez sky; "Compared with the Rayleigh model, our model can depict the existence of neutral points in the sky".
- Relevance to Study 3: older key analytical alternative to full vector RT; reproduces neutral points, which a pure Rayleigh compass model cannot.

### 3.4 Zeng, Han, Wang (2008). Vector RT of skylight polarisation and aerosol vertical profile
- Citation: Zeng, J.; Han, Q.; Wang, J. (2008). High spectral resolution simulation of polarization of skylight: Sensitivity to aerosol vertical profile. Geophysical Research Letters 35, L20801. doi:10.1029/2008GL035645
- URL: https://espo.nasa.gov/polaris/node/9511
- Read: abstract.
- Facts: "Differences between simulated and measured polarization data in highspectral resolution are found to be within 1%"; near the O2 A band, surface DoLP "varies strongly and is sensitive to the vertical change of tropospheric aerosol mass"; with vertically uniform aerosol "such sensitivity is minimal at all wavelengths".
- Relevance to Study 3: supports using a column AOD driven RT model for broadband compass channels, since vertical profile matters mainly inside absorption bands.

## 4. Open measured sky polarisation datasets

### 4.1 Poughon, Aubry, Monnoyer, Viollet, Serres (2024). Two month annotated full sky polarimetric images
- Citation: Poughon, L.; Aubry, V.; Monnoyer, J.; Viollet, S.; Serres, J. R. (2024). An extended database of annotated skylight polarization images covering a period of two months. BMC Research Notes 17, 306. doi:10.1186/s13104-024-06959-6
- URL: https://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-024-06959-6 ; data: https://doi.org/10.57745/9L2YUB (Recherche Data Gouv). Licence: CC BY 4.0.
- Read: full text (article page).
- Facts: rooftop in Marseille, 6 July to 29 August 2022; about 40,000 images every 10 minutes from a Sony IMX250MYR colour polarimetric sensor with a 185 degree fisheye; "Data is manually annotated to help researchers to select the weather condition" (clear, mist, few, scattered, broken, overcast); "All provided files are Numpy data files"; includes a Rayleigh clear sky simulator and sun ephemeris calibration. Limitation stated: "Polarimetric images have been acquired over only two months."
- Relevance to Study 3: the best open real sky source for validating our sky model and per sample DoP weighting on unseen real skies; it is Mediterranean summer, not desert dust, so it tests transfer rather than dust.

### 4.2 Poughon et al. (2024). One month skylight polarisation dataset
- Citation: Poughon, L.; Aubry, V.; Monnoyer, J.; Viollet, S.; Serres, J. (2024). 1 Month long skylight polarization images dataset. Recherche Data Gouv. doi:10.57745/610QTS
- URL: https://b2find.eudat.eu/dataset/6416223f-b63d-5d23-b80b-d1c9fc59ec3d
- Read: metadata record.
- Facts: "A public database composed of real-world color polarimetric images" of the sky "in various weather condition"; La Timone, Marseille, about August 2022; marked open access, licence not named on the record (check at the DOI before use).
- Relevance to Study 3: an earlier subset of 4.1; cite 4.1 as the primary source and use this only if 4.1 is unavailable.

### 4.3 Liang and Bai. PSNS simulated dataset (not measured)
- Citation: Liang, H.; Bai, H. Polarized Skylight Navigation Simulation (PSNS) Dataset. arXiv:2007.13081. Venue and year of formal publication not stated on the opened PDF.
- URL: https://arxiv.org/pdf/2007.13081 ; data on Baidu Pan (link in the PDF); code: https://github.com/HuajuLiang/HypotheticalPolarizationCamera. Licence: not stated.
- Read: full text (PDF).
- Facts: about 138,000 simulated images with noise, edge illumination loss and clouds; roll and pitch are always zero; "the DOP of the whole sky decreases sharply with the increase of atmospheric turbidity".
- Relevance to Study 3: simulated only and unlicensed, so not usable as evidence; useful as a design comparison for our simulator.

Not found: no opened source offers a downloadable zenith DoP time series or full sky polarisation images from a desert or dust event.

## 5. Polarisation or sun compass fused with VO or VIO, and VIO robustness in planetary or desert analogues

### 5.1 Steidle, Stürzl, Triebel (2019). Polarisation compass inside a VIO EKF
- Citation: Steidle, F.; Stürzl, W.; Triebel, R. (2019). Visual inertial sensor fusion with a bio inspired polarization compass for navigation of MAVs. IMAV 2019, Madrid.
- URL: https://elib.dlr.de/131074
- Read: abstract (full PDF restricted).
- Facts: the compass "estimates the position of the sun indirectly from the pattern of skylight polarization"; fused with IMU and visual odometry in an indirect EKF; adding it "does not only eliminate the drift of yaw angle estimates" but improves the overall state; two integration variants compared; no numbers on the abstract page.
- Relevance to Study 3: the direct prior art for compass plus VIO fusion; any Study 3 claim must be about dust aware weighting and evaluation, not about the fusion itself.

### 5.2 Shan, Guo, Li, Tao (2025). LPVIMO SAM: polarisation imagery as features, magnetometer for heading
- Citation: Shan, D.; Guo, P.; Li, W.; Tao, D. (2025). LPVIMO SAM: Tightly coupled LiDAR/Polarization Vision/Inertial/Magnetometer/Optical Flow Odometry via Smoothing and Mapping. arXiv:2504.20380; doi:10.1109/IROS60139.2025.11247522
- URL: https://arxiv.org/abs/2504.20380
- Read: abstract.
- Facts: "The magnetometer acquires the heading angle, and the optical flow obtains the speed and height"; polarisation is used for "extracting the polarization information of the scene" to help low texture VIO; "can maintain stable positioning even when one of the two subsystems fails".
- Relevance to Study 3: a 2025 polarisation plus VIO system that does not use skylight as a compass, which leaves the dusty sky compass aiding VO question open.

### 5.3 Giubilato et al. (2026). S3LI Vulcano planetary analogue dataset and VIO baselines
- Citation: Giubilato, R.; Müller, M. G.; Sewtz, M.; Encinar Gonzalez, L. A.; Folkesson, J.; Triebel, R. (2026). The S3LI Vulcano Dataset: A Dataset for Multi Modal SLAM in Unstructured Planetary Environments. arXiv:2601.19557.
- URL: https://arxiv.org/pdf/2601.19557 ; data: rmc.dlr.de/s3li_dataset ; toolkit: github.com/DLR-RM/s3li-toolkit. Dataset licence not stated in the paper.
- Read: full text (PDF).
- Facts: stereo, LiDAR, IMU, D GNSS on volcanic terrain; R VIO2, VINS Fusion and SqrtVINS evaluated, with initialisation failures and lost tracking reported; "Natural environments are characterized by extreme perceptual aliasing and abundance of ambiguous features"; large errors come from "single failure events along the path, and are not indicative of constant drift". No mention of sun or polarisation.
- Relevance to Study 3: 2026 evidence that analogue VIO failures are episodic, which argues for reporting failure counts and consistency, not only mean drift; also a candidate unseen environment for VO only checks.

### 5.4 Zhang, Huang, Xu, Ye, Xiao, Tong (2025). Visual LiDAR odometry on the Erfoud dataset
- Citation: Zhang, L.; Huang, R.; Xu, Y.; Ye, Z.; Xiao, C.; Tong, X. (2025). Visual LiDAR Odometry for Planetary Rover with Plane Constraints. ISPRS Archives XLVIII G 2025, 1699 to 1705 (ISPRS Geospatial Week 2025, Dubai). doi:10.5194/isprs-archives-XLVIII-G-2025-1699-2025
- URL: https://isprs-archives.copernicus.org/articles/XLVIII-G-2025/1699/2025/
- Read: abstract.
- Facts: planetary terrain is "GNSS-denied and characterized by low texture and unstructured surfaces"; ground plane constraints reduce attitude drift; on Erfoud, ATE of 3.334 % and 3.869 % of trajectory length.
- Relevance to Study 3: a 2025 desert analogue drift baseline (about 3 to 4 percent of distance) against which compass aided heading gains can be compared.

### 5.5 Meyer et al. (2021). MADMAX dataset, Erfoud region, Morocco
- Citation: Meyer, L. et al. (2021). The MADMAX data set for visual inertial rover navigation on Mars. Journal of Field Robotics. doi:10.1002/rob.22016
- URL: https://www.dlr.de/en/rm/research/publications-and-downloads/datasets/marokko-navigations-tests ; data: https://datasets.arches-projekt.de/morocco2018/
- Read: dataset page (not the paper).
- Facts: recorded in 2018 in the Moroccan desert "close to the city of Erfoud"; "36 different navigation experiments, captured at eight Mars analog sites of widely varying environmental conditions"; stereo, colour and omnidirectional cameras plus IMU, RTK GNSS ground truth. No dataset licence stated on the page.
- Relevance to Study 3: real desert imagery suitable for an unseen environment VO check; it has no polarisation channel, so compass inputs would have to be simulated from logged time and position.

### 5.6 Singh, Khattak, Goel, Paton, Alexis, Nesnas. BEVIO for lunar day and night VIO
- Citation: Singh, M.; Khattak, S.; Goel, A.; Paton, M.; Alexis, K.; Nesnas, I. A. BEVIO: Efficient Bird's Eye View based Sparse Update Visual Inertial Odometry for Lunar Day Night Navigation. arXiv:2606.00709 (June 2026 identifier; the PDF carries a 2025 copyright line).
- URL: https://arxiv.org/pdf/2606.00709
- Read: full text (PDF).
- Facts: integrated into xVIO and field tested with the ERNEST rover at Plaster City, California (desert); "enables reliable day and nighttime self-illuminated traverses at visual update rates as low as 0.25 Hz"; in daylight image space matching gives more matches but mostly distant, low parallax features.
- Relevance to Study 3: recent desert field VIO showing sunlight conditions change which features are useful; no absolute heading aid is used.

### 5.7 Boirum (2015). Continuous sun tracking for rover absolute bearing
- Citation: Boirum, C. (2015). Improving Localization of Planetary Rovers with Absolute Bearing by Continuously Tracking the Sun. Master's thesis, Carnegie Mellon University, CMU RI TR 16 01.
- URL: https://ri.cmu.edu/?p=4512
- Read: abstract.
- Facts: proposes "using a visual sun compass as a navigational aid to continuously determine absolute bearing"; uses "a high rate 187° field of view visual sun compass"; no numerical results on the abstract page.
- Relevance to Study 3: older key sun compass for rovers; direct sun sensing fails under thick dust whereas polarisation degrades gradually, which is the gap VECTRA targets.

## Novelty check

Among the works opened in this scan, none combines (a) a radiative transfer sky model with dust coupled to camera degradation, (b) per sample DoP weighted compass fusion with VO, and (c) confirmation on unseen environments. Part (a) is only partly covered: vector RT with aerosol is established (Pust and Shaw 2012; Zeng et al. 2008; Feng et al. 2024; DeLeon et al. 2025), and Su et al. (2026) test a compass in dust, but no opened work couples a dusty sky model to degradation of the navigation camera images. Part (b) is not new as a principle: Stürzl (2017) estimates a per measurement covariance, Steidle et al. (2019) fuse a polarisation compass with VIO, and Wang et al. (2024) adapt compass noise with a chi square test, so the defensible novelty is the specific physically grounded DoP weight under dust and its consistency analysis, not uncertainty aware fusion as such. Part (c) has open ingredients (Poughon et al. 2024 real sky images under CC BY 4.0; MADMAX and S3LI for VO), but no opened work evaluates a compass aided VO pipeline on held out environments. On this evidence, the combination of (a), (b) and (c) appears new, while each component taken alone has clear prior art that must be cited.

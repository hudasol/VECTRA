# A. Biology and insect-inspired robotics: source notes

Compiled 2026-11-01. Every fact below was taken from a page or file opened in this session. Reading levels:
- FULL = full text read.
- FULL-via-summariser = the fetch tool returned a model-written digest of the full document, not raw text. Quotes from these must be re-checked against the PDF before publication.
- ABSTRACT = abstract only.
- PRESS = press release or marketing page.

DOIs were taken from Crossref or PubMed records returned in this session, or from the opened page itself.

---

## 1. Desert ant path integration (Cataglyphis)

### 1.1 Muller and Wehner 1988 (PNAS)
- Citation: Muller M, Wehner R (1988). Path integration in desert ants, Cataglyphis fortis. Proc Natl Acad Sci USA 85(14):5287-5290. doi:10.1073/pnas.85.14.5287 (PubMed PMID 16593958; PMC281735).
- Read: ABSTRACT only (PubMed record via NCBI E-utilities). Full text blocked: PMC served a reCAPTCHA page, pnas.org returned 403, Europe PMC returned 403.
- Facts:
  - The ants do not do exact vector summation. Quote: "not by performing a true vector summation ... but by employing a computationally simple approximation."
  - The approximation leaves systematic errors. Quote: "small, but systematic, navigational errors."
  - Error magnitudes in degrees or percent are NOT available from the abstract. Do not state numbers from this paper without opening the full text.

### 1.2 Ronacher 2020 (review from the Wehner school, on 3-D path integration)
- Citation: Ronacher B (2020). Path integration in a three-dimensional world: the case of desert ants. J Comp Physiol A 206(3):379-387. doi:10.1007/s00359-020-01401-1 (open access, CC BY 4.0).
- Read: FULL (PMC page fetched at ncbi.nlm.nih.gov/pmc/articles/PMC7192874).
- Facts:
  - Compass: "walking directions are derived primarily via a sky compass that takes advantage of the sun azimuth position and the polarization pattern of the sky." Other cues include spectral gradients and wind direction.
  - Step counting: "Cataglyphis uses a pedometer, more precisely a stride integrator, to assess travelled distances" (citing Wittlinger et al. 2006, 2007).
  - Robustness: the stride integrator survives "carrying heavy prey, walking backwards, or even the loss of one or two legs."
  - Error budget (the author's estimate, not a measurement): if an ant misjudged inclination by 12.5 degrees, the home-vector error would be "less than 7 degrees for slopes up to 45 degrees."
  - The review also reports that ants on a 45 to 60 degree training slope show a marked behavioural change in slope detection. Slope measurement is "roughly constant up to a 45 degree inclination."

### 1.3 Wittlinger, Wehner and Wolf 2006 (stilts and stumps)
- Citation: Wittlinger M, Wehner R, Wolf H (2006). The ant odometer: stepping on stilts and stumps. Science 312(5782):1965-1967. doi:10.1126/science.1126912.
- Read: ABSTRACT only (PubMed).
- Facts:
  - Quote: "Travel distance is overestimated by experimental animals walking on stilts and underestimated by animals walking on stumps."
  - Quote: "They continuously integrate directions steered (as determined by their celestial compass) and distances traveled."

### 1.4 Sommer and Wehner 2004 (distance underestimation)
- Citation: Sommer S, Wehner R (2004). The ant's estimation of distance travelled: experiments with desert ants, Cataglyphis fortis. J Comp Physiol A 190(1):1-6. doi:10.1007/s00359-003-0465-4.
- Read: ABSTRACT only (PubMed).
- Facts:
  - Quote: "ants tend to underestimate their distances travelled. This underestimation is the more pronounced, the larger the foraging distance gets."
  - Odometer error is therefore distance dependent and biased, described by "a logarithmic and an exponential model." The authors argue the bias may be adaptive, because it concentrates nest search on the familiar landmark corridor.

### 1.5 Muller and Wehner 2007 (wind and sky compass cues)
- Citation: Muller M, Wehner R (2007). Wind and sky as compass cues in desert ant navigation. Naturwissenschaften 94(7):589-594. doi:10.1007/s00114-007-0232-4.
- Read: ABSTRACT only (PubMed). The rero.ch full-text link returned 410.
- Facts:
  - Quote: "it is only the polarization compass that invariably outcompetes the wind compass."
  - The sun compass wins "only under certain conditions." Ants deprived of the polarization compass steer intermediate courses between the sun and wind compasses.

### 1.6 Wehner 2003 (review essay)
- Citation: Wehner R (2003). Desert ant navigation: how miniature brains solve complex tasks. J Comp Physiol A 189(8):579-588. doi:10.1007/s00359-003-0431-1.
- Read: ABSTRACT only (PubMed).
- Facts:
  - The ant toolkit is listed as "its skylight (polarization) compass, its path integrator, its view-dependent ways of recognizing places and following landmark routes."
  - Quote: "Cataglyphis uses path integration as an egocentric guideline to acquire continually updated spatial information."

### 1.7 Voegeli, Sommer, Knaden and Wehner 2025 (path-integration vectors)
- Citation: Voegeli B, Sommer S, Knaden M, Wehner R (2025). Vector-based navigation in desert ants: the significance of path-integration vectors. J Comp Physiol A 211(2):209-220. doi:10.1007/s00359-024-01725-2.
- Read: abstract from PubMed, plus the article body via the fetch tool. The body is FULL-via-summariser, so re-check the quotes.
- Facts:
  - Quote: "optimal combination of path-integration vectors and view-based vectors."
  - Quote: "path integration is a necessary requirement even for providing the navigational system with landmark information."
  - Quote: "their path integrator is reset to zero-state only when the animals have returned to the nest."
  - Feeder distances were 4.5 m and 5.7 m. The summariser reports no quantitative path-integration error rate in this paper.

### 1.8 Horvath and Wehner 1999 (skylight polarization as ants perceive it)
- Citation: Horvath G, Wehner R (1999). Skylight polarization as perceived by desert ants and measured by video polarimetry. J Comp Physiol A 184:1-7. doi:10.1007/s003590050300.
- Read: FULL-via-summariser (arago.elte.hu PDF).
- Facts:
  - Quote: "never exceeded mean values of d = 60% (and 75% in individual pixels of sky)." Measurements were taken under clear sky in three Tunisian habitats.
  - Degree of polarization (d) is "much more affected by atmospheric disturbances and surface reflections than is the angle of polarization." Digest-level claim: the angle of polarization was largely unaffected by atmospheric conditions.
  - The paper did NOT test cloud cover as a variable. It is not a direct source for cloud failure of the sky compass.

### 1.9 Merkle, Rost and Alt (arXiv q-bio/0512031, 2005): egocentric path-integration models
- Citation: Merkle T, Rost M, Alt W. Egocentric Path Integration Models and their Application to Desert Arthropods. arXiv:q-bio/0512031 (14 Dec 2005). Journal venue not checked.
- Read: abstract and introduction (PDF text via pdftotext).
- Facts:
  - Quote: "we propose several possible types of systematic errors that can cause deviations from the correct homeward course."
  - Local landmark vectors are error-prone. Quote: "since landmarks can disappear or change their appearance."
  - The global vector is the fallback after landmark failure (citing Ziegler and Wehner 1997).

---

## 2. Stone et al. 2017 (bee central complex model)
- Citation: Stone T, Webb B, Adden A, Weddig NB, Honkanen A, Templin R, Wcislo W, Scimeca L, Warrant E, Heinze S (2017). An anatomically constrained model for path integration in the bee brain. Curr Biol 27(20):3069-3085.e11. doi:10.1016/j.cub.2017.08.052 (PMC6196076; PMID 28988858).
- Read: FULL (PMC XML via NCBI E-utilities; the PMC HTML page was blocked by reCAPTCHA).
- Facts:
  - Robot test, directly relevant to a visual-inertial design. Quote: "using camera-perceived optic flow and inertial-rotation based compass estimation as inputs."
  - Result: after outbound journeys of 6-12 m, the circuit returned the robot "to within an average of 16 cm of home (SD 11.1 cm; n=10)."
  - Noise: the simulated network is "robust to added noise of 10-20%." Fixed noise on connection weights is more damaging than per-step noise.
  - Memory limit: routes of up to 5000 steps give accurate returns, while "very long routes (>20,000 steps) start to saturate the memory" with distance undershoot.
  - Model scope: it explicitly supports holonomic motion, where ground velocity is not aligned with body orientation.

---

## 3. Polarised-light compass robots

### 3.1 Lambrinos et al. 2000 and 1997 (Sahabot)
- Citation: Lambrinos D, Moller R, Labhart T, Pfeifer R, Wehner R (2000). A mobile robot employing insect strategies for navigation. Robotics and Autonomous Systems 30(1-2):39-64. doi:10.1016/S0921-8890(99)00064-0.
- Earlier paper: Lambrinos D, Kobayashi H, Pfeifer R, Maris M, Labhart T, Wehner R (1997). An autonomous agent navigating with a polarized light compass. Adaptive Behavior 6(1):131-161. doi:10.1177/105971239700600104.
- Read: the 2000 paper itself is UNOPENED (ScienceDirect 403). What I read:
  - the University of Zurich Labhart-lab project page that describes both papers (curl, FULL page);
  - the metadata page for the 1997 paper (fetch digest; the abstract was paraphrased only).
- Facts, all from the UZH project page, https://mls.uzh.ch/en/research/fgrimls/Labhart/ModelsRobots/MobileRobot.html:
  - Sensor layout. Quote: "three polarization-opponent sensors (POL-OP units) ... directed to the zenith", tuned to e-vector orientations "parallel, 60 degrees and 120 degrees to the robots' long axis."
  - Sahabot 2 added path integration. Quote: "Sahabot 2 ... was equipped with a path integration mechanism." It also had a camera system for landmark navigation.
  - Accuracy. Quote: "The navigational precision was comparable to that of the desert ant Cataglyphis bicolor."
  - Control experiment. Quote: "precision of orientation dropped dramatically when the polarization compass was replaced by proprioreception."
  - Method comparison. The instantaneous method of comparing the three POL-OP units was "slightly more exact" than the sequential rotating method.
  - No numeric error is given on that page. Do not quote numbers for Sahabot without the paper.

### 3.2 Chu group polarization sensors
- Opened (ABSTRACT, via DOAJ record, fetch digest): Wang Y, Chu J, Zhang R, Li J, Guo X, Lin M (2019). A bio-inspired polarization sensor with high outdoor accuracy and central-symmetry calibration method with integrating sphere. Sensors 19(16):3448. doi:10.3390/s19163448.
- Facts (digest-level, so check wording against the abstract):
  - Indoor accuracy of +/-0.009 degrees.
  - Static outdoor accuracy of +/-0.05 degrees under clear skies.
  - Dynamic tests show a +/-0.5 degree heading deviation relative to an inertial navigation system.
  - Indoor calibration parameters performed poorly outdoors and had to be replaced with an outdoor value, driven mainly by the spectrum of the incoming light.
  - This is a sensor paper, not a robot homing test.
- Chu et al. 2008 (Sensors and Actuators A 148(1):75-82, doi:10.1016/j.sna.2008.07.016) is UNOPENED.

### 3.3 AntBot: Dupeyroux, Serres and Viollet 2019 (Science Robotics)
- Citation: Dupeyroux J, Serres JR, Viollet S (2019). AntBot: A six-legged walking robot able to home like desert ants in outdoor environments. Science Robotics 4(27):eaau0307. doi:10.1126/scirobotics.aau0307 (PubMed PMID 33137736).
- Read: ABSTRACT (PubMed) and the CNRS press release (full). The Science page returned 403.
- Facts, from the abstract:
  - Quote: "The mean homing error recorded during the overall trajectory was as small as 0.67% under lighting conditions similar to those encountered by ants."
  - Sensor budget: "two optical sensors equipped with just 14 pixels, two of which were dedicated to an insect-inspired compass." The other 12 pixels were for optic flow.
  - The compass with two rotating polarizers was "equivalent to two costly arrays composed of 374 photosensors."
  - Motivation. Quote: "most of them are still prone to considerable drift and uncertainty."
- Facts, from the CNRS press release (https://www.cnrs.fr/en/press/first-walking-robot-moves-without-gps). These are press claims only and are NOT verified against the paper:
  - "precision of up to 1 cm after having covered a total distance of 14 meters."
  - "measures its heading with 0.4 degree precision by clear or cloudy weather."
  - The robot weighs 2.3 kg.
  - The press text says the optical movement sensor is "directed to the sun." This is likely loose wording, so do not repeat it. Check the paper for the optic-flow sensor orientation.

### 3.4 Dupeyroux et al. IROS 2017 and ECMR 2017
See UNOPENED. Crossref confirms:
- A novel insect-inspired optical compass sensor for a hexapod walking robot. IROS 2017, pp. 3439-3445. doi:10.1109/IROS.2017.8206183.
- A bio-inspired celestial compass applied to an ant-inspired robot for autonomous navigation. ECMR 2017. doi:10.1109/ECMR.2017.8098680.

### 3.5 Gattaux et al.: Antcar (visual route following and homing)
**(a) Nature Communications 2025**
- Citation: Gattaux GG, Wystrach A, Serres JR, Ruffier F (2025). Route-centric ant-inspired memories enable panoramic route-following in a car-like robot. Nat Commun 16. doi:10.1038/s41467-025-62327-3. Article number not recorded.
- Read: FULL (nature.com open access page).
- Facts:
  - Quote: "tested over 1.6 km across 113 challenging real-world trials."
  - Quote: "less than 25 cm median lateral error using minimal resources (800-pixel input, 300 MB RAM, 500 mW power, and 18.75 kB memory per 50 m route)."
  - Cloudy-day reverse route of 50 m: lateral error 0.9 +/- 0.5 m and angular error 6.3 +/- 4.2 degrees (median +/- MAD).
  - Background. Quote: "experienced solitary foraging ants navigate along familiar routes using only visual memories, without relying on dead reckoning."
  - This is route following, not path integration.

**(b) arXiv 2025**
- Citation: Gattaux GG, Serres JR, Ruffier F, Wystrach A. Visual Homing in Outdoor Robots Using Mushroom Body Circuits and Learning Walks. arXiv:2507.09725 (13 Jul 2025). Venue not stated in the PDF.
- Read: FULL (PDF text).
- Facts:
  - Quote: "purely path-integration-based methods are prone to drift due to cumulative sensor errors."
  - Homing and search worked "up to 18 meters from the nest" using a GPS-RTK-emulated, noisy path-integration signal as the learning scaffold.
  - The onboard system runs at 8 Hz on a Raspberry Pi 4 with 32x32 pixel views and under 9 kB of memory.

---

## 4. De Croon et al. 2022 and MAVLab / TU Delft

### 4.1 De Croon, Dupeyroux, Fuller and Marshall 2022
- Citation: de Croon GCHE, Dupeyroux JJG, Fuller SB, Marshall JAR (2022). Insect-inspired AI for autonomous robots. Science Robotics 7(67):eabl6334. doi:10.1126/scirobotics.abl6334.
- Read:
  - the TU Delft portal abstract and the MAVLab summary page (curl, FULL pages);
  - the TU Delft repository PDF via the fetch tool, which is FULL-via-summariser. Page numbers are as reported by the summariser. Re-check quotes against the PDF.
- Facts:
  - Quote: "Path integration has been successfully implemented onboard wheeled and legged robots with remarkable accuracy" (p. 4, no figure given).
  - The review gives no quantitative account of path-integration drift. It lists the limits of the field instead. Quote: "there are no scientific studies yet that demonstrate insect-inspired navigation methods working robustly" (p. 5).
  - Quote: "a robot traveled outdoor paths of ~100 m with a memory requirement of 3 megabytes (MB)/km" (p. 4). It contrasts this with SLAM maps needing "hundreds of megabytes."
  - Neuromorphic example: Loihi PID control at "an average 0.0126 mW power consumption per time stamp for a total of 40,000 neurons" (p. 7). Another example: "an SNN composed of only 35 spiking neurons controlled a flying robot" (p. 7).
  - Opteran disclosure. Quote: "J.A.R.M. is the chief scientific officer and cofounder of Opteran" (p. 10).
  - AntBot is shown in the review (Fig. 1) as a hexapod with a UV sensor.

### 4.2 Firlefyn, Hagenaars and de Croon 2024
- Citation: Firlefyn MVM, Hagenaars JJ, de Croon GCHE. Direct learning of home vector direction for insect-inspired robot navigation. arXiv:2405.03827 (6 May 2024). Venue not stated in the PDF.
- Read: FULL (PDF text).
- Facts:
  - Quote: "come back by means of odometry, and eliminate the resultant drift by inferring the home vector orientation from the currently experienced view."
  - Quote: "average errors of the inferred home vectors in general stay well below the 90 degrees required for successful homing, and below 24 degrees if all images contain sufficient texture and illumination."
  - The drift correction works "as long as this drift falls within the region explored during the learning flights."
  - Bee and wasp foraging trips of "up to 13.5 km" are cited as motivation.

### 4.3 Other MAVLab neuromorphic work
Titles only (arXiv search result lists), not opened: arXiv:2303.08778 (fully neuromorphic vision and control for autonomous drone flight), arXiv:2011.00534 (Loihi optic-flow landing), arXiv:2103.02751 (neuromorphic sensing toolbox). See UNOPENED.

---

## 5. Opteran (commercial insect-brain navigation)
- Sources: https://opteran.com/ and https://opteran.com/opteran-mind/ (company pages).
- Read: PRESS (marketing pages, FULL). No peer-reviewed Opteran paper or technical page was found or opened. The de Croon review discloses Opteran's involvement (see 4.1).
- Facts, all company claims:
  - Quote: "GPS free navigation indoors and outdoors, simply learning a new space by being shown it."
  - Quote: "Infrastructure-free map building at 1KB/m2 without post-processing."
  - A SAFELOG quote on the site says the localization "outperforms existing systems such as LiDAR or SLAM." That is a company or partner assertion, with no accuracy figure.
  - The site makes no stated claims about night or cloud performance.

---

## 6. Explicit limitations of path integration, sky compass, and related robotics results

| Limitation | Source | Reading level | Exact support |
|---|---|---|---|
| Error accumulation in robot path integration | Gattaux et al. arXiv 2507.09725 | FULL | "purely path-integration-based methods are prone to drift due to cumulative sensor errors" |
| Odometric drift must be corrected by views | Firlefyn et al. arXiv 2405.03827 | FULL | Drift removed by learned home-vector direction, valid only while drift stays within the learning-flight region |
| Systematic biases in the ant itself | Muller and Wehner 1988; Sommer and Wehner 2004 | ABSTRACT | "small, but systematic, navigational errors"; distance underestimation grows with distance |
| Memory saturation of the integrator | Stone et al. 2017 | FULL | Distance undershoot beyond >20,000 steps in the simulated circuit |
| Path integrator must be reset or fused with views | Voegeli et al. 2025; Wehner 2003 | digest / ABSTRACT | Reset only at the nest; "optimal combination" of path integration and view vectors |
| Robotics evidence gap | de Croon et al. 2022 | digest | "no scientific studies yet that demonstrate insect-inspired navigation methods working robustly" |
| Night failure of the sky compass | Freas et al. 2024 (eLife) | digest only | Moonlight is "a million times dimmer than sunlight." With no moon, ants "did not significantly alter their paths" under the filter. |
| Cloud failure of the sky compass | NO primary source found | n/a | Horvath and Wehner 1999 tested clear skies only. AntBot press release claims 0.4 degrees "by clear or cloudy weather" (press only). |

Freas et al. 2024 (eLife 13:RP97615, https://elifesciences.org/articles/97615):
- Read via fetch digest only. DOI not confirmed in this session.
- Species: nocturnal bull ants, Myrmecia midas.
- Authors: Freas CA, Narenda A, Murray T, Cheng K.
- Numbers from the digest: 62.8% of the daily foraging force returns at night; the cue works under a crescent moon of about 20% illumination.

---

## UNOPENED (could not read the source, with reason)

| Item | Reason |
|---|---|
| Muller and Wehner 1988 full text | PMC reCAPTCHA, pnas.org 403, Europe PMC 403. Only the abstract was read. |
| Dupeyroux et al. 2019 AntBot full text | science.org 403. Only the PubMed abstract and the CNRS press release were read. |
| Lambrinos et al. 2000 full text | ScienceDirect 403. Only the UZH project page and the 1997 metadata page were read. |
| Dupeyroux et al. IROS 2017 and ECMR 2017 | HAL pages are behind an Anubis bot wall (fetch tool also denied), and IEEE was not reachable. DOIs are from Crossref, with no content read. |
| Chu et al. 2008 (Sens Actuators A 148:75-82) | Paywalled. DOI is from Crossref. |
| Gattaux et al. Antcar 2023 (Frontiers in Neurorobotics) | The HAL and ISM pages 404 or were blocked. No verified DOI, so none is given. The 2025 Nat Commun paper covers Antcar instead. |
| Wehner reviews: Wehner and Srinivasan 2003, JEB review PDFs, Wehner 2020 monograph, and the imls.uzh.ch PDFs | 403, or a silverchair stub. Only the PubMed abstracts and the Ronacher review were read. |
| MAVLab neuromorphic papers (arXiv 2303.08778, 2011.00534, 2103.02751) | Listed in arXiv search only. The Loihi power figures above come from the de Croon review digest. |
| Europe PMC REST, Semantic Scholar, OpenAlex | 403 or rate-limited (429). Crossref and NCBI E-utilities were used instead. |
| SPIE "Challenges for biomimetic night-time sky polarization navigation" (doi 10.1117/12.2219083) | Page returned only meta tags. |
| Opteran peer-reviewed paper | None found. Only company marketing pages were read. |
| Primary measurement of sky-compass failure under cloud | Not found in any opened source. |

---

## Synthesis: what is established vs. unknown under degraded sensing

1. Established: Cataglyphis combines a polarised-skylight and sun compass with a stride-counting odometer (stilts and stumps experiments), and the sky compass dominates other compass cues when it is available.
2. Established: the ant integrator is imperfect by design. It makes small systematic errors and underestimates distance more as the foraging distance grows (Muller and Wehner 1988; Sommer and Wehner 2004). Error magnitudes in degrees are not available without the full texts.
3. Established: bee-inspired central-complex circuits can run on a robot with optic flow plus an inertial compass, returning to within about 16 cm after 6-12 m outbound (Stone et al. 2017). This is the closest published analogue to a heading cue plus visual-inertial estimate, and it was tested on a single platform over short ranges only (n=10).
4. Established: polarisation-compass robots reach ant-like accuracy under clear daylight. AntBot reports 0.67% mean homing error, and Sahabot is reported "comparable" to Cataglyphis. Lambrinos' result that proprioceptive heading is far worse is the key comparator for a GNSS-free ground robot.
5. Established (robotics side): path integration alone drifts, and recent insect-inspired work pairs it with learned views to cancel the drift (Firlefyn et al. 2024; Gattaux et al. 2025).
6. Established (biology side): ants themselves use path integration together with views and landmarks, and the integrator seems necessary for learning those views (Wehner 2003; Voegeli et al. 2025).
7. Partly known: night operation. Some nocturnal ants use polarised moonlight, but it fails or weakens when the moon is absent (Freas et al. 2024). Daytime desert ants are not shown to cope with darkness.
8. Unknown or unsupported in what I opened: cloud and overcast degradation of an ant-style polarisation compass, with measured heading error. Only press-level claims (AntBot, 0.4 degrees under cloud) and a clear-sky-only measurement paper were found.
9. Unknown: long-range drift of an ant-inspired integrator on a wheeled or legged robot over hundreds of metres. The review concedes no study yet shows insect-inspired navigation "working robustly" (de Croon et al. 2022).
10. Unknown or unverifiable: commercial insect-brain navigation (Opteran) has no peer-reviewed accuracy figures in what I could open, so cite it only as a company claim.

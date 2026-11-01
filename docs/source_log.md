# Source log

One row per source. "Read how" records whether we opened the page ourselves or only saw a summary from a fetch tool.

| # | Link | Access date | Type | Use | Licence as stated | Read how |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | https://docs.openvins.com/getting-started.html | 2026-10-19 | Software documentation | Required inputs, supported datasets, run routes | Not checked on this page; see repository licence | Fetch tool summary |
| 2 | https://docs.openvins.com/gs-datasets.html | 2026-10-19 | Software documentation | Dataset list, ROS bag format, calibration and time sync notes | Not checked | Fetch tool summary |
| 3 | https://docs.openvins.com/gs-installing.html | 2026-10-19 | Software documentation | Install routes including Docker | Not checked | Fetch tool summary |
| 4 | https://docs.openvins.com/gs-calibration.html | 2026-10-19 | Software documentation | Kalibr style calibration, IMU noise parameters | Not checked | Fetch tool summary |
| 5 | https://docs.openvins.com/gs-tutorial.html | 2026-10-19 | Software documentation | Tutorial run steps | Not checked | Fetch tool summary |
| 6 | https://tartanair.org/tartanground | 2026-10-19 | Dataset page (official) | Sensors, sizes, download method | Not stated (copyright notice only) | Fetch tool summary |
| 7 | https://arxiv.org/abs/2505.10696 | 2026-10-19 | Paper (preprint) | Dataset description, trajectory counts | Not applicable | Abstract and summary |
| 8 | https://docs.voxel51.com/dataset_zoo/datasets_hf/tartanground.html | 2026-10-19 | Third party page | Mentions a subset hosted elsewhere | Page states CC BY 4.0 for the subset | Fetch tool summary; secondary source only |
| 9 | https://arxiv.org/abs/2505.10696 | 2026-11-01 | Paper (preprint, v2 of 30 Jul 2025) | 878 trajectories, 63 environments, six stereo cameras, 10 Hz poses, IMU mentioned only as post processing output | No licence in the paper | Full text read |
| 10 | https://arxiv.org/abs/2003.14338 | 2026-11-01 | Paper (preprint) | TartanAir design, weather list, statement that dark scenes are poorly simulated | No licence in the paper | Full text read for sections I to V |
| 11 | https://tartanair.org/modalities.html | 2026-11-01 | Dataset documentation (official) | 10 Hz cameras, IMU derived from the pose by spline differentiation, noise code provided | See row 12 | Page read |
| 12 | https://tartanair.org/ | 2026-11-01 | Dataset documentation (official) | Licence text for TartanAir V2 | CC BY 4.0 for the dataset, MIT for the toolkit (TartanAir V2 only) | Page read |
| 13 | https://arxiv.org/abs/1708.03852 | 2026-11-01 | Paper (VINS-Mono) | Drift confined to four degrees of freedom | Not applicable | Full text read |
| 14 | https://arxiv.org/abs/2510.10979 | 2026-11-01 | Paper (preprint, AMO-HEAD) | Closest prior art for adaptive weighting of a heading cue | Not applicable | Full text read |
| 15 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8638515/ | 2026-11-01 | Paper (review of adaptive filtering) | Covariance matching, identifiability counter example | Open access | Full text read |
| 16 | https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf | 2026-11-01 | Paper (trajectory evaluation tutorial) | Alignment follows unobservable degrees of freedom | Not applicable | Full text read |
| 17 | https://elib.dlr.de/141662/1/rob.22016.pdf | 2026-11-01 | Paper (MADMAX data set) | Real Sahara analogue data, dual antenna heading ground truth, no magnetometer | Article is CC BY; data set licence not seen | Full text read |
| 18 | https://arxiv.org/abs/2608.30690 | 2026-11-01 | Paper (preprint) | Graded corruption evaluation for monocular SLAM, failure versus drift | Not applicable | Full text read |
| 19 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6196076 | 2026-11-01 | Paper (Stone et al. 2017) | Robot test with optic flow and inertial compass, 16 cm average return error | Open access | Full text read through the NCBI service |
| 20 | https://pubmed.ncbi.nlm.nih.gov/ (AntBot, PMID 33137736) | 2026-11-01 | Abstract | 0.67 percent mean homing error | Not applicable | Abstract only |
| 21 | https://www.icao.int/Meetings/MIDANPIRG-RASG/Documents/WP%2069.pdf | 2026-11-01 | Regulator working paper | 37,770 reported GPS signal loss events in the Middle East region in 2023 | Not stated | Fetch tool summary |
| 22 | https://ad.easa.europa.eu/blob/EASA_SIB_2022_02R4.pdf/SIB_2022-02R4_1 | 2026-11-01 | Regulator bulletin | Jamming and spoofing increase since February 2022 | Not stated | Fetch tool summary |
| 23 | https://mscio.eu/media/documents/20260402_MSCIO_ADVISORY_01_2026._UPDATE_12.pdf | 2026-11-01 | Maritime advisory | Dead reckoning advised, disruptions persisted | Not stated | Fetch tool summary |

## Conflicts and open questions

1. Licence. The TartanGround paper and the official page state no licence. The TartanAir V2 documentation states CC BY 4.0 and an MIT toolkit (row 12), and a third party page (row 8) says CC BY 4.0 for a subset. We still treat the TartanGround licence as unverified until it is confirmed on an official source.
2. IMU rate. Not stated in the paper or the official page. The TartanAir documentation describes an IMU interpolated from the pose with no noise unless noise is added (row 11). Whether TartanGround does the same is not verified.
3. Trajectory and environment counts. The paper text we opened is v2 dated 30 Jul 2025 and gives 878 trajectories in 63 environments. A figure of 70 environments and 910 trajectories for an earlier version is plausible but unverified, because we did not open v1.
4. Download size. The paper says about 15 TB and the official page about 16 TB. Subsets will be used.
5. Rows marked "Fetch tool summary" must be re-read directly before any statement from them goes into a paper.

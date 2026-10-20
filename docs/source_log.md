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

## Conflicts and open questions

1. Licence. The official TartanGround page states no licence. A third party page (row 8) says the source dataset is released under CC BY 4.0. We treat the licence as unverified until Aiman's check (task A1) confirms it on an official source.
2. IMU rate. Not stated on the official page. Needed before any OpenVINS run.
3. Trajectory and environment counts. The paper abstract gives 878 trajectories in 63 environments. Another text we saw gave different figures. To be checked against the current official page.
4. Download size. The page gives about 16 TB in one place and about 15 TB in another. Subsets will be used.
5. All rows marked "Fetch tool summary" must be re-read directly before any statement from them goes into a paper.

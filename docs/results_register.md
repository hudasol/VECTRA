# Results register

Every run is recorded here, including failed and negative runs. No row may be deleted. Numbers in this file come from files under results/ produced by code.

| Run ID | Date | Experiment | Config file | Seed | Commit | Outcome | Result file |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | 2026-11-01 | E01 sim, pilot split | configs/e01_sim.yaml (levels and W set from this run) | 0 to 9 | 573fee3 | 2,400 runs. Used only to set levels and the B2 window. See results/pilot_summary.md | results/pilot_final.csv |
| R-002 | 2026-11-01 | E01 sim, held out split, primary and secondary | configs/e01_sim.yaml sha256 42aa4e9c... | 0 to 9 | c7e7a8f (tag protocol-v0.1-frozen) | 4,800 runs, no run excluded. B2 lower than B1 and B0 at D0 to D3 (Holm adjusted); B2 not different from B1g at any level; D4 mostly failed for every system | results/e01_heldout.csv, results/e01_primary_tests.csv, results/e01_secondary.csv |
| R-003 | 2026-11-01 | E01 sim, sensitivity grid S1, level D2 | configs/e01_sim.yaml with one heading parameter changed | 0 to 9 | c7e7a8f | 13,440 runs, descriptive. B2 ahead of B1g only when cue noise greatly exceeds the filter assumption (16 degrees) | results/e01_sensitivity.csv |
| R-004 | 2026-11-01 | E02 image based, pilot split (WesternDesertTown, 6 trajectories) | configs/e02.yaml (draft) | VO seeds 17 onward, filter seeds 0 and 1 | 5a3a157 | Used only to set the nominal visual noise and the B3a window, and to check the levels | results/e02_vo/WesternDesertTown__*.npz, results/e02_pilot*.csv |
| R-005 | 2026-11-01 | E02 held out visual odometry (34 trajectories, DesertGasStation, MiddleEast, EndofTheWorld) | configs/e02.yaml frozen (tag protocol-v0.2-frozen) | one degradation seed per level | 719347c | All 34 processed, none failed. VO success falls from 1.00 (D0) to 0.48 (D4) in the median | results/e02_vo/*.npz, results/e02_heldout_vo_stats.csv |
| R-006 | 2026-11-01 | E02 held out filters and prespecified tests F1, F2, F3 | configs/e02.yaml frozen | 48 sky scenarios, filter seeds 0 and 1 | daf9d7f, 6ba3a13 | 97,920 runs, none excluded. H1 and H2 supported, H3 rejected (B2 slightly better than B3), H4 half supported (coverage up, drift unchanged) | results/e02_heldout.csv.gz, results/e02_heldout_F1.csv, F2, F3, secondary, envelope |
| R-007 | 2026-11-01 | E02 exploratory B4 (added after R-006, not prespecified) | configs/e02.yaml frozen | as R-006 | 3262668 | Descriptive only. B2 and B3 reproduce R-006 exactly | results/e02_heldout_explore_B4.csv.gz |
| R-008 | 2026-11-01 | E02 sky model envelope (model only, no data) | configs/e02.yaml | none | bb01f45 | 89 days in 2026 with compass noise above 10 degrees at some time, up to 65 minutes | results/e02_sky_envelope.json |

Status on 2026-11-01: Study 1 (E01, surrogate) and Study 2 (E02, rendered TartanGround desert scenes with a simulated sky compass) have been run. No real sensor or field test has been run.

Deviations from protocol v0.1: none.

Deviations from protocol v0.2: none in the prespecified tests. Added after the held out run and labelled exploratory: system B4 (R-007) and the time of day and gate lock out analyses in the paper.

Errata in protocol v0.2 (found by the internal review after the run; the frozen file is left as written):
1. The systems table says the B3a window is the last 20 visual updates. Section 9 and configs/e02.yaml say 10, and the run used 10.
2. The protocol says the inflated visual update makes the NIS equal to the gate. The code multiplies the visual noise by the ratio of the NIS to the gate, so the resulting NIS is at or above the gate. The paper describes the code.

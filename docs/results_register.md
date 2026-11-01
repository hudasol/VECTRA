# Results register

Every run is recorded here, including failed and negative runs. No row may be deleted. Numbers in this file come from files under results/ produced by code.

| Run ID | Date | Experiment | Config file | Seed | Commit | Outcome | Result file |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | 2026-11-01 | E01 sim, pilot split | configs/e01_sim.yaml (levels and W set from this run) | 0 to 9 | 573fee3 | 2,400 runs. Used only to set levels and the B2 window. See results/pilot_summary.md | results/pilot_final.csv |
| R-002 | 2026-11-01 | E01 sim, held out split, primary and secondary | configs/e01_sim.yaml sha256 42aa4e9c... | 0 to 9 | c7e7a8f (tag protocol-v0.1-frozen) | 4,800 runs, no run excluded. B2 lower than B1 and B0 at D0 to D3 (Holm adjusted); B2 not different from B1g at any level; D4 mostly failed for every system | results/e01_heldout.csv, results/e01_primary_tests.csv, results/e01_secondary.csv |
| R-003 | 2026-11-01 | E01 sim, sensitivity grid S1, level D2 | configs/e01_sim.yaml with one heading parameter changed | 0 to 9 | c7e7a8f | 13,440 runs, descriptive. B2 ahead of B1g only when cue noise greatly exceeds the filter assumption (16 degrees) | results/e01_sensitivity.csv |

Status on 2026-11-01: the simulation study E01 sim has been run on synthetic trajectories. No TartanGround experiment has been run.

Deviations from protocol v0.1: none so far.

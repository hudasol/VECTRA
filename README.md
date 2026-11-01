# VECTRA

Vector based Estimation and Cognition for Terrain Robotics and Autonomy (provisional name).

Status: private working repository. Two studies have been run (see docs/results_register.md). Study 1 (E01) is a surrogate simulation with a synthetic heading cue. Study 2 (E02) uses rendered desert scenes from TartanGround, stereo visual odometry under five levels of image degradation, and a simulated zenith polarisation compass driven by the sun position over Abu Dhabi. No real sensor or field test has been run.

## Purpose

We study whether a robot that uses a compass like heading cue, in the way desert ants do, can keep a better position estimate than a visual inertial system alone when the camera becomes unreliable. The work is framed as a student research project. Everything in this repository is either a plan, a document that cites a public source, or the output of code that we ran. We label each of these clearly.

## Primary research question

Under controlled visual degradation, does a reliability aware fusion of a heading cue reduce drift in a ground rover estimate compared with (B0) visual inertial only and (B1) heading aided fusion with fixed noise?

The question, hypotheses, metrics and statistics are written in docs/experiment_protocol_v0.1.md (Study 1) and docs/experiment_protocol_v0.2.md (Study 2), both frozen before their held out runs. The earlier draft is docs/experiment_protocol.md.

## Scope

- First platform: a simulated ground rover. A drone is considered only after the rover study is complete.
- Study 1 (E01): a simulated planar rover with degradation levels D0 to D4 applied to the visual measurements and a synthetic heading cue. Protocol: docs/experiment_protocol_v0.1.md.
- Study 2 (E02): TartanGround desert scenes (CC BY 4.0), degraded stereo images, stereo visual odometry, an eight state filter and six compass weighting schemes, 34 held out trajectories. Protocol: docs/experiment_protocol_v0.2.md (tag protocol-v0.2-frozen).
- The heading cue in E01 is synthetic. Results from E01 say nothing about a real polarisation sensor.
- This repository is a proposal seed and not a deployed system. It carries no endorsement from any organisation.

## Layout

| Path | Content |
| --- | --- |
| docs/ | Charter, registers, protocols, feasibility note, memos, literature notes in docs/literature |
| src/vectra/ | E01 trajectories, sensors and estimator; E02 image degradation, stereo visual odometry, sky compass model and filter; shared evaluation |
| experiments/E01/, experiments/E02/ | Run, pilot, sensitivity and analysis scripts |
| results/ | Output files of the runs registered in docs/results_register.md |
| tests/ | Unit tests |
| paper/ | Manuscript, diagrams, and the scripts that generate every figure, table and quoted number |
| configs/ | Frozen E01 settings in e01_sim.yaml, plus pointer files |
| data/ | README only. Datasets are never committed |
| src/ | Adapters, degradation, estimators, evaluation (empty until implemented) |
| tests/ | Tests (empty until implemented) |
| experiments/ | One folder per experiment, starting with E01 |
| results/ | Summary tables produced by code |
| environment/ | Dependency list and environment notes |

## Working rules

1. Free tools and free data only.
2. No claim without a source we opened, a number we computed or an experiment we ran.
3. The primary metric is chosen and written down before any result exists.
4. Every random step takes a seed.
5. The repository stays private until the authors agree otherwise.
6. Every number in a document must come from a file produced by code in this repository once results exist.

## Registers

- docs/evidence_register.md: each source and what it supports.
- docs/novelty_register.md: closest prior work and how this project differs.
- docs/results_register.md: every run, its configuration and its outcome, including negative results.
- docs/claims_and_limitations.md: what we may claim, with its evidence, and what we may not.

## Licence

To be decided. The options and the decision criteria are in docs/licence_decision.md. Until a licence is added, all rights are reserved.

## Authors

To be confirmed by the author team. See CITATION.cff.

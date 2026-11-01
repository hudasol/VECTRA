# VECTRA

Vector based Estimation and Cognition for Terrain Robotics and Autonomy (provisional name).

Status: private working repository. The simulation study E01 has been run on synthetic trajectories with a synthetic heading cue (see docs/results_register.md). No image based experiment and no real sensor test has been run.

## Purpose

We study whether a robot that uses a compass like heading cue, in the way desert ants do, can keep a better position estimate than a visual inertial system alone when the camera becomes unreliable. The work is framed as a student research project. Everything in this repository is either a plan, a document that cites a public source, or the output of code that we ran. We label each of these clearly.

## Primary research question

Under controlled visual degradation, does a reliability aware fusion of a heading cue reduce drift in a ground rover estimate compared with (B0) visual inertial only and (B1) heading aided fusion with fixed noise?

The question, hypotheses, metrics and statistics for the simulation study are written in docs/experiment_protocol_v0.1.md, which is frozen (tag protocol-v0.1-frozen). The earlier draft is docs/experiment_protocol.md.

## Scope

- First platform: a simulated ground rover. A drone is considered only after the rover study is complete.
- First experiment (E01): a simulated planar rover with controlled degradation levels D0 to D4 applied to the visual measurements and a synthetic heading cue. A TartanGround image stage is planned and has not been run.
- The heading cue in E01 is synthetic. Results from E01 say nothing about a real polarisation sensor.
- This repository is a proposal seed and not a deployed system. It carries no endorsement from any organisation.

## Layout

| Path | Content |
| --- | --- |
| docs/ | Charter, registers, protocols, feasibility note, memos, literature notes in docs/literature |
| src/vectra/ | Trajectories, sensors, estimators and evaluation for E01 |
| experiments/E01/ | Run, sensitivity and analysis scripts |
| results/ | Output files of the runs registered in docs/results_register.md |
| tests/ | Unit tests |
| paper/ | Draft paper, figure and table scripts |
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

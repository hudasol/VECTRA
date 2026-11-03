# VECTRA

Sky Polarisation Compass Aiding of Stereo Visual Odometry for GNSS Denied Desert Ground Robots under Degraded Vision.

VECTRA is an independent research study on one transferable idea from desert ants: an absolute heading from the sky, combined with a relative motion estimate, for a ground robot that has lost satellite positioning and whose cameras degrade in dust, glare and low light. It is not a deployed system and carries no endorsement from any organisation.

Every result is labelled by the kind of evidence behind it: RENDERED (TartanGround scenes), SIMULATED (degradation, compass, IMU noise, wheel odometry, radiative transfer) or MEASURED (open sky polarisation images and aerosol climatology). No real rover or real polarisation sensor has been run.

## Studies

| Study | Protocol (frozen tag) | What it tests |
| --- | --- | --- |
| Study 1 (E01) | docs/experiment_protocol_v0.1.md (protocol-v0.1-frozen) | Surrogate front end and a synthetic heading cue |
| Study 2 (E02) | docs/experiment_protocol_v0.2.md (protocol-v0.2-frozen) | Rendered desert scenes, stereo VO, single scattering sky, six weighting schemes |
| Study 3 (E03) | docs/protocol_v0.3.md (protocol-v0.3-frozen) | Radiative transfer sky checked against measured skies, bias, tilt and dust coupled compass, nineteen systems, confirmation on unseen environments |

The current manuscript is paper/vectra_paper.tex; the Study 2 manuscript is kept as paper/vectra_study2_paper.tex. Study 3 results are summarised in docs/results_register.md and in the manuscript; the red team reviews and the response are in docs/review/ and docs/STUDY3_RESPONSE.md; every Study 3 judgement call is in docs/DECISIONS_S3.md.

## Reproduce

Python 3.11 or newer with numpy, scipy, pandas, numba, opencv-python, matplotlib, statsmodels and scikit-learn (see environment/). No dataset is stored in the repository.

```
python -m pytest -q tests                                   # unit tests
python experiments/E03/sky_v2.py --photons 120000           # radiative transfer tables and blind window (about 25 min)
bash scripts/download_measured_sky.sh                       # MEASURED check, downloads 2.7 GB, verifies sha256
python experiments/E03/run_vo3.py --split confirmation      # downloads TartanGround trajectories, stereo VO (7 min each)
bash experiments/E03/run_confirm.sh                         # confirmation run and analyses
python experiments/E03/homing.py                            # SIMULATED homing study
cd paper && python make_numbers_e03.py && python make_tables_e03.py && python make_figures_e03.py all && latexmk -pdf vectra_paper.tex
```

Study 2 steps are in experiments/E02 (run_vo.py, run_filters.py, analyze_e02.py) and paper/make_numbers.py.

The compass planner lists the hours when a sky compass is expected to be unreliable at a site:

```
python experiments/E03/compass_planner.py --lat 24.45 --lon 54.38 --utc 4 --start 2026-06-19 --days 3 --aod 0.56
```

## Layout

| Path | Content |
| --- | --- |
| src/vectra/ | Sky models (sky.py, sky_rt.py), compass simulator (compass3.py), degradation, stereo VO, filters (filter2.py, filter3.py), evaluation |
| experiments/E01, E02, E03 | Run, pilot, analysis and planning scripts for each study |
| configs/ | Frozen settings (e01_sim.yaml, e02.yaml, e03.yaml) |
| results/ | Output files of every registered run |
| paper/ | Manuscripts and the scripts that generate every figure, table and quoted number |
| docs/ | Protocols, registers, reviews, decisions, literature notes |
| scripts/ | Download scripts with checksums |
| tests/ | Unit tests |
| data/ | README only; datasets are never committed |

## Working rules

1. Free tools and free open data only; no accounts.
2. No claim without a source we opened, a number we computed or an experiment we ran.
3. Hypotheses, metrics and statistics are frozen in a tag before a confirmation run; deviations are logged.
4. Every random step takes a seed; every number in the manuscript comes from a result file through code.

## Data and licences

Code and documents: MIT (LICENSE). TartanGround: CC BY 4.0, downloaded by the scripts. Marseille skylight polarisation images (Poughon et al., doi:10.57745/610QTS): CC BY-SA 4.0, downloaded by scripts/download_measured_sky.sh. NASA POWER climatology: public, cached in results/e03_sky. IEEEtran.cls keeps its own licence.

## Citation

See CITATION.cff.

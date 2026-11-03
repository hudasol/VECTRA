#!/usr/bin/env bash
# Deviation sensitivity (added after the freeze): the confirmation poses carry no roll or pitch, so the frozen
# primary run has no tilt error. This run applies the development tilt model (Gauss Markov, 2 degrees, 20 s).
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 experiments/E03/run_filters3.py --split confirm --out results/e03/confirm_tilt.csv.gz --workers 2 --draws 1 --keys D0_s0 D2_s0 D4_s0 --assume-tilt 1 --estimators B0 B1 B1g B2 B3 B4 B4R B3R B5 B6 B7 B8 W3 W4R MAG SUN
python3 experiments/E03/analyze_e03.py describe results/e03/confirm_tilt.csv.gz confirm_tilt
echo TILT_DONE

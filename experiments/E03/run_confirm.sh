#!/usr/bin/env bash
# Study 3 confirmation run (protocol v0.3), then the secondary analyses. Run once.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 experiments/E03/run_filters3.py --split confirm --out results/e03/confirm.csv.gz --workers 2 --keys D0_s0 D2_s0 D2_s1 D2_s2 D4_s0 D4_s1 D4_s2
python3 experiments/E03/analyze_e03.py confirm results/e03/confirm.csv.gz
python3 experiments/E03/analyze_e03.py describe results/e03/confirm.csv.gz confirm
python3 experiments/E03/variance_components.py results/e03/confirm.csv.gz
python3 experiments/E03/run_filters3.py --split confirm --out results/e03/confirm_uncoupled.csv.gz --workers 2 --coupling 0 --draws 1 --keys D0_s0 D2_s0 D4_s0 --estimators B0 B1 B1g B2 B3 B4
python3 experiments/E03/analyze_e03.py describe results/e03/confirm_uncoupled.csv.gz confirm_uncoupled
python3 experiments/E03/run_filters3.py --split confirm --out results/e03/confirm_anchored.csv.gz --workers 2 --draws 1 --keys D0_s0 D2_s0 D4_s0 --estimators B0 B1 B1g B2 B3 B4 B4R --sky-table results/e03_sky/dop_tables_anchored.npz
python3 experiments/E03/analyze_e03.py describe results/e03/confirm_anchored.csv.gz confirm_anchored
echo CONFIRM_DONE

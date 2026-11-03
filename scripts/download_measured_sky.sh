#!/usr/bin/env bash
# Download one day of the open Marseille skylight polarisation images (Poughon et al. 2024, doi:10.57745/610QTS,
# licence CC BY-SA 4.0) and run the MEASURED zenith check. About 2.7 GB. Data stay out of the repository.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
D="$ROOT/data/measured_sky"
mkdir -p "$D"
BASE="https://entrepot.recherche.data.gouv.fr/api/access/datafile"
[ -f "$D/2022-07-29_raw.npy" ] || curl -sSL -o "$D/2022-07-29_raw.npy" "$BASE/190593"
[ -f "$D/2022-07-29_raw_annotations.npy" ] || curl -sSL -o "$D/2022-07-29_raw_annotations.npy" "$BASE/190951"
echo "a6e51b45c08ef99f76ce1838778ad7fef2cd21fde8fe477ca4525b57c462f0ae  $D/2022-07-29_raw.npy" | sha256sum -c -
python3 -I "$ROOT/experiments/E03/measured_sky/poughon_zenith.py" "$D/2022-07-29_raw.npy" "$D/2022-07-29_raw_annotations.npy" "$D/zen0729.json"
python3 -I "$ROOT/experiments/E03/measured_sky/poughon_analysis.py" "$D/zen0729.json" "$ROOT/results/e03/measured_marseille_0729.json"

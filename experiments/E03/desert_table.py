"""Blind window by desert latitude from the global map (SIMULATED, AOD 0.3, zenith compass noise above 10 degrees).
Output results/e03_sky/desert_windows.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
m = np.load(ROOT / "results/e03_sky/global_blind_map.npz")
lat, doy, mins = m["lat"], m["doy"], m["minutes"]
deserts = [("Thar", 27.0), ("Sahara, central", 23.0), ("Rub al Khali", 20.0), ("Sahara, Sahel edge", 16.0),
           ("Abu Dhabi", 24.45), ("Great Sandy", -20.0), ("Kalahari", -23.0), ("Namib", -24.0), ("Atacama", -24.5),
           ("Simpson", -25.0)]
rows = []
for name, la in deserts:
    i = int(np.argmin(np.abs(lat - la)))
    for gi, g in enumerate(["zenith", "zenith_ring", "sun_sensor"]):
        rows.append({"desert": name, "lat_used": float(lat[i]), "geometry": g,
                     "days_per_year_with_window": int(2 * np.sum(mins[i, :, gi] > 0)),
                     "max_minutes": int(mins[i, :, gi].max())})
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results/e03_sky/desert_windows.csv", index=False)
lat_any = lat[(mins[:, :, 0] > 0).any(1)]
print(df.pivot(index="desert", columns="geometry", values="max_minutes"))
print(df.pivot(index="desert", columns="geometry", values="days_per_year_with_window"))
print("zenith window latitudes", lat_any.min(), lat_any.max())

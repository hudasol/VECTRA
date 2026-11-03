import sys, json
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from safe_npy import load
a = load(sys.argv[1])
ann = dict(map(tuple, np.load(sys.argv[2], allow_pickle=True)))   # small annotation array of strings
rows = []
for k in range(a.shape[0]):
    img = a[k, 0].astype(float)
    H, W = img.shape
    c = (H // 2) // 4 * 4
    out = {"t": a[k, 2], "exp": float(a[k, 1]), "gain": int(a[k, 3]), "label": ann.get(a[k, 2], "?"),
           "mean": float(img.mean()), "max": float(img.max())}
    for r in (8, 40):
        blk = img[c - r:c + r, c - r:c + r]
        # 2x2 polariser super pixel: offsets (0,0),(0,1),(1,0),(1,1)
        p = [blk[i::2, j::2].mean() for i in (0, 1) for j in (0, 1)]
        out[f"p_{r}"] = p
    rows.append(out)
json.dump(rows, open(sys.argv[3], "w"))
print(len(rows), rows[0], rows[200])

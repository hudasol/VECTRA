"""Layer 2: image degradation for E02, applied to 8 bit grayscale stereo frames.

The model works in linear intensity and follows the order of image formation:
scene radiance, dust haze (Koschmieder attenuation along the rendered depth, plus airlight), veiling glare, exposure,
photon and read noise, auto gain, gamma encoding and 8 bit quantisation. Motion blur
grows with yaw rate and with exposure time, so a darker scene also blurs more.
Frame drops follow a two state Markov chain. All parameters are per level and each
call takes an explicit random generator.
"""
import numpy as np
import cv2

GAMMA = 2.2


def level_params(cfg_levels, name):
    p = dict(cfg_levels[name])
    p.setdefault("gain", 1.0)
    p.setdefault("visibility_m", float("inf"))
    p.setdefault("glare", 0.0)
    p.setdefault("drop_frac", 0.0)
    return p


def drop_mask(n, frac, mean_burst, dt, rng):
    if frac <= 0:
        return np.zeros(n, bool)
    p_end = min(1.0, dt / mean_burst)
    p_start = p_end * frac / max(1e-9, 1 - frac)
    out = np.zeros(n, bool)
    s = False
    for k in range(n):
        s = (rng.random() >= p_end) if s else (rng.random() < p_start)
        out[k] = s
    out[0] = False
    return out


class Degrader:
    def __init__(self, p, cam, rng, size):
        self.p, self.cam, self.rng, self.size = p, cam, rng, size
        h = w = size
        # one glare centre per sequence, upper half of the image
        gx, gy = rng.uniform(0.15, 0.85) * w, rng.uniform(0.05, 0.45) * h
        yy, xx = np.mgrid[0:h, 0:w]
        r2 = ((xx - gx) ** 2 + (yy - gy) ** 2) / (0.25 * w) ** 2
        self.glare_map = (np.exp(-r2) + 0.35).astype(np.float32)
        # Koschmieder haze: transmission exp(-beta r), beta = 3.912 / visibility,
        # with r the range along each pixel ray from the rendered depth map.
        f = size / 2.0
        yy, xx = np.mgrid[0:h, 0:w]
        self.ray_scale = np.sqrt(1 + ((xx - (w - 1) / 2) ** 2 + (yy - (h - 1) / 2) ** 2) / f ** 2).astype(np.float32)
        V = p["visibility_m"]
        self.beta = 0.0 if not np.isfinite(V) else 3.912 / V

    def __call__(self, img, depth, yaw_rate, rng):
        p, c = self.p, self.cam
        if p["gain"] >= 1.0 and not np.isfinite(p["visibility_m"]) and p["glare"] <= 0:
            return img
        lin = (img.astype(np.float32) / 255.0) ** GAMMA
        if self.beta > 0:
            r = np.minimum(depth * self.ray_scale, c["max_range_m"])
            tr = np.exp(-self.beta * r)
            lin = lin * tr + c["airlight"] * (1.0 - tr)
        if p["glare"] > 0:
            lin = lin + p["glare"] * self.glare_map
        g = p["gain"]
        texp = min(c["texp_max_s"], c["texp_base_s"] / g)
        g_eff = g * (texp / c["texp_base_s"])   # light gathered relative to D0
        blur_px = abs(yaw_rate) * texp * (self.size / 2.0) + c["blur_base_px"] * (texp / c["texp_base_s"] - 1.0)
        if blur_px >= 1.0:
            L = int(round(blur_px))
            k = np.zeros((1, L), np.float32)
            k[0, :] = 1.0 / L
            lin = cv2.filter2D(lin, -1, k, borderType=cv2.BORDER_REFLECT)
        e = np.clip(lin, 0, 1) * c["full_well_e"] * g_eff
        e = e + rng.normal(0.0, 1.0, e.shape).astype(np.float32) * np.sqrt(e + c["read_noise_e"] ** 2)
        lin = e / (c["full_well_e"] * g_eff)          # auto gain back to the D0 brightness
        out = np.clip(lin, 0, 1) ** (1.0 / GAMMA) * 255.0
        return np.clip(out + 0.5, 0, 255).astype(np.uint8)

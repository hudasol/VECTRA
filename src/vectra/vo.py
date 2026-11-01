"""Layer 3: stereo visual odometry front end for E02.

Features are tracked with pyramidal Lucas Kanade in the left image, triangulated
from the left right disparity at frame k-1, and the relative pose to frame k is
solved with PnP and RANSAC. The output per frame is the planar body velocity
(forward, right) and the yaw rate, or a failure flag.

Frames: images follow the pinhole convention (x right, y down, z forward).
The body frame is NED style: x forward, y right, z down. So body = (z, x, y) of camera.
"""
import numpy as np
import cv2

LK = dict(winSize=(21, 21), maxLevel=3,
          criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))


class StereoVO:
    def __init__(self, fx, cx, cy, baseline, max_feats=300, min_inliers=15,
                 min_disp=1.0, max_depth=40.0):
        self.K = np.array([[fx, 0, cx], [0, fx, cy], [0, 0, 1]], dtype=np.float64)
        self.fx, self.cx, self.cy, self.b = fx, cx, cy, baseline
        self.max_feats, self.min_inliers = max_feats, min_inliers
        self.min_disp, self.max_depth = min_disp, max_depth
        self.prev = None
        self.prev_pts = None

    def _detect(self, img, existing):
        mask = np.full(img.shape, 255, np.uint8)
        if existing is not None:
            for p in existing.reshape(-1, 2):
                cv2.circle(mask, (int(p[0]), int(p[1])), 7, 0, -1)
        n = self.max_feats - (0 if existing is None else len(existing))
        if n <= 0:
            return existing
        new = cv2.goodFeaturesToTrack(img, maxCorners=n, qualityLevel=0.01, minDistance=7, mask=mask,
                                      blockSize=7)
        if new is None:
            return existing
        new = new.astype(np.float32)
        return new if existing is None or len(existing) == 0 else np.vstack([existing, new])

    def _triangulate(self, left, right, pts):
        pr, st, _ = cv2.calcOpticalFlowPyrLK(left, right, pts, None, **LK)
        st = st.reshape(-1).astype(bool)
        d = pts[:, 0, 0] - pr[:, 0, 0]
        dy = np.abs(pts[:, 0, 1] - pr[:, 0, 1])
        ok = st & (dy < 1.5) & (d > self.min_disp)
        Z = np.where(ok, self.fx * self.b / np.maximum(d, 1e-6), 0.0)
        ok &= Z < self.max_depth
        X = (pts[:, 0, 0] - self.cx) * Z / self.fx
        Y = (pts[:, 0, 1] - self.cy) * Z / self.fx
        return np.stack([X, Y, Z], 1), ok

    def step(self, left, right, dt):
        """Return (ok, v_forward, v_right, yaw_rate, n_inliers)."""
        out = (False, 0.0, 0.0, 0.0, 0)
        if self.prev is None:
            self.prev = (left, right)
            self.prev_pts = self._detect(left, None)
            return out
        pl, pr_img = self.prev
        pts = self.prev_pts
        if pts is None or len(pts) < 8:
            pts = self._detect(pl, None)
        if pts is not None and len(pts) >= 8:
            X, okz = self._triangulate(pl, pr_img, pts)
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(pl, left, pts, None, **LK)
            st = st.reshape(-1).astype(bool)
            # forward backward check
            back, st2, _ = cv2.calcOpticalFlowPyrLK(left, pl, nxt, None, **LK)
            fb = np.linalg.norm((back - pts).reshape(-1, 2), axis=1)
            good = st & st2.reshape(-1).astype(bool) & (fb < 1.0)
            sel = good & okz
            if sel.sum() >= self.min_inliers:
                ok, rvec, tvec, inl = cv2.solvePnPRansac(
                    X[sel].astype(np.float64), nxt[sel].reshape(-1, 2).astype(np.float64), self.K, None,
                    iterationsCount=100, reprojectionError=1.5, confidence=0.99, flags=cv2.SOLVEPNP_ITERATIVE)
                if ok and inl is not None and len(inl) >= self.min_inliers:
                    Rm, _ = cv2.Rodrigues(rvec)
                    Rc = Rm.T
                    p = -Rm.T @ tvec.reshape(3)
                    yaw = np.arctan2(Rc[0, 2], Rc[0, 0])
                    out = (True, p[2] / dt, p[0] / dt, yaw / dt, int(len(inl)))
            keep = good
            tracked = nxt[keep] if keep.any() else None
        else:
            tracked = None
        self.prev = (left, right)
        self.prev_pts = self._detect(left, tracked)
        return out

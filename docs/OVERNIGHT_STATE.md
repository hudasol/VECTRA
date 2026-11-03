# Overnight state (Study 3)

Machine: Linux cloud container, 2 cores, 7 GB RAM, 29 GB free disk, Python 3.13.16, no torch, no GPU.
Start: 2026-11-03 05:47 (UTC+4). Effective work start after setup: 10:41. Hard freeze: 17:47.

## Repository
- Working copy: the lead author's local repository (78 commits, tags protocol-v0.1-frozen and protocol-v0.2-frozen), cloned into the container through a git bundle. No other copies with newer commits were found.
- Remote: https://github.com/hudasol/VECTRA, main pushed on 2026-11-03.
- Tags: study2-final and protocol-v0.3-frozen created locally and in the lead author's local repository (synced from GitHub). Pushing tags is refused by the session git proxy (HTTP 403 on every tag push, main pushes succeed). Tags stay in the local repository; see the log.

## Step status
| Step | Status |
| --- | --- |
| Repository scrub and push | done |
| Red team | done (docs/review) |
| Protocol v0.3 | frozen, tag protocol-v0.3-frozen (local) |
| Sky model v2 | done, with a MEASURED check |
| Estimator work | done except SE(3) and an external VIO baseline |
| Data and confirmation | confirmation VO done; confirmation run started 12:31 |
| Paper | pending |
| Review | pending |

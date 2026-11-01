# Decision memo

Status: inputs received and reviewed on 2026-11-01. The selected option below is a proposal by the lead author. It is not a decision until the faculty authors sign.

## Inputs

| Input | Owner | Due | Received | Summary |
| --- | --- | --- | --- | --- |
| Feasibility note | Huda Mueen | 23 Oct 2026 | Draft done | docs/baseline_feasibility.md |
| Dataset reality check (A1) | Aiman Shariff | 22 Oct 2026 | Received, reviewed | docs/dataset_audit_A1.md. Counts of 878 trajectories and 63 environments confirmed against the paper text. Four gaps remain (IMU file, view frames, licence, extrinsics) |
| Novelty audit (M1) | Maryam Zafar | 23 Oct 2026 | Received, completed by the lead author | docs/novelty_register.md, section Audit result. The gap is narrow and the contribution is a controlled evaluation, not a new estimator |

## Proposed decision criteria (to be agreed before reading the inputs)

Continue if: a usable data subset is confirmed with a stated licence or a documented fallback; the audit finds a gap that is not already covered; and at least one estimator route can run end to end.
Narrow if: the gap is partly covered, or only route (b) is feasible. State the narrower question.
Change if: the gap is already covered, or no usable data and no feasible estimator exist.

## Options

Continue / Narrow / Change. Proposed option: Narrow. The question is restated as a preregistered, controlled comparison on a simulated rover, with the TartanGround image stage as a later step. This is proposed, not decided.

## Open risks

1. The heading cue is synthetic, so no result applies to a real sensor.
2. The TartanGround licence and IMU details are unconfirmed.
3. In E01, reliability weighting did not beat a simple gate (results register R-002).
4. 34 of 48 screened works were not opened, so the novelty finding is bounded by the opened set.

## Sign off

Lead author: pending. Faculty review: pending.

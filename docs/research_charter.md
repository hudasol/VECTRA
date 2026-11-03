# Research charter

Status: draft v0, 2026-10-20. Owner: Huda Mueen (lead). To be reviewed by all authors.

## Problem

Position estimation for a ground robot degrades when the camera becomes unreliable, for example through low light, dust, glare or texture loss, and when satellite positioning is unavailable or interfered with. Desert ants keep a usable estimate under such conditions by combining a compass cue with step counting (path integration). We ask whether a heading cue, weighted by an estimate of its own reliability, improves a visual inertial estimate when vision degrades.

## Primary question

Under controlled visual degradation, does reliability aware heading fusion (B2) reduce drift compared with visual inertial only (B0) and heading aided fusion with fixed noise (B1)?

## Hypotheses

Written in full in docs/experiment_protocol.md (draft v0, not frozen).

## Scope

In scope: a simulated ground rover, public data, free tools, a synthetic heading cue in the first experiment (E01).
Out of scope for now: drones, a physical polarisation sensor, any claim about real world performance, any claim of operational readiness.

## Evidence tiers

1. Simulation (TartanGround and similar).
2. Public real world data (to be chosen after the dataset check).
3. Target environment data (not available; stated as a limitation).

A claim is stated only at the tier where its evidence exists.

## Deliverables

Repository with documents and history; protocol draft v0; baseline feasibility note.

## Authors

Huda Mueen (lead author), Aiman Shariff, Maryam Zafar, Dr. Shamik [surname], Dr. Narina Thakur, Dr. Rajesh Subramanian.

## Decision gates

Gate 1 (end of task H1): continue, narrow or change topic, based on the feasibility note, the dataset check and the novelty audit. Gate criteria were applied by the lead author.

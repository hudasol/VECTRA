# Study 3 final review (independent, sceptical)

Scope: paper/vectra_paper.tex and the inputs paper/s3_*.tex, the macros in paper/numbers_e03.tex, docs/protocol_v0.3.md, docs/DECISIONS_S3.md, results/e03 and results/e03_sky. The review began at commit 6743b1b; the later commits up to 526f4f6 add a short version (vectra_paper_short.tex, s3_methods_short.tex, s3_system_short.tex) built from the same sources, so every finding below applies to the short version as well. No file other than this one was changed.

Method: paper/make_numbers_e03.py was run against results/ with its output redirected to a scratch file; the 471 regenerated macros are identical to paper/numbers_e03.tex. Every macro used in s3_*.tex was resolved and checked against the source files, the hard coded numbers were recomputed with pandas from the row level CSV files, and tests/test_e03.py was run (6 passed). Only verified problems are listed. Line numbers refer to the current files.

## A. Quantitative claims that do not match the result files

### 1. The dust coupling effect is misstated and compares two different designs (high)

Location: paper/s3_results.tex line 40: "B3 reaches \suBthreeDfourhd{} (1.98) degrees at D4 instead of \scBthreeDfourhd{} (3.59); coupling roughly halves the compass benefit at the most severe level".

Evidence: results/e03/confirm_uncoupled.csv.gz contains degradation seed s0 and IMU draw 0 only (4,320 rows), while results/e03/confirm.csv.gz contains seeds s0 to s2 and two IMU draws. Restricting the primary run to the same seed and draw gives, at D4 (trajectory level median of the mean): B0 8.02, B3 3.15 (coupled), against B0 8.02, B3 1.98 (uncoupled). The compass benefit is therefore 6.04 degrees uncoupled and 4.87 degrees coupled, a reduction of about 19 percent, not a halving. Even with the mixed comparison the paper uses (B0 8.94 and B3 3.59 from the primary run) the benefit falls from 6.04 to 5.35 degrees, about 11 percent. What roughly doubles is the residual B3 error (1.98 to 3.15), not the loss of benefit.

Suggested fix: compare like with like (seed s0, IMU draw 0 for both) and add the macros for the restricted primary values to make_numbers_e03.py; replace "roughly halves the compass benefit" with a statement such as "coupling raises the B3 heading RMSE at D4 from 1.98 to 3.15 degrees on the same seed and IMU draw and reduces the compass benefit by about a fifth (6.0 to 4.9 degrees)". State in the text that the uncoupled and anchored runs use one degradation seed and one IMU draw (see Finding 17).

### 2. "The window lies only in May, June and July" is true only at mean aerosol (medium)

Location: paper/s3_methods.tex line 10.

Evidence: results/e03_sky/blind_window_abudhabi.csv has min_gt10 = 25 minutes for August (doy 233) under the high aerosol case (AOD 0.87, zenith geometry). At the low and mean aerosol cases only May, June and July have a window.

Suggested fix: "At the mean climatological aerosol the window lies only in May, June and July on the 21st of each month examined; with one and a half times that aerosol August also has a 25 minute window."

### 3. The Marseille angle of polarisation residual is a scaled MAD, not a median absolute residual (medium)

Location: paper/s3_methods.tex line 7: "a median absolute residual of \sMeasAopMad{} (6.4) degrees".

Evidence: experiments/E03/measured_sky/poughon_analysis.py computes aop_residual_mad_deg as 1.4826 times the median absolute residual. The raw median absolute residual is 6.35 / 1.4826 = 4.3 degrees. The same JSON gives an RMS residual of 38.2 degrees over all daylight images (dominated by overcast images, per label MAD 65.4 degrees for label "o").

Suggested fix: either report 4.3 degrees as the median absolute residual, or keep 6.4 degrees and call it "a robust standard deviation (1.4826 times the median absolute deviation)". Consider adding the clear sky value (5.9 degrees, label "c") since the text discusses clear images.

### 4. "To within 10^-12 (unit tests)" is hard coded and does not describe the unit tests (low)

Location: paper/s3_methods.tex line 4 (macro \sSSerr{}); paper/make_numbers_e03.py sets put("SSerr", "$10^{-12}$") as a literal and does not read the file it loads.

Evidence: results/e03_sky/validation.json gives single_scatter_max_abs_error = 3.3e-16 for the DoP. tests/test_e03.py (test_rt_single_scattering_matches_rayleigh_and_zenith_aop) asserts a DoP error below 1e-6 and a zenith AoP error below 1e-6 degrees. No file supports 1e-12 for the angle of polarisation.

Suggested fix: compute the macro from validation.json and word it as "the DoP to within 3e-16 (validation run) and both DoP and zenith AoP to within 1e-6 (unit tests)", or simply "to numerical precision".

### 5. The blind window bracket understates the aerosol range (low)

Location: s3_abstract.tex, s3_intro.tex line 8, s3_discussion.tex lines 4 and 16 ("68 to 103 minutes"); s3_discussion.tex line 4 ("from about an hour to minutes").

Evidence: results/e03_sky/blind_window_anchored.json: radiative transfer 97, 103, 108 minutes (low, mean, high aerosol); measured anchored 62, 68, 64 minutes. The bracket 68 to 103 holds at mean aerosol only; across the aerosol range it is 62 to 108 minutes. The primary model gives 103 minutes, which is closer to two hours than to "about an hour". The anchored table is also non monotone in aerosol (64 at high against 68 at mean), which suggests Monte Carlo noise of a few minutes that is not reported.

Suggested fix: say "68 to 103 minutes at the mean June aerosol (62 to 108 over half to one and a half times that aerosol)", replace "about an hour" with "one to two hours", and mention the Monte Carlo resolution of the window length.

### 6. The H2 noon value pools all levels but is placed next to a D0 statement (low)

Location: paper/s3_results.tex line 8: "at D0 its heading RMSE is 7.66 ... In the June noon scenarios its mean heading RMSE reaches 38.8 degrees."

Evidence: experiments/E03/analyze_e03.py line 132 defines noon as 21 June at 11:45 and 12:30 and averages over all runs at D0, D2 and D4. Recomputed: 38.81 (pooled, run level mean); at D0 only 53.3; at 12:30 only 45.9.

Suggested fix: "In the June 11:45 and 12:30 scenarios, pooled over levels, its run level mean heading RMSE is 38.8 degrees (53.3 at D0)", and generate the value as a macro instead of hard coding it.

## B. Claims that overreach the evidence

### 7. "No sky geometry removes the window" contradicts the paper's own anchored ring result (high)

Location: s3_abstract.tex ("no sky geometry removes the window"), s3_methods.tex line 12 ("Only a non celestial cue such as a magnetometer removes the window entirely; no sky geometry does"), s3_discussion.tex lines 4 and 16.

Evidence: the same paragraph reports \sWinRingAnch{} = 0 minutes for the zenith plus ring geometry under the measured anchored table (blind_window_anchored.json: measured_anchored low, mean and high all give zenith_ring = 0). On 21 June in Abu Dhabi the minimum solar zenith is 1.0 degree (blind_window_abudhabi.csv), so the sun is never exactly at the zenith there. The theoretical statement (heading is unobservable when the sun is exactly at the zenith) is correct, but the operational claim that the window, defined as minutes with noise above 10 degrees, cannot be removed by any sky geometry is contradicted by the anchored result.

Suggested fix: separate the two statements: "At the instant the sun is exactly at the zenith no polarisation geometry gives heading; the operational window (noise above 10 degrees) shrinks to 11 minutes with the ring under radiative transfer and to zero under the measured anchored model, so whether a ring sensor has any window in Abu Dhabi depends on the near zenith DoP." Apply the same change in the abstract and conclusion.

### 8. The overconfidence is not shown to come from visual translation (high)

Location: s3_abstract.tex ("which an oracle analysis traces to biased visual translation"), s3_results.tex line 43 ("This, rather than the heading, is why every filter is overconfident"), s3_discussion.tex line 8 ("now we know why ... so the overconfidence comes from the visual translation"), s3_discussion.tex line 16.

Evidence: results/e03/dev_by_level.csv, median position NEES: oracle heading (ORH) 57.2, 46.5, 52.8 at D0, D2, D4; oracle translation (ORT) 13.7, 32.9, 69.4, with coverage 0.43, 0.26, 0.12. With true body velocity the filter is still far from consistent (ideal 2) and at D4 it is more overconfident than with an oracle heading. B0 (no compass) has a lower NEES than B3 at D0 (35.0 against 67.3), so adding the compass increases overconfidence. No joint oracle (true heading and true translation) was run. The VO bias analysis (experiments/E03/vo_bias.py) is labelled post hoc in its own docstring and uses the development split. The data show that neither oracle alone restores consistency; they do not identify the cause.

Suggested fix: replace "now we know why" with "an oracle heading does not restore consistency (NEES near 50), and neither does an oracle translation (NEES 14 to 69); the visual forward speed is biased by 2 to 4 percent and its spread is about four times the assumed noise, which is a candidate cause". Label the VO bias analysis post hoc and add a joint oracle run before claiming attribution. Adjust the abstract and conclusion accordingly.

### 9. The B4 recommendation is not supported by the confirmation data (medium)

Location: paper/s3_discussion.tex line 2: "For a designer the robust recommendation is the simplest scheme without a hard gate (B4), because it was selected on one split, confirmed as non inferior on another".

Evidence: results/e03/confirm_summary.json confirm_scores rank B4 11th of 14 VO systems (2.14 degrees), behind every other weighting scheme (B6 1.93, B5 1.98, B7 2.00, B3 2.01, B8 2.06, B2 2.11). At D4 B4 has 4.02 degrees against B3 3.59 and B6 3.41 (confirm_by_level.csv). H7 failed (Kendall tau 0.16), so the development selection did not transfer, which the paper itself states. H3 shows only that B4 is not worse than B2 by more than 0.5 degrees.

Suggested fix: "Any of the weighting schemes is acceptable; none is established as best. B4 has the practical advantage of never rejecting a sample, but it was not better than the others on the confirmation split."

### 10. The wheel odometry comparison is presented without its simulation caveat in the Discussion (medium)

Location: s3_results.tex line 14 ("The ant's combination ... outperforms degraded vision in this setting"); s3_discussion.tex line 10 ("Ant style navigation is competitive. A wheel odometer with a sky compass beat degraded stereo vision ...; in the homing study a tilt aware sky compass kept the error near 2 percent of a 3 km path").

Evidence: W3 uses SIMULATED wheel odometry with assumed scale error (2 percent), noise and slip, while B0 runs real stereo VO on rendered images, so the two arms differ in realism. The advantage is level dependent: on the development split W3 drifts more than B0 at D0 (2.17 against 0.98 percent, dev_by_level.csv) and in the tilt sensitivity run (2.12 against 1.57). The 2 percent figure (54 m at 3 km, results/e03/homing.csv) is a SIMULATED homing result with a March morning start; at a June noon start it is 989 m (33 percent). The Discussion paragraph carries no SIMULATED or ASSUMED label.

Suggested fix: in the Discussion write "SIMULATED wheel odometry with assumed slip ... beat degraded stereo vision at D4 (but not with clear images on the development split)", and "in the SIMULATED homing study ... near 2 percent on a March morning, 33 percent across the June noon window".

### 11. The Marseille correlation of 0.98 was used to choose the time offset (medium)

Location: paper/s3_methods.tex line 7: "The zenith DoP follows sin^2 theta_s closely (correlation \sMeasCorr{})".

Evidence: results/e03/measured_marseille_0729.json records time_zone_fit = "UTC+2 (DoP versus sin^2 of solar zenith, r = 0.98)", that is, the time offset was selected by this criterion, and poughon_analysis.py then hard codes a 2 hour offset. The correlation is therefore not independent evidence for the model. (UTC+2 is also the legal summer time in Marseille, so the choice is plausible.)

Suggested fix: state that the image timestamps were taken as UTC+2 (summer time), that this offset also maximised the correlation, and present the correlation as a consistency check rather than as validation.

### 12. "Several fold" overstates the heading reduction (low)

Location: paper/s3_discussion.tex line 2: "a weighted sky compass cuts heading error several fold once the cameras degrade".

Evidence: confirm_by_level.csv: B0 to B3 at D2 3.18 to 1.37 (2.3 times), at D4 8.94 to 3.59 (2.5 times); pooled H1 5.10 to 1.98 (2.6 times). In the tilt sensitivity run 8.02 to 3.65 (2.2 times).

Suggested fix: "by more than half" or "by a factor of about 2.5".

### 13. The aerosol climatology is labelled MEASURED although it is reanalysis (low)

Location: s3_intro.tex line 8 and s3_discussion.tex line 13 ("the only MEASURED inputs are ... the aerosol climatology").

Evidence: protocol_v0.3.md Section 3 describes the POWER aerosol as "MERRA 2 based"; validation.json lists the source as SYN1DEG. MERRA-2 is a reanalysis that assimilates satellite AOD, not a direct measurement.

Suggested fix: "the aerosol climatology (MERRA-2 reanalysis via NASA POWER)" and drop it from the MEASURED list, or introduce a separate label such as REANALYSIS.

### 14. The freeze tag is not publicly verifiable (low)

Location: paper/s3_system.tex line 47: "Protocol v0.3 was frozen in a repository tag".

Evidence: the tag protocol-v0.3-frozen exists locally (commit faa2131, 11:40, before the confirmation results commit 60f7365 at 12:58), but DECISIONS_S3.md D04 states that tags cannot be pushed through the session proxy, so a reader of the public repository cannot check it.

Suggested fix: cite the freeze commit hash (faa2131) in the paper, or push the tag before submission.

## C. Consistency between the protocol hypotheses and the paper

### 15. The Holm family differs between the protocol and the analysis, and this is not logged (medium)

Location: paper/s3_system.tex line 49 ("Holm correction over the confirmatory family"); s3_results.tex line 19 (table caption: "Holm over H1, H2, H4 and H5").

Evidence: protocol_v0.3.md Section 6 says "Holm over the confirmatory family (H1 to H6)", while Section 7 says H6 is "not part of the Holm family" and H3 and H3b are non inferiority tests decided by the interval. results/e03/confirm_tests.csv applies Holm over four p values (H1, H2, H4, H5). The protocol is internally inconsistent and the resolution is not recorded in DECISIONS_S3.md or in Section VII (Deviations). The conclusions are unaffected (all four adjusted p values are 1.2e-4, and every one sided Wilcoxon p equals or is close to the exact minimum for n = 15).

Suggested fix: add a decision line and a sentence in the Deviations section: "Protocol Section 6 lists H1 to H6 for Holm, Section 7 excludes H6; H3 and H3b are interval based. Holm was applied to H1, H2, H4 and H5."

### 16. H3 and H3b are one test reported as two supported hypotheses (medium)

Location: s3_system.tex line 51; s3_results.tex line 10 ("H3 and H3b are supported"); tab_e03_tests.tex rows H3 and H3b.

Evidence: dev_selection.json selected S = B4, so H3 (S against B2) and H3b (B4 against B2) are the same comparison. confirm_tests.csv rows H3 and H3b are identical in every field (B4 against B2, diff 0.014, interval [-0.019, 0.111]). The paper reports both as supported without saying they are identical; the Methods text defines them separately without noting that S = B4.

Suggested fix: in the Methods add "Because S = B4 (selected on the development split), H3 and H3b reduce to the same comparison"; in the Results write "H3 (equivalently H3b, since S = B4) is supported", and merge or footnote the two table rows so they are not read as independent evidence.

### 17. H2 is stated "with bias and tilt" although the primary run had no tilt; the secondary run designs are not stated (medium)

Location: s3_system.tex line 51 ("H2: with bias and tilt, the ungated B1 ..."); s3_results.tex line 40 (uncoupled and anchored runs).

Evidence: DECISIONS_S3.md D20 and Deviation (v) state that the confirmation poses carry no roll or pitch, so the frozen H2 test contains bias but no tilt. The Results paragraph correctly says "With a heading bias" but the Methods keep the protocol wording. The tilt run supports H2 (B1 7.89 against B0 1.80 at D0, confirm_tilt_by_level.csv) and could be cited. Separately, the uncoupled and anchored runs use one degradation seed and one IMU draw (protocol Section 8 specifies one IMU draw; the seed restriction is not stated anywhere in the paper), which matters for Finding 1.

Suggested fix: add to the H2 result "the confirmation poses are level, so H2 was tested with bias only; in the tilt sensitivity run B1 is also worse than B0 at D0 (7.89 against 1.80)". State the seed and IMU draw of each secondary run in the Secondary analyses paragraph.

## D. Style rules

### 18. Style checks pass (no action)

Evidence: a byte level scan of s3_*.tex, vectra_paper.tex, vectra_paper_short.tex and tab_e03_*.tex found no em dash (U+2014), no LaTeX triple hyphen and no emoji; the only double hyphens are page ranges in s3_bib.tex and the "--" placeholder for missing p values in tab_e03_tests.tex. No AI system or assistant is mentioned; the only match for "AI" is the cited title "Insect-inspired AI for autonomous robots" (de Croon et al.). No university or institution is named as an affiliation; all six authors use "[Department], [University], [City]" and "[email placeholder]". The author list and order (Huda Mueen, Aiman Shariff, Maryam Zafar, Dr. Shamik [surname], Dr. Narina Thakur, Dr. Rajesh Subramanian) match vectra_study2_paper.tex and the history since commit 52b56d4, and the short version uses the same block.

## E. Verified without problems

The following were recomputed and match: all confirmatory test values in tab_e03_tests.tex and the text (H1 to H5, including medians, paired differences and intervals); H6 (B3C NEES 47.7, coverage 0.16; B3 48.0, 0.14) and H7 (tau 0.16); every per level value quoted from confirm_by_level.csv, dev_by_level.csv, confirm_anchored_by_level.csv and confirm_tilt_by_level.csv; the row count 63,840 (15 trajectories, 7 VO runs each, 16 scenarios, 2 IMU draws, 19 systems); the statement that B5 to B8 lie within about 0.2 degrees of B3 and B4; the B7 D0 and D4 statements; the SUN and MAG statements; the gross order under H7; the B3R gating explanation (B3R gates 363 samples per run at D2 on the development split against 87 for B3); the variance components; the VO scale and spread (0.21 m/s against an assumed 0.0548 m/s, configs/e03.yaml, about four times); all homing values and the exponent range 0.85 to 1.59; the Cramer Rao deviation (at most 2.8 percent); the latitude limit of 34 degrees (every latitude from -34 to 34 has a window, none beyond); the desert table; the AoP sign flip claim (all 18 flipped cells have DoP below 0.005); the Marseille d_max of 0.613 and the 15 percent gap (recomputed ratio 0.86 at solar zenith 50 to 70 degrees); and the Study 1 values 5.12 and 1.20 percent on 24 held out trajectories.

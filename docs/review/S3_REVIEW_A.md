# S3 Review A: sky model and compass error model

Scope: paper/vectra_paper.tex, src/vectra/sky.py, configs/e02.yaml, docs/claims_and_limitations.md, docs/literature/E_polarisation_compass.md. Each item gives the claim affected (C), the weakness (W), a settling test (T) and the expected direction (D).

Framing identity: near the zenith the model gives d ≈ k d_max θ²/2 (k the sky factor), so noise exceeds σ* while the sun is within θ* = sqrt(2c / (k d_max σ*)) of the zenith; with frozen values θ* ≈ 7.4 degrees at σ* = 10 degrees. Window length scales as sqrt(c / (k d_max σ*)). The reported 64 to 45 minute shrinkage when d_max doubles is exactly 1/sqrt(2), so the headline window is an algebraic consequence of four assumed constants.

## Weaknesses

**1. Rayleigh shape near the sun.** C: the 89 day, 65 minute window (contribution i, R-008). W: single scattering forces d ∝ θ² near the sun; the paper's own comparison (8 percent measured at 70 degrees elevation against 3.7 percent modelled) shows the shape, not only the scale, is wrong. T: tabulate zenith DoP from an open vector radiative transfer code for solar zenith 0 to 60 degrees, desert aerosol and sand surface; recompute R-008. D: uncertain; likely shorter in clear air, but see item 2.

**2. No neutral points or negative polarisation.** C: "the zenith e vector is perpendicular to the solar meridian"; zero mean angle error. W: multiple scattering causes negative polarisation (e-vector parallel to the scattering plane) around the sun, bounded by the Babinet and Brewster points [1]. With the sun near the zenith, the zenith may fall in that region, where the AoP is rotated 90 degrees: the worst possible error modulo 180 degrees, and a bias rather than noise. T: in the item 1 run, record the polarisation sign at the zenith versus solar zenith and inject 90 degree flips where negative. D: worse for all compass systems near noon, especially B1.

**3. d_max = 0.6 and sky factors double count.** C: haze and dust results. W: 0.6 is a measured whole sky maximum in an aerosol laden desert, so "clear" already includes depolarisation; haze 0.6 and dust 0.3 multiply on top. A flat factor also keeps the Rayleigh angular shape, while aerosol and surface representation dominate real sky DoP [2]. By the identity, dust lengthens the window about 1.8 times. T: report R-008 per sky condition; derive k(θ, condition) from radiative transfer. D: longer, condition dependent window.

**4. Sky condition independent of image degradation.** C: headline gains at D3 and D4 (R-006). W: D4 (visibility 20 m, light gain 0.025) is paired with clear sky and with noon. A dust layer limiting visibility to tens of metres will nearly depolarise skylight, and deep low light cannot occur at noon. The largest benefits come from physically impossible pairings. T: couple scenarios (dust levels force the dust sky; low light forces low sun) and rerun the D3 and D4 primary tests on the coupled set. D: much smaller benefit under dust; possibly larger in twilight.

**5. Constant c is unsourced and sets the window.** C: "64 minutes", "89 days". W: c = 0.05 degrees agrees with σ_DoP = 0.002 (AoP noise ≈ σ_DoP/2d), but neither is traced to a sensor, band, exposure or bandwidth; the 10 degree threshold is arbitrary. T: tabulate the window for c from 0.02 to 0.5 degrees and σ* from 2 to 20 degrees; derive c from a named sensor noise budget. D: realistic budgets likely give larger c and a longer window.

**6. Gaussian, independent noise at low DoP.** C: B3 results at 11:45. W: AoP error is Gaussian and DoP noise is drawn independently and rectified. Real Stokes noise is shared, AoP becomes heavy tailed then uniform as d falls, and measured DoP is biased high, so B3 is overconfident at the window edges. T: simulate noisy Stokes parameters and estimate AoP and DoP from them. D: B3 loses part of its advantage; more gate rejections.

**7. No bias or misalignment.** C: "lowers heading RMSE by about an order of magnitude". W: z = yaw_true + white noise; real compasses have mounting offset, polariser calibration error and structured deviations from Rayleigh. Study 1 showed a drifting bias defeats every aided filter. T: add a 0.5 to 2 degree offset and a bias random walk; add a bias state. D: smaller gains, possibly reversed at D0 and D1.

**8. No tilt.** C: all E02 results. W: tilt error depends on inclination and solar altitude [3] and is largest near high sun; TartanGround provides full attitude, so this is cheap. T: evaluate DoP and AoP along the tilted view from ground truth roll and pitch. D: terrain correlated heading errors; an asymmetric, wider window.

**9. Albedo and wavelength unspecified.** C: transfer of a Tunisian d_max to Abu Dhabi. W: multiple scattering of surface reflected light "greatly reduces the DoP" and spectral shape depends on surface reflectance [2]; no sensor band is named. T: fix a band and run item 1 with sand albedo. D: probably lower DoP, longer window.

**10. Cloud error white per sample.** C: cloud result and the gate lockout explanation. W: 10 degrees redrawn every 0.2 s averages to about 0.8 degrees over a 30 s epoch; real cloud errors persist. T: one error per epoch, or an Ornstein Uhlenbeck process with 30 s time constant. D: much worse for B1 and B3; directly tests lockout.

**11. Perfect ephemeris and clock.** C: heading near noon. W: the code never uses sun azimuth. When the sun passes 1 degree from the zenith its azimuth moves about 14 degrees per minute, so clock and position errors map into heading. T: form heading from sun azimuth and measured AoP with realistic clock and position errors. D: modest error, concentrated in the window.

**12. Zenith geometry generalised.** C: "a polarisation compass that looks at the zenith alone needs another heading source"; abstract wording. W: an imaging sensor fitting the full sky pattern keeps azimuth information until the sun is within a few degrees of the zenith. T: add a wide field pattern fit as a sensitivity case. D: much shorter window; restrict the claim to zenith sensors.

## References (opened for this review)

[1] Horváth, G.; Bernáth, B.; Suhai, B.; Barta, A.; Wehner, R. "First observation of the fourth neutral polarization point in the atmosphere." J. Opt. Soc. Am. A 19(10), 2085 to 2093, 2002. https://arago.elte.hu/sites/default/files/4thNeutralPoint_JOSAA.pdf

[2] Pust, N. J.; Shaw, J. A. "Wavelength dependence of the degree of polarization in cloud-free skies: simulations of real environments." Opt. Express 20(14), 15559 to 15568, 2012. https://www.montana.edu/jshaw/documents/Wavelength%20dependence%20of%20atmospheric%20DoP%20-%20PustShaw%20-%20Opt%20Express%202012.pdf

[3] Liang, H.; Bai, H.; Zhou, T.; Shen, K. "Influence of Sensor Tilts on Bio-inspired Polarized Skylight Orientation Determination." arXiv:2007.08987. https://arxiv.org/abs/2007.08987

## Three most damaging issues

1. Item 4: the D3 and D4 headline gains rest on physically incompatible sky and image pairings.
2. Items 1 and 2: missing multiple scattering and neutral points; the window may hold 90 degree biased headings, and its length is a shape artefact.
3. Items 7 and 8: no bias and no tilt; Study 1 already shows bias reverses the benefit.

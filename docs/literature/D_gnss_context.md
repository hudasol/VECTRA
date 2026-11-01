# D. GNSS interference evidence and regional context (research notes)

Compiled 2026-11-01. Rules followed: nothing cited from memory; every item below was opened in this session via WebFetch (a small extractor model returned the text, so I did not see raw page text) or via curl + pdftotext (raw text, marked RAW). "Quote" lines are only text returned by those tools. Where no verbatim quote was returned, I say so rather than invent one. Press and vendor sources are labelled.

Read-depth key: FULL = whole document passed to the extractor or read as raw text; PARTIAL = extractor reported truncation or only part read; PAGE = single web page.

---
## 0. VERIFICATION OF THE THREE PREVIOUSLY NOTED CLAIMS

### 0.1 "ICAO MID 461 reports Jan 2019 to Sep 2020"  -> MIS-ATTRIBUTED, number is real but source and wording differ
- The number 461 was found in exactly one opened document: Civil Aviation Authority of Malaysia, Safety Information 07/2021 REV1, "Harmful Interference to Global Navigation Satellite System (GNSS) and its Impacts on Flight Operations", dated 29 March 2022.
- It attributes the study to IATA ("IATA GNSS/GPS Interference - Global Aviation Data Management, November 11th 2020"), covering January 2019 to September 2020, region "MENA" (not "MID").
- Wording returned: "a total of 461 GNSS jamming or suspected interference reports in MENA States." The same document also gives 831 reports for MENA plus neighbouring States.
- The wording is therefore: IATA (GADM) data, MENA States, jamming OR SUSPECTED interference reports. It is not an ICAO MID-compiled count.
- I could NOT open the likely primary (ICAO MID CNS SG/10 presentation "CNS SG PPT8 - GPS Interference", 2020): curl returned 403 and WebFetch failed. So the 461 is verified only at second hand (a national regulator citing IATA).
- 461 does NOT appear in: ICAO MID ATM SG/7 WP6 (Nov 2021), MIDANPIRG/19 WP16, MIDANPIRG/21 WP47 and WP69, CNS SG/7 PPT12 (IATA, May 2022), SEIG-4 PPT5, IFALPA 19SAB07 (18 Jul 2019, predates the period), IATA Kuwait Safety Summit slides (Dec 2024).
- Caution: ATM SG/7 WP6 (UAE GCAA and IATA, 14 Nov 2021) covers Jan 2019 to Dec 2020 and its FIR chart bars (approximately LTAA 2350, ORBB 1603 per extractor reading of a chart) are far above 461 and the paper says one report may span several FIRs. So "461" and the FIR chart counts use different units. Do not mix them.
- Safe wording: "IATA's Global Aviation Data Management recorded 461 jamming or suspected-interference reports from MENA States between January 2019 and September 2020 (as cited in CAAM SI 07/2021 REV1)."

### 0.2 "UKMTO advisory October 2025"  -> VERIFIED (RAW text read)
- UKMTO Advisory 034-25, 071310UTC Oct 2025, category "ELECTRONIC INTERFERENCE", range 03-07 Oct 2025, inside the UKMTO Summary Report 04-10 October 2025 (hosted by MSCIO). See source D3.
- Also verified, separate: UKMTO advisory of 18 May 2025 on Strait of Hormuz interference (via Baird Maritime press, source D5; UKMTO original not opened).

### 0.3 "over 1,650 vessels affected in 2026 per press"  -> UNSAFE AS STATED
- Origin is a vendor blog, not press and not an authority: Windward, "GPS Jamming Rises 55% in a Week in the Middle East Gulf" (page title "...1,650 Ships Hit"), 8 March 2026 (modified 18 Mar). It says more than 1,650 vessels experienced "GPS and AIS interference" on a single day, 7 March 2026. Method and thresholds not disclosed.
- A later Windward blog (23 Jun 2026) restates it as ">1,650 vessels in the first two weeks after Feb 28", i.e. a different time window for the same figure. The same blog gives Q1 2026 ">1,100 vessels" and ~978,000 events, mixing units.
- Other measurements disagree in size: ~1,100 vessels in 24h (Windward via Inside GNSS, 2 Mar 2026); "up to 1,000 ships" (Kpler analyst via AFP/Dawn, 13 Mar 2026); 655 vessels / 1,735 events (RICS secondary summary, 26 Mar 2026).
- No UKMTO, JMIC or MSCIO document I opened gives a vessel count; they give qualitative statements (D4).
- Safe wording: "Commercial maritime analytics firms reported that on the order of 1,000 or more vessels in the Gulf and Gulf of Oman experienced GNSS or AIS interference in the first days of March 2026 (Windward; Kpler via AFP), figures that are vendor-derived and unverified."

---
## 1. MEASURED PREVALENCE (aviation, space-based, maritime)

### D1. ICAO MID, ATM SG/7-WP/6, "GNSS/GPS Interference Reported in MID Region"
- Publisher/author: ICAO MID Office meeting paper, presented by UAE GCAA and IATA. ATM SG/7 (virtual), 15-18 Nov 2021; paper dated 14/11/2021.
- URL: https://www.icao.int/MID/Documents/2021/ATM%20SG7/WP6.pdf
- Read: FULL (via extractor).
- Facts: (a) Period Jan 2019 to Dec 2020. (b) Ankara FIR (LTAA) and Baghdad FIR (ORBB) and borders account for 83.8% of reports ("which equates to 83.8% of total reports received"). (c) 64% of reports during approach, descent or climb. (d) Chart note: one report may contain interference across several FIRs, so FIR counts must not be summed.
- Note: authors are UAE GCAA co-presenting; this is UAE-linked official material.

### D2. ICAO MID, MIDANPIRG/21 and RASG-MID/11 WP/69, IATA "GNSS Radio Frequency Interference Incidents"
- Abu Dhabi, 4-8 Mar 2024, paper dated 20/02/2024, Agenda 4.2. Author IATA.
- URL: https://www.icao.int/Meetings/MIDANPIRG-RASG/Documents/WP%2069.pdf
- Read: FULL (via extractor).
- Facts: (a) "a total of 37,770 'GPS signal loss' events in the MID region from January 2023 to December 2023." (b) 92.96 events per 1,000 FDx flights in MID vs world 29.83. (c) EUR-MENA routes about 329.40 per 1,000 flights, roughly 45% of flights had a signal-loss event. (d) Globally 75.8% of events lasted under 30 min, 18.2% 30-60 min.
- Caution: these are aircraft-reported "GPS signal lost" events (FDX), not confirmed interference and not UAE-specific.

### D2b. ICAO MID, CNS SG/7 PPT12 (IATA GADM), 16 May 2022, Muscat
- URL: https://www.icao.int/MID/Documents/2022/CNS%20and%20MIDAMC/PPT12.pdf   Read: FULL (slides via extractor).
- Facts: 586 GNSS/GPS jamming or suspected interference reports from 15 operators, Jan-Dec 2021 (quote: "Total 586 GNSS/GPS jamming or suspected interference reports"); 46,936 "GPS signal lost" events from 38 operators, Aug-Dec 2021 only; 105 interference NOTAMs over MENA in 2021 (FAA SWIFT); Turkish FIRs 76.86% of IDX reports; annual average 4.172 per 1,000 takeoffs and landings, peak 11.46 in Aug 2021.
- Same figures appear in SEIG-4 PPT5 (https://www2023.icao.int/MID/Documents/2022/SEIG4%20and%20NASP/PPT5.pdf), read FULL, dated 2 Mar 2022 per footers.

### D2c. ICAO MID, MIDANPIRG/20 and RASG-MID/10 PPT26 (ICAO MID and IATA)
- URL: https://www.icao.int:443/MID/MIDANPIRG/Documents/MID20%20and%20RASGMID10/PPT26%20-%20GNSS%20Interference.pdf   Read: FULL (slides via extractor). Date not stated in extract.
- Facts: 164,577 "GPS Signal Loss" events plotted for MENA (period not stated); duration average 14.5 min, median 6.0 min (outliers removed); many reports excluded because location undeterminable; one manufacturer detected 10,843 RFI events globally in 2021 "most in the Middle East" (ITU circular CR/488).
- Caution: period not stated; use only the duration statistics, with that caveat.

### D2d. ICAO MID, ATM SG/10 WP/4 "GNSS Vulnerabilities", Jeddah 20-23 Oct 2024 (paper dated 20 Sep 2024), Secretariat
- URL: https://icao.int/MID/Documents/2024/ATM%20SG10/WP4.pdf   Read: FULL (via extractor).
- Facts: (a) spoofing reports since Aug 2023 concentrated in Baghdad, Tehran, Cairo FIRs. (b) one spoofed FMS showed 60 NM off track; one flight vectored all the way to destination; one operator nearly entered restricted airspace. (c) historical RSA-14 data Jan 2015 to Jun 2018: Beirut 32, Ankara 10, Cairo 10 reports etc; cruise 28% of reports. (d) no UAE figures.
- Quote: none retrieved verbatim.

### D3. UKMTO Summary Report 04-10 October 2025 (RAW pdftotext, 192 lines, read lines 1-60 plus keyword scan of rest)
- Publisher: UKMTO (Royal Navy, UK), with US MARAD; file hosted by MSCIO (EU NAVFOR Atalanta).
- URL: https://mscio.eu/media/documents/20251010_UKMTO_Summary_Report-10Oct25.pdf
- Facts: (a) Advisory 034-25: "UKMTO received numerous reports of GNSS interference from vessels in the area shown above, between 3 and 7 October 2025." (b) states a "significant increase of reports compared with the same period in the previous week"; the report itself says this may reflect "increased disruption or improved compliance with reporting". (c) reports concentrated around Bandar-e-Pars, Strait of Hormuz and Port Sudan; AIS-speed-anomaly rule: vessels >1,000 GT showing >25 kts. (d) hexagon legend: red >50 anomalous events per cell.
- No counts of vessels given. Good primary source for "persistent and reported", not for prevalence numbers.

### D4. MSCIO Advisory 01/2026 Update 12, 2 April 2026 (RAW pdftotext, 383 lines, read lines 1-100 plus keyword scan)
- Publisher: MSCIO (Maritime Security Centre Indian Ocean, EU NAVFOR Atalanta). URL: https://mscio.eu/media/documents/20260402_MSCIO_ADVISORY_01_2026._UPDATE_12.pdf
- Facts: (a) "GNSS/AIS spoofing levels inside the Arabian Gulf, SoH and Gulf of Oman have decreased, however, intermittent disruptions are still reported." (b) advises vessels "to be prepared to rely on dead-reckoning navigation if necessary" and says "GNSS are highly likely to be unreliable". (c) context: military operations since 28 Feb 2026; transit of Hormuz "NOT recommended"; 28 incidents involving commercial vessels since 28 Feb. (d) Red Sea GNSS/GPS disruption also reported.
- Important: also shows interference fell back in April 2026; do not write as monotonic growth.

### D5. Press / trade (label PRESS)
- Baird Maritime (PRESS), "Hours-long GNSS interference reported in Strait of Hormuz", 22 May 2025, reporting UKMTO advisory of 18 May 2025 and JMIC. Read PAGE. Fact: GNSS interference "lasted several hours" and affected ECDIS, ARPA, AIS, GMDSS inputs; JMIC says Red Sea and Hormuz levels not linked. URL: https://www.bairdmaritime.com/security/incidents/piracy/hours-long-gnss-interference-reported-in-strait-of-hormuz
- JMIC Advisory 008-25 Final Update 016, 27 Jun 2025 (primary, Combined Maritime Forces/JMIC with UKMTO and MSCIO). Read FULL. Fact: "Regional electronic interference remains which may have an impact on commercial shipping"; interference mostly central Arabian Gulf; figure uses gpsjam.org map. URL: https://mscio.eu/media/documents/008_JMIC_Advisory_Note__Final_Update__016.pdf
- Britannia P&I Club loss-prevention update, June 2025 (INDUSTRY). Read FULL. Fact: reports "an increase in electronic interference and loss of positional data for GNSS receivers"; no counts. URL: https://britanniapandi.com/wp-content/uploads/2025/09/Electronic-interference-in-Arabian-Gulf-and-Strait-of-Hormuz-Update.pdf
- Windward blogs (VENDOR): https://windward.ai/blog/gps-jamming-surges-in-the-middle-east-gulf-1650-ships-hit/ (8 Mar 2026) and https://windward.ai/blog/gps-jamming-is-mainstream-changes-between-2025-and-2026/ (23 Jun 2026). Read PAGE each. Numbers: at least 30 jamming clusters incl. UAE; Q1 2026 98% of global events in Middle East Gulf (vs 57% in Q4 2025) - vendor claim, method undisclosed.
- Inside GNSS (TRADE PRESS), 2 Mar 2026, https://insidegnss.com/?p=196401. Read PAGE. Facts: >1,100 vessels (Windward), ~150 ships stranded near Hormuz (Reuters, attributed).
- Dawn / AFP (PRESS), "War-related GPS glitches in UAE put ships on land, cars at sea", 13 Mar 2026, https://www.dawn.com/news/1981534. Read PAGE. Facts: Kpler analyst: up to 1,000 ships jammed in the Gulf and Gulf of Oman; phones located users at sea; delivery that should take 10-15 min took 30 (one driver anecdote). No UAE official statement in the article.
- Khaleej Times (PRESS), 12 Mar 2026, https://khaleejtimes.com/uae/uae-gps-google-maps-waze-glitches-iran-attack. Read PAGE. Facts: residents report map apps placing them in the sea; expert (MBRSC Lab) attributes to jamming/spoofing "security measures"; no TDRA or GCAA statement.
- RICS (PROFESSIONAL BODY, secondary compilation), "GNSS Spoofing and mitigation in the Arabian Gulf", 26 Mar 2026 (current to 24 Mar), https://www.rics.org/news-insights/gnss-spoofing-and-mitigation-in-the-arabian-gulf. Read PAGE. Facts: 655 vessels, 1,735 events, about 600 incidents off UAE waters (per its secondary sources, unverified); Qatar Oct 2025 position drifts of 2-5 NM reported; PTP timing holdover up to 25 min. Quote: "persistent operational reality, not an anomaly."

### D6. Peer-reviewed space-based measurement
- Murrian, Narula, Iannucci, Budzien, O'Hanlon, Psiaki, Humphreys, "First results from three years of GNSS Interference Monitoring from Low Earth Orbit", arXiv:2009.04093v2 (UT Austin, NRL, Cornell, Virginia Tech). Read: FULL (via extractor). URL: https://arxiv.org/pdf/2009.04093
- Facts: ISS-hosted FOTON receiver, Mar 2017 to Jun 2020; persistent Syria source since 2017; geolocation 95% semi-major axis about 220 m; hotspots Syria, Libya region, China L2. The Persian Gulf was NOT covered in the paper; the period predates 2022-2026 escalation. Quote: none retrieved. Use only as method evidence that interference is detectable from orbit.
- I found no Zurich/ETH source in this session (not searched specifically beyond one query). Listed under UNOPENED.

---
## 2. EASA, ICAO, IMO/ITU, EU AND US POLICY DOCUMENTS DEFINING THE PROBLEM

### P1. EASA Safety Information Bulletin 2022-02R4 (issued 3 July 2026; revises R3 of 5 Jul 2024)
- URL: https://ad.easa.europa.eu/blob/EASA_SIB_2022_02R4.pdf/SIB_2022-02R4_1 ; web page https://www.easa.europa.eu/en/domains/air-operations/global-navigation-satellite-system-outages-and-alterations. Read: SIB FULL (extractor), page PAGE.
- Facts: interference "increased since February 2022"; affected areas named: south and eastern Mediterranean, Black Sea, Middle East, Baltic Sea, Arctic; Persian Gulf not named in the SIB text; EASA does not consider it an unsafe condition requiring a Safety Directive; spoofing harder for crews to detect. Quotes: "growing severity and sophistication of GNSS jamming and spoofing incidents." and "it is not possible to predict GNSS interference or its effects."
- EASA Conflict Zone Information Bulletin 2026-03-R13 (Middle East and Persian Gulf, issued 28/02/2026, revised 24/06/2026): read PAGE; it does not mention GNSS at all. Do not cite it for GNSS.

### P2. Joint IMO / ICAO / ITU statement on satellite interference
- URL: https://www.imo.org/en/mediacentre/pressbriefings/pages/joint-imo-icao-itu-statement-satellite-interference.aspx. Read PAGE; page shows no date (search result dated it April 2025, from a press site, so treat date as unverified).
- Facts: "grave concern" about rising jamming and spoofing in RNSS bands; five actions for Member States (protect RNSS, strengthen PNT resilience, keep conventional navigation infrastructure as backup, cooperation, reporting mechanisms). ICAO SG quote: "Radio Navigation Satellite Service interference can impact aircraft operations far beyond the immediate affected area". Cited: SOLAS V/19.2.1.6, MSC.1/Circ.1644 (not opened).

### P3. EU Council document 9198/1/25 REV 1, 4 Jun 2025, TTE Council AOB, 13 Member States "call for common actions" on GNSS jamming and spoofing
- URL: https://data.consilium.europa.eu/doc/document/ST-9198-2025-REV-1/en/pdf. Read FULL (extractor).
- Facts: Baltic interference since 2022; Action 5: "Reassess the current reliance on GNSS-based navigation and develop resilient Positioning, Navigation and Timing"; Poland monthly unique ICAO IDs affected 2,732 (Jan 2025). Europe-specific; shows policy framing, not Gulf data.

### P4. US Executive Order 13905 (12 Feb 2020; 85 FR 9359, 18 Feb 2020)
- URL: https://www.govinfo.gov/content/pkg/FR-2020-02-18/html/2020-03337.htm. Read FULL (extractor).
- Facts: defines PNT services and "responsible use"; orders PNT profiles within 1 year; Sec 4(h) a national plan within 1 year for R&D and pilot testing of PNT not dependent on GNSS; Sec 4(i) GNSS-independent UTC source in 180 days. Quote: "engage the public and private sectors to identify and promote the responsible use of PNT services". The order does not define "disruption".

### P5. UK Government Office for Science, "Satellite-derived time and position: a study of critical dependencies" (Blackett review), published 30 Jan 2018
- URL: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/676675/satellite-derived-time-and-position-blackett-review.pdf ; landing page https://gov.uk/government/publications/satellite-derived-time-and-position-blackett-review. Read PARTIAL: first 100,000 of 126,748 characters.
- Facts: GNSS an "invisible utility", dependence hidden; London sensor about 4.6 jamming incidents per day, airport-area sensor about 4.8 (2013-2017); 2009 test: jammer with under one thousandth of mobile-phone power knocked ship systems offline; five-day GNSS disruption estimated at £5.2 billion (London Economics, quoted by the review); recommends GNSS-independent backup. Foreword names signatories, the review itself states no date in extracted text, so date taken from gov.uk page.

---
## 3. UAE-SPECIFIC PUBLIC MATERIAL

### U1. UAE GCAA, ICAO MID PBN SG/8 WP/11 "GNSS Interference and GPS Anomalies", 21 Nov 2023 (Doha, 12-13 Dec 2023)
- URL: https://www.icao.int/MID/Documents/2023/PBN%20SG8-PBN%20Airspace%20Design%20Workshop/WP%2011%20-%20GNSS%20Anomalies%20UAE%20GCAA.pdf. Read FULL (extractor).
- Facts: no total count of UAE reports; one described event: a Learjet 45 entered the Emirates FIR via SIR VOR on 3 Oct 2023 after GPS jamming before entry and needed radar vectors; Figure 1 shows jamming events in Emirates FIR reported in 2023 by the national carrier (data not readable); asks for an action group to "address this emerging risk with high priority". Quote: "Regulations should prioritize safeguarding safety-critical aeronautical CNS systems."

### U2. UAE, ICAO A41-WP/196 "GNSS Interference", submitted to the 41st ICAO Assembly, dated "2/8/22" (ambiguous, likely 2 Aug 2022)
- URL: https://www.icao.int/Meetings/a41/Documents/WP/wp_196_en.pdf. Read FULL (extractor).
- Facts: states jamming and/or possible spoofing "has intensified near conflict zones and in other areas"; no quantitative data; asks Assembly to urge States to implement GNSS Manual (Doc 9849) mitigations.

### U3. UAE, ICAO MID CNS SG/14 WP/5, "UAE Best Practices for Enhancing Surveillance Data Integrity Against GNSS Interference", 10 Oct 2025, Abu Dhabi 19-23 Oct 2025
- URL: https://www.icao.int/sites/default/files/MID/MeetingDocs/2025/Fourteenth%20Meeting%20of%20the%20of%20the%20MIDANPIRG%20Communication%2C%20Navigation%20and%20Surveillance%20Sub-Group%20%28CNS%20SG/2-%20Documentation/WP05.pdf. Read FULL (extractor).
- Facts: official UAE statement that it "has observed an increase in reported interference cases" over the past two years; interference complaint form sent to the Telecommunications Regulatory Authority; ATC exports at least 5 min of data either side of an event; spoofing indicators include inconsistent ground speeds and duplicate targets. No counts.

### U4. TDRA, "Interference Coordination" slides in ICAO MID FM WG/5 WP/10 (2026, date not stated)
- URL: https://www.icao.int/sites/default/files/MID/MeetingDocs/2026/FM%20WG5%20%26%20CNS%20SG15/3-%20FM%20WG5%20-%20Documentation/WP10.pdf. Read FULL (six slides via extractor).
- Facts: TDRA classifies GPS jamming/spoofing incidents as international (letters to ICAO and ITU), national (locate and clear source) or circumstantial (observe and document); intermittent interference monitored 24-48 hours. This is the only TDRA primary found. No TDRA public statement on the March 2026 events was found.

### U5. Gap statement
- No UAE GCAA or TDRA public statement on the 2026 Gulf events was found in the pages opened. Khaleej Times and Dawn/AFP contain none either. Do not write "UAE authorities confirmed" anything.

### U6. Institutional public pages (describe focus only; no endorsement implied)
- TII Autonomous Robotics Research Center, https://tii.ae/autonomous-robotics. Read PAGE. Focus: perception and computer vision, control and decision making, communication and networking, swarm and coordination; works across air, land, sea surface, underwater; aims for operation without "human intervention and human infrastructure". The page does not name navigation or GNSS-denied work. The ARRC brochure PDF (https://webfiles.tii.ae/2024-10/TII_ARRC_Brochure.pdf) returned binary data: UNREAD.
- Khalifa University KUCARS, https://www.ku.ac.ae/?p=34544. Read PAGE. Focus list includes "GPS-denied navigation", sense and avoid, embodied AI; MBZIRC maritime challenge involves a GNSS-denied coastal environment; UGV-UAV collaborative inspection of critical infrastructure listed; AV-Lab has an autonomous shuttle, a delivery vehicle, a legged robot, four drones. Page text contains internal inconsistencies (extractor flagged); use only the focus-area list.
- EDGE Group, official product page not opened (WAM page returned empty). Instead: Janes (TRADE PRESS) "IDEX 2025: Edge Group to supply GPS-Protect to UAE MoD", https://janes.com/osint-insights/defence-news-details/air/idex-2025-edge-group-to-supply-gps-protect-to-uae-mod. Read PAGE. Facts: contract AED227 million (USD61.81 million) for a GNSS anti-jamming system developed by Sign4l; claimed jam-to-signal up to 105 dB (single jammer); four-element antenna array; "platform-agnostic" for UAVs, land and maritime platforms. Shows GNSS interference is treated as a procurement-level threat in the UAE; it is anti-jam hardware, not GNSS-free navigation. EDGE UGV portfolio pages: UNOPENED.

---
## 4. EXAMPLES OF GNSS-DENIED NEEDS FOR GROUND ROBOTS
Important distinction: most oil-and-gas and mining material is about structural GNSS denial (enclosures, tank floors, underground), not hostile interference. Do not present it as evidence of jamming.

- G1. Szrek et al., "Accuracy Evaluation of Selected Mobile Inspection Robot Localization Techniques in a GNSS-Denied Environment", Sensors 21(1):141, Dec 2020, DOI 10.3390/s21010141. Read abstract via DOAJ record (PARTIAL). Facts: compares four methods (wheel odometry, IMU dead reckoning, visual odometry, UWB trilateration) against geodetic ground truth in an underground mine; ground robot; the abstract gives no error numbers; oil and gas not mentioned. URL: https://doaj.org/article/fa03678ad61d4afd8d7578c0675d5565
- G2. Bryner (Gecko Robotics), Robotics 24/7, 15 Aug 2021 (VENDOR AUTHOR, trade press), https://robotics247.com/article/how_robotic_navigation_can_assist_inspection_gps_denied_environments. Read PAGE. Facts: power, oil and gas, refineries, tank floors, boilers described as GPS-denied; industrial sites "devoid of GPS" (quote); no statistics. Qualitative only.
- G3. Kulkarni et al. (NTNU, Alexis group), "UniPilot: Enabling GPS-Denied Autonomy Across Embodiments", arXiv 2509.11793 (2025, exact date not shown). Read: FULL (extractor). Facts: 829 g payload; tested on quadrotor, ANYmal legged robot, VTOL; reports 0.062 +/- 0.033 m absolute translational error (LiDAR-radar-inertial); tank-inspection use. Does not discuss jamming. Source has internal inconsistencies between text and table (LiDAR range, IMU rate); do not quote those. https://arxiv.org/pdf/2509.11793
- G4. SINTEF organised workshop at European Robotics Forum 2026, "Robotic GNSS-denied localisation for inspection and maintenance", https://www.sintef.no/en/events/archive/2026/erf26-workshop-innovation-and-developments-in-robotic-gnss-denied-localisation-for-inspection-maintenance/. Read PAGE. Facts: frames localisation as "mission-critical enabler of safety, compliance, and repeatability" (ship interiors, offshore facilities, tunnels, plants); 80 minute programme; oil and gas not named. Evidence of a research community, nothing quantitative.
- G5. Advanced Navigation (VENDOR marketing), autonomous haulage page, https://www.unmannedsystemstechnology.com/feature/keeping-haulage-trucks-moving-through-gnss-interruptions/, date and author not stated. Read PAGE. Claim: "a single 400-tonne truck stoppage can cascade through the system"; says most stoppages come from temporary GNSS/RTK degradation, no data. Use only as an illustration, flagged vendor.
- G6. KUCARS (U6) and the MBZIRC description: an in-region academic statement that GPS-denied navigation is a research focus and that a coastal challenge was GNSS-denied.
- Desert logistics and defence-adjacent civil use: I found NO opened source with desert-logistics GNSS-denial evidence. Gap.

---
## 5. QUANTIFIED HARM OF GNSS LOSS

- Q1. RTI International for NIST, "Economic Benefits of the Global Positioning System to the U.S. Private Sector" (page published 2 Oct 2019, updated 3 Feb 2025), https://www.nist.gov/news-events/news/2019/10/economic-benefits-global-positioning-system-us-private-sector-study. Read PAGE (news summary, not the full 2019 report). Facts: about $1 billion per day if GPS lost; up to 50% higher if several weeks during April-May planting season; $1.4 trillion benefits (2017 dollars); ten sectors including mining, oil and gas, precision agriculture. US macro-economic estimate, not ground-robot specific, not UAE.
- Q2. Blackett review (P5): £5.2 billion for a five-day outage (London Economics, as quoted); UK macro-economic; not robots.
- Q3. Humphreys, Stanford PNT Symposium slides, 14 Nov 2013, https://web.stanford.edu/group/scpnt/pnt/PNT13/2013_Presentation_Files/3-Humphreys-PNT13.pdf. Read FULL (extractor). Facts: UAV spoofing work cited to Shepard et al. 2012 and Kerns et al. (J. Field Robotics); quote: "Crashing is easier than control." The slides carry no numerical UAV test results. UT Austin news item 28 Jun 2012 (https://ae.utexas.edu/?p=8578, PAGE): team took control of a hovering UAV from "about a kilometer away" in a DHS-invited demonstration at White Sands. Kerns et al. paper itself not opened.
- Q4. Murrian et al. (D6): cold-start spoofing-style interference needs about 0 dB power ratio vs about 31.8 dB for matched-spectrum jamming (extractor-reported figure). Technical vulnerability evidence, not harm to missions.
- Q5. Aviation consequence evidence: 60 NM off-track FMS indication (D2d); UAE Learjet needed radar vectors (U1). These are anecdotal case reports, not rates.
- Q6. Zeng et al., "All Your GPS Are Belong To Us" (USENIX Security 2018): not opened (usenix.org not on allowlist). UNOPENED.
- Q7. Drones (MDPI) Dec 2024, "Jamming and Spoofing Techniques for Drone Neutralization: An Experimental Study", https://doaj.org/article/b94da69a118c4c12a1d570744f7b087b. Read abstract record only. No numbers; qualitative.
- Gap: I found no peer-reviewed or agency source that quantifies harm of GNSS loss specifically for UAE ground vehicles or UAS (failure rate, mission loss rate). The honest position is that the quantification exists for economies and aviation, and for ground robots only as demonstrations.

---
## UNOPENED (with reason)
- ICAO MID CNS SG/10 PPT8 "GPS Interference" (2020) https://www.icao.int/MID/Documents/2020/CNS%20SG10/CNS%20SG%20PPT8-%20GPS%20Interference.pdf : curl 403 (bot filter), WebFetch client_error. Most likely primary for the 461 figure.
- ICAO MIDANPIRG/17 WP9; CNS SG12 PPT11; ASRG-5 PPT3; PBN SG9 PPT6; ICAO GADM analysis 2024 PPT7; RSA-14 appendix: appeared in search results, not fetched (prioritised other items).
- IATA Kuwait 2024 slides (PPT26): opened, but charts unreadable in extraction, so no numbers taken.
- ICAO MIDANPIRG/23 WP-02 (4 Jun 2026) and CNS SG/15 WP08 (7 May 2026): opened, no statistics.
- UKMTO website (ukmto.org) and the original 18 May 2025 advisory: not fetched; used MSCIO-hosted summary and Baird press.
- Zeng et al. USENIX Security 2018: usenix.org not on fetch allowlist (usenix.net redirected).
- Kerns et al., J. Field Robotics 2014 and Shepard et al. ION GNSS 2012: only seen as citations.
- Murrian et al. published journal version; ETH Zurich or other independent LEO jamming maps: not found/opened. Spire, Kpler, Lloyd's List and Wired primary pieces: not opened (only seen through AFP, Inside GNSS and RICS).
- London Economics 2017 report and full RTI 2019 report: not opened; numbers only through the Blackett review and NIST summary.
- EUSPA User Technology Report itself: not opened; GPS World commentary only (10 Mar 2025, PAGE; it quotes STRIKE3 figures: more than 450,000 interfering signals, 59,000 assessed intentional, 2016-2019, 23 countries; attribution to STRIKE3 not to EUSPA).
- IMO MSC.1/Circ.1644, ITU Radio Regulations, ICAO Doc 9849: referenced only.
- DHS/NIST resilient PNT profiles (NIST IR 8323): appeared in search, not opened.
- EDGE official UGV pages (WAM page empty), TII ARRC brochure (binary), Fraunhofer publica record (access denied), CAAS SIB 2026-01: not read.
- gpsjam.org: not opened.
- GCAA website and TDRA website public statements: not located.

---
## SYNTHESIS (what is safe to put in the paper)
1. SAFE: GNSS interference in the Middle East is documented by ICAO MID working papers; e.g. 37,770 aircraft-reported "GPS signal loss" events in MID in 2023, 92.96 per 1,000 flights vs 29.83 world (IATA, MIDANPIRG/21 WP69). Label as reported events, not confirmed jamming.
2. SAFE: EASA SIB 2022-02R4 (3 Jul 2026) states jamming and spoofing have increased since Feb 2022 and names the Middle East; EASA says it cannot be predicted.
3. SAFE: UKMTO Advisory 034-25 (3-7 Oct 2025) reported numerous vessel reports of GNSS interference in the Gulf and Hormuz; MSCIO (2 Apr 2026) advised dead reckoning and said levels had decreased but disruptions persisted.
4. SAFE: UAE officially told ICAO (CNS SG/14 WP5, Oct 2025) it "has observed an increase in reported interference cases"; UAE also raised the issue at the 41st ICAO Assembly (2022) and PBN SG/8 (2023, Learjet event of 3 Oct 2023).
5. FIX: "461 reports Jan 2019 to Sep 2020" is IATA GADM data for MENA States ("jamming or suspected interference"), cited via Malaysia CAAM SI 07/2021 REV1; do not call it an ICAO MID report unless the ICAO CNS SG/10 slide is opened.
6. NOT SAFE: "over 1,650 vessels in 2026". It is a Windward vendor blog figure with changing time windows (one day 7 Mar vs two weeks) and undisclosed method; at most write "around 1,000 or more vessels, per vendor and press estimates".
7. NOT SAFE: any claim that GCAA or TDRA publicly confirmed the March 2026 disruptions, or any UAE interference count; none found.
8. NOT SAFE: oil-and-gas or mining GNSS-denial examples as evidence of hostile interference; they are structural denial (tank floors, underground) and some are vendor pieces. Desert logistics: no source found.
9. NOT SAFE: quantified harm to UAE ground robots or UAS; only national-economy estimates ($1B per day US, NIST/RTI 2019; £5.2B five days UK) and demonstrations (UAV spoofing from about 1 km, UT Austin 2012) exist in opened sources.
10. TII ARRC and KUCARS may be described only by public focus (KUCARS lists GPS-denied navigation; TII page does not); EDGE GPS-Protect (AED227 million, Janes) shows anti-jam spending, not an endorsement of GNSS-free navigation.

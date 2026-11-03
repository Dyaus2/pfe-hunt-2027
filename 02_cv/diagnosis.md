# Phase 2: Why the current CV likely fails screening

Input: `Resume_pfe.pdf` (French, 2 pages, ~1,170 words, LaTeX).
Postings checked on 2026-11-03 (listed below).

## Verdict
Your **content is strong**: real metrics, a full MLOps chain, a serious RAG project. The rejections 4–5 days after applying look like **screening filters**, not a weak profile. The most likely causes, in order:

| # | Problem | Why it hurts | Fix (applied in the new CVs) |
|---|---|---|---|
| 1 | **Education reads "2023 – 2026"** | ATS parsers and recruiters read this as *already graduated*. An end-of-studies internship (PFE) legally requires an enrolled student (French *convention de stage*, German § 15 BeschV, J-1 "currently enrolled"). A "graduate" is filtered out automatically, or seen as needing a work visa instead of an internship visa. | "2023 – 2027 (expected) – final year; 6-month mandatory end-of-studies internship (PFE) from Jan/Feb 2027" |
| 2 | **No availability, duration or mobility line** | Recruiters screen PFE candidates on *start date + duration + mandatory internship*. None of these appear, so they assume "doesn't fit". | Top line under the name: "Seeking 6-month end-of-studies internship (PFE), from Jan/Feb 2027 — open to relocation" plus "Mandatory internship – tripartite agreement signed by ESPRIT" |
| 3 | **SOC / cybersecurity framing** | The headline section says "Deux stages en environnement SOC", and the top experience is dense with DFIR, YARA/Sigma and MITRE jargon. An industrial or aero recruiter (Safran, Thales) files you as a *cybersecurity* profile. | Lead with *anomaly detection, calibrated classification, MLOps*. Put the security context second. Profile rewritten around applied DS. |
| 4 | **Keyword gaps vs. real postings** (table below) | ATS ranking is keyword-driven. "LLM", "time series", "computer vision", "cloud" and "data visualization" are missing or buried, even though your projects cover them. | Skills section restructured. Keywords added **only where backed by the CV** (e.g. image captioning → computer vision; ARIMA project → time series; AWS badge → cloud). |
| 5 | **French-only** | DE/CH/US/UAE/QA screeners and many FR multinationals filter on English CVs. | English master CV plus corrected French CV. |
| 6 | **Generic title** | "Étudiant Ingénieur – Data Science & IA" says nothing about the job you want. | Headline: "Data Science & AI Engineering Student — ML / MLOps / LLM-RAG" |
| 7 | **Density** | Seven long bullets for ATOR, plus long multi-line DressMe bullets. Screeners spend about 7–10 s per CV, so the strongest numbers (18%→84%, PR-AUC 0.927) are buried in jargon. | Strongest numbers moved first in each bullet. Shorter bullets. DressMe (design-phase only) compressed to 2 lines. |
| 8 | **Format risks** | LaTeX two-column right-aligned dates sometimes parse badly (dates merged into titles). No real issue found in the text layer, but Word-format CVs are safer for Workday/SuccessFactors uploads. | Single-column `.docx` with standard headings (Experience, Education, Skills), plus a PDF export. |

## Keyword match against 6 real postings

| Posting (checked 2026-11-03) | Must-have keywords | In old CV? |
|---|---|---|
| **Thales**, *STAGE – Ingénieur Data Scientist – Maintenance prédictive par IA*, Toulouse ([Workday](https://thales.wd3.myworkdayjobs.com/Careers/job/Toulouse/STAGE---Ingnieur-Data-Scientist---Maintenance-prdictive-par-IA---F-H_R0344657-2); via [freehire](https://freehire.me/jobs/stage-ingenieur-data-scientist-maintenance-predictive-par-ia-f-h-thales-fya7dtz6)), posted 2026-10-26 | Python, R, SQL, scikit-learn, TensorFlow, PyTorch, **time series**, sensor / operational log analysis, **predictive maintenance**, model evaluation | Most yes. "Time series" was only inside the R project; "log analysis" was hidden behind DFIR wording; predictive maintenance absent (cannot be claimed, but anomaly detection on logs maps to it, so say it in the letter, not as a skill). |
| **ENGIE Axima**, *Stagiaire Data Scientist Maintenance Prédictive*, Paris La Défense, 6 months ([Wizbii](https://www.wizbii.com/company/engie/job/stagiaire-data-scientist-maintenance-predictive-h-f)) | **R**, time series, classification, **anomaly & drift detection**, sensor fault detection, robust regression, data visualization; Azure ML (plus) | Anomaly + drift detection yes (PSI). R yes. Visualization was weak (Power BI/Tableau only in the skills list). |
| **Bosch**, *Internship Data Science in Manufacturing*, Reutlingen, 6 months ([SmartRecruiters](https://jobs.smartrecruiters.com/BoschGroup/744000141677619-internship-data-science-in-manufacturing); applications closed 2026-10-23, still a good benchmark) | Python, PyTorch, TensorFlow, SQL, data visualization, deep learning, **computer vision**, prototypes, English + **German** | CV absent from skills (fix: captioning project = CNN/ViT/CLIP/BLIP). No German (cannot fix; target English-language teams). |
| **Allphins**, *Data Scientist – Stage 6 mois (fin d'études)*, Paris ([WTTJ](https://www.welcometothejungle.com/fr/companies/allphins/jobs/data-scientist-h-f-stage-6-mois-teletravail-possible_paris)) | Python, pandas, scikit-learn, statistics, ML model development/testing, data viz, **engineering school final year**, fluent English | Yes, except "final year" was not visible (the dates problem). |
| **Askills** (client: large energy company), *Stage Data Scientist/IA – Agents IA appliqués à l'ingénierie*, Lyon, Feb/Mar 2027, 6 months ([collective.work](https://www.collective.work/jobs/fr/stage-data-scientistia-developpement-dagents-ia-appliques-a-lingenierie-hf-joj2)) | **LLM**, advanced RAG, **agents**, prompt engineering, **evaluation framework** (faithfulness, relevance, latency) | RAG yes, evaluation (hit@k/MRR) yes, but the word **"LLM" appears nowhere** in the old CV, and "multi-agent" only in a French title. |
| **Decathlon Digital**, *Stage AI Engineer – IA Alternatives*, Paris, Q1 2027, 6 months ([Jooble](https://fr.jooble.org/jdp/-6367917635997691699)) | Bac+5 final-year, AI engineering (details truncated on the aggregator; UNVERIFIED) | Dates problem again. |

### Keywords now covered (all backed by your existing content)
LLM · RAG · hybrid search · reranking · retrieval evaluation · anomaly detection · drift monitoring · time-series forecasting (ARIMA/SARIMA) · computer vision (CNN, ViT, CLIP, BLIP) · probability calibration · MLOps · champion/challenger · CI tests (pytest) · Docker · FastAPI · SQL · data visualization (Power BI, Tableau) · AWS (Cloud Foundations badge).

### Keywords you do NOT have (don't add them until they're true)
MLflow, Airflow, Kubernetes, CI/CD pipelines (GitHub Actions), Spark, Azure ML, German. **Quick wins before applying:** add MLflow tracking and a GitHub Actions test workflow to one public repo (e.g. the Phase 4 skeletons). Then you can honestly list them.

## Length norms by country (recruiter practice, not law)

| Country | Norm for an intern CV | Our output |
|---|---|---|
| France | **1 page** strongly preferred for *stage* | FR CV: 2 pages, with page 1 self-sufficient. Consider cutting DressMe + Show-Attend-Tell for a 1-page send. |
| Germany | 1–2 pages; photo optional (not needed for international/English applications); a tabular *Lebenslauf* is common | EN master, 2 pages |
| Switzerland | 1–2 pages | EN master |
| USA | **1 page** | Use the EN master but drop DressMe, Show-Attend-Tell and the 2025 internship bullets → fits 1 page |
| Canada | 1–2 pages, no photo | EN master |
| UAE / Qatar | 1–2 pages; nationality and visa status often expected | EN master; add "Nationality: Tunisian" if a form asks |
| Tunisia | 1–2 pages, FR or EN | FR or EN |

## Other fixes
- **Email:** keep `hazem.ilahi@esprit.tn` (proves enrollment) and consider a personal backup in the header if the school mailbox expires after graduation.
- **Language levels:** French shown as "advanced (professional working proficiency)", matching what you told me. Add a CEFR level only if you have a certificate (DELF/DALF/TCF).
- **Hedera certifications:** a placeholder line is in both CVs. **Delete it before sending** unless the certificates are issued.
- **Apply via the company ATS with the .docx** when the system parses CVs (Workday, SuccessFactors, Taleo). Send the PDF by email.

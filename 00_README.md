# PFE hunt 2027: Hazem Ilahi (index)

Everything here was produced on **2026-11-03** from your CV (Resume_pfe.pdf) and what you told me. Each external fact carries a source URL and a check date. Items I could not confirm are marked **UNVERIFIED** and collected below.

## 1. Deliverables

| # | What | Files |
|---|---|---|
| 01 | **Visa and feasibility check** (8 countries, ranked table, where to spend effort) | [01_visa_feasibility/feasibility.md](01_visa_feasibility/feasibility.md) |
| 02 | **CV diagnosis** (why screening fails, keyword match vs 6 real postings, length norms) | [02_cv/diagnosis.md](02_cv/diagnosis.md) |
| 02 | **New CVs**, ATS-friendly, EN + FR, .docx + .pdf | [EN docx](02_cv/Hazem_Ilahi_CV_EN.docx) · [EN pdf](02_cv/Hazem_Ilahi_CV_EN.pdf) · [FR docx](02_cv/Hazem_Ilahi_CV_FR.docx) · [FR pdf](02_cv/Hazem_Ilahi_CV_FR.pdf) · source: [02_cv/build/](02_cv/build/) (`node build/build_cv.js .`) |
| 02 | **LinkedIn** headline + About (EN) + profile fixes | [02_cv/linkedin.md](02_cv/linkedin.md) |
| 03 | **59 targets** (10 A / 30 B / 19 C; FR 29, DE 12, TN 10, CH 7, CA 1), with live offers checked via company job APIs | [targets.xlsx](03_targets/targets.xlsx) (status dropdown, filters) · [targets.csv](03_targets/targets.csv) · generator [build_targets.py](03_targets/build_targets.py) |
| 03 | **Application plan**, day by day, 5 Nov → 31 Dec | [03_targets/plan.md](03_targets/plan.md) |
| 04 | **Letters**: master EN/FR, cold email EN/FR + LinkedIn note, follow-ups EN/FR, **10 tailored letters** (A-priority) | [04_letters/](04_letters/) · [tailored/](04_letters/tailored/) |
| 05 | **4 PFE proposals**: pitch EN + FR, verified literature, tested starter code, executed Colab notebooks | [05_pfe_proposals/README.md](05_pfe_proposals/README.md) |
| 06/07 | Interview bank / portfolio | Not started (optional). Say **"go portfolio"** for Phase 5. |

## 2. How to use this (first 72 hours)
1. **Fix GitHub access** so this repo can be pushed (see §4, item 1). Until then, everything lives only in this session's local git history.
2. Read `01_visa_feasibility/feasibility.md` TL;DR (2 min). **France first, Germany/Switzerland need offers by early Dec, Tunisia in parallel.**
3. Send the **ESPRIT email** (questions in §4).
4. Open `targets.xlsx` → filter `priority = A` → apply with the matching letter in `04_letters/tailored/` + `02_cv/Hazem_Ilahi_CV_FR.pdf` (France) or `_EN.pdf` (others). Set `status`.
5. Follow `03_targets/plan.md` daily (2 h/day; follow-ups at day 7 and day 14).

## 3. UNVERIFIED items (do not rely on them without checking)
**Visa / legal (01)**
- Germany: ZAV processing time for internship approval; maximum internship duration "6 months" (portal entry only); whether "Praktikum im Einvernehmen" TLS slots are available right now (TLScontact blocked automated access).
- France: the France-Visas pages blocked automated fetches, so wording was confirmed via search snippets only. Unconfirmed: the "lodge up to 3 months before departure" rule, the 15–45 days processing time and €99 fee (secondary source), and whether the convention must be *visée* by the préfecture/DREETS for Tunisians in 2027.
- Switzerland: "up to 8 weeks" permit time (university guidance, secondary).
- USA: Tunisia's absence from Proclamation 10998 (secondary lists only), the ~1-month F/M/J interview wait (third-party tracker), and J-1 sponsor fees.
- UAE: official MoHRE/u.ae page returned 404, so only secondary sources were used. Qatar: permit rules from third-party guides only.
- Canada: Mitacs 2027 deadline (16 Sep 2026) from secondary summaries.
- Tunisia: whether a PFE stipend is legally required.

**Targets (03)**
- **Safran Tarnos (A) and Safran Bordes**: safran-group.com blocks bots, so offers were confirmed only via the search-engine index. Open them yourself.
- Pay amounts in Germany (Bosch etc.): not stated in postings.
- ENGIE PdM offer: aggregator says "expire bientôt"; the ENGIE careers URL was not HTTP-checked.
- Askills offer: host reputation unknown (intermediary; end client not named). Kept as C.
- KPMG Tunisie listing: not HTTP-checked; undated.
- ST Tunis careers page did not respond to automated checks.
- InstaDeep: internships page reachable, but Tunis openings were not visible in the filtered view.
- Airbus Helicopters (Marignane) Data Scientist offer: sibling postings require security clearance ("habilitation"). Eligibility for a Tunisian national is unclear (kept as B).
- Decathlon Digital AI Engineer posting (used only in the CV keyword analysis): details truncated on aggregator.

**Letters / CV**
- Bosch Agentic AI letter: the posting asks for **beginner German**, which is not on your CV. The letter has an **[EDIT BEFORE SENDING]** line: keep only a true statement.
- Thales Bordeaux letter: commits you to learning TDA basics. Keep it only if you agree (marked **[à confirmer]**).
- CVs: the **Hedera placeholder line** must be replaced with the exact certificate titles, or deleted, before sending.
- "AWS Cloud Foundations (badge, Nov 2026)": written exactly as you described. Check the official badge title on Credly and adjust.

## 4. What YOU must do
**Access / accounts**
1. **GitHub push is blocked (403).** Connect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on `Dyaus2/pfe-hunt-2027` (same page). Then ask me to push. Commits made so far are local.
2. Update LinkedIn (`02_cv/linkedin.md`): headline, About, ESPRIT end date **2027**, Open-to-work → Internship.

**Email ESPRIT (this week)**
1. Is a PFE start in **March 2027** accepted, and what is the latest defence date?
2. How fast can ESPRIT sign a **tripartite convention** with a foreign host (English version available?).
3. Can ESPRIT issue an **English (and German) letter** stating the internship is **mandatory**, 6 months, part of the engineering degree? This is needed for Germany (BA) and Switzerland (ABB posting asks for it).
4. Does ESPRIT have partner companies, alumni or an IAESTE link for placements abroad?

**Confirm yourself**
- Each A-target offer is still open (Safran in particular). Check the TLScontact Tunis appointment availability for "Praktikum im Einvernehmen" (DE) and for long-stay "stagiaire" (FR).
- Your language claims: the CVs say French "advanced (professional working proficiency)". Add CEFR levels only if you have certificates.
- Before sending any letter, replace `[Date]` and every `[bracket]`.

**Apply (from 5 Nov)**: the 10 A-targets first: ABB CH, Bosch ×2, Safran Tarnos, Thales Toulouse PdM, ATR, Sanofi Lyon, Airbus acoustic, Thales Bordeaux, InstaDeep. Use the application channel column. Never use guessed email addresses.

## 5. Reproducibility
- CVs: `cd 02_cv && node build/build_cv.js . && soffice --headless --convert-to pdf *.docx`
- Targets: `cd 03_targets && python3 build_targets.py`
- Tailored letters: `python3 04_letters/build_tailored.py`
- Proposals: `cd 05_pfe_proposals/<X>/code && pip install -r requirements.txt && python -m pytest -q`. Notebooks: `python 05_pfe_proposals/tools/build_notebook.py 05_pfe_proposals/<X>`.

## 6. Commit log (one commit per deliverable)
Phase 1 → Phase 2 → Phase 3 → Phase 4 (wip A+B, wip C, final) → README. See `git log`.

"""Build targets.csv + targets.xlsx. Every URL below was checked on 2026-11-03
(live API/HTTP check or search-engine evidence where the site blocks bots, noted in `evidence_note`)."""
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

CHECKED = "2026-11-03"
FR_VISA = ("FR: long-stay visa 'stagiaire' (VLS-TS) on tripartite convention de stage — "
           "https://france-visas.gouv.fr/stagiaire-etudiant ; gratification ≥ €4.50/h mandatory >2 months — "
           "https://www.service-public.gouv.fr/particuliers/vosdroits/F32131")
DE_VISA = ("DE: host requests BA approval (§15 Nr.6 BeschV), then D-visa 'Praktikum im Einvernehmen' via TLScontact Tunis — "
           "https://tunis.diplo.de/tn-de/service/05-visaeinreise/2440344-2440344 ; "
           "https://www.arbeitsagentur.de/arbeiten-in-deutschland/praktika-und-ferienjobs-fuer-auslaendische-studierende")
CH_VISA = ("CH: mandatory internship of a foreign-university student, cantonal + SEM permit, customary wage — "
           "https://www.zh.ch/de/wirtschaft-arbeit/erwerbstaetigkeit-auslaender/studierende-und-praktikanten.html")
TN_VISA = "TN: no visa (national). ESPRIT PFE agreement only."
FR_PAID = "Yes (legal gratification ≥ €4.50/h)"
DE_PAID = "Usually paid at Bosch/large groups — amount UNVERIFIED; < €1,030/month requires extra funding proof (embassy)"
CH_PAID = "Yes (customary local wage required by permit rules)"
TN_PAID = "UNVERIFIED"

COLS = ["id", "company", "country", "city", "sector", "size_reputation", "offer_title", "offer_url", "careers_url",
        "visa_handling_evidence", "language", "paid", "start_date_fit", "application_channel", "deadline",
        "fit_score_1to5", "fit_reason", "priority", "status", "evidence_note", "checked_on"]

T = []
def add(**k):
    k.setdefault("status", ""); k.setdefault("deadline", "Not stated — apply ASAP"); k.setdefault("checked_on", CHECKED)
    T.append(k)

# ---------------- FRANCE: live offers ----------------
add(company="Thales", country="France", city="Toulouse", sector="Aerospace & defence",
    size_reputation="CAC 40 group, ~80k employees", offer_title="STAGE – Ingénieur Data Scientist – Maintenance prédictive par IA – F/H (R0344657)",
    offer_url="https://thales.wd3.myworkdayjobs.com/Careers/job/Toulouse/STAGE---Ingnieur-Data-Scientist---Maintenance-prdictive-par-IA---F-H_R0344657-2",
    careers_url="https://thales.wd3.myworkdayjobs.com/Careers", visa_handling_evidence=FR_VISA, language="French posting; Python/R/SQL",
    paid=FR_PAID, start_date_fit="Start not stated (PFE); posted 2026-10-26", application_channel="Workday (online)",
    fit_score_1to5=5, fit_reason="Predictive maintenance on sensor + operational logs = your ATOR anomaly detection + calibrated GBM on logs",
    priority="A", evidence_note="Live via Workday API")
add(company="Thales", country="France", city="Bordeaux", sector="Aerospace & defence", size_reputation="CAC 40 group",
    offer_title="STAGE – Ingénieur analyste Data Science – H/F (R0346387)",
    offer_url="https://thales.wd3.myworkdayjobs.com/Careers/job/Bordeaux/STAGE---Ingnieur-analyste-Data-Science---H-F_R0346387",
    careers_url="https://thales.wd3.myworkdayjobs.com/Careers", visa_handling_evidence=FR_VISA, language="French + English",
    paid=FR_PAID, start_date_fit="6-month Bac+5 internship; start not stated; posted 2026-11-03", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="Python scikit-learn/pandas analysis role; asks topological data analysis (TDA) — not on CV, learn basics",
    priority="A", evidence_note="Live via Workday API")
add(company="Thales", country="France", city="Toulouse", sector="Aerospace & defence", size_reputation="CAC 40 group",
    offer_title="STAGE – Ingénieur IA appliquée à l'exploitation Cloud – F/H (R0343224)",
    offer_url="https://thales.wd3.myworkdayjobs.com/Careers/job/Toulouse/STAGE---Ingnieur-IA-applique--l-exploitation-Cloud---F---H_R0343224-1",
    careers_url="https://thales.wd3.myworkdayjobs.com/Careers", visa_handling_evidence=FR_VISA, language="French",
    paid=FR_PAID, start_date_fit="6-month PFE; start not stated; posted 2026-10-21", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="AI for cloud operations ≈ anomaly detection on ops logs + MLOps",
    priority="B", evidence_note="Live via Workday API")
add(company="Thales", country="France", city="Moirans", sector="Aerospace & defence", size_reputation="CAC 40 group",
    offer_title="STAGE – Data scientist, contexte international – assurance qualité – F/H (R0344736)",
    offer_url="https://thales.wd3.myworkdayjobs.com/Careers/job/Moirans/STAGE---Data-scientist--contexte-international---assurance-qualit---F-H_R0344736-1",
    careers_url="https://thales.wd3.myworkdayjobs.com/Careers", visa_handling_evidence=FR_VISA, language="French; international context",
    paid=FR_PAID, start_date_fit="3–6 months from Feb 2027 (fits)", application_channel="Workday (online)",
    fit_score_1to5=3, fit_reason="Quality data + dataviz (Power BI/Tableau) — lighter ML", priority="B", evidence_note="Live via Workday API")
add(company="Thales", country="France", city="Élancourt", sector="Aerospace & defence (optronics)", size_reputation="CAC 40 group",
    offer_title="Stage ingénieur IA / Deep Learning pour la classification sur images – H/F (R0344089)",
    offer_url="https://thales.wd3.myworkdayjobs.com/Careers/job/Elancourt/Stage-ingnieur-IA---Deep-Learning-pour-la-classification-sur-images---H-F_R0344089-1",
    careers_url="https://thales.wd3.myworkdayjobs.com/Careers", visa_handling_evidence=FR_VISA + " | RISK: defence site — security vetting may exclude non-EU nationals (UNVERIFIED for this offer)",
    language="French", paid=FR_PAID, start_date_fit="Start not stated; posted 2026-10-29", application_channel="Workday (online)",
    fit_score_1to5=3, fit_reason="Computer vision (CNN/ViT from captioning project)", priority="C", evidence_note="Live via Workday API")
add(company="Airbus Commercial Aircraft", country="France", city="Toulouse", sector="Aerospace", size_reputation="World #1 aircraft maker",
    offer_title="STAGE 2027 – Acoustic Testing : Développement d'outils d'IA appliqués aux données acoustiques d'essais (JR10444460)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Toulouse-Area/STAGE-2027---Acoustic-Testing---Dveloppement-d-outils-d-IA-appliqus-aux-donnes-acoustiques-d-essais--F-H-_JR10444460",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA, language="English + French (negotiation level)",
    paid=FR_PAID, start_date_fit="6 months, ideally Feb 2027 (fits)", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="AI on test data to flag production defects = anomaly detection + data audit", priority="A",
    evidence_note="Live via Workday API (posted 2026-11-02)")
add(company="ATR (Airbus / Leonardo JV)", country="France", city="Toulouse (Blagnac)", sector="Aerospace", size_reputation="World leader regional turboprops",
    offer_title="ATR – Internship 2027 – AI & Data Engineering – Automated Technical Knowledge Extraction (JR10447326)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Toulouse-Area/ATR---Internship-2027----AI---Data-Engineering---Automated-Technical-Knowledge-Extraction_JR10447326",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA, language="French fluent + English ≥ B2",
    paid=FR_PAID, start_date_fit="Feb/Mar 2027, 6 months (fits)", application_channel="Workday (online)",
    fit_score_1to5=5, fit_reason="Knowledge extraction from technical docs = Garage Augmenté (697k pages of manuals, OCR, RAG)", priority="A",
    evidence_note="Live via Workday API (posted 2026-10-16)")
add(company="Airbus Helicopters", country="France", city="Marignane", sector="Aerospace", size_reputation="World #1 civil helicopters",
    offer_title="STAGE 2027 – Data Scientist – IA & Facilitateurs Numériques (JR10444528)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Marseille-Area/STAGE-2027---Data-Sciencist---IA---Facilitateurs-Numriques--h-f-_JR10444528",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA + " | RISK: Marignane postings checked state 'nécessite une habilitation de sécurité' — confirm eligibility for a Tunisian national before investing time",
    language="English + French (intermediate/advanced)", paid=FR_PAID, start_date_fit="6 months, ideally Jan 2027", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="Predictive decision-support DS role", priority="B", evidence_note="Live via Workday API (posted 2026-10-14); clearance text seen on sibling Marignane posting JR10444521")
add(company="Airbus Helicopters", country="France", city="Marignane", sector="Aerospace", size_reputation="World #1 civil helicopters",
    offer_title="STAGE 2027 en Conception de Conversations et Gestion des Connaissances IA (JR10444521)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Marseille-Area/STAGE-2027--en-Conception-de-Conversations-et-Gestion-des-Connaissances-IA--h-f-_JR10444521",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA + " | RISK: posting says 'nécessite une habilitation de sécurité ou … être éligible à une habilitation'",
    language="English + French fluent", paid=FR_PAID, start_date_fit="6 months, ideally Jan 2027", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="Turn technical docs into AI knowledge base = RAG experience", priority="C", evidence_note="Live via Workday API (posted 2026-11-03); clearance requirement explicit")
add(company="Airbus Atlantic", country="France", city="Nantes", sector="Aerostructures", size_reputation="Airbus subsidiary, ~15k employees",
    offer_title="STAGE 2027 – Ingénieur Data & Procédés Composites (JR10446763)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Nantes-Area/STAGE-2027---Ingnieur-Data---Procds-Composites--ALL-GENDER-_JR10446763",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA, language="French",
    paid=FR_PAID, start_date_fit="Jan 2027, 6 months (fits)", application_channel="Workday (online)",
    fit_score_1to5=3, fit_reason="Industrial process data; mandatory-internship wording matches PFE", priority="B", evidence_note="Live via Workday API")
add(company="Airbus Atlantic", country="France", city="Montoir-de-Bretagne", sector="Aerostructures / MRO", size_reputation="Airbus subsidiary",
    offer_title="STAGE 2027 – Digitalisation d'atelier de maintenance aéronautique (JR10442723)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Saint-Nazaire-Area/STAGE-2027---Digitalisation-d-atelier-de-maintenance-mcanique--ALL-GENDER-_JR10442723",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA, language="French fluent, English intermediate",
    paid=FR_PAID, start_date_fit="Mar 2027, 6 months (ends Aug — check ESPRIT)", application_channel="Workday (online)",
    fit_score_1to5=3, fit_reason="Maintenance digitalisation; less ML-heavy", priority="C", evidence_note="Live via Workday API")
add(company="Airbus", country="France", city="Paris area", sector="Aerospace", size_reputation="World #1 aircraft maker",
    offer_title="STAGE 2027 Déploiement de l'Intelligence Artificielle sur un site de production (JR10443609)",
    offer_url="https://ag.wd3.myworkdayjobs.com/Airbus/job/Paris-Area/STAGE-2027-Dploiement-de-l-Intelligence-Artificielle-sur-un-site-de-production_JR10443609",
    careers_url="https://ag.wd3.myworkdayjobs.com/Airbus", visa_handling_evidence=FR_VISA + " | RISK: posting says 'Ce stage nécessite une habilitation'",
    language="English + French fluent", paid=FR_PAID, start_date_fit="6 months, ideally Jan 2027", application_channel="Workday (online)",
    fit_score_1to5=4, fit_reason="Recommenders + text analytics in production plant", priority="C", evidence_note="Live via Workday API; clearance required")
add(company="Sanofi (Digital M&S Data & AI)", country="France", city="Lyon", sector="Pharma", size_reputation="CAC 40, ~90k employees",
    offer_title="Internship 6 months – Data and IA engineer (R2873938)",
    offer_url="https://sanofi.wd3.myworkdayjobs.com/SanofiCareers/job/Lyon/internship-6-months-data-and-ia-engineer_R2873938",
    careers_url="https://sanofi.wd3.myworkdayjobs.com/SanofiCareers", visa_handling_evidence=FR_VISA, language="English fluent",
    paid=FR_PAID, start_date_fit="January 2027, 6 months (fits)", application_channel="Workday (online)",
    fit_score_1to5=5, fit_reason="Multi-agent / agentic AI from prototype to production in manufacturing = RAG + MLOps chain", priority="A",
    evidence_note="Live via Workday API (posted 2026-10-23)")
add(company="Safran Helicopter Engines", country="France", city="Tarnos", sector="Aerospace propulsion", size_reputation="CAC 40 group, ~100k employees",
    offer_title="Stage Data Scientist F/H (ref. 189784) — chatbot for industrial-application support, LLMs, agentic",
    offer_url="https://www.safran-group.com/fr/offres/france/tarnos/stage-data-scientist-fh-189784",
    careers_url="https://www.safran-group.com/fr/offres", visa_handling_evidence=FR_VISA, language="French (EN version of posting exists)",
    paid=FR_PAID, start_date_fit="3–6 months from Feb 2027 (fits)", application_channel="Safran careers site (online)",
    fit_score_1to5=5, fit_reason="LLM chatbot + classification + agents for industrial apps = Garage Augmenté RAG + ATOR classifier",
    priority="A", evidence_note="Safran site blocks automated access (Cloudflare 403); content confirmed via search-engine index 2026-11-03 — open it yourself to confirm it's live")
add(company="Safran Landing Systems / Safran (Bordes site)", country="France", city="Bordes", sector="Aerospace", size_reputation="CAC 40 group",
    offer_title="Stage Data Analyst Business Intelligence F/H (ref. 189775)",
    offer_url="https://www.safran-group.com/fr/offres/france/bordes/stage-data-analyst-business-intelligence-fh-189775",
    careers_url="https://www.safran-group.com/fr/offres", visa_handling_evidence=FR_VISA, language="French",
    paid=FR_PAID, start_date_fit="3–6 months from Jan 2027", application_channel="Safran careers site",
    fit_score_1to5=2, fit_reason="BI/analyst — under-uses your ML profile; apply only as backup at Safran", priority="C",
    evidence_note="Search-engine index only (site blocks bots); entity name on this site UNVERIFIED")
add(company="ENGIE Axima (Direction Maintenance Prédictive)", country="France", city="Paris La Défense", sector="Energy services",
    size_reputation="ENGIE group, CAC 40", offer_title="Stagiaire Data Scientist Maintenance Prédictive (H/F)",
    offer_url="https://www.wizbii.com/company/engie/job/stagiaire-data-scientist-maintenance-predictive-h-f",
    careers_url="https://jobs.engie.com/", visa_handling_evidence=FR_VISA, language="French",
    paid=FR_PAID, start_date_fit="6 months; start not stated", application_channel="Wizbii → ENGIE ATS",
    fit_score_1to5=4, fit_reason="Anomaly + drift detection on HVAC sensors, R + time series", priority="B",
    evidence_note="Aggregator page says 'expire bientôt' — may close soon; ENGIE careers URL not HTTP-checked (UNVERIFIED)")
add(company="Askills (for an unnamed major energy company)", country="France", city="Lyon", sector="Engineering consulting",
    size_reputation="UNVERIFIED — intermediary; end client not named", offer_title="Stage Data Scientist/IA – Développement d'Agents IA appliqués à l'ingénierie",
    offer_url="https://www.collective.work/jobs/fr/stage-data-scientistia-developpement-dagents-ia-appliques-a-lingenierie-hf-joj2",
    careers_url="https://www.collective.work/", visa_handling_evidence=FR_VISA, language="French",
    paid=FR_PAID, start_date_fit="Feb/Mar 2027, 6 months (fits)", application_channel="collective.work",
    fit_score_1to5=4, fit_reason="Advanced RAG + agents + evaluation framework", priority="C",
    evidence_note="Aggregator only; reputation of host UNVERIFIED (your rule: no unknown hosts)")

# ---------------- FRANCE: spontaneous / watch ----------------
for c, city, sec, rep, url, fit, reason, pr in [
    ("Renault Group", "Guyancourt (Technocentre)", "Automotive", "Global carmaker", "https://www.renaultgroup.com/en/careers/", 4,
     "Publishes 'CS27' PFE offers (incl. data/AI for Industry 4.0, data engineering from 01/01/2027 seen on engagement-jeunes)", "B"),
    ("Stellantis", "Poissy / Vélizy", "Automotive", "Global carmaker", "https://www.stellantis.com/en/careers", 3,
     "AI/data PFE seen on aggregators (Jan 2027 start) — confirm on official site", "B"),
    ("Schneider Electric", "Grenoble / Rueil", "Energy management & automation", "CAC 40", "https://www.se.com/fr/fr/about-us/careers/overview.jsp", 4,
     "Industrial IoT + predictive maintenance products", "B"),
    ("EDF (EDF R&D)", "Palaiseau (Paris-Saclay)", "Energy", "State-owned utility", "https://www.edf.fr/edf-recrute", 4,
     "Applied ML on plant/sensor data, forecasting", "B"),
    ("Orange (Orange Innovation)", "Châtillon / Rennes", "Telecom", "CAC 40", "https://orange.jobs/", 4,
     "AI/LLM + network anomaly detection (security background = plus)", "B"),
    ("Michelin", "Clermont-Ferrand", "Tyres / industry", "CAC 40", "https://www.michelin.com/en/careers", 4,
     "Industry 4.0, predictive maintenance in plants", "B"),
    ("Air France Industries (AFI KLM E&M)", "Roissy / Orly", "Aircraft MRO", "Air France-KLM group", "https://recrutement.airfrance.com/", 5,
     "Past 'Stage Data Science – maintenance prédictive' offer (2025) shows recurring topic", "B"),
    ("Alstom", "Saint-Ouen / Villeurbanne", "Rail", "Global rail OEM", "https://www.alstom.com/careers", 4,
     "Rail predictive maintenance (HealthHub)", "B"),
    ("Dassault Systèmes", "Vélizy", "Software", "CAC 40", "https://careers.3ds.com/", 3, "AI in industrial software; competitive", "C"),
    ("Capgemini (Invent / Engineering)", "Paris / Toulouse", "IT & engineering services", "CAC 40, 340k employees", "https://www.capgemini.com/fr-fr/carrieres/", 3,
     "Large PFE intake, accustomed to foreign interns; RAG/MLOps projects", "B"),
    ("Valeo", "Bobigny / Créteil", "Automotive supplier", "Global tier-1", "https://valeo.wd3.myworkdayjobs.com/valeo_jobs", 3,
     "R&D trainees; few DS-labelled offers today", "C"),
    ("Dataiku", "Paris", "AI platform software", "Unicorn, established", "https://job-boards.greenhouse.io/dataiku/jobs/5339585004", 3,
     "Only 'Software Engineer Intern – Paris' open now; DS fit indirect", "C"),
]:
    add(company=c, country="France", city=city, sector=sec, size_reputation=rep, offer_title="Spontaneous application / watch for 2027 PFE offers",
        offer_url="", careers_url=url, visa_handling_evidence=FR_VISA, language="French/English", paid=FR_PAID,
        start_date_fit="Feb 2027 realistic for FR", application_channel="Careers portal + spontaneous email/LinkedIn to hiring teams",
        fit_score_1to5=fit, fit_reason=reason, priority=pr, evidence_note="Careers URL reachable (HTTP 200/403 bot-block) on check date")

# ---------------- GERMANY ----------------
add(company="Robert Bosch GmbH", country="Germany", city="Schwieberdingen", sector="Automotive / industrial tech", size_reputation="~420k employees",
    offer_title="Pflichtpraktikum im Bereich Agentic AI Harness, Generative KI und agentische Workflows (744000158529669)",
    offer_url="https://jobs.smartrecruiters.com/BoschGroup/744000158529669", careers_url="https://jobs.smartrecruiters.com/BoschGroup",
    visa_handling_evidence=DE_VISA + " | Posting: mandatory internship, enrolment required, attach 'gültige Arbeits- und Aufenthaltserlaubnis' if applicable",
    language="Very good English + beginner German (German not on your CV — start an A1 course to qualify)", paid=DE_PAID, start_date_fit="6 months, start by agreement → target Mar 2027",
    application_channel="SmartRecruiters (online)", fit_score_1to5=4, fit_reason="GenAI agents & workflows = RAG/n8n experience", priority="A",
    evidence_note="Live via SmartRecruiters API (posted 2026-10-29)")
add(company="Robert Bosch GmbH", country="Germany", city="Stuttgart", sector="Automotive / industrial tech", size_reputation="~420k employees",
    offer_title="Internship in Digital & Integrated Production Solutions (744000159155779)",
    offer_url="https://jobs.smartrecruiters.com/BoschGroup/744000159155779", careers_url="https://jobs.smartrecruiters.com/BoschGroup",
    visa_handling_evidence=DE_VISA, language="Fluent English", paid=DE_PAID, start_date_fit="6 months, start by agreement → target Mar 2027",
    application_channel="SmartRecruiters (online)", fit_score_1to5=4, fit_reason="Shop-floor data + IT solutions; English-only team", priority="A",
    evidence_note="Live via SmartRecruiters API (posted 2026-11-02)")
add(company="Robert Bosch GmbH (all mandatory internships)", country="Germany", city="Various", sector="Automotive / industrial tech",
    size_reputation="~420k employees", offer_title="Watch 'Pflichtpraktikum'/'Mandatory internship' + data/AI; many require fluent German — filter on 'Languages: English'",
    offer_url="", careers_url="https://jobs.smartrecruiters.com/BoschGroup", visa_handling_evidence=DE_VISA, language="Check each (many need German)",
    paid=DE_PAID, start_date_fit="Mar 2027", application_channel="SmartRecruiters", fit_score_1to5=3,
    fit_reason="Large volume of 6-month data/AI internships", priority="B", evidence_note="Board live (API) on check date")
add(company="ABB Research Center Germany", country="Germany", city="Mannheim", sector="Electrification & automation", size_reputation="Global, ~110k employees",
    offer_title="MSc or BSc Thesis / Internship (m/f/d) AI for Intent-Based Networking (JR00043251)",
    offer_url="https://abb.wd3.myworkdayjobs.com/External_Career_Page/job/Mannheim-Baden-Wurttemberg-Germany/MSc-or-BSc-Thesis---Internship--m-f-d--AI-for-Intent-Based-Networking_JR00043251-1",
    careers_url="https://abb.wd3.myworkdayjobs.com/External_Career_Page", visa_handling_evidence=DE_VISA, language="Fluent English",
    paid=DE_PAID, start_date_fit="Start not stated; posted 2026-10-22", application_channel="Workday (online)",
    fit_score_1to5=3, fit_reason="LLM/NLP: generate network requirements from text; CCNA background is a plus", priority="B",
    evidence_note="Live via Workday API")
for c, city, sec, rep, url, fit, reason, pr in [
    ("Siemens AG", "Munich / Erlangen", "Industrial automation", "~320k employees", "https://jobs.siemens.com/", 4,
     "Search 'Mandatory Internship' + data science; English-speaking teams in Digital Industries", "B"),
    ("SAP SE", "Walldorf / Berlin", "Enterprise software", "Largest EU software co.", "https://jobs.sap.com/", 3,
     "Many AI internships in English; check 'Internship' + 'AI'", "B"),
    ("Infineon Technologies", "Munich / Dresden", "Semiconductors", "DAX", "https://www.infineon.com/cms/en/careers/", 3,
     "ML for manufacturing data; many roles German-speaking", "C"),
    ("Fraunhofer IAIS", "Sankt Augustin", "Applied research institute", "Europe's largest applied-research org.", "https://www.iais.fraunhofer.de/en/career.html", 4,
     "Applied ML/LLM projects with industry; English common", "B"),
    ("Fraunhofer (all institutes, e.g. IPA, IOSB, IIS)", "Various", "Applied research", "Fraunhofer-Gesellschaft", "https://jobs.fraunhofer.de/", 4,
     "Search 'Praktikum' + 'machine learning' / 'anomaly'", "B"),
    ("DLR – German Aerospace Center", "Various", "Aerospace research", "Federal research centre", "https://www.dlr.de/en/careers", 3,
     "Applied AI for aerospace; security screening possible (UNVERIFIED)", "C"),
    ("Carl Zeiss AG", "Oberkochen / Jena", "Optics & industrial tech", "Global, ~45k employees", "https://www.zeiss.com/career/en/home.html", 3,
     "ML internships (e.g., synthetic data) seen on aggregators — confirm on official site", "C"),
    ("Schaeffler AG", "Herzogenaurach", "Automotive & industrial bearings", "Global tier-1", "https://www.schaeffler.com/en/careers/", 4,
     "Condition monitoring / predictive maintenance products", "B"),
]:
    add(company=c, country="Germany", city=city, sector=sec, size_reputation=rep, offer_title="Spontaneous application / watch for mandatory-internship offers",
        offer_url="", careers_url=url, visa_handling_evidence=DE_VISA, language="English (check German requirement per offer)", paid=DE_PAID,
        start_date_fit="Mar 2027 realistic (BA approval + visa)", application_channel="Careers portal", fit_score_1to5=fit,
        fit_reason=reason, priority=pr, evidence_note="Careers URL reachable (HTTP 200/403 bot-block) on check date")

# ---------------- SWITZERLAND ----------------
add(company="ABB Corporate Research Switzerland", country="Switzerland", city="Baden-Dättwil", sector="Electrification & automation",
    size_reputation="Global, ~110k employees", offer_title="Internship in Domain Adaptation for Time-Series Using Deep-Learning f/m/d (80–100%) (JR00026201)",
    offer_url="https://abb.wd3.myworkdayjobs.com/External_Career_Page/job/Baden-Daettwil-Aargau-Switzerland/Internship-in-Domain-Adaptation-for-Time-Series-Using-Deep-Learning--80-100--_JR00026201",
    careers_url="https://abb.wd3.myworkdayjobs.com/External_Career_Page",
    visa_handling_evidence=CH_VISA + " | Posting: 'You hold a current valid VISA/work permit for Switzerland or a confirmation for a mandatory internship from your university'",
    language="English", paid=CH_PAID, start_date_fit="Start not stated; posted 2026-10-16 → propose Feb/Mar 2027",
    application_channel="Workday (online)", fit_score_1to5=5,
    fit_reason="Industrial time series + DL + domain shift = ATOR drift monitoring/PSI + anomaly detection; explicit mandatory-internship route",
    priority="A", evidence_note="Live via Workday API")
for c, city, sec, rep, url, fit, reason, pr in [
    ("Roche", "Basel / Kaiseraugst", "Pharma", "Global top-3 pharma", "https://careers.roche.com/global/en", 3,
     "6-month data internships exist (e.g., Real World Data, Apr 2026); watch for 2027", "B"),
    ("Swiss Re", "Zurich", "Reinsurance", "Global #2 reinsurer", "https://careers.swissre.com/", 3,
     "Intern Data Scientist roles recur (one checked was closed/410)", "B"),
    ("Hitachi Energy", "Baden / Zurich", "Power grids", "Global", "https://www.hitachienergy.com/careers", 3,
     "Many CH internships (80–100%); few DS-labelled today", "C"),
    ("Novartis", "Basel", "Pharma", "Global top-3 pharma", "https://www.novartis.com/careers", 2, "No DS internship found on check date", "C"),
    ("CSEM", "Neuchâtel", "Applied research & technology", "Swiss RTO", "https://www.csem.ch/en/jobs/", 4,
     "Applied ML for industry (edge AI, time series)", "B"),
    ("Idiap Research Institute", "Martigny", "AI research institute", "EPFL-affiliated", "https://www.idiap.ch/en/join-us", 2,
     "Research-heavy (you prefer applied)", "C"),
]:
    add(company=c, country="Switzerland", city=city, sector=sec, size_reputation=rep, offer_title="Spontaneous application / watch for internship offers",
        offer_url="", careers_url=url, visa_handling_evidence=CH_VISA, language="English", paid=CH_PAID,
        start_date_fit="Feb/Mar 2027 if employer handles permit", application_channel="Careers portal",
        fit_score_1to5=fit, fit_reason=reason, priority=pr, evidence_note="Careers URL reachable on check date")

# ---------------- TUNISIA ----------------
add(company="InstaDeep (a BioNTech company)", country="Tunisia", city="Tunis", sector="AI (decision-making AI, biotech AI)",
    size_reputation="Acquired by BioNTech (2023); founded in Tunis", offer_title="Internships page — 5–6-month internships; apply per role",
    offer_url="https://www.instadeep.com/internships/", careers_url="https://www.instadeep.com/careers/",
    visa_handling_evidence=TN_VISA + " | Page: internships target local talent; no visa sponsorship (irrelevant for you in Tunis)",
    language="English", paid=TN_PAID, start_date_fit="5–6 months (fits Feb 2027)", application_channel="Role-specific application link only (no email)",
    fit_score_1to5=5, fit_reason="Top AI employer in Tunisia; MLOps/DevOps & research-engineer intern tracks have existed", priority="A",
    evidence_note="Page live; Tunis office not shown in the filtered view → confirm Tunis openings on the page")
for c, sec, rep, url, fit, reason, pr, note in [
    ("STMicroelectronics (Tunis R&D)", "Semiconductors", "Global, Tunis R&D site", "https://www.st.com/content/st_com/en/about/careers.html", 4,
     "Published PFE 2026 GenAI/data topics → expect 2027 PFE book", "B", "Site did not answer automated check (UNVERIFIED reachability)"),
    ("Vermeg", "Fintech software", "Tunisian-origin software group, global clients", "https://www.vermeg.com/careers/", 3, "Data/AI PFE topics in finance software", "B", "Careers URL reachable"),
    ("Sofrecom Tunisie (Orange group)", "Telecom consulting", "Orange subsidiary", "https://www.sofrecom.com/", 3, "AI/GenAI PFE topics (seen in Morocco entity)", "B", "Homepage reachable; careers subpage 404"),
    ("Dräxlmaier Group (Tunisia plants)", "Automotive wiring", "German family group, large TN employer", "https://www.draexlmaier.com/en/career", 3, "Industrial data / quality analytics", "B", "Careers URL reachable"),
    ("Talan Tunisie", "IT consulting", "Talan group (FR)", "https://www.talan.com/", 3, "Data & AI PFE book; Tunis–France projects", "B", "Homepage reachable; careers subpage 404"),
    ("Cognira", "Retail AI (demand forecasting)", "Established retail-analytics firm (US/TN)", "https://cognira.com/careers/", 4, "Data Science PFE on demand forecasting / XAI listed on tanqeeb (undated)", "B", "Careers URL reachable"),
    ("KPMG Tunisie", "Audit & advisory", "Big Four", "https://emplois-afrique.kpmg.com/emploi/tunis/stagiaire-pfe-plateforme-d-evaluation-et-d-optimisation-de-l-empreinte-carbone-numerique-via-l-ia/3358/30342978944", 3,
     "AI PFE topics in Tunis (undated listing)", "C", "Listing URL from search index, not HTTP-checked (UNVERIFIED live)"),
    ("Sagemcom (Tunisia)", "Telecom/energy devices", "French group with TN site", "https://www.sagemcom.com/", 2, "Embedded/IoT data", "C", "Homepage reachable"),
    ("LEONI (Tunisia plants)", "Automotive wiring", "Large TN employer", "https://www.leoni.com/", 2, "Manufacturing analytics", "C", "Homepage reachable; careers subpage 404"),
]:
    add(company=c, country="Tunisia", city="Tunis area", sector=sec, size_reputation=rep, offer_title="PFE book / spontaneous application",
        offer_url="", careers_url=url, visa_handling_evidence=TN_VISA, language="French/English", paid=TN_PAID,
        start_date_fit="Feb 2027 (fits)", application_channel="Careers portal / PFE book / LinkedIn",
        fit_score_1to5=fit, fit_reason=reason, priority=pr, evidence_note=note)

# ---------------- OTHER (low feasibility) ----------------
add(company="Mitacs Globalink Research Internship", country="Canada", city="Various universities", sector="Research internship program",
    size_reputation="Canadian national program; Tunisia is a partner country", offer_title="GRI 2027 — 12 weeks, May–Jul 2027 (NOT a 6-month PFE)",
    offer_url="https://www.mitacs.ca/our-programs/globalink-research-internship-students/", careers_url="https://www.mitacs.ca/",
    visa_handling_evidence="Program arranges participation; but student deadline 16 Sep 2026 has PASSED", language="English", paid="Program-funded",
    start_date_fit="Does not fit (12 weeks, summer)", application_channel="Closed for 2027", fit_score_1to5=1,
    fit_reason="Listed only so you don't waste time on it", priority="C", evidence_note="Page reachable; deadline per secondary sources")

def write():
    for i, t in enumerate(T, 1):
        t["id"] = i
    with open("targets.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); [w.writerow({c: t.get(c, "") for c in COLS}) for t in T]
    wb = Workbook(); ws = wb.active; ws.title = "targets"
    ws.append(COLS)
    for t in T: ws.append([t.get(c, "") for c in COLS])
    hdr = PatternFill("solid", fgColor="1F3864")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF"); cell.fill = hdr; cell.alignment = Alignment(wrap_text=True, vertical="top")
    widths = {"id": 5, "company": 28, "country": 11, "city": 16, "sector": 18, "size_reputation": 22, "offer_title": 45, "offer_url": 40,
              "careers_url": 35, "visa_handling_evidence": 50, "language": 20, "paid": 22, "start_date_fit": 24, "application_channel": 22,
              "deadline": 16, "fit_score_1to5": 8, "fit_reason": 45, "priority": 8, "status": 14, "evidence_note": 35, "checked_on": 11}
    for i, c in enumerate(COLS, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(c, 15)
    for row in ws.iter_rows(min_row=2):
        for cell in row: cell.alignment = Alignment(wrap_text=True, vertical="top")
    fills = {"A": "C6EFCE", "B": "FFEB9C", "C": "F2F2F2"}
    pcol = COLS.index("priority") + 1
    for r in range(2, ws.max_row + 1):
        p = ws.cell(r, pcol).value
        ws.cell(r, pcol).fill = PatternFill("solid", fgColor=fills.get(p, "FFFFFF"))
    dv = DataValidation(type="list", formula1='"to apply,applied,followed-up,interview,offer,rejected,skip"', allow_blank=True)
    ws.add_data_validation(dv); scol = get_column_letter(COLS.index("status") + 1); dv.add(f"{scol}2:{scol}{ws.max_row}")
    ws.freeze_panes = "C2"; ws.auto_filter.ref = ws.dimensions
    # summary sheet
    s = wb.create_sheet("summary")
    s.append(["country", "A", "B", "C", "total"])
    for ctry in ["France", "Germany", "Switzerland", "Tunisia", "Canada"]:
        rows = [t for t in T if t["country"] == ctry]
        s.append([ctry] + [sum(1 for t in rows if t["priority"] == p) for p in "ABC"] + [len(rows)])
    s.append(["ALL"] + [sum(1 for t in T if t["priority"] == p) for p in "ABC"] + [len(T)])
    for cell in s[1]: cell.font = Font(bold=True)
    wb.save("targets.xlsx")
    print(len(T), "targets;", {p: sum(1 for t in T if t['priority'] == p) for p in 'ABC'})

if __name__ == "__main__":
    write()

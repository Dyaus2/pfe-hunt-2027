"""Generates the 10 tailored letters for A-priority targets (see 03_targets/targets.xlsx).
Hooks quote only facts stated in the postings checked on 2026-11-03."""
from pathlib import Path

HEAD_EN = "Hazem Ilahi\nTunis, Tunisia · +216 97 111 410 · hazem.ilahi@esprit.tn · linkedin.com/in/hazem-ilahi-016a7a315 · github.com/Dyaus2\n\n[Date]\n"
HEAD_FR = "Hazem Ilahi\nTunis, Tunisie · +216 97 111 410 · hazem.ilahi@esprit.tn · linkedin.com/in/hazem-ilahi-016a7a315 · github.com/Dyaus2\n\n[Date]\n"

P_EN = {
 "ator": "- **Anomaly detection + calibrated classification on event data.** At NEXT STEP IT (2026) I designed the ML layer of a forensics framework: Isolation Forest plus a Platt-calibrated histogram gradient-boosting classifier on 110 behavioural features per process. Coverage rose from **18% to 84% at a 1% false-positive rate**; PR-AUC **0.927** vs 0.278 for rules; 1.6% calibration error; 5-fold cross-validation grouped by capture.",
 "mlops": "- **MLOps that protects production.** Weekly snapshot → ETL → retraining → 14 offline quality gates → 7-day silent champion/challenger trial on live traffic → atomic canary deployment with automatic rollback and PSI drift monitoring; 500+ tests, including fault-injection tests proving an ML failure never stops the rule engine.",
 "rag": "- **Hybrid RAG on technical documentation.** In the Garage Augmenté team project I own the knowledge base and retrieval layer: 2,019 owner's manuals (≈697,000 pages, 26 brands) collected by 7 resumable scrapers, Tesseract OCR on ≈18,500 pages, a 98,000-unit index (≈39M tokens), hybrid BGE-M3 + BM25 search with reciprocal rank fusion, cross-encoder reranking, metadata filters, and an ablation bench (hit@k, MRR).",
 "ts": "- **Time series.** ARIMA/SARIMA modelling with diagnostics and forecasts (U.S. construction spending, R), plus drift monitoring (PSI) on production features.",
 "cv": "- **Deep learning for vision.** Reproduced Show, Attend and Tell (CNN + LSTM attention) and extended it with a ViT encoder, CLIP reranking and BLIP fine-tuning (PyTorch).",
 "e2e": "- **End-to-end data product.** Kadastra: ≈26,000 scraped listings, XGBoost pricing, a data-leak fix, and deployment with FastAPI, Django, React and Docker.",
}
P_FR = {
 "ator": "- **Détection d'anomalies et classification calibrée sur des données d'événements.** Chez NEXT STEP IT (2026), j'ai conçu la couche ML d'un framework d'investigation numérique : Isolation Forest et classifieur par gradient boosting calibré (Platt) sur 110 variables comportementales par processus. Couverture portée de **18 % à 84 % à 1 % de faux positifs** ; PR-AUC de **0,927** contre 0,278 pour les règles ; erreur de calibration de 1,6 % ; validation croisée à 5 plis groupée par capture.",
 "mlops": "- **Un MLOps qui protège la production.** Snapshot hebdomadaire → ETL → réentraînement → 14 critères de qualité hors ligne → essai silencieux champion/challenger de 7 jours sur le trafic réel → déploiement atomique avec contrôle canari, retour arrière automatique et surveillance de la dérive (PSI) ; plus de 500 tests, dont des tests d'injection de pannes.",
 "rag": "- **RAG hybride sur de la documentation technique.** Dans le projet Garage Augmenté, je suis responsable de la base de connaissances et de la recherche : 2 019 manuels (≈ 697 000 pages, 26 marques) collectés par 7 collecteurs reprenables, OCR Tesseract de ≈ 18 500 pages, index de 98 000 unités (≈ 39 M tokens), recherche hybride BGE-M3 + BM25 fusionnée par RRF, reranking par cross-encoder, filtres de métadonnées et banc d'ablation (hit@k, MRR).",
 "ts": "- **Séries temporelles.** Modélisation ARIMA/SARIMA avec diagnostics et prévisions (dépenses de construction aux États-Unis, R) et surveillance de la dérive (PSI) des variables en production.",
 "cv": "- **Deep learning pour la vision.** Reproduction de Show, Attend and Tell (CNN + LSTM à attention), étendu avec un encodeur ViT, un reranking CLIP et un fine-tuning de BLIP (PyTorch).",
 "e2e": "- **Produit data de bout en bout.** Kadastra : ≈ 26 000 annonces collectées, estimation de prix par XGBoost, correction d'une fuite de données, déploiement FastAPI, Django, React et Docker.",
}

VISA_FR = ("**Aspects pratiques.** Ce stage est le stage de fin d'études obligatoire (6 mois) de mon cycle ingénieur, à partir de **{start}**. "
           "ESPRIT signe une convention tripartite, et je dépose ma demande de visa long séjour « stagiaire » dès sa signature. Je travaille en français et en anglais.")
VISA_DE = ("**Practicalities.** This is the mandatory 6-month end-of-studies internship (PFE) of my engineering degree; I can start in **{start}**. "
           "As a student of a foreign university, the internship needs approval from the Federal Employment Agency (§ 15 No. 6 BeschV). "
           "The host requests it with a short form (registration form + internship plan), and I take care of the visa. ESPRIT signs a tripartite agreement.")
VISA_CH = ("**Practicalities.** This is the mandatory 6-month end-of-studies internship (PFE) of my engineering degree, from **{start}**. "
           "As your posting requires, ESPRIT will provide a written confirmation that the internship is mandatory, and it signs a tripartite agreement.")
VISA_FR_EN = ("**Practicalities.** This is the mandatory 6-month end-of-studies internship (PFE) of my engineering degree, from **{start}**. "
              "ESPRIT signs a tripartite internship agreement (convention de stage), and I apply for the French long-stay 'stagiaire' visa as soon as it is signed.")
VISA_TN = ("**Practicalities.** This is the mandatory 6-month end-of-studies internship (PFE) of my engineering degree at ESPRIT, from **{start}**, "
           "under ESPRIT's internship agreement.")

L = [
 dict(file="01_ABB_CH_time_series_domain_adaptation_EN.md", lang="en", company="ABB Corporate Research (Baden-Dättwil, Switzerland)",
      offer="Internship in Domain Adaptation for Time-Series Using Deep-Learning (JR00026201)", start="February/March 2027",
      hook="Models that silently degrade when the data distribution shifts are the failure mode I spent my last internship guarding against (drift monitoring, gated retraining). Your project on domain adaptation for industrial time series is the most direct continuation of that work I have seen.",
      proofs=["ator", "mlops", "ts"],
      bridge="Monitoring distribution shift (PSI) and refusing to promote a model that fails offline gates taught me to treat domain shift as a measurable engineering problem. I'd like to go one step further with you and *adapt* models across domains instead of only detecting the shift.",
      visa=VISA_CH, close="I would be glad to discuss how I could contribute to the project."),
 dict(file="02_Thales_Toulouse_predictive_maintenance_FR.md", lang="fr", company="Thales – Toulouse",
      offer="STAGE – Ingénieur Data Scientist – Maintenance prédictive par IA (R0344657)", start="février 2027",
      hook="Anticiper les défaillances à partir de données de capteurs et de journaux d'exploitation : c'est exactement le type de problème sur lequel j'ai travaillé, sur des journaux système plutôt que sur des capteurs.",
      proofs=["ator", "mlops", "ts"],
      bridge="Les méthodes se transposent directement à la maintenance prédictive : variables construites à partir de journaux, détection non supervisée d'événements rares, score de risque calibré pour prioriser les interventions, surveillance de la dérive. J'aimerais les appliquer à vos équipements avec Python, scikit-learn et PyTorch.",
      visa=VISA_FR, close="Je serais ravi d'échanger avec vous lors d'un entretien."),
 dict(file="03_Safran_HE_Tarnos_data_scientist_FR.md", lang="fr", company="Safran Helicopter Engines – Tarnos",
      offer="Stage Data Scientist F/H (réf. 189784)", start="février 2027",
      hook="Votre équipe poursuit le développement d'un chatbot d'appui opérationnel aux applications industrielles, avec des modèles de classification, des modèles de langage et de l'agentique. C'est la combinaison exacte de mes deux derniers projets.",
      proofs=["rag", "ator", "mlops"],
      bridge="Je peux apporter une couche de recherche robuste (hybride, filtrée, évaluée) pour ancrer les réponses du chatbot dans votre documentation, un classifieur calibré pour router les demandes, et la discipline MLOps nécessaire pour le déployer sans régression.",
      visa=VISA_FR, close="Je serais heureux de vous présenter ces travaux lors d'un entretien."),
 dict(file="04_ATR_knowledge_extraction_FR.md", lang="fr", company="ATR – Toulouse",
      offer="Internship 2027 – AI & Data Engineering – Automated Technical Knowledge Extraction (JR10447326)", start="février/mars 2027",
      hook="Extraire automatiquement la connaissance de documents techniques volumineux et hétérogènes est le cœur de mon projet Garage Augmenté, sur des manuels automobiles.",
      proofs=["rag", "mlops"],
      bridge="Collecte, OCR des pages scannées, normalisation des métadonnées, découpage, indexation et évaluation de la recherche : je connais les pièges de chaque étape et je saurais les transposer à la documentation aéronautique d'ATR.",
      visa=VISA_FR, close="Je serais ravi d'en discuter avec vous."),
 dict(file="05_Sanofi_Lyon_data_ia_engineer_EN.md", lang="en", company="Sanofi – Digital M&S Data & AI (Lyon)",
      offer="Internship 6 months – Data and IA engineer (R2873938)", start="January/February 2027",
      hook="Your posting describes building multi-agent architectures from prototype to production and integrating agentic solutions into manufacturing and supply-chain workflows. That 'prototype-to-production' step is where I have spent most of my effort.",
      proofs=["rag", "mlops", "ator"],
      bridge="I would bring an evaluation-first approach to agentic systems (retrieval metrics, offline gates, silent trials before promotion), plus Python data pipelines that keep the data clean and governed.",
      visa=VISA_FR_EN, close="I would be glad to discuss this in an interview."),
 dict(file="06_Airbus_acoustic_testing_AI_FR.md", lang="fr", company="Airbus Commercial Aircraft – Toulouse",
      offer="STAGE 2027 – Acoustic Testing : Développement d'outils d'IA appliqués aux données acoustiques d'essais (JR10444460)", start="février 2027",
      hook="Repérer automatiquement dans les données d'essais acoustiques les signatures d'un défaut, pour que la production puisse le corriger, est un problème de détection d'anomalies, mon domaine de prédilection.",
      proofs=["ator", "mlops", "cv"],
      bridge="L'audit des données d'essais, la construction de variables, le choix entre approche non supervisée et classifieur calibré, puis l'industrialisation de l'outil : ce sont les étapes que j'ai déjà menées de bout en bout.",
      visa=VISA_FR, close="Je serais ravi d'échanger avec votre équipe."),
 dict(file="07_Thales_Bordeaux_data_science_FR.md", lang="fr", company="Thales – Bordeaux",
      offer="STAGE – Ingénieur analyste Data Science (R0346387)", start="février 2027",
      hook="Votre offre demande des bases solides en algorithmes de ML, Python (scikit-learn, pandas, NumPy) et la capacité à présenter ses conclusions : c'est mon quotidien de data scientist.",
      proofs=["ator", "ts", "e2e"],
      bridge="Je n'ai pas encore pratiqué l'analyse topologique des données (TDA) citée dans l'offre ; [à confirmer avant envoi :] je m'engage à me former à ses outils de base avant le début du stage.",
      visa=VISA_FR, close="Je serais ravi d'en discuter lors d'un entretien."),
 dict(file="08_Bosch_agentic_AI_EN.md", lang="en", company="Robert Bosch GmbH – Schwieberdingen",
      offer="Mandatory internship: Agentic AI Harness, Generative AI and agentic workflows (744000158529669)", start="March 2027",
      hook="I'm applying for your mandatory internship in agentic AI and generative-AI workflows. I build LLM-backed systems with retrieval, orchestration (n8n, FastAPI) and evaluation, and I'd like to do it at Bosch scale.",
      proofs=["rag", "mlops", "ator"],
      bridge="Agent harnesses fail silently without good tooling around them. My strength is that tooling: retrieval quality metrics, regression tests, safe rollout and rollback.",
      visa=VISA_DE, close="I'd be happy to talk. [EDIT BEFORE SENDING — the posting asks for beginner German, which is not on your CV. Keep ONE true option: 'I have beginner-level German (A1).' OR 'I am starting an A1 German course before arrival.']"),
 dict(file="09_Bosch_digital_production_EN.md", lang="en", company="Robert Bosch GmbH – Stuttgart",
      offer="Internship in Digital & Integrated Production Solutions (744000159155779)", start="March 2027",
      hook="IT solutions with a direct connection to the shop floor are where data science pays off fastest, and that is the kind of applied work I want to do in my end-of-studies internship.",
      proofs=["ator", "mlops", "e2e"],
      bridge="I can contribute Python data pipelines, anomaly detection on operational data, and production-grade services (FastAPI, Docker, automated tests) that shop-floor teams can rely on.",
      visa=VISA_DE, close="I would be glad to discuss how I can support the team."),
 dict(file="10_InstaDeep_Tunis_EN.md", lang="en", company="InstaDeep – Tunis",
      offer="[Exact internship title from instadeep.com/internships — Tunis]", start="February 2027",
      hook="InstaDeep is the reference for applied AI built in Tunisia, and I would like to spend my end-of-studies internship shipping models with a team that holds that bar.",
      proofs=["ator", "mlops", "rag"],
      bridge="Whether the role leans towards ML engineering, MLOps or applied research, I bring production habits: one feature code path for training and serving, calibrated metrics and automated rollback.",
      visa=VISA_TN, close="I would be glad to discuss this in an interview."),
]

def render(x):
    fr = x["lang"] == "fr"
    P = P_FR if fr else P_EN
    head = HEAD_FR if fr else HEAD_EN
    subj = (f"Objet : candidature – {x['offer']} – stage de fin d'études de 6 mois à partir de {x['start']}" if fr
            else f"Re: {x['offer']} — 6-month end-of-studies internship from {x['start']}")
    sal = "Madame, Monsieur," if fr else "Dear Hiring Team,"
    intro = (f"Élève ingénieur en dernière année de Data Science & IA à ESPRIT (Tunisie, diplôme prévu en 2027), je vous adresse ma candidature pour le stage {x['offer']}. {x['hook']}"
             if fr else f"I am a final-year Data Science & AI engineering student at ESPRIT (Tunisia, graduating 2027). {x['hook']}")
    lead = "Mes réalisations les plus proches de votre besoin :" if fr else "What I would bring:"
    sign = ("Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.\n\nHazem Ilahi" if fr
            else "Kind regards,\nHazem Ilahi")
    body = "\n".join(P[k] for k in x["proofs"])
    return (f"<!-- Target: {x['company']} | checked 2026-11-03 | see 03_targets/targets.xlsx -->\n\n{head}\n{x['company']}\n{subj}\n\n{sal}\n\n{intro}\n\n{lead}\n\n{body}\n\n"
            f"{x['bridge']}\n\n{x['visa'].format(start=x['start'])}\n\n{x['close']}\n\n{sign}\n")

out = Path(__file__).parent / "tailored"
out.mkdir(exist_ok=True)
for x in L:
    (out / x["file"]).write_text(render(x), encoding="utf-8")
print("wrote", len(L), "letters to", out)

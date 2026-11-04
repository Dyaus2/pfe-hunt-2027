// Single source of truth for CV content (EN + FR).
// Rule: only facts from Hazem's own CVs (latest: Hazem_Ilahi_Resume_EN/French.pdf, Nov 2026) or verified project results. No inflation.
// Rich text: a string, or an array of segments [text, url?] (url → hyperlink).

const L = {
  mail: "mailto:hazem.ilahi@esprit.tn",
  linkedin: "https://linkedin.com/in/hazem-ilahi-016a7a315",
  github: "https://github.com/Dyaus2",
  site: "https://dyaus2.github.io/",
  credly: "https://www.credly.com/earner/earned/badge/64339ed0-debf-40c3-8ec5-70c4a48f495b",
  twDemo: "https://dyaus2.github.io/turbowatch/",
  twRepo: "https://github.com/Dyaus2/turbowatch",
};

const contact = (city) => [
  [`${city} | +216 97 111 410 | `], ["hazem.ilahi@esprit.tn", L.mail], [" | "], ["linkedin.com/in/hazem-ilahi-016a7a315", L.linkedin],
  [" | "], ["github.com/Dyaus2", L.github], [" | "], ["dyaus2.github.io", L.site],
];

const EN = {
  name: "Hazem Ilahi",
  headline: "Data Science & AI Engineering Student — Machine Learning | MLOps | LLM / RAG",
  seeking: "Seeking 6-month end-of-studies internship (PFE), from Jan/Feb 2027 — open to relocation",
  seekingSub: "Mandatory curricular internship — tripartite internship agreement signed by ESPRIT",
  contact: contact("Tunis, Tunisia"),
  h: { profile: "PROFILE", exp: "EXPERIENCE", proj: "PROJECTS", skills: "TECHNICAL SKILLS", edu: "EDUCATION", cert: "CERTIFICATIONS", lang: "LANGUAGES" },
  profile:
    "Final-year engineering student in Data Science & AI at ESPRIT (graduating 2027) with hands-on experience in machine learning, MLOps and LLM/RAG systems. " +
    "During my last internship I designed the ML detection layer of a digital-forensics framework: anomaly detection plus a calibrated gradient-boosting classifier that raised attack-stage coverage from 18% to 84% at 1% false positives, shipped with a weekly retraining pipeline (champion/challenger, drift monitoring, automatic rollback). " +
    "Looking for an applied data science / ML engineering internship: anomaly detection, predictive analytics, LLM/RAG applications, MLOps, forecasting.",
  experience: [
    {
      title: "Machine Learning Intern — NEXT STEP IT (Security Operations Center)",
      right: "Jul 2026 – Sep 2026",
      sub: "ATOR DFIR — ML threat-detection layer and MLOps pipeline",
      subRight: "Charguia 1, Tunisia",
      bullets: [
        "Raised attack-stage coverage on a public adversary-emulation corpus from 18% (Sigma rules alone) to 84% (rules + ML) at a 1% false-positive rate, recovering 135 of the 168 stages missed by rules.",
        "Designed and integrated the ML layer of ATOR DFIR, a forensics and threat-hunting framework for Windows/Linux endpoints, on top of the security team's YARA/Sigma rule engine.",
        "Threat-likelihood classifier (histogram gradient boosting, Platt calibration): PR-AUC 0.927 vs 0.278 for rules, 1.6% calibration error, 5-fold cross-validation grouped by capture.",
        "Unsupervised anomaly detection (Isolation Forest, 300 trees): 23 of the top 25 flags on the benchmark were true attack stages; MITRE ATT&CK tactic classifier with confidence threshold (79.7% precision).",
        "Built the training set from 115 public attack captures (Empire, Covenant, Mimikatz, Metasploit) via ETL into the framework schema, labeled by process lineage; 110 behavioral features per process, computed by one code path shared by training and production.",
        "Weekly MLOps pipeline: snapshot, ETL, retraining, 14 offline quality gates, 7-day silent champion/challenger trial on live traffic, atomic deployment with canary check, automatic rollback, drift monitoring (PSI) and protection of retraining against reference poisoning.",
        "Integration: 10 REST endpoints and a threat-hunting page for SOC analysts (P1–P4 priorities, verdicts); 500+ automated tests, including fault-injection tests guaranteeing that an ML failure never interrupts rule-based detection.",
      ],
      stack: "Stack: Python 3.13, scikit-learn, pandas, NumPy, SQLite, FastAPI, Jinja2, pytest, Git",
    },
    {
      title: "Software Developer Intern — NEXT STEP IT",
      right: "Jul 2025 – Sep 2025",
      sub: "SOC report-generation web platform (pair internship)",
      subRight: "Charguia 1, Tunisia",
      bullets: [
        "Co-designed and developed, in a pair, a Python/Django web platform for SOC analysts with an intuitive UI/UX.",
        "Automated SOC report generation, replacing repetitive manual writing; prepared the solution for future deployment.",
      ],
      stack: "Stack: Python, Django, HTML/CSS, Git",
    },
  ],
  projects: [
    {
      // numbers: github.com/Dyaus2/turbowatch results/ (RESULTS.md, DRIFT.md, COPILOT.md, COPILOT_BROWSER.md)
      title: "TurboWatch — Predictive maintenance copilot for turbofan engines",
      right: "2026",
      sub: [["Personal project — live demo: "], ["dyaus2.github.io/turbowatch", L.twDemo], [" · code: "], ["github.com/Dyaus2/turbowatch", L.twRepo]],
      bullets: [
        "Remaining-useful-life prediction on NASA C-MAPSS turbofan data: gradient boosting with a P10–P90 band and a 1D-CNN (PyTorch) on causal, regime-normalized features shared by training and serving; test RUL RMSE 15.5 cycles (CNN) / 16.3 (GBM), mean of 5 seeds, engine-grouped splits.",
        "Calibrated risk and a k-of-n alarm policy tuned on a cost matrix: 97% of test-set failures detected a median 36 cycles ahead at a 2% false-alarm rate; SHAP explanation for every prediction.",
        "RAG maintenance copilot over FAA/NASA documents (bge-small + BM25, RRF, cross-encoder reranking): cited answers, refusal when out of scope; correct passage ranked first on 26/26 test questions, also when running fully in the browser (transformers.js).",
        "MLOps and delivery: MLflow, PSI drift detection with champion/challenger retraining (FD003 test RMSE 20.7 → 15.0), FastAPI + React/TypeScript dashboard with live replay, Docker, GitHub Actions CI.",
      ],
      stack: "Stack: Python, scikit-learn, PyTorch, SHAP, MLflow, FastAPI, sentence-transformers, React, TypeScript, Docker",
    },
    {
      title: "UnderHood (Garage Augmenté) — Multi-agent RAG assistant for automotive pre-diagnosis",
      right: "2026 – 2027",
      sub: "ESPRIT team project — owner of the knowledge base and retrieval layer",
      bullets: [
        "Corpus: 7 resumable Python collectors gathering 2,019 owner's manuals (≈697,000 pages, 26 brands, 73% official sources), covering 54 of the 56 priority models of the Tunisian market. SHA-256 deduplication, Tesseract OCR (≈18,500 pages), 364 model families, Qdrant index of 101,417 passages.",
        "Retrieval: query expansion in French / English / Tunisian Derja plus LLM query rewriting, hybrid BGE-M3 + BM25 search (RRF), brand/model/year filtering, cross-encoder reranking and exact lookup of 9,533 OBD-II codes, all exposed as a FastAPI service to the diagnostic agent (LangGraph).",
        "Evaluation: ablation on 40 questions (hit@5, MRR, double-blind LLM judging): the vehicle filter raises the share of correct answers found in the right manual from 0% to 72% (MRR 0.63).",
      ],
      stack: "Stack: Python, Qdrant, BGE-M3, BM25, FastAPI, LangGraph, PyMuPDF, Tesseract",
    },
    {
      title: "DressMe — Smart personal fashion assistant for the Tunisian market",
      right: "2026 – 2027",
      sub: "ESPRIT team project (7 people, Advanced Data Science Project) — from design to working prototype (API + mobile app)",
      bullets: [
        "Style representation: benchmarked encoders on Polyvore (152,785 items, 95% bootstrap CIs). Chose Qwen3-VL-Embedding-2B, as accurate as the 8B model but 3.7× faster. \"Fashion DNA\" learned by a Set Transformer trained contrastively (InfoNCE).",
        "Personalized outfits: compatibility head per category pair (AUC 0.852 vs 0.830 for cosine alone). Beam-search generation conditioned on weather and occasion. Personalization by Thompson sampling with a population prior, evaluated on 40 simulated personas over 60 days.",
        "Vision and generative AI: SAM 3 segmentation and garment recognition from photos (96.6% accuracy in auto-fill). Diffusion-based virtual try-on (Qwen Image Edit via ComfyUI). Local LLM stylist (Qwen 9B) with every sentence checked against facts: 199 of 200 answers grounded.",
        "Explainable AI and marketplace: exact per-criterion contributions to the score; occlusion maps evaluated for faithfulness (deletion/insertion curves); concepts shown only above 0.85 AUC; second-hand prices predicted by quantile LightGBM with conformal calibration (80.0% coverage on 423k listings), explained with TreeSHAP.",
      ],
      stack: "Stack: Python, PyTorch, FastAPI, LightGBM, llama.cpp, React Native (Expo)",
    },
    {
      title: "Kadastra — AI real-estate intelligence platform",
      right: "2026",
      sub: "ESPRIT team project (Data Crunchers) — Microsoft TDSP methodology",
      bullets: [
        "End-to-end pipeline for the Tunisian real-estate market: collection of ≈26,000 listings (Mubawab, Tayara), XGBoost price estimation, contract and investment-scenario generation.",
        "Removed a data leak in the model features; calibrated financial constants on Tunisian legislation and Central Bank (BCT) rates; full-stack deployment with FastAPI, Django, React and Docker.",
      ],
    },
    {
      title: "Show, Attend and Tell — Image captioning (computer vision + NLP)",
      right: "2026",
      sub: "Deep learning project — PyTorch, Flickr8k",
      bullets: [
        "Reproduced the CNN + LSTM attention encoder-decoder, then extended it with a ViT encoder, CLIP reranking of beam search and BLIP fine-tuning; evaluated with BLEU and attention-map visualization.",
      ],
    },
    {
      title: "Time-series forecasting — U.S. construction spending",
      right: "2026",
      sub: "Statistical modeling project in R",
      bullets: [
        "Three-phase analysis of residential construction spending (U.S. Census Bureau): graphical analysis, deterministic polynomial trends, ARIMA/SARIMA modeling with diagnostics and forecasts.",
      ],
    },
  ],
  skills: [
    ["Programming", "Python, R, SQL, C/C++, Java, PHP"],
    ["ML / DL", "scikit-learn, XGBoost, PyTorch, TensorFlow, Keras; anomaly detection, classification, probability calibration, grouped cross-validation; computer vision (CNN, ViT, CLIP, BLIP); time-series forecasting (ARIMA/SARIMA)"],
    ["LLM / RAG / NLP", "RAG pipelines, Qdrant, BGE-M3 embeddings, BM25, hybrid search, cross-encoder reranking, retrieval evaluation (hit@k, MRR), Transformers"],
    ["MLOps", "automated retraining, model registry, MLflow, champion/challenger deployment, drift monitoring (PSI), quality gates, canary deployment and rollback, pytest"],
    ["Data", "pandas, NumPy, ETL, web scraping, OCR (Tesseract), SQLite, Power BI, Tableau"],
    ["Cloud & deployment", "AWS (Cloud Foundations), Docker, Docker Compose, FastAPI, Django, Flask, Spring Boot, Symfony, REST APIs, n8n, Git"],
    ["Methods", "Microsoft TDSP, CRISP-DM, Design Thinking, Agile/Scrum"],
  ],
  education: [
    {
      title: "ESPRIT — École Supérieure Privée d'Ingénierie et de Technologies",
      right: "2023 – 2027 (expected)",
      sub: "Engineering degree program, Data Science & Artificial Intelligence — final year; 6-month mandatory end-of-studies internship (PFE) from Jan/Feb 2027",
      subRight: "Ariana, Tunisia",
    },
    {
      title: "IPEIT — Preparatory Institute for Engineering Studies of Tunis",
      right: "2020 – 2023",
      sub: "Two-year preparatory program for national engineering-school entrance exams, Physics–Chemistry",
      subRight: "Montfleury, Tunis, Tunisia",
    },
  ],
  certs: [
    [["AWS Cloud Foundations — Amazon Web Services (badge, Nov 2026) — "], ["verify on Credly", L.credly]],
    "Fundamentals of Deep Learning — NVIDIA (2026)",
    "Applications of AI for Anomaly Detection — NVIDIA (2026)",
    "Building Transformer-Based Natural Language Processing Applications — NVIDIA (2026)",
    "CCNA 2: Switching, Routing, and Wireless Essentials (SRWE) — Cisco Networking Academy (2025)",
  ],
  languages: "English: fluent | French: advanced (professional working proficiency) | Arabic: native",
};

const FR = {
  name: "Hazem Ilahi",
  headline: "Élève ingénieur en Data Science & IA — Machine Learning | MLOps | LLM / RAG",
  seeking: "Recherche un stage de fin d'études (PFE) de 6 mois à partir de janvier/février 2027 — mobilité internationale",
  seekingSub: "Stage obligatoire du cursus — convention de stage tripartite signée par ESPRIT",
  contact: contact("Tunis, Tunisie"),
  h: { profile: "PROFIL", exp: "EXPÉRIENCE PROFESSIONNELLE", proj: "PROJETS", skills: "COMPÉTENCES TECHNIQUES", edu: "FORMATION", cert: "CERTIFICATIONS", lang: "LANGUES" },
  profile:
    "Élève ingénieur en dernière année à ESPRIT (diplôme prévu en 2027), spécialité Science des Données & IA, avec une expérience pratique en machine learning, MLOps et systèmes LLM/RAG. " +
    "Lors de mon dernier stage, j'ai conçu la couche de détection par ML d'un framework d'investigation numérique : détection d'anomalies et classifieur calibré par gradient boosting, portant la couverture des étapes d'attaque de 18 % à 84 % à 1 % de faux positifs, avec une chaîne de réentraînement hebdomadaire (champion/challenger, surveillance de la dérive, retour arrière automatique). " +
    "Je recherche un stage appliqué en data science / ML engineering : détection d'anomalies, analyse prédictive, applications LLM/RAG, MLOps, prévision.",
  experience: [
    {
      title: "Stagiaire Machine Learning — NEXT STEP IT (département SOC)",
      right: "Juillet 2026 – Septembre 2026",
      sub: "ATOR DFIR — couche de détection de menaces par ML et chaîne MLOps",
      subRight: "Charguia 1, Tunisie",
      bullets: [
        "Couverture des étapes d'attaque sur un corpus public d'émulation d'adversaire portée de 18 % (règles Sigma seules) à 84 % (règles + ML) à 1 % de faux positifs ; 135 des 168 étapes manquées par les règles récupérées.",
        "Conception et intégration de la couche ML d'ATOR DFIR, framework d'investigation numérique et de chasse aux menaces sur postes Windows/Linux, au-dessus d'un moteur de règles YARA/Sigma développé par l'équipe sécurité.",
        "Classifieur de vraisemblance de menace (gradient boosting par histogrammes, calibration de Platt) : PR-AUC de 0,927 contre 0,278 pour les règles, erreur de calibration de 1,6 %, validation croisée à 5 plis groupée par capture.",
        "Détection d'anomalies non supervisée (Isolation Forest, 300 arbres) : 23 des 25 premiers signalements du benchmark sont de vraies étapes d'attaque ; classifieur de tactique MITRE ATT&CK avec seuil de confiance (79,7 % de précision).",
        "Jeu d'entraînement constitué à partir de 115 captures d'attaques publiques (Empire, Covenant, Mimikatz, Metasploit) converties par ETL vers le schéma du framework et labellisées par filiation de processus ; 110 variables comportementales par processus, calculées par un code unique partagé entre entraînement et production.",
        "Chaîne MLOps hebdomadaire : snapshot, ETL, réentraînement, 14 critères de qualité hors ligne, essai silencieux champion/challenger de 7 jours sur le trafic réel, déploiement atomique avec contrôle canari, retour arrière automatique, surveillance de la dérive (PSI) et protection du réentraînement contre l'empoisonnement de la référence.",
        "Intégration : 10 endpoints REST et page de chasse aux menaces pour analystes SOC (priorités P1–P4, verdicts) ; plus de 500 tests automatisés, dont des tests d'injection de pannes garantissant qu'une défaillance ML n'interrompt jamais la détection par règles.",
      ],
      stack: "Stack : Python 3.13, scikit-learn, pandas, NumPy, SQLite, FastAPI, Jinja2, pytest, Git",
    },
    {
      title: "Stagiaire Développeur — NEXT STEP IT",
      right: "Juillet 2025 – Septembre 2025",
      sub: "Plateforme web de génération de rapports SOC (stage en binôme)",
      subRight: "Charguia 1, Tunisie",
      bullets: [
        "Conception et développement en binôme d'une plateforme web Python/Django destinée aux analystes SOC, avec une interface UI/UX intuitive.",
        "Automatisation de la génération des rapports SOC, en remplacement de la rédaction manuelle répétitive ; préparation de la solution en vue d'un futur déploiement.",
      ],
      stack: "Stack : Python, Django, HTML/CSS, Git",
    },
  ],
  projects: [
    {
      title: "TurboWatch — Copilote de maintenance prédictive pour turboréacteurs",
      right: "2026",
      sub: [["Projet personnel — démo : "], ["dyaus2.github.io/turbowatch", L.twDemo], [" · code : "], ["github.com/Dyaus2/turbowatch", L.twRepo]],
      bullets: [
        "Prédiction de la durée de vie résiduelle (RUL) sur les données turboréacteurs NASA C-MAPSS : gradient boosting avec bande P10–P90 et CNN 1D (PyTorch) sur des variables causales normalisées par régime, partagées entre entraînement et production ; RMSE RUL sur le test de 15,5 cycles (CNN) / 16,3 (GBM), moyenne sur 5 graines, découpage par moteur.",
        "Risque calibré et politique d'alarme k parmi n réglée sur une matrice de coûts : 97 % des pannes du jeu de test détectées avec une avance médiane de 36 cycles, à 2 % de fausses alarmes ; explication SHAP de chaque prédiction.",
        "Copilote RAG de maintenance sur documents FAA/NASA (bge-small + BM25, RRF, reranking par cross-encoder) : réponses citées, refus hors périmètre ; bon passage classé premier sur 26 questions de test sur 26, y compris en exécution entièrement dans le navigateur (transformers.js).",
        "MLOps et livraison : MLflow, détection de dérive PSI avec réentraînement champion/challenger (RMSE test FD003 20,7 → 15,0), API FastAPI + tableau de bord React/TypeScript avec rejeu en direct, Docker, CI GitHub Actions.",
      ],
      stack: "Stack : Python, scikit-learn, PyTorch, SHAP, MLflow, FastAPI, sentence-transformers, React, TypeScript, Docker",
    },
    {
      title: "UnderHood (Garage Augmenté) — Assistant multi-agents de pré-diagnostic automobile (RAG)",
      right: "2026 – 2027",
      sub: "Projet d'équipe, ESPRIT — responsable de la base de connaissances et de la couche de recherche",
      bullets: [
        "Corpus : 7 collecteurs Python reprenables : 2 019 manuels du propriétaire (≈ 697 000 pages, 26 marques, 73 % de sources officielles), couvrant 54 des 56 modèles prioritaires du marché tunisien. Déduplication SHA-256, OCR Tesseract (≈ 18 500 pages), 364 familles de modèles, index Qdrant de 101 417 passages.",
        "Recherche : expansion de requêtes FR / EN / derja tunisienne et réécriture par LLM, recherche hybride BGE-M3 + BM25 (RRF), filtre marque/modèle/année, reranking par cross-encoder et consultation exacte de 9 533 codes OBD-II. Le tout est exposé en service FastAPI à l'agent de diagnostic (LangGraph).",
        "Évaluation : ablation sur 40 questions (hit@5, MRR, jugement LLM en double aveugle) : le filtre véhicule fait passer le taux de bonnes réponses dans le bon manuel de 0 % à 72 % (MRR 0,63).",
      ],
      stack: "Stack : Python, Qdrant, BGE-M3, BM25, FastAPI, LangGraph, PyMuPDF, Tesseract",
    },
    {
      title: "DressMe — Assistant de mode personnel intelligent pour le marché tunisien",
      right: "2026 – 2027",
      sub: "Projet d'équipe (7 personnes, Advanced Data Science Project), ESPRIT — de la conception au prototype fonctionnel (API + application mobile)",
      bullets: [
        "Représentation du style : benchmark d'encodeurs sur Polyvore (152 785 articles, IC bootstrap à 95 %). Choix de Qwen3-VL-Embedding-2B, aussi précis que le 8B mais 3,7× plus rapide. « Fashion DNA » apprise par un Set Transformer entraîné en contrastif (InfoNCE).",
        "Tenues personnalisées : tête de compatibilité par paire de catégories (AUC 0,852 contre 0,830 pour le cosinus seul). Génération par beam search selon la météo et l'occasion. Personnalisation par Thompson sampling avec prior de population, évaluée sur 40 personas simulées pendant 60 jours.",
        "Vision et IA générative : segmentation SAM 3 et reconnaissance des vêtements sur photo (96,6 % de précision en remplissage automatique). Essayage virtuel par diffusion (Qwen Image Edit via ComfyUI). Styliste LLM local (Qwen 9B) dont chaque phrase est vérifiée contre les faits : 199 réponses sur 200 ancrées.",
        "IA explicable et marché : contributions exactes de chaque critère au score ; cartes d'occlusion évaluées en fidélité (courbes deletion/insertion) ; concepts affichés seulement au-delà d'une AUC de 0,85 ; prix de seconde main prédits par LightGBM quantile et calibration conforme (couverture 80,0 % sur 423 k annonces), expliqués par TreeSHAP.",
      ],
      stack: "Stack : Python, PyTorch, FastAPI, LightGBM, llama.cpp, React Native (Expo)",
    },
    {
      title: "Kadastra — Plateforme d'intelligence immobilière basée sur l'IA",
      right: "2026",
      sub: "Projet d'équipe (Data Crunchers), ESPRIT — méthodologie Microsoft TDSP",
      bullets: [
        "Pipeline de bout en bout pour le marché immobilier tunisien : collecte de ≈ 26 000 annonces (Mubawab, Tayara), estimation de prix par XGBoost, génération de contrats et de scénarios d'investissement.",
        "Suppression d'une fuite de données dans les variables du modèle ; calage des constantes financières sur la législation tunisienne et les taux de la BCT ; déploiement full-stack FastAPI, Django, React et Docker.",
      ],
    },
    {
      title: "Show, Attend and Tell — Génération automatique de légendes d'images (vision + NLP)",
      right: "2026",
      sub: "Projet de Deep Learning — PyTorch, Flickr8k",
      bullets: [
        "Reproduction du modèle encodeur-décodeur à attention (CNN + LSTM), puis extensions : encodeur ViT, reranking du beam search par CLIP et fine-tuning de BLIP ; évaluation BLEU et visualisation des cartes d'attention.",
      ],
    },
    {
      title: "Analyse de séries temporelles — Dépenses de construction aux États-Unis",
      right: "2026",
      sub: "Projet de modélisation statistique en R",
      bullets: [
        "Analyse des dépenses de construction résidentielle (U.S. Census Bureau) en trois phases : analyse graphique, ajustement déterministe (tendances polynomiales), modélisation ARIMA/SARIMA avec diagnostics et prévisions.",
      ],
    },
  ],
  skills: [
    ["Langages", "Python, R, SQL, C/C++, Java, PHP"],
    ["ML / DL", "scikit-learn, XGBoost, PyTorch, TensorFlow, Keras ; détection d'anomalies, classification, calibration, validation croisée groupée ; vision par ordinateur (CNN, ViT, CLIP, BLIP) ; séries temporelles (ARIMA/SARIMA)"],
    ["LLM / RAG / NLP", "pipelines RAG, Qdrant, embeddings BGE-M3, BM25, recherche hybride, reranking par cross-encoder, évaluation hit@k / MRR, Transformers"],
    ["MLOps", "réentraînement automatisé, registre de modèles, MLflow, déploiement champion/challenger, surveillance de la dérive (PSI), critères de qualité, déploiement canari et retour arrière, pytest"],
    ["Data", "pandas, NumPy, ETL, web scraping, OCR (Tesseract), SQLite, Power BI, Tableau"],
    ["Cloud & déploiement", "AWS (Cloud Foundations), Docker, Docker Compose, FastAPI, Django, Flask, Spring Boot, Symfony, API REST, n8n, Git"],
    ["Méthodologies", "Microsoft TDSP, CRISP-DM, Design Thinking, Agile/Scrum"],
  ],
  education: [
    {
      title: "ESPRIT — École Supérieure Privée d'Ingénierie et de Technologies",
      right: "2023 – 2027 (diplôme prévu)",
      sub: "Cycle ingénieur, Science des Données & Intelligence Artificielle — dernière année ; stage de fin d'études obligatoire de 6 mois (PFE) à partir de janvier/février 2027",
      subRight: "Ariana, Tunisie",
    },
    {
      title: "IPEIT — Institut Préparatoire aux Études d'Ingénieurs de Tunis",
      right: "2020 – 2023",
      sub: "Cycle préparatoire, Physique-Chimie",
      subRight: "Montfleury, Tunisie",
    },
  ],
  certs: [
    [["AWS Cloud Foundations — Amazon Web Services (badge, novembre 2026) — "], ["vérifier sur Credly", L.credly]],
    "Fundamentals of Deep Learning — NVIDIA (2026)",
    "Applications of AI for Anomaly Detection — NVIDIA (2026)",
    "Building Transformer-Based Natural Language Processing Applications — NVIDIA (2026)",
    "CCNA 2 : Switching, Routing, and Wireless Essentials (SRWE) — Cisco Networking Academy (2025)",
  ],
  languages: "Arabe : langue maternelle | Français : courant (niveau avancé, usage professionnel) | Anglais : courant",
};

module.exports = { EN, FR };

// Single source of truth for CV content (EN + FR).
// Rule: only facts from Resume_pfe.pdf or stated by Hazem. No inflation.

const contact = "Tunis, Tunisia | +216 97 111 410 | hazem.ilahi@esprit.tn | linkedin.com/in/hazem-ilahi-016a7a315 | github.com/Dyaus2";
const contactFr = "Tunis, Tunisie | +216 97 111 410 | hazem.ilahi@esprit.tn | linkedin.com/in/hazem-ilahi-016a7a315 | github.com/Dyaus2";

const EN = {
  name: "Hazem Ilahi",
  headline: "Data Science & AI Engineering Student — Machine Learning | MLOps | LLM / RAG",
  seeking: "Seeking 6-month end-of-studies internship (PFE), from Jan/Feb 2027 — open to relocation",
  seekingSub: "Mandatory curricular internship — tripartite internship agreement signed by ESPRIT",
  contact,
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
      title: "Garage Augmenté — Multi-agent RAG assistant for automotive pre-diagnosis",
      right: "2026 – 2027",
      sub: "ESPRIT team project — owner of the knowledge base and retrieval layer",
      bullets: [
        "Modular RAG pipeline on Qdrant: multilingual query expansion (French, English, Tunisian Arabic), hybrid dense BGE-M3 + BM25 retrieval fused by reciprocal rank fusion, brand/model/year filtering, cross-encoder reranking and exact lookup of 9,533 OBD fault codes.",
        "7 resumable Python collectors (XML catalogs, JSON APIs, sitemaps, Next.js data routes): 2,019 unique owner's manuals (≈697,000 pages, 26 brands), 73% from official manufacturer sources, covering 54 of 56 priority models chosen from a Tunisian car-market study (2015–2026 registrations).",
        "Corpus preparation: SHA-256 deduplication, Tesseract OCR of ≈18,500 pages, vehicle metadata normalized into 364 model families, topic tagging; main index of 98,000 units (≈39M tokens).",
        "FastAPI service for the n8n workflow, ablation benchmark (hit@k, MRR) and documented hand-off package (Docker Compose, ingestion and evaluation scripts) for the GPU host.",
      ],
      stack: "Stack: Python, Qdrant, BGE-M3, BM25, PyMuPDF, Tesseract, FastAPI, Docker Compose, n8n",
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
      title: "DressMe — Smart personal fashion assistant for the Tunisian market",
      right: "2026 – 2027",
      sub: "ESPRIT team project (Advanced Data Science Project) — design phase, Design Thinking",
      bullets: [
        "User research (17-respondent survey, 6 personas) turned into 5 business and data-science objectives with metrics and a 3-version roadmap; designed a 5-layer architecture (FastAPI gateway, Redis Streams, PostgreSQL/FAISS).",
        "Specified 6 ML pipelines (YOLO + SAM 2 + Qwen3-VL ingestion, BPR outfit compatibility on Polyvore, Two-Tower + LightGBM recommender, ReAct resale agent) and an explainability strategy (TreeSHAP, LIME, counterfactuals).",
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
    ["MLOps", "automated retraining, model registry, champion/challenger deployment, drift monitoring (PSI), quality gates, canary deployment and rollback, pytest"],
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
    "AWS Cloud Foundations — Amazon Web Services (badge, Nov 2026)",
    "Fundamentals of Deep Learning — NVIDIA (2026)",
    "Applications of AI for Anomaly Detection — NVIDIA (2026)",
    "Building Transformer-Based Natural Language Processing Applications — NVIDIA (2026)",
    "CCNA 2: Switching, Routing, and Wireless Essentials (SRWE) — Cisco Networking Academy (2025)",
    "[PLACEHOLDER — 3 Hedera certifications, expected Dec 2026: replace with exact titles once issued, or delete before sending]",
  ],
  languages: "English: fluent | French: advanced (professional working proficiency) | Arabic: native",
};

const FR = {
  name: "Hazem Ilahi",
  headline: "Élève ingénieur en Data Science & IA — Machine Learning | MLOps | LLM / RAG",
  seeking: "Recherche un stage de fin d'études (PFE) de 6 mois à partir de janvier/février 2027 — mobilité internationale",
  seekingSub: "Stage obligatoire du cursus — convention de stage tripartite signée par ESPRIT",
  contact: contactFr,
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
      title: "Garage Augmenté — Assistant multi-agents RAG de pré-diagnostic automobile",
      right: "2026 – 2027",
      sub: "Projet d'équipe, ESPRIT — responsable de la base de connaissances et de la couche de recherche",
      bullets: [
        "Pipeline RAG modulaire sur Qdrant : expansion de requêtes multilingue (français, anglais, arabe tunisien), recherche hybride dense BGE-M3 + BM25 fusionnée par reciprocal rank fusion, filtrage marque/modèle/année, reranking par cross-encoder et consultation exacte de 9 533 codes défaut OBD.",
        "7 collecteurs Python reprenables (catalogues XML, API JSON, sitemaps, routes de données Next.js) : 2 019 manuels du propriétaire uniques (≈ 697 000 pages, 26 marques), 73 % de sources constructeurs officielles, 54 des 56 modèles prioritaires couverts (issus d'une étude du marché automobile tunisien, immatriculations 2015–2026).",
        "Préparation du corpus : déduplication SHA-256, OCR Tesseract de ≈ 18 500 pages, normalisation des métadonnées véhicule en 364 familles de modèles, étiquetage thématique ; index principal de 98 000 unités (≈ 39 M tokens).",
        "Service FastAPI pour le workflow n8n, banc d'ablation (hit@k, MRR) et paquet de transfert documenté (Docker Compose, scripts d'ingestion et d'évaluation) pour la machine GPU hébergeant l'index.",
      ],
      stack: "Stack : Python, Qdrant, BGE-M3, BM25, PyMuPDF, Tesseract, FastAPI, Docker Compose, n8n",
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
      title: "DressMe — Assistant de mode personnel intelligent pour le marché tunisien",
      right: "2026 – 2027",
      sub: "Projet d'équipe (Advanced Data Science Project), ESPRIT — phase de conception, Design Thinking",
      bullets: [
        "Recherche utilisateur (17 répondants, 6 personas) traduite en 5 objectifs métier et data science avec métriques et feuille de route en 3 versions ; architecture en 5 couches (passerelle FastAPI, Redis Streams, PostgreSQL/FAISS).",
        "Spécification de 6 pipelines ML (ingestion YOLO + SAM 2 + Qwen3-VL, compatibilité de tenues BPR sur Polyvore, recommandeur Two-Tower + LightGBM, agent de revente ReAct) et d'une stratégie d'explicabilité (TreeSHAP, LIME, contrefactuels).",
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
    ["MLOps", "réentraînement automatisé, registre de modèles, déploiement champion/challenger, surveillance de la dérive (PSI), critères de qualité, déploiement canari et retour arrière, pytest"],
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
    "AWS Cloud Foundations — Amazon Web Services (badge, novembre 2026)",
    "Fundamentals of Deep Learning — NVIDIA (2026)",
    "Applications of AI for Anomaly Detection — NVIDIA (2026)",
    "Building Transformer-Based Natural Language Processing Applications — NVIDIA (2026)",
    "CCNA 2 : Switching, Routing, and Wireless Essentials (SRWE) — Cisco Networking Academy (2025)",
    "[À COMPLÉTER — 3 certifications Hedera, prévues décembre 2026 : indiquer les intitulés exacts une fois obtenues, sinon supprimer avant envoi]",
  ],
  languages: "Arabe : langue maternelle | Français : courant (niveau avancé, usage professionnel) | Anglais : courant",
};

module.exports = { EN, FR };

# Proposition de PFE B : assistant RAG industrialisé pour la documentation technique, avec évaluation et LLMOps
*Hazem Ilahi, ESPRIT (Data Science & IA). 6 mois, février–juillet 2027.*

**Problème métier.** Ingénieurs et équipes support perdent du temps à chercher dans des milliers de pages de manuels, procédures, rapports d'essais et tickets. Les chatbots génériques hallucinent, ne citent pas leurs sources, et personne ne mesure s'ils retrouvent le bon document.

**Valeur.** Des réponses plus rapides, citant le passage exact ; moins de sollicitations des experts ; un niveau de qualité mesurable (métriques de recherche et de fidélité) imposé à chaque mise en production.

**Données nécessaires.** Corpus documentaire (PDF/Word/HTML ; les scans sont acceptés car l'OCR est dans le périmètre), métadonnées (produit, version, langue, confidentialité), 150 à 300 vraies questions avec le passage correct (construites avec les experts aux mois 1–2), puis les retours utilisateurs du pilote.

**Déjà réalisé (dépôt de démarrage, CPU, données publiques).** Recherche hybride BM25 + dense fusionnée par Reciprocal Rank Fusion, reranking par cross-encoder, banc d'évaluation (hit@k, MRR, latence p95, F1 SQuAD, proxy de groundedness), réponse extractive ou LLM avec filtrage des citations, et service FastAPI. Sur un échantillon SQuAD v2 (621 passages, 600 questions) : BM25 hit@1 0,81, hit@10 0,97. Sur un test CPU de 100 questions, hybride + reranking cross-encoder atteint **hit@1 0,90 / MRR@10 0,92**. Ce travail prolonge mon projet Garage Augmenté : 697 000 pages de manuels, BGE-M3 + BM25, reranking.

## Plan sur 6 mois
| Mois | Jalon | Livrable |
|---|---|---|
| Fév. | Cas d'usage, inventaire du corpus, règles d'accès et de confidentialité, protocole des questions de référence | Note de cadrage, 100 premières Q/R de référence |
| Mars | Ingestion : parsing, OCR, découpage, métadonnées ; index hybride | Pipeline d'ingestion reproductible, index v1, banc v1 |
| Avr. | Réglage de la recherche (taille des chunks, poids hybrides, reranker, expansion de requêtes), FR/EN | Rapport d'ablation |
| Mai | Génération : prompt à citations obligatoires, refus en cas de doute, fidélité par LLM-juge | Banc qualité des réponses, garde-fous |
| Juin | LLMOps : API, collecte des retours, portes de qualité au déploiement, suivi du coût et de la latence | Pilote avec 10 à 20 utilisateurs |
| Juil. | Analyse du pilote, documentation, transfert, soutenance | Rapport final, runbook |

**Architecture.** Sources → parsing/OCR → découpage + métadonnées → index BM25 + base vectorielle (Qdrant) → recherche hybride + reranker → LLM (validé par l'entreprise : modèle open source sur site ou API entreprise) avec citations → FastAPI → interface ou Teams. Un banc d'évaluation hors ligne conditionne chaque changement ; la journalisation en ligne couvre latence, retours et dérive des requêtes.

**Stack.** Python, Qdrant/FAISS, BGE-M3 (ou embedder interne), BM25, cross-encoders, PyMuPDF et Tesseract, FastAPI, Docker, MLflow ou traçage type Langfuse, pytest.

**KPI.** hit@5 ≥ objectif convenu sur le jeu de référence ; MRR ; fidélité (part des réponses entièrement justifiées par les passages cités) ; précision des « je ne sais pas » ; latence p95 ; coût par requête ; taux de satisfaction utilisateur.

**Risques et parades.** Données confidentielles : modèles sur site, index à accès contrôlé, aucune donnée ne sort. Hallucinations : citations obligatoires, politique de refus, porte de fidélité. Scans ou tableaux de mauvaise qualité : contrôle qualité OCR, parsing adapté aux tableaux. Absence de jeu de référence : le construire tôt avec les experts, car c'est le cœur de l'évaluation.

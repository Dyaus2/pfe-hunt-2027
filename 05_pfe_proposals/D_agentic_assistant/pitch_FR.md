# Proposition de PFE D : assistant IA agentique pour les opérations industrielles, avec garde-fous et harnais d'évaluation
*Hazem Ilahi, ESPRIT (Data Science & IA). 6 mois, février–juillet 2027.*

**Pourquoi ce sujet (demande observée en phase 3).** Plusieurs offres de stage 2027 actuellement ouvertes demandent des workflows agentiques et LLM en contexte industriel : Sanofi (architectures multi-agents, du prototype à la production, en fabrication et supply chain), Bosch (harnais d'IA agentique et workflows GenAI), Safran Helicopter Engines (chatbot avec LLM et agentique pour applications industrielles) et un client du secteur de l'énergie via Askills (agents avec cadre d'évaluation).

**Problème métier.** Opérateurs et ingénieurs répètent des tâches en plusieurs étapes, réparties sur plusieurs systèmes : lire un code défaut, vérifier la procédure, calculer une limite, ouvrir un ordre de travail. Les agents LLM peuvent les automatiser, mais sans garde-fous ni mesure ils sont risqués (mauvaises actions, faits inventés, effets de bord non contrôlés).

**Valeur.** Délai réduit entre l'alarme et la bonne action, procédures homogènes, et des effets de bord (tickets, commandes) toujours soumis à validation humaine et journalisés. Un gabarit d'agent réutilisable et un harnais d'évaluation extensible par l'entreprise.

**Données et accès nécessaires.** Documents de procédures (ou l'index RAG de la proposition B), tables des codes défaut et des équipements, une API bac à sable du système de tickets ou de GMAO, plus de 100 demandes réelles avec résultats attendus (construites avec les opérateurs) et le LLM validé (sur site ou API entreprise).

**Déjà réalisé (dépôt de démarrage, CPU, données d'usine synthétiques).** Quatre outils (recherche dans les procédures, consultation des codes défaut, calculatrice sécurisée, création d'ordres de travail). Garde-fous : liste blanche, validation des arguments, budget d'étapes, validation humaine obligatoire pour les effets de bord, erreurs d'outils renvoyées comme observations. Un planificateur à règles sur CPU (classifieur d'intention + règles d'extraction) et un planificateur LLM de type ReAct compatible avec tout modèle. Un harnais de 12 scénarios. La baseline à règles obtient **12/12**. Un modèle ouvert de 0,5 B exécuté sur CPU en test rapide obtient **0/3** (il boucle jusqu'à épuisement du budget d'étapes), ce qui montre précisément l'utilité du harnais et des garde-fous.

## Plan sur 6 mois
| Mois | Jalon | Livrable |
|---|---|---|
| Fév. | Choix de 2–3 workflows cibles avec les opérateurs ; analyse de risque de chaque outil | Note de cadrage, 50 scénarios |
| Mars | Couche d'outils sur API bac à sable (lecture seule d'abord), outil de recherche (RAG) | SDK d'outils, tests unitaires |
| Avr. | Planificateurs : baseline à règles vs LLM (ouvert et hébergé), schémas d'outils, sorties structurées | Résultats du harnais v1 |
| Mai | Garde-fous : interface de validation, contrôles de politique, journal d'audit, scénarios d'attaque | Rapport de sûreté |
| Juin | Pilote avec un petit groupe d'opérateurs, optimisation latence et coût, supervision | Métriques du pilote |
| Juil. | Évaluation, documentation, transfert, soutenance | Rapport final, runbook |

**Architecture.** Utilisateur → boucle agent (planificateur ↔ outils) → couche de garde-fous (liste blanche, validation de schéma, approbations, budget) → outils (recherche RAG, base des défauts, GMAO bac à sable, calculatrice) → journal d'audit et harnais d'évaluation (scénarios hors ligne + traces en ligne).

**Stack.** Python, scikit-learn, LLM ouverts via Hugging Face transformers (classe Qwen/Llama sur GPU) ou LLM entreprise, FastAPI, Qdrant (RAG), pytest, Docker, traçage (type OpenTelemetry/Langfuse).

**KPI.** Taux de réussite sur la suite de scénarios ; précision des appels d'outils ; violations de garde-fous (objectif : 0 effet de bord non approuvé) ; étapes et latence par tâche ; coût par tâche ; satisfaction des opérateurs.

**Risques et parades.** Mauvaises actions : lecture seule d'abord, validation de chaque écriture, bac à sable uniquement. Faits inventés : réponses issues des sorties d'outils, avec citation des sources. Dépendance à un modèle ou fournisseur : interface de planification agnostique, le harnais compare les modèles. Petits modèles insuffisants : repli sur règles ou RAG, seules les intentions bien maîtrisées vont au LLM.

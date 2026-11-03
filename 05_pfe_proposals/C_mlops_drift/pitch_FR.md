# Proposition de PFE C : plateforme MLOps de surveillance de la dérive et de réentraînement champion/challenger sécurisé
*Hazem Ilahi, ESPRIT (Data Science & IA). 6 mois, février–juillet 2027.*

**Problème métier.** Les modèles en production se dégradent silencieusement quand les données ou les comportements changent (nouveaux produits, saisons, capteurs, marchés). Les équipes ne réentraînent jamais (la performance décline) ou réentraînent à l'aveugle (les régressions arrivent en production). Il n'existe pas de méthode commune pour détecter la dérive, tester un nouveau modèle sans risque et revenir en arrière.

**Valeur.** Moins de défaillances silencieuses, des mises en production plus rapides et plus sûres, et un historique auditable des modèles (qui a promu quoi, quand et pourquoi). Un gabarit réutilisable par toutes les équipes data de l'entreprise.

**Données nécessaires.** Un ou deux modèles en production avec leurs journaux d'entrées et leurs résultats ou labels (éventuellement différés), le processus de déploiement actuel et l'indicateur métier piloté par chaque modèle.

**Déjà réalisé (dépôt de démarrage, CPU, données publiques).** Dérive PSI par variable, portes de qualité (AUC, calibration ECE, non-régression face au champion), registre de modèles avec promotion et retour arrière, et simulateur préquentiel comparant modèle statique, réentraînement périodique et champion/challenger déclenché par la dérive (essai en shadow + retour arrière automatique). Sur le flux réel **Elec2** (marché de l'électricité, 134 semaines) : AUC moyenne **0,764 statique → 0,839 périodique → 0,845 champion/challenger** (20 promotions, 5 retours arrière automatiques). Le simulateur met aussi en évidence un vrai problème : le PSI sur variables brutes signale une dérive sur les 126 semaines surveillées au seuil usuel de 0,2 (fatigue d’alertes), ce qui constitue une question de recherche pour le PFE. Cela prolonge la chaîne de réentraînement hebdomadaire que j'ai construite pour ATOR DFIR (14 critères, essai silencieux de 7 jours, canari, retour arrière, PSI).

## Plan sur 6 mois
| Mois | Jalon | Livrable |
|---|---|---|
| Fév. | Audit de 1–2 modèles en production, métriques, délai des labels ; architecture cible | Analyse d'écarts, document de conception |
| Mars | Surveillance : dérive des entrées et des scores, qualité des données, performance avec labels différés | Jobs de surveillance + tableau de bord |
| Avr. | Registre (MLflow), portes de qualité, tests CI des modèles (données, entraînement, parité entraînement/production) | Pipeline d'entraînement conditionné |
| Mai | Champion/challenger : déploiement shadow, règles de promotion, retour arrière automatique | Workflow de mise en production sur le modèle n° 1 |
| Juin | Réglage des alertes (dérive actionnable), estimation de performance sans labels, extension au modèle n° 2 | Runbook, politique d'alerte |
| Juil. | Mesure de l'impact, documentation, transfert, soutenance | Rapport final |

**Architecture.** Journaux de variables et d'inférence → jobs de surveillance (dérive, qualité des données, performance) → alertes → pipeline de réentraînement (Airflow/Prefect ou CI) → portes de qualité → registre (MLflow) → déploiement shadow/canari → promotion ou retour arrière, avec piste d'audit.

**Stack.** Python, scikit-learn, MLflow, rapports de dérive type Evidently ou PSI/KS maison, Docker, FastAPI, GitHub Actions ou GitLab CI, Airflow ou Prefect, pytest, Grafana ou Power BI.

**KPI.** Délai de détection d'une dégradation ; part des versions passant les portes ; régressions arrivées en production (objectif 0) ; délai de retour arrière ; précision des alertes (part des alertes de dérive ayant nécessité une action) ; indicateur métier avant/après.

**Risques et parades.** Labels différés : indicateurs de dérive des scores et estimation sans labels, validation a posteriori. Fatigue d'alertes : références saisonnières, règles multi-signaux, seuils réglés sur l'historique. Adoption : commencer par un modèle, utiliser le gabarit, démontrer le retour arrière en direct.

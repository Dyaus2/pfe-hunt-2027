# Proposition de PFE A : maintenance prédictive et détection d'anomalies sur données capteurs
*Hazem Ilahi, ESPRIT (Data Science & IA). 6 mois, février–juillet 2027.*

**Problème métier.** Les pannes non planifiées (moteurs, pompes, compresseurs, bancs d'essai) entraînent arrêts de production, risques sécurité et réparations d'urgence coûteuses. La maintenance à intervalle fixe remplace les pièces trop tôt ou trop tard. L'équipe a besoin (1) d'une **alerte de santé** précoce et fiable et (2) d'une estimation de la **durée de vie résiduelle (RUL)** pour planifier les interventions.

**Valeur.** Moins d'arrêts non planifiés, une maintenance déclenchée sur l'état réel et des pièces commandées à temps. Les KPI ci-dessous sont validés avec l'entreprise dès le premier mois.

**Données nécessaires.** Signaux capteurs horodatés par équipement (vibrations, températures, pressions, courants, conditions opératoires), historiques de maintenance et de pannes (dates, modes de défaillance) et, idéalement, quelques historiques jusqu'à la panne. Le prototypage démarre sur le benchmark public **NASA C-MAPSS** en attendant l'accès aux données internes.

**Déjà réalisé (dépôt de démarrage, CPU, données publiques).** Variables glissantes causales partagées entre entraînement et production ; modèle RUL par gradient boosting avec validation croisée groupée par moteur ; moniteur de santé Isolation Forest avec alarme après k cycles consécutifs ; score asymétrique PHM08. Sur C-MAPSS FD001 : **RMSE test de 15,3 cycles**, RMSE en validation croisée de 18,7 ± 0,7, alarmes levées sur 100 % des moteurs d'entraînement avec une avance médiane de 41 cycles. Ce sont des diagnostics d'alarme en échantillon, à re-mesurer sur des unités tenues à l'écart.

## Plan sur 6 mois
| Mois | Jalon | Livrable |
|---|---|---|
| Fév. | Audit des données, typologie des pannes, KPI et modèle de coût validés | Rapport qualité des données, baseline sur données internes |
| Mars | Pipeline de variables (code unique), étiquetage des fenêtres de panne | Feature store versionné, tests anti-fuite |
| Avr. | Modèles : RUL (GBM vs LSTM/CNN 1D [GPU]), anomalies (IF vs autoencodeur), calibration | Rapport comparatif, validation croisée groupée |
| Mai | Politique d'alarme réglée sur le coût métier, explicabilité (SHAP par alarme) | Note de politique d'alarme, tableaux de bord |
| Juin | Industrialisation : service FastAPI, surveillance de la dérive, réentraînement planifié | Pilote déployé sur une ligne / famille d'équipements |
| Juil. | Évaluation du pilote, documentation, transfert, soutenance | Rapport final, runbook |

**Architecture.** Historien capteurs / CSV → ingestion et validation → pipeline de variables (partagé entraînement/production) → modèles (RUL + score de santé) → politique d'alarme → API et tableau de bord. Autour : surveillance (dérive PSI, taux d'alarmes) et réentraînement planifié (voir proposition C).

**Stack.** Python, pandas, scikit-learn, PyTorch (modèles séquentiels, GPU Colab ou interne), SHAP, FastAPI, Docker, MLflow, pytest.

**KPI.** RMSE RUL et score PHM08 sur équipements tenus à l'écart ; taux de détection des pannes à taux de fausses alarmes fixé ; avance médiane ; alarmes par équipement et par mois ; part d'alarmes confirmées par les techniciens.

**Risques et parades.** Peu de pannes étiquetées : score de santé non supervisé et variables de dégradation guidées par la physique, validation avec les experts. Accès ou confidentialité des données : démarrage sur C-MAPSS, NDA signé tôt, travail sur site. Changements de régime opératoire : normalisation par condition opératoire et surveillance de la dérive. Fatigue d'alarmes : réglage sur une matrice de coûts, règles de persistance k parmi n.

# TurboWatch — lines to paste into the CV (numbers verified in github.com/Dyaus2/turbowatch/results)

## EN (Projects section, first entry)
**TurboWatch — Predictive maintenance copilot (personal project, 2026)** · live demo: dyaus2.github.io/turbowatch · code: github.com/Dyaus2/turbowatch
- Fleet-health system on NASA C-MAPSS turbofan data: RUL models (gradient boosting with P10–P90 band, 1D-CNN in PyTorch) on causal, regime-normalised features; held-out RUL RMSE 15.5 cycles (CNN) / 16.3 (GBM) on the official FD001 test set (5 seeds).
- Cost-tuned k-of-n alarm policy: 97% of failures detected a median 36 cycles ahead at a 2% false-alarm rate (test set); SHAP explanations per prediction.
- RAG maintenance copilot over FAA/NASA documents (bge-small + BM25, RRF, cross-encoder rerank): cited answers, refusal when out of scope, hit@1 100% on 26 document questions.
- MLOps & delivery: MLflow, PSI drift + champion/challenger retraining (FD003 test RMSE 20.7 → 15.0), FastAPI + React/TypeScript dashboard with live replay, Docker, pytest + GitHub Actions CI.
Stack: Python, scikit-learn, PyTorch, SHAP, MLflow, FastAPI, sentence-transformers, React, TypeScript, Docker

## FR (section Projets, en premier)
**TurboWatch — Copilote de maintenance prédictive (projet personnel, 2026)** · démo : dyaus2.github.io/turbowatch · code : github.com/Dyaus2/turbowatch
- Système de santé de flotte sur les données turboréacteurs NASA C-MAPSS : modèles RUL (gradient boosting avec bande P10–P90, CNN 1D PyTorch) sur variables causales normalisées par régime ; RMSE RUL de 15,5 cycles (CNN) / 16,3 (GBM) sur le jeu de test officiel FD001 (5 graines).
- Politique d'alarme k parmi n réglée sur une matrice de coûts : 97 % des pannes détectées avec une avance médiane de 36 cycles, à 2 % de fausses alarmes (jeu de test) ; explications SHAP par prédiction.
- Copilote RAG de maintenance sur documents FAA/NASA (bge-small + BM25, RRF, reranking cross-encoder) : réponses citées, refus hors périmètre, hit@1 de 100 % sur 26 questions.
- MLOps et livraison : MLflow, dérive PSI + réentraînement champion/challenger (RMSE test FD003 20,7 → 15,0), API FastAPI + tableau de bord React/TypeScript avec rejeu en direct, Docker, CI pytest + GitHub Actions.
Stack : Python, scikit-learn, PyTorch, SHAP, MLflow, FastAPI, sentence-transformers, React, TypeScript, Docker

Live demo verified on 2026-11-04: https://dyaus2.github.io/turbowatch/ (static build; the copilot runs in the browser).

# PFE proposal C: MLOps platform for drift monitoring and safe champion/challenger retraining
*Hazem Ilahi, ESPRIT (Data Science & AI). 6 months, Feb–Jul 2027.*

**Business problem.** Models in production degrade silently when data or behaviour changes (new products, seasons, sensors, markets). Teams either never retrain (performance decays) or retrain blindly (regressions reach production). There is no common way to detect drift, test a new model safely, and roll back.

**Value.** Fewer silent model failures, faster and safer releases, and an auditable model history (who promoted what, when, and why). One reusable template that every data science team at the host can apply to its models.

**Data needed.** One or two existing production models with their input logs and (possibly delayed) outcomes or labels, the current deployment process, and the business metric each model drives.

**Already built (starter repo, CPU, public data).** PSI drift per feature, quality gates (AUC, calibration ECE, no-regression vs champion), a file-based model registry with promotion and rollback, and a prequential simulator comparing static, periodic and drift-triggered champion/challenger (shadow trial + automatic rollback). On the real **Elec2** electricity-market stream (134 weekly batches): mean AUC **0.764 static → 0.839 periodic → 0.845 champion/challenger** (20 promotions, 5 automatic rollbacks). It also shows a real problem: raw-feature PSI flags drift in all 126 monitored weeks at the usual 0.2 threshold (alert fatigue), which is a research question for the PFE. This mirrors the weekly retraining chain I built for ATOR DFIR (14 gates, 7-day silent trial, canary, rollback, PSI).

## 6-month plan
| Month | Milestone | Deliverable |
|---|---|---|
| Feb | Audit of 1–2 production models, metrics, label delay; target architecture | Gap analysis, design doc |
| Mar | Monitoring: input/score drift, data-quality checks, performance with delayed labels | Monitoring jobs + dashboard |
| Apr | Registry (MLflow), quality gates, CI tests for models (data, training, serving parity) | Gated training pipeline |
| May | Champion/challenger: shadow deployment, promotion rules, automatic rollback | Release workflow on model #1 |
| Jun | Alert tuning (actionable drift), label-free performance estimation, generalise to model #2 | Runbook, alert policy |
| Jul | Measure impact, documentation, hand-over, defence | Final report |

**Architecture.** Feature/inference logs → monitoring jobs (drift, data quality, performance) → alerting → retraining pipeline (Airflow/Prefect or CI) → quality gates → registry (MLflow) → shadow/canary deployment → promotion or rollback, with an audit trail.

**Stack.** Python, scikit-learn, MLflow, Evidently-style drift reports or custom PSI/KS, Docker, FastAPI, GitHub Actions or GitLab CI, Airflow or Prefect, pytest, Grafana or Power BI.

**KPIs.** Time to detect a degradation; share of releases passing gates; number of regressions reaching production (target 0); time to roll back; alert precision (share of drift alerts that needed action); business metric before vs after.

**Risks and mitigations.** Delayed labels: use score-drift proxies and label-free estimation, and validate later. Alert fatigue: seasonal references, multi-signal rules, thresholds tuned on history. Organisational adoption: start with one model, use the template, demo the rollback live.

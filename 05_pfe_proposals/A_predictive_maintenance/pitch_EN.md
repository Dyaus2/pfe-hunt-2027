# PFE proposal A: Predictive maintenance and anomaly detection on equipment sensor data
*Hazem Ilahi, ESPRIT (Data Science & AI). 6 months, Feb–Jul 2027.*

**Business problem.** Unplanned equipment failures (engines, pumps, compressors, test benches) cause downtime, safety risk and expensive emergency repairs. Fixed-interval maintenance replaces parts too early or too late. The team needs (1) an early, trustworthy **health alarm** and (2) a **remaining-useful-life (RUL)** estimate to plan interventions.

**Value.** Fewer unplanned stops, maintenance scheduled on real condition, and spare parts ordered in time. The KPIs below are agreed with the host in month 1.

**Data needed.** Time-stamped sensor channels per asset (vibration, temperatures, pressures, currents, operating settings), maintenance and failure logs (dates, failure modes), and ideally a few run-to-failure histories. Prototyping starts on the public **NASA C-MAPSS** turbofan benchmark while access to host data is arranged.

**Already built (starter repo, CPU, public data).** Causal rolling features shared by training and serving; gradient-boosting RUL model with engine-grouped cross-validation; Isolation-Forest health monitor with k-consecutive-cycle alarms; PHM08 asymmetric score. On C-MAPSS FD001: **test RMSE 15.3 cycles**, CV RMSE 18.7 ± 0.7, alarms raised on 100% of training engines with a median lead time of 41 cycles. These are in-sample alarm diagnostics, to be re-measured on held-out units.

## 6-month plan
| Month | Milestone | Deliverable |
|---|---|---|
| Feb | Data audit, failure-mode taxonomy, KPI and cost model agreed | Data-quality report, baseline on host data |
| Mar | Feature pipeline (one code path), labelling of failure windows | Versioned feature store, leakage tests |
| Apr | Models: RUL (GBM vs LSTM/1D-CNN [GPU]), anomaly detection (IF vs autoencoder), calibration | Benchmark report with grouped CV |
| May | Alarm policy tuned on business cost (missed failure vs false alarm), explainability (SHAP per alarm) | Alarm-policy note, dashboards |
| Jun | Industrialisation: FastAPI scoring service, drift monitoring, retraining job | Deployed pilot on 1 line/asset family |
| Jul | Pilot evaluation, documentation, hand-over, defence | Final report, runbook |

**Architecture.** Sensor historian/CSV → ingestion and validation → feature pipeline (shared train/serve) → models (RUL + health score) → alarm policy → API and dashboard. Monitoring (PSI drift, alarm rate) and scheduled retraining sit around it (see proposal C).

**Stack.** Python, pandas, scikit-learn, PyTorch (sequence models, Colab or host GPU), SHAP, FastAPI, Docker, MLflow, pytest.

**KPIs.** RUL RMSE and PHM08 score on held-out assets; failure detection rate at a fixed false-alarm rate; median lead time; alarms per asset per month; share of alarms confirmed by technicians.

**Risks and mitigations.** Few labelled failures: use unsupervised health scoring plus physics-informed degradation features, and validate with experts. Data access or confidentiality: start on C-MAPSS, sign NDA early, work on-prem. Operating-regime shifts: normalise per operating condition and monitor drift. Alarm fatigue: tune on a cost matrix, use k-of-n persistence rules.

# State of practice: predictive maintenance and time-series anomaly detection
All references were verified on 2026-11-03 via Crossref (DOI) or the arXiv API.

| # | Reference | Why it matters here |
|---|---|---|
| 1 | Saxena, Goebel, Simon, Eklund (2008). *Damage propagation modeling for aircraft engine run-to-failure simulation*. PHM 2008. [doi:10.1109/PHM.2008.4711414](https://doi.org/10.1109/PHM.2008.4711414) | Origin of C-MAPSS and of the asymmetric PHM08 score used in `evaluate.py`. |
| 2 | Liu, Ting, Zhou (2008). *Isolation Forest*. ICDM 2008. [doi:10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17) | Unsupervised health-score baseline: cheap, robust, no failure labels needed. |
| 3 | Malhotra et al. (2016). *LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection*. [arXiv:1607.00148](https://arxiv.org/abs/1607.00148) | Reconstruction-error health index for multivariate sensors (GPU upgrade path). |
| 4 | Zheng, Ristovski, Farahat, Gupta (2017). *Long Short-Term Memory Network for Remaining Useful Life estimation*. ICPHM. [doi:10.1109/ICPHM.2017.7998311](https://doi.org/10.1109/ICPHM.2017.7998311) | LSTM RUL on C-MAPSS; template for the [GPU] cell. |
| 5 | Li, Ding, Sun (2018). *Remaining useful life estimation in prognostics using deep convolution neural networks*. Reliability Engineering & System Safety. [doi:10.1016/j.ress.2017.11.021](https://doi.org/10.1016/j.ress.2017.11.021) | 1D-CNN RUL with a piecewise-linear (capped) RUL target, the same target shape used here. |
| 6 | Schmidl, Wenig, Papenbrock (2022). *Anomaly detection in time series: a comprehensive evaluation*. PVLDB 15(9). [doi:10.14778/3538598.3538602](https://doi.org/10.14778/3538598.3538602) | Large-scale benchmark of dozens of detectors: no single method wins everywhere, so start with simple, well-validated baselines. |

**Takeaways for the PFE.**
1. Use a capped RUL target and engine-grouped validation; otherwise leakage inflates scores (see the CV fix in the starter repo).
2. Start with GBM + Isolation Forest, and move to sequence models only if they beat the baseline on held-out assets.
3. Evaluate alarms on business cost and lead time, not only on RMSE.

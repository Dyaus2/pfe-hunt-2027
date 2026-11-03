# State of practice: MLOps, drift detection and safe model updates
All references were verified on 2026-11-03 via Crossref (DOI), the arXiv API, or the publisher page.

| # | Reference | Why it matters here |
|---|---|---|
| 1 | Sculley et al. (2015). *Hidden Technical Debt in Machine Learning Systems*. NeurIPS 2015. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) | Why ML systems decay: entanglement, feedback loops and pipeline debt. The motivation for monitoring and gates. |
| 2 | Breck, Cai, Nielsen, Salib, Sculley (2017). *The ML Test Score: A rubric for ML production readiness and technical debt reduction*. IEEE Big Data. [doi:10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038) | Concrete test checklist (data, model, infrastructure, monitoring), used for the quality gates. |
| 3 | Gama, Žliobaitė, Bifet, Pechenizkiy, Bouchachia (2014). *A survey on concept drift adaptation*. ACM Computing Surveys. [doi:10.1145/2523813](https://doi.org/10.1145/2523813) | Taxonomy of drift and of adaptation strategies (triggered vs periodic retraining, windowing). |
| 4 | Rabanser, Günnemann, Lipton (2019). *Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift*. [arXiv:1810.11953](https://arxiv.org/abs/1810.11953) | Compares shift detectors; supports monitoring model outputs rather than only raw features (our alert-fatigue finding). |
| 5 | Kreuzberger, Kühl, Hirschl (2023). *Machine Learning Operations (MLOps): Overview, Definition, and Architecture*. [arXiv:2205.02302](https://arxiv.org/abs/2205.02302) | Reference architecture and roles: registry, CI/CD/CT, monitoring. |
| 6 | Shankar, Garcia, Hellerstein, Parameswaran (2022). *Operationalizing Machine Learning: An Interview Study*. [arXiv:2209.09125](https://arxiv.org/abs/2209.09125) | Practitioner evidence: staged rollouts, alert fatigue and on-call pain, which this PFE addresses. |
| 7 | Elec2 electricity dataset, OpenML data_id 151. [openml.org/d/151](https://www.openml.org/d/151) | Classic real-world drifting stream used in the simulator. |

**Takeaways for the PFE.** Monitor score and performance, not only inputs. Make retraining conditional on gates, and make promotion conditional on a shadow comparison. Rollback must be automatic and rehearsed.

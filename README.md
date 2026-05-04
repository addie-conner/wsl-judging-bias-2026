# WSL Judging Bias — Research Series (Conner 2026)

Public replication archive for a three-paper research series on bias in World Surf League judging, 2009–2026.

**Author:** Addie Conner (independent; Chorus Research)
**ORCID:** [0009-0007-7853-4140](https://orcid.org/0009-0007-7853-4140)
**Contact:** addieconner@gmail.com
**License:** CC-BY-4.0

---

## What's here

This repository contains the largest publicly-available WSL judging dataset assembled (60,834 panel-trim-mean wave scores; 301,478 individual judge-scoring decisions; 86.3% with judge-nationality coverage; 2009–2026, men's and women's CT), plus the full analysis pipeline and three companion manuscripts.

### Three manuscripts

- **`manuscript/paper1_empirical.md`** — *Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging.* The empirical flagship.
- **`manuscript/paper2_methodology.md`** — *Eighteen Gates and the Causality Ladder.* Methodology framework for bias identification in subjective-sport judging.
- **`manuscript/paper3_reform.md`** — *Reforming Olympic Surfing Judging Before LA 2028.* Four-part reform agenda + SHA-locked prospective forecast for the 2028 LA Olympic surfing event.

`manuscript/submission/` contains submission-ready DOCX versions, the cover letter for *Journal of Quantitative Analysis in Sports*, the APA-7 reference list, the BibTeX file, and the data-availability statement.

### Pre-registration and held-out validation

- **`outputs/preregistration_2026-05-03.md`** — pre-registered hypotheses, statistical specifications, and falsifiable effect-size predictions, sealed before any of the analyses reported in Paper 1 were run.
- **`data/HOLDOUT_MANIFEST.json`** — sealed 2025 women's Championship Tour replication set (n = 1,815 wave-rows; sha256 `c7130018b373836efd3b8542e9380a22`).

### Data

- **`data/heats.parquet`** — 24,901 panel-trim-mean wave-rows (2022–2025 men's and women's CT).
- **`data/judges.parquet`** — 60,834 wave-rows containing 301,478 individual judge-scoring decisions, with judge nationality on 86.3% of judge-score values, spanning 2009–2026.
- **`data/heats_holdout.parquet`** — 1,815 sealed 2025 women's CT wave-rows for held-out replication.
- **`data/heats_training.parquet`** — 23,086 training-period wave-rows.
- **`data/wavepool_*`** — 28 panel-trim-mean wave-rows from the 2025 Surf Abu Dhabi Pro (sole wavepool event in the active dataset).
- **`data/surfer_wikipedia.parquet`** — sponsor and biographical data parsed from public Wikipedia pages (used in Paper 1's sponsor-alignment subsection).

### Predictions

- **`outputs/olympic_2028_la_predictions.md`** / `.json` — 49 SHA-locked prospective predictions for the 2026 WSL Championship Tour and the 2028 LA Olympic surfing event, registered at git commit `1ee95a5e4ccb` against heats SHA `7f07fb121abe`. Predictions resolve at the events themselves; results will be appended.

### Analysis results (SHA-traceable JSONs)

`outputs/` contains 12 SHA-traceable JSON files covering every test in the 18-gate validation harness:

- `tier1_results.json` — Bayesian hierarchical posterior, sensitivity bounds (E-value, Rosenbaum Γ), FDR (BH and Bonferroni), synthetic control on BRA panel-composition reform, Causal Forest CATE by rank-quartile, XGBoost+SHAP, H32 permutation test.
- `tier2_results.json` — Stochastic Block Model (Louvain), distance correlation + mutual information, NMF on the Nielsen-style 5×5 contribution matrix, TMLE (LinearDRLearner), wild cluster bootstrap, DFBETAS leave-one-event-out leverage.
- `tier3_results.json` — Bayesian Model Averaging across spec battery, split conformal prediction, negative-control outcome tests, stability selection (Lasso bootstrap).
- `tier4_results.json` — copula tail dependence, GEV/POT extreme-value, transfer entropy between mechanisms, VAR + Granger causality, e-values, permutation feature importance, PC algorithm DAG discovery.
- `tier5_results.json` — mixture-Bayesian (atoms + Gaussian) for H11 PPC, AUS-bloc permutation test, hold-out validation on sealed 2025 women's CT, Callaway–Sant'Anna staggered-DiD on BRA panel reform.
- `per_judge_counterfactual_2026-05-04.json` — per-judge difference-in-differences identification: AUS bloc, BRA bloc post-reform, named-individual cases (Jack Robinson and Ethan Ewing at Margaret River).
- `comprehensive_stats_2026-05-04.json` — median polish, RF + Shapley R², singles/doubles/triples/quads, ANOVA decomposition, MANOVA, PCA + factor analysis + CCA, robust regression, Nielsen contribution matrix.
- `full_paper_grade_results.json` — full primary tests on the 60,834-row corpus, DML with tight hyperparameters, multilevel mixed-effects.
- `full_data_rerun_results.json` — re-run heterogeneity + H32 + cross-correlation on the updated corpus.
- `patch_yellow_flags_results.json` — corrected Cameron-Gelbach-Miller wild cluster bootstrap, fixed VAR.
- `sponsor_alignment_analysis.json` — does sponsor-aligned surfer score higher at brand-sponsored events? Within-heat and within-surfer tests.
- `olympic_2024_bias_replication.json` / `.md` — cross-Olympic-pool replication on Paris 2024 Teahupo'o.

### Scripts

`scripts/` contains the Python analysis scripts, organised by tier. Reproducible against the data files in `data/`. Required: `pandas`, `statsmodels`, `econml`, `pymc`, `arviz`, `scikit-learn`, `scipy`, `networkx`, `xgboost`, `shap`. The scripts produce the JSON output files in `outputs/`.

### Substack companion series

`substack/` contains the six-piece public-facing companion essay series, written for general readers without a statistics background. Same findings as the manuscripts. Final published versions live on the author's Substack.

---

## Reproducing the analyses

```bash
# Clone
git clone https://github.com/addie-conner/wsl-judging-bias-2026.git
cd wsl-judging-bias-2026

# Install dependencies
pip install pandas statsmodels econml pymc arviz scikit-learn scipy networkx xgboost shap

# Run any tier
python scripts/tier1_2026-05-04.py
python scripts/tier2_2026-05-04.py
# ... etc
```

Each script writes its results to a JSON file in `outputs/`. The scripts are deterministic given the data files and the seeds set inside them.

---

## Citing this work

Until the SportRxiv / MetaArXiv preprint DOIs are assigned, cite as:

> Conner, A. (2026). *Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging.* Replication archive: https://github.com/addie-conner/wsl-judging-bias-2026

Once the preprints are live, cite the preprint DOIs in the [preprint registration] section below.

---

## Preprint registration

- **Paper 1 (empirical):** [DOI to be added once MetaArXiv preprint is live]
- **Paper 2 (methodology):** [DOI to be added]
- **Paper 3 (reform):** [DOI to be added]

OSF project page: https://osf.io/59szg/

---

## License

Creative Commons Attribution 4.0 International (CC-BY-4.0). You are free to share and adapt the material, including for commercial use, with attribution.

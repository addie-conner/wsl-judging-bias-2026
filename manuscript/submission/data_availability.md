## Data Availability Statement

All data and code supporting the findings in this manuscript are publicly available at the project replication archive: **https://github.com/addie-conner/chorus/tree/main/wsl/** (replace with final canonical URL once the repository is made public).

The archive contains:

- `data/heats.parquet` — 24,901 panel-trim-mean wave-rows used as the aggregate dataset.
- `data/judges.parquet` — 60,834 wave-rows containing 301,478 individual judge-scoring decisions, with judge nationality on 86.3% of judge-score values.
- `data/HOLDOUT_MANIFEST.json` — sealed 2025 women's Championship Tour replication set (n = 1,815 wave-rows; sha256 `c7130018b373836efd3b8542e9380a22`; locked 2026-05-03 UTC).
- `outputs/preregistration_2026-05-03.md` — pre-registered hypotheses and specifications, sealed at git SHA `7d0e2c8` on 2026-05-03 UTC.
- `outputs/olympic_2028_la_predictions.md` and `olympic_2028_la_predictions_locked.json` — 49 SHA-locked prospective predictions for the 2026 WSL Championship Tour and 2028 LA Olympic surfing event, registered at git SHA `1ee95a5e4ccb`.
- `scripts/` — Python analysis scripts (Tier 1–5 + comprehensive battery + per-judge counterfactual + sponsor-alignment), reproducible against the data files.
- `outputs/*.json` — SHA-traceable analysis result files for each test in the 18-gate validation harness.

Per-judge scoring data was assembled from publicly accessible sources: the WSL XHR endpoint `/wave-judges-scores?waveId=<id>` (no authentication required), the pre-2022 WSL events directory pattern `/events/{year}/{mct,wct}/{event_id}/{slug}/results` recovered from Common Crawl WARC archives (CC-MAIN-2018-43 and adjacent crawls), and Wayback Machine snapshots of WSL competition pages. No proprietary or authenticated WSL data was used.

The repository is committed at the SHA referenced in the pre-registration. Subsequent commits add analyses but do not modify the pre-registered specifications or the hold-out manifest.

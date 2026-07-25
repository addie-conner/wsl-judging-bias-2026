#!/usr/bin/env python3
"""
Panel-composition descriptive analysis (Paper 1, Table 1).

Computes, per year (2018+), the mean number of Brazilian-passport judges seated
(a) on panels scoring a Brazilian surfer, and (b) on ALL panels (any mapped
surfer nationality). The two series are reported side by side so that a reader
can see whether a decline on Brazilian-surfer panels is specific to Brazilian
surfers (an assignment-policy signal) or is a whole-roster phenomenon (a
judge-supply signal). They are not separable from these data alone; see the
paper's Descriptive section.

Coverage caveats (encoded in the output JSON):
  * judge_*_nationality is populated only for 2018+ rows (0% for 2009-2017).
  * surfer_country is populated only for pre-2018 rows in judges.parquet; for
    2018+ it must be imputed from a surfer-name -> country map built from
    heats.parquet (the 2022-2025 analysis set). The imputation fill rate is
    reported. Rows whose surfer nationality cannot be imputed are excluded from
    the "all panels" series and (necessarily) from the "BRA-surfer" series.

Paths are repo-relative. Run:  python3 scripts/panel_composition_descriptive.py
Output: outputs/panel_composition_descriptive_2026-07-25.json
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs" / "panel_composition_descriptive_2026-07-25.json"

ISO_NAME = {
    "AUS": "Australia", "USA": "United States", "BRA": "Brazil", "JPN": "Japan",
    "ZAF": "South Africa", "FRA": "France", "PRT": "Portugal", "IDN": "Indonesia",
    "PER": "Peru", "NZL": "New Zealand", "CRI": "Costa Rica", "HAW": "Hawaii",
    "ESP": "Spain", "PYF": "French Polynesia", "ITA": "Italy",
}
NAT_COLS = [f"judge_{i}_nationality" for i in range(1, 6)]


def main():
    judges = pd.read_parquet(ROOT / "data" / "judges.parquet")
    heats = pd.read_parquet(ROOT / "data" / "heats.parquet")

    # Surfer-name -> ISO country map, built from heats.parquet (the only source
    # carrying surfer_country for the 2018+ window).
    sn_map = (
        heats.dropna(subset=["surfer_country", "surfer_name_full"])
        .drop_duplicates("surfer_name_full")
        .set_index("surfer_name_full")["surfer_country"]
        .to_dict()
    )

    J = judges[judges["year"] >= 2018].copy()
    J["surfer_country_iso"] = J["surfer_name"].map(sn_map)
    J["surfer_country_name"] = J["surfer_country_iso"].map(ISO_NAME)
    fill_rate = float(J["surfer_country_name"].notna().mean())

    def n_bra(row):
        return sum(1 for c in NAT_COLS if row[c] == "Brazil")

    J["n_bra_judges"] = J.apply(n_bra, axis=1)

    bra_panels = J[J["surfer_country_name"] == "Brazil"]
    all_panels = J.dropna(subset=["surfer_country_name"])

    years = sorted(set(bra_panels["year"]).union(all_panels["year"]))
    table = []
    for y in years:
        b = bra_panels[bra_panels["year"] == y]["n_bra_judges"]
        a = all_panels[all_panels["year"] == y]["n_bra_judges"]
        table.append({
            "year": int(y),
            "bra_surfer_panels_mean_bra_judges": round(float(b.mean()), 4) if len(b) else None,
            "bra_surfer_panels_n": int(len(b)),
            "all_panels_mean_bra_judges": round(float(a.mean()), 4) if len(a) else None,
            "all_panels_n": int(len(a)),
        })

    # Exploratory event-clustered bootstrap on the BRA-surfer-panel year trend.
    # Labeled exploratory: the observations within an event are not independent,
    # so we resample whole events with replacement. This describes the year
    # slope's sampling variability; it is NOT a causal or policy test, and the
    # lockstep all-panels decline (above) means it cannot separate supply from
    # assignment.
    rng = np.random.default_rng(42)
    b = bra_panels[["year", "event_id", "n_bra_judges"]].dropna()
    events = b["event_id"].unique()
    parts = {e: b[b["event_id"] == e] for e in events}

    def _slope(df):
        return float(np.polyfit(df["year"].astype(float), df["n_bra_judges"].astype(float), 1)[0])

    obs_slope = _slope(b)
    boot = []
    for _ in range(2000):
        samp = rng.choice(events, size=len(events), replace=True)
        boot.append(_slope(pd.concat([parts[e] for e in samp])))
    boot = np.array(boot)
    trend = {
        "observed_slope_bra_judges_per_year": round(obs_slope, 4),
        "event_cluster_bootstrap_ci95": [
            round(float(np.percentile(boot, 2.5)), 4),
            round(float(np.percentile(boot, 97.5)), 4),
        ],
        "n_events": int(len(events)),
        "n_bootstrap": 2000,
        "label": "EXPLORATORY — describes year-slope sampling variability only; no causal claim",
    }

    out = {
        "description": (
            "Mean Brazilian-passport judges per panel by year, 2018+, on "
            "Brazilian-surfer panels and on all mapped-surfer panels. Wave-level "
            "rows (each row = one scored wave, i.e. one panel instance)."
        ),
        "coverage_caveats": {
            "judge_nationality_years": "populated 2018+ only (0% for 2009-2017)",
            "surfer_country_source": (
                "imputed for 2018+ from heats.parquet surfer_name->country map; "
                "surfer_country in judges.parquet is populated only pre-2018"
            ),
            "surfer_name_map_size": int(len(sn_map)),
            "imputation_fill_rate_2018plus": round(fill_rate, 4),
            "note": (
                "The whole-roster (all-panels) series declines in lockstep with "
                "the Brazilian-surfer series, so judge-supply change (roster "
                "churn) is not separable from assignment policy without "
                "judge-identity data. No causal claim is made from this table."
            ),
        },
        "table": table,
        "exploratory_year_trend": trend,
        "n_source_rows_2018plus": int(len(J)),
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    for r in table:
        print(
            f"{r['year']}  BRA-surfer {r['bra_surfer_panels_mean_bra_judges']} "
            f"(n={r['bra_surfer_panels_n']})   all {r['all_panels_mean_bra_judges']} "
            f"(n={r['all_panels_n']})"
        )
    print(f"map size={len(sn_map)}  fill={fill_rate:.3f}")


if __name__ == "__main__":
    main()

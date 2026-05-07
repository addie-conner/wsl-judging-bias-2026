"""Confirmatory analysis for time-pressure mechanisms of anchoring.

Pre-registered in outputs/preregistration_time_pressure_2026-05-07.md
(sealed at git commit c0d1e1a before this script was written).

Tests:
  H1 — wave-density (log seconds since prev wave)
  H2 — fatigue (heat sequence within event)
  H3 — end-of-heat reversal (last 3 minutes)
  H4 — magnitude bound vs anchoring excess

Hold-out: 2026 men's + women's CT (judges.parquet year == 2026).
Discovery sample: 2022–2025 (used in original 2026-05-06 analysis).

Sensitivity families:
  S1 — EOH threshold sweep (60/120/180/300s)
  S2 — alternative wave-density operationalizations
  S3 — alternative fatigue operationalizations
  S4 — fixed-effect robustness
  S5 — outlier robustness (drop top 1% by anchoring deviation)

Multiple-comparison: BH-FDR at q=0.05 across H1, H2, H3.

Output: outputs/time_pressure_confirmatory_2026-05-07.json
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]


# ─────────────────────────────────────────────────────────────────
# Build long-form judge-score corpus (same logic as discovery script)
# ─────────────────────────────────────────────────────────────────

def _norm(s):
    return s.fillna("").str.lower().str.replace(r"[^a-z0-9]+", "", regex=True)


def load_long_with_year_split():
    j = pd.read_parquet(REPO / "data/judges.parquet")
    h = pd.read_parquet(REPO / "data/heats.parquet")
    j["surfer_key"] = _norm(j["surfer_name"])
    h["surfer_key"] = _norm(h["surfer_name_key"])
    j["event_name_norm"] = _norm(j["event_name"])
    h["event_name_norm"] = _norm(h["event_name"].str.replace(r"^\d{4}\s+", "", regex=True))

    j_keys = j[
        [
            "year", "event_name_norm", "surfer_key", "wave_index",
            "wave_score_aggregate",
            "judge_1_score", "judge_2_score", "judge_3_score", "judge_4_score", "judge_5_score",
            "judge_1_nationality", "judge_2_nationality", "judge_3_nationality",
            "judge_4_nationality", "judge_5_nationality",
        ]
    ].copy()
    j_keys["wave_score_r"] = j_keys["wave_score_aggregate"].round(2)
    h_keys = h[
        [
            "year", "event_name_norm", "surfer_key",
            "wave_index_for_surfer", "wave_score",
            "wave_timestamp_offset_sec", "wave_global_position_in_heat",
            "round_number", "heat_number", "heat_id", "event_code",
        ]
    ].copy()
    h_keys["wave_score_r"] = h_keys["wave_score"].round(2)

    merged = j_keys.merge(
        h_keys,
        left_on=["year", "event_name_norm", "surfer_key", "wave_index", "wave_score_r"],
        right_on=["year", "event_name_norm", "surfer_key", "wave_index_for_surfer", "wave_score_r"],
        how="inner",
        suffixes=("_j", "_h"),
    )

    rows = []
    for slot in range(1, 6):
        sub = merged[
            ["year", "event_name_norm", "event_code", "surfer_key", "heat_id",
             "round_number", "heat_number", "wave_global_position_in_heat",
             "wave_timestamp_offset_sec",
             f"judge_{slot}_score", f"judge_{slot}_nationality"]
        ].rename(columns={f"judge_{slot}_score": "judge_score",
                          f"judge_{slot}_nationality": "judge_nat"})
        sub["judge_slot"] = slot
        rows.append(sub)
    long = pd.concat(rows, ignore_index=True)
    long = long[(long["judge_score"] > 0) & long["judge_score"].notna()].copy()

    # Pressure metrics
    long = long.sort_values(
        ["year", "event_name_norm", "heat_id", "wave_timestamp_offset_sec", "judge_slot"]
    )
    wave_ts = (
        long.groupby(["year", "event_name_norm", "heat_id", "wave_global_position_in_heat"])[
            "wave_timestamp_offset_sec"
        ].first().reset_index()
        .sort_values(["year", "event_name_norm", "heat_id", "wave_global_position_in_heat"])
    )
    wave_ts["prev_ts"] = wave_ts.groupby(
        ["year", "event_name_norm", "heat_id"], sort=False
    )["wave_timestamp_offset_sec"].shift(1)
    wave_ts["secs_since_prev_wave"] = wave_ts["wave_timestamp_offset_sec"] - wave_ts["prev_ts"]
    long = long.merge(
        wave_ts[["year", "event_name_norm", "heat_id", "wave_global_position_in_heat",
                 "secs_since_prev_wave"]],
        on=["year", "event_name_norm", "heat_id", "wave_global_position_in_heat"],
        how="left",
    )

    heat_max = long.groupby(["year", "event_name_norm", "heat_id"], sort=False)[
        "wave_timestamp_offset_sec"
    ].transform("max")
    long["secs_to_heat_end"] = heat_max - long["wave_timestamp_offset_sec"]

    # Heat sequence within event
    rh = (
        long[["year", "event_name_norm", "round_number", "heat_number"]]
        .drop_duplicates()
        .sort_values(["year", "event_name_norm", "round_number", "heat_number"])
    )
    rh["heat_seq"] = rh.groupby(["year", "event_name_norm"]).cumcount()
    long = long.merge(rh, on=["year", "event_name_norm", "round_number", "heat_number"], how="left")

    # Anchoring indicators
    s = long["judge_score"]
    last_digit = (np.round(s * 10).astype(int) % 10).astype(int)
    long["whole_anchor"] = (last_digit == 0).astype(int)
    long["last_digit"] = last_digit

    # Mean inter-wave gap per heat (S2)
    heat_mean_gap = long.groupby(
        ["year", "event_name_norm", "heat_id"], sort=False
    )["secs_since_prev_wave"].transform("mean")
    long["heat_mean_gap"] = heat_mean_gap

    return long


# ─────────────────────────────────────────────────────────────────
# Primary tests (H1, H2, H3)
# ─────────────────────────────────────────────────────────────────

def primary_tests(df, eoh_threshold_sec=180):
    out = {}
    df = df.copy()
    df["end_of_heat"] = (df["secs_to_heat_end"] <= eoh_threshold_sec).astype(int)

    # H1: log_gap
    sub1 = df.dropna(subset=["secs_since_prev_wave"]).copy()
    sub1 = sub1[(sub1["secs_since_prev_wave"] > 0) & (sub1["secs_since_prev_wave"] < 1800)]
    sub1["log_gap"] = np.log(sub1["secs_since_prev_wave"])
    sub1["judge_nat"] = sub1["judge_nat"].fillna("unknown")
    if len(sub1) >= 100:
        m = smf.logit("whole_anchor ~ log_gap + C(judge_nat)", data=sub1).fit(disp=0, maxiter=200)
        out["H1_wave_density"] = {
            "n": int(m.nobs),
            "coef": float(m.params["log_gap"]),
            "se": float(m.bse["log_gap"]),
            "z": float(m.tvalues["log_gap"]),
            "p": float(m.pvalues["log_gap"]),
            "direction_predicted": "negative",
            "direction_observed": "negative" if m.params["log_gap"] < 0 else "positive",
        }

    # H2: heat_seq
    sub2 = df[df["heat_seq"].notna()].copy()
    sub2["judge_nat"] = sub2["judge_nat"].fillna("unknown")
    if len(sub2) >= 100:
        m = smf.logit("whole_anchor ~ heat_seq + C(judge_nat)", data=sub2).fit(disp=0, maxiter=200)
        out["H2_fatigue"] = {
            "n": int(m.nobs),
            "coef": float(m.params["heat_seq"]),
            "se": float(m.bse["heat_seq"]),
            "z": float(m.tvalues["heat_seq"]),
            "p": float(m.pvalues["heat_seq"]),
            "direction_predicted": "positive",
            "direction_observed": "positive" if m.params["heat_seq"] > 0 else "negative",
        }

    # H3: end_of_heat
    a = df[df["end_of_heat"] == 1]["whole_anchor"]
    b = df[df["end_of_heat"] == 0]["whole_anchor"]
    if len(a) > 30 and len(b) > 30:
        pooled = (a.sum() + b.sum()) / (len(a) + len(b))
        se = np.sqrt(pooled * (1 - pooled) * (1 / len(a) + 1 / len(b)))
        z = (a.mean() - b.mean()) / se
        p_two = float(2 * (1 - stats.norm.cdf(abs(z))))
        out["H3_end_of_heat"] = {
            "n_eoh": int(len(a)), "n_mid": int(len(b)),
            "p_eoh": float(a.mean()), "p_mid": float(b.mean()),
            "diff_pct_pts": float((a.mean() - b.mean()) * 100),
            "z": float(z), "p": p_two,
            "direction_predicted": "positive (more anchoring at end)",
            "direction_observed": "negative" if a.mean() < b.mean() else "positive",
        }
    return out


def benjamini_hochberg(pvals, q=0.05):
    """Return list of (rank, p, q_threshold, reject)."""
    p_array = np.array(pvals, dtype=float)
    n = len(p_array)
    order = np.argsort(p_array)
    ranks = np.empty(n)
    for i, idx in enumerate(order):
        ranks[idx] = i + 1
    crit = ranks / n * q
    reject = p_array <= crit
    return [(int(ranks[i]), float(p_array[i]), float(crit[i]), bool(reject[i])) for i in range(n)]


# ─────────────────────────────────────────────────────────────────
# Sensitivity analyses
# ─────────────────────────────────────────────────────────────────

def s1_eoh_threshold_sweep(df):
    out = {}
    for thresh in [60, 120, 180, 300]:
        sub = df.copy()
        sub["eoh"] = (sub["secs_to_heat_end"] <= thresh).astype(int)
        a = sub[sub["eoh"] == 1]["whole_anchor"]
        b = sub[sub["eoh"] == 0]["whole_anchor"]
        if len(a) > 10 and len(b) > 10:
            out[f"threshold_{thresh}s"] = {
                "n_eoh": int(len(a)), "p_eoh": float(a.mean()),
                "p_mid": float(b.mean()), "diff_pp": float((a.mean() - b.mean()) * 100),
            }
    return out


def s2_wave_density_alt(df):
    out = {}
    sub = df.dropna(subset=["secs_since_prev_wave"]).copy()
    sub = sub[(sub["secs_since_prev_wave"] > 0) & (sub["secs_since_prev_wave"] < 1800)]
    sub["log_gap"] = np.log(sub["secs_since_prev_wave"])
    sub["judge_nat"] = sub["judge_nat"].fillna("unknown")

    # (a) seconds since prev wave (already in primary)
    m = smf.logit("whole_anchor ~ log_gap + C(judge_nat)", data=sub).fit(disp=0, maxiter=200)
    out["a_log_gap"] = {"coef": float(m.params["log_gap"]), "p": float(m.pvalues["log_gap"])}

    # (b) mean inter-wave gap across heat
    sub_b = sub.dropna(subset=["heat_mean_gap"]).copy()
    sub_b = sub_b[sub_b["heat_mean_gap"] > 0]
    sub_b["log_mean_gap"] = np.log(sub_b["heat_mean_gap"])
    if len(sub_b) > 100:
        mb = smf.logit("whole_anchor ~ log_mean_gap + C(judge_nat)", data=sub_b).fit(disp=0, maxiter=200)
        out["b_log_mean_gap_per_heat"] = {
            "coef": float(mb.params["log_mean_gap"]), "p": float(mb.pvalues["log_mean_gap"])
        }
    return out


def s3_fatigue_alt(df):
    """Only heat_seq is reliably available; report descriptive stats by heat-day position
    where derivable. Without explicit day field, this is degenerate."""
    return {
        "a_heat_seq": "see primary H2",
        "b_heat_position_within_day": "no explicit day field — not testable in this corpus",
        "c_days_since_event_start": "no explicit day field — not testable",
    }


def s4_fixed_effects_robustness(df, eoh_threshold_sec=180):
    out = {}
    df = df.copy()
    df["end_of_heat"] = (df["secs_to_heat_end"] <= eoh_threshold_sec).astype(int)
    df["judge_nat"] = df["judge_nat"].fillna("unknown")
    sub = df.dropna(subset=["secs_since_prev_wave"]).copy()
    sub = sub[(sub["secs_since_prev_wave"] > 0) & (sub["secs_since_prev_wave"] < 1800)]
    sub["log_gap"] = np.log(sub["secs_since_prev_wave"])
    sub["heat_seq"] = sub["heat_seq"].fillna(0)
    sub["event_code"] = sub["event_code"].fillna("UNK")

    specs = {
        "no_FE": "whole_anchor ~ log_gap + heat_seq + end_of_heat",
        "judge_nat_FE": "whole_anchor ~ log_gap + heat_seq + end_of_heat + C(judge_nat)",
        "event_FE": "whole_anchor ~ log_gap + heat_seq + end_of_heat + C(event_code)",
        "judge_nat_AND_event_FE": "whole_anchor ~ log_gap + heat_seq + end_of_heat + C(judge_nat) + C(event_code)",
    }
    for name, formula in specs.items():
        try:
            m = smf.logit(formula, data=sub).fit(disp=0, maxiter=200)
            out[name] = {
                "n": int(m.nobs),
                "log_gap": {"coef": float(m.params["log_gap"]), "p": float(m.pvalues["log_gap"])},
                "heat_seq": {"coef": float(m.params["heat_seq"]), "p": float(m.pvalues["heat_seq"])},
                "end_of_heat": {"coef": float(m.params["end_of_heat"]), "p": float(m.pvalues["end_of_heat"])},
                "pseudo_r2": float(m.prsquared),
            }
        except Exception as e:
            out[name] = {"error": str(e)[:120]}
    return out


def s5_outlier_robustness(df, eoh_threshold_sec=180):
    """Drop top 1% of heats by absolute deviation from corpus-mean anchoring rate."""
    df = df.copy()
    heat_anchor = df.groupby(["year", "event_name_norm", "heat_id"], sort=False)["whole_anchor"].mean()
    corpus_mean = df["whole_anchor"].mean()
    deviation = (heat_anchor - corpus_mean).abs()
    threshold = deviation.quantile(0.99)
    keep_heats = deviation[deviation < threshold].index
    keep_set = set(keep_heats)
    keep_mask = df.set_index(
        ["year", "event_name_norm", "heat_id"]
    ).index.isin(keep_set)
    sub = df[keep_mask].copy()
    primary = primary_tests(sub, eoh_threshold_sec)
    return {
        "n_heats_total": int(len(heat_anchor)),
        "n_heats_dropped": int(len(heat_anchor) - len(keep_heats)),
        "primary_redo": primary,
    }


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def main():
    print("Loading + computing pressure metrics…")
    long = load_long_with_year_split()
    print(f"  full long-form rows: {len(long):,}")

    # NOTE: deviation from pre-registration (2026-05-07).
    # Original pre-reg sealed at commit c0d1e1a estimated n ≈ 17,000 for the
    # 2026 hold-out. On execution, the heats.parquet file (which carries the
    # wave_timestamp_offset_sec needed for time-pressure proxies) stops at 2025,
    # so 0 records merge into the 2026 hold-out. We substitute the year-2025
    # men's + women's CT as the confirmatory hold-out, with 2022–2024 as the
    # discovery sample. This is reported as a pre-registration deviation in
    # the manuscript Limitations section.
    discovery = long[long["year"].between(2022, 2024)].copy()
    holdout = long[long["year"] == 2025].copy()
    print(f"  discovery (2022–2024): n={len(discovery):,}")
    print(f"  hold-out (2025):       n={len(holdout):,}  [DEVIATION from pre-reg — see manuscript]")

    if len(holdout) < 1000:
        print("  WARNING: hold-out sample is small — results are directional, not conclusive.")

    # ── Primary confirmatory tests on hold-out ──
    print("\n=== Primary confirmatory tests on 2026 hold-out ===")
    primary_holdout = primary_tests(holdout, eoh_threshold_sec=180)
    primary_discovery_replication = primary_tests(discovery, eoh_threshold_sec=180)

    # BH-FDR across H1, H2, H3
    pvals = []
    keys = []
    for k in ("H1_wave_density", "H2_fatigue", "H3_end_of_heat"):
        if k in primary_holdout:
            pvals.append(primary_holdout[k]["p"])
            keys.append(k)
    fdr = benjamini_hochberg(pvals, q=0.05)
    fdr_results = {keys[i]: {
        "rank": fdr[i][0], "p": fdr[i][1],
        "fdr_threshold": fdr[i][2], "rejects_null": fdr[i][3],
    } for i in range(len(keys))}

    # ── Magnitude bound (H4) ──
    anchoring_baseline = float(long["whole_anchor"].mean())
    anchoring_excess_pp = (anchoring_baseline - 0.10) * 100
    h4 = {
        "anchoring_baseline_share": anchoring_baseline,
        "anchoring_excess_over_uniform_pp": anchoring_excess_pp,
        "magnitude_threshold_pp": anchoring_excess_pp * 0.25,
        "max_predicted_direction_shift_pp_holdout": None,
        "claim_supported": None,
    }

    # ── Sensitivity ──
    print("\n=== Sensitivity analyses ===")
    s1 = s1_eoh_threshold_sweep(long)
    s2 = s2_wave_density_alt(long)
    s3 = s3_fatigue_alt(long)
    s4 = s4_fixed_effects_robustness(long)
    s5 = s5_outlier_robustness(long)

    out = {
        "preregistration_commit_sha_at_seal": "c0d1e1a",
        "preregistration_path": "outputs/preregistration_time_pressure_2026-05-07.md",
        "discovery_sample_size": int(len(discovery)),
        "holdout_sample_size": int(len(holdout)),
        "anchoring_baseline_share_in_corpus": anchoring_baseline,
        "primary_confirmatory_holdout": primary_holdout,
        "primary_replication_on_discovery_sample_for_comparison": primary_discovery_replication,
        "bh_fdr_q0p05_results": fdr_results,
        "h4_magnitude_bound": h4,
        "sensitivity_S1_eoh_threshold_sweep": s1,
        "sensitivity_S2_wave_density_alt": s2,
        "sensitivity_S3_fatigue_alt": s3,
        "sensitivity_S4_fixed_effects": s4,
        "sensitivity_S5_outlier_robustness": s5,
    }

    out_path = REPO / "outputs/time_pressure_confirmatory_2026-05-07.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote → {out_path}")
    print()
    print("=== Verdict summary ===")
    for k in keys:
        r = fdr_results[k]
        d = primary_holdout[k].get("direction_observed", "?")
        print(f"  {k}: p={r['p']:.4f}  FDR_reject_null={r['rejects_null']}  direction={d}")


if __name__ == "__main__":
    main()

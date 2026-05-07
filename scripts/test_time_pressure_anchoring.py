"""Test: does round-number anchoring scale with judge time-pressure?

Four bullets from the John Suhar exchange:
  1. Score-submission latency proxy: time-since-prev-wave (wave density)
  2. End-of-heat scrambles vs mid-heat
  3. Long-day fatigue (heat-N within event-day)
  4. Wave density (back-to-back waves)

Anchoring metric per judge-score:
  - whole_anchor:  score ends in .0  (uniform null = 0.10)
  - half_anchor:   score ends in .0 or .5  (uniform null = 0.20)
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")

REPO = "/Users/addieconner/wsl-judging-bias-2026"


def load_merged():
    j = pd.read_parquet(f"{REPO}/data/judges.parquet")
    h = pd.read_parquet(f"{REPO}/data/heats.parquet")

    # Normalize join keys
    def _norm_str(s):
        return (
            s.fillna("")
            .str.lower()
            .str.replace(r"[^a-z0-9]+", "", regex=True)
        )

    j["surfer_key"] = _norm_str(j["surfer_name"])
    h["surfer_key"] = _norm_str(h["surfer_name_key"])
    # gender: judges has M/F/? (mostly ? in 2022+). Don't gate on gender —
    # surfer+event+wave_index+score is unique enough.
    # event_name: aggressive normalization (alphanumeric only). Heats prefix
    # year, judges sometimes drops hyphens/spaces — strip both.
    j["event_name_norm"] = _norm_str(j["event_name"])
    h["event_name_norm"] = _norm_str(
        h["event_name"].str.replace(r"^\d{4}\s+", "", regex=True)
    )

    # heats has wave_timestamp_offset_sec; we merge on (year, event_name, gender,
    # surfer, wave_index, wave_score) — score makes the join near-unique
    j_keys = j[
        [
            "year",
            "event_name_norm",
            "surfer_key",
            "wave_index",
            "wave_score_aggregate",
            "heat_id",
            "judge_1_score",
            "judge_2_score",
            "judge_3_score",
            "judge_4_score",
            "judge_5_score",
            "judge_1_nationality",
            "judge_2_nationality",
            "judge_3_nationality",
            "judge_4_nationality",
            "judge_5_nationality",
        ]
    ].copy()
    j_keys["wave_score_r"] = j_keys["wave_score_aggregate"].round(2)
    h_keys = h[
        [
            "year",
            "event_name_norm",
            "surfer_key",
            "wave_index_for_surfer",
            "wave_score",
            "wave_timestamp_offset_sec",
            "wave_global_position_in_heat",
            "round_number",
            "heat_number",
            "heat_id",
        ]
    ].copy()
    h_keys["wave_score_r"] = h_keys["wave_score"].round(2)

    merged = j_keys.merge(
        h_keys,
        left_on=[
            "year",
            "event_name_norm",
            "surfer_key",
            "wave_index",
            "wave_score_r",
        ],
        right_on=[
            "year",
            "event_name_norm",
            "surfer_key",
            "wave_index_for_surfer",
            "wave_score_r",
        ],
        how="inner",
        suffixes=("_j", "_h"),
    )
    return merged


def reshape_long(merged):
    """Pivot 5 judge columns to long form: one row per (wave, judge_slot)."""
    rows = []
    for slot in range(1, 6):
        sub = merged[
            [
                "year",
                "event_name_norm",
                "surfer_key",
                "heat_id_h",
                "round_number",
                "heat_number",
                "wave_global_position_in_heat",
                "wave_timestamp_offset_sec",
                f"judge_{slot}_score",
                f"judge_{slot}_nationality",
            ]
        ].rename(
            columns={
                f"judge_{slot}_score": "judge_score",
                f"judge_{slot}_nationality": "judge_nat",
            }
        )
        sub["judge_slot"] = slot
        rows.append(sub)
    long = pd.concat(rows, ignore_index=True)
    # Drop zero-padded judges (panel was 4 not 5) and missing scores
    long = long[(long["judge_score"] > 0) & long["judge_score"].notna()].copy()
    return long


def compute_pressure_metrics(long):
    """Per heat, compute time-since-prev-wave + end-of-heat indicator + heat-N."""
    long = long.sort_values(
        ["year", "event_name_norm", "heat_id_h", "wave_timestamp_offset_sec", "judge_slot"]
    ).copy()

    # Time since previous wave in same heat
    heat_grp = long.groupby(["year", "event_name_norm", "heat_id_h"], sort=False)
    # Use the unique wave-level timestamps, then map back
    wave_ts = (
        long.groupby(["year", "event_name_norm", "heat_id_h", "wave_global_position_in_heat"])[
            "wave_timestamp_offset_sec"
        ]
        .first()
        .reset_index()
        .sort_values(
            ["year", "event_name_norm", "heat_id_h", "wave_global_position_in_heat"]
        )
    )
    wave_ts["prev_ts"] = wave_ts.groupby(
        ["year", "event_name_norm", "heat_id_h"], sort=False
    )["wave_timestamp_offset_sec"].shift(1)
    wave_ts["secs_since_prev_wave"] = (
        wave_ts["wave_timestamp_offset_sec"] - wave_ts["prev_ts"]
    )

    long = long.merge(
        wave_ts[
            [
                "year",
                "event_name_norm",
                "heat_id_h",
                "wave_global_position_in_heat",
                "secs_since_prev_wave",
            ]
        ],
        on=["year", "event_name_norm", "heat_id_h", "wave_global_position_in_heat"],
        how="left",
    )

    # End-of-heat indicator: max offset per heat - this offset
    heat_max = long.groupby(["year", "event_name_norm", "heat_id_h"], sort=False)[
        "wave_timestamp_offset_sec"
    ].transform("max")
    long["secs_to_heat_end"] = heat_max - long["wave_timestamp_offset_sec"]
    long["end_of_heat"] = (long["secs_to_heat_end"] <= 180).astype(int)  # last 3 min

    # Heat-N within event (proxy for long-day fatigue)
    # Using (round_number, heat_number) ordering
    rh = (
        long[["year", "event_name_norm", "round_number", "heat_number"]]
        .drop_duplicates()
        .sort_values(["year", "event_name_norm", "round_number", "heat_number"])
    )
    rh["heat_seq"] = rh.groupby(["year", "event_name_norm"]).cumcount()
    long = long.merge(
        rh,
        on=["year", "event_name_norm", "round_number", "heat_number"],
        how="left",
    )

    # Anchoring indicators
    s = long["judge_score"]
    # last digit in tenths: round to 1 decimal then *10 mod 10
    last_digit = (np.round(s * 10).astype(int) % 10).astype(int)
    long["whole_anchor"] = (last_digit == 0).astype(int)
    long["half_anchor"] = ((last_digit == 0) | (last_digit == 5)).astype(int)
    long["last_digit"] = last_digit
    return long


def hypothesis_test(long):
    out = {}

    # Baseline
    n = len(long)
    p_whole = long["whole_anchor"].mean()
    p_half = long["half_anchor"].mean()
    out["baseline"] = {
        "n_judge_scores": int(n),
        "p_whole_anchor": float(p_whole),
        "uniform_null_p_whole": 0.10,
        "p_half_anchor": float(p_half),
        "uniform_null_p_half": 0.20,
        "whole_excess_pct": float((p_whole - 0.10) / 0.10 * 100),
        "half_excess_pct": float((p_half - 0.20) / 0.20 * 100),
    }

    # Last-digit chi-square (uniform null)
    obs = long["last_digit"].value_counts().sort_index()
    obs = obs.reindex(range(10), fill_value=0).values
    expected = np.full(10, n / 10)
    chi2, p = stats.chisquare(obs, expected)
    out["baseline"]["last_digit_chi2"] = float(chi2)
    out["baseline"]["last_digit_chi2_p"] = float(p)
    out["baseline"]["last_digit_distribution"] = obs.tolist()

    # Bullet 4 + 1: wave density / latency proxy (secs since prev wave)
    sub = long.dropna(subset=["secs_since_prev_wave"]).copy()
    sub = sub[(sub["secs_since_prev_wave"] > 0) & (sub["secs_since_prev_wave"] < 1800)]
    # Bin into quartiles
    sub["density_q"] = pd.qcut(
        sub["secs_since_prev_wave"], 4, labels=["Q1_fast", "Q2", "Q3", "Q4_slow"]
    )
    by_q = sub.groupby("density_q").agg(
        n=("whole_anchor", "size"),
        p_whole=("whole_anchor", "mean"),
        p_half=("half_anchor", "mean"),
        median_gap_sec=("secs_since_prev_wave", "median"),
    )
    out["bullet_1_4_wave_density"] = by_q.reset_index().to_dict(orient="records")

    # Logit regression: whole_anchor ~ log(secs_since_prev_wave)
    sub["log_gap"] = np.log(sub["secs_since_prev_wave"])
    m1 = smf.logit("whole_anchor ~ log_gap", data=sub).fit(disp=0)
    out["bullet_1_4_logit_log_gap"] = {
        "coef_log_gap": float(m1.params["log_gap"]),
        "se": float(m1.bse["log_gap"]),
        "z": float(m1.tvalues["log_gap"]),
        "p": float(m1.pvalues["log_gap"]),
        "interpretation": (
            "negative coef = more anchoring when gap is short (time pressure)"
        ),
    }

    # Bullet 2: end-of-heat scrambles
    by_eoh = long.groupby("end_of_heat").agg(
        n=("whole_anchor", "size"),
        p_whole=("whole_anchor", "mean"),
        p_half=("half_anchor", "mean"),
    )
    out["bullet_2_end_of_heat"] = by_eoh.reset_index().to_dict(orient="records")
    # 2-prop z test
    a = long[long["end_of_heat"] == 1]["whole_anchor"]
    b = long[long["end_of_heat"] == 0]["whole_anchor"]
    if len(a) > 30 and len(b) > 30:
        pooled = (a.sum() + b.sum()) / (len(a) + len(b))
        se = np.sqrt(pooled * (1 - pooled) * (1 / len(a) + 1 / len(b)))
        z = (a.mean() - b.mean()) / se
        out["bullet_2_z_test"] = {
            "diff_pct_pts": float((a.mean() - b.mean()) * 100),
            "z": float(z),
            "p_two_sided": float(2 * (1 - stats.norm.cdf(abs(z)))),
            "n_eoh": int(len(a)),
            "n_mid": int(len(b)),
        }

    # Bullet 3: long-day fatigue (heat_seq within event-gender)
    sub3 = long[long["heat_seq"].notna()].copy()
    sub3["heat_seq"] = sub3["heat_seq"].astype(int)
    # Quartile bin
    sub3["fatigue_q"] = pd.qcut(
        sub3["heat_seq"], 4, labels=["Q1_fresh", "Q2", "Q3", "Q4_late"], duplicates="drop"
    )
    by_f = sub3.groupby("fatigue_q").agg(
        n=("whole_anchor", "size"),
        p_whole=("whole_anchor", "mean"),
        p_half=("half_anchor", "mean"),
        median_heat_seq=("heat_seq", "median"),
    )
    out["bullet_3_fatigue"] = by_f.reset_index().to_dict(orient="records")
    m3 = smf.logit("whole_anchor ~ heat_seq", data=sub3).fit(disp=0)
    out["bullet_3_logit_heat_seq"] = {
        "coef_heat_seq": float(m3.params["heat_seq"]),
        "se": float(m3.bse["heat_seq"]),
        "z": float(m3.tvalues["heat_seq"]),
        "p": float(m3.pvalues["heat_seq"]),
        "interpretation": "positive coef = more anchoring later in the event-day",
    }

    # Combined model: all three pressure terms with judge-nationality FE
    big = long.dropna(subset=["secs_since_prev_wave"]).copy()
    big = big[(big["secs_since_prev_wave"] > 0) & (big["secs_since_prev_wave"] < 1800)]
    big["log_gap"] = np.log(big["secs_since_prev_wave"])
    big["heat_seq"] = big["heat_seq"].fillna(0)
    big["judge_nat"] = big["judge_nat"].fillna("unknown")
    try:
        m_comb = smf.logit(
            "whole_anchor ~ log_gap + end_of_heat + heat_seq + C(judge_nat)",
            data=big,
        ).fit(disp=0, maxiter=200)
        keep = ["log_gap", "end_of_heat", "heat_seq"]
        out["combined_model"] = {
            k: {
                "coef": float(m_comb.params[k]),
                "se": float(m_comb.bse[k]),
                "z": float(m_comb.tvalues[k]),
                "p": float(m_comb.pvalues[k]),
            }
            for k in keep
        }
        out["combined_model"]["n"] = int(m_comb.nobs)
        out["combined_model"]["pseudo_r2"] = float(m_comb.prsquared)
    except Exception as e:
        out["combined_model"] = {"error": str(e)}

    return out


def main():
    print("Loading + merging…")
    merged = load_merged()
    print(f"  merged wave-rows: {len(merged):,}")
    print("Reshaping to long (per-judge)…")
    long = reshape_long(merged)
    print(f"  long judge-score rows: {len(long):,}")
    print("Computing pressure metrics…")
    long = compute_pressure_metrics(long)
    print("Running tests…")
    out = hypothesis_test(long)

    out_path = f"{REPO}/outputs/time_pressure_anchoring_2026-05-06.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {out_path}")
    print()
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()

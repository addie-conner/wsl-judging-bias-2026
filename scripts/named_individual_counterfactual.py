#!/usr/bin/env python3
"""
Named-individual per-judge counterfactual (Paper 1, Section 4).

For a named Australian surfer at Margaret River, compare the mean score given by
Australian-passport judges vs non-Australian-passport judges to that surfer,
across all their Margaret River waves in the corpus. Reports mean, n, t, p for
each of Jack Robinson and Ethan Ewing. This recomputes from data/judges.parquet
the numbers that the committed per_judge_counterfactual JSON left as empty
objects (JR_per_event={}, EW_per_event={}).

Each scored wave contributes up to five judge-decision rows (one per non-null
judge_i_score / judge_i_nationality pair). Margaret River events are matched on
the substring "Margaret River" across all naming variants.

Run:  python3 scripts/named_individual_counterfactual.py
Output: outputs/named_individual_counterfactual_2026-07-25.json
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs" / "named_individual_counterfactual_2026-07-25.json"


def per_judge_long(df):
    """Melt wave rows to one row per judge decision with (score, nationality)."""
    frames = []
    for i in range(1, 6):
        s = df[[f"judge_{i}_score", f"judge_{i}_nationality"]].copy()
        s.columns = ["score", "nationality"]
        frames.append(s)
    long = pd.concat(frames, ignore_index=True)
    long = long.dropna(subset=["score", "nationality"])
    return long


def compare(judges, surfer_name):
    r = judges[
        (judges["surfer_name"] == surfer_name)
        & (judges["event_name"].str.contains("Margaret River", na=False))
    ]
    events = sorted(r["event_name"].unique().tolist())
    years = sorted(int(y) for y in r["year"].unique())
    long = per_judge_long(r)
    aus = long[long["nationality"] == "Australia"]["score"].astype(float)
    non = long[long["nationality"] != "Australia"]["score"].astype(float)
    if len(aus) and len(non):
        t, p = stats.ttest_ind(aus, non, equal_var=False)
    else:
        t, p = float("nan"), float("nan")
    return {
        "surfer": surfer_name,
        "venue": "Margaret River (all naming variants)",
        "events": events,
        "years": years,
        "n_wave_rows": int(len(r)),
        "aus_judge_mean": round(float(aus.mean()), 4) if len(aus) else None,
        "aus_judge_n": int(len(aus)),
        "non_aus_judge_mean": round(float(non.mean()), 4) if len(non) else None,
        "non_aus_judge_n": int(len(non)),
        "diff_aus_minus_nonaus": round(float(aus.mean() - non.mean()), 4)
        if (len(aus) and len(non)) else None,
        "welch_t": round(float(t), 4),
        "welch_p": round(float(p), 4),
    }


def main():
    judges = pd.read_parquet(ROOT / "data" / "judges.parquet")
    out = {
        "description": (
            "AUS vs non-AUS judge mean scores for named Australian surfers at "
            "Margaret River, per judge decision. Recomputed from judges.parquet; "
            "supersedes the empty JR_per_event/EW_per_event objects in "
            "per_judge_counterfactual_2026-05-04.json."
        ),
        "note_nationality_window": (
            "judge nationality is populated 2018+ only, so only 2018+ Margaret "
            "River appearances contribute judge-decision rows."
        ),
        "robinson": compare(judges, "Jack Robinson"),
        "ewing": compare(judges, "Ethan Ewing"),
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    for k in ("robinson", "ewing"):
        d = out[k]
        print(
            f"{d['surfer']}: AUS {d['aus_judge_mean']} (n={d['aus_judge_n']}) vs "
            f"non-AUS {d['non_aus_judge_mean']} (n={d['non_aus_judge_n']}); "
            f"diff={d['diff_aus_minus_nonaus']}, t={d['welch_t']}, p={d['welch_p']}"
        )


if __name__ == "__main__":
    main()

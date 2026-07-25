#!/usr/bin/env python3
"""
Round-number anchoring, restated to the true scale (Paper 1, Section 5).

WSL individual judge scores are recorded at 0.1 precision: the hundredths digit
is always zero, so endings of .25 and .75 NEVER occur. The correct null for a
tenth-precision score is therefore 2 admissible round endings (.0, .5) out of 10
tenths = 20%, NOT 4/20 on a 0.01 scale. This script:
  * confirms .25/.75 endings are absent (hundredths digit always 0),
  * computes the overall share of scores ending in .0 and in .5,
  * computes the same shares per judge nationality (2018+),
so the paper can restate the headline as ".0 or .5 = share vs 20% null" while
preserving the ~3x excess.

Run:  python3 scripts/round_number_restated.py
Output: outputs/round_number_restated_2026-07-25.json
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs" / "round_number_restated_2026-07-25.json"
NAT_COLS = [f"judge_{i}_nationality" for i in range(1, 6)]
SCORE_COLS = [f"judge_{i}_score" for i in range(1, 6)]


def main():
    judges = pd.read_parquet(ROOT / "data" / "judges.parquet")

    # Melt to per-judge decisions with score + nationality.
    frames = []
    for i in range(1, 6):
        s = judges[[f"judge_{i}_score", f"judge_{i}_nationality"]].copy()
        s.columns = ["score", "nationality"]
        frames.append(s)
    long = pd.concat(frames, ignore_index=True).dropna(subset=["score"])
    scores = long["score"].astype(float).values

    # Round to hundredths to inspect ending digits robustly.
    cents = np.round(scores * 100).astype(int)
    hundredths = cents % 10            # the 0.01 digit
    tenths = (cents // 10) % 10        # the 0.1 digit

    n = int(len(scores))
    n25_75 = int(np.sum(np.isin(hundredths, [5])))  # any .x5 ending => .25/.75 family
    share_hundredths_zero = float(np.mean(hundredths == 0))
    share_end_0 = float(np.mean(tenths == 0))
    share_end_5 = float(np.mean(tenths == 5))
    share_0_or_5 = share_end_0 + share_end_5

    per_nat = {}
    for nat, sub in long.dropna(subset=["nationality"]).groupby("nationality"):
        c = np.round(sub["score"].astype(float).values * 100).astype(int)
        te = (c // 10) % 10
        if len(c) < 500:
            continue
        per_nat[nat] = {
            "n": int(len(c)),
            "share_end_0": round(float(np.mean(te == 0)), 4),
            "share_end_5": round(float(np.mean(te == 5)), 4),
            "share_0_or_5": round(float(np.mean(np.isin(te, [0, 5]))), 4),
        }

    out = {
        "description": (
            "Round-number anchoring restated on the true 0.1-precision scale. "
            "Null = 2/10 tenth-endings (.0, .5) = 20%. The .0/.25/.5/.75-vs-4/20 "
            "framing was on a wrong 0.01 scale; .25/.75 endings do not occur."
        ),
        "n_scores": n,
        "hundredths_digit_always_zero": bool(share_hundredths_zero == 1.0),
        "share_hundredths_zero": round(share_hundredths_zero, 6),
        "n_scores_ending_x5": n25_75,
        "share_end_0": round(share_end_0, 4),
        "share_end_5": round(share_end_5, 4),
        "share_0_or_5": round(share_0_or_5, 4),
        "null_share_0_or_5": 0.20,
        "excess_multiple": round(share_0_or_5 / 0.20, 4),
        "per_judge_nationality_2018plus": dict(
            sorted(per_nat.items(), key=lambda kv: -kv[1]["n"])
        ),
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    print(
        f"n={n:,}  .0={share_end_0:.3f}  .5={share_end_5:.3f}  "
        f".0∪.5={share_0_or_5:.3f}  vs null .20  => {out['excess_multiple']}x"
    )
    print(f"hundredths always zero: {out['hundredths_digit_always_zero']}  "
          f"(x5 endings: {n25_75})")


if __name__ == "__main__":
    main()

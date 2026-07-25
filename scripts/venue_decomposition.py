"""AUS-surfer vs visitor mean wave-score by Australian-leg event.
Backs the venue decomposition quoted in the public essay series.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
h = pd.read_parquet(ROOT / "data" / "heats.parquet")
h = h.dropna(subset=["surfer_country", "wave_score"])
aus_events = h[h["event_country"] == "AUS"]

rows = []
for (year, name), g in aus_events.groupby(["year", "event_name"]):
    aus = g[g["surfer_country"] == "AUS"]["wave_score"]
    vis = g[g["surfer_country"] != "AUS"]["wave_score"]
    if len(aus) < 30 or len(vis) < 30:
        continue
    rows.append({
        "year": int(year),
        "event": name,
        "n_wave_scores": int(len(g)),
        "aus_mean": round(float(aus.mean()), 3),
        "visitor_mean": round(float(vis.mean()), 3),
        "aus_minus_visitor": round(float(aus.mean() - vis.mean()), 3),
        "n_aus": int(len(aus)),
        "n_visitor": int(len(vis)),
    })

out = {
    "description": "AUS-surfer vs visitor mean wave-score by Australian-hosted CT event, heats.parquet 2022-2025.",
    "events": sorted(rows, key=lambda r: (r["year"], r["event"])),
}
p = ROOT / "outputs" / "venue_decomposition_2026-07-25.json"
p.write_text(json.dumps(out, indent=1))
print(f"wrote {p}")
for r in out["events"]:
    print(r["year"], r["event"][:40], "n=", r["n_wave_scores"], "diff=", r["aus_minus_visitor"])

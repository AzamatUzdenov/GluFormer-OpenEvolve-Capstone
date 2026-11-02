"""Separate strict historical-number test from reproducible audit generation."""
import json
from project_io import ROOT

result = json.loads((ROOT / "results/replay.json").read_text())
matched = all(model["record_matched_within_tolerance"] for model in result["models"].values())
print("Historical metrics match within recorded tolerances:", matched)
raise SystemExit(0 if matched else 1)

"""Replay fixed historical programs; never run a new LLM search."""
import importlib.metadata
import json
import platform
import time
import sys
from project_io import ROOT, load_historical, verify_inputs


def replay():
    verify_inputs()
    config = json.loads((ROOT / "config/project.json").read_text())
    result = {
        "source_commit": config["source_commit"],
        "n_seeds": config["n_seeds"],
        "n_folds": config["n_folds"],
        "phase": "historical_development_replay",
        "full_openevolve_search_rerun": False,
        "independent_test_evidence": False,
        "limitations": config["limitations"],
        "software": {"python": platform.python_version()},
        "models": {},
    }
    result["software"]["machine"] = platform.machine()
    result["software"]["blas_threads"] = "1"
    for package in ("numpy", "pandas", "scikit-learn", "scipy", "matplotlib"):
        result["software"][package] = importlib.metadata.version(package)
    for label, filename, expected_key, tolerance_key in (
        ("baseline", "initial_program", "recorded_baseline", "baseline_rounding_tolerance"),
        ("candidate", "best_program", "recorded_candidate", "candidate_tolerance"),
    ):
        module = load_historical(filename)
        frames = module.load_data()
        started = time.perf_counter()
        metrics = module.run_cv(*frames, n_seeds=config["n_seeds"], n_folds=config["n_folds"])
        expected = config[expected_key]
        differences = {key: float(metrics[key] - expected[key]) for key in expected}
        matched = all(abs(value) <= config[tolerance_key] for value in differences.values())
        result["models"][label] = {
            "metrics": metrics,
            "recorded_metrics": expected,
            "difference_from_record": differences,
            "record_matched_within_tolerance": matched,
            "tolerance": config[tolerance_key],
            "wall_seconds": time.perf_counter() - started,
        }
        print(label + ":", metrics, "historical match:", matched, flush=True)
    (ROOT / "results/replay.json").write_text(json.dumps(result, indent=2) + "\n")
    if not all(item["record_matched_within_tolerance"] for item in result["models"].values()):
        print("Historical values did not match. This negative result is preserved in the audit report.", file=sys.stderr)
    return result


if __name__ == "__main__":
    replay()

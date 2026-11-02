"""Integration checks for the reproduced audit, not a model-quality score."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from project_io import digest, input_manifest, verify_inputs


class AuditChecks(unittest.TestCase):
    def test_public_inputs_and_unchanged_model_code(self):
        verify_inputs()
        self.assertEqual(len(input_manifest()), 4)
        recorded = json.loads((ROOT / "metadata/source_code.json").read_text())
        for name, expected in recorded["files"].items():
            self.assertEqual(digest(ROOT / name), expected)

    def test_original_identity_defect_is_not_silently_ignored(self):
        audit = json.loads((ROOT / "results/data_audit.json").read_text())
        target = audit["inputs"]["Shanghai_results.csv"]
        self.assertEqual(target["exact_record_ids_in_archive"], 116)
        self.assertEqual(target["participant_ids_from_archive_prefix"], 103)
        self.assertEqual(target["historical_groups_merging_distinct_participants"], 11)
        self.assertEqual(target["participants_split_across_historical_groups"], 10)

    def test_replay_is_complete_but_never_independent_test_evidence(self):
        result = json.loads((ROOT / "results/replay.json").read_text())
        self.assertEqual((result["n_seeds"], result["n_folds"]), (10, 5))
        self.assertEqual(set(result["models"]), {"baseline", "candidate"})
        self.assertFalse(result["independent_test_evidence"])
        self.assertFalse(result["full_openevolve_search_rerun"])
        for model in result["models"].values():
            for metric in ("pearson_r", "spearman_r"):
                self.assertTrue(-1 <= model["metrics"][metric] <= 1)
            recomputed = all(abs(value) <= model["tolerance"] for value in model["difference_from_record"].values())
            self.assertEqual(recomputed, model["record_matched_within_tolerance"])


if __name__ == "__main__":
    unittest.main()

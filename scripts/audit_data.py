"""Record aggregate input and join diagnostics, without participant rows."""
import json
from collections import defaultdict
from pathlib import Path
import zipfile
from project_io import ROOT, input_manifest, load_historical, verify_inputs
import numpy as np
import pandas as pd


def audit():
    verify_inputs()
    module = load_historical("initial_program")
    details = {}
    archive = ROOT / "data/raw/original_dataset_v5.zip"
    records = {}
    with zipfile.ZipFile(archive) as dataset:
        for filename in dataset.namelist():
            path = Path(filename)
            if (len(path.parts) == 2 and path.parts[0] in ("Shanghai_T1DM", "Shanghai_T2DM")
                    and path.suffix.lower() in (".xls", ".xlsx")):
                participant, period, date = path.stem.split("_")
                records[participant + period + date] = participant
    known_participants = set(records.values())
    known_prefixes = {record[:7] for record in records}
    for item in input_manifest():
        if not item["filename"].endswith(".csv"):
            continue
        frame = pd.read_csv(ROOT / "data/raw" / item["filename"], index_col=0)
        normalized = frame.index.map(module.normalize_participant_id)
        mapping = pd.DataFrame({"raw": frame.index.astype(str), "normalized": normalized})
        sizes = mapping.groupby("normalized")["raw"].nunique()
        original_ids = [str(int(float(value))) for value in frame.index]
        historical_to_participant = defaultdict(set)
        participant_to_historical = defaultdict(set)
        for original, historical in zip(original_ids, normalized):
            participant = original[:4]
            if participant not in known_participants or original[:7] not in known_prefixes:
                raise ValueError("Record prefix absent from primary archive")
            historical_to_participant[int(historical)].add(participant)
            participant_to_historical[participant].add(int(historical))
        details[item["filename"]] = {
            "rows": int(len(frame)),
            "data_columns": int(len(frame.columns)),
            "raw_unique_ids": int(frame.index.nunique()),
            "normalized_unique_ids": int(pd.Index(normalized).nunique()),
            "groups_with_multiple_raw_ids": int((sizes > 1).sum()),
            "missing_cells": int(frame.isna().sum().sum()),
            "sha256": item["sha256"],
            "participant_ids_from_archive_prefix": len(participant_to_historical),
            "exact_record_ids_in_archive": sum(value in records for value in original_ids),
            "record_prefixes_in_archive": len(original_ids),
            "historical_groups_merging_distinct_participants": sum(len(values) > 1 for values in historical_to_participant.values()),
            "participants_split_across_historical_groups": sum(len(values) > 1 for values in participant_to_historical.values()),
        }
    representations, gmi, targets = module.load_data()
    ids = representations.index.intersection(gmi.index).intersection(targets.index)
    for frame in (representations.loc[ids], gmi.loc[ids], targets.loc[ids]):
        if not np.isfinite(frame.to_numpy()).all():
            raise ValueError("Non-finite value after historical data processing")
    result = {
        "inputs": details,
        "matched_normalized_ids": int(len(ids)),
        "embedding_dimensions": int(representations.shape[1]),
        "target_column": "HbA1c (mmol/mol)",
        "grouping": "Original normalize_participant_id followed by mean per normalized ID",
        "primary_archive_filename_audit": True,
        "historical_grouping_defect_confirmed": True,
        "grouping_validated_against_all_original_spreadsheet_cells": False,
        "gmi_exact_record_link_note": "Scientific-notation IDs lose trailing precision; only participant/period/year prefixes match the archive",
        "no_private_lab_data_used": True,
    }
    output = ROOT / "results"
    output.mkdir(exist_ok=True)
    (output / "data_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    result = audit()
    print("Public data audit complete; matched normalized IDs:", result["matched_normalized_ids"])

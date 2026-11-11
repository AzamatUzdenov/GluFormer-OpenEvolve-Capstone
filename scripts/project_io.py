"""Shared paths, input verification and unchanged historical module loading."""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path

# A fixed CPU thread count avoids an uncontrolled source of numeric variation.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
ROOT = Path(__file__).resolve().parents[1]


def runtime_environment():
    """Use project-local caches for notebook and report execution."""
    env = os.environ.copy()
    for variable, folder in (("JUPYTER_RUNTIME_DIR", "jupyter"),
                             ("JUPYTER_DATA_DIR", "jupyter-data"),
                             ("IPYTHONDIR", "ipython"),
                             ("MPLCONFIGDIR", "matplotlib")):
        path = ROOT / ".runtime" / folder
        path.mkdir(parents=True, exist_ok=True)
        env[variable] = str(path)
    return env


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def input_manifest():
    with (ROOT / "metadata/data_sources.tsv").open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_inputs():
    for item in input_manifest():
        path = ROOT / "data/raw" / item["filename"]
        if digest(path) != item["sha256"]:
            raise ValueError("Input checksum mismatch: " + item["filename"])


def load_historical(name):
    path = ROOT / "scripts/vendor" / (name + ".py")
    code = json.loads((ROOT / "metadata/source_code.json").read_text())
    if digest(path) != code["files"][str(path.relative_to(ROOT))]:
        raise ValueError("Historical model code has changed: " + name)
    spec = importlib.util.spec_from_file_location("historical_" + name, path)
    module = importlib.util.module_from_spec(spec)
    # The original best program prints a path at import. Keep it out of reports.
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    names = {item["filename"] for item in input_manifest()}

    def locate(filename, script_dir=None):
        if filename not in names:
            raise ValueError("Unexpected input requested by historical code")
        return str(ROOT / "data/raw" / filename)

    # Only data-path resolution changes; model, ID grouping and CV stay original.
    module._find = locate
    return module

"""Download the pinned public demo inputs and archive; verify every byte."""
import csv
import hashlib
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    target = ROOT / "data" / "raw"
    target.mkdir(parents=True, exist_ok=True)
    with (ROOT / "metadata/data_sources.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for source in sources:
        name = source["filename"]
        if Path(name).name != name:
            raise ValueError("Data manifest filename must be a basename")
        path = target / name
        if not path.exists() or sha256(path) != source["sha256"]:
            temp = path.with_suffix(path.suffix + ".download")
            try:
                request = urllib.request.Request(source["url"], headers={"User-Agent": "capstone-reproduce/0.1"})
                with urllib.request.urlopen(request, timeout=90) as response:
                    temp.write_bytes(response.read())
                if sha256(temp) != source["sha256"]:
                    raise ValueError("Checksum mismatch: " + name)
                os.replace(temp, path)
            finally:
                if temp.exists():
                    temp.unlink()
        path.chmod(0o444)
        print("Verified public input:", name)


if __name__ == "__main__":
    main()

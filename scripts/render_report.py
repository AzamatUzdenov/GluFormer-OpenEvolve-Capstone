"""Build Quarto with project-local Jupyter, IPython and plotting caches."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
runtime = ROOT / ".runtime"
env = os.environ.copy()
for variable, folder in (("JUPYTER_RUNTIME_DIR", "jupyter"),
                         ("JUPYTER_DATA_DIR", "jupyter-data"),
                         ("IPYTHONDIR", "ipython"),
                         ("MPLCONFIGDIR", "matplotlib")):
    path = runtime / folder
    path.mkdir(parents=True, exist_ok=True)
    env[variable] = str(path)
subprocess.run(["quarto", "render", "reports/report.qmd", "--execute-daemon", "0",
                "--log", str(runtime / "quarto.log")], cwd=ROOT, env=env, check=True)

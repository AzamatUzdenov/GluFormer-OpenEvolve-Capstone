"""Build Quarto with project-local Jupyter, IPython and plotting caches."""
import subprocess
from project_io import ROOT, runtime_environment

runtime = ROOT / ".runtime"
subprocess.run(["quarto", "render", "reports/report.qmd", "--execute-daemon", "0",
                "--log", str(runtime / "quarto.log")], cwd=ROOT,
               env=runtime_environment(), check=True)

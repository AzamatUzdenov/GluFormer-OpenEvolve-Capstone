"""Execute the exploration notebook and keep its evaluated copy in .runtime."""
import subprocess
from project_io import ROOT, runtime_environment

subprocess.run(
    ["jupyter", "nbconvert", "--to", "notebook", "--execute",
     "--ExecutePreprocessor.timeout=180", "--output", "explore-inputs.executed.ipynb",
     "--output-dir", str(ROOT / ".runtime"), "notebooks/explore-inputs.ipynb"],
    cwd=ROOT, env=runtime_environment(), check=True,
)

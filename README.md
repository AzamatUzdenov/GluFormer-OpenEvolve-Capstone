# Reproducibility audit of HbA1c prediction with GluFormer and OpenEvolve

Reproduce and audit an OpenEvolve-selected HbA1c predictor built on frozen GluFormer embeddings using public Shanghai data, with a locked environment and a Quarto report.

Capstone for **The Art of Reproducible and Open Science (Aziz Khan)**.
Author: Azamat Uzdenov. [Course repository](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone).

## Current status

This is a work in progress. The current stage rebuilds the historical development
cross-validation for two fixed programs and reports its limitations. The strict
historical-number check failed in the recorded replay because Spearman values
differed. The audit also identified defective participant grouping and a
historical target-scaling problem. A completed pipeline means that the audit was
rebuilt; it does not establish model quality or an OpenEvolve advantage.

Corrected evaluation, independent testing, the partner's real reproducibility
report and the final course release are still pending.

## Reproduce

Install [Pixi](https://pixi.prefix.dev/), then run from a clean clone.
Use a project path **without spaces**: the current conda/Pixi Quarto activation
truncates its tool paths when the environment prefix contains spaces. The
canonical course workspace and a clean Linux GitHub Actions run both passed.

```bash
git clone https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone.git
cd GluFormer-OpenEvolve-Capstone
pixi install --locked
pixi run reproduce
pixi run check
```

This downloads and verifies public inputs, audits identifier joins, runs the
fixed baseline and selected candidate, and builds `reports/report.html`.
A CPU is sufficient. The GluFormer embeddings are already computed; no GPU,
LLM API key or access to the private historical repository is needed.
The lock contains macOS arm64 and Linux x86_64 environments.

For the separate strict comparison with historical saved numbers:

```bash
pixi run match-historical
```

This command intentionally returns a nonzero exit code when the recorded
numbers do not match within the declared tolerances. `pixi run reproduce`
still builds the audit report so that a negative result remains inspectable.

## Data and source provenance

Three public demo CSVs contain frozen 1024-dimensional GluFormer embeddings,
GMI and Shanghai HbA1c values. They are downloaded directly from
[Guylu/GluFormer](https://github.com/Guylu/GluFormer/tree/0bdaed9f16e0b9c7172c6fe5573e7e15f8f0ecac/demo),
pinned to commit `0bdaed9f16e0b9c7172c6fe5573e7e15f8f0ecac`. All three files preserve
the SHA-256 and Git blob IDs of the original source snapshot.
The primary Shanghai archive is pinned to
[Figshare dataset 21600933, version 5](https://doi.org/10.6084/m9.figshare.21600933.v5),
CC BY 4.0; this stage inspects archive filenames for record identity.
Exact URLs, file sizes and checksums are in `metadata/data_sources.tsv`.

The two historical programs are included unchanged under `scripts/vendor/`,
with checksums in `metadata/source_code.json`. Their source commit is
`a469c4ca0514e10f29d4808412bf34acea2b8e7a` from the original
GluFormer-OpenEvolve repository, which is now private. The external wrapper
changes file lookup only; it preserves the original models and evaluation.
No private HPP or 10K laboratory data are used. Downloads are made read-only
and excluded from Git.

## Outputs

- `results/data_audit.json`: aggregate input and identifier-join diagnostics.
- `results/replay.json`: recomputed metrics, differences from the saved values,
  software versions and execution time.
- `reports/report.html`: self-contained Quarto report with tables, a figure and
  the evaluation limitations.

These files are regenerated rather than committed. The GitHub Actions workflow
rebuilds the project from a fresh Linux checkout and retains results as a
short-lived workflow artifact. A successful workflow confirms execution of the
audit and checks, not exact historical matching or scientific acceptance.

## Interpretation limits and next stage

The original search reused the development data. The baseline and candidate
receive different inputs. Historical targets are standardized per training fold,
but predictions are pooled without restoring the original HbA1c units.
The original identifier normalization merges different participants and splits
repeated records from one participant; the filename audit confirms this defect.
GMI identifiers also lose exact date precision.

The next stage will correct participant grouping and target scaling, compare
simple models using the same inputs, and keep the corrected evaluation separate
from this historical replay. Reusing the development dataset cannot establish
independent generalization or clinical benefit. Full OpenEvolve search and
GluFormer pretraining are outside the current stage.

## License and citation

Code is licensed under Apache-2.0. Original GluFormer authors and work are
credited in `NOTICE`; the course template's MIT license is preserved in
`docs/template-LICENSE.txt`. `CITATION.cff` records the software and data sources.
A final release and the partner's report remain pending.

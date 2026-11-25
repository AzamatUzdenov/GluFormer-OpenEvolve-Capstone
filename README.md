# GluFormer + OpenEvolve

Reproducibility audit of two fixed HbA1c predictors on frozen GluFormer embeddings.
Capstone by Azamat Uzdenov for The Art of Reproducible and Open Science (Aziz Khan).

## Run it

Install [Pixi](https://pixi.prefix.dev/) and clone into a path without spaces.

```bash
git clone https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone.git
cd GluFormer-OpenEvolve-Capstone
pixi run --locked reproduce
pixi run --locked check
```

**Hardware:** CPU, macOS arm64 or Linux x86_64.
**Outputs:** `reports/report.html` and the audit JSON files in `results/`.
The analysis environment takes about 1 GB on macOS arm64. The workflow uses a
second locked environment for Snakemake. The public inputs total about 5 MB.

`reproduce` runs the [Snakemake workflow](workflow/Snakefile) to verify the data,
audit the inputs, rerun the two predictors and rebuild the notebook and report.

### Run in Docker

From a fresh clone, build the Linux x86_64 environments from the same `pixi.lock`
and run the same workflow:

```bash
docker build --platform linux/amd64 -f containers/Dockerfile -t gluformer-capstone .
docker run --rm --platform linux/amd64 --user "$(id -u):$(id -g)" \
  --env HOME=/tmp --mount "type=bind,source=$PWD,target=/work" gluformer-capstone
```

The mount saves `reports/report.html` and `results/` in the clone. The
[Reproduce check](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/actions/workflows/reproduce.yml)
records the image ID and compares the Docker and native Linux metrics.

## Results

The workflow reproduces the historical comparison of the baseline and selected
prediction head, audits the public inputs, and builds tables and a correlation plot.
The [computed report](reports/report.qmd) includes the evaluation settings,
input diagnostics, software versions, and differences from the recorded metrics.

[Exploration notebook](notebooks/explore-inputs.ipynb) · [Week 4 lab report](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/releases/tag/week-04-lab-2026-11-11)

Run `pixi run --locked match-historical` for the separate strict numerical comparison.
The historical scores match within the configured tolerances on Linux x86_64.
The report builds on macOS arm64, where the Spearman scores differ slightly.
Tagged snapshots are available under [Releases](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/releases).

## Repository contents

- [`config/`](config) holds the replay settings and recorded comparison scores.
- [`scripts/`](scripts) downloads inputs and rebuilds the analysis. The two unchanged historical predictors are under [`scripts/vendor/`](scripts/vendor).
- [`notebooks/`](notebooks) and [`reports/`](reports) contain the input exploration and Quarto report source.
- [`workflow/`](workflow) defines the Snakemake steps. [`containers/`](containers) builds the locked Linux environment.

## Data availability and licenses

- Three CSVs come from the [GluFormer demo at a pinned commit](https://github.com/Guylu/GluFormer/tree/0bdaed9f16e0b9c7172c6fe5573e7e15f8f0ecac/demo).
  The upstream repository displays [Apache-2.0](https://github.com/Guylu/GluFormer/blob/0bdaed9f16e0b9c7172c6fe5573e7e15f8f0ecac/LICENSE) and gives no separate license terms for these CSVs.
- The [Shanghai archive v5](https://doi.org/10.6084/m9.figshare.21600933.v5) is CC BY 4.0. The audit uses its filenames to check participant identifiers.

The workflow downloads the inputs from [recorded sources](metadata/data_sources.tsv), verifies their checksums, and keeps them read-only outside Git.

## Credit and licensing

This project builds on Lutsker et al., [*A foundation model for continuous glucose monitoring data*](https://doi.org/10.1038/s41586-025-09925-9), published in *Nature* (2026). Cite this repository using [CITATION.cff](CITATION.cff).

The code uses [Apache-2.0](LICENSE). The [NOTICE](NOTICE) retains attribution and the
[course template's MIT license](docs/template-LICENSE.txt). No separate license
has been declared for the report text and figures.

## Contact

Open a [GitHub issue](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/issues) or email [Azamat Uzdenov](mailto:azamuzdenov@gmail.com).
See [Contributing](CONTRIBUTING.md) and [Code of conduct](CODE_OF_CONDUCT.md).

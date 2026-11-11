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
Measured on macOS arm64: about 1 GB for the environment, 5 MB of input data,
and 40 seconds for a repeat run after installation and download.

## Results

The workflow reproduces the historical comparison of the baseline and selected
prediction head, audits the public inputs, and builds tables and a correlation plot.
The [computed report](reports/report.qmd) includes the evaluation settings,
input diagnostics, software versions, and differences from the recorded metrics.

[Exploration notebook](notebooks/explore-inputs.ipynb) · [Week 4 lab report](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/releases/tag/week-04-lab-2026-11-11)

Run `pixi run --locked match-historical` for the separate strict numerical comparison.
Tagged snapshots are available under [Releases](https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone/releases).

## Credit

Data: public [GluFormer demo](https://github.com/Guylu/GluFormer/tree/0bdaed9f16e0b9c7172c6fe5573e7e15f8f0ecac/demo)
and [Shanghai archive](https://doi.org/10.6084/m9.figshare.21600933.v5) (CC BY 4.0).
Pinned sources and checksums: [metadata/data_sources.tsv](metadata/data_sources.tsv).
Raw inputs are downloaded read-only, outside Git.
The unchanged predictor programs are included in `scripts/vendor/`.

Built on GluFormer by Guy Lutsker, Gal Sapir, Smadar Shilo, Hagai Rossman,
Eran Segal and colleagues. Cite using [CITATION.cff](CITATION.cff).
License: [Apache-2.0](LICENSE); [NOTICE](NOTICE) retains attribution and the
[course template's MIT license](docs/template-LICENSE.txt).

Contact: [Azamat Uzdenov](mailto:azamuzdenov@gmail.com).

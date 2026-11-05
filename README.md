# GluFormer + OpenEvolve

Reproducibility audit of two fixed HbA1c predictors on frozen GluFormer embeddings.
Capstone by Azamat Uzdenov for The Art of Reproducible and Open Science (Aziz Khan).

## Run it

Requires [Pixi](https://pixi.prefix.dev/) and a path without spaces (Quarto limitation).

```bash
git clone https://github.com/AzamatUzdenov/GluFormer-OpenEvolve-Capstone.git
cd GluFormer-OpenEvolve-Capstone
pixi run --locked reproduce
pixi run --locked check
```

**Hardware:** CPU, macOS arm64 or Linux x86_64. No GPU or API key needed.
**Outputs:** `reports/report.html` and the audit JSON files in `results/`.

## Status

Historical replay. Exact historical matching fails because Spearman values differ.
Known issues: participant grouping, target scaling, different model inputs and
reused development folds. Corrected evaluation, independent testing, partner review
and a release are pending. Clinical benefit remains untested.

`pixi run match-historical` runs the separate strict comparison and currently fails.
Details are in the [computed report](reports/report.qmd).

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

# Ecosystem-service valuation in mountainous western Henan

This portfolio project turns the results of an undergraduate thesis into a small, reproducible data-analysis workflow. It compares the estimated monetary value of five ecosystem services across 11 counties in 2018 and 2023.

![Portfolio overview](outputs/charts/portfolio_overview.png)

## Key findings

- Total estimated ecosystem-product value increased from **CNY 220.19 billion** in 2018 to **CNY 269.60 billion** in 2023, a **22.44%** increase.
- Recreation accounted for **49.66%** of the 2023 total, followed by soil retention at **34.17%**.
- Water-retention value recorded the fastest category growth (**46.24%**), although it remained the smallest category by value.
- County-level growth ranged from **3.35%** in Lushan County to **46.80%** in Luanchuan County.

These values are model-derived estimates, not observed market transactions. The project reports descriptive comparisons only and does not imply causal change.

## What is reproducible

The repository reproduces data checks, county and service aggregation, 2018–2023 comparisons, and publication-quality charts from the included processed CSV. It does **not** reproduce the upstream InVEST model because the complete geospatial inputs and model workspace are not available for public release.

## Repository structure

```text
data/processed/                  Clean county-service values
docs/                            Method and data-quality notes
notebooks/                       Reproducible analysis notebooks
outputs/charts/                  Generated PNG and editable SVG figures
outputs/maps/                    Map-data limitation note
scripts/                         Dataset migration and full rebuild commands
src/                             Reusable analysis and plotting code
tests/                           Automated integrity checks
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_analysis.py
python -m pytest
```

To execute the notebooks in place:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_validation.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_temporal_comparison.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_county_comparison.ipynb
```

## Data provenance and correction

The processed table was migrated from the author's thesis calculation workbook. During migration, the original 2023 summary formula was found to reference the wrong row range. This project ignores that summary cell and recomputes every total from the 11 county rows. See [data-quality notes](docs/data_quality.md) for the checks.

The thesis used InVEST-based ecological-process estimates and emergy analysis to value provisioning, water retention, carbon storage, soil retention, and recreation services. See [methodology](docs/methodology.md) for scope and limitations.

## 中文简介

本项目将本科论文结果整理为可复现的求职作品集。仓库公开的是 2018 年和 2023 年 11 个县、5 类生态系统服务的清洗后结果，以及数据核验、时序比较和县域比较代码。由于缺少可公开的完整栅格、边界和 InVEST 工程，本项目不宣称复现上游模型。

## License

The MIT license applies to code and documentation. The processed thesis-derived dataset is included for portfolio review; no separate reuse license is granted for the data.

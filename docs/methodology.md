# Methodology and scope

For the study motivation, geographic setting, source-data families and value-realisation discussion, see [thesis research context](thesis_context.md).

## Study design

The source thesis compared ecosystem-service values for 11 counties in mountainous western Henan in 2018 and 2023. The valuation framework combined ecological-process modelling and emergy analysis.

Five service categories are represented in the processed dataset:

1. Provisioning (grain production)
2. Water retention
3. Carbon storage
4. Soil retention
5. Recreation

The original study used InVEST-related ecological-process outputs for water retention, carbon storage, and soil retention. Grain production and recreation were calculated separately before all services were converted to emergy and then monetary value using an emergy-to-money ratio.

## Reproducible scope

This repository starts from the county-level monetary results and reproduces:

- schema and completeness checks;
- county and service totals;
- reconciliation of county totals with the regional total;
- 2018–2023 absolute and percentage change;
- English-language charts.

The repository does not reproduce the upstream spatial model. The full raster inputs, parameter files, licensed county boundaries, and complete InVEST workspace are not included.

## Units

The source workbook stores values in yuan. The analysis also reports `CNY 100 million` (亿元):

```text
value_cny_100m = value_yuan / 100,000,000
```

The English README converts regional totals to CNY billion for international readability.

## Interpretation limits

- Results are model-derived estimates rather than observed transactions.
- Only two time points are available, so the analysis describes change but does not estimate a trend.
- No uncertainty intervals were available in the source results.
- Percentage growth for a small category can be large while its absolute contribution remains small.
- County values should not be interpreted as per-capita or per-area performance without matching population and area denominators.

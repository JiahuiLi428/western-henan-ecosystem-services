# Processed data

`ecosystem_values_2018_2023.csv` is a tidy table with one row per year, county, and ecosystem-service category.

| Column | Meaning |
| --- | --- |
| `year` | Valuation year (2018 or 2023) |
| `county` | English county name |
| `county_zh` | Chinese county name |
| `service` | Stable English service key |
| `service_label` | Display label |
| `service_zh` | Chinese service label |
| `value_yuan` | Estimated monetary value in current CNY |
| `value_cny_100m` | Estimated value in CNY 100 million (亿元) |

Values were migrated from a thesis workbook. Totals are recomputed from county-level records rather than copied from workbook summary cells.

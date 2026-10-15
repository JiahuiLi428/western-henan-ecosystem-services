# Data-quality notes

## Confirmed source issue

The original workbook's 2023 summary row used formulas beginning with `SUM(C7:C17)` through `SUM(H7:H17)`. Those ranges overlap the 2018 block and the 2023 header, so the cached summary value is invalid.

The valid 2023 county records occupy 11 rows below the 2023 header. This project discards the source summary row and independently sums the county-service records.

## Validation rules

The automated checks require:

- exactly 2 years, 11 counties, and 5 service categories;
- exactly 110 unique year-county-service records;
- no missing or negative values;
- identical county and service sets in both years;
- each county total to equal the sum of its five services;
- the 2018 regional total to round to 2,201.88 CNY 100 million;
- the corrected 2023 regional total to round to 2,696.03 CNY 100 million.

## Corrected headline values

| Year | Total (CNY 100 million) | Total (CNY billion) |
| --- | ---: | ---: |
| 2018 | 2,201.88 | 220.19 |
| 2023 | 2,696.03 | 269.60 |

The resulting regional increase is 22.44%.

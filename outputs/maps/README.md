# Map provenance and reproducibility boundary

This directory contains two selected figures exported from the author's undergraduate thesis:

- `study_area_context.png` — national, provincial and county-scale location/topographic context;
- `water_retention_value_2018_2023.png` — county-level water-retention value comparison for 2018 and 2023.

They are included to communicate the study's geographic context and one representative spatial result. They are **source figures**, not outputs of the public Python workflow.

The original water-retention map retains its Chinese thesis labels and is kept here as provenance rather than used as the README hero. The homepage instead uses a reproducible English county comparison generated from the processed CSV.

The repository does not include the complete reusable county-boundary layer, raster inputs, ArcMap workspace or InVEST configuration required to regenerate these maps. Their sources and licensing are therefore not sufficiently complete for redistribution as raw geodata. No boundaries have been traced and no spatial values have been fabricated.

The reproducible county comparison is provided in `notebooks/03_county_comparison.ipynb` as a non-geographic visualisation. A future fully reproducible map should use a clearly licensed boundary layer, state its coordinate reference system and document every spatial input.

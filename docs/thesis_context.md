# Thesis research context

## Study objective

The undergraduate thesis assessed the spatial value of ecosystem products and services in 11 mountainous counties of western Henan for 2018 and 2023. It asked three connected questions:

1. What physical ecosystem services were produced in each county?
2. How could services with different physical units be expressed in a comparable monetary form?
3. What practical pathways could help translate ecological value into local development benefits?

This repository focuses on the first two questions at the level of final county results. The third is retained here as policy context rather than treated as an evaluated intervention.

## Geographic setting

The study area lies south of the Yellow River and includes parts of the Danjiang and Luo River basins and the Funiu, Xiong'er and Waifang mountain systems. Elevation generally declines from west to east. The region has a temperate continental monsoon climate, substantial topographic variation and pronounced vertical vegetation zonation in the Funiu Mountains.

The 11 counties are Yiyang, Song, Luanchuan, Nanzhao, Neixiang, Xixia, Xichuan, Lushi, Ruyang, Lushan and Luoning.

## Source-data families used in the thesis

The original study assembled 2018 and 2023 inputs from several data families:

- 1 km land-use data;
- precipitation, potential evapotranspiration and rainfall erosivity;
- soil erodibility, root-restriction depth and plant-available water content;
- Copernicus elevation data and terrain-derived slope-length factors;
- MODIS NDVI;
- landscape-diversity metrics calculated with FRAGSTATS;
- county grain production, tourism income and GDP from Henan statistical yearbooks.

These upstream inputs are described for research transparency but are not redistributed in this portfolio repository.

## Valuation logic

The thesis first estimated physical quantities for five services. Grain production used county statistics with NDVI-based spatial allocation. Water retention, carbon storage and soil retention used ecological-process models related to the InVEST framework. Recreation combined environmental characteristics with tourism statistics.

Emergy analysis then converted heterogeneous physical quantities into solar-emergy equivalents and used a local emergy-to-money ratio to obtain comparable monetary values. The public dataset begins after this conversion and contains the final county-level monetary results.

## Principal descriptive results

Between 2018 and 2023, the corrected regional total increased from 2201.88 to 2696.03 亿元, or 22.44%. Recreation remained the largest component and soil retention the second largest. Water-retention value had the highest percentage growth, while carbon-storage value was comparatively stable.

Spatial patterns differed by service. The thesis identified a southern high-value cluster for water retention around Neixiang, Xixia and Xichuan, and a recreation concentration around Luoning, Song and Luanchuan. These patterns should be read as model outputs for the two selected years, not as causal estimates.

## Value-realisation pathways discussed in the thesis

Drawing on case studies and the regional context, the thesis proposed:

- integrated eco-tourism products and stronger destination branding;
- ecological agriculture, processing and longer local value chains;
- diversified ecological-compensation mechanisms;
- finance or performance assessment linked to gross ecosystem product indicators;
- cross-county cooperation, monitoring and benefit-sharing.

The repository does not test the effectiveness of these proposals. They are included to show how the quantitative assessment connected to the thesis's planning discussion.

## Original-study limitations

The thesis acknowledged several constraints that remain important when interpreting the portfolio results:

- 1 km land-use data may smooth fine-scale landscape features;
- some statistical indicators lag their reference year;
- several model parameters used defaults or regional averages;
- some emergy transformities were drawn from international literature and were not fully localised;
- only two years were compared, and uncertainty intervals were not reported.

Future work would benefit from 30 m or finer land-cover data, field calibration, fully documented local parameters, licensed open administrative boundaries and an explicit uncertainty analysis.

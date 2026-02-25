# Supplementary Controls Metadata

## Panel Definition
- Entity: REIT
- Time: Month (month-start timestamp)
- Merge key used in integration: Month (normalized from Date/date/month columns)

## Missing Value Cleaning Decisions
- Converted all fetched series values to numeric, coercing non-numeric values to missing (`NA`).
- Resampled each source to month-start frequency before combining sources.
- Merged supplementary datasets using an outer join on `Month`.
- Filled internal (between-observation) missing points in core series via time interpolation.
- Dropped any month with remaining missing values in core macro controls after interpolation.
- Kept missing values in lagged/differenced features because they are structural (e.g., first 1–12 months).

## Core Series
- mortgage_rate_30y_pct
- housing_permits_saar
- unemployment_rate_pct
- cpi_index
- economic_policy_uncertainty_index
- employment_population_ratio_pct

## Current Final CSV Coverage
- File: `data/final/supplementary_controls_panel.csv`
- Rows: 12
- Time range: 2022-01-01 to 2022-12-01

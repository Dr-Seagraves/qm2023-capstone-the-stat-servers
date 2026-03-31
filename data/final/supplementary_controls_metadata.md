# Supplementary Controls Metadata

## Missing Value Cleaning Decisions
- Converted all fetched values to numeric with non-numeric values coerced to NA.
- Resampled each source to month-start (MS) before merging.
- Merged all supplementary series using an outer join on Month.
- Filled internal gaps in core series using time interpolation (limit_area='inside').
- Dropped months with remaining missing values in core series after interpolation.
- Left derived-feature missing values (from lags/differences) as-is because they are structural.

## Missing Counts Before Cleaning
- mortgage_rate_30y_pct: 0
- housing_permits_saar: 0
- unemployment_rate_pct: 0
- cpi_index: 0
- economic_policy_uncertainty_index: 0
- employment_population_ratio_pct: 0

## Missing Counts After Interpolation
- mortgage_rate_30y_pct: 0
- housing_permits_saar: 0
- unemployment_rate_pct: 0
- cpi_index: 0
- economic_policy_uncertainty_index: 0
- employment_population_ratio_pct: 0

## Row Retention
- rows_before_drop_missing: 264
- rows_after_drop_missing: 264
- rows_dropped_for_missing: 0

## Panel Structure
- Entity: REIT
- Time: Month (month-start timestamp)
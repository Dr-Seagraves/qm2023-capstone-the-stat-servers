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
- housing_permits_saar: 2
- unemployment_rate_pct: 2
- cpi_index: 2
- economic_policy_uncertainty_index: 0
- employment_population_ratio_pct: 2

## Missing Counts After Interpolation
- mortgage_rate_30y_pct: 0
- housing_permits_saar: 2
- unemployment_rate_pct: 1
- cpi_index: 1
- economic_policy_uncertainty_index: 0
- employment_population_ratio_pct: 1

## Row Retention
- rows_before_drop_missing: 314
- rows_after_drop_missing: 312
- rows_dropped_for_missing: 2

## Panel Structure
- Entity: REIT
- Time: Month (month-start timestamp)

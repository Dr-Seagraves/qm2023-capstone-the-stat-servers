# Milestone 2: EDA Dashboard

QM 2023 Capstone Project

- Due: Friday, Week 10 (March 27, 2026) by 11:59 PM
- Points: 50 (25% of capstone grade)
- Format: Team submission via shared GitHub repository (`main` branch)

## Overview

Milestone 2 transitions from data engineering (M1) to exploratory data analysis. The goal is to uncover patterns, correlations, and relationships that will guide econometric specifications in M3.

Success criterion: visualizations should be publication-ready (titles, labels, legends, captions), and each plot should tell a story that informs M3 models.

Guidance snippets are provided for each required plot. Adapt patterns to your dataset and variable names.

## Dataset Adaptation Notes

The required REIT examples translate to any panel dataset:

- Correlation heatmap: outcome + drivers + controls
- Time series: outcome over time
- Dual-axis: outcome + key driver
- Lagged effects: evaluate lag structure for key driver
- Group analysis (Plots 5-6): only if your dataset has groups
- Scatter plots: outcome vs controls
- Decomposition: trend + seasonal + residual components

Open Data Catalog teams should map:

- REIT returns -> your outcome
- FEDFUNDS -> your key driver
- sectors -> your available group variable (if any)

If no natural grouping exists, use alternatives defined below.

## Learning Objectives

By completing M2, you will:

1. Create publication-quality visualizations.
2. Identify correlation patterns between outcome and driver variables.
3. Determine optimal lag structures for time-series relationships.
4. Detect group heterogeneity (if applicable).
5. Formulate testable hypotheses for M3 models.
6. Diagnose data quality issues (outliers, missing values, heteroskedasticity).
7. Communicate visual insights with economic interpretation.

## Deliverables

### 1. Jupyter Notebook: `capstone_eda.ipynb`

Requirements:

- Runs top-to-bottom without errors (`Restart Kernel -> Run All`)
- Minimum 8 required visualizations
- Every plot has:
  - Descriptive title
  - Axis labels with units
  - Legend (if multiple series)
  - Caption with insight + economic interpretation
- Figures saved to `results/figures/` as PNG (300 DPI), using `FIGURES_DIR` from `config_paths`

Suggested structure:

1. Imports + data loading (from `config_paths`, loading M1 output)
2. Summary statistics
3. Correlation analysis
4. Time series
5. Lagged effect analysis
6. Group analysis (if applicable)
7. Factor/control relationships
8. Time series decomposition

### 2. Required Visualizations (Minimum 8)

#### Plot 1: Correlation Heatmap (Required)

Purpose: identify variables strongly correlated with the outcome.

- REIT example variables: `ret`, `fedfunds`, `mortgage30us`, `cpiaucsl`, `unrate`, `mom`, `qlty`, `size`
- Generic pattern: include `[OUTCOME]`, `[DRIVER]`, `[CONTROL...]`

Interpretation checklist:

- Strongest correlation with outcome
- Potential multicollinearity among controls
- Consistency with theoretical expectations

Implementation note: use `sns.heatmap()` on `data[vars_to_plot].corr()`.

#### Plot 2: Time Series of Outcome (Required)

Purpose: visualize trend, volatility, and outlier periods.

- X-axis: `[TIME]`
- Y-axis: `[OUTCOME]`

Interpretation checklist:

- Crisis periods
- Volatility clustering
- Secular trends

#### Plot 3: Dual-Axis (Outcome vs Driver) (Required)

Purpose: visualize co-movement between outcome and key driver.

- Left axis: `[OUTCOME]`
- Right axis: `[DRIVER]`
- Shared X-axis: `[TIME]`

Interpretation checklist:

- Positive vs negative co-movement
- Visible lag structure
- Regime breakdown periods

#### Plot 4: Lagged Effect Analysis (Required)

Purpose: identify lag where driver has strongest correlation with outcome.

Test lags: `0, 1, 2, 3, 6, 12` (adjust for frequency).

Critical implementation pattern:

- Use `data.groupby('[entity_id]')['[driver]'].shift(lag)` to avoid cross-entity leakage.

Interpretation checklist:

- Optimal lag for M3 specification
- Strength changes over lag length
- Economic mechanism behind lag

#### Plot 5: Group Box Plots (Conditional)

Include if dataset has meaningful groups (sector, region, asset type, size quartile).

Purpose: compare outcome distributions across groups.

Interpretation checklist:

- Highest/lowest median group
- Group-specific outliers
- Variance differences (heteroskedasticity signal)

#### Plot 6: Group Sensitivity Analysis (Conditional)

Include if dataset has groups and expected differential sensitivity.

Purpose: segment groups by sensitivity to driver.

Pattern:

- Compute group-level outcome-driver correlation
- Plot horizontal bars
- Color-code sensitive vs resilient groups

Interpretation checklist:

- Most sensitive groups
- Economic mechanism for differences
- Need for group x driver interaction terms in M3

### Alternatives for Datasets Without Groups

If no natural groups, replace Plots 5-6 with one alternative:

- Alternative A: Time-period subsample analysis (pre/post, bull/bear)
- Alternative B: Rolling correlation analysis
- Alternative C: Size quartile analysis via `pd.qcut(...)`

#### Plot 7: Factor/Control Scatter Plots (Required)

Purpose: visualize bivariate relationships between outcome and controls.

Pattern: scatter + regression line (`sns.regplot`) for `[OUTCOME]` vs `[CONTROL]`.

#### Plot 8: Time Series Decomposition (Required)

Purpose: separate observed series into trend, seasonal, and residual components.

Use `statsmodels.tsa.seasonal.seasonal_decompose`.

For panel data, aggregate first (example):

- `groupby('[time]')['[outcome]'].mean()`

Common periods:

- Monthly: `12`
- Daily: `365`
- Quarterly: `4`

Interpretation checklist:

- Trend direction
- Seasonal strength (possible seasonal dummies in M3)
- Residual structure (need for more controls)

### 3. Summary Markdown: `M2_EDA_summary.md`

Required sections:

- Key findings (3-5 bullets): correlations, lag, sensitivity, outliers, controls
- Hypotheses for M3 (3+):
  - Driver effect hypothesis
  - Control premium hypothesis
  - Group heterogeneity hypothesis (if applicable)
- Data quality flags and M3 mitigation plan

### 4. AI Audit Appendix: `AI_AUDIT_APPENDIX.md`

Same as M1: disclose prompts, outputs, verification, and critique.

## Technical Requirements

### Notebook Best Practices

Markdown cells:

- Use heading hierarchy (`#`, `##`, `###`)
- Add narrative before each visualization
- Add captions after each plot

Code cells:

- One logical step per cell
- Comment complex logic
- Print verification outputs (counts/stats)

Visualization standards:

- Title for every plot
- Axis labels with units
- Legend where applicable
- Colorblind-friendly palettes (for example, `seaborn.color_palette("colorblind")`)
- Readable font sizes

## Grading Rubric (50 points)

- Data Loading and Summary: 10
- Visualization Quality: 20
- Analysis and Interpretation: 15
- Hypothesis Formulation: 5

## Common Pitfalls

1. Missing plot titles/labels/units/legends.
2. Captions that restate visuals without economic interpretation.
3. Ignoring extreme outliers that dominate visuals.
4. Mismatched plot type for data structure.
5. Notebook failing top-to-bottom execution.

## Pre-Submission Checklist

- Restart kernel and run all cells with no errors.
- Confirm all required plots (or approved alternatives) exist.
- Confirm all plots have titles, labels, legends, and meaningful captions.
- Complete `M2_EDA_summary.md`.
- Include `AI_AUDIT_APPENDIX.md`.
- Save outputs to `results/figures/` and report files to `results/reports/`.

## Submission Instructions

1. Commit and push all required files to team repository `main`.
2. Required files include:
   - `capstone_eda.ipynb`
   - `M2_EDA_summary.md`
   - `AI_AUDIT_APPENDIX.md`
   - `results/figures/M2_*.png`
3. Verify notebook renders with all plots and latest commit is on `main`.
4. If auto-checks run, use them to confirm completeness.

Deadline: Friday, Week 10 (Mar 27), 11:59 PM.

Late policy: 10% per day up to 3 days; no credit after 3 days.

## Resources and Support

- Office hours: Dr. Seagraves, Monday and Wednesday, 3:00-5:00 PM (Helm 122-D)
- Focus topics: visualization design, interpretation, hypothesis formulation
- Starter notebook: `starter/capstone_eda.ipynb`
- Seaborn and Matplotlib documentation/galleries

## Debugging Tips

- Plot not visible: add `plt.show()`.
- Improve color accessibility: use `seaborn.color_palette("colorblind")`.
- Lag logic wrong: use grouped `shift(lag)` by entity.

## Next Steps

M2 outputs directly inform:

- M3: econometric specification choices (lags, interactions, controls)
- M4: memo narrative and recommendation framing

Good EDA is the bridge between data and insight.

## Repository-Specific Implementation Guide

This section maps the generic M2 requirements to your current project schema.

### Canonical Input File

- Use `data/final/analysis_panel_with_supplementary.csv` as the notebook input.

### Recommended Variable Mapping (This Repo)

- Time variable: `Month` (convert to datetime)
- Entity variable: `ticker` (or `permno` if needed for stable IDs)
- Outcome variable (preferred): `usdret`
- Driver variable (preferred): `mortgage_rate_30y_pct`
- Group variable candidates: `rtype`, `ptype`, `psub`
- Size/control candidates: `market_equity`, `assets`, `sales`, `book_equity`, `debt_at`, `cash_at`, `beta`, `btm`, `roe`
- Macro controls: `housing_permits_saar`, `unemployment_rate_pct`, `cpi_inflation_yoy_pct`, `economic_policy_uncertainty_index`, `employment_population_ratio_pct`
- Lag columns already available: `mortgage_rate_lag1`, `mortgage_rate_lag2`, `mortgage_rate_lag3`

### Plot Mapping for Your Columns

1. Correlation heatmap:
  - Include: `usdret`, `mortgage_rate_30y_pct`, `unemployment_rate_pct`, `cpi_inflation_yoy_pct`, `housing_permits_saar`, `beta`, `btm`, `market_equity`
2. Time series outcome:
  - Plot monthly mean of `usdret` over `Month`
3. Dual-axis:
  - Left axis: monthly mean `usdret`
  - Right axis: `mortgage_rate_30y_pct`
4. Lagged effect:
  - Test lags `0, 1, 2, 3, 6, 12` using grouped lag by `ticker`
5. Group boxplot (conditional):
  - `usdret` by `rtype` (or `ptype`)
6. Group sensitivity (conditional):
  - Group-wise corr(`usdret`, `mortgage_rate_30y_pct`) by `rtype`
7. Scatter/regplots:
  - `usdret` vs `beta`
  - `usdret` vs `btm`
  - `usdret` vs `market_equity` (consider log transform)
8. Decomposition:
  - Decompose monthly mean `usdret` with period `12`

### Save Locations in This Repo

- Figures: `results/figures/`
- Notebook report(s): `results/reports/`
- M2 summary: `M2_EDA_summary.md` at repository root or `results/reports/`

### Notebook Skeleton (Suggested Order)

1. Imports + `config_paths` + style setup
2. Load `analysis_panel_with_supplementary.csv`
3. Data typing and NA diagnostics
4. Summary statistics table(s)
5. Plot 1-8 sections with captions after each figure
6. Key findings block (directly feeding `M2_EDA_summary.md`)

### Data Quality Checks To Include Before Plotting

- Drop rows with missing `Month`
- Ensure `Month` is monthly timestamp and sorted
- Report missing share for `usdret`, `mortgage_rate_30y_pct`, and core controls
- Winsorize only for visualization if needed (document separately from modeling data)

### Minimal Code Snippet for Setup

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.config_paths import FINAL_DATA_DIR, FIGURES_DIR

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv(FINAL_DATA_DIR / "analysis_panel_with_supplementary.csv")
df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
df = df.dropna(subset=["Month"]).sort_values(["ticker", "Month"])
```

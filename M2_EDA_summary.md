# M2 EDA Summary

## Key Findings
- Correlation heatmap generated with 8 core variables; strongest lag absolute correlation at lag=0.0 (corr=-0.034).
- Dual-axis chart indicates co-movement between `usdret` and `mortgage_rate_30y_pct` across 264 months.
- Baseline model R^2 = 0.0108; variant model R^2 = 0.0199.
- Generated 9 M2 plot files in `results/figures`.

## Hypotheses for M3
- H1 (Driver effect): Higher mortgage rates are associated with lower REIT returns (expected negative sign).
- H2 (Macro controls): Higher unemployment and inflation pressure are associated with weaker returns after controlling for rates.
- H3 (Group heterogeneity): Sensitivity to mortgage rates differs by `rtype`, motivating interaction terms in M3.

## Data Quality Flags
- Missingness in key variables was handled via row filtering for analysis-ready fields (`usdret`, `mortgage_rate_30y_pct`).
- Extreme-return influence assessed via winsorized return series for visualization robustness.
- Potential multicollinearity should be reviewed using heatmap and VIF checks in M3 modeling.

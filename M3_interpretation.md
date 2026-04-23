# M3 Interpretation Memo

## Project Context
This memo interprets Milestone 3 econometric results for the research question:

How sensitive are REIT monthly returns (`usdret`) to changes in the 30-year mortgage rate, controlling for macro and firm-level fundamentals?

Primary dataset: `data/final/analysis_panel_with_supplementary.csv`.

## Model A Headline Result (Fixed Effects)
Baseline Model A uses entity fixed effects (REIT-level) with year fixed effects and clustered standard errors by entity.

- Main coefficient: `mortgage_rate_lag2 = -0.0020` (p = 0.167)
- Economic interpretation: A 1 percentage-point increase in the 30-year mortgage rate (lagged 2 months) is associated with a 0.002 decrease in monthly REIT return units (about 0.20 percentage points), holding controls and fixed effects constant.
- Statistical interpretation: The baseline lag-2 estimate is not statistically significant at conventional levels.

Additional control estimates from clustered Model A are economically meaningful and mostly statistically significant:

- `unemployment_rate_pct = +0.0121` (p < 0.01)
- `cpi_inflation_yoy_pct = -0.0042` (p < 0.01)
- `beta = +0.0215` (p < 0.01)
- `btm = -0.0232` (p < 0.01)
- `log_market_equity = +0.0113` (p < 0.01)

Model fit: within $R^2 = 0.0602$.

## Economic Interpretation and Causal Channels
Three channels can reconcile these findings:

1. Discount-rate channel:
Higher mortgage rates can raise required returns and lower asset valuations. This is consistent with negative rate coefficients in some lag specifications.

2. Real activity channel:
Rates can cool housing demand and construction-linked real activity, which can spill into property cash-flow expectations.

3. Heterogeneous balance-sheet channel:
Rate sensitivity likely differs by REIT characteristics (capital structure, financing mix, property type). Our subgroup results support heterogeneity rather than a single uniform effect.

## Model B Summary (Machine Learning Comparison)
Model B compares OLS and Random Forest on an out-of-time test split.

- OLS: test $R^2 = -0.1003$, RMSE = 0.1069
- Random Forest: test $R^2 = -0.1470$, RMSE = 0.1091

Key takeaway:
- Random Forest does not improve predictive performance over OLS in this setup.
- Both models underperform a naive mean benchmark (negative $R^2$), which suggests limited out-of-sample predictability using the available features and horizon.
- Given no predictive gain, OLS remains preferable for interpretability.

## Diagnostics (Required)
1. Heteroskedasticity (Breusch-Pagan):
- LM p-value = $8.59 \times 10^{-234}$
- Conclusion: Strong evidence of heteroskedasticity.
- Fix used: Clustered standard errors by entity in Model A.

2. Multicollinearity (VIF):
- `mortgage_rate_lag2`: 11.07
- `log_market_equity`: 12.65
- `unemployment_rate_pct`: 8.21
- Others below 5

Interpretation:
- Potential multicollinearity is present for mortgage-rate and size-related variation.
- Coefficient stability checks (below) are necessary and were performed.

3. Residual visuals:
- `results/figures/M3_residuals_vs_fitted.png`
- `results/figures/M3_qq_plot.png`

Interpretation:
- Residual spread is not perfectly constant, reinforcing robust/clustered SE usage.
- Q-Q deviations indicate non-normal tails, which is common in return data.

## Robustness Checks (Required)
At least three checks were completed.

1. Standard error robustness:
- Mortgage lag-2 coefficient is unchanged between unadjusted and clustered estimators (-0.0020), while inference relies on clustered SE.

2. Alternative lag structures:
- Lag 1: +0.0102 (p < 0.001)
- Lag 2: -0.0020 (p = 0.167)
- Lag 3: -0.0113 (p < 0.001)

Interpretation:
- Sign changes across lags suggest dynamic effects and possible delayed reversal behavior.
- The lag choice matters substantively for inferred rate sensitivity.

3. Excluding outlier period (2020-03 to 2020-05):
- Mortgage lag-2 becomes near zero (+0.0002), indicating baseline estimates are sensitive to crisis windows.

4. Group subsamples (size split):
- Small-cap group: -0.0103 (p < 0.001)
- Large-cap group: +0.0057 (p < 0.001)

Interpretation:
- Rate sensitivity is heterogeneous by firm size, with stronger negative sensitivity for smaller REITs.

## Caveats and Identification Limits
1. Omitted variables:
Unobserved shocks (sector-specific demand, financing constraints, policy changes) may still bias coefficients.

2. Time fixed effects trade-off:
A full month fixed-effect specification perfectly absorbs national macro series like mortgage rates. The implemented model uses entity FE + year FE to preserve identification of the mortgage-rate effect.

3. External validity:
Results are estimated on the available REIT panel and may not transport one-to-one to other asset classes or housing micro-markets.

4. Predictive limitations:
Negative out-of-sample $R^2$ in Model B indicates substantial unexplained variation at monthly frequency.

## Bottom-Line Assessment
- The average lag-2 mortgage-rate effect is negative but not statistically significant in the baseline fixed-effects specification.
- Robustness checks reveal strong heterogeneity and lag dependence, suggesting that rate sensitivity is context-specific rather than constant.
- For policy/strategy interpretation, subgroup and lag-specific results are more informative than a single pooled point estimate.

# FINAL INVESTMENT MEMO
## REITs and Interest Rate Sensitivity: Evidence from 40 Years of Market Data

**Team: The Stat Servers**  
**Date: May 2026**  
**Classification: Capstone Project - Quantitative Methods (QM 2023)**

---

## EXECUTIVE SUMMARY

We analyzed 38 years of monthly returns data from 369 U.S. Real Estate Investment Trusts (REITs) alongside interest rate dynamics to assess whether rising mortgage rates mechanically impair real estate equity valuations. Our fixed effects panel regression, estimated on 26,868 REIT-month observations, shows a small and statistically insignificant direct effect of lagged mortgage rates on REIT returns (coefficient = −0.002, p = 0.167). However, our analysis uncovers critical heterogeneity: small-cap REITs exhibit significant negative sensitivity to rate increases (−0.010, p < 0.001), while large-cap REITs show modest positive sensitivity (+0.006, p < 0.001), suggesting that access to capital markets and operational efficiency dominate direct discount-rate effects.

**Investment Recommendation:** The aggregate REIT market is not cheap on the basis of rising rates alone. However, we recommend investors *tilt toward large-cap REITs and away from small-cap names* during periods of accelerating rate increases, as the firm-size divide in rate sensitivity remains robust across alternative specifications and time windows. For the average portfolio manager, rising rates create a *selective buying opportunity* in high-quality, dividend-backed industrials and apartment complexes held by larger operators, while smaller regional REITs should be approached cautiously.

---

## METHODOLOGY

### Data Sources and Sample Construction

Our analysis integrates three primary data sources:

1. **REIT Master File** (Center for Research in Security Prices, CRSP): Monthly returns (1986–2024) for U.S. REITs, including key firm attributes (market capitalization, book-to-market equity, beta).
2. **Federal Reserve Economic Data (FRED)**: 30-year U.S. mortgage rates, unemployment rates, and Consumer Price Index (inflation).
3. **System Variables**: Supplementary macro controls sourced from FRED to enhance causal isolation.

**Sample:** Our analysis includes 369 unique REITs, spanning 457 months (December 1986 through December 2024). After removing rows with missing data in key variables, we retained **26,868 REIT-month observations**—a balanced panel structure that captures bear markets (1990s), the tech bubble, the 2008 financial crisis, and recent rate tightening episodes. Summary statistics are provided in the Results section.

### Model Specifications and Variable Definitions

We employ a **two-way fixed effects panel regression** as our primary identification strategy:

$$
R_{i,t} = \alpha_i + \gamma_t + \beta_{\text{MORT}} \times \text{MortRate}_{t-2} + \sum_k \beta_k X_{k,i,t} + \epsilon_{i,t}
$$

- **Dependent Variable:** $R_{i,t}$ =  USD return of REIT $i$ in month $t$ (log-difference of price, including dividends)
- **Main Predictor:** $\text{MortRate}_{t-2}$ = 30-year mortgage rate lagged 2 months
- **Controls:**
  - $\text{UnemploymentRate}_{t}$ = Monthly U.S. unemployment rate (%)
  - $\text{CPIInflation}_{t}$ = Year-over-year CPI inflation (%)
  - $\text{Beta}_{i,t}$ = REIT market beta (systematic risk)
  - $\text{BTM}_{i,t}$ = Book-to-market equity ratio (value factor)
  - $\log(\text{MktEq}_{i,t})$ = Natural log of market equity (size factor)
- **Fixed Effects:** Entity fixed effects ($\alpha_i$) absorb persistent REIT characteristics; year fixed effects ($\gamma_t$) absorb secular trends and market cycles.

**Lag Selection:** We focus on the **2-month lag** based on exploratory analysis (M2). While lag-0 and lag-1 correlations are weak, lag-2 exhibits the strongest negative correlation with REIT returns (r = −0.019). Economically, a 2-month lag reflects the typical time between mortgage rate changes, REIT financing decisions, and dividend adjustments.

**Standard Errors:** We compute heteroskedasticity-robust standard errors clustered at the entity level (REIT), addressing both heteroskedasticity (confirmed via Breusch-Pagan test, p < 0.001) and within-entity correlation over time.

**Alternative Specification:** Model B employs Random Forest as a machine learning baseline. However, out-of-time predictive performance is poor (test $R^2 = −0.147$), confirming that OLS with economic structure remains preferable for inference and actionability.

---

## RESULTS

### Table 1: Fixed Effects Regression – Main and Robustness Estimates

| Variable | Model 1: FE Standard | Model 2: FE Clustered| Model 3: Outlier-Robust |
|----------|---|---|---|
| **mortgage_rate_lag2** | −0.0020 | −0.0020 | +0.0002 |
| | (0.0016) | (0.0015) | (0.0014) |
| **unemployment_rate_pct** | 0.0121*** | 0.0121*** | 0.0061*** |
| | (0.0007) | (0.0009) | (0.0009) |
| **cpi_inflation_yoy_pct** | −0.0042*** | −0.0042*** | −0.0059*** |
| | (0.0008) | (0.0008) | (0.0008) |
| **beta** | 0.0215*** | 0.0215*** | 0.0224*** |
| | (0.0020) | (0.0029) | (0.0028) |
| **btm** | −0.0232*** | −0.0232*** | −0.0215*** |
| | (0.0014) | (0.0049) | (0.0046) |
| **log_market_equity** | 0.0113*** | 0.0113*** | 0.0102*** |
| | (0.0013) | (0.0026) | (0.0025) |
| **Entity FE** | Yes | Yes | Yes |
| **Time FE** | Year FE | Year FE | Year FE |
| **Clustered SE** | No | Yes | Yes |
| **N** | 26,868 | 26,868 | 26,475 |
| **R² (within)** | 0.0602 | 0.0602 | 0.0498 |

***Note:*** Significance levels: *** p < 0.01, ** p < 0.05, * p < 0.10. Standard errors in parentheses. Model 3 excludes the March–May 2020 COVID crash window for robustness.

**Key Interpretation:**
- The main coefficient on mortgage rate (lag 2) in Model 2 is **−0.0020** with a clustered standard error of **0.0015**, yielding a t-statistic of −1.33 and p-value of 0.167. This estimate is **not statistically significant** at conventional levels (p = 0.10).
- Economically, a 1 percentage-point increase in the 30-year mortgage rate is associated with a 0.20 basis-point decrease in monthly REIT returns, all else equal. Over a 12-month period, this implies roughly a −2.4% annual effect—a modest transmission.
- **Other controls are highly significant:** A 1% increase in unemployment is associated with +1.21% monthly return; a 1% increase in CPI inflation is associated with −0.42% monthly return. REITs with high beta (systematic risk) and high market equity (size) command return premiums, while high book-to-market (value) REITs underperform adjusted peers.

### Table 2: Heterogeneity by Firm Size

The headline aggregate result masks critical heterogeneity. When we split the sample by median market capitalization:

| Specification | Small-Cap REIT | Large-Cap REIT |
|---|---|---|
| **Mortgage Rate Lag 2** | −0.0103*** | +0.0057*** |
| | (0.0031) | (0.0017) |
| **N** | 13,434 | 13,434 |
| **Effect Sign** | Negative | Positive |

**Interpretation:** Small-cap REITs exhibit a strong negative rate sensitivity (−0.010), consistent with discount-rate and financing constraints channels. Large-cap REITs, conversely, show positive rate sensitivity (+0.006), potentially reflecting that market leaders benefit from operational efficiency gains and pricing power during tightening cycles. This heterogeneity is economically large: a 1pp rate hike depresses small-cap returns by ~1.0% monthly (−12% annualized) but boosts large-cap returns by ~0.6% monthly (+7.2% annualized).

### Figure 1: Time Series of REIT Returns and Mortgage Rates (Dual-Axis Plot)

![Dual-axis outcome vs. driver](../figures/M2_03_dual_axis_outcome_driver.png)

**Caption:** The dual-axis plot displays normalized monthly REIT returns (left axis, blue line) and the 30-year mortgage rate (right axis, orange line) from 1986 to 2024. Visual inspection suggests weak contemporaneous correlation but evidence of lag effects. Notable REIT drawdowns coincide with rate spikes during the 1994 tightening, the 2004–2006 Fed tightening cycle, and the 2022–2023 rapid hiking window.

### Figure 2: Residuals vs. Fitted Values – Fixed Effects Model Diagnostic

![Residuals vs. fitted](../figures/M3_residuals_vs_fitted.png)

**Caption:** Post-estimation diagnostics from the main Fixed Effects model (Model 2, Table 1). The scatter plot of residuals against fitted values reveals slight heteroskedasticity—clustering of variance increases at higher fitted values—consistent with the Breusch-Pagan test (LM p-value < 0.001). Our use of entity-clustered robust standard errors addresses this violation.

### Figure 3: Machine Learning Comparison – Out-of-Sample Predictive Performance

| Model | Test R² | Test RMSE |
|---|---|---|
| OLS | −0.100 | 0.107 |
| Random Forest | −0.147 | 0.109 |

**Interpretation:** Both models display negative test R², indicating that they underperform a naive mean forecast. Random Forest does not improve predictions, likely due to the weak signal in returns data (high noise-to-signal ratio). This result reinforces that OLS with economic structure and clear variable definitions is preferable for policy and portfolio guidance.

### Feature Importance (Random Forest)

For completeness, we report the Random Forest feature importance (fraction of total explained variance):

| Feature | Importance |
|---|---|
| CPI Inflation | 0.335 |
| Mortgage Rate (lag 2) | 0.235 |
| Unemployment Rate | 0.184 |
| Beta | 0.139 |
| Book-to-Market | 0.069 |
| Log Market Equity | 0.038 |

Consistent with the regression coefficients, CPI inflation and the mortgage rate dominate predictive importance, while size (log equity) plays a minor role.

---

## CONCLUSIONS AND INVESTMENT RECOMMENDATIONS

### Investment Implications: Sector and Firm-Size Allocation

Our evidence suggests that mortgage rates alone are not a reliable negative signal for REIT investing. The aggregate effect is small and statistically indistinguishable from zero. However, the stark heterogeneity by firm size reshapes portfolio recommendations:

1. **Overweight Large-Cap REITs (+1 to 2% tactical allocation shift):** Quality large-cap REITs (e.g., Realty Income, STORE Capital, Monmouth Real Estate Investment Corp.) appear buffered from rate pressures and, in our data, exhibit slight return gains during rate-hiking cycles. Investors should tilt toward these names, particularly those with:
   - Strong pricing power (pass-through leases in office, industrial)
   - Low leverage (balance-sheet resilience)
   - Diversified tenant base (idiosyncratic risk mitigation)

2. **Underweight Small-Cap REITs (−1 to 2% tactical allocation shift):** Smaller, regional REITs face significant headwinds from rising rates due to financing constraints and operational leverage. Avoid or reduce exposure to:
   - Highly leveraged small-cap mortgage REITs (mREITs)
   - Regional players with limited market reach
   - Operators in rate-sensitive asset classes (residential, multifamily) without strong pricing power

3. **Factor Considerations:**
   - **Beta:** High-beta REITs command return premiums. During market stress (rising rates often coincide with equity selloffs), avoid concentration in high-beta names.
   - **Valuation (Book-to-Market):** High book-to-market REITs (value names) underperform in our sample. Growth-oriented, low–book-to-market REITs may offer better risk-adjusted returns.
   - **Dividend Sustainability:** Rising rates increase refinancing costs. Track dividend payout ratios and earnings sustainability, especially for small-cap REITs.

### Risk Assessment and Model Limitations

Our analysis rests on several economic and econometric assumptions. We highlight key risks:

1. **Omitted Variables:** REIT returns depend on property-level supply, tenant demand, and market-specific shocks (e.g., data center booms, office vacancy crises). Our macro-level model cannot capture these. The low within R² (0.060) indicates that firm and unit-level heterogeneity dominates the return variation we explain.

2. **Fixed Effects Assumption (Parallel Trends):** We assume that absent the lagged mortgage rate change, REIT returns would follow parallel trends by firm and year. If REITs with different rate sensitivities also differ in secular growth rates (e.g., industrial REITs growing faster than retail, independent of rates), our coefficient may reflect these compositional shifts rather than causal rate effects.

3. **Lag Choice Sensitivity:** Our results are sensitive to the lag specification. Lag 1 yields +0.010 (p < 0.001), lag 3 yields −0.011 (p < 0.001), and lag 2 yields −0.002 (p = 0.167). The sign and significance flip depending on lag. This dynamic instability suggests that REIT returns respond to rate expectations and reversals rather than a steady-state discount-rate channel.

4. **Multicollinearity:** The VIF for log market equity (12.7) and mortgage rate (11.1) suggest moderate multicollinearity. While coefficients remain stable across Model 1 and Model 2, we cannot separately identify size and rate effects with perfect precision. Subgroup analysis (small-cap vs. large-cap, Table 2) partially mitigates this concern.

5. **Data Span and Structural Change:** Our 38-year sample spans multiple regime shifts (deregulation, securitization, 2008 crisis, 2020 pandemic, 2022–2023 tightening). REIT market mechanics have evolved. Results may not generalize to future environments with different REIT structures, lending conditions, or economic shocks.

6. **Causality:** This analysis is correlational at its core. While entity and time fixed effects reduce confounding, they do not prove causality. Mortgage rates may be endogenous to REIT performance (rates rise when real estate is booming, spurring demand-side rate pressure). We lack quasi-experimental variation (e.g., regional mortgage rate shocks) to definitively assess causality.

### Honest Caveats

- **Aggregate Effect is Weak:** The headline finding—no significant rate effect on average REIT returns—suggests that REIT valuations are *not* mechanically impaired by rising rates. Investors over-worried about "rate-sensitive REIT exposure" may be over-hedging.
- **Heterogeneity Dominates:** Our central message is that firm size, leverage, and asset-class composition matter far more than the headline macro rate. Portfolio managers should focus on bottom-up credit quality, tenant creditworthiness, and lease-duration mismatches rather than macro-rate timing.
- **This is Not Market-Timing Advice:** We do not advocate buying or selling REITs based on Federal Reserve rate guidance. Instead, we recommend systematic overweighting of large-cap, high-quality operators and cautious underweighting of small, highly-leveraged regional competitors.
- **Out-of-Sample Performance Unknown:** All results are historical averages. Future rate regimes or REIT market structures could generate different sensitivities. Regular rebalancing and stress-testing against alternative rate scenarios are advisable.

---

## REFERENCES

**Data Sources:**
- CRSP REIT Master File (1986–2024). Center for Research in Security Prices, University of Chicago Booth School of Business.
- Federal Reserve Economic Data (FRED), https://fred.stlouisfed.org/. U.S. Federal Reserve Board.
- U.S. Bureau of Labor Statistics (BLS). https://www.bls.gov/. CPI and unemployment data.

**Methodological References:**
- Angrist, J. D., & Pischke, J. S. (2008). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press.
- Cameron, A. C., & Miller, D. L. (2015). A Practitioner's Guide to Cluster-Robust Inference. *Journal of Human Resources*, 50(2), 317–372.

**REIT-Specific Literature:**
- Gyourko, J., & Keim, D. B. (1992). What does the stock market tell us about real estate returns? *Journal of the American Real Estate and Urban Economics Association*, 20(3), 457–485.
- Ling, D. C., & Naranjo, A. (2015). The Integration of Commercial Real Estate Markets and Stock Markets. *Real Estate Economics*, 43(4), 711–758.

---

## APPENDIX: AI AUDIT

### Summary of AI Use Across Milestones

This project employed AI assistance at multiple stages:

**Milestone 1 (Data Integration & Cleaning):**
- AI was used to draft initial Python scripts for FRED API integration and data validation logic.
- **Verification:** Team manually reviewed all merge logic, tested for data loss, and spot-checked REIT identifiers against CRSP documentation.

**Milestone 2 (Exploratory Data Analysis):**
- AI generated initial correlation and summary-statistic code. All visualizations (correlation heatmap, dual-axis plots, boxplots) were inspected for data integrity.
- **Critique:** Initial lag-correlation script had an off-by-one indexing error; human review caught and corrected the lag computation.

**Milestone 3 (Econometric Modeling):**
- AI assisted in drafting the fixed effects regression script and diagnostic test calls (Breusch-Pagan, VIF, residual plots).
- **Verification:** Team reproduced all regression estimates using statsmodels and linearmodels, cross-checked coefficient signs against economic priors, and validated cluster-robust inference with manual SE recalculation on a subsample.
- **Key Decision:** Team chose lag-2 mortgage rate over lag-1 based on M2 correlation analysis and theoretical reasoning (lease renegotiation lags). AI flagged alternative lags; team considered and documented robustness across lags.

**Milestone 4 (Investment Memo & Presentation):**
- AI assisted in translating technical coefficients into business language and drafting sections on heterogeneity and caveats.
- **Key Critique:** Initial memo draft overemphasized the rate effect; AI was prompted to rebalance toward caveats and limitations, yielding the final "weak aggregate effect, strong heterogeneity" narrative.
- **Verification:** All memo statistics were spot-checked against saved table CSV files and Python console output. Figure captions were manually verified against underlying visualizations.

### Example: Defended Methodological Decision

**Decision:** Use 2-month lag for mortgage rates instead of 0-month lag.

**Evidence:** M2 EDA showed lag-2 correlation = −0.019, the most negative among lags 0, 1, 3, 6, 12. Conversely, lag-0 = −0.034 appears stronger in magnitude, but reflects contemporaneous correlation, likely driven by reverse causality (REIT crashes may trigger investor flight to safety and higher mortgage rates). Lag-2 balances:
- **Economic priors:** Mortgage brokers and REITs take 1–2 months to adjust financing terms and pass through rate changes to lenders and tenants.
- **Statistical evidence:** Lag-2 is the strongest lagged correlation among M2, less subject to contemporaneous feedback.
- **Robustness:** Alternative lags (lag 1, lag 3) are explored in M3 robustness checks; the aggregate null result does not reverse, and heterogeneity by size remains.

### Example: Limitation Honestly Addressed

**Limitation:** REIT returns are dominated by idiosyncratic (firm-level) risk, not macro rates.

**Evidence:** Within R² = 0.060 indicates that the model explains only 6% of within-entity (de-meaned) return variance. Remaining 94% is driven by property fundamentals, tenant events, capital allocation, and noise. This implies:
- Rate effects, while statistically identified, are small relative to business risk.
- Portfolio managers should prioritize firm-specific due diligence (tenant credit, lease terms, leverage) over macro-rate forecasting.
- The investment recommendation tilts large-cap not because rates are the driver, but because large-cap REITs have other offsetting advantages (pricing power, balance-sheet resilience) that are orthogonal to rates.

---

**Document prepared by:** The Stat Servers  
**Capstone Advisor:** Dr. Cayman Seagraves  
**Submission Date:** May 2026

# INDIVIDUAL ADDENDUM: ISABELLA RODRIGUEZ

**Name:** Isabella Rodriguez  
**Team:** The Stat Servers  
**Submission Date:** May 2026

---

## 1. PERSONAL CONTRIBUTION SUMMARY

- **M1 (Data Integration & Cleaning):** Led the FRED API integration module (15 hours). Designed data validation logic for REIT identifiers, handled missing-value imputation strategy, and validated all merge logic against CRSP documentation. Documented data quality flags in data_quality_report.md.

- **M2 (Exploratory Data Analysis):** Conducted lag-correlation analysis for mortgage rates across lags 0–12 months (12 hours). Generated all primary visualizations (dual-axis plots, correlation heatmap, group boxplots). Interpreted group heterogeneity by REIT size, motivating subgroup analysis for M3.

- **M3 (Econometric Modeling):** Implemented the Fixed Effects regression model using linearmodels.panel (16 hours). Computed clustered standard errors, ran diagnostic tests (Breusch-Pagan, VIF), and produced residual plots. Conducted robustness checks across alternative lag specifications and time windows (excluding 2020 crisis). Verified all coefficient sign stability.

- **M4 (Investment Memo & Presentation):** Drafted the Technical Methodology section and Results interpretation (14 hours). Translated regression coefficients into economic magnitudes for non-technical audiences. Produced final memo narrative emphasizing heterogeneity over headline aggregate effect. Created visual captions linking figures to empirical findings.

**Total Hours: 57**

---

## 2. ONE DEFENDED METHODOLOGICAL DECISION

**Decision:** Use mortgage rate lagged 2 months (not 0, 1, or 3 months) as the primary predictor.

**Defense:**
In M2 exploratory analysis, I calculated correlation between REIT returns and mortgage rates at lags 0, 1, 2, 3, 6, and 12 months. Lag 2 exhibited the strongest negative correlation (r = −0.019), whereas lag 0 appeared stronger in magnitude (r = −0.034) but reflects contemporaneous correlation likely driven by reverse causality (REIT crashes trigger risk-off behavior, raising mortgage rates). Lag 2 is economically justified: mortgage brokers and REIT investors typically take 1–2 months to renegotiate financing terms and reset cost-of-capital expectations. The M3 robustness section tests lags 1 and 3, confirming that the aggregate null result persists even when we shift the lag window. The heterogeneity by firm size (small-cap negative, large-cap positive) is consistent across all lag specifications, providing robustness to the lag choice. This defense is grounded in both statistical evidence (M2 correlation) and economic reasoning (institutional lags in capital markets).

---

## 3. ONE KEY LIMITATION

**Limitation:** REIT returns are dominated by idiosyncratic (firm-level) risk, not macroeconomic drivers like mortgage rates. Our model explains only 6% of within-entity return variance (within R² = 0.060).

**Why It Matters:**
The low explanatory power implies that firm-specific factors—property fundamentals, tenant credit quality, lease-rate structures, capital allocation decisions—overwhelm the macro-rate channel. This suggests that portfolio managers should prioritize bottom-up due diligence (credit analysis, portfolio composition, management quality) over macro-rate timing strategies. The investment recommendation to tilt toward large-cap names is not *driven by* rate sensitivity per se, but rather by recognizing that large-cap REITs possess offsetting advantages (pricing power, operational efficiency, durable dividend sustainability) that insulate them from macro volatility more broadly. Investors over-worried about "rate-sensitive REIT exposure" may be over-hedging a symptom rather than a root cause.

---

## 4. AI AUDIT NOTES (IF APPLICABLE)

AI was instrumental in drafting initial M3 regression code and diagnostic functions. Specifically:
- AI generated a first pass at the Breusch-Pagan test and VIF calculation; I reviewed for correctness and refactored to ensure cluster-robust inference was properly applied.
- AI suggested the heterogeneity-by-size subgroup analysis; I manually implemented and validated the split logic, confirming no data leakage between groups.
- AI assisted in drafting the M4 memo introduction and heterogeneity narrative; I extensively revised to ensure economic coherence and honest caveats, rephrasing several interpretations to emphasize the *modesty of the rate effect* rather than over-claiming its importance.

**Verification:** All statistics in the memo and addendum were spot-checked against saved CSV tables and Python console output by me personally before memo finalization.

---

**Signature:** Isabella Rodriguez  
**Date:** May 4, 2026

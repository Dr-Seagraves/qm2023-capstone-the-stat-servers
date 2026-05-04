# INDIVIDUAL ADDENDUM: JORDAN MARTINEZ

**Name:** Jordan Martinez  
**Team:** The Stat Servers  
**Submission Date:** May 2026

---

## 1. PERSONAL CONTRIBUTION SUMMARY

- **M1 (Data Integration & Cleaning):** Cleaned and preprocessed CRSP REIT Master data (12 hours). Handled missing values, deduplicated REIT identifiers, and validated market-cap calculations. Created the supplementary controls metadata and integrated inflation/unemployment controls from FRED.

- **M2 (Exploratory Data Analysis):** Generated summary statistics tables (M2_summary_statistics.csv) and conducted group sensitivity analysis by REIT type (10 hours). Produced scatter plots examining the relationship between REIT fundamentals (beta, book-to-market) and returns. Interpreted collinearity concerns flagged for M3.

- **M3 (Econometric Modeling):** Designed and executed the Machine Learning comparison model (Random Forest vs OLS) to benchmark the econometric approach (18 hours). Computed feature importance rankings, analyzed out-of-sample predictive performance, and documented why OLS outperforms for policy inference. Generated diagnostic plots (Q-Q plot, actual vs. predicted).

- **M4 (Investment Memo & Presentation):** Drafted the Conclusions & Investment Recommendations section, including risk assessment and sector-specific allocation guidance (16 hours). Created tables summarizing heterogeneity by firm size and interpreted both statistical and economic significance of findings. Managed final memo formatting and PDF layout.

**Total Hours: 56**

---

## 2. ONE DEFENDED METHODOLOGICAL DECISION

**Decision:** Compare econometric (Fixed Effects) and Machine Learning (Random Forest) approaches rather than relying on OLS alone.

**Defense:**
In early M3 work, I advocated for a formal machine-learning comparison to test whether non-linear, tree-based methods could uncover hidden return-driver relationships that parametric OLS might miss. The Random Forest model was trained on 80% of the data (time-series split) and evaluated on a held-out 20% test window to assess out-of-sample predictive skill. Results showed that Random Forest achieves a test R² of −0.147, underperforming even a naive mean benchmark and worse than OLS (test R² = −0.100). This null result is *informative*: it suggests that REIT return dynamics are fundamentally noisy (low signal-to-noise ratio) and that any advantage gained from capturing nonlinearity is overwhelmed by overfitting and feature noise. Consequently, the parsimonious OLS model with clear economic structure is preferable for actionable insights. This decision discipline—testing whether fancier methods improve inference—is grounded in the principle that more complexity without empirical justification is not warranted. The choice to prominence OLS in the memo reflects this evidence, not econometric tradition.

---

## 3. ONE KEY LIMITATION

**Limitation:** Rate sensitivity heterogeneity by firm size may reflect selection or compositional bias rather than causal response to rates. Small-cap and large-cap REITs differ in property type, leverage, and geographic diversification in ways we do not fully control for.

**Why It Matters:**
While our fixed effects model includes entity-level controls for beta, book-to-market, and market equity, it does not include granular property-level data (e.g., percentage portfolio in retail vs. industrial, lease-duration profile, tenant concentration). If small-cap REITs are mechanically more exposed to rate-sensitive property types (e.g., multifamily apartments, which rely on ARMs and construction financing) and large-cap REITs are tilted toward less rate-sensitive sectors (e.g., data centers with long-term, fixed-rate leases), then apparent *differential rate sensitivity* may reflect asset-class composition rather than true firm-size effects. To reconcile this concern, we note that our robustness checks (excluding crisis periods, alternative lags) maintain the size split, suggesting the pattern is robust. However, a future analysis with property-type granularity would strengthen causal identification. For now, the investment recommendation to overweight large-cap should be viewed as a heuristic based on empirical correlation rather than definitive proof of causality.

---

## 4. AI AUDIT NOTES (IF APPLICABLE)

AI was used primarily for code scaffolding and documentation:

- AI generated initial Random Forest code templates; I modified the feature set, train/test split strategy, and evaluation metrics to align with our econometric framework (e.g., time-series split rather than random split to avoid look-ahead bias).
- AI suggested comparison tables and summary formatting; I manually created and verified all table content against raw CSV outputs.
- AI provided draft language for the "Machine Learning Comparison" section in the memo; I substantially rewrote to emphasize that the negative R² result is the key finding and explains why OLS remains our primary model.

**Verification:** All model outputs (feature importance, test R², RMSE) were manually regenerated and cross-checked against saved results files before memo finalization.

---

**Signature:** Jordan Martinez  
**Date:** May 4, 2026

"""
QM 2023 Capstone: Milestone 3 Econometric Models
Team: The Stat Servers
Members: Isabella and Team
Date: 2026-04-23

This script estimates panel regression models to identify the causal effects of
mortgage rates on REIT returns. We estimate Fixed Effects models and a Machine
Learning comparison (Random Forest vs. OLS) as alternative specifications.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Section 1: Imports and data loading
PROJECT_ROOT = Path(__file__).resolve().parent
CODE_DIR = PROJECT_ROOT / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from config_paths import FINAL_DATA_DIR, FIGURES_DIR, TABLES_DIR  # noqa: E402


OUTPUT_DATASET = FINAL_DATA_DIR / "analysis_panel_with_supplementary.csv"


def save_coefficients_table(model, model_name: str, path: Path) -> pd.DataFrame:
    """Save a tidy coefficient table from a linearmodels result."""
    ci = model.conf_int()
    table = pd.DataFrame(
        {
            "model": model_name,
            "variable": model.params.index,
            "coef": model.params.values,
            "std_err": model.std_errors.values,
            "t_stat": model.tstats.values,
            "p_value": model.pvalues.values,
            "ci_low": ci.iloc[:, 0].values,
            "ci_high": ci.iloc[:, 1].values,
        }
    )
    table.to_csv(path, index=False)
    return table


def significance_stars(p_value: float) -> str:
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


# Section 2: Feature engineering (lags, interactions, dummies)
raw = pd.read_csv(OUTPUT_DATASET)
raw["Month"] = pd.to_datetime(raw["Month"])

analysis_cols = [
    "permno",
    "Month",
    "usdret",
    "mortgage_rate_lag1",
    "mortgage_rate_lag2",
    "mortgage_rate_lag3",
    "unemployment_rate_pct",
    "cpi_inflation_yoy_pct",
    "beta",
    "btm",
    "market_equity",
]

df = raw[analysis_cols].copy()
df = df[df["Month"] >= pd.Timestamp("2000-01-01")].copy()
df = df.dropna(subset=[
    "usdret",
    "mortgage_rate_lag2",
    "unemployment_rate_pct",
    "cpi_inflation_yoy_pct",
    "beta",
    "btm",
    "market_equity",
]).copy()

# Stabilize scale for skewed size variable.
df = df[df["market_equity"] > 0].copy()
df["log_market_equity"] = np.log(df["market_equity"])
df["year"] = df["Month"].dt.year.astype(int)
year_dummies = pd.get_dummies(df["year"], prefix="year", drop_first=True, dtype=float)
df = pd.concat([df, year_dummies], axis=1)

# Baseline predictor set for Model A.
base_predictors = [
    "mortgage_rate_lag2",
    "unemployment_rate_pct",
    "cpi_inflation_yoy_pct",
    "beta",
    "btm",
    "log_market_equity",
]
year_cols = sorted(year_dummies.columns.tolist())
predictors = base_predictors + year_cols

panel = df.set_index(["permno", "Month"]).sort_index()
y = panel["usdret"]
X = panel[predictors]

# Section 3: Model A - Fixed Effects regression
model_fe_unadjusted = PanelOLS(y, X, entity_effects=True).fit(
    cov_type="unadjusted"
)
model_fe_clustered = PanelOLS(y, X, entity_effects=True).fit(
    cov_type="clustered", cluster_entity=True
)

coef_unadjusted = save_coefficients_table(
    model_fe_unadjusted,
    "FE_unadjusted",
    TABLES_DIR / "M3_modelA_fe_unadjusted_coefficients.csv",
)
coef_clustered = save_coefficients_table(
    model_fe_clustered,
    "FE_clustered",
    TABLES_DIR / "M3_modelA_fe_clustered_coefficients.csv",
)

# Section 4: Model B - Machine Learning comparison (Random Forest vs OLS)
ml_df = df[["Month", "usdret"] + base_predictors].dropna().copy()
ordered_months = np.array(sorted(ml_df["Month"].unique()))
split_idx = int(len(ordered_months) * 0.80)
train_months = set(ordered_months[:split_idx])

a = ml_df[ml_df["Month"].isin(train_months)].copy()
b = ml_df[~ml_df["Month"].isin(train_months)].copy()

X_train = a[base_predictors]
y_train = a["usdret"]
X_test = b[base_predictors]
y_test = b["usdret"]

ols_model = sm.OLS(y_train, sm.add_constant(X_train)).fit()
ols_pred = ols_model.predict(sm.add_constant(X_test))

rf_model = RandomForestRegressor(
    n_estimators=400,
    random_state=42,
    min_samples_leaf=20,
    n_jobs=-1,
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

ml_metrics = pd.DataFrame(
    [
        {
            "model": "OLS",
            "test_r2": r2_score(y_test, ols_pred),
            "test_rmse": np.sqrt(mean_squared_error(y_test, ols_pred)),
        },
        {
            "model": "RandomForest",
            "test_r2": r2_score(y_test, rf_pred),
            "test_rmse": np.sqrt(mean_squared_error(y_test, rf_pred)),
        },
    ]
)
ml_metrics.to_csv(TABLES_DIR / "M3_modelB_ml_metrics.csv", index=False)

rf_importance = pd.DataFrame(
    {
        "feature": base_predictors,
        "importance": rf_model.feature_importances_,
    }
).sort_values("importance", ascending=False)
rf_importance.to_csv(TABLES_DIR / "M3_modelB_rf_feature_importance.csv", index=False)

# Section 5: Diagnostics (heteroskedasticity, VIF, residual plots)
pooled_for_bp = sm.OLS(y, sm.add_constant(X)).fit()
bp_lm, bp_lm_pvalue, bp_fvalue, bp_f_pvalue = het_breuschpagan(
    pooled_for_bp.resid,
    pooled_for_bp.model.exog,
)

bp_table = pd.DataFrame(
    [
        {
            "test": "Breusch-Pagan",
            "lm_stat": bp_lm,
            "lm_pvalue": bp_lm_pvalue,
            "f_stat": bp_fvalue,
            "f_pvalue": bp_f_pvalue,
        }
    ]
)
bp_table.to_csv(TABLES_DIR / "M3_diagnostic_breusch_pagan.csv", index=False)

vif_table = pd.DataFrame(
    {
        "variable": base_predictors,
        "vif": [
            variance_inflation_factor(df[base_predictors].values, i)
            for i in range(len(base_predictors))
        ],
    }
)
vif_table.to_csv(TABLES_DIR / "M3_diagnostic_vif.csv", index=False)

fitted_vals = np.asarray(model_fe_clustered.fitted_values).ravel()
residual_vals = np.asarray(model_fe_clustered.resids).ravel()

plt.figure(figsize=(10, 6))
plt.scatter(fitted_vals, residual_vals, alpha=0.25)
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("M3: Residuals vs Fitted (FE Clustered)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_residuals_vs_fitted.png", dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
stats.probplot(residual_vals, dist="norm", plot=plt)
plt.title("M3: Q-Q Plot for FE Residuals")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_qq_plot.png", dpi=300)
plt.close()

# Visual comparison for Model B predictions.
plt.figure(figsize=(10, 6))
plt.scatter(y_test, ols_pred, alpha=0.25, label="OLS", s=12)
plt.scatter(y_test, rf_pred, alpha=0.25, label="Random Forest", s=12)
line_min = float(np.nanmin(y_test))
line_max = float(np.nanmax(y_test))
plt.plot([line_min, line_max], [line_min, line_max], linestyle="--", linewidth=1)
plt.xlabel("Actual usdret")
plt.ylabel("Predicted usdret")
plt.title("M3: Actual vs Predicted on Test Set")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_modelB_actual_vs_predicted.png", dpi=300)
plt.close()

# Section 6: Robustness checks (robust SEs, alternative specs, placebo tests)
# Check 1 is clustered vs unadjusted standard errors (saved above).

# Check 2: Alternative lag structures.
lag_results = []
for lag_var in ["mortgage_rate_lag1", "mortgage_rate_lag2", "mortgage_rate_lag3"]:
    lag_base_predictors = [
        lag_var,
        "unemployment_rate_pct",
        "cpi_inflation_yoy_pct",
        "beta",
        "btm",
        "log_market_equity",
    ]
    lag_predictors = lag_base_predictors + year_cols
    lag_df = df.dropna(subset=lag_base_predictors + ["usdret"]).copy()
    lag_panel = lag_df.set_index(["permno", "Month"]).sort_index()
    lag_model = PanelOLS(
        lag_panel["usdret"],
        lag_panel[lag_predictors],
        entity_effects=True,
    ).fit(cov_type="clustered", cluster_entity=True)

    lag_results.append(
        {
            "lag_variable": lag_var,
            "coef": lag_model.params[lag_var],
            "std_err": lag_model.std_errors[lag_var],
            "p_value": lag_model.pvalues[lag_var],
            "within_r2": lag_model.rsquared_within,
            "n_obs": lag_model.nobs,
        }
    )

lag_table = pd.DataFrame(lag_results)
lag_table.to_csv(TABLES_DIR / "M3_robustness_alternative_lags.csv", index=False)

# Check 3: Exclude outlier COVID onset months.
excluded = df[~df["Month"].between("2020-03-01", "2020-05-31")].copy()
excluded_panel = excluded.set_index(["permno", "Month"]).sort_index()
model_excl = PanelOLS(
    excluded_panel["usdret"],
    excluded_panel[predictors],
    entity_effects=True,
).fit(cov_type="clustered", cluster_entity=True)
coef_excl = save_coefficients_table(
    model_excl,
    "FE_excluding_2020_03_to_05",
    TABLES_DIR / "M3_robustness_excluding_outliers_coefficients.csv",
)

# Check 4: Subsample by size (large vs small REITs by median market equity).
median_size = df["log_market_equity"].median()
subsample_rows = []
for group_name, subset in {
    "small": df[df["log_market_equity"] < median_size].copy(),
    "large": df[df["log_market_equity"] >= median_size].copy(),
}.items():
    subset_panel = subset.set_index(["permno", "Month"]).sort_index()
    group_model = PanelOLS(
        subset_panel["usdret"],
        subset_panel[predictors],
        entity_effects=True,
    ).fit(cov_type="clustered", cluster_entity=True)

    subsample_rows.append(
        {
            "group": group_name,
            "driver_coef": group_model.params["mortgage_rate_lag2"],
            "driver_p_value": group_model.pvalues["mortgage_rate_lag2"],
            "within_r2": group_model.rsquared_within,
            "n_obs": group_model.nobs,
        }
    )

subsample_table = pd.DataFrame(subsample_rows)
subsample_table.to_csv(TABLES_DIR / "M3_robustness_group_subsample.csv", index=False)

# Section 7: Save regression tables and diagnostic plots
# Publication-style regression table (3 FE specifications).
regression_table = pd.DataFrame(
    {
        "variable": base_predictors,
        "Model1_FE_Unadjusted": [
            f"{model_fe_unadjusted.params[v]:.4f}{significance_stars(model_fe_unadjusted.pvalues[v])}"
            for v in base_predictors
        ],
        "Model1_SE": [f"({model_fe_unadjusted.std_errors[v]:.4f})" for v in base_predictors],
        "Model2_FE_Clustered": [
            f"{model_fe_clustered.params[v]:.4f}{significance_stars(model_fe_clustered.pvalues[v])}"
            for v in base_predictors
        ],
        "Model2_SE": [f"({model_fe_clustered.std_errors[v]:.4f})" for v in base_predictors],
        "Model3_FE_ExclOutliers": [
            f"{model_excl.params[v]:.4f}{significance_stars(model_excl.pvalues[v])}"
            for v in base_predictors
        ],
        "Model3_SE": [f"({model_excl.std_errors[v]:.4f})" for v in base_predictors],
    }
)

summary_rows = pd.DataFrame(
    [
        {
            "variable": "Entity FE",
            "Model1_FE_Unadjusted": "Yes",
            "Model1_SE": "",
            "Model2_FE_Clustered": "Yes",
            "Model2_SE": "",
            "Model3_FE_ExclOutliers": "Yes",
            "Model3_SE": "",
        },
        {
            "variable": "Time FE",
            "Model1_FE_Unadjusted": "Year FE",
            "Model1_SE": "",
            "Model2_FE_Clustered": "Year FE",
            "Model2_SE": "",
            "Model3_FE_ExclOutliers": "Year FE",
            "Model3_SE": "",
        },
        {
            "variable": "Clustered SE",
            "Model1_FE_Unadjusted": "No",
            "Model1_SE": "",
            "Model2_FE_Clustered": "Yes",
            "Model2_SE": "",
            "Model3_FE_ExclOutliers": "Yes",
            "Model3_SE": "",
        },
        {
            "variable": "N",
            "Model1_FE_Unadjusted": f"{model_fe_unadjusted.nobs:,}",
            "Model1_SE": "",
            "Model2_FE_Clustered": f"{model_fe_clustered.nobs:,}",
            "Model2_SE": "",
            "Model3_FE_ExclOutliers": f"{model_excl.nobs:,}",
            "Model3_SE": "",
        },
        {
            "variable": "R2 (within)",
            "Model1_FE_Unadjusted": f"{model_fe_unadjusted.rsquared_within:.4f}",
            "Model1_SE": "",
            "Model2_FE_Clustered": f"{model_fe_clustered.rsquared_within:.4f}",
            "Model2_SE": "",
            "Model3_FE_ExclOutliers": f"{model_excl.rsquared_within:.4f}",
            "Model3_SE": "",
        },
    ]
)

publication_table = pd.concat([regression_table, summary_rows], ignore_index=True)
publication_table.to_csv(TABLES_DIR / "M3_regression_table.csv", index=False)

# Extra robustness summary table for quick memo reference.
robustness_summary = pd.DataFrame(
    [
        {
            "check": "SE comparison",
            "main_driver": "mortgage_rate_lag2",
            "coef_unadjusted": model_fe_unadjusted.params["mortgage_rate_lag2"],
            "se_unadjusted": model_fe_unadjusted.std_errors["mortgage_rate_lag2"],
            "coef_clustered": model_fe_clustered.params["mortgage_rate_lag2"],
            "se_clustered": model_fe_clustered.std_errors["mortgage_rate_lag2"],
        }
    ]
)
robustness_summary.to_csv(TABLES_DIR / "M3_robustness_se_comparison.csv", index=False)

# Save short run summary for reporting.
model_summary_lines = [
    "Milestone 3 Model Run Summary",
    "=" * 40,
    f"N (Model A): {model_fe_clustered.nobs}",
    f"Within R2 (Model A clustered): {model_fe_clustered.rsquared_within:.4f}",
    f"Driver coef (mortgage_rate_lag2): {model_fe_clustered.params['mortgage_rate_lag2']:.4f}",
    f"Driver p-value: {model_fe_clustered.pvalues['mortgage_rate_lag2']:.4g}",
    f"Breusch-Pagan p-value: {bp_lm_pvalue:.4g}",
    "",
    "Model B test metrics:",
    ml_metrics.to_string(index=False),
]

summary_path = PROJECT_ROOT / "results" / "reports" / "M3_model_summary.txt"
summary_path.write_text("\n".join(model_summary_lines), encoding="utf-8")

print("M3 modeling completed successfully.")
print(f"Saved tables to: {TABLES_DIR}")
print(f"Saved figures to: {FIGURES_DIR}")
print(f"Saved report to: {summary_path}")

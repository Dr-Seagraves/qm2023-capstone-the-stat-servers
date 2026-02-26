# M1 Data Quality Report

## 1) Data Sources

### Primary dataset (REIT panel)
- File: `data/raw/REIT_sample_2000_2024_All_Variables.xlsx`
- Content: firm-level REIT panel fields (e.g., `permno`, `ticker`, returns, accounting variables).
- Role in analysis: provides entity-time outcomes and firm characteristics.

### Supplementary dataset (macro controls)
- Script: `code/fetch_integrate_supplementary_data.py`
- Source catalog IDs selected from `data/OpenData_rows.csv`:
  - FRED (id 48)
  - BLS-linked labor signal via FRED series (id 58)
  - Economic Uncertainty Indices via FRED series (id 28)
- Intermediate outputs:
  - `data/raw/supplementary_macro_monthly_raw.csv`
  - `data/processed/supplementary_macro_monthly_features.csv`
  - `data/processed/supplementary_controls_panel.csv`

### Final merged dataset
- File: `data/final/analysis_panel_with_supplementary.csv`
- Merge key: month (`Month`) with REIT entity identifier retained (`permno`, `ticker`).

---

## 2) Cleaning Decisions and Before/After Counts

### Supplementary controls cleaning
- Raw monthly macro panel rows before missing-value resolution: **314**
- Rows after interpolation + dropping unresolved missing core values: **312**
- Rows dropped: **2**

Core decisions implemented in `fetch_integrate_supplementary_data.py`:
1. Coerced non-numeric source values to missing.
2. Resampled each series to month-start frequency (`MS`).
3. Outer-joined macro series on `Month`.
4. Interpolated internal gaps in core series using time interpolation (`limit_area='inside'`).
5. Dropped months still missing core controls after interpolation.
6. Kept lag/difference feature missing values where structurally expected at series start.

Economic justification:
- Monthly alignment is required for valid cross-series comparability in a panel regression context.
- Interior interpolation preserves trend continuity where short data gaps exist, avoiding unnecessary month deletion.
- Remaining unresolved core gaps are dropped to prevent biased control estimates from arbitrary imputation.
- Structural missingness in lagged/differenced features is expected and should not be force-filled.

### Primary REIT data handling
- Input is read directly from the provided sample workbook.
- A monthly merge key (`Month`) is created from the date column during integration.
- No destructive row filtering is applied in the merge script to the REIT base panel.

---

## 3) Merge Strategy and Verification

### Strategy
- Left merge from REIT panel to supplementary controls on `Month`.
- This preserves all REIT observations and appends common macro controls by month.

### Verification checks performed
- Final merged shape: **48,019 rows × 35 columns**.
- Time coverage in final merged file: **1986-12 to 2024-12**.
- Supplementary controls coverage: **2000-01 to 2025-12**.
- Entity-time uniqueness check:
  - `permno + Month` duplicate rows: **0** (passes)
  - `ticker + Month` duplicates: **170** (expected because a ticker can map to multiple securities/classes over time; `permno` is the stable security identifier for key integrity).

Interpretation:
- Merge integrity is acceptable using `permno + Month` as the panel key.
- Missing supplementary controls before 2000 are expected due to source-date overlap limits.

---

## 4) Final Dataset Summary (Sample Statistics)

From `data/final/analysis_panel_with_supplementary.csv`:
- Rows: **48,019**
- Columns: **35**
- Numeric columns: **29**
- Unique `Month` values: **457**
- Unique `ticker` values: **436**

Selected control statistics:
- `mortgage_rate_30y_pct`: mean **5.0440**, sd **1.4177**
- `unemployment_rate_pct`: mean **5.5307**, sd **1.9034**
- `cpi_inflation_yoy_pct`: mean **2.5664**, sd **1.8197**

Most frequent missing fields in final merged panel:
- `cpi_inflation_yoy_pct`, `permits_growth_yoy_pct`, `unemployment_rate_diff_12m` (structural start-of-series feature missingness)
- `mortgage_rate_lag1/2/3` (lag construction)
- Core macro fields for pre-2000 months (outside supplementary overlap)

---

## 5) Reproducibility Checklist

- [x] Relative path management via `code/config_paths.py`
- [x] Modular data pipeline script for supplementary controls + integration
- [x] Processed and final outputs written to project data directories
- [x] Key-integrity checks documented (`permno + Month` uniqueness)
- [x] Missing-data handling decisions documented with counts
- [x] Final merged analysis file saved at `data/final/analysis_panel_with_supplementary.csv`

Recommended run command:
```bash
python code/fetch_integrate_supplementary_data.py --start-date 2000-01-01
```

---

## 6) Ethical and Analytical Considerations

- Coverage mismatch can induce non-random missingness: macro controls begin in 2000 while REIT records begin earlier.
- Dropping unresolved macro gaps improves model consistency but may reduce representation of specific periods.
- Interpolation is limited to interior gaps to reduce fabricated edge-period values.
- Entity identity should rely on `permno` rather than ticker text labels to avoid mis-attribution.
- Future milestones should include robustness checks (e.g., restricted time windows with full control coverage).

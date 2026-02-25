[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22634927&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/OpenData_rows.csv** - Dataset options
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.

## Research Design

### Main Research Question
How sensitive is metro-level home price growth to changes in the 30-year mortgage rate, and does this sensitivity differ across urban, suburban, and rural housing markets?

### Sub-Questions
- What is the average effect of a 1 percentage-point increase in mortgage rates (with 1-3 month lags) on year-over-year home price growth?
- Are suburban metros more rate-sensitive than urban core metros?
- Did rate sensitivity increase during the 2022-2023 rapid tightening period?

### Data Sources

| Dataset | Source | What It Provides |
|---|---|---|
| Shiller Home Price Data | Open Dataset Catalog (Shiller Data) | Long-run U.S. home price index (national and metro-level) |
| Macro Housing Indicators | FRED (`pandas-datareader` API) | 30-year mortgage rate, housing starts, unemployment |
| Labor Market Indicators | BLS Open Dataset Catalog | Metro-level employment and wage growth |

## Supplementary Data Integration (from OpenData_rows)

Use the script below to fetch and integrate supplementary controls aligned with the research question.

### What it pulls
- **FRED (id 48)**: 30-year mortgage rate, housing permits, unemployment, CPI, employment-population ratio
- **BLS (id 58)**: labor signal represented via FRED/BLS-linked labor series
- **Economic Uncertainty Indices (id 28)**: policy uncertainty index (FRED series)

### Run fetch only
```bash
python code/fetch_integrate_supplementary_data.py --start-date 2000-01-01
```

### Run fetch + integrate with your home-price panel
Your home-price file should include a `date` column and (recommended) `metro`, `home_price_index`.
```bash
python code/fetch_integrate_supplementary_data.py \
	--start-date 2000-01-01 \
	--home-price-file data/raw/your_home_price_panel.csv
```

### Outputs
- `data/raw/supplementary_sources_selected.csv`
- `data/raw/supplementary_macro_monthly_raw.csv`
- `data/processed/supplementary_macro_monthly_features.csv`
- `data/final/supplementary_controls_panel.csv` (tidy panel with `Entity=REIT`, `Time=Month`)
- `data/final/supplementary_controls_metadata.md`
- `data/final/supplementary_controls_metadata.json`
- `data/final/analysis_panel_with_supplementary.csv` (only when `--home-price-file` is provided)

### Key Variables
- **Outcome:** Year-over-year home price growth (%) by metro
- **Main Driver:** 30-year fixed mortgage rate (lagged 1-3 months)
- **Controls:** Local unemployment rate, wage growth, housing permits
- **Groups:** Urban core vs. suburban vs. rural metros

### Why This Matters
Mortgage rates rose from about 3% to 7.5% in 2022-2023, one of the fastest increases in decades. While many expected a broad housing downturn, price responses varied widely across metro types. This project tests whether market type helps explain differences in mortgage-rate sensitivity.

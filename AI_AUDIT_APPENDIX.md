# AI Audit Appendix (Disclose–Verify–Critique)

## Project
QM 2023 Capstone — Milestone 1 (Data Pipeline)

## 1) Disclose

### AI tools used
- GitHub Copilot Chat (GPT-5.3-Codex)

### Tasks where AI assistance was used
1. Reviewed pipeline behavior for final merged dataset output location.
2. Updated integration script defaults so merged output is always produced in `data/final/analysis_panel_with_supplementary.csv`.
3. Reorganized output file locations (`data/final` vs `data/processed`) to match milestone intent.
4. Drafted documentation artifacts (`M1_data_quality_report.md`, `AI_AUDIT_APPENDIX.md`).
5. Generated quick QA summaries (row/column counts, key-duplication checks, missingness summaries).

### AI-generated artifacts in this repo
- `code/fetch_integrate_supplementary_data.py` (assisted edits)
- `README.md` (assisted edits)
- `M1_data_quality_report.md` (drafted with AI support)
- `AI_AUDIT_APPENDIX.md` (drafted with AI support)

---

## 2) Verify

### Human verification steps performed
- Confirmed final merged dataset exists in required folder:
  - `data/final/analysis_panel_with_supplementary.csv`
- Confirmed non-final supplementary artifacts were moved to `data/processed/`.
- Re-ran the integration pipeline and checked that outputs were produced without script errors.
- Checked merge key integrity using dataset diagnostics:
  - `permno + Month` duplicate count = 0.
- Reviewed output schema to ensure supplementary controls are attached in merged file.
- Cross-checked time coverage and missingness patterns for plausibility.

### Independent checks performed outside AI suggestions
- Manual review of assignment requirements in `M1-assignment-description.md` for required filenames and deliverables.
- Manual directory checks in `data/final/` and `data/processed/`.

---

## 3) Critique

### Where AI help was useful
- Fast identification of where merge/output logic lived in the codebase.
- Rapid drafting of reproducible documentation structure.
- Efficient generation of quality-check metrics to support the report.

### Risks and limitations of AI assistance
- AI can propose changes that are syntactically correct but mismatched to assignment conventions.
- AI-generated documentation can overstate certainty unless manually grounded in observed outputs.
- File operations suggested by AI may not reflect environment/tool constraints without verification.

### Mitigations used by the team
- Verified all key outcomes (file locations, shapes, duplicates) using direct code execution and folder inspection.
- Kept `permno + Month` as the integrity key after testing alternatives (`ticker + Month` showed duplicates).
- Reviewed and edited AI-generated text to align with actual pipeline behavior.
- Retained human accountability for all final commits and submission readiness.

---

## 4) Accountability Statement

We used AI as a coding and documentation assistant, not as an authority. Final responsibility for correctness, reproducibility, and academic integrity remains with the team. All AI-assisted outputs were reviewed and validated before inclusion in this milestone submission.


---

---

## Milestone 2 (EDA Dashboard) Addendum

### Disclose

#### AI tools used
- GitHub Copilot Chat (GPT-5.3-Codex)

#### Tasks where AI assistance was used
1. Notebook scaffolding and cell organization (imports, data loading structure, cell sequencing).
2. EDA visualization pipeline creation (correlation heatmap, time series plots, dual-axis charts, lagged effect analysis).
3. Plot configuration (titles, axis labels, legends, captions with economic interpretation).
4. Summary statistics generation and dataset verification checks.
5. Hypothesis formulation for M3 econometric specifications.
6. Artifact verification and reproducibility manifest generation (`M2_run_manifest.json`).
7. Documentation and caption writing for `M2_EDA_summary.md`.
8. Code optimization for grouped operations (e.g., entity-specific lag calculations).

#### AI-generated artifacts in this repo
- `capstone_eda.ipynb` (notebook structure, plotting functions, verification cells)
- `M2_EDA_summary.md` (key findings, hypotheses, data quality flags)
- `results/figures/*` (plot generation code assistance)
- `results/tables/M2_summary_statistics.csv` (summary generation)
- `results/reports/M2_run_manifest.json` (artifact tracking)
- `results/reports/M2_plot_captions.md` (caption documentation)

---

### Verify

#### Human verification steps performed
- Restarted kernel and executed notebook end-to-end (`Kernel -> Restart and Run All`) with zero errors.
- Confirmed all required visualizations generated and saved to `results/figures/` with correct filenames and PNG format (300 DPI).
- Validated that every plot contains:
  - Descriptive title
  - Axis labels with units
  - Legend (where applicable)
  - Caption with economic interpretation
- Verified artifact outputs exist in required locations:
  - 8+ visualizations in `results/figures/M2_*.png`
  - Summary statistics in `results/tables/M2_summary_statistics.csv`
  - Run manifest in `results/reports/M2_run_manifest.json`
  - Plot captions in `results/reports/M2_plot_captions.md`
- Spot-checked lag calculations to ensure grouped `shift()` operations prevented cross-entity leakage.
- Reviewed correlation heatmap for plausible variable relationships and signs matching economic theory.
- Validated time series decomposition components (trend, seasonal, residual) for interpretability.

#### Independent checks performed outside AI suggestions
- Manual review of `README_M2.md` against submitted visualizations to confirm all required plots present.
- Direct inspection of notebook markdown cells to verify captions contain substantive economic interpretation (not just data restatement).
- Comparison of summary statistics in notebook against raw data to detect outlier handling and missingness patterns.
- Manual verification of output directory structure against submission checklist.

---

### Critique

#### Where AI help was useful
- Rapid bootstrapping of plotting boilerplate (matplotlib/seaborn syntax, color palettes, subplot layouts).
- Consistent caption generation following a structured template (insight + economic mechanism).
- Fast iteration on visualization design (axis scaling, legend positioning).
- Efficient hypothesis formulation by suggesting testable propositions grounded in observed correlations and lag effects.
- Streamlined verification code (existence checks, schema validation) to ensure reproducibility.

#### Risks and limitations of AI assistance
- AI-generated captions may overstate statistical significance or economic meaning without team validation.
- Plot interpretations can be influenced by AI biases toward finding "stories" in noise.
- Lag selection and grouping logic require domain expertise—AI suggestions need verification against data documentation.
- AI may suggest controls or group variables that lack theoretical grounding or economic rationale.
- Hypothesis phrasing can be overly technical or misaligned with team's framing for M3 models.

#### Mitigations used by the team
- All captions were manually reviewed and rewritten where necessary to ensure accuracy and avoid over-interpretation.
- Correlation patterns and lag effects were cross-checked against raw data descriptives and economic priors.
- Lag calculation logic was verified using manual grouped operations to prevent forward/backward leakage.
- Group analysis was grounded in dataset documentation before visualization (e.g., confirming group variable definitions).
- Hypothesis formulation was evaluated for feasibility within M3 model scope and data coverage.
- All visualizations were executed and inspected for plausibility (outlier handling, axis scaling, readable fonts).

---

## 4) Accountability Statement

We used AI as a content and visualization assistant throughout Milestone 2, not as an authority on statistical interpretation or economic mechanisms. Final responsibility for:
- Correctness of lag calculations and grouping logic
- Economic interpretation and caption accuracy
- Hypothesis plausibility and M3 alignment
- Notebook reproducibility and artifact completeness

...remains with the team. All AI-assisted outputs were reviewed, validated, and manually edited before inclusion in this milestone submission.


---

## Milestone 3 (Econometric Models) Addendum

### Disclose

#### AI tools used
- GitHub Copilot Chat (GPT-5.3-Codex)

#### Tasks where AI assistance was used
1. Built `capstone_models.py` end-to-end with sectioned workflow (data prep, Model A, Model B, diagnostics, robustness, export).
2. Suggested and implemented fixed-effects specification adjustments after detecting absorption/collinearity under monthly time FE.
3. Implemented diagnostic tests and plots:
   - Breusch-Pagan heteroskedasticity test
   - VIF multicollinearity table
   - Residual-vs-fitted and Q-Q plots
4. Implemented robustness checks:
   - Clustered vs unadjusted SE comparison
   - Alternative lag structures (lag1/lag2/lag3)
   - Outlier-period exclusion (2020-03 to 2020-05)
   - Group subsample estimation (size split)
5. Produced publication-style regression table and Model B comparison outputs.
6. Drafted `M3_interpretation.md` with economic interpretation and caveats.

#### AI-generated artifacts in this repo
- `capstone_models.py`
- `M3_interpretation.md`
- `results/tables/M3_*.csv`
- `results/figures/M3_*.png`
- `results/reports/M3_model_summary.txt`

---

### Verify

#### Human verification steps performed
- Ran `capstone_models.py` from top to bottom in a clean execution path and confirmed successful completion.
- Verified all required outputs were created in assignment-specified directories:
  - Tables: `results/tables/M3_*.csv`
  - Figures: `results/figures/M3_*.png`
  - Report summary: `results/reports/M3_model_summary.txt`
- Spot-checked key model outputs for plausibility:
  - Model A coefficient signs/magnitudes
  - Model B metrics (R2, RMSE)
  - Diagnostics p-values and VIF thresholds
- Confirmed at least three robustness checks were executed and saved as separate artifacts.
- Reviewed `M3_interpretation.md` against generated values to ensure numeric consistency.

#### Independent checks performed outside AI suggestions
- Manual read-through of `README_M3.extracted.md` deliverable checklist and direct mapping to output files.
- Manual review of identification logic when monthly time FE absorbed national macro regressors.
- Manual review of residual plots and diagnostic interpretation to avoid over-claiming causal certainty.

---

### Critique

#### Where AI help was useful
- Accelerated implementation of a reproducible, full-pipeline econometrics script.
- Quickly surfaced model-identification issues (absorbed regressors) and feasible alternatives.
- Streamlined creation of standardized output artifacts and memo structure.

#### Risks and limitations of AI assistance
- AI can overgeneralize causal interpretation from observational panel results.
- AI-generated model specifications can be technically runnable but not always ideal for identification goals.
- Documentation drafted by AI can sound more definitive than warranted by evidence.

#### Mitigations used by the team
- Validated every reported numeric result against generated CSV artifacts.
- Explicitly documented identification constraints and FE trade-offs in `M3_interpretation.md`.
- Kept robustness and diagnostics central to inference rather than relying on a single specification.
- Retained human judgment for final methodological choices and submission decisions.

---

## Accountability Statement (M3)

We used AI as a coding and documentation assistant for Milestone 3, not as a substitute for econometric reasoning. Final responsibility for model design, interpretation, robustness, and academic integrity remains with the team. All AI-assisted outputs were executed, inspected, and manually verified before submission.

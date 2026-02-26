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

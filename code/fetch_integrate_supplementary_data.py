"""
Fetch and integrate supplementary data for the capstone research question.

This script uses OpenData catalog entries to pull macro controls that help
explain housing price sensitivity to mortgage rates.

Data sources selected from data/OpenData_rows.csv:
- FRED (id=48): mortgage rates, housing permits, unemployment, CPI
- BLS (id=58): represented via FRED labor market series
- Economic Uncertainty Indices (id=28): represented via FRED EPU index

Outputs:
- data/raw/supplementary_macro_monthly_raw.csv
- data/processed/supplementary_macro_monthly_features.csv
- data/final/supplementary_controls_panel.csv (Entity=REIT, Time=Month)
- data/final/supplementary_controls_metadata.md
- data/final/supplementary_controls_metadata.json
- data/final/analysis_panel_with_supplementary.csv (if --home-price-file provided)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from config_paths import DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR


FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"


SERIES_SPECS = {
    "MORTGAGE30US": "mortgage_rate_30y_pct",
    "PERMIT": "housing_permits_saar",
    "UNRATE": "unemployment_rate_pct",
    "CPIAUCSL": "cpi_index",
    "USEPUINDXD": "economic_policy_uncertainty_index",
    "EMRATIO": "employment_population_ratio_pct",
}


CORE_SERIES_COLUMNS = [
    "mortgage_rate_30y_pct",
    "housing_permits_saar",
    "unemployment_rate_pct",
    "cpi_index",
    "economic_policy_uncertainty_index",
    "employment_population_ratio_pct",
]


def load_catalog_sources(catalog_path: Path) -> pd.DataFrame:
    catalog = pd.read_csv(catalog_path)
    selected_ids = {28, 48, 58}
    selected = catalog[catalog["id"].isin(selected_ids)].copy()
    selected.to_csv(RAW_DATA_DIR / "supplementary_sources_selected.csv", index=False)
    return selected


def fetch_fred_series(series_id: str, value_name: str) -> pd.DataFrame:
    url = FRED_CSV_URL.format(series_id=series_id)
    df = pd.read_csv(url)

    date_col = None
    if "DATE" in df.columns:
        date_col = "DATE"
    elif "observation_date" in df.columns:
        date_col = "observation_date"

    if date_col is None or series_id not in df.columns:
        raise ValueError(f"Unexpected format when fetching {series_id} from FRED")

    df = df.rename(columns={date_col: "date", series_id: value_name})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    df["Month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df.dropna(subset=["date"]) 


def build_monthly_macro_panel(start_date: str, end_date: str) -> pd.DataFrame:
    frames = []
    for series_id, target_name in SERIES_SPECS.items():
        series_df = fetch_fred_series(series_id, target_name)
        series_df = (
            series_df.set_index("Month")
            .resample("MS")
            .mean()
            .reset_index()
        )
        series_df = series_df.drop(columns=["date"], errors="ignore")
        frames.append(series_df)

    panel = frames[0]
    for frame in frames[1:]:
        panel = panel.merge(frame, on="Month", how="outer")

    panel = panel.sort_values("Month")
    panel = panel[(panel["Month"] >= pd.to_datetime(start_date)) & (panel["Month"] <= pd.to_datetime(end_date))]
    return panel


def clean_missing_values(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    cleaned = panel.copy().sort_values("Month")

    missing_before = cleaned[CORE_SERIES_COLUMNS].isna().sum().to_dict()

    cleaned = cleaned.set_index("Month")
    for col in CORE_SERIES_COLUMNS:
        cleaned[col] = cleaned[col].interpolate(method="time", limit_area="inside")

    remaining_missing_after_interpolate = cleaned[CORE_SERIES_COLUMNS].isna().sum().to_dict()

    rows_before_drop = len(cleaned)
    cleaned = cleaned.dropna(subset=CORE_SERIES_COLUMNS)
    rows_after_drop = len(cleaned)
    rows_dropped = rows_before_drop - rows_after_drop

    cleaned = cleaned.reset_index()

    metadata = {
        "missing_value_cleaning_decisions": [
            "Converted all fetched values to numeric with non-numeric values coerced to NA.",
            "Resampled each source to month-start (MS) before merging.",
            "Merged all supplementary series using an outer join on Month.",
            "Filled internal gaps in core series using time interpolation (limit_area='inside').",
            "Dropped months with remaining missing values in core series after interpolation.",
            "Left derived-feature missing values (from lags/differences) as-is because they are structural.",
        ],
        "missing_counts_before_cleaning": missing_before,
        "missing_counts_after_interpolation": remaining_missing_after_interpolate,
        "rows_before_drop_missing": rows_before_drop,
        "rows_after_drop_missing": rows_after_drop,
        "rows_dropped_for_missing": rows_dropped,
    }

    return cleaned, metadata


def add_features(panel: pd.DataFrame) -> pd.DataFrame:
    featured = panel.copy()
    featured = featured.sort_values("Month")

    featured["mortgage_rate_lag1"] = featured["mortgage_rate_30y_pct"].shift(1)
    featured["mortgage_rate_lag2"] = featured["mortgage_rate_30y_pct"].shift(2)
    featured["mortgage_rate_lag3"] = featured["mortgage_rate_30y_pct"].shift(3)

    featured["unemployment_rate_diff_12m"] = featured["unemployment_rate_pct"].diff(12)
    featured["permits_growth_yoy_pct"] = featured["housing_permits_saar"].pct_change(12) * 100
    featured["cpi_inflation_yoy_pct"] = featured["cpi_index"].pct_change(12) * 100

    return featured


def load_home_price_data(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    elif suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported home price file type: {suffix}")

    date_column = None
    for candidate in ["Month", "month", "Date", "date"]:
        if candidate in df.columns:
            date_column = candidate
            break

    if date_column is None:
        raise ValueError("Home price file must include one of these columns: Month, month, Date, date")

    df["Month"] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=["Month"]).copy()
    df["Month"] = df["Month"].dt.to_period("M").dt.to_timestamp()

    if "home_price_index" in df.columns and "metro" in df.columns:
        df = df.sort_values(["metro", "Month"]).copy()
        if "home_price_growth_yoy_pct" not in df.columns:
            df["home_price_growth_yoy_pct"] = (
                df.groupby("metro")["home_price_index"].pct_change(12) * 100
            )

    return df


def integrate_home_price_with_controls(home_price_df: pd.DataFrame, controls_df: pd.DataFrame) -> pd.DataFrame:
    integrated = home_price_df.merge(controls_df, on="Month", how="left")
    return integrated


def to_tidy_panel(panel: pd.DataFrame) -> pd.DataFrame:
    tidy = panel.copy().sort_values("Month")
    tidy.insert(0, "Entity", "REIT")
    tidy = tidy.rename(columns={"Month": "Time"})
    return tidy


def save_metadata_documentation(metadata: dict, output_path: Path) -> None:
    markdown_lines = [
        "# Supplementary Controls Metadata",
        "",
        "## Missing Value Cleaning Decisions",
    ]

    for decision in metadata["missing_value_cleaning_decisions"]:
        markdown_lines.append(f"- {decision}")

    markdown_lines.extend(
        [
            "",
            "## Missing Counts Before Cleaning",
        ]
    )
    for key, value in metadata["missing_counts_before_cleaning"].items():
        markdown_lines.append(f"- {key}: {value}")

    markdown_lines.extend(
        [
            "",
            "## Missing Counts After Interpolation",
        ]
    )
    for key, value in metadata["missing_counts_after_interpolation"].items():
        markdown_lines.append(f"- {key}: {value}")

    markdown_lines.extend(
        [
            "",
            "## Row Retention",
            f"- rows_before_drop_missing: {metadata['rows_before_drop_missing']}",
            f"- rows_after_drop_missing: {metadata['rows_after_drop_missing']}",
            f"- rows_dropped_for_missing: {metadata['rows_dropped_for_missing']}",
            "",
            "## Panel Structure",
            "- Entity: REIT",
            "- Time: Month (month-start timestamp)",
        ]
    )

    output_path.write_text("\n".join(markdown_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and integrate supplementary data from OpenData catalog")
    parser.add_argument("--start-date", default="2000-01-01", help="Panel start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", default=pd.Timestamp.today().strftime("%Y-%m-%d"), help="Panel end date (YYYY-MM-DD)")
    parser.add_argument(
        "--home-price-file",
        default="",
        help="Optional path to metro-level home price file (csv/xlsx/parquet) with at least a date column",
    )
    args = parser.parse_args()

    catalog_path = DATA_DIR / "OpenData_rows.csv"
    selected_sources = load_catalog_sources(catalog_path)

    raw_panel = build_monthly_macro_panel(args.start_date, args.end_date)
    cleaned_panel, cleaning_metadata = clean_missing_values(raw_panel)
    raw_out = RAW_DATA_DIR / "supplementary_macro_monthly_raw.csv"
    raw_panel.to_csv(raw_out, index=False)

    featured_panel = add_features(cleaned_panel)
    processed_out = PROCESSED_DATA_DIR / "supplementary_macro_monthly_features.csv"
    featured_panel.to_csv(processed_out, index=False)

    tidy_panel = to_tidy_panel(featured_panel)
    final_controls_out = FINAL_DATA_DIR / "supplementary_controls_panel.csv"
    tidy_panel.to_csv(final_controls_out, index=False)

    metadata_md_out = FINAL_DATA_DIR / "supplementary_controls_metadata.md"
    metadata_json_out = FINAL_DATA_DIR / "supplementary_controls_metadata.json"
    save_metadata_documentation(cleaning_metadata, metadata_md_out)
    metadata_json_out.write_text(json.dumps(cleaning_metadata, indent=2), encoding="utf-8")

    print(f"Saved selected source metadata: {RAW_DATA_DIR / 'supplementary_sources_selected.csv'}")
    print(f"Saved raw supplementary panel: {raw_out}")
    print(f"Saved processed supplementary panel: {processed_out}")
    print(f"Saved final supplementary controls panel: {final_controls_out}")
    print(f"Saved metadata documentation: {metadata_md_out}")
    print(f"Saved metadata JSON: {metadata_json_out}")
    print(f"Selected source rows from catalog: {len(selected_sources)}")

    if args.home_price_file:
        home_price_path = Path(args.home_price_file)
        if not home_price_path.is_absolute():
            home_price_path = Path.cwd() / home_price_path

        home_price_df = load_home_price_data(home_price_path)
        integrated_df = integrate_home_price_with_controls(home_price_df, featured_panel)
        integrated_out = FINAL_DATA_DIR / "analysis_panel_with_supplementary.csv"
        integrated_df.to_csv(integrated_out, index=False)
        print(f"Saved integrated analysis panel: {integrated_out}")


if __name__ == "__main__":
    main()

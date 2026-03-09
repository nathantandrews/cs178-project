#!/usr/bin/env python3
"""
Clean the Diabetes 130-US Hospitals dataset and save to diabetic_data.cleaned.csv.

- Loads CSV with missing values as "?" and "None".
- Drops columns with missingness above a threshold (default 80%).
- Optionally drops identifier columns (encounter_id, patient_nbr).
- Writes the cleaned DataFrame to diabetic_data.cleaned.csv in the same directory.
"""

import argparse
from pathlib import Path

import pandas as pd


def clean_diabetic_data(
    input_path: str | Path,
    output_path: str | Path | None = None,
    missing_threshold: float = 0.80,
    drop_id_columns: bool = True,
) -> pd.DataFrame:
    """
    Load, clean, and optionally save the diabetic data.

    Parameters
    ----------
    input_path : path to diabetic_data.csv
    output_path : path for cleaned CSV; if None, uses input dir / diabetic_data.cleaned.csv
    missing_threshold : drop columns with fraction missing > this (0.0--1.0)
    drop_id_columns : if True, drop encounter_id and patient_nbr

    Returns
    -------
    Cleaned DataFrame.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Output path: same directory as input, name diabetic_data.cleaned.csv
    if output_path is None:
        output_path = input_path.parent / "diabetic_data.cleaned.csv"
    else:
        output_path = Path(output_path)

    print(f"Loading {input_path} ...")
    df = pd.read_csv(
        input_path,
        na_values=["?", "None"],
        low_memory=False,
    )
    print(f"  Loaded shape: {df.shape}")

    # Drop columns with too much missing data
    n_rows = len(df)
    missing_pct = df.isna().sum() / n_rows
    cols_high_missing = missing_pct[missing_pct > missing_threshold].index.tolist()
    if cols_high_missing:
        df = df.drop(columns=cols_high_missing, errors="ignore")
        print(f"  Dropped {len(cols_high_missing)} columns with >{missing_threshold*100:.0f}% missing: {cols_high_missing}")
    else:
        print(f"  No columns with >{missing_threshold*100:.0f}% missing.")

    # Optionally drop identifier columns
    id_cols = ["encounter_id", "patient_nbr"]
    if drop_id_columns:
        existing_ids = [c for c in id_cols if c in df.columns]
        if existing_ids:
            df = df.drop(columns=existing_ids, errors="ignore")
            print(f"  Dropped ID columns: {existing_ids}")

    print(f"  Cleaned shape: {df.shape}")
    print(f"  Remaining missing (top 5):\n{df.isna().sum().sort_values(ascending=False).head(5)}")

    # Save
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Clean Diabetes 130-US Hospitals data and write diabetic_data.cleaned.csv"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=Path(__file__).resolve().parent
        / "diabetes+130-us+hospitals+for+years+1999-2008"
        / "diabetic_data.csv",
        type=Path,
        help="Path to diabetic_data.csv (default: dataset folder next to this script)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output path for cleaned CSV (default: same dir as input, diabetic_data.cleaned.csv)",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.80,
        help="Drop columns with fraction missing > this (default: 0.80)",
    )
    parser.add_argument(
        "--keep-ids",
        action="store_true",
        help="Keep encounter_id and patient_nbr (default: drop them)",
    )
    args = parser.parse_args()

    clean_diabetic_data(
        input_path=args.input,
        output_path=args.output,
        missing_threshold=args.threshold,
        drop_id_columns=not args.keep_ids,
    )


if __name__ == "__main__":
    main()

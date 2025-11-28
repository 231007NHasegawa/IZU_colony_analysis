#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step 2 — Build the daily colony-phase (DCP) dataset
--------------------------------------------------

Input:
    photo_list.csv  (columns: date, phase)
        date: YYYYMMDD
        phase: o / p / t  (or 0/1/2)

Output:
    output/dataset/DCP.csv
        date, phase_num

Notes:
    - Only days with usable photographs (i.e., listed in photo_list.csv)
      are assigned a phase.
    - Missing days are excluded (as defined in the Methods).
"""

import pandas as pd
from pathlib import Path

# Input files
PHOTO_LIST = Path("photo/photo_list.csv")

# Output directory
OUTDIR = Path("output/dataset")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Mapping o/p/t → 0/1/2
PHASE_MAP = {"o": 0, "p": 1, "t": 2}


def main():
    print("[INFO] Step2: Building DCP dataset")

    if not PHOTO_LIST.exists():
        raise FileNotFoundError("photo_list.csv not found in current directory.")

    # Load photo_list.csv
    df = pd.read_csv(PHOTO_LIST)

    # Basic check
    if "date" not in df.columns or "phase" not in df.columns:
        raise ValueError("photo_list.csv must contain columns: date, phase")

    # Normalize phase values
    df["phase"] = df["phase"].astype(str).str.strip().str.lower()

    # Map phase to numeric values
    if set(df["phase"].unique()).issubset(set(PHASE_MAP.keys())):
        df["phase_num"] = df["phase"].map(PHASE_MAP)
    else:
        # fallback: numeric input
        df["phase_num"] = pd.to_numeric(df["phase"], errors="coerce")

    # Parse date
    df["date"] = pd.to_datetime(
        df["date"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(subset=["date", "phase_num"]).copy()

    # Sort
    df = df.sort_values("date").reset_index(drop=True)

    # Output file
    outfile = OUTDIR / "DCP.csv"
    df.to_csv(outfile, index=False)

    print(f"[INFO] DCP dataset saved → {outfile}")
    print(f"[INFO] Total valid records: {len(df)}")


if __name__ == "__main__":
    main()

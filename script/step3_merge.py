#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step 3 — Merge CDST (temperature) dataset and DCP (colony phase) dataset
------------------------------------------------------------------------

Input:
    output/dataset/CDST.csv
        columns: date, sst_habukuchi
    output/dataset/DCP.csv
        columns: date, phase_num

Output:
    output/dataset/merged_dataset.csv
        columns: date, sst_habukuchi, phase_num

Notes:
    - Left merge (CDST is the reference timeline)
    - Days without photographs keep phase_num = NaN
"""

import pandas as pd
from pathlib import Path

# Paths
DATASET_DIR = Path("output/dataset")
CDST = DATASET_DIR / "CDST.csv"
DCP = DATASET_DIR / "DCP.csv"
OUTFILE = DATASET_DIR / "merged_dataset.csv"


def main():
    print("[INFO] Step3: Merging CDST × DCP")

    if not CDST.exists():
        raise FileNotFoundError("CDST.csv not found in output/dataset/")
    if not DCP.exists():
        raise FileNotFoundError("DCP.csv not found in output/dataset/")

    # Load datasets
    sst = pd.read_csv(CDST)
    dcp = pd.read_csv(DCP)

    # Parse date
    sst["date"] = pd.to_datetime(sst["date"])
    dcp["date"] = pd.to_datetime(dcp["date"])

    # Left merge: all SST rows kept, phase added when available
    merged = pd.merge(sst, dcp, on="date", how="left")

    # Sort output
    merged = merged.sort_values("date").reset_index(drop=True)

    # Save
    merged.to_csv(OUTFILE, index=False)

    print(f"[INFO] Saved merged dataset → {OUTFILE}")
    print(f"[INFO] Total rows: {len(merged)}")
    print(f"[INFO] Date range: {merged['date'].min()} → {merged['date'].max()}")


if __name__ == "__main__":
    main()

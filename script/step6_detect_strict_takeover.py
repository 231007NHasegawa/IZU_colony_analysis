#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
step6_detect_strict_takeover.py
-----------------------------------------
Strict takeover periods = periods beginning on each onset date,
and ending the last consecutive t-day that occurs with no missing
boundaries.

Uses:
    - onset_temperature_windows.csv
    - merged_dataset.csv

Output:
    strict_takeover_periods.csv
"""

import pandas as pd
from pathlib import Path

MERGED = Path("output/dataset/merged_dataset.csv")
ONSET = Path("output/takeover_phase/onset_temperature_windows.csv")
OUTDIR = Path("output/takeover_phase")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "strict_takeover_periods.csv"


def main():
    df = pd.read_csv(MERGED)
    df["date"] = pd.to_datetime(df["date"])

    onset_df = pd.read_csv(ONSET)
    onset_df["onset_date"] = pd.to_datetime(onset_df["onset_date"])

    results = []

    for _, row in onset_df.iterrows():
        onset = row["onset_date"]
        idx = df.index[df["date"] == onset][0]

        j = idx
        while j + 1 < len(df) and df.at[j + 1, "phase_num"] == 2:
            j += 1

        end = df.at[j, "date"]

        results.append({
            "onset_date": onset.date(),
            "end_date": end.date(),
            "duration_strict": (end - onset).days + 1
        })

    pd.DataFrame(results).to_csv(OUTFILE, index=False)
    print(f"[INFO] Saved strict takeover periods → {OUTFILE}")


if __name__ == "__main__":
    main()

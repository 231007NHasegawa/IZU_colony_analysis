#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
step5_onset_temp_windows.py
-----------------------------------------
Compute 3-, 5-, 7-day temperature windows preceding takeover onset.

Output:
    output/takeover_phase/onset_temperature_windows.csv
"""

import pandas as pd
from pathlib import Path

MERGED = Path("output/dataset/merged_dataset.csv")
OUTDIR = Path("output/takeover_phase")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "onset_temperature_windows.csv"


def window_stats(df, idx, size):
    start = max(0, idx - (size - 1))
    sub = df.iloc[start:idx + 1]["sst"].dropna()
    if len(sub) == 0:
        return None
    return {
        "mean": sub.mean(),
        "median": sub.median(),
        "min": sub.min(),
        "max": sub.max(),
    }


def main():
    df = pd.read_csv(MERGED)
    df["date"] = pd.to_datetime(df["date"])

    rows = []

    for i in range(1, len(df)):
        if df.at[i, "phase_num"] == 2 and df.at[i - 1, "phase_num"] in (0, 1):
            onset = df.at[i, "date"]
            record = {"onset_date": onset.date()}

            for w in (3, 5, 7):
                stats = window_stats(df, i, w)
                if stats:
                    for k, v in stats.items():
                        record[f"w{w}_{k}"] = v
                else:
                    for k in ("mean", "median", "min", "max"):
                        record[f"w{w}_{k}"] = None

            rows.append(record)

    out = pd.DataFrame(rows)
    out.to_csv(OUTFILE, index=False)
    print(f"[INFO] Saved onset SST windows → {OUTFILE}")


if __name__ == "__main__":
    main()

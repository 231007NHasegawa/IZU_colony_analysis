#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
step6_detect_strict_takeover.py
-----------------------------------------
Strict takeover periods =

Start:
    - onset date (o/p → t transition)

During takeover:
    - phase_num == 2 (t) → OK
    - phase_num == NaN (missing) → OK (treated as continuous)
End:
    - the first following date where phase_num ∈ {0,1}
      (recovery confirmed)
    - if missing continues until dataset end → strict end not defined

Input:
    output/dataset/merged_dataset.csv
    output/takeover_phase/onset_temperature_windows.csv

Output:
    strict_takeover_periods.csv
"""

import pandas as pd
from pathlib import Path
import numpy as np

MERGED = Path("output/dataset/merged_dataset.csv")
ONSET = Path("output/takeover_phase/onset_temperature_windows.csv")
OUTDIR = Path("output/takeover_phase")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "strict_takeover_periods.csv"


def main():
    df = pd.read_csv(MERGED)
    df["date"] = pd.to_datetime(df["date"])

    # Allow missing phase values to be NaN
    df["phase_num"] = pd.to_numeric(df["phase_num"], errors='coerce')

    onset_df = pd.read_csv(ONSET)
    onset_df["onset_date"] = pd.to_datetime(onset_df["onset_date"])

    results = []

    for _, row in onset_df.iterrows():
        onset_date = row["onset_date"]

        # find onset index
        idx_list = df.index[df["date"] == onset_date].tolist()
        if len(idx_list) == 0:
            print(f"[WARN] onset date not found: {onset_date}")
            continue
        start_idx = idx_list[0]

        j = start_idx
        n = len(df)

        # expand forward: allow t or missing
        while j + 1 < n:
            next_phase = df.at[j + 1, "phase_num"]

            if next_phase == 2 or np.isnan(next_phase):
                j += 1
                continue
            else:
                # recovery (o or p)
                break

        # recovery must be o/p
        if j + 1 < n and df.at[j + 1, "phase_num"] in (0, 1):
            end_idx = j
            end_date = df.at[end_idx, "date"]
            duration = (end_date - onset_date).days + 1

            results.append({
                "onset_date": onset_date.date(),
                "end_date": end_date.date(),
                "duration_strict": duration
            })
        else:
            print(f"[WARN] strict recovery not found → skipping onset {onset_date.date()}")

    pd.DataFrame(results).to_csv(OUTFILE, index=False)
    print(f"[INFO] Saved strict takeover periods → {OUTFILE}")


if __name__ == "__main__":
    main()

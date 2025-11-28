#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
step4_detect_takeover.py
-----------------------------------------
General takeover periods:

Definition:
    - A takeover period begins the first day with phase = 2 (t)
      after a day classified as 0 (o) or 1 (p), OR when t appears
      at the start of the dataset.
    - A takeover period ends the last consecutive or missing-data-
      bridged t-day before returning to phase 0 or 1.
    - Missing days between t-days are treated as part of the period.

Output:
    output/takeover_phase/general_takeover_periods.csv
"""

import pandas as pd
from pathlib import Path

DCP = Path("output/dataset/DCP.csv")
OUTDIR = Path("output/takeover_phase")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "general_takeover_periods.csv"


def main():
    df = pd.read_csv(DCP)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    periods = []
    n = len(df)
    i = 0

    while i < n:
        # detect start of takeover
        if df.loc[i, "phase_num"] == 2:
            if i == 0 or df.loc[i - 1, "phase_num"] in (0, 1):

                start = df.loc[i, "date"]
                j = i

                # extend through t or missing
                while j + 1 < n and (
                    pd.isna(df.loc[j + 1, "phase_num"]) or df.loc[j + 1, "phase_num"] == 2
                ):
                    j += 1

                end = df.loc[j, "date"]

                periods.append({
                    "start_date": start.date(),
                    "end_date": end.date(),
                    "duration_general": (end - start).days + 1
                })

                i = j + 1
                continue

        i += 1

    pd.DataFrame(periods).to_csv(OUTFILE, index=False)
    print(f"[INFO] Saved general takeover periods → {OUTFILE}")


if __name__ == "__main__":
    main()

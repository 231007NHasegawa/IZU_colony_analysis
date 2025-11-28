#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Step 1 — Extract daily SST (Habukuchi station = 波浮口) from all PDF files in temp/.

PDF structure:
    日 波浮口 若郷 野伏 ...
    1 25.9 28.9 25.5 ...
    2 26.4 28.0 27.6 ...
    ...

We extract:
    day = first number in line
    sst = second number in line  → 波浮口（水温）

Output:
    output/dataset/CDST.csv
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import re

TEMP_DIR = Path("temp")
OUTDIR = Path("output/dataset")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Japanese station name (Habukuchi)
TARGET_STATION_JP = "波浮口"


def extract_sst_from_pdf(pdf_path):
    """
    Extract (date, SST) from the PDF based on text lines.
    We locate lines beginning with a day number (1–31),
    then extract the second numeric field as 波浮口 SST.
    """

    year = int(pdf_path.stem.split(".")[0])
    month = int(pdf_path.stem.split(".")[1])

    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text is None:
                continue

            for line in text.splitlines():

                # Skip header lines
                if TARGET_STATION_JP in line:
                    continue

                # Find leading day number
                m = re.match(r"^\s*(\d{1,2})\s+(.+)$", line)
                if not m:
                    continue

                day = int(m.group(1))
                rest = m.group(2)

                # Extract all numeric fields from the rest of the line
                nums = re.findall(r"\d+\.\d|\d+", rest)

                if len(nums) == 0:
                    continue

                # 波浮口 = first numeric field after day
                sst_text = nums[0]

                try:
                    sst = float(sst_text)
                except:
                    continue

                date = f"{year:04d}-{month:02d}-{day:02d}"
                rows.append([date, sst])

    return rows


def main():
    all_rows = []

    for pdf in sorted(TEMP_DIR.glob("*.pdf")):
        print(f"[INFO] Processing {pdf.name}")
        extracted = extract_sst_from_pdf(pdf)
        all_rows.extend(extracted)

    if not all_rows:
        print("[ERROR] No SST records extracted.")
        return

    df = pd.DataFrame(all_rows, columns=["date", "sst"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna().sort_values("date")

    outpath = OUTDIR / "CDST.csv"
    df.to_csv(outpath, index=False, encoding="utf-8-sig")

    print(f"[INFO] Saved CDST.csv with {len(df)} rows → {outpath}")


if __name__ == "__main__":
    main()

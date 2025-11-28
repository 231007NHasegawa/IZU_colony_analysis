#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
make_photo_list.py
-----------------------------------------------------

Usage:
    1. Create a folder named 'photo' in the current directory.
    2. Put all image files (JPG, PNG, TIFF, BMP, etc.) into ./photo.
    3. Run this script:
           python3 make_photo_list.py

This script scans ./photo, extracts shooting dates from EXIF
(DateTimeOriginal) when available, or extracts YYYYMMDD from
the filename as a fallback.

A CSV file will be created:
      ./photo/photo_list.csv

Columns:
    photo_id   : original filename
    date       : shooting date (YYYYMMDD)
    phase      : left blank, except when multiple images share
                 the same date → "duplication" is inserted.
                 (User must manually keep only one record.)

Supported image formats (case-insensitive):
    JPG, JPEG, PNG, TIF, TIFF, BMP
"""

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import re
import pandas as pd


PHOTO_DIR = Path("photo")
OUTPUT_CSV = PHOTO_DIR / "photo_list.csv"
VALID_EXT = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"]


def get_exif_date(img_path):
    """Extract DateTimeOriginal (YYYY:MM:DD HH:MM:SS) → YYYYMMDD."""
    try:
        img = Image.open(img_path)
        exif = img._getexif()
        if exif is None:
            return None

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                # Format example: "2023:08:15 12:33:01"
                return value.split(" ")[0].replace(":", "")
    except Exception:
        return None

    return None


def extract_date_from_filename(fname):
    """Fallback: extract YYYYMMDD from the first 8 digits of filename."""
    m = re.match(r"(\d{8})", fname)
    return m.group(1) if m else None


def main():
    if not PHOTO_DIR.exists():
        print("[ERROR] './photo' directory does not exist.")
        print("Create the folder and place images inside it.")
        return

    images = [
        f for f in sorted(PHOTO_DIR.iterdir())
        if f.is_file() and f.suffix.lower() in VALID_EXT
    ]

    if not images:
        print("[WARNING] No image files found in ./photo")
        return

    records = []

    # ---------- Extract dates ----------
    for img_path in images:
        fname = img_path.name

        # 1) Try EXIF
        date_str = get_exif_date(img_path)

        # 2) If EXIF missing, try filename
        if date_str is None:
            date_str = extract_date_from_filename(fname)

        if date_str is None:
            print(f"[WARNING] Could not extract date: {fname}")
            continue

        records.append({"photo_id": fname, "date": date_str})

    if not records:
        print("[ERROR] No valid photo records created.")
        return

    # ---------- Convert to DataFrame for sorting ----------
    df = pd.DataFrame(records)

    # Sort by date ascending
    df = df.sort_values("date").reset_index(drop=True)

    # Mark duplications
    df["phase"] = ""
    dup_dates = df["date"].value_counts()
    for d, count in dup_dates.items():
        if count > 1:
            df.loc[df["date"] == d, "phase"] = "duplication"

    # ---------- Save CSV inside ./photo ----------
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"\n[INFO] Created photo list → {OUTPUT_CSV.resolve()}")
    print("[INFO] Rows with 'duplication' must be manually reduced.\n")


if __name__ == "__main__":
    main()

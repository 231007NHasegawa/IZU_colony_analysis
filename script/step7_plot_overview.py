#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step 7 — Plot phase × SST overview
----------------------------------

Input:
    output/dataset/merged_dataset.csv

Output:
    output/takeover_phase/phase_temperature_overview.svg
    output/takeover_phase/phase_temperature_overview.png
"""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATASET_DIR = Path("output/dataset")
TAKEOVER_DIR = Path("output/takeover_phase")
TAKEOVER_DIR.mkdir(parents=True, exist_ok=True)

MERGED = DATASET_DIR / "merged_dataset.csv"


def main():
    print("[INFO] Step7: Plotting phase × temperature overview")

    if not MERGED.exists():
        raise FileNotFoundError("merged_dataset.csv not found. Run step3 first.")

    df = pd.read_csv(MERGED)
    df["date"] = pd.to_datetime(df["date"])

    PHASE_COLOR = {0: "gray", 1: "orange", 2: "red"}

    fig, ax_phase = plt.subplots(figsize=(14, 4))

    # --- Draw phase lines ---
    for i in range(len(df) - 1):
        d0, y0 = df.at[i, "date"], df.at[i, "phase_num"]
        d1, y1 = df.at[i + 1, "date"], df.at[i + 1, "phase_num"]

        if pd.isna(y0) or pd.isna(y1):
            continue

        # horizontal line
        ax_phase.plot(
            [d0, d1],
            [y0, y0],
            color=PHASE_COLOR[y0],
            linewidth=2.5,
        )

        if y0 != y1:
            ax_phase.plot(
                [d1, d1],
                [y0, y1],
                color="lightgray",
                linestyle="dotted",
                linewidth=2.0,
            )

    ax_phase.set_ylim(-0.3, 2.3)
    ax_phase.set_yticks([0, 1, 2])
    ax_phase.set_yticklabels(["ordinary (0)", "partial (1)", "takeover (2)"])
    ax_phase.set_xlabel("Date")
    ax_phase.set_ylabel("Phase")

    # --- Temperature axis ---
    ax_temp = ax_phase.twinx()
    ax_temp.plot(
        df["date"],
        df["sst"],
        color="#66a3ff",
        linewidth=0.8,
    )
    ax_temp.set_ylabel("Sea surface temperature (°C)")

    fig.tight_layout()

    out_svg = TAKEOVER_DIR / "phase_temperature_overview.svg"
    out_png = TAKEOVER_DIR / "phase_temperature_overview.png"

    fig.savefig(out_svg)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)

    print(f"[INFO] Saved → {out_svg}")
    print(f"[INFO] Saved → {out_png}")


if __name__ == "__main__":
    main()

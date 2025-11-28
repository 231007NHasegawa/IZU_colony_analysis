#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run all analysis steps sequentially.
Each step is defined in its own script in script/.
Renamed to a clear monotonic order: step1 → step7.
"""

import subprocess
from pathlib import Path

SCRIPTS = [
    "step1_extract_sst.py",            
    "step2_build_dcp.py",             
    "step3_merge.py",                 
    "step4_detect_takeover.py",       
    "step5_onset_temp_windows.py",    
    "step6_detect_strict_takeover.py",
    "step7_plot_overview.py",         
]

def main():
    script_dir = Path("script")

    print("\n===== Running pipeline =====\n")

    for step in SCRIPTS:
        path = script_dir / step
        print(f"[RUN] {step}")

        if not path.exists():
            print(f"[ERROR] Script not found: {path}")
            return

        result = subprocess.run(["python3", str(path)])

        if result.returncode != 0:
            print(f"[FAIL] {step} failed. Stopping.")
            return

        print(f"[OK] {step} completed.\n")

    print("\n===== Pipeline completed successfully! =====\n")

if __name__ == "__main__":
    main()

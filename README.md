# IZU_colony_analysis
Automated pipeline for extracting colony-phase transitions and seawater temperature conditions in a wild botrylline ascidian colony monitored at Izu Ōshima, Japan.

This repository contains all scripts used to reproduce the analyses described in:

Hasegawa et al. (in prep.). Seasonal dynamics of a wild botrylline ascidian colony and temperature dependence of takeover events.

The pipeline integrates (1) daily colony-phase records derived from underwater photographs and (2) daily surface seawater temperature (SST) extracted from monthly PDF files. It then identifies takeover periods, computes temperature statistics, and produces summary datasets and visualizations.

---

## Directory structure

IZU_colony_analysis/
│
├── photo/ # Place raw image files here
├── script/ # Analysis scripts (step1–step7)
├── output/ # Automatically generated
│ ├── dataset/
│ └── takeover_phase/
│
├── make_photo_list.py
├── run_pipeline.py
└── README.md

---

## Requirements

Python 3.9 or higher is recommended.

Required Python libraries:

pandas
numpy
matplotlib
pdfplumber
Pillow

---

## Preparing photo_list.csv

Before running the pipeline, you must prepare the daily colony-phase dataset.

1. Create a directory named `photo/`.
2. Place all image files inside `photo/`  
   Supported formats: JPG, JPEG, PNG, TIFF (upper/lowercase accepted).
3. Run:

python3 make_photo_list.py

This generates:

photo/photo_list.csv

### Format of photo_list.csv

photo_id,date,phase
IMG_20230810.JPG,20230810,
IMG_20230811.JPG,20230811,
IMG_20230811-2.JPG,20230811,duplication

Notes:

- `date` comes from EXIF metadata (if available) or from filename.
- If multiple photos were taken on the same date, the script labels them with `duplication`.  
  Remove redundant rows manually and keep one photo per date.
- The user must manually assign the colony phase for each date:
  - `o` = ordinary
  - `p` = partial
  - `t` = takeover

This is the only manual step in the workflow.

---

## Preparing SST PDF files

PDF files of SST data must be placed in:

temp/

Expected filename format:
2023.08.pdf
2023.09.pdf
...

The pipeline extracts SST from the station named **波浮口** (Habukuchi), the closest fixed-point monitoring site to the observation location.

---

## Running the pipeline

Execute all steps with:

python3 run_pipeline.py


Steps executed:

1. Extract daily SST → CDST.csv
2. Build DCP dataset from photo_list.csv
3. Merge CDST × DCP
4. Detect general takeover periods
5. Compute temperature windows before takeover onset
6. Detect strict takeover periods
7. Generate SST × colony-phase overview figure

---

## Output files

### `output/dataset/`
- `CDST.csv` — Continuous daily SST dataset  
- `DCP.csv` — Daily colony-phase dataset  
- `merged_dataset.csv` — Combined SST + colony-phase time series  

### `output/takeover_phase/`
- `takeover_periods.csv`  
- `onset_temperature_windows.csv`  
- `strict_takeover_periods.csv`  
- `overview_plot.png`, `overview_plot.pdf`

---

## Reproducibility

The pipeline is deterministic:

- No randomization
- All outputs fully regenerable from photo_list.csv and the SST PDF files
- Updating either input automatically updates all downstream results

---

## Citation

If you use this repository, please cite:

Hasegawa N et al. (2025) IZU_colony_analysis: Pipeline for integrating colony-phase records with seawater temperature data. https://github.com/231007NHasegawa/IZU_colony_analysis

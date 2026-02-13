"""
01_data_cleaning.py

Purpose:
    Load, validate, and minimally clean peer review datasets
    used in the Visual Nudges study.

Scope:
    This script performs structural cleaning only:
    - standardizes column names
    - enforces data types
    - removes empty or malformed records

IMPORTANT:
    The datasets contain NO personal identifiers.
    No anonymization or de-identification is required.

Output:
    A cleaned dataset saved to /data/clean/ for downstream analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# =========================
# 0) Setup
# =========================

# Set paths (adjust if needed)
raw_data_path = Path("data/raw")
clean_data_path = Path("data/clean")

# Create clean directory if it does not exist
clean_data_path.mkdir(parents=True, exist_ok=True)

# =========================
# 1) Load raw data
# =========================

# Example: Excel export from the Visual Peer Review Dashboard
# Assumes ONE file per condition or a merged export
raw_file = raw_data_path / "peer_review_raw.xlsx"

try:
    df_raw = pd.read_excel(raw_file)
    print(f"Raw data loaded: {len(df_raw)} rows; {len(df_raw.columns)} columns")
except FileNotFoundError:
    print(f"ERROR: File not found at {raw_file}")
    sys.exit(1)

# =========================
# 2) Data scope and integrity
# =========================
# The exported datasets contain no direct or indirect personal identifiers.
# Records consist solely of rubric scores, interaction-derived measures,
# and written peer review comments.
#
# No anonymization or de-identification procedures were required.

# =========================
# 3) Standardize column names
# =========================

# Convert column names to lowercase and replace spaces with underscores
df = df_raw.copy()
df.columns = (df.columns
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('[^a-zA-Z0-9_]', '', regex=True))

# =========================
# 4) Basic structural validation
# =========================

# Expected minimal columns (adjust names to match your export)
expected_cols = [
    "semester",              # e.g., "Fall 2025", "Spring 2025"
    "condition",             # "baseline" or "nudge"
    "submission_id",         # identifier for visualization artifact
    "rubric_criterion",      # name of rubric dimension
    "rubric_score",          # numeric score
    "written_comment"        # qualitative feedback
]

missing_cols = set(expected_cols) - set(df.columns)

if missing_cols:
    raise ValueError(
        f"ERROR: Missing required columns: {', '.join(missing_cols)}"
    )

# =========================
# 5) Type coercion
# =========================

df['semester'] = df['semester'].astype('category')
df['condition'] = pd.Categorical(
    df['condition'], 
    categories=['baseline', 'nudge'], 
    ordered=True
)
df['submission_id'] = df['submission_id'].astype('category')
df['rubric_criterion'] = df['rubric_criterion'].astype('category')
df['rubric_score'] = pd.to_numeric(df['rubric_score'], errors='coerce')
df['written_comment'] = df['written_comment'].astype(str)

# =========================
# 6) Remove empty or invalid records
# =========================

df_clean = df[
    df['rubric_score'].notna() &
    df['rubric_criterion'].notna() &
    df['condition'].notna()
].copy()

n_removed = len(df_raw) - len(df_clean)
print(f"After cleaning: {len(df_clean)} rows retained ({n_removed} removed)")

# =========================
# 7) Basic derived checks (no feature extraction yet)
# =========================

# Trim whitespace in comments
df_clean['written_comment'] = df_clean['written_comment'].str.strip()

# Ensure empty comments are explicit NaN
df_clean.loc[df_clean['written_comment'] == '', 'written_comment'] = np.nan
df_clean.loc[df_clean['written_comment'] == 'nan', 'written_comment'] = np.nan

# =========================
# 8) Save cleaned data
# =========================

clean_file = clean_data_path / "peer_review_clean.csv"
df_clean.to_csv(clean_file, index=False)

print(f"Cleaned dataset saved to: {clean_file}")

# =========================
# 9) Session info (for reproducibility)
# =========================

print("\nPython environment info:")
print(f"pandas version: {pd.__version__}")
print(f"numpy version: {np.__version__}")
print(f"Python version: {sys.version}")

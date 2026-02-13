"""
02_descriptive_statistics.py

Purpose:
    Generate descriptive statistics for reviewer-level features
    by experimental condition.

Inputs:
    data/features/reviewer_level_features.csv

Outputs:
    results/descriptive_statistics_by_condition.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

# =========================
# Setup
# =========================

# Create results directory if it doesn't exist
results_path = Path("results")
results_path.mkdir(parents=True, exist_ok=True)

# =========================
# Load features
# =========================

df = pd.read_csv("data/features/reviewer_level_features.csv")

print(f"Loaded {len(df)} reviewer records")

# =========================
# Helper function for descriptive stats
# =========================

def desc_stats(x):
    """Calculate descriptive statistics for a series"""
    return pd.Series({
        'Mean': x.mean(),
        'SD': x.std(),
        'Median': x.median(),
        'IQR': x.quantile(0.75) - x.quantile(0.25)
    })

# =========================
# Compute stats by condition
# =========================

# Group by condition and calculate statistics
desc_table = df.groupby('condition').agg(
    n=('condition', 'size'),
    
    # Written feedback
    total_words_mean=('total_words', 'mean'),
    total_words_sd=('total_words', 'std'),
    total_words_median=('total_words', 'median'),
    total_words_iqr=('total_words', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    
    # Rubric coverage
    rubric_mean=('rubric_coverage', 'mean'),
    rubric_sd=('rubric_coverage', 'std'),
    rubric_median=('rubric_coverage', 'median'),
    rubric_iqr=('rubric_coverage', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    
    # Comparative behavior
    comparison_rate=('has_comparison', 'mean'),
    
    # Score variability
    score_sd_mean=('score_sd', 'mean'),
    score_sd_sd=('score_sd', 'std')
).reset_index()

# =========================
# Save for LaTeX/reporting
# =========================

output_file = results_path / "descriptive_statistics_by_condition.csv"
desc_table.to_csv(output_file, index=False)

print(f"\nDescriptive statistics saved to: {output_file}")
print("\nPreview:")
print(desc_table)

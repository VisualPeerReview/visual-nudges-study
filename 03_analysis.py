"""
03_analysis.py

Purpose:
    Run the statistical analysis for the Visual Nudges study,
    starting with descriptive statistics and moving to more
    advanced (but still reviewer-defensible) inference.

Inputs:
    data/features/reviewer_level_features.csv

Outputs:
    results/tables/
      - table_descriptives_by_condition.csv
      - table_effect_sizes_by_condition.csv
      - table_bootstrap_ci_by_condition.csv
      - table_comparative_flag_by_condition.csv
      - table_wilcoxon_sensitivity.csv
      - table_comparative_association_or.csv
    results/models/
      - model_summaries.txt

Notes:
    - Quasi-experimental between-cohort: interpret as associative.
    - Uses robust, transparent statistics:
        (1) Descriptives
        (2) Standardized mean differences (Hedges g)
        (3) Bootstrap CIs for mean differences
        (4) Nonparametric tests (Wilcoxon) as sensitivity checks
        (5) Logistic regression for comparative-reference rate
          (optional but included, plainly interpreted)
"""

############################################################
# ANALYSIS INTENT
#
# This analysis characterizes associations between interface
# conditions and evaluative analytic behavior using a
# quasi-experimental, between-cohort design.
#
# All inferential statistics are reported as robustness and
# sensitivity checks, not as evidence of causal effects.
# No covariate adjustment or predictive modeling is performed
# due to the presence of cohort-level confounds.
#
# Effect sizes and confidence intervals are used to describe
# the magnitude and stability of observed differences.
############################################################

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from statsmodels.formula.api import logit
import sys

# =========================
# 0) Setup
# =========================

feature_data_path = Path("data/features")
results_table_path = Path("results/tables")
results_model_path = Path("results/models")

# Create directories if they don't exist
results_table_path.mkdir(parents=True, exist_ok=True)
results_model_path.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(20260209)

# =========================
# 1) Load reviewer-level features
# =========================

df = pd.read_csv(feature_data_path / "reviewer_level_features.csv")

print(f"Loaded reviewer-level features: {len(df)} reviewers")

# Basic validation
if not all(col in df.columns for col in ['condition', 'semester']):
    raise ValueError("ERROR: Missing required columns 'condition' and/or 'semester'")

if df['condition'].nunique() < 2:
    raise ValueError("ERROR: Need at least 2 conditions for comparison")

# Ensure condition is an ordered categorical for stable reporting
# (Baseline first, Nudge second)
df['condition'] = pd.Categorical(
    df['condition'],
    categories=['baseline', 'nudge'],
    ordered=True
)

# =========================
# 2) Descriptive statistics (by condition)
# =========================

metrics_continuous = [
    "total_words",
    "mean_words_per_comment",
    "rubric_criteria_addressed",
    "rubric_coverage_ratio",
    "comparative_reference_rate",
    "score_mean",
    "score_sd",
    "score_range"
]

# Reshape to long format for grouped statistics
df_long = df.melt(
    id_vars=['condition'],
    value_vars=metrics_continuous,
    var_name='metric',
    value_name='value'
)

# Calculate descriptive statistics by condition and metric
desc_by_condition = df_long.groupby(['condition', 'metric']).agg(
    n=('value', lambda x: x.notna().sum()),
    mean=('value', 'mean'),
    sd=('value', 'std'),
    median=('value', 'median'),
    iqr=('value', lambda x: x.quantile(0.75) - x.quantile(0.25)),
    min=('value', 'min'),
    max=('value', 'max')
).reset_index().sort_values(['metric', 'condition'])

desc_by_condition.to_csv(
    results_table_path / "table_descriptives_by_condition.csv",
    index=False
)

print(f"✓ Saved: table_descriptives_by_condition.csv")

# =========================
# 3) Effect sizes (Hedges g)
# =========================

def hedges_g(x1, x2):
    """
    Calculate Hedges' g effect size between two groups.
    
    Parameters:
        x1: array-like, first group
        x2: array-like, second group
        
    Returns:
        float: Hedges' g effect size
    """
    x1 = np.array(x1)
    x2 = np.array(x2)
    
    # Remove non-finite values
    x1 = x1[np.isfinite(x1)]
    x2 = x2[np.isfinite(x2)]
    
    n1, n2 = len(x1), len(x2)
    
    if n1 < 2 or n2 < 2:
        return np.nan
    
    s1, s2 = np.std(x1, ddof=1), np.std(x2, ddof=1)
    
    # Pooled standard deviation
    sp = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    
    if not np.isfinite(sp) or sp == 0:
        return np.nan
    
    # Cohen's d
    d = (np.mean(x2) - np.mean(x1)) / sp
    
    # Correction factor J for Hedges' g
    J = 1 - (3 / (4 * (n1 + n2) - 9))
    
    return J * d

# Calculate effect sizes for each metric
effect_sizes = []

for metric in metrics_continuous:
    x_base = df[df['condition'] == 'baseline'][metric].dropna()
    x_nudge = df[df['condition'] == 'nudge'][metric].dropna()
    
    effect_sizes.append({
        'metric': metric,
        'hedges_g_nudge_minus_baseline': hedges_g(x_base, x_nudge),
        'mean_diff_nudge_minus_baseline': x_nudge.mean() - x_base.mean()
    })

df_effects = pd.DataFrame(effect_sizes)

df_effects.to_csv(
    results_table_path / "table_effect_sizes_by_condition.csv",
    index=False
)

print(f"✓ Saved: table_effect_sizes_by_condition.csv")

# =========================
# 4) Bootstrap CIs
# =========================

def bootstrap_mean_diff(x_base, x_nudge, B=5000):
    """
    Calculate bootstrap confidence intervals for mean difference.
    
    Parameters:
        x_base: array-like, baseline group
        x_nudge: array-like, nudge group
        B: int, number of bootstrap samples
        
    Returns:
        dict: mean difference and 95% CI bounds
    """
    x_base = np.array(x_base)
    x_nudge = np.array(x_nudge)
    
    # Remove non-finite values
    x_base = x_base[np.isfinite(x_base)]
    x_nudge = x_nudge[np.isfinite(x_nudge)]
    
    n1, n2 = len(x_base), len(x_nudge)
    
    if n1 < 2 or n2 < 2:
        return {'diff': np.nan, 'lo': np.nan, 'hi': np.nan}
    
    # Bootstrap resampling
    diffs = []
    for _ in range(B):
        boot_base = np.random.choice(x_base, size=n1, replace=True)
        boot_nudge = np.random.choice(x_nudge, size=n2, replace=True)
        diffs.append(boot_nudge.mean() - boot_base.mean())
    
    diffs = np.array(diffs)
    
    return {
        'diff': x_nudge.mean() - x_base.mean(),
        'lo': np.percentile(diffs, 2.5),
        'hi': np.percentile(diffs, 97.5)
    }

# Calculate bootstrap CIs for each metric
bootstrap_results = []

for metric in metrics_continuous:
    x_base = df[df['condition'] == 'baseline'][metric].dropna()
    x_nudge = df[df['condition'] == 'nudge'][metric].dropna()
    
    ci = bootstrap_mean_diff(x_base, x_nudge)
    
    bootstrap_results.append({
        'metric': metric,
        'mean_diff_nudge_minus_baseline': ci['diff'],
        'ci95_lo': ci['lo'],
        'ci95_hi': ci['hi']
    })

df_bootstrap = pd.DataFrame(bootstrap_results)

df_bootstrap.to_csv(
    results_table_path / "table_bootstrap_ci_by_condition.csv",
    index=False
)

print(f"✓ Saved: table_bootstrap_ci_by_condition.csv")

# =========================
# 5) Wilcoxon sensitivity checks
# =========================

wilcoxon_results = []

for metric in metrics_continuous:
    x_base = df[df['condition'] == 'baseline'][metric].dropna()
    x_nudge = df[df['condition'] == 'nudge'][metric].dropna()
    
    if len(x_base) < 1 or len(x_nudge) < 1:
        wilcoxon_results.append({
            'metric': metric,
            'W': np.nan,
            'p_value': np.nan
        })
        continue
    
    try:
        stat, p_value = stats.mannwhitneyu(x_nudge, x_base, alternative='two-sided')
        wilcoxon_results.append({
            'metric': metric,
            'W': stat,
            'p_value': p_value
        })
    except Exception as e:
        print(f"Warning: Wilcoxon test failed for {metric}: {e}")
        wilcoxon_results.append({
            'metric': metric,
            'W': np.nan,
            'p_value': np.nan
        })

df_wilcoxon = pd.DataFrame(wilcoxon_results)

df_wilcoxon.to_csv(
    results_table_path / "table_wilcoxon_sensitivity.csv",
    index=False
)

print(f"✓ Saved: table_wilcoxon_sensitivity.csv")

# =========================
# 6) Binary comparative reference model
# =========================

# Create binary indicator for any comparative reference
df['any_comparative'] = (df['comparative_references'] > 0).astype(int)

# Tabulate by condition
tab_binary = df.groupby('condition').agg(
    n=('any_comparative', 'size'),
    n_any=('any_comparative', 'sum'),
    prop_any=('any_comparative', 'mean')
).reset_index()

tab_binary.to_csv(
    results_table_path / "table_comparative_flag_by_condition.csv",
    index=False
)

print(f"✓ Saved: table_comparative_flag_by_condition.csv")

# Logistic regression
try:
    fit_logit = logit('any_comparative ~ C(condition, Treatment("baseline"))', 
                      data=df).fit(disp=0)
    
    # Extract odds ratios and confidence intervals
    or_vals = np.exp(fit_logit.params)
    ci_vals = np.exp(fit_logit.conf_int())
    
    logit_summary = pd.DataFrame({
        'term': or_vals.index,
        'odds_ratio': or_vals.values,
        'ci95_lo': ci_vals[0].values,
        'ci95_hi': ci_vals[1].values
    })
    
    logit_summary.to_csv(
        results_table_path / "table_comparative_association_or.csv",
        index=False
    )
    
    print(f"✓ Saved: table_comparative_association_or.csv")
    
    # =========================
    # 7) Save model summaries
    # =========================
    
    with open(results_model_path / "model_summaries.txt", 'w') as f:
        f.write("=== Logistic regression: any_comparative ~ condition ===\n\n")
        f.write(str(fit_logit.summary()))
        f.write("\n\n=== Odds ratios (Wald 95% CI) ===\n\n")
        f.write(str(logit_summary))
    
    print(f"✓ Saved: model_summaries.txt")
    
except Exception as e:
    print(f"Warning: Logistic regression failed: {e}")

print("\n" + "="*50)
print("Analysis complete!")
print("="*50)

# =========================
# 8) Session info
# =========================

print("\nPython environment info:")
print(f"pandas version: {pd.__version__}")
print(f"numpy version: {np.__version__}")
print(f"scipy version: {stats.__version__}")
print(f"Python version: {sys.version}")

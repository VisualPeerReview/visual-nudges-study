# Visual Nudges Peer Review Study

This repository contains the analysis pipeline for the **Visual Nudges in Peer Review** study, which examines how interface design affects evaluative behavior in educational peer review contexts.

## Overview

This project analyzes peer review data from a quasi-experimental, between-cohort design comparing:
- **Baseline condition**: Standard peer review interface
- **Nudge condition**: Interface with visual nudges encouraging comparative evaluation

The analysis pipeline includes data cleaning, feature extraction, descriptive statistics, and robust inferential analyses (effect sizes, bootstrap confidence intervals, and nonparametric sensitivity checks).

## Project Structure

```
.
├── data/
│   ├── raw/              # Raw data files (not tracked in git)
│   ├── clean/            # Cleaned data
│   └── features/         # Extracted reviewer-level features
├── results/
│   ├── tables/           # Statistical tables (CSV format)
│   └── models/           # Model summaries and diagnostics
├── 01_data_cleaning.py
├── 02_descriptive_statistics.py
├── 03_analysis.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/visual-nudges-study.git
cd visual-nudges-study
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Preparation

Place your raw data file in the `data/raw/` directory as `peer_review_raw.xlsx`.

The raw data should contain the following columns:
- `semester`: Academic term (e.g., "Fall 2025")
- `condition`: Experimental condition ("baseline" or "nudge")
- `submission_id`: Identifier for the reviewed artifact
- `rubric_criterion`: Name of evaluation dimension
- `rubric_score`: Numeric score assigned
- `written_comment`: Qualitative feedback text

### Running the Analysis

Execute the scripts in sequence:

```bash
# Step 1: Clean and validate raw data
python 01_data_cleaning.py

# Step 2: Generate descriptive statistics
python 02_descriptive_statistics.py

# Step 3: Run full statistical analysis
python 03_analysis.py
```

### Output Files

After running the pipeline, you'll find:

**Tables** (`results/tables/`):
- `table_descriptives_by_condition.csv`: Descriptive statistics by condition
- `table_effect_sizes_by_condition.csv`: Hedges' g effect sizes
- `table_bootstrap_ci_by_condition.csv`: Bootstrap 95% confidence intervals
- `table_wilcoxon_sensitivity.csv`: Nonparametric test results
- `table_comparative_flag_by_condition.csv`: Binary comparative behavior rates
- `table_comparative_association_or.csv`: Logistic regression odds ratios

**Models** (`results/models/`):
- `model_summaries.txt`: Full model output summaries

## Analysis Methods

### Key Metrics Analyzed

1. **Written Feedback Volume**
   - Total words across all comments
   - Mean words per comment

2. **Rubric Coverage**
   - Number of criteria addressed
   - Coverage ratio (proportion of available criteria)

3. **Comparative Behavior**
   - Rate of comparative references
   - Binary flag for any comparative language

4. **Score Patterns**
   - Mean score assigned
   - Standard deviation of scores
   - Score range

### Statistical Approach

This is a **quasi-experimental, between-cohort design**. All analyses are interpreted as **associations**, not causal effects, due to potential cohort-level confounds.

The analysis includes:

1. **Descriptive Statistics**: Means, standard deviations, medians, and IQRs by condition
2. **Effect Sizes**: Hedges' g (bias-corrected Cohen's d)
3. **Bootstrap Confidence Intervals**: 5,000 resamples for robust inference
4. **Nonparametric Tests**: Mann-Whitney U (Wilcoxon rank-sum) as sensitivity checks
5. **Logistic Regression**: For binary comparative behavior outcomes

## Data Privacy

**Important**: The datasets contain **NO personal identifiers**. All records consist solely of:
- Rubric scores
- Interaction-derived measures
- Written peer review comments (contextual feedback on visualizations)

No anonymization or de-identification procedures were required or performed.

## Reproducibility

Random seed is set to `20260209` for all stochastic procedures (bootstrap resampling).

Python environment details are logged at the end of each script execution.

## Citation

If you use this code, please cite:

```bibtex
@software{visual_nudges_2026,
  title = {Visual Nudges in Peer Review: Analysis Pipeline},
  author = {[Your Name]},
  year = {2026},
  url = {https://github.com/yourusername/visual-nudges-study}
}
```

## License

[Choose appropriate license: MIT, Apache 2.0, etc.]

## Contact

For questions or issues, please open an issue on GitHub or contact [your email].

## Acknowledgments

This analysis pipeline was developed for research on peer review pedagogies in data visualization education.

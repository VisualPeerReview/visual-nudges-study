# Visual Nudges Peer Review Study

This repository contains the analysis pipeline for the **Visual Nudges in Peer Review** study, which examines how interface design affects evaluative behavior in educational peer review contexts.

## Overview

This project analyzes peer review data from a quasi-experimental, between-cohort design comparing:
- **Baseline condition**: Standard peer review interface
- **Nudge condition**: Interface with visual nudges encouraging comparative evaluation

The analysis pipeline includes data cleaning, feature extraction, descriptive statistics, and robust inferential analyses (effect sizes, bootstrap confidence intervals, and nonparametric sensitivity checks).

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

## Citation

If you use this code, please cite:

```bibtex
@software{visual_nudges_2026,
  title = {Visual Nudges in Peer Review: Analysis Pipeline},
  author = {[Alon Friedman]},
  year = {2026},
  url = {https://github.com/yourusername/visual-nudges-study}
}
```

## License

[Choose appropriate license: MIT, Apache 2.0, etc.]

## Contact

For questions or issues, please open an issue on GitHub or contact [alonfriedman@usf.edu].

## Acknowledgments

This analysis pipeline was developed for research on peer review pedagogies in data visualization education.

Supported by the National Science Foundation - Division of Undergraduate Education (DUE) & Directorate for Education and Human Resources (EHR) - View Grant No. 2216227

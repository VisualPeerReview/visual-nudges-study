# Visual Nudges Peer Review Study

This repository contains the analysis pipeline and materials for the **Visual Nudges** study, which examines how lightweight interface interventions structure analytic judgment in visualization-based peer review.

## Overview

This project analyzes peer review data from a quasi-experimental, between-cohort design comparing:

- **Baseline condition**: Standard peer review interface
- **Visual Nudge condition**: Interface augmented with lightweight visual nudges that support rubric coverage, feedback articulation, comparative evaluation, and score differentiation

The analysis pipeline includes data cleaning, feature extraction, descriptive statistics, effect-size estimation, bootstrap confidence intervals, nonparametric sensitivity checks, and logistic regression for binary outcomes.

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

1. **Written Feedback Articulation**
   - Total words across all comments
   - Mean words per comment

2. **Rubric Coverage**
   - Number of criteria addressed
   - Coverage ratio (proportion of available criteria)

3. **Comparative Behavior**
   - Rate of comparative references
   - Binary flag for any comparative language

4. **Score Differentiation**
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

The datasets included in this repository do **not** contain direct personal identifiers. The available records consist of research variables such as:

- Rubric scores
- Interaction-derived measures
- Written peer review comments about visualization submissions

The repository is intended to support transparency and reproducibility for the associated publication while avoiding the release of personally identifying information or private platform infrastructure.

## Website
For more information, please visit our website: https://visualpeerreview.org/

## License
This repository is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or issues, please open an issue on GitHub or contact [alonfriedman@usf.edu].

## Acknowledgments

This analysis pipeline was developed for research on visual nudges, interface design, and evaluative behavior in visualization-based peer review.

Supported by the National Science Foundation (NSF), Division of Undergraduate Education (DUE), Directorate for Education and Human Resources (EHR), Grant No. 2216227.

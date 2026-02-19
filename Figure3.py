{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
\
# =========================\
# IMPORT PACKAGES\
# =========================\
import pandas as pd\
import numpy as np\
import matplotlib.pyplot as plt\
import seaborn as sns\
\
# =========================\
# READ DATA\
# =========================\
spring_path = "~/Desktop/IEEE Vis 2026/Spring 2025.xlsx"\
fall_path   = "~/Desktop/IEEE Vis 2026/Fall 2025.xlsx"\
\
Spring_2025 = pd.read_excel(spring_path)\
Fall_2025   = pd.read_excel(fall_path)\
\
# Assign conditions\
Spring_2025["Condition"] = "Baseline Interface"\
Fall_2025["Condition"]   = "Visual Nudge Interface"\
\
# Combine\
df_all = pd.concat([Spring_2025, Fall_2025], ignore_index=True)\
\
# Ensure ordering\
df_all["Condition"] = pd.Categorical(\
    df_all["Condition"],\
    categories=["Baseline Interface", "Visual Nudge Interface"],\
    ordered=True\
)\
\
# =========================\
# DETECT RUBRIC COLUMNS\
# =========================\
rubric_cols = df_all.select_dtypes(include=np.number).columns.tolist()\
\
# =========================\
# LONG FORMAT\
# =========================\
df_long = df_all.melt(\
    id_vars=["Condition"],\
    value_vars=rubric_cols,\
    var_name="Rubric",\
    value_name="Score"\
)\
\
# =========================\
# SUMMARY STATISTICS\
# =========================\
summary_df = (\
    df_long\
    .groupby(["Rubric", "Condition"])\
    .agg(\
        mean_score=("Score", "mean"),\
        sd=("Score", "std"),\
        n=("Score", "count")\
    )\
    .reset_index()\
)\
\
summary_df["se"] = summary_df["sd"] / np.sqrt(summary_df["n"])\
summary_df["ci"] = 1.96 * summary_df["se"]\
\
# =========================\
# IEEE COLORS\
# =========================\
ieee_colors = \{\
    "Baseline Interface": "#75787B",       # IEEE Cool Gray\
    "Visual Nudge Interface": "#007377"    # IEEE Teal\
\}\
\
# =========================\
# PLOT\
# =========================\
plt.figure(figsize=(10,6))\
\
sns.barplot(\
    data=summary_df,\
    x="Rubric",\
    y="mean_score",\
    hue="Condition",\
    palette=ieee_colors,\
    ci=None\
)\
\
# Add error bars manually\
for i, row in summary_df.iterrows():\
    x_pos = list(summary_df["Rubric"].unique()).index(row["Rubric"])\
    offset = -0.2 if row["Condition"] == "Baseline Interface" else 0.2\
    \
    plt.errorbar(\
        x=x_pos + offset,\
        y=row["mean_score"],\
        yerr=row["ci"],\
        fmt="none",\
        capsize=5,\
        color="black",\
        linewidth=1.2\
    )\
\
plt.title("Rubric-Level Mean Scores by Interface", fontsize=16, fontweight="bold")\
plt.xlabel("Rubric Dimension", fontweight="bold")\
plt.ylabel("Mean Score", fontweight="bold")\
plt.xticks(rotation=40)\
plt.legend(title="", loc="upper center")\
plt.tight_layout()\
\
plt.savefig("rubric_dimension_VIS_clean.png", dpi=300)\
plt.show()}
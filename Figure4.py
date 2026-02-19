{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # =========================\
# PACKAGES\
# =========================\
import pandas as pd\
import numpy as np\
from scipy.stats import binomtest\
from plotnine import *\
from mizani.formatters import percent_format\
\
# =========================\
# READ DATA\
# =========================\
spring = pd.read_excel("~/Desktop/IEEE Vis 2026/Spring 2025.xlsx")\
fall   = pd.read_excel("~/Desktop/IEEE Vis 2026/Fall 2025.xlsx")\
\
# Assign clean condition labels\
spring["Condition"] = "Baseline"\
fall["Condition"]   = "Visual Nudge"\
\
# Combine\
df_all = pd.concat([spring, fall], ignore_index=True)\
\
# Ensure ordering\
df_all["Condition"] = pd.Categorical(\
    df_all["Condition"],\
    categories=["Baseline", "Visual Nudge"],\
    ordered=True\
)\
\
# =========================\
# IDENTIFY COMPARISON COLUMN\
# =========================\
comparison_column = "Comparative_Reference"  # <-- change if needed\
\
if comparison_column not in df_all.columns:\
    raise ValueError("Check your column name for comparative references.")\
\
# =========================\
# COMPUTE PROPORTIONS\
# =========================\
df_comp = (\
    df_all\
    .groupby("Condition")[comparison_column]\
    .agg(["sum", "count"])\
    .reset_index()\
)\
\
df_comp.columns = ["Condition", "Success", "Total"]\
df_comp["Proportion"] = df_comp["Success"] / df_comp["Total"]\
\
# =========================\
# EXACT BINOMIAL CI\
# =========================\
ci_low = []\
ci_high = []\
\
for _, row in df_comp.iterrows():\
    result = binomtest(int(row["Success"]), int(row["Total"]))\
    ci = result.proportion_ci(confidence_level=0.95, method="exact")\
    ci_low.append(ci.low)\
    ci_high.append(ci.high)\
\
df_comp["CI_low"] = ci_low\
df_comp["CI_high"] = ci_high\
\
# =========================\
# IEEE COLORS\
# =========================\
vis_colors = \{\
    "Baseline": "#75787B",       # IEEE Cool Gray\
    "Visual Nudge": "#007377"    # IEEE Teal\
\}\
\
# =========================\
# PLOT\
# =========================\
p = (\
    ggplot(df_comp, aes(x="Proportion", y="Condition", color="Condition"))\
    \
    # Background rail\
    + geom_segment(aes(x=0, xend=1, y="Condition", yend="Condition"),\
                   color="grey90", size=5)\
    \
    # Filled rail\
    + geom_segment(aes(x=0, xend="Proportion", y="Condition", yend="Condition"),\
                   size=5)\
    \
    # Error bars\
    + geom_errorbarh(aes(xmin="CI_low", xmax="CI_high"),\
                     height=0.25,\
                     size=1.2,\
                     color="black")\
    \
    # Point\
    + geom_point(size=7, stroke=2, fill="white", shape="o")\
    \
    # Percentage label\
    + geom_text(\
        aes(label=df_comp["Proportion"].map(lambda x: f"\{x:.0%\}")),\
        ha="left",\
        nudge_x=0.02,\
        size=12\
    )\
    \
    + scale_x_continuous(\
        labels=percent_format(),\
        limits=(0, 1),\
        breaks=np.linspace(0, 1, 5)\
    )\
    \
    + scale_color_manual(values=vis_colors)\
    \
    + labs(\
        title="Effect of Visual Nudges on Cross-Submission Comparison",\
        x="Proportion of Reviews Containing Cross-Submission Comparison",\
        y=""\
    )\
    \
    + theme_minimal(base_size=14)\
    + theme(\
        legend_position="none",\
        panel_grid_minor=element_blank(),\
        panel_grid_major_y=element_blank(),\
        axis_text_y=element_text(weight="bold")\
    )\
)\
\
print(p)\
\
# =========================\
# SAVE FIGURE\
# =========================\
p.save("Figure4_Comparative_References.png", width=10, height=5, dpi=300)}
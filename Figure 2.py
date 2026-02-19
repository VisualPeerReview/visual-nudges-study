{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
# =========================\
# PACKAGES\
# =========================\
import pandas as pd\
import numpy as np\
import seaborn as sns\
import matplotlib.pyplot as plt\
import re\
\
# =========================\
# READ DATA\
# =========================\
spring = pd.read_excel("~/Desktop/IEEE Vis 2026/Spring 2025.xlsx")\
fall   = pd.read_excel("~/Desktop/IEEE Vis 2026/Fall 2025.xlsx")\
\
# Assign conditions\
spring["Condition"] = "Baseline"\
fall["Condition"]   = "Visual Nudge"\
\
# Combine datasets\
df_all = pd.concat([spring, fall], ignore_index=True)\
\
# Ensure categorical ordering\
df_all["Condition"] = pd.Categorical(\
    df_all["Condition"],\
    categories=["Baseline", "Visual Nudge"],\
    ordered=True\
)\
\
# =========================\
# PREPARE DATA\
# =========================\
# Word count function\
def count_words(text):\
    if pd.isna(text):\
        return np.nan\
    return len(re.findall(r"\\S+", str(text)))\
\
df_all["Comment_Length"] = df_all["Comments"].apply(count_words)\
\
df_clean = df_all.dropna(subset=["Comment_Length"])\
\
\
# =========================\
# VISUAL SETTINGS\
# =========================\
ieee_colors = \{\
    "Baseline": "#75787B",       # IEEE Cool Gray\
    "Visual Nudge": "#007377"    # IEEE Teal\
\}\
\
# Trim extreme outliers for display (98th percentile)\
y_limit = np.quantile(df_balanced["Comment_Length"], 0.98)\
\
# =========================\
# PLOT\
# =========================\
plt.figure(figsize=(8,5))\
\
# Violin (background distribution)\
sns.violinplot(\
    data=df_balanced,\
    x="Condition",\
    y="Comment_Length",\
    palette=ieee_colors,\
    cut=0,\
    inner=None,\
    scale="width",\
    alpha=0.12\
)\
\
# Boxplot (summary)\
sns.boxplot(\
    data=df_balanced,\
    x="Condition",\
    y="Comment_Length",\
    width=0.2,\
    showcaps=True,\
    boxprops=\{"facecolor":"white", "edgecolor":"black"\},\
    whiskerprops=\{"color":"black"\},\
    medianprops=\{"color":"black"\},\
    showfliers=False\
)\
\
# Jittered points\
sns.stripplot(\
    data=df_balanced,\
    x="Condition",\
    y="Comment_Length",\
    palette=ieee_colors,\
    jitter=0.15,\
    size=5, f\
    alpha=0.65\
)\
\
plt.ylim(0, y_limit)\
\
plt.title(\
    "Effect of Visual Nudges on Feedback Articulation",\
    fontsize=14,\
    weight="bold"\
)\
plt.xlabel("")\
plt.ylabel("Word Count")\
\
plt.tight_layout()\
plt.savefig("Effect_of_Visual_Nudges_Articulation.png", dpi=300)\
plt.show()}
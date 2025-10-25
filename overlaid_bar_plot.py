import matplotlib
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

matplotlib.use("TkAgg")

# --- User configuration ---
directory = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_per_aria"

# Map filenames to display names (update as needed)
names = {
    "forced_aligner.pkl": "MMS-FA",
    "forced_aligner_sv.pkl": "MMS-FA-SV",
    "gc.pkl": "ALT",
    "hbe.pkl": "LA-JPD",
    "schufo.pkl": "PLLA",
    "whisperx.pkl": "WhisperX",
    "whisperx_sv.pkl": "WhisperX-SV"
}

# --- Load data ---
records = []
for filename in os.listdir(directory):
    if filename.endswith(".pkl") and filename in names:
        model_name = names[filename]
        with open(os.path.join(directory, filename), "rb") as f:
            data = pickle.load(f)
        for aria_name, metrics in data.items():
            clean_aria = aria_name.replace("_", " ")  # normalize aria name
            records.append({
                "Aria": clean_aria,
                "Model": model_name,
                "RMSE": metrics["rmse"],
                "PCO": metrics["pco"]
            })

df = pd.DataFrame(records)

# Sort arias alphabetically for stable order
df = df.sort_values("Aria")

# --- Shared setup ---
sns.set_theme(style="whitegrid", context="talk")

# High-contrast, colorblind-friendly palette
palette = [
    "#1b9e77",  # green
    "#d95f02",  # orange
    "#7570b3",  # purple
    "#e7298a",  # pink
    "#66a61e",  # lime
    "#e6ab02",  # yellow
    "#a6761d"   # brown
]

model_list = sorted(df["Model"].unique())
model_colors = {m: palette[i % len(palette)] for i, m in enumerate(model_list)}

x = np.arange(df["Aria"].nunique())
bar_width = 0.6


# --- Helper plotting function ---
def plot_metric(metric: str, ylabel: str, log_scale: bool, save_name: str):
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    for idx, aria in enumerate(sorted(df["Aria"].unique())):
        sub = df[df["Aria"] == aria].sort_values(metric, ascending=False)
        for i, row in enumerate(sub.itertuples()):
            ax.bar(
                idx,
                getattr(row, metric),
                width=bar_width,
                color=model_colors[row.Model],
                edgecolor="black",
                linewidth=0.3,
                zorder=2 + i,
                label=row.Model if idx == 0 else None
            )

    if log_scale:
        ax.set_yscale("log")

    ax.set_xticks(x)
    ax.set_xticklabels(sorted(df["Aria"].unique()), rotation=45, ha="right", fontsize=10)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Aria")
    ax.set_title(f"Per-Aria {ylabel} Comparison", pad=15)
    ax.legend(title="Model", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.savefig(os.path.join(directory, save_name), dpi=300, bbox_inches="tight")
    plt.show()


# --- Plot RMSE (log scale) ---
plot_metric("RMSE", "Onset RMSE (log scale)", log_scale=True, save_name="rmse_overlaid_sorted_bar_plot_log.png")

# --- Plot PCO (no log scale) ---
plot_metric("PCO", "PCO", log_scale=False, save_name="pco_overlaid_sorted_bar_plot.png")

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

# --- Load all RMSE data ---
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
                "RMSE": metrics["rmse"]
            })

df = pd.DataFrame(records)

# Ensure consistent model order
order = ["PLLA", "LA-JPD", "ALT", "MMS-FA", "MMS-FA-SV", "WhisperX", "WhisperX-SV"]
df["Model"] = pd.Categorical(df["Model"], categories=order, ordered=True)

# Sort aria alphabetically for readability
df = df.sort_values("Aria")

# --- Pivot for plotting ---
pivot_df = df.pivot(index="Aria", columns="Model", values="RMSE").fillna(np.nan)

# --- Plot ---
sns.set_theme(style="whitegrid", context="talk")
fig, ax = plt.subplots(figsize=(13, 7))

palette = sns.color_palette("Set2", n_colors=len(order))
x = np.arange(len(pivot_df))
bar_width = 0.1  # controls spacing between bars

# Plot one bar per model, offset by width
for i, model in enumerate(order):
    if model in pivot_df.columns:
        ax.bar(
            x + i * bar_width - (len(order) * bar_width) / 2,  # center bars around aria
            pivot_df[model].values,
            width=bar_width,
            label=model,
            color=palette[i]
        )

# --- Aesthetics ---
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(pivot_df.index, rotation=45, ha="right", fontsize=10)
ax.set_ylabel("Onset RMSE (log scale)")
ax.set_xlabel("Aria")
ax.set_title("Per-Aria Onset RMSE Comparison Across Models", pad=15)

ax.legend(title="Model", bbox_to_anchor=(1.05, 1), loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig(
    os.path.join(directory, "rmse_grouped_bar_plot_log.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()

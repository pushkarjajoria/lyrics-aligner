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

# Map filenames to display names
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
df = df.sort_values("Aria")

# --- Plot subset function ---
def plot_metric_subset(metric: str, ylabel: str, log_scale: bool, save_name: str, selected_arias: list):
    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    # Filter to only selected arias
    sub_df = df[df["Aria"].isin(selected_arias)].copy()
    x_positions = np.arange(len(selected_arias))

    # Define markers per model
    markers = {
        "PLLA": "o",
        "LA-JPD": "s",
        "ALT": "D",
        "MMS-FA": "^",
        "MMS-FA-SV": "^",  # same marker, diff color
        "WhisperX": "*",
        "WhisperX-SV": "*",  # same marker, diff color
    }

    # Distinct, high-contrast colors
    colors = {
        "PLLA": "#1b9e77",
        "LA-JPD": "#d95f02",
        "ALT": "#7570b3",
        "MMS-FA": "#e7298a",
        "MMS-FA-SV": "#ad005f",
        "WhisperX": "#66a61e",
        "WhisperX-SV": "#3a570e",
    }

    # Plot each model with scatter symbols
    for model in sorted(sub_df["Model"].unique()):
        model_data = sub_df[sub_df["Model"] == model]
        y_values = []
        for aria in selected_arias:
            val = model_data.loc[model_data["Aria"] == aria, metric]
            y_values.append(val.values[0] if not val.empty else np.nan)

        ax.scatter(
            x_positions,
            y_values,
            label=model,
            marker=markers[model],
            s=90,
            color=colors[model],
            edgecolor="black",
            linewidth=0.4,
            zorder=3
        )

    if log_scale:
        ax.set_yscale("log")

    ax.set_xticks(x_positions)
    ax.set_xticklabels(selected_arias, rotation=30, ha="right", fontsize=10)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Aria")
    ax.set_title(f"Aria {ylabel} Comparison", pad=15)
    ax.legend(title="Model", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(directory, save_name), format="pdf", bbox_inches="tight")
    plt.show()


# --- Example: plot for 4 arias ---
selected_arias = ["Rigoletto Quel vecchio", "Norma Casta Diva", "Rigoletto Pari siamo", "Verdi Rigoletto Questa o Quella"]

# RMSE (log scale)
plot_metric_subset(
    metric="RMSE",
    ylabel="Onset RMSE (log scale)",
    log_scale=True,
    save_name="rmse_subset_symbol_plot.pdf",
    selected_arias=selected_arias
)

# PCO (no log scale)
plot_metric_subset(
    metric="PCO",
    ylabel="PCO",
    log_scale=False,
    save_name="pco_subset_symbol_plot.pdf",
    selected_arias=selected_arias
)

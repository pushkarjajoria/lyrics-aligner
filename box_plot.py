import matplotlib
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

matplotlib.use("TkAgg")

# --- User configuration ---
directory = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_rmse"

# Map filenames to display names (update this as needed)
names = {
    "forced_aligner.pkl": "MMS-FA",
    "forced_aligner_sv.pkl": "MMS-FA-SV",
    "gc.pkl": "ALT",
    "hbe.pkl": "LA-JPD",
    "schufo.pkl": "PLLA",
    "whisperx.pkl": "WhisperX",
    "whisperx_sv.pkl": "WhisperX-SV"
}


records = []
for filename in os.listdir(directory):
    if filename.endswith(".pkl") and filename in names:
        with open(os.path.join(directory, filename), "rb") as f:
            vals = pickle.load(f)
            if isinstance(vals, np.ndarray):
                vals = vals.tolist()
            model_name = names[filename]
            for v in vals:
                records.append({"Model": model_name, "RMSE": v})

df = pd.DataFrame(records)

order = ["PLLA", "LA-JPD", "ALT", "MMS-FA", "MMS-FA-SV", "WhisperX", "WhisperX-SV"]

sns.set_theme(style="whitegrid", context="talk")
plt.figure(figsize=(8, 6))

palette = sns.color_palette("Set2", n_colors=len(order))

sns.boxplot(data=df, x="Model", y="RMSE", order=order, palette=palette, showfliers=False)
sns.stripplot(data=df, x="Model", y="RMSE", order=order, color="black", size=3, jitter=True, alpha=0.5)

plt.yscale("log")
plt.ylabel("Onset RMSE (log scale)")
plt.xlabel("Model")
plt.title("Per-Aria Onset RMSE Comparison Across Models", pad=15)
plt.xticks(rotation=20, ha="center")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("/nethome/unknown_user/Github/lyrics-aligner/results/per_model_rmse/rmse_box_plot.png", dpi=300)

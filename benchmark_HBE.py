import pickle

from evaluate_helper import compute_alignment_metrics, print_results
import os
from pathlib import Path
import pandas as pd
import ast


def build_timestamp_cache(dataset_dir, label_directory):
    """
    Generate timestamps for all arias and save them to a pickle file.
    Handles irregular CSV rows (e.g. arrays with commas in last field).
    """
    timestamps = {}

    for csv_file in os.listdir(label_directory):
        if not csv_file.endswith(".csv"):
            continue

        # Extract aria name (e.g., "aria" from "aria_align.csv")
        aria_name = csv_file.replace("_align.csv", "")
        aria_path = Path(dataset_dir) / aria_name
        label_path = aria_path / "labels.tsv"
        csv_path = Path(label_directory) / csv_file

        if not aria_path.is_dir():
            print(f"Skipping {aria_name}: not found in dataset_dir.")
            continue

        if not label_path.exists():
            print(f"Skipping {aria_name}: missing {label_path}")
            continue

        word_onsets = []
        parsed_arrays = []

        # Read the file manually (handles variable commas)
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Split only on first comma and last comma group
                    parts = line.split(",")
                    onset = parts[0].strip()

                    # Reconstruct the last column (it may contain internal commas)
                    last_field = ",".join(parts[1:]).strip()
                    try:
                        arr = ast.literal_eval(last_field)
                    except Exception:
                        arr = []
                    word_onsets.append(onset)
                    parsed_arrays.append(arr)

        except Exception as e:
            print(f"Error reading {csv_path}: {e}")
            continue

        # Read ground truth labels
        try:
            label_df = pd.read_csv(label_path, sep="\t")
        except Exception as e:
            print(f"Error reading labels.tsv for {aria_name}: {e}")
            continue

        # Merge both
        timestamps_data = [{"start": onset, "extra": arr}
                           for onset, arr in zip(word_onsets, parsed_arrays)]

        timestamps[aria_name] = {
            "labels": label_df,
            "timestamps": timestamps_data
        }

    return timestamps


if __name__ == "__main__":
    timestamps = build_timestamp_cache("/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset", "/nethome/pjajoria/Github/lyrics-aligner/results/multilingual_predictions")
    results = compute_alignment_metrics(timestamps, tolerance=0.3)
    res_path = "/nethome/pjajoria/Github/lyrics-aligner/results/per_model_rmse"
    per_aria = results["per_aria"]
    rmse_per_aria = []
    for aria, value in per_aria.items():
        rmse_per_aria.append(value['rmse'])
    with open(f"{res_path}/hbe.pkl", "wb") as f:
        pickle.dump(rmse_per_aria, f)

    res_path_per_aria = "/nethome/pjajoria/Github/lyrics-aligner/results/per_model_per_aria"
    with open(f"{res_path_per_aria}/hbe.pkl", "wb") as f:
        pickle.dump(per_aria, f)

    print_results(results)

import pickle

from evaluate_helper import compute_alignment_metrics, print_results
import os
from pathlib import Path
import pandas as pd
import ast


def build_timestamp_cache(dataset_dir, prediction_directory):
    """
    Generate timestamps for all arias and save them to a pickle file.
    Handles irregular CSV rows (e.g. arrays with commas in last field).
    """
    timestamps = {}

    for csv_file in os.listdir(prediction_directory):
        if not csv_file.endswith(".csv"):
            continue

        # Extract aria name (e.g., "aria" from "aria_align.csv")
        aria_name = csv_file.replace(".csv", "")
        aria_path = Path(dataset_dir) / aria_name
        label_path = aria_path / "labels.tsv"
        csv_path = Path(prediction_directory) / csv_file

        if not aria_path.is_dir():
            print(f"Skipping {aria_name}: not found in dataset_dir.")
            continue

        if not label_path.exists():
            print(f"Skipping {aria_name}: missing {label_path}")
            continue

        # Read the file manually (handles variable commas)
        pred_df = pd.read_csv(csv_path, sep=",")
        onset_times = pred_df['start']
        # Read ground truth labels
        try:
            label_df = pd.read_csv(label_path, sep="\t")
        except Exception as e:
            print(f"Error reading labels.tsv for {aria_name}: {e}")
            continue

        # Merge both
        timestamps_data = [{"start": onset_times}]

        timestamps[aria_name] = {
            "labels": label_df,
            "timestamps": timestamps_data
        }

    return timestamps


if __name__ == "__main__":
    timestamps = build_timestamp_cache("/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria_Dataset", "/nethome/unknown_user/Github/lyrics-aligner/results/whisperx_sepa_vocals")
    results = compute_alignment_metrics(timestamps, tolerance=0.3)
    res_path = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_rmse"
    per_aria = results["per_aria"]
    rmse_per_aria = []
    for aria, value in per_aria.items():
        rmse_per_aria.append(value['rmse'])
    with open(f"{res_path}/whisperx_sv.pkl", "wb") as f:
        pickle.dump(rmse_per_aria, f)

    res_path_per_aria = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_per_aria"
    with open(f"{res_path_per_aria}/whisperx_sv.pkl", "wb") as f:
        pickle.dump(per_aria, f)

    print_results(results)

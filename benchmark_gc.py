import pickle

import pandas as pd
from pathlib import Path

import os

from evaluate_helper import compute_alignment_metrics, print_results


def build_timestamp_cache(dataset_dir):
    """
    Generate timestamps for all arias and save them to a pickle file.

    Args:
        dataset_dir (str): Path to the dataset directory.

    Returns:
        dict: Dictionary of timestamps for all arias, where each entry contains:
              {
                  "labels": pandas.DataFrame,
                  "timestamps": list[dict]
              }
    """
    timestamps = {}

    for aria_dir in os.listdir(dataset_dir):
        aria_path = Path(dataset_dir) / aria_dir
        if not aria_path.is_dir():
            continue

        gc_labels_path = aria_path / "text" / f"{aria_dir}_aligned_gc.txt"
        label_path = aria_path / "labels.tsv"

        try:
            with open(gc_labels_path, "r") as f:
                gc_label_lines = f.readlines()
        except FileNotFoundError:
            print(f"Could not find gc labels in {gc_labels_path}")
            continue

        word_onsets = []
        for line in gc_label_lines:
            onset = line.split(" ")[0]
            word_onsets.append(onset)

        label = pd.read_csv(label_path, sep="\t")
        timestamps[aria_dir] = {
          "labels": label,
          "timestamps": [{"start": word_onsets}]
        }
    return timestamps


if __name__ == "__main__":
    timestamps = build_timestamp_cache("/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset_gc")
    results = compute_alignment_metrics(timestamps, tolerance=0.3)
    res_path = "/nethome/pjajoria/Github/lyrics-aligner/results/per_model_rmse"
    per_aria = results["per_aria"]
    rmse_per_aria = []
    for aria, value in per_aria.items():
        rmse_per_aria.append(value['rmse'])
    with open(f"{res_path}/gc.pkl", "wb") as f:
        pickle.dump(rmse_per_aria, f)

    res_path_per_aria = "/nethome/pjajoria/Github/lyrics-aligner/results/per_model_per_aria"
    with open(f"{res_path_per_aria}/gc.pkl", "wb") as f:
        pickle.dump(per_aria, f)
    print_results(results)

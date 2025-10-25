import os
import pickle
from pathlib import Path
import pandas as pd
import torch
from evaluate_helper import compute_alignment_metrics, print_results
from ctc_forced_aligner import (
    load_audio,
    load_alignment_model,
    generate_emissions,
    preprocess_text,
    get_alignments,
    get_spans,
    postprocess_results,
)

# Configuration

# Language code (use ISO-639-1 or ISO-639-3 depending on model requirements)
LANGUAGE = "ISO-639-1"

# Select computation device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Choose model precision based on device
MODEL_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Load forced alignment model and tokenizer
ALIGNMENT_MODEL, ALIGNMENT_TOKENIZER = load_alignment_model(
    DEVICE, dtype=MODEL_DTYPE
)


def update_labels_in_pickle(dataset_dir, pickle_path):
    """
    Update only the labels in an existing timestamp pickle file.

    This function reloads the label files (labels.tsv) from the dataset directory,
    replaces the old labels in the pickle, and saves the updated pickle
    back to the same path.

    Args:
        dataset_dir (str): Path to the dataset directory.
        pickle_path (str): Path to the existing pickle file.

    Returns:
        dict: Updated timestamps dictionary with new labels.
    """
    if not os.path.exists(pickle_path):
        raise FileNotFoundError(f"Pickle file not found: {pickle_path}")

    # Load the existing pickle data
    with open(pickle_path, "rb") as f:
        timestamps = pickle.load(f)

    updated_count = 0
    skipped_count = 0

    for aria_dir in os.listdir(dataset_dir):
        aria_path = Path(dataset_dir) / aria_dir
        if not aria_path.is_dir():
            continue

        label_path = aria_path / "labels.tsv"
        if not label_path.exists():
            print(f"Skipping {aria_dir}: labels.tsv not found.")
            skipped_count += 1
            continue

        if aria_dir not in timestamps:
            print(f"Skipping {aria_dir}: not found in pickle data.")
            skipped_count += 1
            continue

        try:
            new_labels = pd.read_csv(label_path, sep="\t")
            timestamps[aria_dir]["labels"] = new_labels
            updated_count += 1
        except Exception as e:
            print(f"Error updating {aria_dir}: {e}")
            skipped_count += 1
            continue

    # Save the updated pickle file
    with open(pickle_path, "wb") as f:
        pickle.dump(timestamps, f)

    print(f"Updated labels for {updated_count} arias (skipped {skipped_count}).")
    print(f"Saved updated pickle to {pickle_path}")

    return timestamps


def get_word_timestamps(audio_path, text_path):
    """
    Generate word-level timestamps using the forced aligner.

    Args:
        audio_path (Path): Path to the audio file.
        text_path (Path): Path to the text (lyrics) file.

    Returns:
        list[dict]: A list of dictionaries, each containing:
                    {
                        "word": str,
                        "start": float,
                        "end": float
                    }
    """
    batch_size = 16

    # Load audio waveform in the same dtype and device as the alignment model
    audio_waveform = load_audio(audio_path, ALIGNMENT_MODEL.dtype, ALIGNMENT_MODEL.device)

    # Read and clean text input
    with open(text_path, "r", encoding="utf-8") as f:
        text = " ".join(line.strip() for line in f.readlines()).strip()

    # Generate emissions from the alignment model
    emissions, stride = generate_emissions(ALIGNMENT_MODEL, audio_waveform, batch_size=batch_size)

    # Tokenize and preprocess text
    tokens_starred, text_starred = preprocess_text(text, romanize=True, language=LANGUAGE)

    # Obtain alignment segments
    segments, scores, blank_token = get_alignments(emissions, tokens_starred, ALIGNMENT_TOKENIZER)

    # Convert token-level alignments to word-level spans
    spans = get_spans(tokens_starred, segments, blank_token)

    # Postprocess results into structured timestamps
    word_timestamps = postprocess_results(text_starred, spans, stride, scores)

    return word_timestamps


def build_timestamp_cache(dataset_dir, pickle_path, sepa_vocals=False):
    """
    Generate timestamps for all arias and save them to a pickle file.

    Args:
        dataset_dir (str): Path to the dataset directory.
        pickle_path (str): Path to save the pickle file.

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
        if sepa_vocals:
            audio_path = aria_path / f"separated_vocals/{aria_dir}_vocals.wav"
        else:
            audio_path = aria_path / "audio" / "song.mp3"
        text_path = aria_path / "text" / "song.txt"
        label_path = aria_path / "labels.tsv"

        if not (audio_path.exists() and text_path.exists() and label_path.exists()):
            print(f"Skipping {aria_dir}: Missing one or more required files.")
            continue

        try:
            word_timestamps = get_word_timestamps(audio_path, text_path)
            labels = pd.read_csv(label_path, sep="\t")

            timestamps[aria_dir] = {
                "labels": labels,
                "timestamps": word_timestamps
            }

        except Exception as e:
            print(f"Error processing {aria_dir}: {e}")
            continue

    # Save results to pickle
    with open(pickle_path, "wb") as f:
        pickle.dump(timestamps, f)

    print(f"Timestamps saved to {pickle_path}")
    return timestamps


def main(dataset_dir, pickle_path):
    if os.path.exists(pickle_path):
        print(f"Loading cached timestamps from {pickle_path}")
        with open(pickle_path, "rb") as f:
            timestamps = pickle.load(f)
    else:
        print("No cached file found. Generating timestamps...")
        timestamps = build_timestamp_cache(dataset_dir, pickle_path)

    results = compute_alignment_metrics(timestamps, tolerance=0.3)
    res_path = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_rmse"
    per_aria = results["per_aria"]
    rmse_per_aria = []
    for aria, value in per_aria.items():
        rmse_per_aria.append(value['rmse'])
    with open(f"{res_path}/forced_aligner.pkl", "wb") as f:
        pickle.dump(rmse_per_aria, f)

    res_path_per_aria = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_per_aria"
    with open(f"{res_path_per_aria}/forced_aligner.pkl", "wb") as f:
        pickle.dump(per_aria, f)

    print_results(results)


if __name__ == "__main__":
    dataset_dir = "/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria_Dataset/"
    # pickle_path = "/nethome/unknown_user/Github/lyrics-aligner/results/forced_aligner_timestamps_separated_vocals.pkl"
    pickle_path = "/nethome/unknown_user/Github/lyrics-aligner/results/forced_aligner_timestamps.pkl"
    # update_labels_in_pickle(dataset_dir, pickle_path)
    main(dataset_dir, pickle_path)

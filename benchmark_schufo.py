from typing import Dict, List

import os
import pickle

import torch
from torch.utils.data import DataLoader

import model
from datahandler import AriaDataset
import pandas as pd

import align
from evaluate_helper import compute_alignment_metrics, print_results


def get_alignments(dataset_path, model_path="/nethome/unknown_user/Github/lyrics-aligner/checkpoint/base/model_parameters.pth", alignment_model=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if alignment_model is None:
        print("Using baseline alignment model...")
        alignment_model = model.InformedOpenUnmix3().to(device)
        state_dict = torch.load(model_path, map_location=device)
        alignment_model.load_state_dict(state_dict)
        alignment_model.eval()

    # Load dataset and perform training/test split
    w2ph_dict_path = os.path.join(dataset_path, "word2phonemes.pickle")
    with open(w2ph_dict_path, "rb") as w2ph_file:
        w2phoneme_dict = pickle.load(w2ph_file)

    full_dataset = AriaDataset(path=dataset_path, word2phoneme_dict=w2phoneme_dict)
    # The original code used DataLoader(..., batch_size=None). Keep same signature (assuming dataset yields samples)
    dataloader = DataLoader(full_dataset, batch_size=None, batch_sampler=None, collate_fn=None, shuffle=True)

    # Load phoneme-to-index mapping (same file used by align.py)
    pickle_in = open('/nethome/unknown_user/Github/lyrics-aligner/files/phoneme2idx.pickle', 'rb')
    phoneme2idx = pickle.load(pickle_in)
    pickle_in.close()

    outputs_dir = os.path.join("/nethome/unknown_user/Github/lyrics-aligner/results/schufo")
    word_onsets_dir = os.path.join(outputs_dir, "word_onsets")
    os.makedirs(word_onsets_dir, exist_ok=True)
    onsets_map = {}
    with torch.no_grad():
        print("Evaluating the model on dataset:", dataset_path)

        for name, audio, phonemes, sr, _, words, _, _, _, _, _ in dataloader:
            audio = torch.Tensor(audio)[None, :]

            lyrics_phoneme_idx = [phoneme2idx[ph] for ph in phonemes]
            phonemes_idx = torch.tensor(lyrics_phoneme_idx, dtype=torch.float32, device=device)[None, :]

            # Predict using the baseline model
            _, scores = alignment_model((audio.to(device), phonemes_idx))
            scores = scores.cpu()

            optimal_path = align.optimal_alignment_path(scores)

            # Compute phoneme onsets: use hop_length=256 same as align.py, use sr from dataloader
            phoneme_onsets = align.compute_phoneme_onsets(optimal_path, hop_length=256, sampling_rate=sr)

            # Compute word onsets/offsets from phonemes and phoneme_onsets
            word_onsets, word_offsets = align.compute_word_alignment(phonemes, phoneme_onsets)

            # Save word-level onsets to file (one line per word: "<word>\\t<onset>")
            out_file_path = os.path.join(word_onsets_dir, f"{name}.txt")
            # save word onsets
            w_file = open(out_file_path, 'a')
            for m, word in enumerate(words):
                w_file.write(word + '\t' + str(word_onsets[m]) + '\n')
            w_file.close()

            onsets_map[name] = word_onsets

    return onsets_map


def read_second_entries(dir_path: str) -> Dict[str, List[str]]:
    """
    Read all .txt files in dir_path and return a dict:
      key -> filename without .txt
      value -> list of the second entry (index 1) from each line split by '\t'
    Lines with fewer than 2 tab-separated fields are skipped.
    """
    result: Dict[str, List[str]] = {}
    for fname in sorted(os.listdir(dir_path)):
        if not fname.lower().endswith(".txt"):
            continue
        key = os.path.splitext(fname)[0]
        file_path = os.path.join(dir_path, fname)
        values: List[str] = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            for raw_line in fh:
                line = raw_line.rstrip("\n\r")
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) < 2:
                    # skip lines that don't have a second column
                    continue
                values.append(parts[1])
        result[key] = values
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Schufo's code for forced aligment on Aria dataset")
    parser.add_argument("--dataset_path", type=str, default="/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria_Dataset")
    parser.add_argument("--model-path", type=str, default="/nethome/unknown_user/Github/lyrics-aligner/checkpoint/base/model_parameters.pth")
    args = parser.parse_args()

    # res = get_alignments(args.dataset_path, args.model_path)
    res_path = "/nethome/unknown_user/Github/lyrics-aligner/results/schufo"
    res = read_second_entries(f"{res_path}/word_onsets")
    timestamps = {}
    for k, v in res.items():
        timestamps[k] = {
          "labels": pd.read_csv(str(os.path.join(args.dataset_path, k, "labels.tsv")), sep="\t"),
          "timestamps": [{"start": v}]
        }
    results = compute_alignment_metrics(timestamps, tolerance=0.3)
    per_aria = results["per_aria"]
    rmse_per_aria = []
    rmse_res_path = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_rmse"
    for aria, value in per_aria.items():
        rmse_per_aria.append(value['rmse'])
    with open(f"{rmse_res_path}/schufo.pkl", "wb") as f:
        pickle.dump(rmse_per_aria, f)

    res_path_per_aria = "/nethome/unknown_user/Github/lyrics-aligner/results/per_model_per_aria"
    with open(f"{res_path_per_aria}/schufo.pkl", "wb") as f:
        pickle.dump(per_aria, f)
    print_results(results)


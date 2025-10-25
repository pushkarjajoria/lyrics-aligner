import os
import argparse
import pickle
import torch
import pandas as pd
import matplotlib.pyplot as plt

import model
from datahandler import AriaDataset
import align


def get_single_aria_prediction(aria_name: str, dataset_path: str, model_path: str):
    """
    Run a forward pass for a single aria using the given model and return predicted word onsets.
    """

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    alignment_model = model.InformedOpenUnmix3().to(device)
    state_dict = torch.load(model_path, map_location=device)
    alignment_model.load_state_dict(state_dict)
    alignment_model.eval()

    # Load word2phoneme dictionary
    w2ph_dict_path = os.path.join(dataset_path, "word2phonemes.pickle")
    with open(w2ph_dict_path, "rb") as f:
        w2phoneme_dict = pickle.load(f)

    # Load only the requested aria
    full_dataset = AriaDataset(path=dataset_path, word2phoneme_dict=w2phoneme_dict)
    sample = None
    for name, audio, phonemes, sr, _, words, *_ in full_dataset:
        if name == aria_name:
            sample = (name, audio, phonemes, sr, words)
            break
    if sample is None:
        raise ValueError(f"Aria '{aria_name}' not found in dataset at {dataset_path}")

    name, audio, phonemes, sr, words = sample
    audio = torch.Tensor(audio)[None, :]

    # Load phoneme2idx map
    with open('/nethome/unknown_user/Github/lyrics-aligner/files/phoneme2idx.pickle', 'rb') as f:
        phoneme2idx = pickle.load(f)

    phonemes_idx = [phoneme2idx[ph] for ph in phonemes]
    phonemes_idx = torch.tensor(phonemes_idx, dtype=torch.float32, device=device)[None, :]

    # Predict alignment
    with torch.no_grad():
        _, scores = alignment_model((audio.to(device), phonemes_idx))
        scores = scores.cpu()

        optimal_path = align.optimal_alignment_path(scores)
        phoneme_onsets = align.compute_phoneme_onsets(optimal_path, hop_length=256, sampling_rate=sr)
        word_onsets, _ = align.compute_word_alignment(phonemes, phoneme_onsets)

    return words, word_onsets


def plot_alignment_scatter(aria_name: str, dataset_path: str, predictions_dir: str, output_dir: str, model_path: str = None):
    """
    Plot a scatter plot comparing predicted and ground-truth word onsets for a single aria.
    """

    # Ground-truth labels
    aria_dir = os.path.join(dataset_path, aria_name)
    labels_path = os.path.join(aria_dir, "labels.tsv")
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Ground truth file not found: {labels_path}")

    gt_df = pd.read_csv(labels_path, sep="\t")
    gt_words = gt_df["Text"].tolist()
    gt_starts = gt_df["Start Time"].tolist()

    # Get predicted onsets either from model or from saved outputs
    if model_path:
        print(f"Using model predictions from {model_path}")
        pred_words, pred_starts = get_single_aria_prediction(aria_name, dataset_path, model_path)
    else:
        pred_file = os.path.join(predictions_dir, f"{aria_name}.txt")
        if not os.path.exists(pred_file):
            raise FileNotFoundError(f"Predicted onset file not found: {pred_file}")
        pred_words, pred_starts = [], []
        with open(pred_file, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue
                pred_words.append(parts[0])
                pred_starts.append(float(parts[1]))

    # Align by minimum length
    n = min(len(gt_starts), len(pred_starts))
    gt_starts = gt_starts[:n]
    pred_starts = pred_starts[:n]

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{aria_name}.png")

    # Scatter plot
    plt.figure(figsize=(7, 7))
    plt.scatter(gt_starts, pred_starts, color="blue", alpha=0.6, s=20, label="Predicted vs Ground Truth")
    plt.plot([min(gt_starts), max(gt_starts)], [min(gt_starts), max(gt_starts)], 'r--', label="Ideal (y = x)")
    plt.xlabel("Ground Truth Onset (s)")
    plt.ylabel("Predicted Onset (s)")
    plt.title(f"Word Onset Alignment: {aria_name}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Scatter plot saved to: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot scatter plot comparing predicted vs ground-truth word onsets.")
    parser.add_argument("--aria_name", type=str, required=True, help="Name of the aria to visualize.")
    parser.add_argument("--dataset_path", type=str, default="/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria_Dataset")
    parser.add_argument("--predictions_dir", type=str, default="/nethome/unknown_user/Github/lyrics-aligner/results/schufo/word_onsets")
    parser.add_argument("--out_path", type=str, default="/nethome/unknown_user/Github/lyrics-aligner/results/plots/scatter_plots")
    parser.add_argument("--model_path", type=str, default=None, help="Path to model checkpoint. If provided, run inference.")
    args = parser.parse_args()

    plot_alignment_scatter(
        aria_name=args.aria_name,
        dataset_path=args.dataset_path,
        predictions_dir=args.predictions_dir,
        output_dir=args.out_path,
        model_path=args.model_path,
    )

"""
python plot_alignment_scatter.py --aria_name Norma_Casta_Diva --model_path /nethome/unknown_user/Github/lyrics-aligner/checkpoint/big_testset_0210_1529/model_final.pth --out_path /nethome/unknown_user/Github/lyrics-aligner/results/plots
"""

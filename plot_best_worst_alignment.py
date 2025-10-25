import matplotlib
import os
import pickle
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


def plot_best_worst_alignment(
    aria_name_best: str,
    checkpoint_file_best: str,
    aria_name_worst: str,
    checkpoint_file_worst: str,
    output_dir: str = "./alignment_plots"
):
    """
    Create scatter plots comparing ground truth vs predicted word onsets
    for the best and worst improvement arias in a single fold.

    Args:
        aria_name_best (str): Name of aria with best improvement.
        checkpoint_file_best (str): Path to pickle results file for best aria.
        aria_name_worst (str): Name of aria with worst improvement.
        checkpoint_file_worst (str): Path to pickle results file for worst aria.
        output_dir (str): Directory to save output plots.
    """

    def load_alignment_data(pkl_path, aria_name):
        """Helper to load GT and both model predictions from .pkl."""
        if not os.path.exists(pkl_path):
            raise FileNotFoundError(f"File not found: {pkl_path}")

        with open(pkl_path, "rb") as f:
            results = pickle.load(f)

        if aria_name not in results["per_file"]:
            raise KeyError(f"{aria_name} not found in {pkl_path}")

        entry = results["per_file"][aria_name]
        gt = entry["ground_truth"]["start_times"]
        trained = entry["trained_model"]["onsets"]
        baseline = entry["baseline_model"]["onsets"]

        # Align by min length to avoid mismatched sequence lengths
        n = min(len(gt), len(trained), len(baseline))
        gt = gt[:n]
        trained = trained[:n]
        baseline = baseline[:n]

        return gt, trained, baseline

    def plot_alignment(gt, trained, baseline, aria_name, tag):
        """Plot a single scatter plot for one aria."""
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{aria_name}_{tag}.png")

        plt.figure(figsize=(7, 7))
        plt.scatter(gt, baseline, alpha=0.6, s=25, color="gray", label="Baseline")
        plt.scatter(gt, trained, alpha=0.6, s=25, color="tab:blue", label="Finetuned")
        plt.plot([min(gt), max(gt)], [min(gt), max(gt)], "r--", label="Ideal (y=x)")
        plt.xlabel("Ground Truth Onset (s)")
        plt.ylabel("Predicted Onset (s)")
        plt.title(f"{aria_name} ({tag})")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        # plt.show()
        print(f"Saved scatter plot: {out_path}")

    # Load data
    gt_best, trained_best, baseline_best = load_alignment_data(checkpoint_file_best, aria_name_best)
    gt_worst, trained_worst, baseline_worst = load_alignment_data(checkpoint_file_worst, aria_name_worst)

    # Plot both
    plot_alignment(gt_best, trained_best, baseline_best, aria_name_best, "best")
    plot_alignment(gt_worst, trained_worst, baseline_worst, aria_name_worst, "worst")


if __name__ == "__main__":
    best_aria = "Puccini_Turandot_Nessun_dorma"
    best_ckpt_file = "results/augmentation1810_1800_44.pkl"

    worst_aria = "Verdi_Rigoletto_Caro_Nome"
    worst_ckpt_file = "results/augmentation1810_1800_43.pkl"

    plot_best_worst_alignment(best_aria, best_ckpt_file, worst_aria, worst_ckpt_file, output_dir="/nethome/unknown_user/Github/lyrics-aligner/results/plots/finetuned")

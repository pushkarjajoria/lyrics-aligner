import pickle
import numpy as np
from pathlib import Path

from eval_model import evaluate_alignment

# Hardcoded 5 folds
pkl_files = [
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_42.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_43.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_44.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_45.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1910_2352_46.pkl",
]


def update_results_file(pkl_path):
    """
    Add RMSE, MAE, MedAE, and PCO to per-file and summary sections
    if they do not already exist.
    """
    with open(pkl_path, "rb") as f:
        results = pickle.load(f)

    updated = False
    trained_metrics = {"mse": [], "rmse": [], "mae": [], "medae": [], "pco": []}
    baseline_metrics = {"mse": [], "rmse": [], "mae": [], "medae": [], "pco": []}

    for name, entry in results["per_file"].items():
        gt = entry["ground_truth"]["start_times"]

        # Trained model
        trained = entry["trained_model"]
        if "rmse" not in trained:  # update only if missing
            updated = True
            rmse, mae, medae, pco = evaluate_alignment(gt, trained["onsets"])
            trained.update({"rmse": rmse, "mae": mae, "medae": medae, "pco": pco})

        # Baseline model
        baseline = entry["baseline_model"]
        if "rmse" not in baseline:
            updated = True
            rmse, mae, medae, pco = evaluate_alignment(gt, baseline["onsets"])
            baseline.update({"rmse": rmse, "mae": mae, "medae": medae, "pco": pco})

        # Collect metrics for summary
        for _, model_dict, metrics_dict in [
            ("trained", trained, trained_metrics),
            ("baseline", baseline, baseline_metrics),
        ]:
            metrics_dict["mse"].append(model_dict["mse"])
            metrics_dict["rmse"].append(model_dict["rmse"])
            metrics_dict["mae"].append(model_dict["mae"])
            metrics_dict["medae"].append(model_dict["medae"])
            metrics_dict["pco"].append(model_dict["pco"])

    # Update summary
    results["summary"] = {
        "trained_model": {m: float(np.mean(v)) for m, v in trained_metrics.items()},
        "baseline_model": {m: float(np.mean(v)) for m, v in baseline_metrics.items()},
    }

    if updated:
        with open(pkl_path, "wb") as f:
            pickle.dump(results, f)
        print(f"Updated {Path(pkl_path).name}")
    else:
        print(f"No update needed for {Path(pkl_path).name}")

    return results


def print_results_summary(results, name):
    """Prints the metric summary for one file (fold)."""
    print(f"\n{name}")
    print("  Metric        |  Trained   |  Baseline")
    print("  ---------------+------------+-----------")
    for metric in ["mse", "rmse", "mae", "medae", "pco"]:
        t_val = results["summary"]["trained_model"][metric]
        b_val = results["summary"]["baseline_model"][metric]
        print(f"  {metric:<12} | {t_val:10.6f} | {b_val:10.6f}")


def print_individual_arias(results, name):
    """
    Print per-aria (test sample) metrics for both models.
    Useful for debugging and comparing performance on each aria across folds.
    """
    print(f"\nIndividual aria results for {name}")
    print("  Aria Name                     |  Trained RMSE  |  Baseline RMSE  |  Trained MAE  |  Baseline MAE  |  Trained PCO  |  Baseline PCO")
    print("  ------------------------------+----------------+-----------------+----------------+----------------+----------------+----------------")

    for aria_name, entry in results["per_file"].items():
        t = entry["trained_model"]
        b = entry["baseline_model"]
        print(
            f"  {aria_name:<30} |"
            f" {t['rmse']:.4f}         | {b['rmse']:.4f}          |"
            f" {t['mae']:.4f}         | {b['mae']:.4f}          |"
            f" {t['pco']:.2f}         | {b['pco']:.2f}"
        )


def compute_overall_stats(all_results):
    """Compute mean ± SE across folds for each metric and model."""
    models = ["trained_model", "baseline_model"]
    metrics = ["rmse", "mae", "medae", "pco"]

    overall = {m: {} for m in models}
    for model in models:
        for metric in metrics:
            vals = [r["summary"][model][metric] for r in all_results]
            mean = np.mean(vals)
            se = np.std(vals, ddof=1) / np.sqrt(len(vals))
            overall[model][metric] = (mean, se)
    return overall


def print_latex_table(overall):
    """Print LaTeX table entries for trained and baseline models."""
    for model_label, model_key in [("Finetuned", "trained_model"), ("Baseline", "baseline_model")]:
        metrics = overall[model_key]
        latex_table_entry = (
            f"${metrics['rmse'][0]:.2f}_{{\\pm {metrics['rmse'][1]:.1f}}}$ & "
            f"${metrics['mae'][0]:.2f}_{{\\pm {metrics['mae'][1]:.1f}}}$ & "
            f"${metrics['medae'][0]:.2f}_{{\\pm {metrics['medae'][1]:.1f}}}$ & "
            f"${metrics['pco'][0]:.2f}_{{\\pm {metrics['pco'][1]:.1f}}}$  \\\\"
        )
        print(f"\n{model_label} model LaTeX table entry:")
        print(latex_table_entry)


def main():
    all_results = []
    for pkl_path in pkl_files:
        results = update_results_file(pkl_path)
        print_results_summary(results, Path(pkl_path).name)
        print_individual_arias(results, Path(pkl_path).name)
        all_results.append(results)

    overall = compute_overall_stats(all_results)
    print_latex_table(overall)


if __name__ == "__main__":
    main()

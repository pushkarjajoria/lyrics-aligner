import pickle
import numpy as np
from pathlib import Path
import torch

# Hardcoded list of pickle result files (your 4 folds)
pkl_files = [
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_42.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_43.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_44.pkl",
    "/nethome/unknown_user/Github/lyrics-aligner/results/augmentation1810_1800_45.pkl",
]


def evaluate_alignment(labels, predictions, tolerance=0.3):
    """
    Compute alignment error metrics between ground-truth times and predicted times.

    Args:
        labels (array-like): Ground-truth time points (e.g. onsets).
        predictions (array-like): Predicted time points (same shape as labels).
        tolerance (float): Tolerance in seconds for PCO (percentage of correct onsets).

    Returns:
        rmse (float): Root-mean-squared error.
        mae (float): Mean absolute error.
        medae (float): Median absolute error.
        pco (float): Percentage of correct onsets within tolerance (in %).
    """
    labels = np.array(labels)
    predictions = np.array(predictions)

    errors = predictions - labels
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(errors))
    medae = np.median(np.abs(errors))
    pco = np.mean(np.abs(errors) <= tolerance) * 100.0
    return rmse, mae, medae, pco


def update_results_file(pkl_path):
    """Add RMSE, MAE, MedAE, and PCO to per-file and summary parts of one pickle."""
    with open(pkl_path, "rb") as f:
        results = pickle.load(f)

    trained_metrics = {"mse": [], "rmse": [], "mae": [], "medae": [], "pco": []}
    baseline_metrics = {"mse": [], "rmse": [], "mae": [], "medae": [], "pco": []}

    for name, entry in results["per_file"].items():
        gt = entry["ground_truth"]["start_times"]

        # --- trained model ---
        preds_tr = entry["trained_model"]["onsets"]
        mse_tr = entry["trained_model"]["mse"]
        rmse_tr, mae_tr, medae_tr, pco_tr = evaluate_alignment(gt, preds_tr)
        entry["trained_model"].update({
            "rmse": rmse_tr,
            "mae": mae_tr,
            "medae": medae_tr,
            "pco": pco_tr,
        })

        # --- baseline model ---
        preds_bl = entry["baseline_model"]["onsets"]
        mse_bl = entry["baseline_model"]["mse"]
        rmse_bl, mae_bl, medae_bl, pco_bl = evaluate_alignment(gt, preds_bl)
        entry["baseline_model"].update({
            "rmse": rmse_bl,
            "mae": mae_bl,
            "medae": medae_bl,
            "pco": pco_bl,
        })

        # accumulate metrics
        trained_metrics["mse"].append(mse_tr)
        trained_metrics["rmse"].append(rmse_tr)
        trained_metrics["mae"].append(mae_tr)
        trained_metrics["medae"].append(medae_tr)
        trained_metrics["pco"].append(pco_tr)

        baseline_metrics["mse"].append(mse_bl)
        baseline_metrics["rmse"].append(rmse_bl)
        baseline_metrics["mae"].append(mae_bl)
        baseline_metrics["medae"].append(medae_bl)
        baseline_metrics["pco"].append(pco_bl)

    # Compute fold summary stats (mean across test samples)
    results["summary"] = {
        "trained_model": {metric: float(np.mean(vals)) for metric, vals in trained_metrics.items()},
        "baseline_model": {metric: float(np.mean(vals)) for metric, vals in baseline_metrics.items()},
    }

    # Save updated pickle in place
    with open(pkl_path, "wb") as f:
        pickle.dump(results, f)

    # Print summary table
    print(f"\nUpdated: {Path(pkl_path).name}")
    print("  Metric        |  Trained   |  Baseline")
    print("  ---------------+------------+-----------")
    for metric in ["mse", "rmse", "mae", "medae", "pco"]:
        t_val = results["summary"]["trained_model"][metric]
        b_val = results["summary"]["baseline_model"][metric]
        print(f"  {metric:<12} | {t_val:10.6f} | {b_val:10.6f}")


if __name__ == "__main__":
    for pkl_path in pkl_files:
        update_results_file(pkl_path)

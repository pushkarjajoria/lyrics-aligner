import numpy as np
from tabulate import tabulate


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
    # Convert inputs to numpy arrays
    labels = np.array(labels, dtype=float)
    predictions = np.array(predictions, dtype=float)

    if labels.shape != predictions.shape:
        raise ValueError("Labels and predictions must have the same length")

    # Compute errors
    errors = predictions - labels
    abs_errors = np.abs(errors)

    rmse = np.sqrt(np.mean(errors ** 2))
    mae = np.mean(abs_errors)
    medae = np.median(abs_errors)
    # Percentage of predictions within tolerance window
    pco = np.mean(abs_errors < tolerance) * 100.0  # as percentage

    return rmse, mae, medae, pco


def mean_std_se(arr):
    """Helper: Compute mean, standard deviation, and standard error of an array."""
    arr = np.array(arr, dtype=float)
    mean = np.mean(arr)
    std = np.std(arr, ddof=1) if len(arr) > 1 else 0.0
    se = std / np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, std, se


def compute_alignment_metrics(timestamps, tolerance=0.3):
    """
    Compute per-aria and overall alignment metrics using evaluate_alignment.

    Args:
        timestamps (dict): {aria_name: {"labels": DataFrame, "timestamps": list of dicts}}
        tolerance (float): Tolerance window for PCO (in seconds).

    Returns:
        dict: {
            "overall": {"rmse": (mean, se), "mae": (mean, se), "medae": (mean, se), "pco": (mean, se)},
            "per_aria": {aria: {"rmse": ..., "mae": ..., "medae": ..., "pco": ...}, ...},
            "best": {"aria": best_aria_name, "rmse": best_rmse},
            "worst": {"aria": worst_aria_name, "rmse": worst_rmse}
        }
    """
    per_aria = {}
    all_rmse, all_mae, all_medae, all_pco = [], [], [], []

    for aria, data in timestamps.items():
        labels_df = data["labels"]
        preds = data["timestamps"]
        # Extract start times from labels and predictions
        label_times = np.array(labels_df["Start Time"], dtype=float)
        pred_times = np.array([p["start"] for p in preds], dtype=float)

        if len(pred_times.shape) > 1:
            pred_times = pred_times.squeeze()

        if len(label_times) != len(pred_times):
            print(f"Invalid prediction array for Aria: {aria}")
            continue
        # Compute metrics for this aria
        rmse, mae, medae, pco = evaluate_alignment(label_times, pred_times, tolerance=tolerance)
        per_aria[aria] = {"rmse": rmse, "mae": mae, "medae": medae, "pco": pco}
        all_rmse.append(rmse)
        all_mae.append(mae)
        all_medae.append(medae)
        all_pco.append(pco)

    # Compute overall mean and standard error for each metric
    overall = {}
    for metric_vals, name in zip([all_rmse, all_mae, all_medae, all_pco],
                                 ["rmse", "mae", "medae", "pco"]):
        if metric_vals:
            mean, std, se = mean_std_se(metric_vals)
        else:
            mean, std, se = float('nan'), float('nan'), float('nan')
        overall[name] = (mean, se)

    # Identify best and worst aria by RMSE
    if per_aria:
        best_aria = min(per_aria, key=lambda a: per_aria[a]["rmse"])
        worst_aria = max(per_aria, key=lambda a: per_aria[a]["rmse"])
        best_rmse = per_aria[best_aria]["rmse"]
        worst_rmse = per_aria[worst_aria]["rmse"]
    else:
        best_aria = worst_aria = None
        best_rmse = worst_rmse = float('nan')

    return {
        "overall": overall,
        "per_aria": per_aria,
        "best": {"aria": best_aria, "rmse": best_rmse},
        "worst": {"aria": worst_aria, "rmse": worst_rmse},
    }


def print_results(results):
    """Print aggregated and per-aria results in a tabular format."""
    overall = results["overall"]
    per_aria = results["per_aria"]
    best = results["best"]
    worst = results["worst"]

    print("\n=== Overall Metrics (Mean ± SE) ===")
    print(f"RMSE  : {overall['rmse'][0]:.6f} ± {overall['rmse'][1]:.6f}")
    print(f"MAE   : {overall['mae'][0]:.6f} ± {overall['mae'][1]:.6f}")
    print(f"MedAE : {overall['medae'][0]:.6f} ± {overall['medae'][1]:.6f}")
    print(f"PCO   : {overall['pco'][0]:.2f}% ± {overall['pco'][1]:.2f}%")
    print(f"\nBest RMSE  : {best['rmse']:.6f} ({best['aria']})")
    print(f"Worst RMSE : {worst['rmse']:.6f} ({worst['aria']})\n")

    latex_table_entry = (
        f"${overall['rmse'][0]:.2f}_{{\\pm {overall['rmse'][1]:.1f}}}$ & "
        f"${overall['mae'][0]:.2f}_{{\\pm {overall['mae'][1]:.1f}}}$ & "
        f"${overall['medae'][0]:.2f}_{{\\pm {overall['medae'][1]:.1f}}}$ & "
        f"${overall['pco'][0]:.2f}_{{\\pm {overall['pco'][1]:.1f}}}$  \\\\"
    )

    print("LaTeX table entry:")
    print(latex_table_entry)

    # Per-aria table
    table_data = [
        [
            aria,
            f"{vals['rmse']:.6f}",
            f"{vals['mae']:.6f}",
            f"{vals['medae']:.6f}",
            f"{vals['pco']:.2f}%"
        ]
        for aria, vals in per_aria.items()
    ]
    print("=== Per-Aria Metrics ===")
    print(tabulate(table_data, headers=["Aria", "RMSE", "MAE", "MedAE", "PCO"], tablefmt="github"))

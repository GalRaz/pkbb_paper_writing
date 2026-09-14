"""Reconstruct the paper's infant split-half cross-validated RMSE/R2 protocol.

NOTE (2026-09-13): the paper's exact CV code is not in the repo and its
per-parameter CV values are not reproducible from the archived model output
(linked_aligned_eig_unscaled_onlyanimals.csv: 324 param_ids, only 92 with
usable condition tables vs n=162 in the precomputed resnet50_EIG_CV.csv), so
absolute RMSEs are NOT comparable to published Table 1 — `cv_rmse_r2` is used
for relative comparisons within our pipeline (audit memo 2026-08-19). The
July-session claim that this script reproduced 3.939/3.696/0.457 exactly does
not hold under the corrected (test-trials-only) human means. The linking slope
is constrained >= 0, matching the paper's colf_nlxb lower bound.
"""
import os
import numpy as np
import pandas as pd

DATA = os.environ.get("RANCH_ROOT", "/Users/mcfrank/Projects/ranch") + "/pkbb_paper_writing/data/infants"
TYPE_MAP = {"fam": "background", "nov": "deviant"}


def human_condition_means():
    d = pd.read_csv(f"{DATA}/exp1.csv", low_memory=False)
    # TEST trials only: exp1.csv also holds exposure-phase rows (fam_or_test=='fam',
    # LT = total looking during the exposure phase), which must not enter the
    # test-trial condition means (audit 2026-08-19; matches the paper's Rmd).
    d = d[(~d["exclude"]) & (d["fam_or_test"] == "test")].copy()
    d["trial_type"] = d["test_type"].map(TYPE_MAP)
    d["trial_number"] = d["fam_duration"] + 1
    d["half"] = np.where(d["block_num"] % 2 == 0, "even", "odd")
    # condition mean LT per half
    g = (d.groupby(["trial_type", "trial_number", "half"])["LT"]
         .mean().reset_index())
    odd = g[g.half == "odd"].drop(columns="half").rename(columns={"LT": "LT_odd"})
    even = g[g.half == "even"].drop(columns="half").rename(columns={"LT": "LT_even"})
    return odd.merge(even, on=["trial_type", "trial_number"], how="inner")


def _fit_predict(x_train, y_train, x_test):
    X = np.c_[np.ones(len(x_train)), x_train]
    b, *_ = np.linalg.lstsq(X, y_train, rcond=None)
    if b[1] < 0:    # slope >= 0, as in the paper's colf_nlxb lower bound
        return np.full(np.shape(x_test), y_train.mean())
    return b[0] + b[1] * x_test


def cv_rmse_r2(model_cond, human):
    """model_cond: DataFrame [trial_type, trial_number, mean_sample].
    Returns (rmse, r2):
      * rmse -- split-half cross-validated (fit scale on one block-half,
                evaluate RMSE on the other; average the two folds).
      * r2   -- squared Pearson correlation between model condition means and
                mean (odd+even) human LT, full-data fit (matches the paper's
                Table-1 R2; validated best R2 ~ 0.435 vs published 0.457)."""
    j = human.merge(model_cond, on=["trial_type", "trial_number"], how="inner")
    if len(j) < 4 or j["mean_sample"].std() == 0:
        return np.nan, np.nan
    x = j["mean_sample"].values
    rmses = []
    for train, test in [("LT_odd", "LT_even"), ("LT_even", "LT_odd")]:
        pred = _fit_predict(x, j[train].values, x)
        rmses.append(np.sqrt(np.mean((j[test].values - pred) ** 2)))
    y_full = 0.5 * (j["LT_odd"].values + j["LT_even"].values)
    r2 = np.corrcoef(x, y_full)[0, 1] ** 2
    return np.mean(rmses), r2


def run_over_params(linked_aligned_path, human):
    la = pd.read_csv(linked_aligned_path).dropna(subset=["trial_number"])
    la["trial_number"] = la["trial_number"].astype(int)
    rows = []
    for pid, g in la.groupby("param_id"):
        rmse, r2 = cv_rmse_r2(g[["trial_type", "trial_number", "mean_sample"]], human)
        if not np.isnan(rmse):
            rows.append((pid, rmse, r2))
    return pd.DataFrame(rows, columns=["param_id", "rmse", "r2"])


if __name__ == "__main__":
    human = human_condition_means()
    print("conditions:", len(human))
    res = run_over_params(
        f"{DATA}/unscaled_model_data/linked_aligned_eig_unscaled_onlyanimals.csv", human)
    print(f"\nRECONSTRUCTED split-half CV over paper's EIG model output:")
    print(f"  n param   = {len(res)}")
    print(f"  mean RMSE = {res.rmse.mean():.3f}   best RMSE = {res.rmse.min():.3f}")
    print(f"  best R2   = {res.r2.max():.3f}")
    print(f"\nPAPER (Table 1, infant EIG): mean RMSE 3.939  best RMSE 3.696  best R2 0.457")
    # compare directly against the paper's precomputed CV file
    cv = pd.read_csv(f"{DATA}/crossvalidation/resnet50_EIG_CV.csv")
    print(f"paper precomputed CV file:   mean RMSE {cv.rmse.mean():.3f}  best {cv.rmse.min():.3f}  best R2 {cv.r2.max():.3f}  (n={len(cv)})")

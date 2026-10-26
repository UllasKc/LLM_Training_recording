"""
Build the four UC1 pipeline notebooks (without outputs) into
recording_workspace/UC1_Cross_Sell/Deliverables/2_Code/.

The notebooks are the team's "existing pipeline" that the expert runs, debugs and
completes on camera. They deliberately contain the planted bugs documented in
use_cases/UC1_Planted_Bugs_Answer_Key.md. Do NOT open this script on camera.

Usage:  python prep/build_uc1_notebooks.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "recording_workspace" / "UC1_Cross_Sell" / "Deliverables" / "2_Code"

KERNEL = {"name": "ds-venv", "display_name": "Python 3.12 (ds-venv)", "language": "python"}


def md(text):
    return ("markdown", text)


def code(text):
    return ("code", text)


NB01 = [
    md("# 01 · Data preprocessing\n"
       "Cleans the raw 30-Jun-2026 customer snapshot (`input 1`) and writes the cleaned dataset "
       "(**artifact 2**) and a data-quality log (**artifact 3**).\n\n"
       "**Run order:** 01 → 02 → 03 → 04"),
    code('import numpy as np\n'
         'import pandas as pd\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'pd.set_option("display.max_columns", 40)\n'
         'dq_log = []\n'
         '\n'
         '\n'
         'def log(step, rows_affected, action):\n'
         '    dq_log.append({"step": step, "rows_affected": int(rows_affected), "action": action})\n'
         '    print(f"{step:<28} {rows_affected:>6,} rows  -> {action}")'),
    md("## 1. Load and profile"),
    code('raw = pd.read_csv(cfg.RAW_FILE)\n'
         'print(f"{raw.shape[0]:,} rows x {raw.shape[1]} columns | unique customers: {raw[\'customer_id\'].nunique():,}")\n'
         'print(f"Target rate: {raw[cfg.TARGET].mean():.1%}")\n'
         'raw.head()'),
    code('missing = raw.isna().mean().mul(100).round(1)\n'
         'missing[missing > 0].sort_values(ascending=False).to_frame("% missing")'),
    code('raw.describe().T[["min", "50%", "max"]]'),
    md("## 2. Duplicates (CRM merge)"),
    code('df = raw.copy()\n'
         'n_exact = df.duplicated().sum()\n'
         'df = df.drop_duplicates()\n'
         'log("exact duplicates", n_exact, "dropped")\n'
         '\n'
         'n_conflict = df["customer_id"].duplicated().sum()\n'
         'df = df.drop_duplicates(subset="customer_id", keep="first")\n'
         'log("conflicting customer rows", n_conflict, "kept first record (no update timestamp)")\n'
         '\n'
         'assert df["customer_id"].is_unique\n'
         'print(f"{len(df):,} customers")'),
    md("## 3. Dates and tenure"),
    code('df["customer_since"] = pd.to_datetime(df["customer_since"], format="%Y-%m-%d")'),
    code('snapshot = pd.Timestamp(cfg.SNAPSHOT_DATE)\n'
         'months = (snapshot.year - df["customer_since"].dt.year) * 12 + (snapshot.month - df["customer_since"].dt.month)\n'
         'bad_tenure = df["tenure_months"] < 0\n'
         'df.loc[bad_tenure, "tenure_months"] = months[bad_tenure]\n'
         'log("negative tenure", bad_tenure.sum(), "recomputed from customer_since")'),
    md("## 4. Category labels"),
    code('REGION_FIXES = {"n.": "north", "w.": "west"}\n'
         'PRODUCT_FIXES = {"current acct": "current account", "savings": "savings account",\n'
         '                 "cc": "credit card", "p. loan": "personal loan"}\n'
         '\n'
         'orig_region, orig_product = df["region"].copy(), df["primary_product"].copy()\n'
         'df["region"] = df["region"].str.lower().replace(REGION_FIXES).str.title()\n'
         'df["primary_product"] = df["primary_product"].str.strip().str.lower().replace(PRODUCT_FIXES).str.title()\n'
         '\n'
         'assert df["region"].nunique() == 5, f"unexpected regions: {sorted(df[\'region\'].unique())}"\n'
         'assert df["primary_product"].nunique() == 5, f"unexpected products: {sorted(df[\'primary_product\'].unique())}"\n'
         'log("region labels", (orig_region != df["region"]).sum(), "normalised to 5 regions")\n'
         'log("product labels", (orig_product != df["primary_product"]).sum(), "normalised to 5 products")'),
    md("## 5. Impossible and sentinel values"),
    code('bad_age = ~df["age"].between(18, 100)\n'
         'df.loc[bad_age, "age"] = np.nan\n'
         'log("age outside 18-100", bad_age.sum(), "set to missing (system defaults 0 / 999)")\n'
         '\n'
         'bad_balance = df["avg_monthly_balance"] == -99999\n'
         'df.loc[bad_balance, "avg_monthly_balance"] = np.nan\n'
         'log("balance = -99999", bad_balance.sum(), "set to missing (sentinel)")'),
    md("## 6. Missing values"),
    code('df.groupby("customer_segment")["monthly_income"].apply(lambda s: s.isna().mean()).map("{:.1%}".format)'),
    code('# not missing at random (Mass segment) -> keep the signal as a flag, impute within segment\n'
         'df["income_missing"] = df["monthly_income"].isna().astype(int)\n'
         'df["monthly_income"] = df["monthly_income"].fillna(\n'
         '    df.groupby("customer_segment")["monthly_income"].transform("median"))\n'
         'log("monthly_income missing", df["income_missing"].sum(), "flag + segment median")\n'
         '\n'
         '# structural: open rate is only tracked when emails were sent (opted-in customers)\n'
         'print(pd.crosstab(df["marketing_opt_in"], df["email_open_rate"].isna().rename("open_rate_missing")))\n'
         'n = df["email_open_rate"].isna().sum()\n'
         'df["email_open_rate"] = df["email_open_rate"].fillna(0.0)\n'
         'log("email_open_rate missing", n, "0 = not emailed (opted out)")\n'
         '\n'
         'df["never_contacted"] = df["days_since_last_contact"].isna().astype(int)\n'
         'df["days_since_last_contact"] = df["days_since_last_contact"].fillna(365)\n'
         'log("days_since_last_contact", df["never_contacted"].sum(), "never contacted -> flag + 365")'),
    md("## 7. Save"),
    code('df.to_csv(cfg.CLEAN_FILE, index=False)\n'
         'pd.DataFrame(dq_log).to_csv(cfg.DQ_LOG_FILE, index=False)\n'
         'print(f"Saved {len(df):,} rows -> {cfg.CLEAN_FILE.name}")\n'
         'print(f"Saved {len(dq_log)} log entries -> {cfg.DQ_LOG_FILE.name}")\n'
         'print("Still missing (handled in the model pipelines):", df.isna().sum()[lambda s: s > 0].to_dict())'),
]

NB02 = [
    md("# 02 · Model training\n"
       "Stratified train/test split (**artifact 4**), 5-fold cross-validated comparison of a logistic-regression "
       "baseline and gradient boosting **on the training set only**, then fits both and saves them "
       "(**artifact 5**). The test set stays untouched until notebook 03."),
    code('import joblib\n'
         'import pandas as pd\n'
         'from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'features = cfg.feature_columns(df)\n'
         'print(f"{len(df):,} customers | {len(features)} features")\n'
         'print("Excluded:", cfg.EXCLUDED)'),
    md("## 1. Stratified train / test split"),
    code('train_df, test_df = train_test_split(df, test_size=0.2, stratify=df[cfg.TARGET], random_state=cfg.RANDOM_STATE)\n'
         'print(f"train {len(train_df):,} ({train_df[cfg.TARGET].mean():.1%} positive) | "\n'
         '      f"test {len(test_df):,} ({test_df[cfg.TARGET].mean():.1%} positive)")\n'
         '\n'
         'split = pd.concat([train_df[["customer_id"]].assign(split="train"),\n'
         '                   test_df[["customer_id"]].assign(split="test")])\n'
         'split.to_csv(cfg.SPLIT_FILE, index=False)'),
    md("## 2. Cross-validated comparison (training set)"),
    code('cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=cfg.RANDOM_STATE)\n'
         'X_train, y_train = train_df[features], train_df[cfg.TARGET]\n'
         'candidates = {"baseline_logreg": cfg.build_baseline(df),\n'
         '              "gradient_boosting": cfg.build_gradient_boosting(df)}\n'
         '\n'
         'cv_rows = []\n'
         'for name, model in candidates.items():\n'
         '    s = cross_validate(model, X_train, y_train, cv=cv, scoring=["roc_auc", "average_precision"],\n'
         '                       error_score="raise")\n'
         '    cv_rows.append({"model": name, "cv_roc_auc": s["test_roc_auc"].mean(),\n'
         '                    "cv_pr_auc": s["test_average_precision"].mean()})\n'
         'pd.DataFrame(cv_rows).set_index("model").round(3)'),
    md("## 3. Fit on the full training set and save"),
    code('cfg.MODEL_DIR.mkdir(exist_ok=True)\n'
         'for name, model in candidates.items():\n'
         '    model.fit(X_train, y_train)\n'
         '    joblib.dump(model, cfg.MODEL_DIR / f"{name}.joblib")\n'
         '    print(f"saved {name}.joblib")\n'
         'print("boosting iterations after early stopping:", candidates["gradient_boosting"][-1].n_iter_)'),
]

NB03 = [
    md("# 03 · Model testing\n"
       "Evaluates both saved models on the untouched hold-out set: ROC-AUC, PR-AUC, Brier score, lift by decile, "
       "calibration and SHAP drivers. Saves **artifact 6** (model comparison) and **artifact 7** (charts) "
       "and checks the acceptance criteria from the brief."),
    code('import joblib\n'
         'import matplotlib.pyplot as plt\n'
         'import pandas as pd\n'
         'import shap\n'
         'from sklearn.calibration import CalibrationDisplay\n'
         'from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'split = pd.read_csv(cfg.SPLIT_FILE)\n'
         'test_df = df[df["customer_id"].isin(split.loc[split["split"] == "test", "customer_id"])]\n'
         'features = cfg.feature_columns(df)\n'
         'X_test, y_test = test_df[features], test_df[cfg.TARGET]\n'
         'models = {p.stem: joblib.load(p) for p in sorted(cfg.MODEL_DIR.glob("*.joblib"))}\n'
         'print(f"test set: {len(test_df):,} customers, {y_test.mean():.1%} positive | models: {list(models)}")'),
    md("## 1. Hold-out metrics"),
    code('scores = {name: model.predict(X_test) for name, model in models.items()}\n'
         '\n'
         'rows = []\n'
         'for name, s in scores.items():\n'
         '    rows.append({"model": name, "roc_auc": roc_auc_score(y_test, s),\n'
         '                 "pr_auc": average_precision_score(y_test, s), "brier": brier_score_loss(y_test, s)})\n'
         'comparison = pd.DataFrame(rows).set_index("model").round(3)\n'
         'comparison.loc["random (base rate)", "pr_auc"] = round(y_test.mean(), 3)\n'
         'comparison'),
    md("## 2. Lift by decile (gradient boosting)"),
    code('best = "gradient_boosting"\n'
         'scored = test_df.assign(score=scores[best])\n'
         'scored["decile"] = pd.qcut(scored["score"].rank(method="first", ascending=False), 10, labels=range(1, 11))\n'
         'deciles = scored.groupby("decile", observed=True)[cfg.TARGET].agg(customers="size", conversion_rate="mean")\n'
         'deciles["lift"] = deciles["conversion_rate"] / y_test.mean()\n'
         'top20_lift = scored.nlargest(int(len(scored) * 0.2), "score")[cfg.TARGET].mean() / y_test.mean()\n'
         'print(f"Top-20% lift: {top20_lift:.2f}x")\n'
         'deciles.round(3)'),
    code('cfg.CHART_DIR.mkdir(exist_ok=True)\n'
         'fig, ax = plt.subplots(figsize=(8, 4))\n'
         'ax.bar(deciles.index.astype(str), deciles["lift"], color="#2f6db5")\n'
         'ax.axhline(1, color="grey", linestyle="--", linewidth=1)\n'
         'ax.set(xlabel="Score decile (1 = highest propensity)", ylabel="Lift vs average",\n'
         '       title="Conversion lift by decile - hold-out set")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "lift_by_decile.png", dpi=150)\n'
         'plt.show()'),
    md("## 3. Calibration"),
    code('fig, ax = plt.subplots(figsize=(5, 5))\n'
         'CalibrationDisplay.from_predictions(y_test, scores[best], n_bins=10, strategy="quantile", ax=ax,\n'
         '                                    name="gradient boosting")\n'
         'ax.set_title("Calibration - hold-out set")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "calibration.png", dpi=150)\n'
         'plt.show()\n'
         'print(f"mean predicted {scores[best].mean():.3f} vs actual {y_test.mean():.3f}")'),
    md("## 4. Drivers (SHAP)"),
    code('pipe = models[best]\n'
         'preprocess, booster = pipe[:-1], pipe[-1]\n'
         'sample = X_test.sample(1000, random_state=cfg.RANDOM_STATE)\n'
         'X_sample = pd.DataFrame(preprocess.transform(sample), columns=preprocess.get_feature_names_out())\n'
         'shap_values = shap.TreeExplainer(booster).shap_values(X_sample)\n'
         '\n'
         'shap.summary_plot(shap_values, X_sample, max_display=12, show=False)\n'
         'plt.title("Top drivers of cross-sell propensity")\n'
         'plt.tight_layout()\n'
         'plt.savefig(cfg.CHART_DIR / "shap_summary.png", dpi=150, bbox_inches="tight")\n'
         'plt.show()'),
    md("## 5. Acceptance check and save"),
    code('base_pr = comparison.loc["baseline_logreg", "pr_auc"]\n'
         'checks = pd.DataFrame([\n'
         '    {"criterion": f"hold-out ROC-AUC >= {cfg.ACCEPTANCE[\'roc_auc\']}", "value": comparison.loc[best, "roc_auc"]},\n'
         '    {"criterion": f"PR-AUC beats baseline ({base_pr})", "value": comparison.loc[best, "pr_auc"]},\n'
         '    {"criterion": f"top-20% lift >= {cfg.ACCEPTANCE[\'top20_lift\']}x", "value": round(top20_lift, 2)},\n'
         '])\n'
         'checks["pass"] = [checks.loc[0, "value"] >= cfg.ACCEPTANCE["roc_auc"],\n'
         '                  checks.loc[1, "value"] > base_pr,\n'
         '                  checks.loc[2, "value"] >= cfg.ACCEPTANCE["top20_lift"]]\n'
         '\n'
         'comparison.to_csv(cfg.COMPARISON_FILE)\n'
         'deciles.to_csv(cfg.CHART_DIR / "lift_by_decile.csv")\n'
         'checks'),
]

NB04 = [
    md("# 04 · Back-test and model package\n"
       "Answers the brief's question: *which 4,000 customers would the model have contacted on 30 June, and how "
       "many actually converted?* Every customer is scored **out of fold** (by a model that never trained on them). "
       "Saves the back-test list (**artifact 8**) and the final model package (**final output 3**)."),
    code('import json\n'
         '\n'
         'import joblib\n'
         'import pandas as pd\n'
         'from sklearn.model_selection import StratifiedKFold, cross_val_predict\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'features = cfg.feature_columns(df)\n'
         'X, y = df[features], df[cfg.TARGET]'),
    md("## 1. Out-of-fold propensity scores"),
    code('cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=cfg.RANDOM_STATE)\n'
         'oof = cross_val_predict(cfg.build_gradient_boosting(df), X, y, cv=cv, method="predict_proba")[:, 1]\n'
         'scored = df.assign(propensity=oof)\n'
         'scored["propensity"].describe().round(3)'),
    md("## 2. Eligible customers and the 4,000-customer list"),
    code('eligible = scored[(scored["marketing_opt_in"] == 1) & (scored["complaints_12m"] <= cfg.MAX_COMPLAINTS)]\n'
         'base_rate = eligible[cfg.TARGET].mean()\n'
         'print(f"eligible: {len(eligible):,} of {len(df):,} customers | eligible conversion rate {base_rate:.2%}")\n'
         '\n'
         'target_list = (eligible.nlargest(cfg.CAMPAIGN_SIZE, "propensity")\n'
         '               .assign(rank=lambda d: range(1, len(d) + 1))\n'
         '               [["rank", "customer_id", "propensity", "customer_segment", "primary_product", "num_products",\n'
         '                 "tenure_months", "region", "marketing_opt_in", "complaints_12m", cfg.TARGET]]\n'
         '               .rename(columns={cfg.TARGET: "actual_converted"}))\n'
         'target_list.to_csv(cfg.BACKTEST_FILE, index=False)\n'
         'print(f"saved {len(target_list):,} customers -> {cfg.BACKTEST_FILE.name}")\n'
         'target_list.head()'),
    md("## 3. Back-test result"),
    code('expected = target_list["propensity"].sum()\n'
         'actual = int(target_list["actual_converted"].sum())\n'
         'random_conversions = cfg.CAMPAIGN_SIZE * base_rate\n'
         'cost = cfg.CAMPAIGN_SIZE * cfg.COST_PER_CONTACT\n'
         '\n'
         'backtest = {\n'
         '    "customers_contacted": cfg.CAMPAIGN_SIZE,\n'
         '    "expected_conversions": round(float(expected)),\n'
         '    "actual_conversions": actual,\n'
         '    "actual_conversion_rate": round(actual / cfg.CAMPAIGN_SIZE, 3),\n'
         '    "eligible_base_rate": round(float(base_rate), 4),\n'
         '    "lift_vs_eligible": round(actual / cfg.CAMPAIGN_SIZE / base_rate, 2),\n'
         '    "random_conversions": round(float(random_conversions)),\n'
         '    "profit_model_usd": int(actual * cfg.MARGIN_PER_CONVERSION - cost),\n'
         '    "profit_random_usd": int(random_conversions * cfg.MARGIN_PER_CONVERSION - cost),\n'
         '}\n'
         'backtest["passes_backtest_lift"] = bool(backtest["lift_vs_eligible"] >= cfg.ACCEPTANCE["backtest_lift"])\n'
         'pd.Series(backtest)'),
    md("## 4. Package the final model (trained on all 20,000 customers)"),
    code('cfg.PACKAGE_DIR.mkdir(exist_ok=True)\n'
         'final_model = cfg.build_gradient_boosting(df).fit(X, y)\n'
         'joblib.dump(final_model, cfg.PACKAGE_DIR / "model.joblib")\n'
         '\n'
         'holdout = pd.read_csv(cfg.COMPARISON_FILE, index_col="model")\n'
         'metrics = {\n'
         '    "holdout_gradient_boosting": holdout.loc["gradient_boosting", ["roc_auc", "pr_auc", "brier"]].to_dict(),\n'
         '    "holdout_baseline_pr_auc": float(holdout.loc["baseline_logreg", "pr_auc"]),\n'
         '    "backtest": backtest,\n'
         '    "features": features,\n'
         '    "excluded_columns": cfg.EXCLUDED,\n'
         '}\n'
         '(cfg.PACKAGE_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))\n'
         'print("saved model.joblib and metrics.json")'),
    code('h = metrics["holdout_gradient_boosting"]\n'
         'readme = f"""# Cross-sell propensity model\n'
         '\n'
         'Predicts the probability that an existing customer opens an additional product within 90 days.\n'
         'Trained on the 30-Jun-2026 snapshot (20,000 customers, outcome Jul-Sep 2026).\n'
         '\n'
         '## How to score a new snapshot (e.g. 30-Sep-2026)\n'
         '1. Run `2_Code/01_data_preprocessing.ipynb` on the new extract (same cleaning rules).\n'
         '2. `model = joblib.load("model.joblib")`\n'
         '3. `propensity = model.predict_proba(cleaned[features])[:, 1]` (feature list in `metrics.json`).\n'
         '4. Keep opted-in customers with fewer than 2 complaints; contact the top {cfg.CAMPAIGN_SIZE:,}.\n'
         '\n'
         '## Excluded columns\n'
         '- `cross_sell_product_type`, `welcome_pack_sent`: populated after the purchase (leakage)\n'
         '- `gender`: protected attribute (fair-treatment policy)\n'
         '- IDs and dates\n'
         '\n'
         '## Performance\n'
         '| Check | Result |\n'
         '|---|---|\n'
         '| Hold-out ROC-AUC | {h["roc_auc"]:.3f} |\n'
         '| Hold-out PR-AUC | {h["pr_auc"]:.3f} (baseline {metrics["holdout_baseline_pr_auc"]:.3f}) |\n'
         '| Back-test conversions (4,000 contacted) | {backtest["actual_conversions"]:,} vs {backtest["random_conversions"]:,} random |\n'
         '| Back-test profit | ${backtest["profit_model_usd"]:,} vs ${backtest["profit_random_usd"]:,} random |\n'
         '\n'
         '## Limitations\n'
         '- One snapshot and one outcome window: re-validate every quarter before use.\n'
         '- Probabilities assume a campaign mix similar to Jul-Sep 2026.\n'
         '"""\n'
         '(cfg.PACKAGE_DIR / "README.md").write_text(readme, encoding="utf-8")\n'
         'print(readme)'),
]


def write_notebook(path, cells):
    nb = {
        "cells": [
            {"cell_type": kind, "metadata": {}, "source": text.splitlines(keepends=True),
             **({"execution_count": None, "outputs": []} if kind == "code" else {})}
            for kind, text in cells
        ],
        "metadata": {"kernelspec": KERNEL,
                     "language_info": {"name": "python", "version": "3.12"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    for i, cell in enumerate(nb["cells"]):
        cell["id"] = f"cell-{i:02d}"
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def main():
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    for name, cells in [("01_data_preprocessing", NB01), ("02_model_training", NB02),
                        ("03_model_testing", NB03), ("04_backtest_and_package", NB04)]:
        write_notebook(CODE_DIR / f"{name}.ipynb", cells)


if __name__ == "__main__":
    main()

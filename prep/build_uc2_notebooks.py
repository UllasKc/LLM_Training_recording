"""
Build the four UC2 pipeline notebooks (without outputs) into
recording_workspace/UC2_Propensity_To_Pay/Deliverables/2_Code/.

The notebooks are the expert's own pipeline that they walk through, run, debugs and
completes on camera. They deliberately contain the planted bugs documented in
use_cases/UC2_Planted_Bugs_Answer_Key.md. Do NOT open this script on camera.

Usage:  python prep/build_uc2_notebooks.py
"""
from pathlib import Path

from build_uc1_notebooks import code, md, write_notebook

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "recording_workspace" / "UC2_Propensity_To_Pay" / "Deliverables" / "2_Code"

NB01 = [
    md("# 01 · Data preprocessing\n"
       "Cleans the January–June 2026 collections extract (`input 1`) and writes the cleaned accounts "
       "(**artifact 2**) and a data-quality log (**artifact 3**).\n\n"
       "**Run order:** 01 → 02 → 03 → 04"),
    code('import matplotlib.pyplot as plt\n'
         'import numpy as np\n'
         'import pandas as pd\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'pd.set_option("display.max_columns", 40)\n'
         'cfg.CHART_DIR.mkdir(exist_ok=True)\n'
         'dq_log = []\n'
         '\n'
         '\n'
         'def log(step, rows_affected, action):\n'
         '    dq_log.append({"step": step, "rows_affected": int(rows_affected), "action": action})\n'
         '    print(f"{step:<30} {rows_affected:>6,} rows  -> {action}")'),
    md("## 1. Load and profile"),
    code('raw = pd.read_csv(cfg.RAW_FILE)\n'
         'print(f"{raw.shape[0]:,} rows x {raw.shape[1]} columns | unique accounts: {raw[\'account_id\'].nunique():,}")\n'
         'print(f"Paid within 30 days: {raw[cfg.TARGET].mean():.1%}")\n'
         'raw.head()'),
    code('missing = raw.isna().mean().mul(100).round(1)\n'
         'missing = missing[missing > 0].sort_values()\n'
         '\n'
         'fig, ax = plt.subplots(figsize=(7, 2.6))\n'
         'ax.barh(missing.index, missing.values, color="#2f6db5")\n'
         'for i, v in enumerate(missing.values):\n'
         '    ax.text(v, i, f" {v:.1f}%", va="center")\n'
         'ax.set(xlabel="% of rows missing", title="Missing values in the raw extract")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "01_missing_values.png", dpi=150)\n'
         'plt.show()'),
    code('raw[["days_past_due", "amount_due", "outstanding_balance", "utilization_ratio", "monthly_income"]].describe().T[["min", "50%", "max"]]'),
    md("## 2. Duplicates"),
    code('df = raw.copy()\n'
         'n_exact = df.duplicated().sum()\n'
         'df = df.drop_duplicates()\n'
         'log("exact duplicates", n_exact, "dropped")\n'
         'assert df["account_id"].is_unique\n'
         'print(f"{len(df):,} accounts")'),
    md("## 3. Delinquency date and cohort month\n"
       "The cohort month drives the out-of-time split, so it must be exact."),
    code('df["delinquency_date"] = pd.to_datetime(df["delinquency_date"], format="mixed")\n'
         'df["cohort_month"] = df["delinquency_date"].dt.month\n'
         'print(df["cohort_month"].value_counts().sort_index().to_dict())\n'
         'outside = sorted(int(m) for m in df.loc[~df["cohort_month"].between(1, 6), "cohort_month"].unique())\n'
         'assert not outside, f"cohort months outside Jan-Jun: {outside}"'),
    code('by_month = df["cohort_month"].value_counts().sort_index()\n'
         'fig, ax = plt.subplots(figsize=(6, 3))\n'
         'ax.bar(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], by_month.values, color="#2f6db5")\n'
         'for i, v in enumerate(by_month.values):\n'
         '    ax.text(i, v, f"{v:,}", ha="center", va="bottom")\n'
         'ax.set(ylabel="Accounts", title="Accounts entering collections by month", ylim=(0, by_month.max() * 1.15))\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "02_accounts_by_month.png", dpi=150)\n'
         'plt.show()'),
    md("## 4. Category labels"),
    code('PRODUCT_FIXES = {"cc": "credit card", "credit_card": "credit card", "pl": "personal loan",\n'
         '                 "personal-loan": "personal loan", "buy now pay later": "bnpl"}\n'
         'CANONICAL = {"credit card": "Credit Card", "personal loan": "Personal Loan", "bnpl": "BNPL"}\n'
         '\n'
         'orig_product = df["product_type"].copy()\n'
         'df["product_type"] = df["product_type"].str.strip().str.lower().replace(PRODUCT_FIXES).map(CANONICAL)\n'
         'assert df["product_type"].notna().all(), "unmapped product labels"\n'
         'log("product labels", (orig_product != df["product_type"]).sum(), "normalised to 3 products")\n'
         '\n'
         '# blanks, "N/A" and "Unknown" all mean the same thing: status not known\n'
         'n_unknown = df["employment_status"].isna().sum() + (df["employment_status"] == "Unknown").sum()\n'
         'df["employment_status"] = df["employment_status"].fillna("Unknown")\n'
         'log("employment placeholders", n_unknown, "merged into Unknown")'),
    md("## 5. Business-rule violations (data dictionary)"),
    code('bad_dpd = ~df["days_past_due"].between(1, 90)\n'
         'log("days_past_due outside 1-90", bad_dpd.sum(), "removed")\n'
         'df = df[~bad_dpd]\n'
         '\n'
         'bad_due = df["amount_due"] > df["outstanding_balance"]\n'
         'log("amount_due > balance", bad_due.sum(), "removed")\n'
         'df = df[~bad_due]\n'
         '\n'
         'sentinel = df["utilization_ratio"] == 9.99\n'
         'df.loc[sentinel, "utilization_ratio"] = np.nan\n'
         'log("utilization = 9.99", sentinel.sum(), "set to missing (sentinel)")\n'
         'print(f"{len(df):,} accounts remain")'),
    md("## 6. Income and affordability"),
    code('df["income_missing"] = df["monthly_income"].isna().astype(int)\n'
         'df["payment_burden"] = df["amount_due"] / df["monthly_income"]\n'
         '\n'
         'infinite = np.isinf(df["payment_burden"])\n'
         'assert not infinite.any(), f"infinite payment_burden for {infinite.sum()} accounts"\n'
         'log("monthly_income missing", df["income_missing"].sum(), "flag; burden left missing")\n'
         'df["payment_burden"].describe().round(3)'),
    code('bands = pd.cut(df["payment_burden"], [0, 0.05, 0.1, 0.2, 0.35, 0.5, float("inf")],\n'
         '               labels=["<5%", "5-10%", "10-20%", "20-35%", "35-50%", ">50%"])\n'
         'by_band = df.groupby(bands, observed=True)[cfg.TARGET].mean()\n'
         'fig, ax = plt.subplots(figsize=(6.5, 3))\n'
         'ax.bar(by_band.index.astype(str), by_band.values, color=["#c25b12" if b in ("35-50%", ">50%") else "#2f6db5" for b in by_band.index])\n'
         'ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")\n'
         'ax.set(xlabel="Amount due as % of monthly income", ylabel="Paid within 30 days",\n'
         '       title="Affordability: pay rate by payment burden")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "03_pay_rate_by_burden.png", dpi=150)\n'
         'plt.show()'),
    md("## 7. Save"),
    code('df.to_csv(cfg.CLEAN_FILE, index=False)\n'
         'pd.DataFrame(dq_log).to_csv(cfg.DQ_LOG_FILE, index=False)\n'
         'print(f"Saved {len(df):,} rows -> {cfg.CLEAN_FILE.name}")\n'
         'print(f"Saved {len(dq_log)} log entries -> {cfg.DQ_LOG_FILE.name}")'),
    code('steps = pd.DataFrame(dq_log).iloc[::-1]\n'
         'fig, ax = plt.subplots(figsize=(8, 3.6))\n'
         'ax.barh(steps["step"], steps["rows_affected"], color="#2f6db5")\n'
         'for i, v in enumerate(steps["rows_affected"]):\n'
         '    ax.text(v, i, f" {v:,}", va="center")\n'
         'ax.set(xlabel="Rows affected", title="Data-quality fixes applied (artifact 3)")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "04_data_quality_fixes.png", dpi=150)\n'
         'plt.show()'),
]

NB02 = [
    md("# 02 · Model training\n"
       "Out-of-time design: **train Jan–Apr, validate and calibrate on May, test on June** (artifact 4). "
       "Trains a logistic-regression baseline and gradient boosting, validates them on May and checks which "
       "features drive the model, then saves both (**artifact 5**). June stays untouched until notebook 03."),
    code('import joblib\n'
         'import matplotlib.pyplot as plt\n'
         'import pandas as pd\n'
         'from sklearn.inspection import permutation_importance\n'
         'from sklearn.metrics import average_precision_score, roc_auc_score\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'features = cfg.feature_columns(df)\n'
         'print(f"{len(df):,} accounts | {len(features)} features")\n'
         'print("Excluded:", cfg.EXCLUDED)'),
    md("## 1. Pay rate by cohort month"),
    code('by_month = df.groupby("cohort_month")[cfg.TARGET].agg(accounts="size", pay_rate="mean")\n'
         'cfg.CHART_DIR.mkdir(exist_ok=True)\n'
         'fig, ax = plt.subplots(figsize=(7, 3.5))\n'
         'ax.bar(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], by_month["pay_rate"], color="#2f6db5")\n'
         'ax.set(ylabel="Paid within 30 days", title="Pay rate by cohort month")\n'
         'ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "05_pay_rate_by_month.png", dpi=150)\n'
         'plt.show()\n'
         'by_month.round(3)'),
    md("## 2. Out-of-time split"),
    code('train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]\n'
         'calib_df = df[df["cohort_month"] == cfg.CALIBRATION_MONTH]\n'
         'test_df = df[df["cohort_month"] == cfg.TEST_MONTH]\n'
         '\n'
         'assert set(train_df["account_id"]).isdisjoint(calib_df["account_id"]), "train and calibration windows overlap"\n'
         'assert set(train_df["account_id"]).isdisjoint(test_df["account_id"]), "train and test windows overlap"\n'
         'for name, part in [("train", train_df), ("calibrate", calib_df), ("test", test_df)]:\n'
         '    months = sorted(int(m) for m in part["cohort_month"].unique())\n'
         '    print(f"{name:<10} months {months}  {len(part):>6,} accounts  "\n'
         '          f"pay rate {part[cfg.TARGET].mean():.1%}")\n'
         '\n'
         'split = pd.concat([train_df[["account_id"]].assign(split="train"),\n'
         '                   calib_df[["account_id"]].assign(split="calibrate"),\n'
         '                   test_df[["account_id"]].assign(split="test")])\n'
         'split.to_csv(cfg.SPLIT_FILE, index=False)'),
    md("## 3. Train and validate on May"),
    code('X_train, y_train = train_df[features], train_df[cfg.TARGET]\n'
         'X_calib, y_calib = calib_df[features], calib_df[cfg.TARGET]\n'
         'models = {"baseline_logreg": cfg.build_baseline(df), "gradient_boosting": cfg.build_gradient_boosting(df)}\n'
         '\n'
         'rows = []\n'
         'for name, model in models.items():\n'
         '    model.fit(X_train, y_train)\n'
         '    p = model.predict_proba(X_calib)[:, 1]\n'
         '    rows.append({"model": name, "may_roc_auc": roc_auc_score(y_calib, p),\n'
         '                 "may_pr_auc": average_precision_score(y_calib, p)})\n'
         'pd.DataFrame(rows).set_index("model").round(3)'),
    md("## 4. What drives the model? (permutation importance on May)"),
    code('imp = permutation_importance(models["gradient_boosting"], X_calib, y_calib, scoring="roc_auc",\n'
         '                             n_repeats=5, random_state=cfg.RANDOM_STATE)\n'
         'importance = pd.Series(imp.importances_mean, index=features).sort_values(ascending=False)\n'
         'importance.head(10).round(3).to_frame("drop in ROC-AUC when shuffled")'),
    code('top = importance.head(10).iloc[::-1]\n'
         'fig, ax = plt.subplots(figsize=(7, 3.8))\n'
         'ax.barh(top.index, top.values, color=["#c25b12" if v == top.max() else "#2f6db5" for v in top.values])\n'
         'ax.set(xlabel="Drop in May ROC-AUC when the feature is shuffled", title="Permutation importance (gradient boosting)")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "06_permutation_importance.png", dpi=150)\n'
         'plt.show()'),
    md("## 5. Save the trained models"),
    code('cfg.MODEL_DIR.mkdir(exist_ok=True)\n'
         'for name, model in models.items():\n'
         '    joblib.dump(model, cfg.MODEL_DIR / f"{name}.joblib")\n'
         '    print(f"saved {name}.joblib")'),
]

NB03 = [
    md("# 03 · Model testing (June, out of time)\n"
       "Evaluates both models on June, which no model has seen. Calibrates the probabilities on May, compares the "
       "agent prioritisation against today's rule (highest days-past-due first), explains the drivers and checks "
       "the acceptance criteria. Saves **artifact 6** (comparison) and **artifact 7** (charts)."),
    code('import joblib\n'
         'import matplotlib.pyplot as plt\n'
         'import numpy as np\n'
         'import pandas as pd\n'
         'import shap\n'
         'from sklearn.calibration import calibration_curve\n'
         'from sklearn.isotonic import IsotonicRegression\n'
         'from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'split = pd.read_csv(cfg.SPLIT_FILE).set_index("account_id")["split"]\n'
         'df["split"] = df["account_id"].map(split)\n'
         'features = cfg.feature_columns(df.drop(columns="split"))\n'
         'calib_df, test_df = df[df["split"] == "calibrate"], df[df["split"] == "test"].copy()\n'
         'models = {name: joblib.load(cfg.MODEL_DIR / f"{name}.joblib") for name in ["baseline_logreg", "gradient_boosting"]}\n'
         'y_test = test_df[cfg.TARGET]\n'
         'print(f"June test cohort: {len(test_df):,} accounts, pay rate {y_test.mean():.1%} | models: {list(models)}")'),
    md("## 1. June metrics (raw probabilities)"),
    code('raw_scores = {name: m.predict_proba(test_df[features])[:, 1] for name, m in models.items()}\n'
         'comparison = pd.DataFrame([{"model": name, "roc_auc": roc_auc_score(y_test, s),\n'
         '                            "pr_auc": average_precision_score(y_test, s),\n'
         '                            "brier": brier_score_loss(y_test, s)} for name, s in raw_scores.items()]).set_index("model")\n'
         'comparison.round(3)'),
    md("## 2. Calibration (fitted on May, checked on June)"),
    code('best = "gradient_boosting"\n'
         'calibrator = IsotonicRegression(out_of_bounds="clip")\n'
         'calibrator.fit(models[best].predict_proba(calib_df[features])[:, 1], calib_df[cfg.TARGET])\n'
         'joblib.dump(calibrator, cfg.MODEL_DIR / "calibrator.joblib")\n'
         '\n'
         'p_raw = raw_scores[best]\n'
         'p_cal = calibrator.predict(p_raw)\n'
         'calibration = pd.DataFrame({\n'
         '    "mean_predicted": [p_raw.mean(), p_cal.mean()],\n'
         '    "actual_pay_rate": [y_test.mean(), y_test.mean()],\n'
         '    "brier": [brier_score_loss(y_test, p_raw), brier_score_loss(y_test, p_cal)],\n'
         '}, index=["raw", "calibrated"])\n'
         '\n'
         'fig, ax = plt.subplots(figsize=(5, 5))\n'
         'for label, p in [("raw", p_raw), ("calibrated on May", p_cal)]:\n'
         '    frac, mean_pred = calibration_curve(y_test, p, n_bins=10, strategy="quantile")\n'
         '    ax.plot(mean_pred, frac, marker="o", label=label)\n'
         'ax.plot([0, 1], [0, 1], linestyle="--", color="grey", linewidth=1)\n'
         'ax.set(xlabel="Predicted probability of paying", ylabel="Actual pay rate", title="Calibration - June cohort")\n'
         'ax.legend()\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "07_calibration.png", dpi=150)\n'
         'plt.show()\n'
         'calibration.round(4)'),
    md("## 3. Agent prioritisation vs today's rule\n"
       "Agents can work 37% of the cohort. Dispute and hardship accounts go to a specialist team. "
       "Success = share of the June cohort's **actual unpaid amount** that the agent list covers."),
    code('test_df["p_pay"] = p_cal\n'
         'test_df["expected_unpaid"] = test_df["p_pay"] * test_df["amount_due"]\n'
         'test_df["actual_unpaid"] = (1 - test_df[cfg.TARGET]) * test_df["amount_due"]\n'
         '\n'
         'capacity = round(cfg.AGENT_CAPACITY_SHARE * len(test_df))\n'
         'eligible = test_df[(test_df[cfg.SPECIALIST_FLAGS] == 0).all(axis=1)]\n'
         'total_unpaid = eligible["actual_unpaid"].sum()\n'
         '\n'
         'def coverage(ranking_column):\n'
         '    chosen = eligible.nlargest(capacity, ranking_column)\n'
         '    return chosen["actual_unpaid"].sum() / total_unpaid\n'
         '\n'
         'prioritisation = pd.Series({\n'
         '    "today: highest days_past_due first": coverage("days_past_due"),\n'
         '    "model: highest expected unpaid first": coverage("expected_unpaid"),\n'
         '})\n'
         'print(f"capacity {capacity:,} of {len(test_df):,} June accounts | eligible {len(eligible):,}")\n'
         '\n'
         'fig, ax = plt.subplots(figsize=(7, 3))\n'
         'ax.barh(prioritisation.index, prioritisation.values, color=["#9aa5b1", "#2f6db5"])\n'
         'ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")\n'
         'ax.set(xlabel="Share of June unpaid amount covered by the agent list", title="Agent prioritisation - June")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "08_prioritisation.png", dpi=150)\n'
         'plt.show()\n'
         'prioritisation.map("{:.1%}".format)'),
    md("## 4. Drivers (SHAP)"),
    code('pipe = models[best]\n'
         'preprocess, booster = pipe[:-1], pipe[-1]\n'
         'sample = test_df[features].sample(1000, random_state=cfg.RANDOM_STATE)\n'
         'X_sample = pd.DataFrame(preprocess.transform(sample), columns=preprocess.get_feature_names_out())\n'
         'shap_values = shap.TreeExplainer(booster).shap_values(X_sample)\n'
         '\n'
         'shap.summary_plot(shap_values, X_sample, max_display=12, show=False)\n'
         'plt.title("Top drivers of paying within 30 days")\n'
         'plt.tight_layout()\n'
         'plt.savefig(cfg.CHART_DIR / "09_shap_summary.png", dpi=150, bbox_inches="tight")\n'
         'plt.show()'),
    code('fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))\n'
         'for ax, feature in zip(axes, ["days_past_due", "payment_burden", "on_time_payment_ratio_12m"]):\n'
         '    shap.dependence_plot(feature, shap_values, X_sample, interaction_index=None, ax=ax, show=False)\n'
         '    ax.axhline(0, color="grey", linewidth=0.8)\n'
         'axes[1].set_xlim(0, 1)\n'
         'fig.suptitle("How each driver moves the chance of paying (SHAP dependence: above 0 = more likely to pay)")\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "10_shap_dependence.png", dpi=150)\n'
         'plt.show()'),
    md("## 5. Acceptance check and save"),
    code('checks = pd.DataFrame([\n'
         '    {"criterion": f"June ROC-AUC >= {cfg.ACCEPTANCE[\'roc_auc\']}", "value": comparison.loc[best, "roc_auc"],\n'
         '     "pass": comparison.loc[best, "roc_auc"] >= cfg.ACCEPTANCE["roc_auc"]},\n'
         '    {"criterion": "PR-AUC beats logistic baseline", "value": comparison.loc[best, "pr_auc"],\n'
         '     "pass": comparison.loc[best, "pr_auc"] > comparison.loc["baseline_logreg", "pr_auc"]},\n'
         '    {"criterion": "model list covers more unpaid than today\'s rule", "value": prioritisation.iloc[1],\n'
         '     "pass": prioritisation.iloc[1] > prioritisation.iloc[0]},\n'
         '    {"criterion": "calibration gap smaller after calibration",\n'
         '     "value": abs(calibration.loc["calibrated", "mean_predicted"] - y_test.mean()),\n'
         '     "pass": abs(calibration.loc["calibrated", "mean_predicted"] - y_test.mean())\n'
         '             < abs(calibration.loc["raw", "mean_predicted"] - y_test.mean())},\n'
         '])\n'
         '\n'
         'summary = comparison.copy()\n'
         'summary.loc[best, "brier_calibrated"] = calibration.loc["calibrated", "brier"]\n'
         'summary.loc[best, "coverage_model"] = prioritisation.iloc[1]\n'
         'summary.loc[best, "coverage_dpd_rule"] = prioritisation.iloc[0]\n'
         'summary.to_csv(cfg.COMPARISON_FILE)\n'
         'checks.round(3)'),
]

NB04 = [
    md("# 04 · June agent work list and model package\n"
       "Scores the June cohort with the calibrated model, removes dispute and hardship accounts, ranks by "
       "**expected unpaid amount = (1 − p) × amount_due**, cuts at agent capacity (**artifact 8**) and packages "
       "the model (**final output 3**)."),
    code('import json\n'
         '\n'
         'import joblib\n'
         'import matplotlib.pyplot as plt\n'
         'import pandas as pd\n'
         '\n'
         'import pipeline_config as cfg\n'
         '\n'
         'df = pd.read_csv(cfg.CLEAN_FILE)\n'
         'june = df[df["cohort_month"] == cfg.TEST_MONTH].copy()\n'
         'features = cfg.feature_columns(df)\n'
         'model = joblib.load(cfg.MODEL_DIR / "gradient_boosting.joblib")\n'
         'calibrator = joblib.load(cfg.MODEL_DIR / "calibrator.joblib")\n'
         'print(f"June cohort: {len(june):,} accounts")'),
    md("## 1. Score and rank"),
    code('june["p_pay"] = calibrator.predict(model.predict_proba(june[features])[:, 1])\n'
         'june["expected_unpaid"] = (1 - june["p_pay"]) * june["amount_due"]\n'
         '\n'
         'capacity = round(cfg.AGENT_CAPACITY_SHARE * len(june))\n'
         'specialist = (june[cfg.SPECIALIST_FLAGS] == 1).any(axis=1)\n'
         'print(f"agent capacity {capacity:,} | routed to specialist team (dispute / hardship): {specialist.sum():,}")\n'
         '\n'
         'work_list = (june[~specialist].nlargest(capacity, "expected_unpaid")\n'
         '             .assign(priority=lambda d: range(1, len(d) + 1))\n'
         '             [["priority", "account_id", "product_type", "days_past_due", "amount_due", "p_pay",\n'
         '               "expected_unpaid", "preferred_channel", "has_open_dispute", "hardship_flag", cfg.TARGET]]\n'
         '             .rename(columns={cfg.TARGET: "actual_paid"}))\n'
         'work_list.to_csv(cfg.WORKLIST_FILE, index=False)\n'
         'print(f"saved {len(work_list):,} accounts -> {cfg.WORKLIST_FILE.name}")\n'
         'work_list.head()'),
    md("## 2. What the list achieves (June outcomes are known)"),
    code('eligible = june[~specialist]\n'
         'actual_unpaid = (1 - eligible[cfg.TARGET]) * eligible["amount_due"]\n'
         'dpd_list = eligible.nlargest(capacity, "days_past_due")\n'
         '\n'
         'result = {\n'
         '    "june_accounts": len(june),\n'
         '    "agent_capacity": capacity,\n'
         '    "expected_unpaid_on_list_usd": round(float(work_list["expected_unpaid"].sum())),\n'
         '    "actual_unpaid_on_list_usd": round(float(((1 - work_list["actual_paid"]) * work_list["amount_due"]).sum())),\n'
         '    "total_unpaid_eligible_usd": round(float(actual_unpaid.sum())),\n'
         '    "coverage_model": round(float(((1 - work_list["actual_paid"]) * work_list["amount_due"]).sum() / actual_unpaid.sum()), 3),\n'
         '    "coverage_dpd_rule": round(float(((1 - dpd_list[cfg.TARGET]) * dpd_list["amount_due"]).sum() / actual_unpaid.sum()), 3),\n'
         '}\n'
         'pd.Series(result)'),
    code('fig, ax = plt.subplots(figsize=(7, 3.4))\n'
         'bins = range(0, 95, 5)\n'
         'ax.hist(dpd_list["days_past_due"], bins=bins, alpha=0.6, color="#9aa5b1", label="today: highest DPD first")\n'
         'ax.hist(work_list["days_past_due"], bins=bins, alpha=0.6, color="#2f6db5", label="model: highest expected unpaid")\n'
         'ax.set(xlabel="Days past due", ylabel="Accounts on the agent list", title="Who gets an agent call: model list vs current rule")\n'
         'ax.legend()\n'
         'fig.tight_layout()\n'
         'fig.savefig(cfg.CHART_DIR / "11_work_list_vs_dpd_rule.png", dpi=150)\n'
         'plt.show()'),
    md("## 3. Package the model"),
    code('cfg.PACKAGE_DIR.mkdir(exist_ok=True)\n'
         'joblib.dump(model, cfg.PACKAGE_DIR / "model.joblib")\n'
         'joblib.dump(calibrator, cfg.PACKAGE_DIR / "calibrator.joblib")\n'
         '\n'
         'comparison = pd.read_csv(cfg.COMPARISON_FILE, index_col="model")\n'
         'metrics = {\n'
         '    "june_gradient_boosting": comparison.loc["gradient_boosting"].dropna().round(4).to_dict(),\n'
         '    "june_baseline_pr_auc": round(float(comparison.loc["baseline_logreg", "pr_auc"]), 4),\n'
         '    "work_list": result,\n'
         '    "features": features,\n'
         '    "excluded_columns": cfg.EXCLUDED,\n'
         '    "windows": {"train": cfg.TRAIN_MONTHS, "calibrate": cfg.CALIBRATION_MONTH, "test": cfg.TEST_MONTH},\n'
         '}\n'
         '(cfg.PACKAGE_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))\n'
         'print("saved model.joblib, calibrator.joblib and metrics.json")'),
    code('g = metrics["june_gradient_boosting"]\n'
         'readme = f"""# Collections propensity-to-pay model\n'
         '\n'
         'Predicts the probability that an account in early collections pays the past-due amount in full within\n'
         '30 days. Scored on **day {cfg.SCORING_DAY}** after the account enters collections.\n'
         'Trained on January-April 2026, calibrated on May, tested out of time on June.\n'
         '\n'
         '## How to build the monthly agent list\n'
         '1. Run `2_Code/01_data_preprocessing.ipynb` on the new month (same cleaning rules).\n'
         '2. `p = calibrator.predict(model.predict_proba(cleaned[features])[:, 1])` (feature list in `metrics.json`).\n'
         '3. `expected_unpaid = (1 - p) * amount_due`; route dispute / hardship accounts to the specialist team.\n'
         '4. Give agents the top {cfg.AGENT_CAPACITY_SHARE:.0%} of the cohort by expected unpaid; nudge the rest by SMS / app.\n'
         '\n'
         '## Excluded columns\n'
         '- `account_status_at_extract`, `amount_recovered_30d`, `total_contact_attempts_30d`: captured after day {cfg.SCORING_DAY} (leakage)\n'
         '- IDs, dates and the cohort month\n'
         '\n'
         '## Performance (June, out of time)\n'
         '| Check | Result |\n'
         '|---|---|\n'
         '| ROC-AUC | {g["roc_auc"]:.3f} |\n'
         '| PR-AUC | {g["pr_auc"]:.3f} (baseline {metrics["june_baseline_pr_auc"]:.3f}) |\n'
         '| Brier raw / calibrated | {g["brier"]:.4f} / {g["brier_calibrated"]:.4f} |\n'
         '| Unpaid amount covered by the agent list | {result["coverage_model"]:.0%} vs {result["coverage_dpd_rule"]:.0%} with highest-DPD-first |\n'
         '\n'
         '## Limitations\n'
         '- Pay rates fell every month in 2026 (BNPL fastest): re-calibrate monthly, retrain quarterly.\n'
         '- Probabilities describe paying *with* the current treatment mix; they are not treatment effects.\n'
         '"""\n'
         '(cfg.PACKAGE_DIR / "README.md").write_text(readme, encoding="utf-8")\n'
         'print(readme)'),
]


def main():
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    for name, cells in [("01_data_preprocessing", NB01), ("02_model_training", NB02),
                        ("03_model_testing", NB03), ("04_worklist_and_package", NB04)]:
        write_notebook(CODE_DIR / f"{name}.ipynb", cells)


if __name__ == "__main__":
    main()

"""
Self-test for the UC2 pipeline: proves every planted bug fails the way the answer key
says, and that the documented fix clears it. Simulates the take: each step is a fresh
kernel + "Run All" on a temporary copy of the workspace (the real workspace is untouched).

Usage:  .venv/bin/python prep/selftest_uc2.py        (Mac)
        .venv\\Scripts\\python.exe prep\\selftest_uc2.py  (Windows)
"""
import json
import os
import shutil
import tempfile
from pathlib import Path

import pandas as pd

from selftest_uc1 import apply_fix, expect_failure, run_notebook, step

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "recording_workspace" / "UC2_Propensity_To_Pay"

# (file, buggy text, fixed text) - must match use_cases/UC2_Planted_Bugs_Answer_Key.md
FIXES = {
    "P1": ("01_data_preprocessing.ipynb",
           'df["delinquency_date"] = pd.to_datetime(df["delinquency_date"], format="mixed")',
           'df["delinquency_date"] = cfg.parse_dates(df["delinquency_date"])'),
    "P2": ("01_data_preprocessing.ipynb",
           'df["income_missing"] = df["monthly_income"].isna().astype(int)\n',
           'df["monthly_income"] = df["monthly_income"].replace(0, np.nan)\n'
           'df["income_missing"] = df["monthly_income"].isna().astype(int)\n'),
    "T1": ("02_model_training.ipynb",
           'train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]',
           'train_df = df[df["cohort_month"].isin(cfg.TRAIN_MONTHS)]'),
    "T2": ("pipeline_config.py",
           'LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d"]',
           'LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d", "total_contact_attempts_30d"]'),
    "E1": ("03_model_testing.ipynb",
           'test_df["expected_unpaid"] = test_df["p_pay"] * test_df["amount_due"]',
           'test_df["expected_unpaid"] = (1 - test_df["p_pay"]) * test_df["amount_due"]'),
}


def fix(code_dir, key):
    apply_fix(code_dir, key, FIXES)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="uc2_selftest_"))
    work = tmp / "UC2_Propensity_To_Pay"
    shutil.copytree(SRC, work, ignore=shutil.ignore_patterns("3_Intermediate", "4_Output", ".ipynb_checkpoints", "__pycache__"))
    code_dir = work / "Deliverables" / "2_Code"
    os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(max(1, (os.cpu_count() or 2) - 1)))
    print(f"Self-test on a temporary copy: {work}\n")
    results = {}

    print("01 data preprocessing")
    step("P1 buggy: format='mixed' misreads day-first dates -> months 7-12",
         lambda: expect_failure(code_dir, "01_data_preprocessing.ipynb", AssertionError, "cohort months outside Jan-Jun"))
    fix(code_dir, "P1")
    step("P2 buggy: zero incomes give infinite payment_burden",
         lambda: expect_failure(code_dir, "01_data_preprocessing.ipynb", AssertionError, "infinite payment_burden"))
    fix(code_dir, "P2")

    def cleaned():
        ns = run_notebook(code_dir, "01_data_preprocessing.ipynb")
        assert ns["df"]["cohort_month"].between(1, 6).all()
        results["dq_log"] = {r["step"]: r["rows_affected"] for r in ns["dq_log"]}
        return f"rows saved: {len(ns['df']):,} | log: {results['dq_log']}"
    step("fixed: runs clean", cleaned)

    print("02 model training")
    step("T1 buggy: training window includes the calibration month",
         lambda: expect_failure(code_dir, "02_model_training.ipynb", AssertionError, "train and calibration windows overlap"))
    fix(code_dir, "T1")

    def leak_symptom():
        ns = run_notebook(code_dir, "02_model_training.ipynb")
        val = pd.DataFrame(ns["rows"]).set_index("model")
        top = ns["importance"].index[0]
        assert top == "total_contact_attempts_30d", f"expected the leak to top the importance, got {top}"
        assert val.loc["gradient_boosting", "may_roc_auc"] > 0.86, val
        return f"May ROC-AUC with leak: {val['may_roc_auc'].round(3).to_dict()} | top feature: {top}"
    step("T2 buggy: total_contact_attempts_30d tops importance, AUC inflated", leak_symptom)
    fix(code_dir, "T2")

    def trained():
        ns = run_notebook(code_dir, "02_model_training.ipynb")
        val = pd.DataFrame(ns["rows"]).set_index("model")
        assert 0.76 < val.loc["gradient_boosting", "may_roc_auc"] < 0.86, val
        results["may"] = val.round(3).to_dict("index")
        results["pay_rate_by_month"] = ns["by_month"]["pay_rate"].round(3).tolist()
        results["top_features"] = ns["importance"].head(6).round(3).to_dict()
        return f"May after fix: {results['may']}"
    step("fixed: realistic May AUC", trained)

    print("03 model testing")

    def logic_symptom():
        ns = run_notebook(code_dir, "03_model_testing.ipynb")
        pr = ns["prioritisation"]
        assert pr.iloc[1] < pr.iloc[0] and not ns["checks"]["pass"].all(), pr
        return f"coverage with p x amount (wrong): {pr.round(3).to_dict()}"
    step("E1 buggy: ranks by p x amount -> worse than today's rule", logic_symptom)
    fix(code_dir, "E1")

    def tested():
        ns = run_notebook(code_dir, "03_model_testing.ipynb")
        assert ns["checks"]["pass"].all(), ns["checks"].to_string()
        results["june"] = ns["comparison"].round(4).to_dict("index")
        results["calibration"] = ns["calibration"].round(4).to_dict("index")
        results["prioritisation"] = ns["prioritisation"].round(3).to_dict()
        results["capacity"] = ns["capacity"]
        results["eligible"] = len(ns["eligible"])
        return f"June: {ns['comparison'].loc['gradient_boosting'].round(3).to_dict()} | coverage {results['prioritisation']}"
    step("fixed: all acceptance checks pass", tested)

    print("04 work list and package")

    def worklisted():
        ns = run_notebook(code_dir, "04_worklist_and_package.ipynb")
        r = ns["result"]
        assert r["coverage_model"] > r["coverage_dpd_rule"] and len(ns["work_list"]) == r["agent_capacity"]
        assert ns["work_list"][["has_open_dispute", "hardship_flag"]].to_numpy().max() == 0
        results["work_list"] = r
        return str(r)
    step("runs clean, list fits capacity, beats today's rule", worklisted)

    deliverables = work / "Deliverables"
    expected = ["3_Intermediate/artifact 2 - cleaned accounts.csv", "3_Intermediate/artifact 3 - data quality log.csv",
                "3_Intermediate/artifact 4 - time split.csv",
                "3_Intermediate/artifact 5 - trained models/gradient_boosting.joblib",
                "3_Intermediate/artifact 5 - trained models/calibrator.joblib",
                "3_Intermediate/artifact 6 - model comparison.csv",
                *[f"3_Intermediate/artifact 7 - charts/{c}.png" for c in [
                    "01_missing_values", "02_accounts_by_month", "03_pay_rate_by_burden", "04_data_quality_fixes",
                    "05_pay_rate_by_month", "06_permutation_importance", "07_calibration", "08_prioritisation",
                    "09_shap_summary", "10_shap_dependence", "11_work_list_vs_dpd_rule"]],
                "3_Intermediate/artifact 8 - june agent work list.csv",
                "4_Output/final output 3 - model package/model.joblib",
                "4_Output/final output 3 - model package/README.md"]
    missing = [f for f in expected if not (deliverables / f).exists()]
    assert not missing, f"missing outputs: {missing}"
    print(f"  [OK] all {len(expected)} expected artifacts written\n")

    shutil.rmtree(tmp, ignore_errors=True)
    print("SELF-TEST PASSED")
    print(json.dumps(results, indent=1, default=str))


if __name__ == "__main__":
    main()

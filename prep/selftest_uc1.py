"""
Self-test for the UC1 pipeline: proves every planted bug fails the way the answer key
says, and that the documented fix clears it. Simulates the take: each step is a fresh
kernel + "Run All" on a temporary copy of the workspace (the real workspace is untouched).

Usage:  .venv/bin/python prep/selftest_uc1.py        (Mac)
        .venv\\Scripts\\python.exe prep\\selftest_uc1.py  (Windows)
"""
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "recording_workspace" / "UC1_Cross_Sell"

# (file, buggy text, fixed text) - must match use_cases/UC1_Planted_Bugs_Answer_Key.md
FIXES = {
    "P1": ("01_data_preprocessing.ipynb",
           'df["customer_since"] = pd.to_datetime(df["customer_since"], format="%Y-%m-%d")',
           'iso = pd.to_datetime(df["customer_since"], format="%Y-%m-%d", errors="coerce")\n'
           'day_first = pd.to_datetime(df["customer_since"], format="%d/%m/%Y", errors="coerce")\n'
           'log("day-first dates", (iso.isna() & day_first.notna()).sum(), "parsed as DD/MM/YYYY")\n'
           'df["customer_since"] = iso.fillna(day_first)\n'
           'assert df["customer_since"].notna().all()'),
    "P2": ("01_data_preprocessing.ipynb",
           'df["region"] = df["region"].str.lower()',
           'df["region"] = df["region"].str.strip().str.lower()'),
    "T1": ("pipeline_config.py",
           '("num", StandardScaler(), numeric_columns(df)),',
           '("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns(df)),'),
    "T2": ("pipeline_config.py",
           'LEAKY_COLUMNS = ["cross_sell_product_type"]',
           'LEAKY_COLUMNS = ["cross_sell_product_type", "welcome_pack_sent"]'),
    "E1": ("03_model_testing.ipynb",
           'model.predict(X_test)',
           'model.predict_proba(X_test)[:, 1]'),
}


def apply_fix(code_dir, key):
    name, old, new = FIXES[key]
    path = code_dir / name
    if name.endswith(".ipynb"):
        nb = json.loads(path.read_text(encoding="utf-8"))
        hits = 0
        for cell in nb["cells"]:
            src = "".join(cell["source"])
            if old in src:
                hits += 1
                cell["source"] = src.replace(old, new).splitlines(keepends=True)
        assert hits == 1, f"{key}: expected the buggy text once in {name}, found {hits}"
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        text = path.read_text(encoding="utf-8")
        assert text.count(old) == 1, f"{key}: buggy text not found exactly once in {name}"
        path.write_text(text.replace(old, new), encoding="utf-8")


def run_notebook(code_dir, name):
    """Fresh kernel + Run All: executes code cells in order; returns the namespace or raises."""
    nb = json.loads((code_dir / name).read_text(encoding="utf-8"))
    sys.modules.pop("pipeline_config", None)
    namespace = {"__name__": "__main__"}
    cwd = os.getcwd()
    os.chdir(code_dir)
    sys.path.insert(0, str(code_dir))
    try:
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), name, "exec"), namespace)
                plt.close("all")
    finally:
        sys.path.remove(str(code_dir))
        os.chdir(cwd)
    return namespace


def expect_failure(code_dir, name, exc_type, text):
    try:
        run_notebook(code_dir, name)
    except exc_type as exc:
        assert text in str(exc), f"{name}: expected '{text}' in error, got: {exc}"
        return str(exc).splitlines()[0][:110]
    raise AssertionError(f"{name}: expected {exc_type.__name__} but it ran cleanly")


def step(label, fn):
    t = time.time()
    detail = fn()
    print(f"  [OK] {label:<58} {time.time() - t:5.1f}s" + (f"\n         {detail}" if detail else ""))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="uc1_selftest_"))
    work = tmp / "UC1_Cross_Sell"
    shutil.copytree(SRC, work, ignore=shutil.ignore_patterns("3_Intermediate", "4_Output", ".ipynb_checkpoints"))
    code_dir = work / "Deliverables" / "2_Code"
    os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(max(1, (os.cpu_count() or 2) - 1)))
    print(f"Self-test on a temporary copy: {work}\n")
    results = {}

    print("01 data preprocessing")
    step("P1 buggy: single date format raises ValueError",
         lambda: expect_failure(code_dir, "01_data_preprocessing.ipynb", ValueError, "doesn't match format"))
    apply_fix(code_dir, "P1")
    step("P2 buggy: untrimmed region labels fail the 5-region check",
         lambda: expect_failure(code_dir, "01_data_preprocessing.ipynb", AssertionError, "unexpected regions"))
    apply_fix(code_dir, "P2")
    step("fixed: runs clean, 20,000 customers saved",
         lambda: f"rows saved: {len(run_notebook(code_dir, '01_data_preprocessing.ipynb')['df']):,}")

    print("02 model training")
    step("T1 buggy: baseline without imputer fails on NaN",
         lambda: expect_failure(code_dir, "02_model_training.ipynb", ValueError, "NaN"))
    apply_fix(code_dir, "T1")

    def leak_symptom():
        cv = pd.DataFrame(run_notebook(code_dir, "02_model_training.ipynb")["cv_rows"]).set_index("model")
        assert cv["cv_roc_auc"].min() > 0.95, f"expected a too-good-to-be-true AUC, got {cv['cv_roc_auc'].round(3).to_dict()}"
        return f"CV ROC-AUC with welcome_pack_sent still in: {cv['cv_roc_auc'].round(3).to_dict()}"
    step("T2 buggy: leaky welcome_pack_sent gives CV AUC > 0.95", leak_symptom)
    apply_fix(code_dir, "T2")

    def trained():
        cv = pd.DataFrame(run_notebook(code_dir, "02_model_training.ipynb")["cv_rows"]).set_index("model")
        assert 0.74 < cv.loc["gradient_boosting", "cv_roc_auc"] < 0.86
        assert cv.loc["gradient_boosting", "cv_pr_auc"] > cv.loc["baseline_logreg", "cv_pr_auc"]
        return f"CV after fix: {cv.round(3).to_dict('index')}"
    step("fixed: CV AUC realistic, boosting beats baseline", trained)

    print("03 model testing")

    def metric_symptom():
        ns = run_notebook(code_dir, "03_model_testing.ipynb")
        roc = ns["comparison"].loc["gradient_boosting", "roc_auc"]
        assert roc < 0.7 and not ns["checks"]["pass"].all(), f"expected low AUC from hard labels, got {roc}"
        return f"ROC-AUC computed on 0/1 labels: {roc}; acceptance checks: {ns['checks']['pass'].tolist()}"
    step("E1 buggy: metrics on predict() labels -> low AUC, checks fail", metric_symptom)
    apply_fix(code_dir, "E1")

    def tested():
        ns = run_notebook(code_dir, "03_model_testing.ipynb")
        assert ns["checks"]["pass"].all(), ns["checks"].to_string()
        results["holdout"] = ns["comparison"].to_dict("index")
        results["top20_lift"] = round(float(ns["top20_lift"]), 2)
        results["decile_lift"] = ns["deciles"]["lift"].round(2).tolist()
        return f"hold-out: {ns['comparison'].loc['gradient_boosting'].to_dict()} | top-20% lift {results['top20_lift']}x"
    step("fixed: all acceptance checks pass", tested)

    print("04 back-test and package")

    def backtested():
        ns = run_notebook(code_dir, "04_backtest_and_package.ipynb")
        bt = ns["backtest"]
        assert bt["passes_backtest_lift"] and bt["customers_contacted"] == 4000
        results["backtest"] = bt
        return f"{bt['actual_conversions']} vs {bt['random_conversions']} random, profit ${bt['profit_model_usd']:,} vs ${bt['profit_random_usd']:,}"
    step("runs clean, back-test passes", backtested)

    deliverables = work / "Deliverables"
    expected = ["3_Intermediate/artifact 2 - cleaned customers.csv", "3_Intermediate/artifact 3 - data quality log.csv",
                "3_Intermediate/artifact 4 - train test split.csv",
                "3_Intermediate/artifact 5 - trained models/gradient_boosting.joblib",
                "3_Intermediate/artifact 6 - model comparison.csv",
                "3_Intermediate/artifact 7 - evaluation charts/shap_summary.png",
                "3_Intermediate/artifact 8 - backtest scored customers.csv",
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

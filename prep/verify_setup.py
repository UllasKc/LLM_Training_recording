"""
Check that the Mac is ready to record: Python, packages, input files, disk space and RAM.

Run by setup_mac.sh, or any time with:  .venv/bin/python prep/verify_setup.py
"""
import importlib
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT / "recording_workspace"

PACKAGES = {"numpy": "2.0.2", "pandas": "2.2.3", "sklearn": "1.5.2", "matplotlib": "3.9.2",
            "seaborn": "0.13.2", "shap": "0.46.0", "joblib": "1.4.2", "openpyxl": "3.1.5",
            "docx": None, "ipykernel": "6.29.5"}

INPUTS = {
    "UC1_Cross_Sell": {"input 1 - customers.csv": 20_260, "input 2 - data dictionary.xlsx": None,
                       "input 3 - campaign brief.docx": None},
    "UC2_Propensity_To_Pay": {"input 1 - collections accounts.csv": 20_240,
                              "input 2 - data dictionary.xlsx": None,
                              "input 3 - collections strategy brief.docx": None},
}

problems, warnings = [], []


def check(label, ok, msg="", warn_only=False):
    print(f"  [{'OK' if ok else ('WARN' if warn_only else 'FAIL')}] {label}{'' if ok else ' - ' + msg}")
    if not ok:
        (warnings if warn_only else problems).append(label)


print("Python")
check(f"Python {platform.python_version()}", sys.version_info[:2] == (3, 12), "Python 3.12 expected")
check(f"Architecture {platform.machine()}", platform.machine() == "arm64", "Apple Silicon expected",
      warn_only=sys.platform != "darwin")

print("Packages")
for mod, want in PACKAGES.items():
    try:
        have = getattr(importlib.import_module(mod), "__version__", "installed")
        check(f"{mod} {have}", want is None or have == want, f"expected {want}")
    except Exception as exc:  # noqa: BLE001 - report any import failure
        check(mod, False, f"import failed: {exc}")

print("Input files")
import pandas as pd  # noqa: E402

for uc, files in INPUTS.items():
    for name, rows in files.items():
        path = WS / uc / "Deliverables" / name
        if not path.exists():
            check(f"{uc}/{name}", False, "missing - run the generators in prep/")
            continue
        if rows:
            n = len(pd.read_csv(path))
            check(f"{uc}/{name} ({n:,} rows)", n == rows, f"expected {rows:,} rows")
        else:
            check(f"{uc}/{name}", True)

print("Model training speed")
try:
    import numpy as np
    from sklearn.ensemble import HistGradientBoostingClassifier

    rng = np.random.default_rng(0)
    X, y = rng.normal(size=(20_000, 25)), rng.integers(0, 2, 20_000)
    t = time.time()
    HistGradientBoostingClassifier(max_iter=300).fit(X, y)
    secs = time.time() - t
    check(f"20k-row boosted model trains in {secs:.1f}s", secs < 30, "slow machine - keep tuning small", warn_only=True)
except Exception as exc:  # noqa: BLE001
    check("model training", False, str(exc))

print("Machine")
free_gb = shutil.disk_usage(Path.home()).free / 1e9
check(f"Free disk {free_gb:.0f} GB", free_gb >= 50, "need ~50 GB+ for a 30-35 min recording", warn_only=True)
if sys.platform == "darwin":
    ram_gb = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout) / 2**30
    check(f"RAM {ram_gb:.0f} GB", ram_gb >= 16, "16 GB+ preferred", warn_only=True)

print()
if problems:
    print(f"NOT READY - fix: {', '.join(problems)}")
    sys.exit(1)
print("READY" + (f" (warnings: {', '.join(warnings)})" if warnings else ""))

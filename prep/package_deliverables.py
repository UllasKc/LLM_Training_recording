"""
Validate a finished take against the Mercor deliverable rules and build Deliverables.zip.
Run it OFF camera, after the recording.

    Windows:  prep\\package_deliverables.cmd UC1        (or UC2, or double-click for a menu)
    Mac:      bash prep/package_deliverables.sh UC1

Checks
  - every required file exists
  - labels: 1_Input -> "input N", 3_Intermediate -> "artifact N", 4_Output -> "final output N"
  - every planted bug was fixed in the corrected code
  - no notebook contains an error output (and warns about notebooks that were never run)

Builds  <workspace>/Deliverables.zip  with the Mercor layout:
  1_Input/        inputs 1-4  +  "input 5 - pipeline code as received"  (the original code, from this repo)
  3_Intermediate/ artifacts
  4_Output/       final outputs 1-3  +  "final output 4 - corrected pipeline code"  (your fixed 2_Code)
Junk (__pycache__, .ipynb_checkpoints, .vscode, .DS_Store, desktop.ini, Office lock files) is left out.
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

USE_CASES = {
    "UC1": {
        "name": "UC1_Cross_Sell",
        "required": [
            "1_Input/input 1 - customers.csv", "1_Input/input 2 - data dictionary.xlsx",
            "1_Input/input 3 - campaign brief.pdf", "1_Input/input 4 - summary deck template.pptx",
            "3_Intermediate/artifact 1 - exploratory pivot analysis.xlsx",
            "3_Intermediate/artifact 2 - cleaned customers.csv", "3_Intermediate/artifact 3 - data quality log.csv",
            "3_Intermediate/artifact 4 - train test split.csv",
            "3_Intermediate/artifact 5 - trained models/gradient_boosting.joblib",
            "3_Intermediate/artifact 6 - model comparison.csv",
            *[f"3_Intermediate/artifact 7 - charts/{c}.png" for c in ["03_data_quality_fixes", "05_lift_by_decile", "08_shap_dependence"]],
            "3_Intermediate/artifact 8 - backtest scored customers.csv",
            "4_Output/final output 1 - backtest target list.xlsx",
            "4_Output/final output 2 - cross-sell summary.pptx",
            "4_Output/final output 3 - model package/model.joblib",
            "4_Output/final output 3 - model package/metrics.json",
            "4_Output/final output 3 - model package/README.md",
        ],
    },
    "UC2": {
        "name": "UC2_Propensity_To_Pay",
        "required": [
            "1_Input/input 1 - collections accounts.csv", "1_Input/input 2 - data dictionary.xlsx",
            "1_Input/input 3 - collections strategy brief.pdf", "1_Input/input 4 - summary deck template.pptx",
            "3_Intermediate/artifact 1 - exploratory pivot analysis.xlsx",
            "3_Intermediate/artifact 2 - cleaned accounts.csv", "3_Intermediate/artifact 3 - data quality log.csv",
            "3_Intermediate/artifact 4 - time split.csv",
            "3_Intermediate/artifact 5 - trained models/gradient_boosting.joblib",
            "3_Intermediate/artifact 5 - trained models/calibrator.joblib",
            "3_Intermediate/artifact 6 - model comparison.csv",
            *[f"3_Intermediate/artifact 7 - charts/{c}.png" for c in ["04_data_quality_fixes", "07_calibration", "10_shap_dependence"]],
            "3_Intermediate/artifact 8 - june agent work list.csv",
            "4_Output/final output 1 - june agent work list.xlsx",
            "4_Output/final output 2 - collections summary.pptx",
            "4_Output/final output 3 - model package/model.joblib",
            "4_Output/final output 3 - model package/calibrator.joblib",
            "4_Output/final output 3 - model package/metrics.json",
            "4_Output/final output 3 - model package/README.md",
        ],
    },
}
LABELS = {"1_Input": "input ", "3_Intermediate": "artifact ", "4_Output": "final output "}
JUNK_DIRS = {"__pycache__", ".ipynb_checkpoints", ".vscode"}
JUNK_FILES = {".DS_Store", "desktop.ini", "Thumbs.db"}


def desktop():
    if sys.platform == "win32":
        import ctypes
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0010, None, 0, buf)  # CSIDL_DESKTOPDIRECTORY
        return Path(buf.value)
    return Path.home() / "Desktop"


def is_junk(path):
    return (any(part in JUNK_DIRS for part in path.parts) or path.name in JUNK_FILES
            or path.name.startswith("~$"))


def squash(text):
    return "".join(text.split())


def fix_checks(uc):
    """(bug id, file, ok-function) per planted bug, from the self-test definitions; whitespace-insensitive."""
    module = __import__("selftest_uc1" if uc == "UC1" else "selftest_uc2")
    checks = []
    for key, (name, buggy, fixed) in module.FIXES.items():
        if buggy in fixed:
            # the fix keeps the original line and adds code next to it: the added lines must be present
            added = [line for line in fixed.splitlines() if line and line not in buggy.splitlines()]
            checks.append((key, name, lambda text, a=added: all(squash(x) in squash(text) for x in a)))
        else:
            checks.append((key, name, lambda text, b=buggy: squash(b) not in squash(text)))
    return checks


def source_text(path):
    if path.suffix == ".ipynb":
        nb = json.loads(path.read_text(encoding="utf-8"))
        return "\n".join("".join(c["source"]) for c in nb["cells"])
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("use_case", choices=["UC1", "UC2", "uc1", "uc2"])
    parser.add_argument("--workspace", type=Path, help="folder that contains Deliverables (default: Desktop/<use case>)")
    args = parser.parse_args()
    uc = args.use_case.upper()
    spec = USE_CASES[uc]
    workspace = args.workspace or desktop() / spec["name"]
    deliverables = workspace / "Deliverables"
    code_dir = deliverables / "2_Code"
    original_code = ROOT / "recording_workspace" / spec["name"] / "Deliverables" / "2_Code"
    fails, warns = [], []

    def report(ok, label, msg="", warn=False):
        print(f"  [{'OK' if ok else ('WARN' if warn else 'FAIL')}] {label}{'' if ok else '  - ' + msg}")
        if not ok:
            (warns if warn else fails).append(label)

    print(f"Packaging {uc}: {deliverables}\n")
    if not deliverables.exists():
        print(f"ERROR: {deliverables} not found. Pass --workspace if the folder is somewhere else.")
        sys.exit(1)

    print("Required files")
    for rel in spec["required"]:
        report((deliverables / rel).exists(), rel, "missing")

    print("Labels")
    for folder, prefix in LABELS.items():
        for item in sorted((deliverables / folder).iterdir()) if (deliverables / folder).exists() else []:
            if is_junk(item):
                continue
            report(item.name.lower().startswith(prefix), f"{folder}/{item.name}", f"name must start with '{prefix.strip()} N'")

    print("Planted bugs fixed")
    for key, name, ok in fix_checks(uc):
        path = code_dir / name
        report(path.exists() and ok(source_text(path)), f"{key} in {name}", "still looks unfixed - compare with the script")

    print("Notebooks")
    for nb_path in sorted(code_dir.glob("*.ipynb")):
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
        errors = sum(o.get("output_type") == "error" for c in code_cells for o in c.get("outputs", []))
        ran = all(c.get("execution_count") for c in code_cells)
        report(errors == 0, f"{nb_path.name}: no error outputs", f"{errors} cell(s) still show an error - re-run it")
        report(ran, f"{nb_path.name}: every cell has been run", "some cells were never run", warn=True)

    zip_path = workspace / "Deliverables.zip"
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(deliverables.rglob("*")):
            rel = path.relative_to(deliverables)
            if path.is_dir() or is_junk(rel) or rel.parts[0] == "2_Code":
                continue
            zf.write(path, Path("Deliverables") / rel)
            count += 1
        for src, dest in [(original_code, "1_Input/input 5 - pipeline code as received"),
                          (code_dir, "4_Output/final output 4 - corrected pipeline code")]:
            for path in sorted(src.rglob("*")):
                rel = path.relative_to(src)
                if path.is_file() and not is_junk(rel):
                    zf.write(path, Path("Deliverables") / dest / rel)
                    count += 1
    size_mb = zip_path.stat().st_size / 1e6
    print(f"\nBuilt {zip_path} ({count} files, {size_mb:.1f} MB)")

    print()
    if fails:
        print(f"NOT READY - fix these, re-run the notebook(s) if needed, then package again: {', '.join(fails)}")
        sys.exit(1)
    print("READY TO UPLOAD" + (f" (warnings: {', '.join(warns)})" if warns else ""))
    print("Upload to Mercor Studio: video.mp4 · unmodified recording_<timestamp>.zip · Deliverables.zip · "
          f"Metadata.rtf ({workspace / 'Metadata.rtf'})")


if __name__ == "__main__":
    main()

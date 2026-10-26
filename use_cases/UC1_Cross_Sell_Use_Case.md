# UC1 – Build and Explain a Cross-Sell / Up-Sell Model

> **Prep document, never open on camera.** Companion files: [UC1_RECORDING_SCRIPT.md](../UC1_RECORDING_SCRIPT.md) (the complete take: clicks, narration, fixes) and [UC1_Planted_Bugs_Answer_Key.md](UC1_Planted_Bugs_Answer_Key.md) (the 5 fixes).

| | |
|---|---|
| Domain | Data Science & ML (DSD) |
| Role | Senior Data Scientist |
| End users | Data Science, Marketing (CRM & Cross-Sell) |
| Complexity | Advanced |
| Target length | ~38 min (allowed 15:00–45:59, one take) |
| Submitted by | Ullas KC (approved by manager) |

---

## 1. What changed from the approved version, and why

The approved use case (predict which existing customers will buy another product; build, validate, explain, package) is **unchanged**. Adjustments:

| # | Approved version | Recorded version | Why |
|---|---|---|---|
| 1 | VS Code **or Internal AutoML Tool** | VS Code (Jupyter) only | Reviewers can't check a proprietary tool; expert judgment must be visible |
| 2 | Terminal, GitHub Desktop, "commit with README" | No Git on camera. README and model package generated into `4_Output` | Your decision (no Git in the demo) |
| 3 | Code written during the video | The **team's existing pipeline** (config + 4 notebooks, built for an earlier snapshot) is a **pre-existing asset**; on camera the expert runs it on the new extract, **diagnoses and fixes 5 issues**, and interprets every result | Matches the internal benchmark recording and Mercor's accepted pattern ("diagnosing schema drift in an existing data pipeline"); keeps 35–40 min focused on judgment instead of typing |
| 4 | Apps: VS Code, Terminal, GitHub Desktop, PowerPoint | **Word → Excel (pivot EDA) → VS Code → Excel (ROI) → PowerPoint** | Multiple connected apps: the benchmark spends 5–10 min on Excel pivots |
| 5 | "Starting material: CSV" | CSV + data dictionary + campaign brief + **deck template** | Business context, constraints and acceptance criteria are mandatory |
| 6 | Generic "train baseline and improve" | Leakage, compliance (opt-in, no gender), budget-constrained **out-of-fold back-test** with ROI | Passes the intern test; real outcomes prove the value |
| 7 | Output: notebook; repo; 3-slide summary | Pivot workbook; corrected pipeline + model package; back-test list with ROI; summary deck | Labelled `input N` / `artifact N` / `final output N` |

---

## 2. Mercor Studio idea submission (copy into the fields)

**Goal**
Before Marketing commits its Q4 cross-sell budget, prove that model-based targeting beats random contact. Explore the 30-Jun-2026 customer snapshot, run the team's existing cross-sell pipeline on it, diagnose and fix what the new extract breaks, validate the model against acceptance criteria, and back-test the 4,000 customers it would have selected against their actual July–September outcomes.

**Starting material**
- `input 1 - customers.csv`: 20,260 rows / 20,000 customers (CRM-merge duplicates), 25 attributes, label `next_product_purchased_90d` (Jul–Sep, 11.6%)
- `input 2 - data dictionary.xlsx`; `input 3 - campaign brief.docx` (budget, $4/contact, $150 margin, opt-in only, no gender, exclude 2+ complaints, acceptance criteria); `input 4 - summary deck template.pptx`
- **Pre-existing code:** `2_Code/` holds the team's pipeline (`pipeline_config.py` + notebooks 01 preprocessing, 02 training, 03 testing, 04 back-test & packaging), written for an earlier snapshot and not yet run on this extract

**Apps**
Microsoft Word, Microsoft Excel (PivotTables, formulas), Visual Studio Code (Jupyter, Python: pandas, scikit-learn, SHAP), Microsoft PowerPoint, File Explorer / Finder

**Deliverable**
Exploratory pivot workbook; corrected pipeline with outputs; cleaned data and data-quality log; trained models, model comparison and evaluation charts; out-of-fold back-test list with ROI workbook; packaged model (model, metrics, README); completed summary deck.

**How the result is checked**
Hold-out ROC-AUC ≥ 0.78; beats the logistic baseline on PR-AUC; top-20% lift ≥ 2.5×; no leaky or protected fields; back-test list of exactly 4,000 compliant customers, scored out of fold, converting at ≥ 2× the eligible average; profit compared with random selection.

**Pitch: problem statement**
Cross-selling to existing customers is the cheapest growth lever, but random campaigns convert only ~1 in 9. Marketing needs evidence, on real outcomes, that targeting pays before committing budget, and an existing pipeline has to work on a changed data extract.

**Pitch: solution**
A senior data scientist profiles the new extract in Excel (pivots reveal duplicates, label drift, a leaking column and non-random missing income), runs the team's pipeline on it, and fixes five issues: two schema-drift breaks (date format, region labels), a missing imputer, a newly added leaky column that inflates AUC to 0.98, and an evaluation bug that scored labels instead of probabilities. The fixed model reaches ROC-AUC 0.81 and 2.8× top-20% lift. An out-of-fold back-test shows the 4,000 customers it would have picked converted 1,312 times vs 546 at random, worth $181k vs $66k on the same budget.

---

## 3. Detailed task scenario

**Pre-existing assets**: `Desktop/UC1_Cross_Sell/Deliverables/`:
```
1_Input/         input 1-4 (data, dictionary, brief, deck template)
2_Code/          pipeline_config.py, 01_data_preprocessing, 02_model_training, 03_model_testing, 04_backtest_and_package
3_Intermediate/  empty (pipeline outputs)
4_Output/        empty (business deliverables)
```
Python 3.12 venv with the `Python 3.12 (ds-venv)` kernel.

**Business context and constraints**: 4,000 contacts at $4; $150 margin; opt-in only; gender not a model input; exclude ≥ 2 complaints; only snapshot-date information; back-test must be out of sample.

**Multi-phase workflow**
1. Brief (Word) and dictionary (Excel): constraints, leakage suspects.
2. Excel PivotTables on the raw extract: conversion by product count, region label drift, the welcome-pack leak, income missingness by segment → **artifact 1**.
3. Review the existing pipeline structure and config in VS Code.
4. Run 01 preprocessing → fix **P1** (date formats) and **P2** (region labels) → artifacts 2–3.
5. Run 02 training → fix **T1** (missing imputer) and **T2** (leaky column) → artifacts 4–5.
6. Run 03 testing → fix **E1** (labels vs probabilities) → artifacts 6–7, acceptance check.
7. Run 04 back-test and packaging → artifact 8, **final output 3**.
8. Excel ROI validation → **final output 1**.
9. Finish the deck from the template → **final output 2**.

**Why an intern could not do this:** they wouldn't spot that AUC 0.98 is leakage, would trust a 0.58 hold-out score instead of recognising an evaluation bug, would let pandas guess ambiguous dates, would score the back-test in-sample, and couldn't tie model metrics to budget and compliance.

---

## 4. App topology (for Metadata.rtf)

`TextEdit (Lookup) -> Finder (Lookup) -> Microsoft Word (Lookup) -> Microsoft Excel (Lookup) -> Microsoft Excel (Create) -> Visual Studio Code (Modify) -> Microsoft Excel (Create) -> Microsoft PowerPoint (Modify) -> Finder (Lookup)`

(Windows practice: Notepad instead of TextEdit, File Explorer instead of Finder.)

---

## 5. Deliverables map

| File | Made by |
|---|---|
| `1_Input/input 1 - customers.csv`, `input 2 - data dictionary.xlsx`, `input 3 - campaign brief.docx`, `input 4 - summary deck template.pptx` | pre-loaded |
| `2_Code/*` | pre-loaded pipeline, **corrected on camera** |
| `3_Intermediate/artifact 1 - exploratory pivot analysis.xlsx` | Excel |
| `3_Intermediate/artifact 2 - cleaned customers.csv` · `artifact 3 - data quality log.csv` | notebook 01 |
| `3_Intermediate/artifact 4 - train test split.csv` · `artifact 5 - trained models/` | notebook 02 |
| `3_Intermediate/artifact 6 - model comparison.csv` · `artifact 7 - evaluation charts/` (lift, calibration, SHAP) | notebook 03 |
| `3_Intermediate/artifact 8 - backtest scored customers.csv` | notebook 04 |
| `4_Output/final output 1 - backtest target list.xlsx` | Excel |
| `4_Output/final output 2 - cross-sell summary.pptx` | PowerPoint |
| `4_Output/final output 3 - model package/` (`model.joblib`, `metrics.json`, `README.md`) | notebook 04 |

After recording (off camera), zip `Deliverables` → `Deliverables.zip`.

---

## 6. Planted data issues (in input 1) and how the pipeline handles them

| Issue | Size | Handled in |
|---|---|---|
| 200 exact duplicates + 60 conflicting rows per customer | 260 rows | 01 §2 (de-duplicate before splitting) |
| Mixed date formats in `customer_since` | ~400 | 01 §3 (**P1**) |
| Region / product label variants (case, spaces, `N.`, `CC`…) | ~4% / ~3% | 01 §4 (**P2**) |
| Sentinels: age 0/999, balance −99999, tenure −1 | ~160 | 01 §3, §5 |
| Income missing, more often for Mass (not at random) | ~8% | 01 §6 (flag + segment median) |
| Structural missing: `email_open_rate` (opted out), `days_since_last_contact` (never contacted) | ~24% / ~16% | 01 §6 |
| Leak 1 `cross_sell_product_type` (filled only for buyers) | — | config `LEAKY_COLUMNS` (already excluded) |
| Leak 2 `welcome_pack_sent` (sent after purchase) | — | config (**T2**) |
| Protected `gender` | — | config `PROTECTED_COLUMNS` |
| Imbalance, 11.6% positive | — | stratified split, PR-AUC, lift |

## 7. Reference results (tested by `prep/selftest_uc1.py`)

| | Value |
|---|---|
| CV ROC-AUC, leak present (T2 symptom) | ~0.98 |
| Hold-out ROC-AUC on labels (E1 symptom) | ~0.58 |
| Hold-out ROC-AUC / PR-AUC, boosting | **0.81 / 0.42** (baseline 0.77 / 0.37; random PR 0.116) |
| Lift: top decile / top 20% | **4.0× / 2.83×** |
| Back-test: eligible / base rate | 14,855 / 13.64% |
| Back-test: expected / actual / random conversions | ~1,298 / **1,312** / 546 |
| Profit: model vs random | **$180.8k vs $65.8k** |

The full scene-by-scene script is in [UC1_RECORDING_SCRIPT.md](../UC1_RECORDING_SCRIPT.md).

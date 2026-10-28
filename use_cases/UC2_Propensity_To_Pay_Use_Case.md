# UC2 – Build and Explain a Propensity-to-Pay Model

> **Prep document, never open on camera.** Companion files: [UC2_RECORDING_SCRIPT.md](../UC2_RECORDING_SCRIPT.md) (the complete take: clicks, narration, fixes) and [UC2_Planted_Bugs_Answer_Key.md](UC2_Planted_Bugs_Answer_Key.md).

| | |
|---|---|
| Domain | Data Science & ML (DSD) |
| Role | Senior Data Scientist |
| End users | Data Science, Collections |
| Complexity | Advanced |
| Target length | ~38 min (allowed 15:00–45:59, one take) |
| Submitted by | Ullas KC (approved by manager) |

---

## 1. What changed from the approved version, and why

The approved use case (predict which customers will make the next payment; build, validate, explain, package) is **unchanged**. Adjustments:

| # | Approved version | Recorded version | Why |
|---|---|---|---|
| 1 | VS Code **or Internal AutoML Tool** | VS Code (Jupyter) only | Reviewers can't check a proprietary tool |
| 2 | Terminal, GitHub Desktop, "commit with README" | No Git on camera; README and model package generated into `4_Output` | Your decision |
| 3 | Code written during the video | The **expert's own pipeline** (config + 4 notebooks, prepared for this request) is a **pre-existing asset**, walked through, run end to end for the first time, debugged (5 issues) and interpreted on camera | Matches the internal benchmark and Mercor's "diagnosing issues in a data pipeline" pattern |
| 4 | Apps: VS Code, Terminal, GitHub Desktop, PowerPoint | **VS Code (notes) → Firefox (brief) → Calc (pivot EDA) → VS Code → Calc (el (validation) → PowerPoint** | Multiple connected apps |
| 5 | "Split appropriately into train and test" | **Out-of-time** (train Jan–Apr, calibrate May, test June), **day-7 scoring point**, **calibration**, business-rule baseline, capacity-constrained work list | Different from UC1 (avoids duplicate-task rejection) and passes the intern test |
| 6 | Output: notebook; repo; 3-slide summary | Pivot workbook; corrected pipeline + model package; validated June work list; summary deck | Labelled `input N` / `artifact N` / `final output N` |

**How UC2 differs from UC1 on camera:** different bug types (a silent date misparse caught by a range check, a divide-by-zero, an off-by-one time window, a leak found through permutation importance, an inverted business formula), temporal drift and calibration, and capacity-weighted prioritisation instead of campaign ROI.

---

## 2. Mercor Studio idea submission (copy into the fields)

**Goal**
Give the collections team a June agent work list that puts 25 agents where the unpaid money is. Explore the January–June 2026 collections extract, walk through and run the propensity-to-pay pipeline built for this request, fix what its first full run exposes, validate out of time on June, calibrate the probabilities, and show that the list covers more unpaid amount than today's "most overdue first" rule.

**Starting material**
- `input 1 - collections accounts.csv`: 20,240 rows / 20,000 accounts entering collections Jan–Jun 2026, 29 attributes, label `paid_within_30d` (43%, falling from 50% to 37%)
- `input 2 - data dictionary.xlsx`; `input 3 - collections strategy brief.pdf` (capacity, day-7 rule, out-of-time and calibration requirements, exclusions, acceptance criteria); `input 4 - summary deck template.pptx`
- **Pre-existing code:** `2_Code/` holds the pipeline built for this request (`pipeline_config.py` + notebooks 01 preprocessing, 02 training, 03 testing, 04 work list & packaging), not yet run end to end on the full extract

**Apps**
Firefox (PDF brief), LibreOffice Calc (pivot tables, formulas), Visual Studio Code (Markdown preview, Jupyter, Python: pandas, scikit-learn, SHAP), LibreOffice Impress, Finder

**Deliverable**
Exploratory pivot workbook; corrected pipeline with outputs; cleaned data and quality log; time split; trained models and calibrator; June comparison and charts; validated June agent work list; packaged model (model, calibrator, metrics, README); completed summary deck.

**How the result is checked**
June (out-of-time) ROC-AUC ≥ 0.78; beats the logistic baseline on PR-AUC; calibration gap reduced; no field captured after day 7; work list equals agent capacity, excludes dispute/hardship accounts and covers more of June's unpaid amount than highest-days-past-due-first.

**Pitch: problem statement**
Cure rates fall every month and the collections target is being missed. Agents call the most overdue accounts first, spending time on customers who would pay anyway and missing high-value accounts that need help.

**Pitch: solution**
A senior data scientist profiles the extract with LibreOffice Calc pivot tables, then walks through and runs their pipeline and fixes five issues: day-first dates silently parsed into the wrong months, zero incomes breaking the affordability ratio, a training window overlapping the calibration month, a contact count that leaks the outcome (exposed by permutation importance), and a ranking that prioritised customers likely to pay. Validated on June, the model reaches ROC-AUC 0.825; calibration corrects a 9-point over-prediction; and the agent list covers 81% of June's unpaid amount vs 47% for the current rule, with the same capacity.

---

## 3. Detailed task scenario

**Pre-existing assets**: `~/Mercor_UC2/UC2_Propensity_To_Pay_vN/Deliverables/` (staged next to the project folder) with `1_Input` (inputs 1–4), `2_Code` (pipeline), and empty `3_Intermediate` and `4_Output`; Python 3.12 venv with the `Python 3.12 (ds-venv)` kernel.

**Business context and constraints**: ~3,500 accounts per month; 25 agents ≈ 37% capacity; re-prioritised on day 7 (7-day contact fields legal, later ones not); out-of-time validation; probabilities feed expected loss, so calibration is required; dispute/hardship accounts go to a specialist team.

**Multi-phase workflow**
1. Brief (PDF in Firefox) and dictionary (LibreOffice Calc): day-7 rule, capacity, three "refreshed at extract" suspects, business rules.
2. LibreOffice Calc pivot tables: product label drift and BNPL, employment placeholders, status-at-extract leak, prior-delinquency gradient → **artifact 1**.
3. Review the pipeline config in VS Code.
4. 01 preprocessing → fix **P1** (dates) and **P2** (zero income) → artifacts 2–3.
5. 02 training → fix **T1** (window overlap) and **T2** (contact-count leak) → artifacts 4–5.
6. 03 testing on June → fix **E1** (inverted expected-unpaid formula) → calibration, coverage, SHAP → artifacts 6–7.
7. 04 work list and packaging → artifact 8, **final output 3**.
8. LibreOffice Calc validation → **final output 1**. 9. Deck → **final output 2**.

**Why an intern could not do this:** they'd let pandas guess dates, divide by zero incomes, random-split drifting data, keep a post-decision feature, trust uncalibrated probabilities that overstate collections by a quarter, and rank by the wrong side of the probability.

---

## 4. App topology (for Metadata.rtf)

`Visual Studio Code (Lookup) -> Finder (Lookup) -> Firefox (Lookup) -> LibreOffice Calc (Lookup) -> LibreOffice Calc (Create) -> Visual Studio Code (Modify) -> LibreOffice Calc (Create) -> LibreOffice Impress (Modify) -> Finder (Lookup)`

---

## 5. Deliverables map (as packaged in `Deliverables.zip` by `prep/package_deliverables`)

| File | Made by |
|---|---|
| `1_Input/input 1–4` | pre-loaded |
| `1_Input/input 5 - pipeline code before the run/` | added by the packager (original code) |
| `3_Intermediate/artifact 1 - exploratory pivot analysis.xlsx` | LibreOffice Calc |
| `artifact 2 - cleaned accounts.csv` · `artifact 3 - data quality log.csv` | notebook 01 |
| `artifact 4 - time split.csv` · `artifact 5 - trained models/` (+ calibrator) | notebooks 02–03 |
| `artifact 6 - model comparison.csv` · `artifact 7 - charts/` (missing values, accounts by month, pay rate by burden, data-quality fixes, pay rate by month, permutation importance, calibration, prioritisation, SHAP summary and dependence, work list vs current rule) | notebooks 02–03 |
| `artifact 8 - june agent work list.csv` | notebook 04 |
| `4_Output/final output 1 - june agent work list.xlsx` | LibreOffice Calc |
| `4_Output/final output 2 - collections summary.pptx` | LibreOffice Impress |
| `4_Output/final output 3 - model package/` (`model.joblib`, `calibrator.joblib`, `metrics.json`, `README.md`) | notebook 04 |
| `4_Output/final output 4 - corrected pipeline code/` | added by the packager (your fixed `2_Code`) |

---

## 6. Planted data issues (in input 1) and handling

| Issue | Size | Handled in |
|---|---|---|
| Exact duplicates | 240 | 01 §2 |
| Day-first dates in `delinquency_date` | 400 | 01 §3 (**P1**) |
| Product label variants | 700 | 01 §4 |
| Employment placeholders (blank / N/A / Unknown) | 1,200 | 01 §4 |
| Days past due −5 / 999 | 80 | 01 §5 (removed) |
| Amount due > balance | 100 | 01 §5 (removed) |
| Utilisation sentinel 9.99 | 42 | 01 §5 |
| Income missing / income = 0 | ~2,000 / 100 | 01 §6 (**P2**) |
| Structural: no utilisation for personal loans | ~30% | left missing |
| Leaks: `account_status_at_extract`, `amount_recovered_30d` | — | config (already excluded) |
| Leak: `total_contact_attempts_30d` (days 1–30) | — | config (**T2**) |
| Drift: pay rate 49.5% → 36.9% Jan→Jun; BNPL worsening fastest | — | out-of-time split + calibration |

## 7. Reference results (tested by `prep/selftest_uc2.py`)

| | Value |
|---|---|
| May ROC-AUC with leak (T2 symptom) | ~0.91 |
| May ROC-AUC baseline / boosting | 0.821 / **0.844** |
| June ROC-AUC / PR-AUC (boosting; baseline) | **0.825 / 0.732** (0.818 / 0.724) |
| Predicted pay rate raw → calibrated vs actual | 45.7% → 40.0% vs 36.9% |
| Coverage of unpaid: bugged ranking / today's rule / model | 45.4% / 47.1% / **81.4%** |
| Capacity · specialist-routed | 1,351 of 3,652 · 388 |

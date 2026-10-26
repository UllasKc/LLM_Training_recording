# UC2 – Build and Explain a Propensity-to-Pay Model

> **Prep document, never open on camera.** It contains the answer key for the planted data issues.

| | |
|---|---|
| Domain | Data Science & ML (DSD) |
| Role | Senior Data Scientist |
| End users | Data Science, Collections |
| Complexity | Advanced |
| Target length | ~35 min (allowed 15:00–45:59, one take) |
| Submitted by | Ullas KC (approved by manager) |

---

## 1. What changed from the approved version, and why

The approved use case (predict which delinquent customers will make the next payment, then build, validate, explain and package the model) is **unchanged**. Adjustments:

| # | Approved version | Recorded version | Why (guideline) |
|---|---|---|---|
| 1 | VS Code **or Internal AutoML Tool** | VS Code (Jupyter) only | Reviewers can't check a proprietary tool; expert judgment must be visible |
| 2 | Terminal, GitHub Desktop, "commit with README" | No Git on camera. Model package + README in Deliverables; reproducibility shown with **Restart Kernel → Run All** | Your decision (no Git in the demo) |
| 3 | Apps: VS Code, Terminal, GitHub Desktop, PowerPoint | **Word → Excel → VS Code → Excel → VS Code → PowerPoint** | 3+ apps in a connected workflow |
| 4 | "CSV: 20,000 customers with payment label" | 20,000 accounts that entered collections **Jan–Jun 2026** + data dictionary + **collections strategy brief** | Business context, constraints and acceptance criteria are mandatory |
| 5 | "Split appropriately into train and test" | **Out-of-time split** (train Jan–Apr, calibrate May, test June), a **day-7 scoring point** that decides which features are legal, **recalibration** for drift, comparison with the **current business rule** | Makes this clearly different from UC1 (reviewers may reject near-duplicate tasks) and passes the intern test |
| 6 | Output: notebook; repo; 3-slide summary | Notebook; **June agent work list (Excel)**; model package + README; 3-slide summary | Deliverable labelling convention |

**How UC2 differs from UC1 on camera:** temporal validation and drift, calibration as a business requirement (expected loss), a business-rule baseline, capacity-constrained prioritisation weighted by amount, and a *timing-based* leakage argument (day 7). UC1 is about random stratified validation, campaign lift and ROI, and compliance filters.

---

## 2. Mercor Studio idea submission (copy into the fields)

**Goal**
Build, validate and explain a propensity-to-pay model for early-stage collections, validated out of time and calibrated, then use it to produce an agent work list for the latest cohort that fits agent capacity and beats the current "highest days-past-due first" rule.

**Starting material (all synthetic)**
- `input 1 - collections accounts.csv`: 20,240 rows / 20,000 accounts that entered collections Jan–Jun 2026 (duplicates included) with 29 attributes and the label `paid_within_30d` (~37% positive, falling over time)
- `input 2 - data dictionary.xlsx`: column definitions and source systems
- `input 3 - collections strategy brief.docx`: Head of Collections request with capacity, scoring point, validation and calibration requirements, exclusions, acceptance criteria

**Apps**
Microsoft Word, Microsoft Excel, Visual Studio Code (Jupyter, Python: pandas, scikit-learn, SHAP), Microsoft PowerPoint, Finder

**Deliverable**
Jupyter notebook (EDA → cleaning → leakage audit → out-of-time split → baselines → model → calibration → explanation → work list); June agent work list workbook; model package (model, calibrator, metrics, README); 3-slide summary deck.

**How the result is checked**
Out-of-time (June) ROC-AUC ≥ 0.78. Beats logistic regression on PR-AUC. Within agent capacity it covers more of the actual unpaid amount than the "highest DPD first" rule. Calibration checked with Brier score and a reliability curve and fixed where predictions drift. No field captured after day 7 is used. The work list fits capacity and excludes dispute/hardship accounts. Results reproduce after Restart Kernel → Run All.

**Pitch: problem statement**
Cure rates are falling through 2026 (especially BNPL) and the collections target is being missed. Agents call the most-overdue accounts first, so they spend time on customers who would have paid anyway and miss high-value accounts that need help.

**Pitch: solution**
A senior data scientist fixes date-format and business-rule errors, uses the day-7 decision point to separate legal early-contact features from three post-outcome leaks, validates out of time to expose drift, recalibrates because the probabilities drive an expected-loss ranking, and shows the work list covers far more unpaid balance than the current rule within the same agent capacity.

---

## 3. Detailed task scenario (required depth)

**Pre-existing assets**
`~/Desktop/UC2_Propensity_To_Pay/Deliverables/` holding inputs 1–3. The Python 3.12 venv and Jupyter kernel `Python 3.12 (ds-venv)` already exist.

**Business context and constraints** (from input 3)
- About 3,500 accounts enter collections per month; 25 agents can work ~37% of a cohort in depth; the rest get an SMS/app nudge
- Accounts are re-prioritised on **day 7**, so 7-day contact fields are legal and anything later is not
- Out-of-time validation is required (the model will run on future months)
- Probabilities feed expected unpaid = (1 − p) × amount_due, so calibration matters
- Dispute or hardship accounts go to a specialist team: scored, but excluded from the agent list

**Multi-phase workflow**
1. **Understand the request**: brief in Word; dictionary in Excel; note the "Refreshed at extract" fields and the day-7 rule.
2. **Data quality**: mixed date formats (the DD/MM trap), duplicates, product labels, employment placeholders, income zeros, invalid DPD, amount_due > balance, utilisation sentinel.
3. **Leakage audit**: drop `account_status_at_extract`, `amount_recovered_30d` and `total_contact_attempts_30d`; keep the 7-day fields and say why.
4. **Out-of-time design**: pay rate by month (it falls from 42% to 31%); train Jan–Apr, calibrate May, test June.
5. **Baselines → model**: the business rule (DPD), logistic regression, HistGradientBoosting.
6. **Calibration**: reliability curve on June; mean predicted vs actual; isotonic recalibration fitted on May; Brier before and after.
7. **Explanation**: SHAP drivers turned into treatment-path recommendations.
8. **Work list**: rank the June cohort by (1 − p) × amount_due; exclude dispute/hardship; cut at capacity; compare covered unpaid amount with the DPD rule; validate in Excel.
9. **Package and reproduce**, then **present** 3 slides.

**Why an intern could not do this:** they would random-split (hiding drift), parse DD/MM dates silently wrong, keep the "total contacts" leak, report uncalibrated probabilities that overstate collections by ~25%, and rank by probability alone, ignoring amount and capacity.

---

## 4. App topology (for Metadata.rtf)

`TextEdit (Lookup) -> Finder (Lookup) -> Microsoft Word (Lookup) -> Microsoft Excel (Lookup) -> Visual Studio Code (Create) -> Microsoft Excel (Create) -> Visual Studio Code (Modify) -> Microsoft PowerPoint (Create) -> Finder (Lookup)`

---

## 5. Deliverables map (everything ends up in `Deliverables/`)

| File | Made by |
|---|---|
| `input 1 - collections accounts.csv`, `input 2 - data dictionary.xlsx`, `input 3 - collections strategy brief.docx` | pre-loaded |
| `artifact 1 - cleaned accounts.csv` | notebook |
| `artifact 2 - model comparison.csv` (DPD rule, logistic, HGB raw, HGB calibrated; out-of-time) | notebook |
| `artifact 3 - scored June cohort.csv` | notebook |
| `final output 1 - propensity_to_pay_model.ipynb` | VS Code |
| `final output 2 - June agent work list.xlsx` (work list + "Capacity Check" sheet) | Excel |
| `final output 3 - model package/` (`model.joblib`, `calibrator.joblib`, `metrics.json`, `README.md`) | notebook + VS Code |
| `final output 4 - collections prioritisation summary.pptx` | PowerPoint |

---

## 6. Planted data issues: answer key

| Issue | Where | Approx. size | Expected expert handling |
|---|---|---|---|
| **Mixed date formats** (`DD/MM/YYYY` among ISO) | `delinquency_date` | ~2% (~400) | Parse each format explicitly. A naive parse turns 05/03 into May 3rd and **creates fake months 7–12**, which is the trap to show |
| Exact duplicate rows | all columns | ~240 | Drop |
| Inconsistent product labels (`CC`, `credit_card`, `PL`, `bnpl`, `Buy Now Pay Later`) | `product_type` | ~3.5% | Map to 3 canonical values |
| Placeholders `""`, `Unknown`, `N/A` | `employment_status` | ~6% | Merge into one "Unknown" category |
| Missing income and income = 0 | `monthly_income` | ~10% + ~100 zeros | Treat 0 as missing; add a missing indicator |
| Invalid DPD −5 and 999 | `days_past_due` | ~80 | Outside the 1–90 range in the dictionary → remove and log |
| amount_due > outstanding_balance | `amount_due` | ~100 | Breaks the dictionary rule → remove and log |
| Utilisation sentinel 9.99 | `utilization_ratio` | ~40 | Set to missing |
| Structural missing: no utilisation for personal loans | `utilization_ratio` | ~30% | Not an error; leave NaN (HGB handles it) |
| **LEAK, obvious:** status at extract | `account_status_at_extract` | — | Mirrors the outcome → drop |
| **LEAK, obvious:** amount recovered | `amount_recovered_30d` | — | Post-outcome → drop |
| **LEAK, subtle:** total contacts over the whole episode | `total_contact_attempts_30d` | — | Covers days 8–30, and payers stop being called → after the day-7 point → drop. `contact_attempts_7d` stays |
| **Drift** | target by month | 42% → 31% | Out-of-time split; recalibrate |
| Concept drift | BNPL, high affordability burden | — | Shows in SHAP and per-segment calibration |

## 7. Reference results (for rehearsal only)

| | Value |
|---|---|
| Out-of-time (June) ROC-AUC, HGB | ~0.82 |
| June actual pay rate vs mean raw prediction | 31.0% vs **38.6%** (over-predicts) |
| After isotonic calibration fitted on May | mean prediction ~33.0%; Brier 0.163 → 0.157 |
| Unpaid amount covered by top 37% (June, excl. dispute/hardship) | **DPD rule 47%** · amount_due only 77% · **model (1 − p) × amount_due 81%** |

True drivers: days past due (cure rate drops sharply past 30), on-time payment ratio, prior delinquencies, affordability burden (amount_due / income; a cliff above ~35%), right-party contact and promise to pay in the first 7 days (a promise is worth less with past broken promises), employment (unemployed strongly negative), hardship, dispute, high utilisation on revolving products, BNPL worsening month by month.

---

## 8. Run sheet (~35 min) with narration cues

| Time | App | Do | Say (cue) |
|---|---|---|---|
| 0:00–0:45 | TextEdit | Task notes visible | Request, deliverables, definition of done |
| 0:45–2:30 | Finder → Word | Open `input 3`; hover over capacity, day-7 rule, calibration, exclusions | "Day 7 is the key constraint. It decides which columns I'm allowed to use." |
| 2:30–4:30 | Excel | `input 2`; trace "Refreshed at extract" rows | Name the three leak candidates and why |
| 4:30–5:30 | VS Code | Open Folder; New Jupyter Notebook; kernel picker → `Python 3.12 (ds-venv)` | |
| 5:30–10:30 | VS Code | Load; **dates (show the fake-month trap)**; duplicates; labels; invalid rows; save `artifact 1` | "If I'd let pandas guess, 5 March would become 3 May and I'd have data from months that haven't happened" |
| 10:30–13:00 | VS Code | Drop leaks; pay rate by month chart; train/calibrate/test by month | "A random split would hide this drift" |
| 13:00–17:30 | VS Code | DPD-rule baseline, logistic regression, HGB; out-of-time metrics | |
| 17:30–21:00 | VS Code | Reliability curve; mean predicted vs actual; isotonic on May; Brier before/after; save `artifact 2` | "The raw model would promise the business ~25% more cures than will happen" |
| 21:00–24:00 | VS Code | SHAP; drivers → treatment paths | e.g. "High burden and unemployed → hardship conversation, not a payment demand" |
| 24:00–26:00 | VS Code | Score June; exclude dispute/hardship; rank by expected unpaid; cut at capacity; coverage vs DPD rule; save `artifact 3` | |
| 26:00–28:30 | Excel | Open `artifact 3`; check row count = capacity, no excluded flags, total expected unpaid; save `final output 2` | |
| 28:30–30:00 | VS Code | Model package + README; Restart Kernel → Run All; metrics match | |
| 30:00–34:00 | PowerPoint | 3 slides: problem and approach · out-of-time results and calibration · work list impact vs current rule and drivers | |
| 34:00–35:00 | Finder | Deliverables folder; acceptance criteria one by one | |

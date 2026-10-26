# UC1 – Build and Explain a Cross-Sell / Up-Sell Model

> **Prep document, never open on camera.** It contains the answer key for the planted data issues.

| | |
|---|---|
| Domain | Data Science & ML (DSD) |
| Role | Senior Data Scientist |
| End users | Data Science, Marketing (CRM & Cross-Sell) |
| Complexity | Advanced |
| Target length | ~35 min (allowed 15:00–45:59, one take) |
| Submitted by | Ullas KC (approved by manager) |

---

## 1. What changed from the approved version, and why

The approved use case (predict which existing customers will buy another product, then build, validate, explain and package the model) is **unchanged**. Only the following were adjusted to fit the Mercor/Frost guidelines:

| # | Approved version | Recorded version | Why (guideline) |
|---|---|---|---|
| 1 | VS Code **or Internal AutoML Tool** | VS Code (Jupyter) only | A proprietary tool can't be checked by reviewers, and AutoML hides the expert judgment the reviewers grade |
| 2 | Terminal, GitHub Desktop, "save to Git / commit with README" | No Git on camera. Model packaged with a README in the Deliverables folder; reproducibility shown with **Restart Kernel → Run All** | Your decision (no Git in the demo). Terminal is on the "use an alternative if possible" list |
| 3 | Apps: VS Code, Terminal, GitHub Desktop, PowerPoint | **Word → Excel → VS Code → Excel → VS Code → PowerPoint** | Keeps 3+ apps in a *connected* workflow where each app has a real job (read brief, read dictionary, model, validate list, present) |
| 4 | "Starting material: CSV" | CSV + **data dictionary** + **stakeholder campaign brief** | Frost requires documented *business context, constraints and acceptance criteria* |
| 5 | Generic "train baseline and improve" | Planted **leakage**, **compliance** rules (opt-in, no gender), **budget-constrained targeting** (4,000 contacts), lift and ROI check | The intern litmus test: expert judgment has to be visible, not just `model.fit()` |
| 6 | Output: notebook; repo; 3-slide summary | Output: notebook; **Q3 target list (Excel)**; model package + README; 3-slide summary | Deliverables labelled `input N` / `artifact N` / `final output N` as required |

---

## 2. Mercor Studio idea submission (copy into the fields)

**Goal**
Build, validate and explain a cross-sell propensity model for a retail bank, then use it to select exactly 4,000 customers for the Q3 cross-sell campaign within budget and compliance rules, and present the results to Marketing.

**Starting material (all synthetic)**
- `input 1 - customers.csv`: 20,260 rows / 20,000 customers (CRM-merge duplicates included) with 25 attributes as of a 30-Jun-2026 snapshot and the label `next_product_purchased_90d` (~11.6% positive)
- `input 2 - data dictionary.xlsx`: column definitions and source systems
- `input 3 - campaign brief.docx`: Head of CRM request with budget, unit economics, compliance rules and acceptance criteria

**Apps**
Microsoft Word, Microsoft Excel, Visual Studio Code (Jupyter, Python: pandas, scikit-learn, SHAP), Microsoft PowerPoint, Finder

**Deliverable**
Jupyter notebook (EDA → cleaning → leakage audit → baseline → improved model → evaluation → explanation → scoring); a Q3 target list workbook with ROI summary; a model package (model file, metrics, README); a 3-slide summary deck.

**How the result is checked**
On a stratified 20% hold-out the model never saw: ROC-AUC ≥ 0.78; beats a logistic-regression baseline on PR-AUC; top-20% lift ≥ 2.5×. No post-outcome (leaky) fields and no gender used. Target list has exactly 4,000 rows, all opted-in and with < 2 complaints. Metrics reproduce exactly after Restart Kernel → Run All.

**Pitch: problem statement**
Cross-selling to existing customers is the cheapest way to grow revenue, but random campaigns waste most of the budget: only ~1 in 9 customers convert. Marketing needs to know *who* to contact and *why* they buy.

**Pitch: solution**
A senior data scientist audits a messy CRM extract, catches two leaky fields that would have faked a near-perfect model, builds a leak-free baseline and an improved gradient-boosted model, judges it on imbalance-appropriate metrics (PR-AUC, decile lift) and checks calibration so expected conversions can be trusted. SHAP turns the drivers into messaging guidance, and the model produces a compliant, budget-sized target list with an ROI estimate.

---

## 3. Detailed task scenario (required depth)

**Pre-existing assets** (on the Mac before recording)
`~/Desktop/UC1_Cross_Sell/Deliverables/` holding inputs 1–3. The Python 3.12 venv and Jupyter kernel `Python 3.12 (ds-venv)` already exist. Nothing else.

**Business context and constraints** (from input 3)
- Budget: 4,000 contacts; $4 per contact; $150 average 12-month margin per additional product
- Compliance: only `marketing_opt_in = 1` may be contacted; `gender` may not be a model input
- Customer care: exclude customers with ≥ 2 complaints in the last 12 months from the target list
- The model may only use information available at the snapshot date (it will be re-run before every campaign)

**Multi-phase workflow**
1. **Understand the request**: brief in Word, data dictionary in Excel; form leakage hypotheses from the "Source System / Notes" columns.
2. **Data quality**: duplicates, category labels, sentinels, impossible values, mixed date formats, missingness (structural vs random).
3. **Leakage audit and split**: confirm and drop post-outcome fields, drop the protected attribute, de-duplicate **before** a stratified train/test split.
4. **Baseline → improvement**: a logistic-regression pipeline, then HistGradientBoosting with early stopping and a small, reasoned tuning step.
5. **Evaluation**: ROC-AUC, PR-AUC against the 11.6% base rate, decile lift and gains, calibration curve.
6. **Explanation**: SHAP summary, with the top drivers turned into business statements.
7. **Scoring and target list**: score the full base, apply compliance and care filters, take the top 4,000, export; validate in Excel and add an ROI summary.
8. **Package and reproduce**: save model, metrics and README; Restart Kernel → Run All and confirm identical metrics.
9. **Present**: 3 slides in PowerPoint.

**Acceptance criteria**: see the "How the result is checked" field in section 2.

**Why an intern could not do this:** an intern would train on all columns and report AUC ≈ 1.0 from the leaky fields, judge an imbalanced problem on accuracy, use gender, ignore opt-in, and couldn't turn a model into a budget- and ROI-justified list. Each of these is a decision point narrated on camera.

---

## 4. App topology (for Metadata.rtf)

`TextEdit (Lookup) -> Finder (Lookup) -> Microsoft Word (Lookup) -> Microsoft Excel (Lookup) -> Visual Studio Code (Create) -> Microsoft Excel (Create) -> Visual Studio Code (Modify) -> Microsoft PowerPoint (Create) -> Finder (Lookup)`

---

## 5. Deliverables map (everything ends up in `Deliverables/`)

| File | Made by | When |
|---|---|---|
| `input 1 - customers.csv` | pre-loaded | — |
| `input 2 - data dictionary.xlsx` | pre-loaded | — |
| `input 3 - campaign brief.docx` | pre-loaded | — |
| `artifact 1 - cleaned customers.csv` | notebook | after cleaning |
| `artifact 2 - model comparison.csv` | notebook | after evaluation (baseline vs improved, all metrics) |
| `artifact 3 - scored eligible customers.csv` | notebook | after scoring |
| `final output 1 - cross_sell_model.ipynb` | VS Code | throughout |
| `final output 2 - Q3 target list.xlsx` | Excel | top 4,000 + "ROI Summary" sheet |
| `final output 3 - model package/` | notebook + VS Code | `model.joblib`, `metrics.json`, `README.md` |
| `final output 4 - Q3 cross-sell summary.pptx` | PowerPoint | 3 slides |

After recording (off camera), zip the `Deliverables` folder as `Deliverables.zip`.

---

## 6. Planted data issues: answer key

| Issue | Where | Approx. size | Expected expert handling |
|---|---|---|---|
| Exact duplicate rows (CRM merge) | all columns | 200 rows | Drop exact duplicates |
| Near-duplicates: same `customer_id`, different balance / last channel | `customer_id` | 60 rows | Keep one row per customer (no update timestamp, so keep the first and say why); **de-duplicate before splitting** or the same customer lands in train and test |
| Inconsistent labels (`north`, `NORTH `, `N.`, `CC`, `current acct`…) | `region`, `primary_product` | ~4% / ~3% | Strip, normalise case, map abbreviations |
| Sentinel ages 0 and 999 | `age` | ~60 rows | Set to missing and impute (median) |
| Sentinel balance −99999 | `avg_monthly_balance` | ~60 rows | Set to missing |
| Negative tenure −1 | `tenure_months` | ~40 rows | Recompute from `customer_since` |
| Mixed date formats (`DD/MM/YYYY` alongside ISO) | `customer_since` | ~2% | Parse each format explicitly (`dayfirst` for the slash format) |
| Income missing, **more often for Mass segment** (not at random) | `monthly_income` | ~8% | Add a missing indicator and impute by segment; say it's not random |
| Missing credit score | `credit_score` | ~3% | Impute; HGB handles NaN natively |
| **Structural** missing: no emails sent to opted-out customers | `email_open_rate` | ~24% | Not an error; NaN means "not emailed". Fill 0 with a flag, or leave NaN for HGB |
| Structural missing: never contacted | `days_since_last_contact` | ~16% | Same reasoning as above |
| **LEAK 1, obvious:** filled only for buyers | `cross_sell_product_type` | — | Target rate is 100% when filled → post-outcome → drop |
| **LEAK 2, subtle:** welcome pack sent after a new product opens | `welcome_pack_sent` | — | Dictionary says "Fulfilment system, refreshed daily"; target rate ~94% vs ~2% → drop |
| Protected attribute | `gender` | — | Excluded per policy (may be kept aside for a fairness check) |
| Class imbalance | target | 11.6% positive | Stratified split; PR-AUC and lift, not accuracy |

## 7. Reference results (for rehearsal only; your numbers will differ slightly)

| Model | ROC-AUC | PR-AUC | Top-20% lift |
|---|---|---|---|
| Any model **with** leaky columns | ~1.00 | ~1.00 | 5.0 (a red flag) |
| Logistic regression (clean) | ~0.78 | ~0.35 | ~2.7 |
| HistGradientBoosting (clean) | ~0.81 | ~0.40 | ~2.9 |

True drivers built into the data: number of products (2–3 is best), tenure 1–5 years, recent product opened in the last 6 months (negative), 6–24 months (positive), app logins (only with the app), email open rate above ~20% for opted-in customers, affluent and established customers, complaints (strongly negative), age (inverted U, peak in the late 30s), credit card holders with high balance, mortgage holders with ≤ 2 products.

---

## 8. Run sheet (~35 min) with narration cues

| Time | App | Do | Say (cue, not a script) |
|---|---|---|---|
| 0:00–0:45 | TextEdit | Task notes visible; read them | "Marketing has asked me to … the deliverables are … I'll know I'm done when …" |
| 0:45–2:30 | Finder → Word | Open `input 3`; hover over each constraint | Name each number: "The budget is 4,000 contacts at four dollars each…" |
| 2:30–4:30 | Excel | Open `input 2`; trace the Source System column | "`welcome_pack_sent` comes from the fulfilment system, refreshed daily. A welcome pack goes out *after* a product is opened, so I suspect leakage and will test it." |
| 4:30–5:30 | VS Code | Open Folder → Deliverables; New Jupyter Notebook; pick kernel `Python 3.12 (ds-venv)` from the kernel picker | Name the buttons you click |
| 5:30–10:30 | VS Code | Load; shape; duplicates; labels; sentinels; dates; missingness; save `artifact 1` | Explain *why* for each fix, especially the non-random income missingness |
| 10:30–13:00 | VS Code | Target rate by leak candidates → drop; drop gender; stratified split | "If I kept this column I'd report a near-perfect model that fails on day one" |
| 13:00–17:30 | VS Code | Logistic baseline → HGB with early stopping; one small tuning step | State the metric choice: "With 11.6% positives, accuracy is meaningless; I'll use PR-AUC" |
| 17:30–21:00 | VS Code | ROC/PR, decile lift table, calibration curve; save `artifact 2` | Compare with the acceptance thresholds aloud |
| 21:00–24:00 | VS Code | SHAP summary plot; hover over each top feature | Turn each driver into a marketing action |
| 24:00–26:00 | VS Code | Score all; filter opt-in and complaints; top 4,000; export `artifact 3` | "Expected conversions are the sum of probabilities, which is why calibration mattered" |
| 26:00–28:30 | Excel | Open `artifact 3`; check row count and filters; ROI sheet; save `final output 2` | Expected conversions × $150 − 4,000 × $4; compare with random targeting |
| 28:30–30:00 | VS Code | Save model, metrics.json, README into `final output 3`; Restart Kernel → Run All | "The metrics match exactly, so the result is reproducible" |
| 30:00–34:00 | PowerPoint | 3 slides: problem and approach · results vs baseline and lift · drivers, target list and ROI | Read the key numbers off the slides |
| 34:00–35:00 | Finder | Show the Deliverables folder | Go through each acceptance criterion as met |

**Mouse and keyboard:** use the ▶ cell Run button and menus, not Shift+Enter or shortcuts (copy/paste are fine). Pause about 1 s after each click. Keep windows maximised or side by side, and minimise anything more than 25% covered.

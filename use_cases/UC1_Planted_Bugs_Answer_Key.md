# UC1: Planted Bugs Answer Key

> **Prep document, never on screen.** Keep it on your phone or a printout.

## Story you tell on camera

*"The team built this pipeline for an earlier snapshot. The warehouse has since changed the extract: new date formats, new region codes and new columns. I'm running it on the 30 June snapshot for the first time, so I expect it to need fixes."*

Every bug below fits that story: they are schema-drift and code-review problems a senior data scientist finds in someone else's pipeline. Fix them the way an expert would: **read the error → say what it means → find the cause → make the smallest correct fix → re-run → confirm.**

How to re-run after each fix: notebook toolbar **Restart** → **Run All**. Every notebook runs in seconds. For a fix in `pipeline_config.py`, save the file first (**File → Save**), then Restart and Run All in the notebook.

Proven by `prep/selftest_uc1.py`: every bug fails as described here and every fix clears it.

| # | Where | Symptom you'll see | Root cause | Fix |
|---|---|---|---|---|
| **P1** | `01_data_preprocessing.ipynb`, section 3 "Dates and tenure" | **ValueError**: `time data "30/08/2023" doesn't match format "%Y-%m-%d"` | The new extract has some `customer_since` dates in DD/MM/YYYY | Use the config's `cfg.parse_dates(...)` helper (one line) |
| **P2** | `01_data_preprocessing.ipynb`, section 4 "Category labels" | **AssertionError**: `unexpected regions: [' South', 'Central', 'East', 'East ', 'North', 'North ', 'South', 'West']` | Region cleaning doesn't strip spaces (the product line below it does) | Add `.str.strip()` |
| **T1** | `pipeline_config.py`, `build_baseline()` (surfaces in `02_model_training.ipynb`, section 2) | **ValueError**: `Input X contains NaN. LogisticRegression does not accept missing values…` | The baseline pipeline has no imputer; `age`, `avg_monthly_balance` and `credit_score` legitimately contain NaN | Wrap the scaler with a median `SimpleImputer` |
| **T2** | `pipeline_config.py`, `LEAKY_COLUMNS` (surfaces in `02`, section 2) | No error, but **CV ROC-AUC ≈ 0.98** for both models: too good to be true | `welcome_pack_sent` (a new column) is populated after the purchase and isn't excluded | Add it to `LEAKY_COLUMNS` |
| **E1** | `03_model_testing.ipynb`, section 1 "Hold-out metrics" | No error, but **hold-out ROC-AUC ≈ 0.58** after CV ≈ 0.80, and the acceptance checks show `False` | Metrics are computed on `predict()` (0/1 labels at a 0.5 threshold) instead of probabilities | Use `predict_proba(X_test)[:, 1]` |

---

## P1: mixed date formats

**Buggy line** (section 3, first cell):
```python
df["customer_since"] = pd.to_datetime(df["customer_since"], format="%Y-%m-%d")
```
**Say:** "The parser fails at position 13 on '30/08/2023'. That's day-first, not ISO. The new extract mixes two formats. I won't let pandas guess, because 05/03 is ambiguous. The config already has a `parse_dates` helper that reads both formats explicitly; this notebook isn't using it."
**Fixed** (one line):
```python
df["customer_since"] = cfg.parse_dates(df["customer_since"])
```
**Confirm:** after Restart → Run All, the output shows `customer_since: 19,600 ISO dates + 400 day-first dates`; the run then stops at P2.

## P2: region labels with spaces

**Buggy line** (section 4):
```python
df["region"] = df["region"].str.lower().replace(REGION_FIXES).str.title()
```
**Say:** "The check expected 5 regions and found 8: 'North' and 'North ' with a trailing space, ' South' with a leading one. I saw the same in the Calc pivot. The product line underneath strips whitespace, but the region line doesn't."
**Fixed:**
```python
df["region"] = df["region"].str.strip().str.lower().replace(REGION_FIXES).str.title()
```
**Confirm:** the notebook runs to the end; `Saved 20,000 rows -> artifact 2 - cleaned customers.csv`.

## T1: baseline without an imputer

**Where:** the error appears in notebook 02, section 2. The traceback points into `pipeline_config.py` → `build_baseline`.
**Buggy line:**
```python
        ("num", StandardScaler(), numeric_columns(df)),
```
**Say:** "Logistic regression can't take missing values. Age, balance and credit score still have NaNs, which I deliberately left for the model pipeline. Gradient boosting handles NaN natively, the baseline doesn't. `SimpleImputer` is even imported at the top of the config but never used, so this was simply forgotten. I'll impute with the median inside the pipeline so it's learned on training folds only."
**Fixed:**
```python
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns(df)),
```
**Confirm:** save the config → Restart → Run All. CV now runs… and shows T2.

## T2: leakage from `welcome_pack_sent`

**Buggy line** (`pipeline_config.py`):
```python
LEAKY_COLUMNS = ["cross_sell_product_type"]         # populated only after the purchase
```
**Say:** "Cross-validated AUC is 0.98 for both models. For a marketing propensity model that's not a win, it's a red flag. In the pivot, customers with a welcome pack converted 85% vs under 1% without. A welcome pack is sent *after* someone opens a product. It's a new column in this extract and the exclusion list predates it."
**Optional one-line proof** (type it in a new cell below, then delete it or keep it):
```python
df.groupby("welcome_pack_sent")[cfg.TARGET].mean()
```
**Fixed:**
```python
LEAKY_COLUMNS = ["cross_sell_product_type", "welcome_pack_sent"]   # populated only after the purchase
```
**Confirm:** save → Restart → Run All. CV ROC-AUC is now ~0.77 (baseline) and ~0.80 (boosting); boosting has higher PR-AUC (~0.37 vs ~0.32). "Realistic, and boosting earns its place." The models are saved (artifact 5).

## E1: metrics on labels instead of probabilities

**Buggy line** (notebook 03, section 1):
```python
scores = {name: model.predict(X_test) for name, model in models.items()}
```
**Say:** "Hold-out AUC 0.58, after 0.80 in cross-validation. A drop that large on a random hold-out means the evaluation is wrong, not the model. `predict()` returns 0/1 labels at a 0.5 threshold; ROC-AUC, PR-AUC and Brier all need probabilities. The lift table and calibration below use the same scores, so one fix corrects everything."
**Fixed:**
```python
scores = {name: model.predict_proba(X_test)[:, 1] for name, model in models.items()}
```
**Confirm:** Restart → Run All. Hold-out ROC-AUC **0.81**, PR-AUC **0.42** vs baseline **0.37**, top-20% lift **2.83×**; all three acceptance checks `True`.

---

## Reference numbers after all fixes (for the deck)

| Item | Value |
|---|---|
| Duplicate rows removed | 200 exact + 60 conflicting = **260** |
| Hold-out ROC-AUC (boosting / baseline) | **0.81** / 0.77 |
| Hold-out PR-AUC (boosting / baseline / random) | **0.42** / 0.37 / 0.116 |
| Top-20% lift | **2.83×** |
| Eligible customers / base rate | 14,855 / **13.6%** |
| Back-test: expected / actual conversions | ~1,298 / **1,312** |
| Random conversions | **546** |
| Conversion rate list vs eligible | **32.8%** vs 13.6% (2.4×) |
| Profit model vs random | **$180.8k** vs **$65.8k** |

If you get a number that's far from these, something differs from the tested pipeline. Stop and check before recording.

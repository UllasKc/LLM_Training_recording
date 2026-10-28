# UC2: Planted Bugs Answer Key

> Prep document, never on screen. Everything here is also inside [UC2_RECORDING_SCRIPT.md](../UC2_RECORDING_SCRIPT.md), which is the file to follow during the take. Proven by `prep/selftest_uc2.py`.

**Story on camera:** *"I've built this collections pipeline for the request. Today I walk you through it and run it end to end on the full January–June 2026 extract for the first time."*

After each fix: (save the config if you changed it) → notebook **Restart** → **Run All**.

| # | Where | Symptom | Root cause | Fix |
|---|---|---|---|---|
| **P1** | `01` §3 Delinquency date | `AssertionError: cohort months outside Jan-Jun: [7, 8, 9, 10, 11, 12]` | `format="mixed"` guesses each date month-first: 05/03/2026 silently becomes 3 May, and 09/03/2026 becomes 3 September, an impossible month (only dates with a day above 12 come out right) | One line: `df["delinquency_date"] = cfg.parse_dates(df["delinquency_date"])` (the config helper reads both formats explicitly) |
| **P2** | `01` §6 Income and affordability | `AssertionError: infinite payment_burden for 100 accounts` | 100 incomes recorded as 0 (not provided); dividing by zero | Add `df["monthly_income"] = df["monthly_income"].replace(0, np.nan)` as the first line of the cell |
| **T1** | `02` §2 Out-of-time split | `AssertionError: train and calibration windows overlap` | `train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]` includes May | `train_df = df[df["cohort_month"].isin(cfg.TRAIN_MONTHS)]` |
| **T2** | `pipeline_config.py` `LEAKY_COLUMNS` (seen in `02` §3–4) | May ROC-AUC ≈ 0.91, and permutation importance shows `total_contact_attempts_30d` at 0.177, three times the next feature | It counts contacts over days 1–30; payers stop being called once they pay. Data after the day-7 decision point | Add `"total_contact_attempts_30d"` to `LEAKY_COLUMNS` |
| **E1** | `03` §3 Agent prioritisation | No error, but the model list covers **45.4%** of unpaid vs **47.1%** for today's rule, and the acceptance check is `False` | `expected_unpaid = p_pay × amount_due` ranks accounts *likely to pay* | `(1 - test_df["p_pay"]) * test_df["amount_due"]` (notebook 04 already uses `1 - p`) |

**After all fixes:** June ROC-AUC 0.825 · PR-AUC 0.732 vs 0.724 · predicted pay rate 45.7% raw → 40.0% calibrated vs 36.9% actual · agent list covers **81.4%** of unpaid vs **47.1%**.

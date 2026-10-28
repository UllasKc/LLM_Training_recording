# Task: Collections propensity-to-pay model + June agent work list

**Request (Head of Collections Strategy):** Cure rates are falling every month and agents call the most overdue accounts first. Build a model that predicts payment within 30 days and give the 25 agents a June work list (~37% of the cohort) that targets the largest expected unpaid amounts.

## Starting point
- **1_Input**: collections accounts (20,000 accounts entering collections Jan–Jun 2026) · data dictionary · strategy brief (PDF) · deck template
- **2_Code**: my propensity-to-pay pipeline (config + 4 notebooks), built for this request, first full run today

## Plan
1. Brief + dictionary: day-7 decision point, capacity, leakage suspects
2. LibreOffice Calc pivots on the raw extract: products, employment, leakage, payment history
3. Run the pipeline and fix what breaks: preprocessing → out-of-time training → June testing → work list
4. Validate the work list in Calc
5. Complete the summary deck in Impress

## Done when
- June ROC-AUC ≥ 0.78 · beats the logistic baseline on PR-AUC · calibration checked and corrected
- No field captured after day 7
- List fits capacity, excludes dispute/hardship, covers more unpaid amount than highest-DPD-first

# Task: Collections propensity-to-pay model + June agent work list

## In plain words
- **Which late payers should our agents call?** Every month thousands of customers miss a card or loan payment, but the 25 agents can only work about **37%** of them in depth.
- Many late customers pay on their own anyway, so calling them wastes effort. Today agents call the most overdue first, which often misses where the most money is at risk.
- **My job:** one week after an account falls behind, estimate its chance of paying without a call. *Chance it won't pay × amount owed* = money at risk. Agents call the accounts with the most money at risk first, and dispute or hardship cases go to a specialist team.
- **Proof:** test it on June. Does the list cover more of the money that stayed unpaid than "most overdue first", with the same number of calls?

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

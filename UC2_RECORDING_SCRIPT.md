# UC2 Propensity to Pay: Complete Recording Script

**Open this on your second laptop and follow it from top to bottom.** Everything is here: setup, what to open, what to click, what to say, every code fix, and the numbers you should see. Nothing from this file is ever shown on the recording screen.

| Marker | Meaning |
|---|---|
| ▶ **DO** | What to click or open on the recording laptop |
| 🎙 **SAY** | What to say. Speak naturally; you don't have to be word-perfect |
| ✔ **CHECK** | What you should see. If it's different, see Emergency at the end |
| 🔧 **FIX** | Code to change, exactly as written |

**Apps on camera** (the same for the Windows practice and the Mac): **VS Code · Firefox · LibreOffice Calc · LibreOffice Impress · File Explorer** (Mac: **Finder**). Microsoft Office is not used because the Mac doesn't have it. **Use Dark mode for UC2** (UC1 is Light) so your recordings vary, as Mercor asks.

---

## Numbers cheat sheet

| What | Value |
|---|---|
| Raw rows / accounts / paid | 20,240 rows / 20,000 accounts / 43.4% paid within 30 days |
| Duplicates · invalid DPD · amount due > balance | 240 · 80 · 100 → **19,820** accounts remain (**420** removed) |
| Day-first dates fixed · product labels · employment placeholders | 400 · 700 · 1,200 |
| Zero incomes (P2) | 100 |
| Pay rate Jan → Jun | 49.5% → 47.0% → 44.7% → 43.8% → 40.5% → **36.9%** |
| Train / calibrate / test | Jan–Apr 12,491 (46.0%) · May 3,677 (40.5%) · Jun 3,652 (36.9%) |
| May ROC-AUC with leak (wrong) | ~0.91; `total_contact_attempts_30d` importance 0.177 |
| May ROC-AUC / PR-AUC after fix | baseline 0.821 / 0.752 · boosting **0.844 / 0.784** |
| **June ROC-AUC / PR-AUC** | boosting **0.825 / 0.732** · baseline 0.818 / 0.724 |
| Pay rate predicted raw → calibrated vs actual | **45.7% → 40.0% vs 36.9%** · Brier 0.1727 → 0.1649 |
| Agent capacity · eligible · specialist | **1,351** of 3,652 · 3,264 eligible · **388** dispute/hardship |
| Unpaid amount covered, wrong ranking (bug) | 45.4% vs 47.1% for today's rule |
| **Unpaid amount covered** | **81.4% model vs 47.1% highest-DPD-first** |
| Work list $ | expected unpaid $377,939 · actual unpaid $393,144 of $483,197 eligible |

---

## PART 1: The day before

1. Recording laptop, PowerShell:
   ```powershell
   cd C:\Users\ullas.kc\Cnx\LLM_Training_recording      # your project folder
   git pull
   .\setup_windows.cmd
   .\.venv\Scripts\python.exe prep\selftest_uc2.py
   ```
   ✔ **READY** and **SELF-TEST PASSED**.
2. VS Code: only the Python and Jupyter extensions, Copilot disabled, "disable AI features" ticked.
   **Windows practice only:** install **Firefox** and **LibreOffice** (free) if missing; open Firefox, Calc and Impress once and dismiss first-run pop-ups.
3. **Read every line** in `recording_workspace\UC2_Propensity_To_Pay\Deliverables\2_Code`.
4. **Rehearse PART 4 once, out loud, with a stopwatch.** Then reset: `prep\stage_recording.cmd UC2`

## PART 2: 30 minutes before

- [ ] `prep\stage_recording.cmd UC2` → a fresh, new `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN` folder (v1, v2, v3…; path printed at the end). Always use the **newest** one
- [ ] Quit Outlook, Slack and chat apps · Teams status **Do not disturb** · Windows **Do not disturb ON**
- [ ] Browser closed · Windows Update paused · charger in
- [ ] Settings → Personalization → Colors → **Dark** mode
- [ ] File Explorer at `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN` (newest), maximised
- [ ] **VS Code** → **File → Open Folder…** → `Cnx` → `Mercor_UC2` → **UC2_Propensity_To_Pay_vN** (newest) → trust → click **Task Notes.md** (formatted preview) → maximised, on top
- [ ] Firefox, LibreOffice Calc and Impress closed · headset on · Teams test call

## PART 3: Start the Teams recording

1. Teams → **Calendar → Meet now** → `UC2 practice` → **Start meeting** → camera **off**, mic **on** → **Join now** → close "Invite people"
2. **Share → Screen** (main display) → drag the floating Teams window to the **bottom-right corner**
3. Sharing toolbar → **More (…) → Record and transcribe → Start recording** → click VS Code → wait 3 s → Scene 1

---

## PART 4: The script (~38 minutes)

**Rules:** name what you click before clicking it · hover, click, pause about 1 s · one action at a time · menus and mouse, not shortcuts · trace text with the cursor · never "this" or "here" without naming it.

---

### Scene 1 · Task notes (0:00–1:00), VS Code

▶ **DO** VS Code is in front showing the **Task Notes** preview.

🎙 **SAY** (cursor under each line)
> "Hi, I'm a senior data scientist. Today's request comes from our Head of Collections Strategy.
> Every month about three and a half thousand accounts fall into early collections: credit cards, personal loans and buy-now-pay-later. Our twenty-five agents can work about thirty-seven percent of them in depth, and today they simply call the most overdue accounts first.
> Cure rates have been falling all year and we're missing target. So they want a propensity-to-pay model, and a June work list that puts the agents where the unpaid money really is.
> I've built a propensity-to-pay pipeline for this request: a configuration file and four notebooks. Today I'll walk you through it and run it end to end on the full extract for the first time.
> My plan: read the brief and the dictionary, explore the data in LibreOffice Calc, walk through and run my pipeline, fixing anything the first full run exposes, validate out of time, and build the June list. I'm done when the criteria at the bottom are met."

▶ **DO** Minimise VS Code.

---

### Scene 2 · The brief (1:00–2:30), File Explorer → Firefox

🎙 **SAY** "Inside Deliverables there are four folders: Input, Code, Intermediate and Output."

▶ **DO** **Deliverables → 1_Input →** right-click **input 3 - collections strategy brief.pdf → Open with → Firefox** (Mac: **Open With → Firefox**) → maximise. Scroll down slowly with the mouse wheel as you talk.

🎙 **SAY** (hover over each item)
> "Twenty-five agents can work about thirteen hundred accounts a month, roughly thirty-seven percent of intake. The rest get an SMS or app nudge.
> The most important constraint: accounts are re-prioritised on **day seven** after entering collections. Anything captured in the first seven days, like contact attempts or a promise to pay, can be used. Anything captured later can't. That's my leakage rule.
> The model will run on future months, so it must be validated on later months than it was trained on: train January to April, validate on May and June.
> The probabilities feed an expected-loss calculation, so they must be calibrated, not just well ranked.
> Accounts with an open dispute or a hardship flag always go to a specialist team, so they're excluded from the agent list.
> Acceptance: out-of-time ROC-AUC of at least 0.78; beat the current rule, highest-days-past-due first, on unpaid amount covered within capacity; beat a logistic baseline on PR-AUC; calibration checked and corrected."

▶ **DO** Close Firefox (Mac: **Firefox → Quit Firefox**).

---

### Scene 3 · Data dictionary (2:30–4:00), LibreOffice Calc

▶ **DO** Double-click **input 2 - data dictionary.xlsx**. It opens in **LibreOffice Calc**; if another app opens it, right-click → **Open with → LibreOffice Calc**. Maximise.

🎙 **SAY** (trace the **Notes** column, then stop on each row named)
> "The key column is Notes. Three fields say 'Refreshed at extract': `account_status_at_extract`, `amount_recovered_30d`, and `total_contact_attempts_30d`. Extract means the fifteenth of August, long after day seven, so all three are leakage suspects.
> The status and recovered amount are obvious: they *are* the outcome. Total contact attempts is subtler: it's described as 'for this episode', so it covers the whole thirty days, not just the first seven.
> By contrast, `contact_attempts_7d`, `right_party_contact_7d` and `promise_to_pay_7d` are explicitly first-seven-days, so they're legal.
> And the dictionary gives business rules I'll enforce: days past due must be between 1 and 90, and the amount due must not exceed the outstanding balance."

▶ **DO** **File → Close** → **Don't Save**.

---

### Scene 4 · Exploring the raw data with pivot tables (4:00–10:30), LibreOffice Calc → artifact 1

▶ **DO** Right-click **input 1 - collections accounts.csv** → **Open with → LibreOffice Calc** → Text Import: **Unicode (UTF-8)**, separated by **Comma** only → **OK** → maximise. Click the **column A header**, then right-click the number in the status bar (bottom right) and tick **CountA**.

✔ **CHECK** status bar **CountA: 20241**

🎙 **SAY** "Twenty thousand two hundred and forty rows plus the header, but the brief says twenty thousand accounts, so there are duplicates. Let me profile the data with pivot tables."

**How to build each pivot in Calc:** click **A1** on the data sheet → **Insert → Pivot Table… → Current selection → OK** → in the layout dialog drag fields into **Row Fields** and **Data Fields** → double-click a data field to choose **Count** or **Average** → **OK**. Format averages via right-click → **Format Cells… → Numbers → Percent**, 1 decimal. Rename a sheet via right-click on its tab → **Rename Sheet…**.

**Pivot 1: products**

▶ **DO** **product_type** → Row Fields · **account_id** → Data Fields (**Count**) · **paid_within_30d** → Data Fields (**Average**, Percent). Rename the sheet `Products`.

✔ **CHECK** Items like **BNPL**, **Buy Now Pay Later**, **CC**, **credit_card**, **Credit Card**, **Personal Loan**, **Personal-Loan**, **PL** (and possibly case variants such as **CREDIT CARD**). BNPL about 34% paid; cards and loans about 46%.

🎙 **SAY**
> "Three products, but many spellings: 'CC', 'credit underscore card', 'PL', 'Buy Now Pay Later'. The pipeline must map all of these to three products.
> And buy-now-pay-later customers pay noticeably less often: about thirty-four percent against forty-six for cards and loans."

**Pivot 2: employment**

▶ **DO** **employment_status** → Row Fields · **account_id** → Count · **paid_within_30d** → Average (Percent). Rename `Employment`.

✔ **CHECK** `(empty)`, `N/A` and `Unknown` rows · Unemployed ≈ 19.6% · Salaried ≈ 48.3% · Student ≈ 31.2%

🎙 **SAY**
> "Three different placeholders mean the same thing: empty, N/A and Unknown, about twelve hundred accounts in total. They should be one category.
> And employment matters a lot: unemployed customers pay under twenty percent of the time, salaried customers about forty-eight."

**Pivot 3: leakage check**

▶ **DO** **account_status_at_extract** → Row Fields · **paid_within_30d** → Average (Percent) · **account_id** → Count. Rename `Leakage check`.

✔ **CHECK** Current 100% · Settled 100% · Delinquent / Charged-Off / Payment Plan 0%

🎙 **SAY**
> "Exactly a hundred percent or zero percent. This isn't a predictor, it's the outcome recorded later. It must never reach the model."

**Pivot 4: payment history**

▶ **DO** **num_prior_delinquencies_12m** → Row Fields · **paid_within_30d** → Average (Percent) · **account_id** → Count. Rename `Payment history`.

✔ **CHECK** 0 → 53.5% · 1 → 41.9% · 2 → 30.6% · 3 → 20.7%

🎙 **SAY**
> "A clean gradient: no previous delinquencies, fifty-three percent pay; three or more, about twenty percent. Payment history will be a strong driver."

*(Optional: **promise_to_pay_7d** → 67.3% vs 38.1%. "A promise in the first week is legitimate information at day seven, and a strong one.")*

▶ **DO** **File → Save As…** → `Deliverables\3_Intermediate` → **File type: Excel 2007-365 (.xlsx)** → `artifact 1 - exploratory pivot analysis` → **Save** → **Use Excel 2007-365!** → **File → Close**.

🎙 **SAY** "Saved as artifact one in Intermediate."

---

### Scene 5 · My pipeline (10:30–12:00), VS Code

▶ **DO** Click **VS Code** in the taskbar (Mac: Dock) → maximise. Expand **Deliverables** and its four folders. Open **2_Code → pipeline_config.py** and scroll slowly.

🎙 **SAY**
> "Back in VS Code. This is the pipeline I've built: one configuration file and four notebooks: preprocessing, training, testing, and the work list with packaging.
> The business rules from the brief are here: scoring on day seven, thirty-seven percent agent capacity, and the time windows: train on months one to four, calibrate on month five, test on month six.
> In the leaky-column list I've put the account status and the recovered amount. I noted a third suspect in the dictionary, so I'll watch for it.
> Dispute and hardship are kept as model inputs, but those accounts are routed to the specialist team. There's also a small date-parsing helper.
> This is its first run on the complete extract, so let's run it and check every result."

---

### Scene 6 · Notebook 01, preprocessing (12:00–17:00): fix P1 and P2

▶ **DO** Open **01_data_preprocessing.ipynb** → confirm the kernel **Python 3.12 (ds-venv)** at the top right → **Run All**.

✔ **CHECK** It stops in **section 3** with month counts that include 7–12, then:
`AssertionError: cohort months outside Jan-Jun: [7, 8, 9, 10, 11, 12]`

🎙 **SAY**
> "The extract only covers January to June, but the parsed dates include July to December. I used format 'mixed' here, which guesses each date. A day-first date like nine, slash, three becomes the third of September. Worse, five, slash, three silently becomes the third of May. That's inside the range, so nothing would ever flag it, and the account lands in the wrong month of my out-of-time split. I wrote a `parse_dates` helper in the config that reads ISO and day-first dates explicitly, so I'll use it instead of guessing."

▶ **DO** Click the **pipeline_config.py** tab → hover over the `parse_dates` function → back to the notebook.

🔧 **FIX P1** In section 3, change the **right-hand side** of this one line:
```python
df["delinquency_date"] = pd.to_datetime(df["delinquency_date"], format="mixed")
```
to:
```python
df["delinquency_date"] = cfg.parse_dates(df["delinquency_date"])
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** Months now 1–6 only. It stops in **section 6**: `AssertionError: infinite payment_burden for 100 accounts`

🎙 **SAY**
> "Dates fixed: the helper reports nineteen thousand six hundred ISO and four hundred day-first dates, and the chart now shows every account in January to June, with intake rising each month. Next: the payment burden, amount due divided by income, is infinite for a hundred accounts. The profile showed a minimum income of zero. A zero here means 'not provided', not a real income of nothing. So zeros must be treated as missing before dividing."

🔧 **FIX P2** In section 6, add this as the **first line** of the cell:
```python
df["monthly_income"] = df["monthly_income"].replace(0, np.nan)
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** It completes: `Saved 19,820 rows -> artifact 2 - cleaned accounts.csv`

🎙 **SAY** (scroll up, hovering over each output)
> "It runs end to end. The load shows twenty thousand two hundred and forty rows, forty-three percent paid.
> The missing-values chart: utilisation is blank for thirty percent. That's personal loans, which have no credit limit, so it's structural, not an error. Income ten percent, employment four.
> The profile shows days past due of minus five and nine hundred and ninety-nine, and a utilisation of 9.99: impossible values.
> Two hundred and forty exact duplicates removed. Seven hundred product labels mapped to three products. Twelve hundred employment placeholders merged into 'Unknown'.
> Business rules from the dictionary: eighty accounts with days past due outside one to ninety and a hundred with an amount due larger than the balance are removed, and forty-two sentinel utilisations set to missing. That leaves nineteen thousand eight hundred and twenty accounts.
> The payment burden now has a median of about six percent of monthly income. And the affordability chart is striking: up to twenty percent of income, around forty-five percent of accounts pay; above thirty-five percent of income, in orange, almost nobody does. That's a cliff, not a slope, which a tree model handles and a straight line doesn't.
> The last chart sums up every cleaning step and how many rows it touched. Everything is logged in artifact three."

---

### Scene 7 · Notebook 02, training (17:00–22:30): fix T1 and T2

▶ **DO** Open **02_model_training.ipynb**.

🎙 **SAY** "Notebook two sets up the out-of-time design, trains both models, validates on May and checks what drives the model."

▶ **DO** **Run All**.

✔ **CHECK** The pay-rate chart appears (Jan 49.5% → Jun 36.9%), then **section 2** fails: `AssertionError: train and calibration windows overlap`

🎙 **SAY**
> "First the bar chart: the pay rate falls every month, from about fifty percent in January to thirty-seven in June. That's exactly why a random split would be misleading, and why calibration matters.
> Then the split fails: training and calibration overlap. My training filter says 'cohort month less than or equal to the calibration month', so May is in both. It's an off-by-one in my time window. The config already defines the training months, so I'll use them."

🔧 **FIX T1** In section 2, change:
```python
train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]
```
to:
```python
train_df = df[df["cohort_month"].isin(cfg.TRAIN_MONTHS)]
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** train `[1, 2, 3, 4]` 12,491 (46.0%) · calibrate `[5]` 3,677 (40.5%) · test `[6]` 3,652 (36.9%). May ROC-AUC **≈ 0.91**. In section 4 the top feature is **total_contact_attempts_30d ≈ 0.177**, three times the next one.

🎙 **SAY**
> "The windows are clean now. But May ROC-AUC is 0.91, which is very high for collections, and the importance chart explains it: the orange bar, `total_contact_attempts_30d`, costs 0.18 of AUC when shuffled, three times anything else. That's the third suspect from the dictionary. It counts contacts over the whole thirty days, and customers who pay stop being called. So low contacts *means* they paid. At day seven we can't know it."

🔧 **FIX T2** Open **pipeline_config.py** and change:
```python
LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d"]   # captured after the day-7 decision point
```
to:
```python
LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d", "total_contact_attempts_30d"]   # captured after the day-7 decision point
```

▶ **DO** **File → Save** → **02_model_training.ipynb** tab → **Restart → Run All**.

✔ **CHECK** 25 features · May: baseline **0.821 / 0.752**, boosting **0.844 / 0.784** · top importance: on_time_payment_ratio_12m, promise_to_pay_7d, days_past_due, payment_burden, right_party_contact_7d

🎙 **SAY**
> "Now realistic. On May, gradient boosting reaches 0.84 against 0.82 for logistic regression, and a better PR-AUC. The importance chart is now spread across sensible drivers: on-time payment history, a promise to pay in the first week, days past due, payment burden, and whether an agent actually reached the customer. Both models are saved as artifact five."

---

### Scene 8 · Notebook 03, testing on June (22:30–27:30): fix E1

▶ **DO** Open **03_model_testing.ipynb** → **Run All**.

✔ **CHECK** It completes, but the prioritisation shows **today's rule 47.1%** vs **model 45.4%**, and the acceptance check "model list covers more unpaid than today's rule" is **False**.

🎙 **SAY**
> "It ran, but the model's agent list covers less unpaid money than today's rule, even though its AUC is good. That's contradictory, so the problem is in how the list is ranked."

▶ **DO** Scroll to section 3 and hover over the `expected_unpaid` line.

🎙 **SAY**
> "Here: expected unpaid is calculated as the probability of paying times the amount due. That ranks the accounts most *likely to pay* at the top: the opposite of what we want. Expected unpaid is one minus the probability of paying, times the amount. Notebook four already uses one minus p; I got it backwards in this evaluation."

🔧 **FIX E1** In section 3, change:
```python
test_df["expected_unpaid"] = test_df["p_pay"] * test_df["amount_due"]
```
to:
```python
test_df["expected_unpaid"] = (1 - test_df["p_pay"]) * test_df["amount_due"]
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** boosting **0.825 / 0.732 / 0.173** · baseline **0.818 / 0.724** · calibration: raw **0.4566**, calibrated **0.3998**, actual **0.3694**; Brier **0.1727 → 0.1649** · `capacity 1,351 of 3,652 June accounts | eligible 3,264` · today's rule **47.1%**, model **81.4%** · all four checks **True**

🎙 **SAY** (hover over each output)
> "June is a month no model has seen. Gradient boosting reaches a ROC-AUC of 0.825, above the 0.78 target, and beats the baseline on PR-AUC.
> Calibration is the big one. The raw model predicts a 45.7 percent pay rate, but only 36.9 percent actually paid. It learned from better months and would over-promise collections by nearly a quarter. Recalibrating on May brings the prediction to forty percent and improves the Brier score. The remaining gap is because June is worse than May again, which is why the README says to re-calibrate monthly. The calibration chart shows the calibrated curve much closer to the diagonal.
> Prioritisation: the agents can work thirteen hundred and fifty-one of the three thousand six hundred and fifty-two June accounts. Today's rule, most overdue first, would cover forty-seven percent of the unpaid money. The model's list covers eighty-one percent: same agents, same capacity.
> The SHAP chart: on-time payment history at the top, then days past due, with cure rates collapsing after thirty days, then whether an agent reached the customer and whether they promised to pay in the first week. A promise is worth much less from someone with broken promises. And payment burden.
> The dependence charts below show the shape of each effect; above the grey line means more likely to pay. Days past due: flat for the first month, then falling steeply after about thirty-five days. Every day counts once an account passes a month. Payment burden: fine up to about a third of income, then a cliff. On-time payment ratio: below about fifty percent, customers rarely pay; above it, the chance rises steadily.
> All four acceptance checks pass. Artifacts six and seven are saved."

---

### Scene 9 · Notebook 04, work list and package (27:30–29:30)

▶ **DO** Open **04_worklist_and_package.ipynb** → **Run All**.

✔ **CHECK** `agent capacity 1,351 | routed to specialist team (dispute / hardship): 388` · `saved 1,351 accounts` · coverage_model **0.814**, coverage_dpd_rule **0.471**

🎙 **SAY**
> "Notebook four builds the actual June list. Every account is scored with the calibrated model, and the three hundred and eighty-eight accounts with a dispute or hardship flag go to the specialist team.
> The rest are ranked by expected unpaid amount, one minus the probability, times the amount due, and cut at thirteen hundred and fifty-one: artifact eight.
> Because we know June's outcomes, I can check it: the list covers eighty-one percent of the unpaid money, against forty-seven percent for the old rule.
> The histogram shows *why*: the old rule, in grey, only ever calls accounts beyond twenty days past due. The model, in blue, also calls high-risk accounts in their first three weeks, while there's still time to cure them, and skips overdue accounts that are likely to pay anyway."
> Finally the model and calibrator are packaged with metrics and a README as final output three."

▶ **DO** Scroll through the printed README.

---

### Scene 10 · Validating the work list in LibreOffice Calc (29:30–32:30) → final output 1

▶ **DO** File Explorer → `Deliverables\3_Intermediate` → right-click **artifact 8 - june agent work list.csv** → **Open with → LibreOffice Calc** → Text Import: **Comma** → **OK** → maximise.

🎙 **SAY** "Before handing this to the team leads, I'll validate it independently."

▶ **DO** Columns **M** and **N** are empty: you build a small summary table there. Column **M** is text labels you type yourself (they are *not* data columns); column **N** is formulas on the data columns. Every row in this file is one account on the agent list. Click **M1**, type the label, click **N1**, type the formula, and so on down:

| Row | M | N |
|---|---|---|
| 1 | `Accounts on list` | `=COUNT(A:A)` |
| 2 | `Total amount due` | `=SUM(E:E)` |
| 3 | `Expected unpaid (model)` | `=SUM(G:G)` |
| 4 | `Accounts that actually paid` | `=SUM(K:K)` |
| 5 | `Actual unpaid on list` | `=SUMPRODUCT((1-K2:K1352)*E2:E1352)` |
| 6 | `Total unpaid, eligible June` | `483197` *(from notebook 04)* |
| 7 | `Coverage - model list` | `=N5/N6` |
| 8 | `Coverage - highest DPD first` | `0.471` *(from notebook 04)* |
| 9 | `Max open dispute (must be 0)` | `=MAX(I:I)` |
| 10 | `Max hardship (must be 0)` | `=MAX(J:J)` |

✔ **CHECK** 1351 · 532,227 · 377,939 · 354 · 393,144 · 483,197 · 0.814 · 0.471 · 0 · 0

🎙 **SAY**
> "Thirteen hundred and fifty-one accounts: exactly the capacity. The model expected about three hundred and seventy-eight thousand dollars to stay unpaid, and three hundred and ninety-three thousand actually did, so the calibrated estimate is close. Only three hundred and fifty-four of these accounts paid on their own, so the agents are working the right people.
> That's eighty-one percent of all the eligible unpaid money in June, against forty-seven percent with the old rule.
> And no dispute or hardship account is on the list."

▶ **DO** **File → Save As…** → `Deliverables\4_Output` → **File type: Excel 2007-365 (.xlsx)** → `final output 1 - june agent work list` → **Save** → **Use Excel 2007-365!** → **File → Close**.

---

### Scene 11 · Summary deck (32:30–36:30), LibreOffice Impress → final output 2

▶ **DO** `1_Input` → right-click **input 4 - summary deck template.pptx** → **Open with → LibreOffice Impress** → **File → Save As…** → `4_Output` → **File type: PowerPoint 2007-365 (.pptx)** → `final output 2 - collections summary` → **Save** → **Use PowerPoint 2007-365!**.

🎙 **SAY** "I'll save my copy to Output first so the template stays clean, then fill in the orange brackets."

▶ **DO** For each orange `[   ]`: double-click into the text → select the **whole** `[   ]`, brackets included → type just the number (units are in the labels) → select it → **Properties** sidebar → **Character → Font Color** arrow → **Automatic** (or **Format → Character… → Font Effects**).

**Slide 2:** `[ ]` accounts removed → **420**
🎙 "Four hundred and twenty accounts removed: duplicates and business-rule violations."

**Slide 3:** ROC-AUC → **0.825** · PR-AUC → **0.732** vs **0.724** · pay rate (%) → **45.7** → **40.0** vs **36.9** · click the **border of the dashed box** → **Delete** → **Insert → Image…** → `3_Intermediate\artifact 7 - charts\07_calibration.png` → **Open** → fit it on the right.
🎙 "Out of time, 0.825 ROC-AUC. And the calibration chart shows why recalibration matters: raw predictions overstate payment."

**Slide 4:** Unpaid covered (%) → **81** vs **47** · Accounts → **1,351** of **3,652** · Specialist → **388**
- The three drivers on the right are already written in the template (from the SHAP results): just hover over each one as you mention it

🎙 **SAY**
> "The model's list covers eighty-one percent of the unpaid money against forty-seven with the old rule, with the same thirteen hundred and fifty-one agent slots. Three hundred and eighty-eight accounts go straight to the specialist team.
> Recommendation: give agents the top thirty-seven percent by expected unpaid amount, nudge the rest digitally, re-calibrate monthly because pay rates keep falling, and track coverage against the old rule every month."

▶ **DO** **File → Save** → **Use PowerPoint 2007-365!** → **File → Close**.

---

### Scene 12 · Wrap-up (36:30–38:00), File Explorer

▶ **DO** Open `Deliverables` and hover over each folder and file.

🎙 **SAY**
> "To wrap up: Input holds the four files I received, plus my pipeline code as it was before this run, delivered as input five. Code is now the corrected pipeline, delivered as final output four. Intermediate holds the pivot analysis, cleaned accounts, quality log, time split, models and calibrator, the model comparison, charts and the June work list. Output holds the validated work list, the summary deck and the packaged model.
> Five issues fixed: a date parser that silently put accounts in the wrong month, zero incomes that broke the affordability ratio, a training window that overlapped the calibration month, a contact count that leaked the outcome, and a ranking that prioritised the customers most likely to pay.
> Every acceptance criterion is met, and the June list is ready for the team leads. Thank you."

▶ **DO** Stay silent for 3 seconds.

---

## PART 5: Stop, package, send

1. Sharing toolbar → **More (…) → Stop recording → Stop sharing → Leave**
2. Teams → Chat → `UC2 practice` → recording → **⋯ → Download** → rename `UC2_practice_v1.mp4`
3. **Validate and zip the deliverables:**
   ```powershell
   cd C:\Users\ullas.kc\Cnx\LLM_Training_recording      # your project folder
   prep\package_deliverables.cmd UC2
   ```
   ✔ ends with **READY TO UPLOAD** and creates `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN\Deliverables.zip` in the newest version folder. It checks every file is labelled input / artifact / final output, all deliverables exist, every fix is in place and no notebook shows an error. It also adds the original code as **input 5** and your corrected code as **final output 4**. If it says **NOT READY**, fix what it lists and run it again.
4. Watch the video at 1.5×: notes visible at the start · 15:00–45:59 · no pop-ups or AI tools · every click named · every fix explained.
5. Send your manager `UC2_practice_v1.mp4` + `Deliverables.zip`. *(For the final Mac take, upload video.mp4, the unmodified recording zip, Deliverables.zip and Metadata.rtf to Mercor Studio.)*
6. Reset: `prep\stage_recording.cmd UC2`

## Emergency

| Situation | What to do |
|---|---|
| A fix still errors | Typo: "Small typo, I'll correct it". Compare with the 🔧 block → Restart → Run All |
| Kernel not listed | Select Kernel → Python Environments… → the `.venv` in `LLM_Training_recording` |
| Notebook 03 says the calibrator is missing | Notebook 02 must have finished first. Run 02, then 03 |
| A notebook stops somewhere not in this script | Stop the take, re-stage, run `prep\selftest_uc2.py` |
| Numbers very different from the cheat sheet | Stop, re-stage, start again |
| LibreOffice shows a yellow read-only bar | Click **Edit Document**; re-stage next time |
| The PDF opens in a different app | Right-click → **Open with → Firefox** |
| Running long | Skip the optional promise-to-pay pivot; shorten the SHAP talk to three drivers |

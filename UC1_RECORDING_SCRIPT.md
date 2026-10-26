# UC1 Cross-Sell: Complete Recording Script

**Open this on your second laptop and follow it from top to bottom.** Everything is here: setup, what to open, what to click, what to say, every code fix, and the numbers you should see. Nothing from this file is ever shown on the recording screen.

**How to read it**

| Marker | Meaning |
|---|---|
| ▶ **DO** | What to click or open on the recording laptop |
| 🎙 **SAY** | What to say. Speak naturally; you don't have to be word-perfect |
| ✔ **CHECK** | What you should see. If it's different, see Emergency at the end |
| 🔧 **FIX** | Code to change, exactly as written |

Windows names are used (Notepad, File Explorer). On the Mac: Notepad → **TextEdit**, File Explorer → **Finder**, `Ctrl` → `Cmd`.

---

## Numbers cheat sheet (you'll need these on camera)

| What | Value |
|---|---|
| Raw rows / customers | 20,260 rows / 20,000 customers / 11.6% bought |
| Duplicates removed | 200 exact + 60 conflicting = **260** |
| Day-first dates fixed | 400 |
| Leak: conversion with / without welcome pack | 85.4% / 0.7% |
| Income missing: Mass vs others | 10.0% vs ~4% |
| CV ROC-AUC with leak (wrong) | ~0.98 |
| CV ROC-AUC after fix: baseline / boosting | 0.773 / **0.798** |
| CV PR-AUC: baseline / boosting | 0.317 / **0.369** |
| Hold-out ROC-AUC with label bug (wrong) | ~0.58 |
| **Hold-out ROC-AUC** boosting / baseline | **0.81** / 0.774 |
| **Hold-out PR-AUC** boosting / baseline / random | **0.421** / 0.367 / 0.116 |
| Lift: top decile / **top 20%** | 4.0× / **2.83×** |
| Eligible customers / eligible conversion rate | 14,855 / 13.64% |
| Back-test expected / **actual** / random conversions | 1,298 / **1,312** / 546 |
| Back-test conversion rate vs eligible | **32.8%** vs 13.6% (2.4×) |
| **Profit** model vs random | **$180,800 vs $65,831** (uplift ≈ $115k) |

---

## PART 1: The day before (setup and rehearsal)

1. On the recording laptop, in PowerShell:
   ```powershell
   cd $env:USERPROFILE\LLM_Training_recording
   git pull
   .\setup_windows.cmd
   .\.venv\Scripts\python.exe prep\selftest_uc1.py
   ```
   ✔ setup ends with **READY**; the self-test ends with **SELF-TEST PASSED**.
2. VS Code: only the **Python** and **Jupyter** extensions. Copilot disabled. Settings → search "disable AI features" → ticked. Restart VS Code.
3. Open Word, Excel and PowerPoint once each, close every pop-up, close them.
4. **Read every line** of the code in `recording_workspace\UC1_Cross_Sell\Deliverables\2_Code` so you can explain any of it.
5. **Rehearse the whole of PART 4 once, out loud, with a stopwatch** (not recorded). Then reset:
   ```powershell
   prep\stage_recording.cmd UC1
   ```
   (This restores the original code with the 5 issues and empties the output folders.)

---

## PART 2: 30 minutes before the take

▶ **DO**
- [ ] `prep\stage_recording.cmd UC1` → a fresh `Desktop\UC1_Cross_Sell`
- [ ] **Quit** Outlook, Slack, WhatsApp and other chat apps (tray icon → right-click → Quit). Teams stays open.
- [ ] Teams status → **Do not disturb**. Windows Settings → System → Notifications → **Do not disturb ON**
- [ ] Close the browser. Pause Windows Update. Plug in the charger
- [ ] Settings → Personalization → Colors → **Light** mode
- [ ] Open **File Explorer** at `Desktop\UC1_Cross_Sell` and maximise it
- [ ] Double-click **Task Notes.txt** → opens in **Notepad** → maximise
- [ ] VS Code, Word, Excel and PowerPoint **closed**
- [ ] Headset on. Teams → Settings → Devices → **Make a test call**
- [ ] Phone silent, with this script open on the second laptop

---

## PART 3: Start the Teams recording

▶ **DO**
1. Teams → **Calendar** → **Meet now** → name it `UC1 practice` → **Start meeting**
2. Camera **OFF**, microphone **ON**, headset selected → **Join now** → close the "Invite people" box
3. **Share** (top bar) → **Screen** → your main display (leave "Include sound" off)
4. Drag the small floating Teams window to the **bottom-right corner**
5. Hover over the sharing toolbar at the top → **More (…)** → **Record and transcribe** → **Start recording**
6. Click Notepad so it's in front. **Wait 3 seconds in silence.** Start Scene 1.

---

## PART 4: The script (~38 minutes)

**Rules for every scene:** name what you click *before* clicking it · hover, click, pause about 1 second · one action at a time · use menus and the mouse, not keyboard shortcuts (Ctrl+C / Ctrl+V are fine) · move the cursor under text as you read it · never say "this" or "here" without naming the thing.

---

### Scene 1 · Task notes (0:00–1:00), Notepad

▶ **DO** Notepad is on screen. Move the cursor slowly under each line as you talk.

🎙 **SAY**
> "Hi, I'm a senior data scientist. Today's request comes from our Head of CRM and Cross-Sell.
> Marketing contacts four thousand customers in every cross-sell campaign. Right now those customers are picked at random, and about one in nine buys another product.
> Before they sign off the Q4 budget, they want proof that a model would do better.
> We have a customer snapshot from the thirtieth of June, and we now know who bought an additional product between July and September.
> Our team already has a cross-sell pipeline, but it was built for an earlier snapshot and hasn't been run on this extract yet.
> So my plan is: read the brief and the data dictionary, explore the raw data in Excel, run the pipeline and fix whatever the new extract breaks, and then back-test: which four thousand customers would the model have picked, and how many of them actually bought.
> I'm done when the criteria at the bottom of my notes are met."

▶ **DO** Click the **Minimise** button (the "–" at the top right of Notepad).

---

### Scene 2 · The brief (1:00–2:30), File Explorer → Word

▶ **DO** In File Explorer, hover over the folders.

🎙 **SAY**
> "Everything for this task is in the Deliverables folder. It has four sub-folders: Input, Code, Intermediate and Output. Inputs are read-only, the pipeline writes its working files to Intermediate, and the business deliverables go to Output."

▶ **DO** Double-click **Deliverables** → double-click **1_Input** → double-click **input 3 - campaign brief.docx** → click **Maximise** in Word.

🎙 **SAY** (hover over each line as you say it)
> "This is the brief from the Head of CRM, dated the first of October, so the July-to-September outcomes are complete.
> The budget is four thousand contacts per campaign, at four dollars per contact. Each additional product sold is worth a hundred and fifty dollars of margin.
> Compliance: we can only contact customers who have opted in to marketing, and gender must not be used as a model input.
> Customer care: anyone with two or more complaints in the last twelve months is excluded.
> And the model may only use information available on the snapshot date. That's my rule for spotting leakage.
> They want a back-test scored only by models that didn't train on those customers, the drivers in plain language, and a short summary on the team template.
> Acceptance criteria: ROC-AUC of at least 0.78 on a hold-out set, beat a logistic-regression baseline on PR-AUC, top-twenty-percent lift of at least 2.5, and the back-test list must convert at least twice the eligible average."

▶ **DO** Click the **X** (top right) to close Word.

---

### Scene 3 · Data dictionary (2:30–4:00), Excel

▶ **DO** Double-click **input 2 - data dictionary.xlsx** → **Maximise**.

🎙 **SAY**
> "The data dictionary lists every column with its source system."

▶ **DO** Move the cursor down the **Source System** column, then stop on the `welcome_pack_sent` row.

🎙 **SAY**
> "Most columns come from core banking, the CRM and the data warehouse, all as of the snapshot date.
> But `welcome_pack_sent` comes from the fulfilment system and is refreshed daily. A welcome pack is sent *after* a customer opens a new product, so this column could leak the outcome. I'll test it."

▶ **DO** Hover over `cross_sell_product_type`, then `gender`, then `email_open_rate`.

🎙 **SAY**
> "`cross_sell_product_type` comes from the sales ledger, also refreshed daily: same suspicion.
> `gender` is marked as a protected attribute, and the brief excludes it.
> And `email_open_rate` is only tracked when emails were sent, so I expect it to be blank for customers who opted out."

▶ **DO** Click **X** to close Excel → **Don't Save** if asked.

---

### Scene 4 · Exploring the raw data with pivots (4:00–11:00), Excel → artifact 1

▶ **DO** Double-click **input 1 - customers.csv** → **Maximise**. Click the **column A header** (the letter A).

✔ **CHECK** The status bar (bottom right) shows **Count: 20261**.

🎙 **SAY**
> "This is the raw extract. When I select column A, the status bar shows twenty thousand two hundred and sixty-one cells, which is twenty thousand two hundred and sixty rows plus the header. But the brief says twenty thousand customers. So there are duplicates. I'll handle those in the pipeline. First I want to understand the data with a few pivot tables."

**Pivot 1: products**

▶ **DO** Click cell **A2** → **Insert** tab → **PivotTable** → the range is filled in → **New Worksheet** → **OK**.

🎙 **SAY**
> "I'll click the Insert tab and then PivotTable. Excel has picked up the whole table. I'll put it on a new worksheet."

▶ **DO** In the **PivotTable Fields** pane on the right:
1. Drag **num_products** into **Rows**
2. Drag **customer_id** into **Values** (it shows "Count of customer_id")
3. Drag **next_product_purchased_90d** into **Values** → click its arrow in the Values box → **Value Field Settings…** → **Average** → **Number Format** → **Percentage**, 1 decimal place → **OK** → **OK**

✔ **CHECK** 1 → 7.8% · 2 → 15.7% · 3 → 20.1% · 4 → 9.2%

🎙 **SAY** (hover over each row)
> "Customers with one product convert at 7.8 percent, two products 15.7, three products 20.1, but four products drops back to 9.2. So it isn't linear: customers who already hold everything are saturated. That's a pattern a tree-based model can capture and a straight line can't."

▶ **DO** Right-click the sheet tab at the bottom → **Rename** → type `Products` → click away.

**Pivot 2: data quality**

▶ **DO** Click the **input 1 - customers** sheet tab → click cell **A2** → **Insert → PivotTable → New Worksheet → OK**. Drag **region** into **Rows** and **customer_id** into **Values**.

✔ **CHECK** Besides Central / East / North / South / West, you see extra items such as **N.**, **W.** and duplicates of East / North / South (these have hidden leading or trailing spaces).

🎙 **SAY**
> "There should be five regions. I can see 'N.' and 'W.' as abbreviations, and a second East, North and South. Those have a hidden space before or after the name. Excel ignores upper and lower case here, but code won't, so the pipeline has to normalise these labels."

▶ **DO** Rename the tab `Data quality`.

**Pivot 3: leakage check**

▶ **DO** Data sheet → **A2** → **Insert → PivotTable → New Worksheet → OK**. Drag **welcome_pack_sent** into **Rows**; **customer_id** into **Values**; **next_product_purchased_90d** into **Values** → **Average** → **Percentage**.

✔ **CHECK** 0 → 0.7% · 1 → 85.4%

🎙 **SAY**
> "This confirms what I suspected from the dictionary. Customers with a welcome pack converted at 85 percent; without one, less than one percent. The welcome pack isn't a predictor, it's a *record* of the purchase. If this column reaches the model, the model will look brilliant in testing and fail in production. It must be excluded."

▶ **DO** Rename the tab `Leakage check`.

**Pivot 4: missing income**

▶ **DO** Data sheet → **A2** → **Insert → PivotTable → New Worksheet → OK**. Drag **customer_segment** into **Rows**; **customer_id** into **Values**; **monthly_income** into **Values** → its arrow → **Value Field Settings… → Count** → **OK**.

✔ **CHECK** Mass: 14,802 customers vs 13,326 incomes · Affluent 4,538 vs 4,361 · Premier 920 vs 879

🎙 **SAY**
> "Count ignores blank cells, so comparing the two columns shows the missing incomes. In the Mass segment ten percent of incomes are missing; in Affluent and Premier it's around four percent. So it's not missing at random. Lower-income customers skip the field more often. That means I shouldn't just fill it in; I'll keep a flag that says the income was missing, because that itself carries information."

▶ **DO** Rename the tab `Missing income`.

*(Optional if time allows: one more pivot with **complaints_12m** in Rows and the average purchase rate: 12.8% → 7.2% → 2.4%. "That supports the brief's rule of excluding customers with two or more complaints.")*

**Save as artifact 1**

▶ **DO** **File → Save As → Browse** → go to `Desktop\UC1_Cross_Sell\Deliverables\3_Intermediate` → **Save as type: Excel Workbook (*.xlsx)** → File name: `artifact 1 - exploratory pivot analysis` → **Save** → close Excel with **X**.

🎙 **SAY**
> "I'll save this as an Excel workbook in the Intermediate folder as artifact one, so the pivots are kept as evidence. Saving as CSV would lose them."

---

### Scene 5 · The existing pipeline (11:00–12:30), VS Code

▶ **DO** **Start** menu → **Visual Studio Code** → **Maximise** → **File → Open Folder…** → Desktop → **UC1_Cross_Sell** → **Select Folder** → if asked, **Yes, I trust the authors**.

▶ **DO** In the Explorer panel on the left, click **Deliverables** to expand it, then **1_Input**, **2_Code**, **3_Intermediate** and **4_Output** in turn.

🎙 **SAY**
> "This is the project in VS Code. Input holds the four files I've just looked at. Code holds the team's pipeline. Intermediate already has my pivot workbook, and Output is empty."

▶ **DO** Click **2_Code → pipeline_config.py**. Scroll slowly from top to bottom.

🎙 **SAY**
> "The pipeline has one shared configuration file and four notebooks that run in order: preprocessing, training, testing, and back-test with packaging.
> At the top are the paths, and the four-notebook flow is described in the header.
> Then the business rules from the brief: four thousand contacts, four dollars per contact, a hundred and fifty dollars margin, and a maximum of one complaint.
> Then the columns: the target, the ID columns, gender as a protected column, and a list of leaky columns, which currently only contains `cross_sell_product_type`. I'll keep an eye on that, given what the pivot showed.
> And at the bottom the two models: a logistic-regression baseline and histogram gradient boosting.
> This was written for the earlier snapshot. Let's see how it handles the new one."

---

### Scene 6 · Notebook 01, preprocessing (12:30–17:30): fix P1 and P2

▶ **DO** Click **01_data_preprocessing.ipynb**. Check the top-right corner shows **Python 3.12 (ds-venv)**. If it doesn't: click **Select Kernel → Jupyter Kernel… → Python 3.12 (ds-venv)**.

🎙 **SAY** (scroll through the section headings)
> "Notebook one cleans the raw snapshot: load and profile, duplicates, dates, category labels, impossible values, missing values, and save. I'll run the whole notebook with Run All at the top."

▶ **DO** Click **Run All** (toolbar at the top of the notebook).

✔ **CHECK** The run stops in section **3. Dates and tenure** with a red error:
`ValueError: time data "30/08/2023" doesn't match format "%Y-%m-%d", at position 13`

🎙 **SAY**
> "It stopped in the dates section. The error says the value thirty, slash, zero eight, slash, twenty twenty-three doesn't match the year-month-day format. That's a day-first date, so the new extract mixes two date formats. I won't let pandas guess, because a date like five, slash, three is ambiguous. The shared config already has a `parse_dates` helper that reads both formats explicitly and fails if anything is left over. This notebook just isn't using it."

▶ **DO** Click the **pipeline_config.py** tab (or open it from the Explorer panel) → hover over the `parse_dates` function → go back to the notebook.

🔧 **FIX P1** In section 3, change the **right-hand side** of this one line:
```python
df["customer_since"] = pd.to_datetime(df["customer_since"], format="%Y-%m-%d")
```
to:
```python
df["customer_since"] = cfg.parse_dates(df["customer_since"])
```
*(Select from `pd.to_datetime` to the end of the line with the mouse, then type the replacement.)*

▶ **DO** Click **Restart** in the notebook toolbar → confirm **Restart** if asked → click **Run All**.

🎙 **SAY**
> "I'll restart the kernel and run everything from the top, so nothing is left over from the failed run."

✔ **CHECK** It now stops in section **4. Category labels**:
`AssertionError: unexpected regions: [' South', 'Central', 'East', 'East ', 'North', 'North ', 'South', 'West']`

🎙 **SAY**
> "The dates are fixed: the helper reports nineteen thousand six hundred ISO dates and four hundred day-first dates. Now the label check fails: it expected five regions and found eight. There's 'North' and 'North' with a space at the end, and 'South' with a space at the front. That's exactly what I saw in the pivot. Looking at the code, the product line strips spaces, but the region line doesn't."

🔧 **FIX P2** In section 4, change this line:
```python
df["region"] = df["region"].str.lower().replace(REGION_FIXES).str.title()
```
to:
```python
df["region"] = df["region"].str.strip().str.lower().replace(REGION_FIXES).str.title()
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** It runs to the end: `Saved 20,000 rows -> artifact 2 - cleaned customers.csv`

🎙 **SAY** (scroll back up and hover over each output as you speak)
> "Now it runs end to end. Let me walk through what it did.
> The load shows twenty thousand two hundred and sixty rows but only twenty thousand unique customers, with 11.6 percent buying.
> The missing-values chart: `cross_sell_product_type` is blank for eighty-eight percent. It's only filled for buyers, which is why it's already on the leaky list. Email open rate is missing for twenty-four percent, days since last contact for sixteen, income for eight.
> The summary statistics show ages of zero and nine hundred and ninety-nine, a balance of minus ninety-nine thousand nine hundred and ninety-nine, and a tenure of minus one. Those are system defaults, not real values.
> Duplicates: two hundred exact copies from the CRM merge, plus sixty customers with two different rows. There's no update timestamp, so the pipeline keeps the first record. Importantly, this happens *before* any train-test split, otherwise the same customer could end up in both.
> Four hundred day-first dates, forty negative tenures recalculated from the start date, eight hundred region and six hundred product labels normalised.
> Sixty impossible ages and sixty sentinel balances set to missing.
> The income chart: missing for ten percent of the Mass segment, highlighted in orange, against about four percent elsewhere. That's the same pattern as the pivot, so it's not random. The pipeline adds an income-missing flag and fills the value with the segment median.
> And this cross-table confirms the email open rate is blank for exactly the four thousand eight hundred and eight customers who opted out, and for nobody else. Blank means *not emailed*, so zero is the right value.
> The remaining missing values, in age, balance and credit score, are left for the model pipelines to handle.
> And the last chart summarises every cleaning step and how many rows it touched: duplicates, labels, sentinels and missing values, all in one view."

▶ **DO** In the Explorer panel, click **3_Intermediate → artifact 3 - data quality log.csv**.

🎙 **SAY**
> "Every cleaning decision is also written to a data-quality log, artifact three, so it can be audited."

---

### Scene 7 · Notebook 02, training (17:30–22:30): fix T1 and T2

▶ **DO** Click **2_Code → 02_model_training.ipynb**.

🎙 **SAY**
> "Notebook two splits the data, compares the two models with five-fold cross-validation on the training set only, then fits and saves them. The test set stays untouched until notebook three."

▶ **DO** **Run All**.

✔ **CHECK** It stops in section **2** with `ValueError: Input X contains NaN. LogisticRegression does not accept missing values encoded as NaN natively.` The traceback mentions `pipeline_config.py`.

🎙 **SAY**
> "The logistic-regression baseline fails: it doesn't accept missing values, and age, balance and credit score still have some, on purpose. Gradient boosting handles missing values natively, but the baseline needs an imputer. The traceback points to the baseline builder in the config file."

▶ **DO** Click **pipeline_config.py** (tab or Explorer panel) → scroll to `build_baseline`.

🎙 **SAY**
> "Here's the baseline: a standard scaler on the numeric columns, but no imputer. And at the top of the file `SimpleImputer` is imported but never used, so it was simply forgotten. I'll put a median imputer in front of the scaler inside the pipeline, so it's learned only from the training folds."

🔧 **FIX T1** In `build_baseline`, change:
```python
        ("num", StandardScaler(), numeric_columns(df)),
```
to:
```python
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns(df)),
```

▶ **DO** **File → Save**. Click the **02_model_training.ipynb** tab → **Restart → Run All**.

✔ **CHECK** It runs, but the cross-validation table shows ROC-AUC **≈ 0.98** for both models.

🎙 **SAY**
> "It runs now, but look at the result: a cross-validated ROC-AUC of 0.98 for both models. For a marketing propensity model that isn't good news, it's a red flag. Nobody predicts human buying behaviour that well. This is the welcome pack I saw in the pivot. Let me prove it."

▶ **DO** Hover over the cross-validation output → click **+ Code** below it → type:
```python
df.groupby("welcome_pack_sent")[cfg.TARGET].mean()
```
→ click the cell's **▶ Run** button.

✔ **CHECK** `0  0.007` · `1  0.855`

🎙 **SAY**
> "Eighty-five percent with a welcome pack, under one percent without: the same as the pivot. It's a new column in this extract, and the leaky-column list in the config was written before it existed."

🔧 **FIX T2** In `pipeline_config.py`, change:
```python
LEAKY_COLUMNS = ["cross_sell_product_type"]         # populated only after the purchase
```
to:
```python
LEAKY_COLUMNS = ["cross_sell_product_type", "welcome_pack_sent"]   # populated only after the purchase
```

▶ **DO** **File → Save** → **02_model_training.ipynb** tab → **Restart → Run All**.

✔ **CHECK** baseline_logreg **0.773 / 0.317** · gradient_boosting **0.798 / 0.369** · `boosting iterations after early stopping: 164`

🎙 **SAY** (hover over each output)
> "Now the numbers are realistic. The 'Excluded' line shows both leaky columns and gender are out.
> The split is stratified: sixteen thousand training and four thousand test customers, both at 11.6 percent positive.
> In cross-validation the baseline reaches a ROC-AUC of 0.77, and gradient boosting 0.80. With only 11.6 percent positives, PR-AUC is the more honest metric, because a random model would score 0.116. That's the dashed line on the chart. Boosting gets 0.37 against 0.32 for the baseline, so it earns its place.
> Early stopping chose a hundred and sixty-four boosting rounds, and both models are saved as artifact five."

---

### Scene 8 · Notebook 03, testing (22:30–27:00): fix E1

▶ **DO** Click **03_model_testing.ipynb**.

🎙 **SAY**
> "Notebook three evaluates both saved models on the untouched hold-out set, then looks at lift, calibration and the drivers, and checks the acceptance criteria."

▶ **DO** **Run All**.

✔ **CHECK** It completes, but the hold-out table shows ROC-AUC **≈ 0.58**, and the acceptance table at the bottom shows **False** values.

🎙 **SAY**
> "It ran, but the hold-out ROC-AUC is 0.58, after 0.80 in cross-validation. A drop that big on a random hold-out set means the *evaluation* is wrong, not the model."

▶ **DO** Scroll up to section 1 and hover over `model.predict(X_test)`.

🎙 **SAY**
> "Here it is: the scores come from `predict`, which returns zero-or-one labels at a fifty-percent threshold. ROC-AUC, PR-AUC and the Brier score all need probabilities. And because the lift table and calibration chart reuse these same scores, one fix corrects everything below it."

🔧 **FIX E1** In section 1, change:
```python
scores = {name: model.predict(X_test) for name, model in models.items()}
```
to:
```python
scores = {name: model.predict_proba(X_test)[:, 1] for name, model in models.items()}
```

▶ **DO** **Restart → Run All**.

✔ **CHECK** gradient_boosting **0.810 / 0.421 / 0.084** · baseline **0.774 / 0.367** · random PR-AUC **0.116** · `Top-20% lift: 2.83x` · acceptance table **True / True / True**

🎙 **SAY** (hover over each output as it comes)
> "Hold-out results: gradient boosting reaches a ROC-AUC of 0.81, above the 0.78 target, and a PR-AUC of 0.42 against 0.37 for the baseline and 0.116 for random.
> The lift table: the top ten percent of customers by score buy at four times the average rate, and the bottom deciles almost never buy. The top twenty percent give a lift of 2.83, above the 2.5 target. The bar chart shows the same thing.
> The calibration curve sits close to the diagonal, and the mean prediction is 11.6 percent, the same as the actual rate. So when the model says thirty percent, about thirty percent really buy. That matters, because Marketing will budget on expected conversions."

▶ **DO** Hover over each row of the SHAP chart as you name it.

🎙 **SAY**
> "The SHAP chart shows what drives the predictions.
> Email open rate is at the top: customers who engage with our emails are the most receptive, so email is the right channel for them.
> Age: propensity peaks in the late thirties.
> Tenure: customers between one and five years are the sweet spot. Very new customers aren't ready yet.
> App logins: digitally active customers buy more.
> Number of products: two or three is best, as the pivot showed.
> Months since the last product was opened: someone who just bought is less likely to buy again straight away.
> And complaints strongly reduce propensity, which supports the customer-care exclusion."

▶ **DO** Scroll to the three **SHAP dependence** charts below and hover over each panel.

🎙 **SAY**
> "The dependence charts show the *shape* of each effect: above the grey line means more likely to buy.
> Tenure: a sharp jump after the first year, positive up to about five years, then negative. That's the sweet spot.
> Number of products: one product is negative, two and three are clearly positive, and four drops back, exactly the saturation I saw in the pivot.
> Email open rate: flat until about twenty-five percent, then rising steeply. So the message to Marketing is that engaged email readers are worth targeting, not just anyone on the list.
> Finally, all three acceptance checks are True. The comparison table and all charts are saved as artifacts six and seven."

---

### Scene 9 · Notebook 04, back-test and package (27:00–29:30)

▶ **DO** Click **04_backtest_and_package.ipynb** → **Run All**.

✔ **CHECK** `eligible: 14,855 of 20,000 customers | eligible conversion rate 13.64%` · expected **1298** · actual **1312** · random **546** · profit **180800** vs **65831** · `passes_backtest_lift True`

🎙 **SAY** (hover over each output)
> "Notebook four answers the brief's real question.
> First, every customer gets an out-of-fold score: the data is split into five parts, and each customer is scored by a model trained on the other four. No customer is scored by a model that has seen them, so the back-test can't flatter us.
> Then the compliance rules: opted-in and fewer than two complaints leaves fourteen thousand eight hundred and fifty-five eligible customers, who buy at 13.6 percent.
> The top four thousand by score are saved as artifact eight.
> The result: the model expected about thirteen hundred conversions, and thirteen hundred and twelve actually happened. That's very close, so the probabilities can be trusted. Random selection would have given about five hundred and forty-six.
> In money: a hundred and eighty thousand dollars of profit against sixty-six thousand at random, on the same sixteen-thousand-dollar budget. The back-test chart shows both side by side.
> Finally the model is retrained on all twenty thousand customers and packaged with its metrics and a README, which is printed here, as final output three, ready to score the thirtieth-of-September snapshot for Q4."

▶ **DO** Scroll slowly through the printed README.

---

### Scene 10 · Validating the back-test in Excel (29:30–32:30) → final output 1

▶ **DO** File Explorer → `Deliverables\3_Intermediate` → double-click **artifact 8 - backtest scored customers.csv** → **Maximise**.

🎙 **SAY**
> "Before this goes to Marketing, I'll validate the list independently in Excel."

▶ **DO** Click cell **M1** and type the labels in column **M**, then the formulas in column **N**:

| Cell | Type in M | Type in N |
|---|---|---|
| row 1 | `Customers contacted` | `=COUNT(C:C)` |
| row 2 | `Expected conversions` | `=SUM(C:C)` |
| row 3 | `Actual conversions` | `=SUM(K:K)` |
| row 4 | `Actual conversion rate` | `=N3/N1` |
| row 5 | `Eligible base rate` | `0.1364` |
| row 6 | `Random conversions` | `=N1*N5` |
| row 7 | `Profit - model` | `=N3*150-N1*4` |
| row 8 | `Profit - random` | `=N6*150-N1*4` |
| row 9 | `Uplift` | `=N7-N8` |
| row 10 | `Min opt-in (must be 1)` | `=MIN(I:I)` |
| row 11 | `Max complaints (must be 1 or less)` | `=MAX(J:J)` |

✔ **CHECK** 4000 · 1297.6 · 1312 · 0.328 · 0.1364 · 545.6 · 180,800 · 65,840 · 114,960 · 1 · 1

🎙 **SAY** (as each result appears)
> "Exactly four thousand customers. Expected conversions about thirteen hundred, actual thirteen hundred and twelve: a 32.8 percent conversion rate, against 13.6 percent for eligible customers, so 2.4 times, above the target of two.
> Random selection would give about five hundred and forty-six.
> Profit is a hundred and eighty thousand eight hundred dollars against about sixty-six thousand: an uplift of roughly a hundred and fifteen thousand dollars for the same budget.
> And the compliance checks: the minimum opt-in is one, so everyone has opted in, and the maximum complaints is one, so nobody with two or more complaints is on the list."

▶ **DO** **File → Save As → Browse** → `Deliverables\4_Output` → **Save as type: Excel Workbook (*.xlsx)** → name `final output 1 - backtest target list` → **Save** → close Excel.

---

### Scene 11 · Summary deck (32:30–37:00), PowerPoint → final output 2

▶ **DO** File Explorer → `Deliverables\1_Input` → double-click **input 4 - summary deck template.pptx**. **Immediately: File → Save As → Browse** → `Deliverables\4_Output` → name `final output 2 - cross-sell summary` → **Save**.

🎙 **SAY**
> "This is the team's summary template. I'll save my own copy into the Output folder first, so the template stays clean. The orange brackets are what I need to fill in."

▶ **DO** For every orange `[ ]`: click into it → delete the brackets → type the value → select the value → **Home → Font Colour (arrow) → Automatic**.

**Slide 2: Problem and approach**
- `[ ]` duplicate rows → **260**

🎙 **SAY** "Two hundred and sixty duplicate rows removed, plus the date, label and sentinel fixes, and the two leaky fields and gender excluded."

**Slide 3: Model results**
- ROC-AUC → **0.81**
- PR-AUC → **0.42** vs **0.37** baseline
- Top-20% lift → **2.83**×
- Click the **dashed box** → press **Delete** → **Insert → Pictures → This Device…** → `Deliverables\3_Intermediate\artifact 7 - charts\05_lift_by_decile.png` → **Insert** → drag it to fill the right-hand side

🎙 **SAY** "ROC-AUC 0.81 against a target of 0.78, PR-AUC 0.42 against 0.37 for the baseline, and 2.83 times lift in the top twenty percent. The chart shows how sharply conversion falls from the top decile down."

**Slide 4: Back-test and Q4 recommendation**
- Conversions → **1,312** vs **546** random
- Profit → **$180.8k** vs **$65.8k**
- Conversion rate → **32.8%** vs **13.6%**
- Driver 1 → **Engaged customers: high email open rate and frequent app logins**
- Driver 2 → **Established relationship: 2–3 products, 1–5 years tenure, late-30s peak**
- Driver 3 → **Timing and care: no product opened in the last 6 months, few complaints**

🎙 **SAY**
> "In the back-test, the four thousand customers the model chose produced thirteen hundred and twelve sales against five hundred and forty-six at random: a hundred and eighty thousand dollars of profit instead of sixty-six thousand.
> The drivers become messaging guidance: target engaged email and app users, customers with an established relationship of two or three products, and avoid customers who just bought or have complained.
> And the recommendation: use the packaged model on the September snapshot for Q4, keep a ten-percent random control group to measure the real uplift, and re-validate every quarter."

▶ **DO** **File → Save** → close PowerPoint.

---

### Scene 12 · Wrap-up (37:00–38:30), File Explorer

▶ **DO** In File Explorer, open `Deliverables` and hover over each folder and its files.

🎙 **SAY**
> "To wrap up. Input holds the four files I received, plus the original pipeline code, which is delivered as input five. Code is now the corrected pipeline, delivered as final output four. Intermediate holds my pivot analysis, the cleaned data and quality log, the train-test split, the trained models, the model comparison, the charts, and the back-test list. Output holds the validated target list with ROI, the summary deck, and the packaged model with its README.
> I fixed five issues along the way: two caused by changes in the new extract, the date format and the region labels; a missing imputer in the baseline; a new column that leaked the outcome and inflated accuracy to 0.98; and an evaluation that scored labels instead of probabilities.
> Every acceptance criterion is met, and the model is ready to score the September snapshot for the Q4 campaign. Thank you."

▶ **DO** Stay silent for **3 seconds**.

---

## PART 5: Stop and save

▶ **DO**
1. Sharing toolbar → **More (…)** → **Stop recording** → **Stop sharing** → **Leave**
2. A few minutes later: Teams → **Chat** → `UC1 practice` → recording tile → **⋯ → Download** → rename it `UC1_practice_v1.mp4`
3. **Validate and zip the deliverables:**
   ```powershell
   cd $env:USERPROFILE\LLM_Training_recording
   prep\package_deliverables.cmd UC1
   ```
   ✔ ends with **READY TO UPLOAD** and creates `Desktop\UC1_Cross_Sell\Deliverables.zip`. It checks every file is labelled input / artifact / final output, all deliverables exist, every fix is in place and no notebook shows an error. It also adds the original code as **input 5** and your corrected code as **final output 4**, and leaves out junk such as `__pycache__`. If it says **NOT READY**, fix what it lists and run it again.
4. Watch the video at 1.5× and check:
   - [ ] Task notes visible at the start · total length between 15:00 and 45:59
   - [ ] No pop-ups, notifications or AI tools visible · no overlapping windows
   - [ ] Every click was named · every fix: error read → cause explained → fix → re-run → confirmed
5. Send your manager `UC1_practice_v1.mp4` + `Deliverables.zip`. *(For the final Mac take, upload video.mp4, the unmodified recording zip, Deliverables.zip and Metadata.rtf to Mercor Studio.)*
6. Reset for the next attempt: `prep\stage_recording.cmd UC1`

---

## Emergency

| Situation | What to do |
|---|---|
| A fix still errors | Probably a typo. Say "Small typo, I'll correct it", compare with the 🔧 block, then Restart → Run All |
| The kernel picker doesn't show `Python 3.12 (ds-venv)` | Select Kernel → **Python Environments…** → the `.venv` inside `LLM_Training_recording` |
| A notebook stops somewhere not listed in this script | Stop the take. Re-stage and run `prep\selftest_uc1.py` |
| Numbers very different from the cheat sheet | Stop. Re-stage (`prep\stage_recording.cmd UC1`) and start again |
| Word or Excel shows a yellow "Protected View" bar | Click **Enable Editing**. Next time re-stage (it removes the flag) |
| A pop-up or notification appears | Close it and carry on without comment |
| Running long | Skip the optional complaints pivot and shorten the SHAP talk to the top four drivers |
| Teams freezes or disconnects | Stop, re-stage and restart the practice take |

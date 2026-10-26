# UC1 Cross-Sell: End-to-End Recording Guide (Windows practice, Teams recording)

> Keep this guide on **your phone, a printout or a second monitor that is NOT shared**. Nothing from `use_cases/` or `prep/` may appear in the recording.

**Timeline:** Part A setup (once) → Part B rehearsal (day before) → Part C prep (30 min before) → Part D Teams → Part E the take (~35–40 min) → Part F stop and save → Part G review and send.

---

## Part A: One-time setup (skip what's already done)

| # | Step | Check |
|---|---|---|
| A1 | Get the latest project: `cd $env:USERPROFILE\LLM_Training_recording` then `git pull` (or re-download the ZIP) | The brief is dated **1 October 2026** |
| A2 | `.\setup_windows.cmd` | Ends with **READY** |
| A3 | VS Code: only the **Python** and **Jupyter** extensions; Copilot **disabled**; Settings → "disable AI features" ticked | No Copilot icon in the status bar |
| A4 | Restart VS Code once after setup | |
| A5 | Open Word, Excel and PowerPoint once each, dismiss all pop-ups and sign-in prompts, close them | Clean start screens |
| A6 | Do the "first-time VS Code check" in [WINDOWS_SETUP.md](../WINDOWS_SETUP.md) section 5 | `ok` printed with the `Python 3.12 (ds-venv)` kernel |

---

## Part B: Rehearsal (day before; do NOT record)

The rule is confident, expert execution with no trial and error. Rehearsal is where you make your mistakes.

1. `prep\stage_recording.cmd UC1` (or double-click it → type `1`).
2. Do the **whole of Part E** with a stopwatch, speaking out loud. Write your own notebook code. Keep cells short: one idea per cell, 3–8 lines.
3. Write down **on paper** (or your phone, never on the Mac/laptop screen): time per segment, cells that errored, and the numbers you got (they should be close to the reference values in Part E).
4. Fix anything slow. Training should take seconds; the whole notebook should "Run All" in **under 1 minute**.
5. **Reset:** `prep\stage_recording.cmd UC1` (your rehearsal moves to `Rehearsal_Backups`).
6. Target length **35–40 min**. Allowed 15:00–45:59. Under 30 min usually means the narration is too thin.

> Your notebook must be typed live during the take. Don't paste blocks of pre-written code. A rehearsal copy you've looked at is fine as memory; reviewers grade visible expert reasoning, not typing speed.

---

## Part C: 30 minutes before the take

**Machine**
- [ ] `prep\stage_recording.cmd UC1`: fresh folder at `C:\Users\<you>\Desktop\UC1_Cross_Sell`
- [ ] **Quit** (right-click the tray icon → Quit): Outlook, Slack, WhatsApp, OneDrive pop-ups, any chat app. Teams stays open; it's the recorder
- [ ] Teams status → **Do not disturb**; Windows → Settings → System → Notifications → **Do not disturb ON**
- [ ] Close every browser tab and window you don't need (ideally close the browser)
- [ ] Display: Settings → System → Display → Scale **100% or 125%**; Light mode for UC1 (Settings → Personalization → Colors)
- [ ] Desktop tidy: right-click Desktop → View → untick **Show desktop icons** (optional)
- [ ] Battery charging; Windows Update not due to restart (Settings → Windows Update → Pause 1 week)

**Apps to have ready (closed or minimised, nothing overlapping)**
- [ ] File Explorer open at `Desktop\UC1_Cross_Sell`, maximised
- [ ] **Notepad** with the contents of `Task Notes.txt` (open the file directly; it's already written, so the "notes under 3 minutes" rule is met)
- [ ] VS Code **closed** (you'll open it on camera)
- [ ] Word, Excel, PowerPoint **closed**

**You**
- [ ] Headset mic, quiet room, water, phone silent (this guide open on it)
- [ ] Mic check: Teams → Settings → Devices → **Make a test call**

---

## Part D: Teams recording setup

1. Teams → **Calendar** → **Meet now** → name it `UC1 practice` → **Start meeting**.
2. Pre-join screen: **Camera OFF**, **Microphone ON**, audio device = your headset → **Join now**. Close "Invite people" with ✕.
3. **Share first, then record**, so the recording starts on your screen and not on the meeting view:
   - Click **Share** → **Screen** → pick your main display. Leave "Include sound" off.
   - A red border shows what's shared. The Teams meeting window shrinks to a small floating box.
4. Move the small floating Teams box to the **bottom-right corner**, out of the way. Hover over the sharing toolbar at the top centre to find **More (…) → Record and transcribe → Start recording** (or press the record button in the floating box). Accept the recording notice.
5. **Wait 3 seconds** in silence, then start Part E.

> **Before the real take, do a 1-minute test:** share, record, say a sentence, open Notepad, stop. Check the MP4 (Part F) for audio level, legibility, and whether the floating Teams box shows in the recording. If it does, keep it in the corner and never put content under it.
>
> If **Record is greyed out**, your org has disabled Teams recording. Use Snipping Tool instead ([WINDOWS_SETUP.md](../WINDOWS_SETUP.md) section 7).

---

## Part E: The take (~35–40 min)

How to read each segment: **Do** = actions · **Say** = narration cues (your own words, *not* read verbatim) · **Check** = what you should see.

**Golden rules (every segment)**
- Before each click: **name the element** and say why ("I'll click the **Run** button on this cell, the triangle on its left, to load the data"). Never "this / here / that" without naming it.
- Hover before clicking, pause about 1 s after each click, one action at a time, wait for cells to finish.
- Mouse and menus, not shortcuts: click the cell ▶ Run button, not Shift+Enter (copy/paste is fine).
- Trace text with the cursor when reading; small circles for emphasis (don't overdo it).
- Windows maximised or side by side; never overlapping.

---

### E0 · Intro and task notes (0:00–0:45), Notepad
**Do:** Notepad is visible and maximised. Slowly trace each section with the cursor.
**Say:** "I'm a senior data scientist. Marketing contacts 4,000 customers per campaign and today picks them at random, converting about one in nine. Before they sign off the Q4 budget they want proof that a model does better. I'll build and explain a cross-sell model, then back-test it: which 4,000 customers it would have picked on 30 June, and how many actually converted. Deliverables: the notebook, a back-test target list in Excel, a packaged model, and a 3-slide summary. I'm done when the criteria at the bottom are met."
**Check:** notes visible for at least 5 seconds.

### E1 · Read the brief (0:45–2:30), File Explorer → Word
**Do:** Minimise Notepad (the **–** button, top right). In File Explorer double-click `Deliverables` → double-click `input 3 - campaign brief.docx` → maximise Word.
**Say** (hover over each line as you name it):
- "The brief is from the Head of CRM, dated 1 October, so the July–September outcomes are complete."
- "Budget: 4,000 contacts at **$4** each; each extra product is worth **$150** of margin."
- "Compliance: only **opted-in** customers may be contacted, and **gender must not be a model input**."
- "Customer care: anyone with **two or more complaints** is excluded."
- "The model may only use information available at the snapshot date. That's my leakage rule."
- "Acceptance: ROC-AUC at least 0.78, beat a logistic baseline on PR-AUC, top-20% lift at least 2.5, and the back-test list must convert at least twice the eligible average."
**Do:** Close Word (✕).

### E2 · Data dictionary and leakage hypotheses (2:30–4:30), Excel
**Do:** Double-click `input 2 - data dictionary.xlsx` → maximise.
**Say:**
- Trace the **Column** and **Source System** columns. "Most features come from Core Banking, CRM and the warehouse, all as of the snapshot."
- Hover over the `welcome_pack_sent` row: "Fulfilment system, refreshed daily. A welcome pack is sent **after** a product is opened, so this probably leaks the outcome. I'll test it."
- Hover over `cross_sell_product_type`: "Sales ledger, refreshed daily, category of the most recent cross-sell. Same suspicion."
- Hover over `gender`: "Flagged as a protected attribute; the brief excludes it."
- Hover over `email_open_rate`: "Only tracked when emails were sent, so I expect structural missing values for opted-out customers."
**Do:** Close Excel (✕, **Don't Save**).

### E3 · Open the project in VS Code (4:30–5:30)
**Do:** Start menu → **Visual Studio Code** → maximise → **File → Open Folder…** → Desktop → `UC1_Cross_Sell` → **Select Folder** → trust the folder if asked.
**Do:** **File → New File… → Jupyter Notebook**. Then **File → Save As…** → into `Deliverables` → name `final output 1 - cross_sell_model.ipynb`.
**Do:** Top right **Select Kernel → Jupyter Kernel… → Python 3.12 (ds-venv)**.
**Say:** "This notebook is my main deliverable. I'm saving it into Deliverables as final output 1 and using the project's Python 3.12 environment."
**Tip:** Start with a **Markdown** cell (click **+ Markdown**) titled `# Cross-sell propensity model: back-test for Q4` and a one-line objective. Add a short Markdown header before each section below; it helps reviewers and makes your narration easier.

### E4 · Data quality (5:30–11:00), VS Code
Work through these in order, one small cell each, narrating the *why*:

| Step | What to do | Say / decision | Check (reference) |
|---|---|---|---|
| 4.1 Load and profile | read the CSV; shape; dtypes; `head()`; target rate | "Twenty thousand two hundred sixty rows, but the extract should have 20,000 customers, so I expect duplicates" | 20,260 rows; target ≈ 11.6% |
| 4.2 Duplicates | count exact duplicates, then duplicate `customer_id` after dropping them; look at one pair | "200 exact copies from the CRM merge, plus 60 customers with conflicting rows, differing only in balance and last channel. There's no update timestamp, so I keep the first and log it. I de-duplicate **before** splitting, otherwise the same customer lands in train and test" | 200 exact; 60 near → 20,000 rows |
| 4.3 Labels | `value_counts()` on `region`, `primary_product`; strip + case-normalise + map abbreviations (`N.`→north, `CC`→credit card, `current acct`, `P. Loan`, `W.`) | "Five regions, but spelled many ways: lower case, trailing spaces, abbreviations" | 5 regions, 5 products |
| 4.4 Sentinels | `describe()`; `age` 0 / 999, `avg_monthly_balance` −99999, `tenure_months` −1 | "999 is a system default, not a customer. Set to missing" | ~60 ages, ~60 balances, ~40 tenures |
| 4.5 Dates and tenure | parse `customer_since`: ISO format first, then `%d/%m/%Y` for the rest; recompute tenure for negatives | "About 2% are day-first. I parse each format explicitly rather than letting pandas guess" | 0 unparsed dates |
| 4.6 Missingness | missing % by column; income missing rate **by segment**; `email_open_rate` missing vs `marketing_opt_in` | "Income is missing 10% for Mass vs 4% for others: not random, so I add a `income_missing` flag. Email open rate is missing exactly for opted-out customers: structural, it means not emailed" | Mass ~10%, others ~4% |
| 4.7 Save | cleaned frame → `Deliverables/artifact 1 - cleaned customers.csv` | "Artifact 1, the cleaned dataset" | file appears in the Explorer panel |

### E5 · Leakage audit and split (11:00–13:30)
| Step | What to do | Say | Check |
|---|---|---|---|
| 5.1 | target rate by `welcome_pack_sent` | "86% vs under 1%: the pack goes out after purchase. Post-outcome, dropped" | ~0.86 vs ~0.01 |
| 5.2 | target rate where `cross_sell_product_type` is filled | "100%: it's only filled for buyers. Dropped" | 1.0 |
| 5.3 | drop leaks + `gender` + IDs/dates; one-hot categoricals | "If I'd kept these I'd report a near-perfect model that fails on day one" | |
| 5.4 | stratified 80/20 split, fixed `random_state` | "Stratified because positives are only 11.6%; fixed seed for reproducibility" | test positive rate ≈ train rate |

### E6 · Baseline → improved model (13:30–18:00)
| Step | What to do | Say | Check (hold-out) |
|---|---|---|---|
| 6.1 | Logistic regression pipeline (impute + scale + one-hot), fit, ROC-AUC and PR-AUC | "First a simple, explainable baseline. With 11.6% positives accuracy is meaningless, so PR-AUC is my main metric; a random model scores 0.116" | ROC ~0.78, PR ~0.35 |
| 6.2 | HistGradientBoostingClassifier with early stopping (handles NaN natively), fit, same metrics | "Gradient boosting can capture non-linear effects such as tenure sweet spots and thresholds" | ROC ~0.81, PR ~0.40 |
| 6.3 | One small, reasoned tuning step (e.g. learning rate or `max_leaf_nodes`), compared on a validation split, not the test set | "I tune on validation so the test set stays untouched" | small or no gain is fine; say so |

### E7 · Evaluation against the criteria (18:00–21:30)
| Step | What to do | Say | Check |
|---|---|---|---|
| 7.1 | decile table: sort the test set by score → 10 bins → conversion rate and lift per decile; top-20% lift | "The top fifth converts about 2.9× the average; the criterion was 2.5" | top-20% lift ~2.9 |
| 7.2 | calibration curve (`CalibrationDisplay`) + Brier score | "Marketing will budget on expected conversions, which is the sum of probabilities, so the probabilities must be honest. The curve sits close to the diagonal" | near-diagonal |
| 7.3 | save comparison table → `Deliverables/artifact 2 - model comparison.csv` | "Artifact 2: baseline vs boosted, all metrics" | |
| 7.4 | Read each criterion out loud: met / not met | | |

### E8 · Explain the drivers (21:30–24:30)
**Do:** SHAP `TreeExplainer` on the boosted model with a sample of about 1,000 test rows → `summary_plot` (beeswarm). Hover over each top feature row.
**Say:** turn each driver into an action, e.g.
- "Customers with **two or three products** are most likely to add another: an established relationship."
- "**Tenure between one and five years** helps; brand-new customers aren't ready yet."
- "Someone who **opened a product in the last six months** is less likely; they just bought."
- "**App logins** matter only for customers with the app, so digital engagement is the channel."
- "**Email open rate** above about 20% lifts propensity, so email works for engaged opted-in customers."
- "**Complaints** strongly reduce propensity, which supports the customer-care exclusion."
- "**Credit-card holders with high balances** respond, which points to a card upgrade offer."

### E9 · Back-test target list (24:30–27:00), VS Code
| Step | What to do | Say | Check (reference) |
|---|---|---|---|
| 9.1 | `cross_val_predict` (5-fold stratified, same model settings, `method="predict_proba"`) on all 20,000 | "For the back-test every customer must be scored by a model that **never saw them**. Otherwise the result would flatter us" | runs in seconds |
| 9.2 | eligible = `marketing_opt_in == 1` and `complaints_12m < 2` | "Compliance and customer-care rules from the brief" | 14,855 eligible; base rate ~13.6% |
| 9.3 | top 4,000 by out-of-fold probability; keep `customer_id`, probability, key features, actual outcome → `Deliverables/artifact 3 - backtest scored customers.csv` | "Artifact 3, the 4,000 customers we would have contacted" | 4,000 rows |
| 9.4 | quick check: sum of probabilities vs actual conversions | "We'll validate this in Excel" | expected ~1,250, actual ~1,300 |

### E10 · Validate and ROI in Excel (27:00–30:00), final output 2
**Do:** File Explorer → `Deliverables` → double-click `artifact 3 - backtest scored customers.csv` → maximise Excel.
1. Click the **column header** of the probability column → status bar shows **Count = 4,001** (header + 4,000). "Exactly 4,000 customers."
2. **Home → Sort & Filter → Filter**. Open the `marketing_opt_in` filter: only **1**. Open `complaints_12m`: only **0** and **1**. "Every row is compliant."
3. New sheet: click **+** at the bottom → rename it `ROI Summary` (right-click the tab → Rename). Type labels in column A and formulas in column B (type them; they're short):

| A | B (formula) |
|---|---|
| Customers contacted | `=COUNTA('artifact 3 - backtest scored customers'!A:A)-1` |
| Expected conversions (model) | `=SUM(<probability column>)` |
| Actual conversions | `=SUM(<outcome column>)` |
| Actual conversion rate | `=B3/B1` |
| Eligible base rate | `0.136` *(from the notebook)* |
| Random-selection conversions | `=B1*B5` |
| Profit, model (actual) | `=B3*150-B1*4` |
| Profit, random | `=B6*150-B1*4` |
| Uplift | `=B7-B8` |

> The sheet name in the first formula must match exactly. Simpler: click into the cell and select the column with the mouse while typing the formula.

**Say:** "Expected about 1,250 vs actual about 1,300: the probabilities are honest. The list converts at 32.6%, about 2.4 times the eligible average, which meets the criterion. Profit is about $180k against $66k for random, an uplift of about $114k on the same budget."
4. **File → Save As → Browse** → `Deliverables` → type **Excel Workbook (*.xlsx)** → name `final output 2 - backtest target list` → **Save**. Close Excel.

### E11 · Package and reproduce (30:00–32:00), VS Code
1. Final cell: refit the chosen model on **all** 20,000 customers; save it with `joblib` to `Deliverables/final output 3 - model package/model.joblib`; write `metrics.json` (hold-out metrics + back-test results).
2. **File → New File… → Markdown** → save as `final output 3 - model package/README.md`: purpose, input columns required, features **excluded** (leaks + gender) and why, how to score the 30-Sep snapshot, hold-out metrics, back-test result, limitations (synthetic snapshot, single period, re-validate each quarter).
3. Back in the notebook: toolbar **Restart** → then **Run All**. "Same seed, same results: hold-out metrics and the back-test reproduce exactly."
**Check:** the metrics printed match `metrics.json`.

### E12 · 3-slide summary (32:00–36:30), PowerPoint, final output 4
**Do:** Start → PowerPoint → **Blank presentation** → maximise. Use **Home → Layout → Title and Content**.

| Slide | Title | Content (bullets) |
|---|---|---|
| 1 | Problem and approach | Random targeting converts ~1 in 9 · 20,000-customer 30-Jun snapshot, Jul–Sep outcomes · cleaned 260 duplicate rows, sentinels, mixed dates · removed 2 leaky fields + gender · logistic baseline → gradient boosting |
| 2 | Model results | Hold-out ROC-AUC 0.81 (target 0.78) · PR-AUC 0.40 vs 0.35 baseline · top-20% lift 2.9× (target 2.5×) · calibration close to diagonal. Optional: Insert → Pictures → the SHAP plot if you saved it as PNG |
| 3 | Back-test and Q4 recommendation | 4,000 compliant customers: 1,304 conversions (32.6%) vs 546 random · profit ≈ $180k vs $66k · drivers → messaging (multi-product, 1–5 yr tenure, app-engaged, card upgrade) · next: score the 30-Sep snapshot with the packaged model; re-validate quarterly |

**File → Save As → Browse** → `Deliverables` → `final output 4 - cross-sell summary.pptx`. Close PowerPoint.

### E13 · Wrap-up (36:30–37:30), File Explorer
**Do:** Show `Deliverables`, hovering over each file as you name it: inputs 1–3, artifacts 1–3, final outputs 1–4.
**Say:** go through each acceptance criterion with its number. "All criteria are met. The model is packaged for the Q4 snapshot." Pause 3 seconds in silence.

---

## Part F: Stop and save the recording

1. Hover over the sharing toolbar → **More (…) → Stop recording** (or the stop button in the floating box).
2. **Stop sharing**, then **Leave** the meeting.
3. Get the file: Teams → **Chat** → the `UC1 practice` meeting chat → the recording tile → **⋯ → Download** (or **Open in OneDrive** → Download). It lands in `Downloads` as MP4. Rename it `UC1_practice_v1.mp4`.
   - The recording appears in the chat a few minutes after the meeting ends.
   - Recordings in OneDrive may auto-expire (often after 60–120 days, depending on org policy), so download them.

## Part G: Review and send for internal approval

1. **Watch the whole video** (at 1.5×) and score yourself:
   - [ ] Task notes visible at the start · total length 15:00–45:59
   - [ ] Every click announced with the element's name · no "this / here" without naming it
   - [ ] No pop-ups or notifications · no overlapping windows · no Copilot/AI visible
   - [ ] No trial and error left unexplained · cursor smooth, not jittery
   - [ ] Every decision explained (duplicates, leakage, metric choice, calibration, out-of-fold back-test)
2. Zip the folder: File Explorer → right-click `Deliverables` → **Send to → Compressed (zipped) folder** → `Deliverables.zip`.
3. Send your manager: `UC1_practice_v1.mp4` + `Deliverables.zip`. Optional: a 3-line note: *"Practice run of UC1 for Mercor Frost. Final recording will be on the Mac with TaskRecorder. Please check the narration, task depth and anything a reviewer might flag."*
4. Record feedback in [Open_Questions.md](Open_Questions.md) or your notes; apply it before the Mac take.
5. Reset for the next attempt: `prep\stage_recording.cmd UC1`.

## If something goes wrong during the take

| Situation | What to do |
|---|---|
| A cell errors (typo) | Stay calm: "That's a typo in the column name, I'll fix it." Fix it and re-run. One or two of these is natural |
| Wrong approach mid-way | Explain the correction as an expert decision ("On reflection, a better choice is…"); don't silently undo |
| A pop-up or notification appears | Dismiss it, say nothing, continue |
| Teams disconnects or freezes | Stop. For an internal practice run, re-stage and restart (the final Mac take must be one continuous take anyway) |
| Running long | Shorten E8 to the top 4 drivers and slide 2 to 3 bullets; keep everything that proves a criterion |

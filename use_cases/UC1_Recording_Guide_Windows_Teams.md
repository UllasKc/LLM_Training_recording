# UC1 Cross-Sell: End-to-End Recording Guide (Windows practice, Teams recording)

> Keep this guide, and [UC1_Planted_Bugs_Answer_Key.md](UC1_Planted_Bugs_Answer_Key.md), on **your phone, a printout or a second monitor that is NOT shared**. Nothing from `use_cases/` or `prep/` may appear in the recording.

**What the video shows:** a senior data scientist receives a business request, explores the data in Excel with pivots, runs the team's **existing pipeline** (4 notebooks + config) on the new snapshot, **diagnoses and fixes 5 problems** caused by changes in the extract and by code-review issues, validates the business case in Excel, and finishes the summary deck. About **38 minutes**, 6 apps: Notepad → File Explorer → Word → Excel → VS Code → Excel → PowerPoint → File Explorer.

**Timeline:** A setup (once) → B rehearsal (day before) → C prep (30 min before) → D Teams → E the take → F stop and save → G review and send.

---

## Part A: One-time setup

| # | Step | Check |
|---|---|---|
| A1 | `cd $env:USERPROFILE\LLM_Training_recording` → `git pull` | `recording_workspace\UC1_Cross_Sell\Deliverables` has `1_Input` and `2_Code` |
| A2 | `.\setup_windows.cmd` | Ends with **READY** and lists the 5 UC1 code files |
| A3 | `.\.venv\Scripts\python.exe prep\selftest_uc1.py` | Ends with **SELF-TEST PASSED** (about 30 s): all 5 bugs and fixes behave as documented on your laptop |
| A4 | VS Code: only the **Python** and **Jupyter** extensions; Copilot disabled; Settings → "disable AI features" ticked; restart VS Code | No Copilot icon |
| A5 | Open Word, Excel and PowerPoint once each, dismiss all pop-ups, close them | |

---

## Part B: Rehearsal (day before; do NOT record)

1. **Read every line** of `2_Code/pipeline_config.py` and the 4 notebooks, and all of the answer key. You must be able to explain any line if asked. This is presented as *your team's* pipeline, so know it like your own.
2. `prep\stage_recording.cmd UC1` → do the **whole of Part E** with a stopwatch, out loud, including the 5 fixes.
3. Note on paper the time per segment and anything you stumbled on.
4. **Reset:** `prep\stage_recording.cmd UC1`. The bugs are back and the outputs are cleared; your rehearsal copy moves to `Rehearsal_Backups`.
5. Target **35–40 min** (allowed 15:00–45:59).

---

## Part C: 30 minutes before the take

- [ ] `prep\stage_recording.cmd UC1`: fresh `Desktop\UC1_Cross_Sell` (bugs present, `3_Intermediate` and `4_Output` empty)
- [ ] **Quit** Outlook, Slack, WhatsApp and other chat apps (tray icon → Quit). Teams stays: it's the recorder. Teams status → **Do not disturb**
- [ ] Windows **Do not disturb ON** (Settings → System → Notifications)
- [ ] Browser closed · Windows Update paused · charger in
- [ ] Display scale 100–125% · **Light mode** for UC1
- [ ] Open, maximised and ready: **File Explorer** at `Desktop\UC1_Cross_Sell`, then **Notepad** with `Task Notes.txt` on top. VS Code, Word, Excel and PowerPoint **closed**
- [ ] Headset mic · Teams → Settings → Devices → **Make a test call**

## Part D: Teams recording

1. Teams → **Calendar → Meet now** → `UC1 practice` → **Start meeting** → camera **off**, mic **on** (headset) → **Join now**; close "Invite people".
2. **Share → Screen** (main display, "Include sound" off). Move the small floating Teams window to the **bottom-right corner**.
3. Sharing toolbar (top centre) → **More (…) → Record and transcribe → Start recording**. Wait 3 s, then begin.

> Do a 1-minute test first: check the audio and whether the floating Teams box shows in the MP4. If **Record** is greyed out, use Snipping Tool ([WINDOWS_SETUP.md](../WINDOWS_SETUP.md) section 7).

---

## Part E: The take (~38 min)

**Golden rules:** name every element before you click it and say why · hover, then click, then pause about 1 s · one action at a time · mouse and menus, not shortcuts (copy/paste are fine) · trace text with the cursor while reading · windows maximised, never overlapping.

### E0 · Task notes (0:00–1:00), Notepad
Trace each line slowly with the cursor.
**Say:** "I'm a senior data scientist. Marketing contacts 4,000 customers per campaign and picks them at random, converting about one in nine. Before signing off the Q4 budget they want proof that a model does better. Our team has a cross-sell pipeline built for an earlier snapshot. I'll explore the new 30 June data, run that pipeline on it, fix whatever the new extract breaks, and back-test which 4,000 customers it would have picked and how many actually converted. Deliverables: an exploratory pivot workbook, the corrected pipeline and model package, a back-test list with ROI, and a summary deck."
Then minimise Notepad (the **–** button).

### E1 · The brief (1:00–2:30), File Explorer → Word
File Explorer → `Deliverables` → `1_Input` → double-click **input 3 - campaign brief.docx** → maximise.
**Say** (hover over each item): dated 1 October, outcomes complete · **4,000 contacts at $4, $150 margin** · **opt-in only, no gender, exclude 2+ complaints** · only snapshot-date information (the leakage rule) · back-test scored by models that never saw the customer · acceptance: ROC-AUC ≥ 0.78, beat the baseline on PR-AUC, top-20% lift ≥ 2.5×, back-test ≥ 2× the eligible average · deck on the team template (input 4).
Close Word.

### E2 · Data dictionary (2:30–4:00), Excel
Double-click **input 2 - data dictionary.xlsx** → maximise.
**Say:** trace **Source System** and **Notes** · `welcome_pack_sent`: "fulfilment system, refreshed daily. A pack goes out after a product opens, so this is a leakage suspect" · `cross_sell_product_type`: same · `gender`: protected · `email_open_rate`: "only tracked when emails were sent".
Close Excel (Don't Save).

### E3 · Exploratory pivots (4:00–11:00), Excel → artifact 1
1. Double-click **input 1 - customers.csv** → maximise. Click the **column A header** → status bar **Count: 20,261**. "20,260 rows plus the header, but the brief says 20,000 customers. There are duplicates; I'll handle them in the pipeline."
2. Click any data cell → **Insert → PivotTable** → *Table/Range* is filled in → **New Worksheet** → **OK**.
3. **Pivot 1, products:** drag `num_products` to **Rows**; `customer_id` to **Values** (Count); `next_product_purchased_90d` to **Values**, then click it → **Value Field Settings → Average → Number Format → Percentage, 1 dp → OK**.
   **Say:** "1 product converts 7.8%, 2 products 15.7%, 3 products 20.1%, but 4 drops to 9.2%. It's not linear: customers with everything are saturated. A tree model will capture that." Rename the sheet tab (right-click → Rename) to **Products**.
4. **Pivot 2, data quality:** go back to the data sheet → Insert → PivotTable → New Worksheet. Rows `region`, Values Count of `customer_id`.
   **Say:** "Five regions should appear, but I see `N.`, `W.` and duplicates with leading or trailing spaces. Excel ignores letter case, but the code won't. The pipeline must normalise these." Tab: **Data quality**.
5. **Pivot 3, leakage check:** Rows `welcome_pack_sent`, Values Average of `next_product_purchased_90d` (as %) and Count of `customer_id`.
   **Say:** "Customers with a welcome pack converted 85.4%, without it 0.7%. That's the outcome itself, recorded after the purchase. It must never be a model input." Tab: **Leakage check**.
6. **Pivot 4, missing income:** Rows `customer_segment`, Values Count of `customer_id` **and** Count of `monthly_income` (Count ignores blanks).
   **Say:** "Mass: 14,802 customers but only 13,326 incomes, so 10% missing, vs about 4% elsewhere. It's not random, so I'll keep a missing flag rather than just fill it in." Tab: **Missing income**.
7. Optional, if time allows: Rows `marketing_opt_in` (6.0% vs 13.4%) and `complaints_12m` (12.8% → 7.2% → 2.4%), which supports the brief's exclusions.
8. **File → Save As → Browse** → `Deliverables\3_Intermediate` → type **Excel Workbook (*.xlsx)** → name **artifact 1 - exploratory pivot analysis** → Save. Close Excel.

### E4 · The existing pipeline (11:00–12:30), VS Code
Start → **Visual Studio Code** → maximise → **File → Open Folder…** → Desktop → `UC1_Cross_Sell` → Select Folder (trust it if asked).
**Say** (expand the folders in the Explorer panel one by one): "Input, Code, Intermediate and Output. Inputs are read-only, everything the pipeline produces goes to Intermediate, and the business deliverables go to Output." Open **2_Code → pipeline_config.py** and scroll slowly: paths · business rules from the brief · `TARGET`, `PROTECTED_COLUMNS`, `LEAKY_COLUMNS` · the two model builders. "Four notebooks run in order: preprocessing, training, testing, back-test. This was built for the earlier snapshot; let's see how it handles the new one."

### E5 · Notebook 01: preprocessing (12:30–17:30), bugs P1 and P2
1. Open **01_data_preprocessing.ipynb**. Top right should show **Python 3.12 (ds-venv)**; if not, Select Kernel → Jupyter Kernel → it. Scroll through the section headers and explain the plan.
2. Toolbar → **Run All**. It stops in section 3 → **P1** (answer key). Read the error aloud, explain it, fix it, then **Restart → Run All**.
3. It stops in section 4 → **P2**. "This matches what I saw in the pivot." Fix, then **Restart → Run All**. It runs to the end.
4. Walk through the outputs, hovering over each: 20,260 rows → **200 exact + 60 conflicting duplicates** ("I de-duplicate before any split so a customer can't land in both train and test") · ~400 day-first dates · label fixes · **age 0/999 and balance −99999** set to missing · income missing by segment (it matches the pivot) · the opt-in/open-rate crosstab: "missing open rate means *not emailed*, so 0 is the right value" · the final save message.
5. In the Explorer panel click **3_Intermediate → artifact 3 - data quality log.csv**: "Every cleaning decision is logged for audit."

### E6 · Notebook 02: training (17:30–22:30), bugs T1 and T2
1. Open **02_model_training.ipynb** → **Run All**. It stops in section 2 → **T1**. The traceback points into `pipeline_config.py`: open it, fix `build_baseline`, **File → Save**, back to the notebook → **Restart → Run All**.
2. Cross-validation completes with **AUC ≈ 0.98** → **T2**. "Too good to be true; the pivot already showed why." Optionally add the one-line proof cell. Fix `LEAKY_COLUMNS` in the config → Save → **Restart → Run All**.
3. **Say:** stratified split (train 16,000 / test 4,000, both 11.6% positive) · CV on the training set only, "the test set stays untouched until notebook 03" · CV ROC-AUC ~0.77 vs ~0.80, PR-AUC ~0.32 vs ~0.37: "with 11.6% positives PR-AUC is the honest metric; random would score 0.116" · early stopping iterations · models saved as **artifact 5**.

### E7 · Notebook 03: testing (22:30–27:00), bug E1
1. Open **03_model_testing.ipynb** → **Run All**. It completes, but the hold-out shows **ROC-AUC ≈ 0.58** and the checks show `False` → **E1**. Fix → **Restart → Run All**.
2. **Say**, as each output appears:
   - Hold-out table: **0.81 / PR-AUC 0.42 vs 0.37 baseline vs 0.116 random**.
   - Lift by decile: "the top decile converts about 4× the average and the bottom deciles almost never; the top 20% is **2.83×**, against a criterion of 2.5". Hover over the bar chart.
   - Calibration: "close to the diagonal, so expected conversions can be trusted for budgeting".
   - SHAP: hover over each top feature and turn it into a marketing action: number of products, tenure 1–5 years, recent product opened (negative), app logins, email open rate, complaints (negative), credit card + high balance.
   - Acceptance table: **all True**. Mention artifacts 6 and 7 saved.

### E8 · Notebook 04: back-test and package (27:00–29:30)
Open **04_backtest_and_package.ipynb** → **Run All**.
**Say:** "Every customer is scored by a model trained on the other four folds, so the back-test can't flatter us" · **14,855 eligible** (opted-in, < 2 complaints), base rate 13.64% · 4,000 selected → **artifact 8** · back-test: **expected ~1,298 vs actual 1,312**: "the probabilities are honest" · **1,312 vs 546 random** · profit **$180.8k vs $65.8k** · the final model is trained on all 20,000 → **final output 3**: model, metrics.json, and a README printed below. Scroll through the README.

### E9 · ROI validation (29:30–32:30), Excel → final output 1
1. File Explorer → `3_Intermediate` → double-click **artifact 8 - backtest scored customers.csv** → maximise.
2. In **column M** type labels and in **column N** formulas (same sheet, no sheet references needed):

| M | N |
|---|---|
| Customers contacted | `=COUNT(C:C)` |
| Expected conversions | `=SUM(C:C)` |
| Actual conversions | `=SUM(K:K)` |
| Actual conversion rate | `=N3/N1` |
| Eligible base rate | `0.1364` *(from notebook 04: "eligible conversion rate 13.64%")* |
| Random-selection conversions | `=N1*N5` |
| Profit: model | `=N3*150-N1*4` |
| Profit: random | `=N6*150-N1*4` |
| Uplift | `=N7-N8` |
| Min marketing_opt_in (must be 1) | `=MIN(I:I)` |
| Max complaints_12m (must be ≤ 1) | `=MAX(J:J)` |

   **Say:** "4,000 customers, all opted in, none with 2+ complaints. 1,312 actual vs 546 random: a $115k uplift on the same $16k budget."
3. **File → Save As → Browse** → `4_Output` → **Excel Workbook (*.xlsx)** → **final output 1 - backtest target list** → Save. Close Excel.

### E10 · Summary deck (32:30–37:00), PowerPoint → final output 2
1. File Explorer → `1_Input` → double-click **input 4 - summary deck template.pptx**. **Immediately File → Save As → Browse** → `4_Output` → **final output 2 - cross-sell summary.pptx** (the template stays untouched).
2. Replace each **orange `[ ]`** with the real number: click into it, type, then select the text → **Home → Font Colour → Automatic** (orange means "still to fill in").
   - Slide 2: duplicate rows **260**
   - Slide 3: ROC-AUC **0.81** · PR-AUC **0.42** vs **0.37** · lift **2.83×**. Click the dashed box → Delete → **Insert → Pictures → This Device** → `3_Intermediate\artifact 7 - evaluation charts\lift_by_decile.png` → drag to fit the right-hand area
   - Slide 4: **1,312** vs **546** · **$180.8k** vs **$65.8k** · **32.8%** vs **13.6%** · three drivers from SHAP (e.g. "2–3 products held", "1–5 years tenure, no product opened in the last 6 months", "engaged app and email users")
3. **Say** while editing: read each number aloud and tie it to the acceptance criterion it proves. **File → Save**. Close PowerPoint.

### E11 · Wrap-up (37:00–38:30), File Explorer
Open `Deliverables` and hover over each folder and file: inputs 1–4 · the corrected code · artifacts 1–8 · final outputs 1–3.
**Say:** "Five issues fixed: two schema-drift problems from the new extract, a missing imputer, a leaky new column, and an evaluation bug. Every acceptance criterion is met, and the model is packaged to score the 30 September snapshot for Q4." Stay silent for 3 s.

---

## Part F: Stop and save

1. Sharing toolbar → **More (…) → Stop recording** → **Stop sharing** → **Leave**.
2. Teams → **Chat** → `UC1 practice` → recording tile → **⋯ → Download** (a few minutes after the meeting ends) → rename it **UC1_practice_v1.mp4**. Download it: OneDrive recordings may expire.

## Part G: Review and send for internal approval

1. Watch it at 1.5× and tick:
   - [ ] Task notes at the start · length 15:00–45:59 · no pop-ups or AI tools visible
   - [ ] Every click named · no "this / here" without a name · smooth cursor
   - [ ] Each bug: error read aloud → cause explained → minimal fix → re-run → confirmed
   - [ ] Each business number tied to an acceptance criterion
2. Right-click `Deliverables` → **Send to → Compressed (zipped) folder** → `Deliverables.zip`.
3. Send your manager **UC1_practice_v1.mp4 + Deliverables.zip** with a note: *"Practice run of UC1 for Mercor Frost; final recording on the Mac with TaskRecorder. Please check narration, depth and anything a reviewer might flag."*
4. Reset: `prep\stage_recording.cmd UC1`.

## If something goes wrong

| Situation | What to do |
|---|---|
| You mistype a fix | It errors again. "Typo, I'll correct it." Fix it and re-run; that's natural |
| A notebook stops somewhere unexpected | Read the error and fix it calmly. If you can't, stop the take: for practice, re-stage and restart. Run `prep\selftest_uc1.py` to compare |
| Numbers differ a lot from the answer key | Stop. Something changed; re-stage and re-run the self-test |
| A pop-up appears | Dismiss it and carry on |
| Running long | Skip the optional pivot (E3.7) and SHAP detail; keep everything that proves a criterion |

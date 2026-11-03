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

## 🍎 MAC FINAL TAKE: use this instead of Parts 1, 2, 3 and 5

Parts 1, 2, 3 and 5 below are written for the Windows practice with Teams. On the Mercor Mac, do the steps in this section instead. **Part 4 (the scenes) is the same on both**; the table at the end of this section lists the few clicks that differ on the Mac.

### Mac Part 1: the day before (off camera)

1. Open **Terminal** (Finder → Applications → Utilities → Terminal) and run:
   ```bash
   cd ~
   git clone https://github.com/UllasKc/LLM_Training_recording.git     # first time only
   cd ~/LLM_Training_recording
   git pull
   bash setup_mac.sh
   .venv/bin/python prep/selftest_uc2.py
   ```
   ✔ setup ends with **READY**; the self-test ends with **SELF-TEST PASSED**. Python 3.12 must be installed first from python.org (see README section 2). You have admin access, so expect a password prompt for the Python installer, and a one-time "install the command line developer tools" prompt the first time you run `git` (click **Install**, then re-run the command).
2. **VS Code:** only the **Python** and **Jupyter** extensions (Microsoft). No Copilot or AI extensions. **Code → Settings → Settings** → search "disable AI features" → tick it.
3. **Open Firefox, LibreOffice Calc and LibreOffice Impress once each**, click **Open** if macOS asks about an app downloaded from the internet, and dismiss every first-run pop-up (LibreOffice: close "Tip of the Day" and untick "Show tips on startup"). Then quit them (app menu → **Quit**).
4. **Default apps** so "Open With" is predictable. In Finder, for one file of each type in `~/LLM_Training_recording/recording_workspace/UC2_Propensity_To_Pay/Deliverables/1_Input`: select it → **File → Get Info** → **Open with:** choose the app → **Change All…** → **Continue**.
   - `.pdf` → **Firefox**
   - `.csv` and `.xlsx` → **LibreOffice** (Calc)
   - `.pptx` → **LibreOffice** (Impress)
5. **Mercor setup:** complete section A of `use_cases/Recording_Checklist.md`: TaskRecorder installed and signed in with the **Mercor OTA** account, permissions green, Accessibility Inspector minimised in the Dock, Insightful running, clock with seconds.
6. **Rehearse the whole of PART 4 once, out loud, with a stopwatch** (not recorded). Then reset with `bash prep/stage_recording.sh UC2`.

### Mac Part 2: 30 minutes before the take

▶ **DO**
- [ ] Terminal:
  ```bash
  cd ~/LLM_Training_recording
  bash prep/stage_recording.sh UC2
  ```
  → a fresh, new `~/Mercor_UC2/UC2_Propensity_To_Pay_vN` folder (the full path is printed). Always use the **newest** one. Then **Terminal → Quit Terminal**
- [ ] **Finder sidebar** (once): Finder → **Go → Home** → drag the `Mercor_UC2` folder into the sidebar under **Favorites**, so it is one click on camera
- [ ] **Quit** every app not in the take: Mail, Messages, Slack, Music and so on (app menu → **Quit**)
- [ ] **Control Centre → Focus → Do Not Disturb** on. Charger plugged in
- [ ] **System Settings → Appearance → Dark** · Desktop & Dock → Position on screen: **Left** (different from UC1)
- [ ] **≥ 50 GB free disk** (Apple menu → About This Mac → More Info → Storage)
- [ ] **Finder** window open at `Mercor_UC2/UC2_Propensity_To_Pay_vN` (newest) → **Window → Fill** (or double-click the title bar). Don't use the green full-screen button: full screen moves the app to its own Space
- [ ] **VS Code → File → Open Folder…** → **Mercor_UC2** (sidebar) → **UC2_Propensity_To_Pay_vN** → **Open** → trust it if asked → off camera, open `Deliverables/2_Code/01_data_preprocessing.ipynb` and check the top-right kernel shows **Python 3.12 (ds-venv)**, then close the notebook → in the Explorer panel click **Task Notes.md** (formatted preview) → **Window → Fill**
- [ ] Firefox, LibreOffice Calc and Impress **closed** · headset on · this script open on the second laptop

### Mac Part 3: start TaskRecorder

▶ **DO**
1. Open **TaskRecorder** → check you're signed in with the **Mercor OTA** account and Accessibility, Screen Recording and Microphone are green
2. Start the recording for this task as described in the Mercor TaskRecorder guide
3. Click VS Code so the task notes are in front. **Wait 3 seconds in silence.** Start Scene 1

### Mac Part 5: stop, package, upload

▶ **DO**
1. Stop TaskRecorder. Note where it saved **video.mp4** and **recording_TIMESTAMP.zip**. Don't open, rename or change the zip
2. Watch the video and check the screenshot count (as in the Mercor guide)
3. Open Terminal again (off camera):
   ```bash
   cd ~/LLM_Training_recording
   bash prep/package_deliverables.sh UC2
   ```
   ✔ ends with **READY TO UPLOAD** and creates `Deliverables.zip` inside the newest `~/Mercor_UC2/UC2_Propensity_To_Pay_vN` folder. If it says **NOT READY**, fix what it lists and run it again
4. **Metadata.rtf** is in the same `UC2_Propensity_To_Pay_vN` folder (hidden in VS Code on purpose). Check that its App Topology matches what you actually did
5. Mercor Studio: upload **video.mp4**, the unmodified **recording_TIMESTAMP.zip**, **Deliverables.zip** and **Metadata.rtf** → run **both** AutoQC checks → fix or dispute every flag → submit

### Mac differences inside Part 4

| Script says | On the Mac |
|---|---|
| File Explorer | **Finder** (`Mercor_UC2` in the sidebar → `UC2_Propensity_To_Pay_vN`) |
| right-click → Open with | **Control-click** (or two-finger click) → **Open With** |
| taskbar | **Dock** |
| maximise | **Window → Fill** (or double-click the title bar), not the green full-screen button |
| Minimise | yellow button (top left) or **Window → Minimise** |
| Close an app (X) | app menu → **Quit** (for example **Firefox → Quit Firefox**) |
| `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN\...` | `~/Mercor_UC2/UC2_Propensity_To_Pay_vN/...`. In a LibreOffice **Save As** dialog, click `Mercor_UC2` in the sidebar (click the **⌄** arrow next to the file name first if the dialog is compact) |
| status bar right-click (CountA) | **Control-click** the status bar |
| Ctrl+C / Ctrl+V | Cmd+C / Cmd+V |

LibreOffice menus (Insert, Format, File, Data) are in the **top menu bar** of the screen on the Mac, not inside the window. Everything else (VS Code Run All, Restart, File → Save, Calc pivot dialogs, Impress Insert → Image…) is identical.

---

## PART 1 (Windows practice): The day before

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

## PART 2 (Windows practice): 30 minutes before

- [ ] `prep\stage_recording.cmd UC2` → a fresh, new `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN` folder (v1, v2, v3…; path printed at the end). Always use the **newest** one
- [ ] Quit Outlook, Slack and chat apps · Teams status **Do not disturb** · Windows **Do not disturb ON**
- [ ] Browser closed · Windows Update paused · charger in
- [ ] Settings → Personalization → Colors → **Dark** mode
- [ ] File Explorer at `Cnx\Mercor_UC2\UC2_Propensity_To_Pay_vN` (newest), maximised
- [ ] **VS Code** → **File → Open Folder…** → `Cnx` → `Mercor_UC2` → **UC2_Propensity_To_Pay_vN** (newest) → trust → click **Task Notes.md** (formatted preview) → maximised, on top
- [ ] Firefox, LibreOffice Calc and Impress closed · headset on · Teams test call

## PART 3 (Windows practice): Start the Teams recording

1. Teams → **Calendar → Meet now** → `UC2 practice` → **Start meeting** → camera **off**, mic **on** → **Join now** → close "Invite people"
2. **Share → Screen** (main display) → drag the floating Teams window to the **bottom-right corner**
3. Sharing toolbar → **More (…) → Record and transcribe → Start recording** → click VS Code → wait 3 s → Scene 1

---

## PART 4 (Windows and Mac): The script (~38 minutes)

**Rules:** name what you click before clicking it · hover, click, pause about 1 s · one action at a time · menus and mouse, not shortcuts · trace text with the cursor · never "this" or "here" without naming it.

---

### Scene 1 · Task notes (0:00–1:00), VS Code

▶ **DO** VS Code is in front showing the **Task Notes** preview.

🎙 **SAY** (cursor under each line)
> "Hi, I'm a senior data scientist. Today's request comes from our Head of Collections Strategy.
> In plain words: which late payers should our agents call? Many customers pay on their own anyway, so we want the calls to go where the most money is at risk of staying unpaid.
> Every month about three and a half thousand accounts fall behind: credit cards, personal loans and buy-now-pay-later. Our twenty-five agents can work about thirty-seven percent of them. Today they just call the most overdue accounts first.
> Fewer accounts pay every month, and we're missing target. So they want a propensity-to-pay model. And a June work list that sends the agents to where the unpaid money really is.
> I've built a pipeline for this: one config file and four notebooks. Today I'll walk you through it. And I'll run it end to end on the full extract for the first time.
> My plan. Read the brief and the dictionary. Explore the data in LibreOffice Calc. Run my pipeline, and fix anything the first run shows. Test it on a later month. Then build the June list. I'm done when the criteria at the bottom are met."

▶ **DO** Minimise VS Code.

---

### Scene 2 · The brief (1:00–2:30), File Explorer → Firefox

🎙 **SAY** "Inside Deliverables there are four folders: Input, Code, Intermediate and Output."

▶ **DO** **Deliverables → 1_Input →** right-click **input 3 - collections strategy brief.pdf → Open with → Firefox** (Mac: **Open With → Firefox**) → maximise. Scroll down slowly with the mouse wheel as you talk.

🎙 **SAY** (hover over each item)
> "Twenty-five agents can work about thirteen hundred accounts a month. That's about thirty-seven percent. The rest get an SMS or an app reminder.
> The most important rule: accounts are ranked on **day seven** after they fall behind. Anything from the first seven days, like calls or a promise to pay, can be used. Anything later can't. That's my leakage rule.
> The model will run on future months. So it must be tested on later months than it trained on. Train on January to April. Test on May and June.
> The probabilities are used to estimate money lost. So they must be calibrated, not just in the right order.
> Accounts with an open dispute or a hardship flag always go to a specialist team. So they're not on the agent list.
> The acceptance criteria. ROC-AUC of at least 0.78 on a later month. Cover more unpaid money than today's rule, most overdue first, with the same capacity. Beat a logistic baseline on PR-AUC. And check and correct the calibration."

▶ **DO** Close Firefox (Mac: **Firefox → Quit Firefox**).

---

### Scene 3 · Data dictionary (2:30–4:00), LibreOffice Calc

▶ **DO** Double-click **input 2 - data dictionary.xlsx**. It opens in **LibreOffice Calc**; if another app opens it, right-click → **Open with → LibreOffice Calc**. Maximise.

🎙 **SAY** (trace the **Notes** column, then stop on each row named)
> "The key column is Notes. Three fields say 'Refreshed at extract': `account_status_at_extract`, `amount_recovered_30d` and `total_contact_attempts_30d`. The extract is from the fifteenth of August. That's long after day seven. So all three could leak.
> The status and the recovered amount are obvious. They *are* the outcome. Total contact attempts is harder to spot. It says 'for this episode'. So it covers all thirty days, not just the first seven.
> But `contact_attempts_7d`, `right_party_contact_7d` and `promise_to_pay_7d` only cover the first seven days. So they're allowed.
> The dictionary also gives two business rules. Days past due must be between 1 and 90. And the amount due can't be more than the balance."

▶ **DO** **File → Close** → **Don't Save**.

---

### Scene 4 · Exploring the raw data with pivot tables (4:00–10:30), LibreOffice Calc → artifact 1

▶ **DO** Right-click **input 1 - collections accounts.csv** → **Open with → LibreOffice Calc** → Text Import: **Unicode (UTF-8)**, separated by **Comma** only → **OK** → maximise. Click the **column A header**, then right-click the number in the status bar (bottom right) and tick **CountA**.

✔ **CHECK** status bar **CountA: 20241**

🎙 **SAY** "Twenty thousand two hundred and forty rows plus the header. But the brief says twenty thousand accounts. So there are duplicates. Let me look at the data with pivot tables."

**How to build each pivot in Calc:** click **A1** on the data sheet → **Insert → Pivot Table… → Current selection → OK** → in the layout dialog drag fields into **Row Fields** and **Data Fields** → double-click a data field to choose **Count** or **Average** → **OK**. Format averages via right-click → **Format Cells… → Numbers → Percent**, 1 decimal. Rename a sheet via right-click on its tab → **Rename Sheet…**.

**Pivot 1: products**

▶ **DO** **product_type** → Row Fields · **account_id** → Data Fields (**Count**) · **paid_within_30d** → Data Fields (**Average**, Percent). Rename the sheet `Products`.

✔ **CHECK** Items like **BNPL**, **Buy Now Pay Later**, **CC**, **credit_card**, **Credit Card**, **Personal Loan**, **Personal-Loan**, **PL** (and possibly case variants such as **CREDIT CARD**). BNPL about 34% paid; cards and loans about 46%.

🎙 **SAY**
> "Three products, but many spellings: 'CC', 'credit underscore card', 'PL', 'Buy Now Pay Later'. The pipeline must map them all to three products.
> And buy-now-pay-later customers pay less often. About thirty-four percent, against forty-six for cards and loans."

**Pivot 2: employment**

▶ **DO** **employment_status** → Row Fields · **account_id** → Count · **paid_within_30d** → Average (Percent). Rename `Employment`.

✔ **CHECK** `(empty)`, `N/A` and `Unknown` rows · Unemployed ≈ 19.6% · Salaried ≈ 48.3% · Student ≈ 31.2%

🎙 **SAY**
> "Three different placeholders mean the same thing: empty, N/A and Unknown. About twelve hundred accounts in total. They should be one group.
> And employment matters a lot. Unemployed customers pay less than twenty percent of the time. Salaried customers about forty-eight."

**Pivot 3: leakage check**

▶ **DO** **account_status_at_extract** → Row Fields · **paid_within_30d** → Average (Percent) · **account_id** → Count. Rename `Leakage check`.

✔ **CHECK** Current 100% · Settled 100% · Delinquent / Charged-Off / Payment Plan 0%

🎙 **SAY**
> "Exactly a hundred percent or zero percent. This doesn't predict the outcome. It *is* the outcome, recorded later. The model must never see it."

**Pivot 4: payment history**

▶ **DO** **num_prior_delinquencies_12m** → Row Fields · **paid_within_30d** → Average (Percent) · **account_id** → Count. Rename `Payment history`.

✔ **CHECK** 0 → 53.5% · 1 → 41.9% · 2 → 30.6% · 3 → 20.7%

🎙 **SAY**
> "A clear pattern. With no earlier late payments, fifty-three percent pay. With three or more, about twenty percent. Payment history will be a strong driver."

*(Optional: **promise_to_pay_7d** → 67.3% vs 38.1%. "A promise in the first week is legitimate information at day seven, and a strong one.")*

▶ **DO** **File → Save As…** → `Deliverables\3_Intermediate` → **File type: Excel 2007-365 (.xlsx)** → `artifact 1 - exploratory pivot analysis` → **Save** → **Use Excel 2007-365!** → **File → Close**.

🎙 **SAY** "Saved as artifact one in Intermediate."

---

### Scene 5 · My pipeline (10:30–12:00), VS Code

▶ **DO** Click **VS Code** in the taskbar (Mac: Dock) → maximise. Expand **Deliverables** and its four folders. Open **2_Code → pipeline_config.py**. Go down the file one block at a time. Each block starts with a `# ----` line.

#### Top of the file

🎙 "Back in VS Code. This is the pipeline I built. One config file and four notebooks: preprocessing, training, testing, and the work list with packaging."

#### `# ---- business rules`

🎙 "The business rules from the brief. We score on day seven. The agents can work thirty-seven percent of the accounts. And the time windows: train on months one to four, calibrate on month five, test on month six."

#### `# ---- columns`

🎙 "The leaky columns. I've put the account status and the recovered amount here. I noted a third suspect in the dictionary, so I'll watch for it. Dispute and hardship stay as model inputs. But those accounts go to the specialist team."

#### `# ---- helpers` and `# ---- models`

🎙 "A small helper to read dates. And the two models: a logistic regression baseline, and gradient boosting. This is the first run on the full extract. So let's run it and check every result."

---

### How to run a notebook, cell by cell (Scenes 6–9)

- Code cells are numbered **[1], [2], [3]…** here, from the top. Headings don't count. After **Restart → Run All**, VS Code shows the same number to the left of each cell.
- To run one cell, click the **▶ Run** button on the left of that cell. Wait for the output. Then say the line.
- ✖ means you should see an error or a wrong number in that cell. That's a planted bug: follow the 🔧 **FIX** under it.
- After every fix: **Restart → Run All** (notebook toolbar). Run All runs every cell from the top, so the cells after the fix already have their output. For those, just click the cell, hover over its output and say the line.

---

### Scene 6 · Notebook 01, preprocessing (12:00–17:00): fix P1 and P2

▶ **DO** Open **01_data_preprocessing.ipynb** → confirm the kernel **Python 3.12 (ds-venv)** at the top right.

🎙 **SAY** "Notebook one cleans the raw extract. I'll run it one cell at a time."

#### [1] `import matplotlib.pyplot as plt` → ▶

✔ No output.

🎙 "The imports and the shared config. Every cleaning step is written to a log."

#### [2] Section 1 · `raw = pd.read_csv(cfg.RAW_FILE)` → ▶

✔ `20,240 rows x 30 columns | unique accounts: 20,000` · `Paid within 30 days: 43.4%`

🎙 "Twenty thousand two hundred and forty rows, but twenty thousand accounts. Forty-three percent paid within thirty days."

#### [3] `missing = raw.isna()…` → ▶

✔ Bar chart: missing values

🎙 "Missing values. Utilisation is blank for thirty percent. Those are personal loans. They have no credit limit, so this is expected, not an error. Income is missing for ten percent, employment for four."

#### [4] `raw[[…]].describe()…` → ▶

✔ days_past_due min **-5** max **999** · utilization_ratio max **9.99** · monthly_income min **0**

🎙 "Some values are impossible. Days past due of minus five, and nine hundred and ninety-nine. A utilisation of 9.99. And a monthly income of zero."

#### [5] Section 2 · `df = raw.copy()` → ▶

✔ `exact duplicates 240 rows` · `20,000 accounts`

🎙 "Two hundred and forty exact duplicates are removed."

#### [6] Section 3 · `df["delinquency_date"] = pd.to_datetime(…, format="mixed")` → ▶ ✖ **P1**

✔ Month counts that include 7–12, then `AssertionError: cohort months outside Jan-Jun: [7, 8, 9, 10, 11, 12]`

🎙 "The extract only covers January to June. But the dates include July to December. I used format 'mixed' here, and it guesses each date. A day-first date like nine, slash, three becomes the third of September. Worse, five, slash, three becomes the third of May. That's inside the range, so nothing would flag it. The account would land in the wrong month of my time split. My config has a `parse_dates` helper. It reads both formats clearly. I'll use it instead of guessing."

▶ **DO** Click the **pipeline_config.py** tab → hover over the `parse_dates` function → back to the notebook.

🔧 **FIX P1** In cell [6], change the **right-hand side** of this one line:
```python
df["delinquency_date"] = pd.to_datetime(df["delinquency_date"], format="mixed")
```
to:
```python
df["delinquency_date"] = cfg.parse_dates(df["delinquency_date"])
```

▶ **DO** **Restart → Run All**.

✔ Cell [6] shows `delinquency_date: 19,600 ISO dates + 400 day-first dates` and months 1–6 only. The run stops at cell [10] (next bug).

🎙 "The dates are fixed. Nineteen thousand six hundred normal dates and four hundred day-first dates."

#### [7] `by_month = …` (chart, already run: click it, hover)

🎙 "Every account is now in January to June. And more accounts come in as the year goes on."

#### [8] Section 4 · `PRODUCT_FIXES = …`

✔ `product labels 700 rows` · `employment placeholders 1,200 rows`

🎙 "Seven hundred product labels are mapped to three products. Twelve hundred employment placeholders are merged into 'Unknown'."

#### [9] Section 5 · `bad_dpd = …`

✔ `80 rows -> removed` · `100 rows -> removed` · `42 rows -> set to missing` · `19,820 accounts remain`

🎙 "The business rules from the dictionary. Eighty accounts have days past due outside one to ninety. A hundred have an amount due bigger than the balance. Both are removed. Forty-two fake utilisations are set to missing. That leaves nineteen thousand eight hundred and twenty accounts."

#### [10] Section 6 · income and affordability ✖ **P2**

✔ Red error: `AssertionError: infinite payment_burden for 100 accounts`

🎙 "Payment burden is the amount due divided by income. It's infinite for a hundred accounts. The profile showed an income of zero. Here zero means 'not provided', not a real income of nothing. So zeros must become missing before we divide."

🔧 **FIX P2** In cell [10], add this as the **first line** of the cell:
```python
df["monthly_income"] = df["monthly_income"].replace(0, np.nan)
```

▶ **DO** **Restart → Run All**.

✔ It runs to the end: `Saved 19,820 rows -> artifact 2 - cleaned accounts.csv`

**All cells have run now. For each cell below: click it, hover over the output, say the line.**

#### [10] Section 6 (fixed)

✔ `monthly_income missing 2,068 rows -> flag; burden left missing` · median (50%) **0.059**

🎙 "Now it works. The typical payment burden is about six percent of monthly income."

#### [11] `bands = pd.cut(…)` (affordability chart)

🎙 "This chart is striking. Up to twenty percent of income, around forty-five percent of accounts pay. Above thirty-five percent, in orange, almost nobody pays. It's a cliff, not a slope. A tree model handles that. A straight line doesn't."

#### [12] Section 7 · save

✔ `Saved 19,820 rows -> artifact 2 …` · `Saved 7 log entries -> artifact 3 …`

🎙 "The clean data is saved as artifact two."

#### [13] `steps = …` (chart)

🎙 "The last chart shows every cleaning step and how many rows it touched. Everything is logged in artifact three."

---

### Scene 7 · Notebook 02, training (17:00–22:30): fix T1 and T2

▶ **DO** Open **02_model_training.ipynb**.

🎙 **SAY** "Notebook two sets up the time split. It trains both models, checks them on May, and shows what drives the model. One cell at a time."

#### [1] `import joblib` → ▶

✔ `19,820 accounts | 26 features` · `Excluded: [...]`

🎙 "Nineteen thousand eight hundred and twenty accounts. The Excluded line shows the IDs, dates, the two leaky columns and the target."

#### [2] Section 1 · `by_month = …` → ▶

✔ Table and bar chart: pay rate **0.495** in month 1 down to **0.369** in month 6

🎙 "The pay rate falls every month. About fifty percent in January, thirty-seven in June. That's why a random split would mislead us. And why calibration matters."

#### [3] Section 2 · `train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]` → ▶ ✖ **T1**

✔ Red error: `AssertionError: train and calibration windows overlap`

🎙 "The split fails. Training and calibration overlap. My filter says 'month less than or equal to the calibration month'. So May is in both. It's an off-by-one. The config already lists the training months, so I'll use them."

🔧 **FIX T1** In cell [3], change:
```python
train_df = df[df["cohort_month"] <= cfg.CALIBRATION_MONTH]
```
to:
```python
train_df = df[df["cohort_month"].isin(cfg.TRAIN_MONTHS)]
```

▶ **DO** **Restart → Run All**.

✔ Cell [3]: train `[1, 2, 3, 4]` 12,491 (46.0%) · calibrate `[5]` 3,677 (40.5%) · test `[6]` 3,652 (36.9%)

🎙 "The windows are clean now. Months one to four for training, May for calibration, June for the test."

#### [4] Section 3 · train and validate on May (already run: click it, hover)

✔ May ROC-AUC **≈ 0.91** ✖ **T2** (too good)

🎙 "But the May ROC-AUC is 0.91. That's very high for collections."

#### [5] and [6] Section 4 · importance table and chart

✔ Top feature **total_contact_attempts_30d ≈ 0.177**, three times the next one (orange bar)

🎙 "The importance chart explains it. The orange bar, `total_contact_attempts_30d`, costs 0.18 of AUC when shuffled. That's three times anything else. It's the third suspect from the dictionary. It counts calls over the whole thirty days. Customers who pay stop being called. So few calls *means* they paid. On day seven we can't know that."

🔧 **FIX T2** Open **pipeline_config.py** and change:
```python
LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d"]   # captured after the day-7 decision point
```
to:
```python
LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d", "total_contact_attempts_30d"]   # captured after the day-7 decision point
```

▶ **DO** **File → Save** → **02_model_training.ipynb** tab → **Restart → Run All**.

**All cells have run now. Scroll back to the top. For each cell: click it, hover over the output, say the line.**

#### [1] `import joblib`

✔ `25 features` · `Excluded:` now has `total_contact_attempts_30d`

🎙 "Now all three leaky columns are excluded."

#### [4] Section 3 · May results

✔ baseline **0.821 / 0.752** · gradient_boosting **0.844 / 0.784**

🎙 "Now it's realistic. On May, gradient boosting gets 0.84. Logistic regression gets 0.82. Boosting also has the better PR-AUC."

#### [5] and [6] Section 4 · importance

✔ Top: on_time_payment_ratio_12m, promise_to_pay_7d, days_past_due, payment_burden, right_party_contact_7d

🎙 "The importance is now spread across sensible drivers. On-time payment history. A promise to pay in the first week. Days past due. Payment burden. And whether an agent actually reached the customer."

#### [7] Section 5 · save

✔ `saved baseline_logreg.joblib` · `saved gradient_boosting.joblib`

🎙 "Both models are saved as artifact five."

---

### Scene 8 · Notebook 03, testing on June (22:30–27:30): fix E1

▶ **DO** Open **03_model_testing.ipynb**.

🎙 **SAY** "Notebook three tests on June. No model has seen June. One cell at a time."

#### [1] `import joblib` → ▶

✔ `June test cohort: 3,652 accounts, pay rate 36.9%`

🎙 "Three thousand six hundred and fifty-two June accounts. Only thirty-seven percent paid."

#### [2] Section 1 · June metrics → ▶

✔ gradient_boosting **0.825 / 0.732 / 0.173** · baseline **0.818 / 0.724**

🎙 "Gradient boosting gets a ROC-AUC of 0.825. The target is 0.78. It also beats the baseline on PR-AUC."

#### [3] Section 2 · calibration → ▶

✔ raw **0.4566** · calibrated **0.3998** · actual **0.3694** · Brier **0.1727 → 0.1649** · calibration chart

🎙 "Calibration is the big one. The raw model predicts a 45.7 percent pay rate. Only 36.9 percent actually paid. It learned from better months. It would over-promise collections by nearly a quarter. Calibrating on May brings it down to forty percent. The Brier score improves. The rest of the gap is because June is worse than May. That's why the README says to re-calibrate every month. In the chart, the calibrated curve is much closer to the diagonal."

#### [4] Section 3 · agent prioritisation → ▶ ✖ **E1** (no error, wrong result)

✔ `capacity 1,351 of 3,652 June accounts | eligible 3,264` · today's rule **47.1%** · model **45.4%**

🎙 "The model's list covers *less* unpaid money than today's rule. But its AUC is good. That doesn't add up. So the problem is in how the list is ranked."

▶ **DO** Hover over the `expected_unpaid` line in cell [4].

🎙 "Here. Expected unpaid is the chance of paying, times the amount due. That puts the accounts most *likely to pay* at the top. The opposite of what we want. Expected unpaid is *one minus* the chance of paying, times the amount. Notebook four already uses one minus p. I got it backwards here."

🔧 **FIX E1** In cell [4], change:
```python
test_df["expected_unpaid"] = test_df["p_pay"] * test_df["amount_due"]
```
to:
```python
test_df["expected_unpaid"] = (1 - test_df["p_pay"]) * test_df["amount_due"]
```

▶ **DO** **Restart → Run All**.

**All cells have run now. For each cell below: click it, hover over the output, say the line.**

#### [4] Section 3 · agent prioritisation (fixed)

✔ today's rule **47.1%** · model **81.4%**

🎙 "The agents can work thirteen hundred and fifty-one of the three thousand six hundred and fifty-two June accounts. Today's rule, most overdue first, covers forty-seven percent of the unpaid money. The model's list covers eighty-one percent. Same agents, same number of calls."

#### [5] Section 4 · SHAP summary chart

▶ **DO** Hover over each row as you name it.

🎙 "What drives payment. On-time payment history is at the top. Then days past due. Cure rates collapse after thirty days. Then whether an agent reached the customer, and whether they promised to pay in the first week. A promise is worth much less from someone who broke promises before. And payment burden."

#### [6] SHAP dependence charts (three panels)

▶ **DO** Hover over each panel.

🎙 "These show the shape of each effect. Above the grey line means more likely to pay.  
Days past due: flat for the first month, then falling fast after about thirty-five days. Every day counts once an account passes a month.  
Payment burden: fine up to about a third of income, then a cliff.  
On-time payment ratio: below about fifty percent, customers rarely pay. Above it, the chance rises steadily."

#### [7] Section 5 · acceptance table

✔ All four checks **True**

🎙 "All four acceptance checks pass. Artifacts six and seven are saved."

---

### Scene 9 · Notebook 04, work list and package (27:30–29:30)

▶ **DO** Open **04_worklist_and_package.ipynb**.

🎙 **SAY** "Notebook four builds the real June list. One cell at a time."

#### [1] `import json` → ▶

✔ `June cohort: 3,652 accounts`

🎙 "It loads the three thousand six hundred and fifty-two June accounts, the model and the calibrator."

#### [2] Section 1 · score and rank → ▶

✔ `agent capacity 1,351 | routed to specialist team (dispute / hardship): 388` · `saved 1,351 accounts -> artifact 8 …`

🎙 "Every account is scored with the calibrated model. Three hundred and eighty-eight accounts have a dispute or hardship flag. They go to the specialist team. The rest are ranked by expected unpaid amount: one minus the chance of paying, times the amount due. The list is cut at thirteen hundred and fifty-one. That's artifact eight."

#### [3] Section 2 · what the list achieves → ▶

✔ coverage_model **0.814** · coverage_dpd_rule **0.471**

🎙 "We know June's results, so I can check it. The list covers eighty-one percent of the unpaid money. The old rule covers forty-seven percent."

#### [4] Histogram → ▶

🎙 "This chart shows why. The old rule, in grey, only calls accounts more than twenty days past due. The model, in blue, also calls high-risk accounts in their first three weeks, while there's still time. And it skips overdue accounts that will probably pay anyway."

#### [5] Section 3 · package → ▶

✔ `saved model.joblib, calibrator.joblib and metrics.json`

🎙 "The model and the calibrator are saved with their metrics."

#### [6] README → ▶

▶ **DO** Scroll through the printed README.

🎙 "And a README. This is final output three."

---

### Scene 10 · Validating the work list in LibreOffice Calc (29:30–32:30) → final output 1

▶ **DO** File Explorer → `Deliverables\3_Intermediate` → right-click **artifact 8 - june agent work list.csv** → **Open with → LibreOffice Calc** → Text Import: **Comma** → **OK** → maximise.

🎙 **SAY** "Before handing this to the team leads, I'll validate it independently."

▶ **DO** Columns **M** and **N** are empty: you build a small summary table there. Column **M** is text labels you type yourself (they are *not* data columns); column **N** is formulas on the data columns (A = `priority`, E = `amount_due`, F = `p_pay`, G = `expected_unpaid`, I = `has_open_dispute`, J = `hardship_flag`, K = `actual_paid`). Every row in this file is one account on the agent list, so counting column A counts the accounts. Click **M1**, type the label, click **N1**, type the formula, and so on down:

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
> "Thirteen hundred and fifty-one accounts. Exactly the capacity. Five hundred and thirty-two thousand dollars due in total.
> Each account's expected unpaid amount is the chance it won't pay, times the amount due. Adding them up gives the money the model expects to stay unpaid: about three hundred and seventy-eight thousand dollars. Three hundred and ninety-three thousand really stayed unpaid. That's within about four percent. So the calibration works: when the model says a forty percent chance of paying, about forty percent really pay. Finance can use these numbers to forecast cash, not just to rank accounts.
> Only three hundred and fifty-four of these accounts paid on their own. So the agents are calling the right people.
> The list covers eighty-one percent of the unpaid money in June. The old rule covers forty-seven percent.
> And no dispute or hardship account is on the list."

▶ **DO** **File → Save As…** → `Deliverables\4_Output` → **File type: Excel 2007-365 (.xlsx)** → `final output 1 - june agent work list` → **Save** → **Use Excel 2007-365!** → **File → Close**.

---

### Scene 11 · Summary deck (32:30–36:30), LibreOffice Impress → final output 2

▶ **DO** `1_Input` → right-click **input 4 - summary deck template.pptx** → **Open with → LibreOffice Impress** → **File → Save As…** → `4_Output` → **File type: PowerPoint 2007-365 (.pptx)** → `final output 2 - collections summary` → **Save** → **Use PowerPoint 2007-365!**.

🎙 **SAY** "First I save my own copy to Output, so the template stays clean. Then I fill in the orange brackets."

▶ **DO** For each orange `[   ]`: double-click into the text → select the **whole** `[   ]`, brackets included → type just the number (units are in the labels) → select it → **Properties** sidebar → **Character → Font Color** arrow → **Automatic** (or **Format → Character… → Font Effects**).

**Slide 2:** `[ ]` accounts removed → **420**

🎙 "Four hundred and twenty accounts removed: duplicates and business-rule violations."

**Slide 3:** ROC-AUC → **0.825** · PR-AUC → **0.732** vs **0.724** · pay rate (%) → **45.7** → **40.0** vs **36.9** · click the **border of the dashed box** → **Delete** → **Insert → Image…** → `3_Intermediate\artifact 7 - charts\07_calibration.png` → **Open** → fit it on the right.

🎙 "Out of time, 0.825 ROC-AUC. And the calibration chart shows why recalibration matters: raw predictions overstate payment."

**Slide 4:** Unpaid covered (%) → **81** vs **47** · Accounts → **1,351** of **3,652** · Specialist → **388**
- The three drivers on the right are already written in the template (from the SHAP results): just hover over each one as you mention it

🎙 **SAY**
> "The model's list covers eighty-one percent of the unpaid money. The old rule covers forty-seven. Same thirteen hundred and fifty-one agent slots. Three hundred and eighty-eight accounts go straight to the specialist team.
> My recommendation. Give agents the top thirty-seven percent by expected unpaid amount. Send the rest an SMS or app reminder. Re-calibrate every month, because pay rates keep falling. And compare against the old rule every month."

▶ **DO** **File → Save** → **Use PowerPoint 2007-365!** → **File → Close**.

---

### Scene 12 · Wrap-up (36:30–38:00), File Explorer

▶ **DO** Open `Deliverables` and hover over each folder and file.

🎙 **SAY**
> "To wrap up. Input has the four files I received. Plus my pipeline code as it was before this run, delivered as input five. Code is now the corrected pipeline, delivered as final output four. Intermediate has the pivot analysis, clean accounts, quality log, time split, models and calibrator, the model comparison, charts and the June work list. Output has the checked work list, the summary deck and the packaged model.
> I fixed five issues. A date parser that quietly put accounts in the wrong month. Zero incomes that broke the payment burden. A training window that overlapped the calibration month. A call count that leaked the answer. And a ranking that put the customers most likely to pay at the top.
> Every acceptance criterion is met. The June list is ready for the team leads. Thank you."

▶ **DO** Stay silent for 3 seconds.

---

## PART 5 (Windows practice): Stop, package, send

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

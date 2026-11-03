# UC1 Cross-Sell: Complete Recording Script

**Open this on your second laptop and follow it from top to bottom.** Everything is here: setup, what to open, what to click, what to say, every code fix, and the numbers you should see. Nothing from this file is ever shown on the recording screen.

**How to read it**

| Marker | Meaning |
|---|---|
| ▶ **DO** | What to click or open on the recording laptop |
| 🎙 **SAY** | What to say. Speak naturally; you don't have to be word-perfect |
| ✔ **CHECK** | What you should see. If it's different, see Emergency at the end |
| 🔧 **FIX** | Code to change, exactly as written |

**Apps on camera** (the same for the Windows practice and the Mac): **VS Code · Firefox · LibreOffice Calc · LibreOffice Impress · File Explorer** (Mac: **Finder**). Microsoft Office is not used because the Mac doesn't have it. On the Mac, `Ctrl` → `Cmd`.

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
   .venv/bin/python prep/selftest_uc1.py
   ```
   ✔ setup ends with **READY**; the self-test ends with **SELF-TEST PASSED**. Python 3.12 must be installed first from python.org (see README section 2). You have admin access, so expect a password prompt for the Python installer, and a one-time "install the command line developer tools" prompt the first time you run `git` (click **Install**, then re-run the command).
2. **VS Code:** only the **Python** and **Jupyter** extensions (Microsoft). No Copilot or AI extensions. **Code → Settings → Settings** → search "disable AI features" → tick it.
3. **Open Firefox, LibreOffice Calc and LibreOffice Impress once each**, click **Open** if macOS asks about an app downloaded from the internet, and dismiss every first-run pop-up (LibreOffice: close "Tip of the Day" and untick "Show tips on startup"). Then quit them (app menu → **Quit**).
4. **Default apps** so "Open With" is predictable. In Finder, for one file of each type in `~/LLM_Training_recording/recording_workspace/UC1_Cross_Sell/Deliverables/1_Input`: select it → **File → Get Info** → **Open with:** choose the app → **Change All…** → **Continue**.
   - `.pdf` → **Firefox**
   - `.csv` and `.xlsx` → **LibreOffice** (Calc)
   - `.pptx` → **LibreOffice** (Impress)
5. **Mercor setup:** complete section A of `use_cases/Recording_Checklist.md`: TaskRecorder installed and signed in with the **Mercor OTA** account, permissions green, Accessibility Inspector minimised in the Dock, Insightful running, clock with seconds.
6. **Rehearse the whole of PART 4 once, out loud, with a stopwatch** (not recorded). Then reset with `bash prep/stage_recording.sh UC1`.

### Mac Part 2: 30 minutes before the take

▶ **DO**
- [ ] Terminal:
  ```bash
  cd ~/LLM_Training_recording
  bash prep/stage_recording.sh UC1
  ```
  → a fresh, new `~/Mercor_UC1/UC1_Cross_Sell_vN` folder (the full path is printed). Always use the **newest** one. Then **Terminal → Quit Terminal**
- [ ] **Finder sidebar** (once): Finder → **Go → Home** → drag the `Mercor_UC1` folder into the sidebar under **Favorites**, so it is one click on camera
- [ ] **Quit** every app not in the take: Mail, Messages, Slack, Music and so on (app menu → **Quit**)
- [ ] **Control Centre → Focus → Do Not Disturb** on. Charger plugged in
- [ ] **System Settings → Appearance → Light** · Dock at the bottom
- [ ] **≥ 50 GB free disk** (Apple menu → About This Mac → More Info → Storage)
- [ ] **Finder** window open at `Mercor_UC1/UC1_Cross_Sell_vN` (newest) → **Window → Fill** (or double-click the title bar). Don't use the green full-screen button: full screen moves the app to its own Space
- [ ] **VS Code → File → Open Folder…** → **Mercor_UC1** (sidebar) → **UC1_Cross_Sell_vN** → **Open** → trust it if asked → off camera, open `Deliverables/2_Code/01_data_preprocessing.ipynb` and check the top-right kernel shows **Python 3.12 (ds-venv)**, then close the notebook → in the Explorer panel click **Task Notes.md** (formatted preview) → **Window → Fill**
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
   bash prep/package_deliverables.sh UC1
   ```
   ✔ ends with **READY TO UPLOAD** and creates `Deliverables.zip` inside the newest `~/Mercor_UC1/UC1_Cross_Sell_vN` folder. If it says **NOT READY**, fix what it lists and run it again
4. **Metadata.rtf** is in the same `UC1_Cross_Sell_vN` folder (hidden in VS Code on purpose). Check that its App Topology matches what you actually did
5. Mercor Studio: upload **video.mp4**, the unmodified **recording_TIMESTAMP.zip**, **Deliverables.zip** and **Metadata.rtf** → run **both** AutoQC checks → fix or dispute every flag → submit

### Mac differences inside Part 4

| Script says | On the Mac |
|---|---|
| File Explorer | **Finder** (`Mercor_UC1` in the sidebar → `UC1_Cross_Sell_vN`) |
| right-click → Open with | **Control-click** (or two-finger click) → **Open With** |
| taskbar | **Dock** |
| maximise | **Window → Fill** (or double-click the title bar), not the green full-screen button |
| Minimise | yellow button (top left) or **Window → Minimise** |
| Close an app (X) | app menu → **Quit** (for example **Firefox → Quit Firefox**) |
| `Cnx\Mercor_UC1\UC1_Cross_Sell_vN\...` | `~/Mercor_UC1/UC1_Cross_Sell_vN/...`. In a LibreOffice **Save As** dialog, click `Mercor_UC1` in the sidebar (click the **⌄** arrow next to the file name first if the dialog is compact) |
| status bar right-click (CountA) | **Control-click** the status bar |
| Ctrl+C / Ctrl+V | Cmd+C / Cmd+V |

LibreOffice menus (Insert, Format, File, Data) are in the **top menu bar** of the screen on the Mac, not inside the window. Everything else (VS Code Run All, Restart, File → Save, Calc pivot dialogs, Impress Insert → Image…) is identical.

---

## PART 1 (Windows practice): The day before (setup and rehearsal)

1. On the recording laptop, in PowerShell:
   ```powershell
   cd C:\Users\ullas.kc\Cnx\LLM_Training_recording      # your project folder
   git pull
   .\setup_windows.cmd
   .\.venv\Scripts\python.exe prep\selftest_uc1.py
   ```
   ✔ setup ends with **READY**; the self-test ends with **SELF-TEST PASSED**.
2. VS Code: only the **Python** and **Jupyter** extensions. Copilot disabled. Settings → search "disable AI features" → ticked. Restart VS Code.
3. **Windows practice only:** install **Firefox** (firefox.com) and **LibreOffice** (libreoffice.org, includes Calc and Impress), both free. On the Mac they're already installed.
   Open Firefox, Calc and Impress once each and dismiss every first-run pop-up (Firefox: skip import and "default browser"; LibreOffice: close "Tip of the Day" and untick "Show tips on startup"), then close them.
4. **Read every line** of the code in `recording_workspace\UC1_Cross_Sell\Deliverables\2_Code` so you can explain any of it.
5. **Rehearse the whole of PART 4 once, out loud, with a stopwatch** (not recorded). Then reset:
   ```powershell
   prep\stage_recording.cmd UC1
   ```
   (This restores the original code with the 5 issues and empties the output folders.)

---

## PART 2 (Windows practice): 30 minutes before the take

▶ **DO**
- [ ] `prep\stage_recording.cmd UC1` → a fresh, new `Cnx\Mercor_UC1\UC1_Cross_Sell_vN` folder (v1 the first time, then v2, v3…; the full path is printed at the end). Always use the **newest** one
- [ ] **Quit** Outlook, Slack, WhatsApp and other chat apps (tray icon → right-click → Quit). Teams stays open.
- [ ] Teams status → **Do not disturb**. Windows Settings → System → Notifications → **Do not disturb ON**
- [ ] Close the browser. Pause Windows Update. Plug in the charger
- [ ] Settings → Personalization → Colors → **Light** mode
- [ ] Open **File Explorer** at `Cnx\Mercor_UC1\UC1_Cross_Sell_vN` (the newest version) and maximise it
- [ ] Open **VS Code** → **File → Open Folder…** → `Cnx` → `Mercor_UC1` → **UC1_Cross_Sell_vN** (newest) → **Select Folder** → trust it if asked → in the Explorer panel click **Task Notes.md** (it opens as a formatted preview) → maximise VS Code
- [ ] Firefox, LibreOffice Calc and Impress **closed**
- [ ] Headset on. Teams → Settings → Devices → **Make a test call**
- [ ] Phone silent, with this script open on the second laptop

---

## PART 3 (Windows practice): Start the Teams recording

▶ **DO**
1. Teams → **Calendar** → **Meet now** → name it `UC1 practice` → **Start meeting**
2. Camera **OFF**, microphone **ON**, headset selected → **Join now** → close the "Invite people" box
3. **Share** (top bar) → **Screen** → your main display (leave "Include sound" off)
4. Drag the small floating Teams window to the **bottom-right corner**
5. Hover over the sharing toolbar at the top → **More (…)** → **Record and transcribe** → **Start recording**
6. Click VS Code so the task notes are in front. **Wait 3 seconds in silence.** Start Scene 1.

---

## PART 4 (Windows and Mac): The script (~38 minutes)

**Rules for every scene:** name what you click *before* clicking it · hover, click, pause about 1 second · one action at a time · use menus and the mouse, not keyboard shortcuts (Ctrl+C / Ctrl+V are fine) · move the cursor under text as you read it · never say "this" or "here" without naming the thing.

---

### Scene 1 · Task notes (0:00–1:00), VS Code

▶ **DO** VS Code is in front showing the **Task Notes** preview. Move the cursor slowly under each line as you talk.

🎙 **SAY**
> "Hi, I'm a senior data scientist. Today's request comes from our Head of CRM and Cross-Sell.
> In plain words: who should we offer a new product to? We have twenty thousand customers, but the budget only covers contacting four thousand, so we want the four thousand most likely to buy.
> Today Marketing picks the four thousand at random. About one in nine buys another product.
> Before they sign off the Q4 budget, they want proof that a model would do better.
> We have a customer snapshot from the thirtieth of June. And we now know who bought a new product between July and September.
> I've built a pipeline for this: one config file and four notebooks. Today I'll walk you through it. And I'll run it end to end on the full snapshot for the first time.
> My plan. Read the brief and the data dictionary. Explore the raw data in LibreOffice Calc. Run my pipeline, and fix anything the first run shows. Then the back-test: which four thousand customers would the model have picked, and how many really bought?
> I'm done when the criteria at the bottom of my notes are met."

▶ **DO** Click VS Code's **Minimise** button (the "–" at the top right; on the Mac, the yellow button at the top left).

---

### Scene 2 · The brief (1:00–2:30), File Explorer → Firefox

▶ **DO** In File Explorer, hover over the folders.

🎙 **SAY**
> "Everything is in the Deliverables folder. It has four folders: Input, Code, Intermediate and Output. Inputs are read-only. The pipeline writes its working files to Intermediate. The final results go to Output."

▶ **DO** Double-click **Deliverables** → double-click **1_Input** → **right-click input 3 - campaign brief.pdf → Open with → Firefox** (Mac: right-click → **Open With → Firefox**) → maximise Firefox.

🎙 **SAY** (hover over each line as you say it)
> "This is the brief from the Head of CRM. It's dated the first of October, so the July-to-September results are complete.
> The budget is four thousand contacts per campaign. Each contact costs four dollars. Each extra product sold earns a hundred and fifty dollars.
> Compliance: we can only contact customers who opted in to marketing. And the model must not use gender.
> Customer care: anyone with two or more complaints in the last twelve months is left out.
> And the model may only use information we had on the snapshot date. That's my rule for spotting leakage."

▶ **DO** Scroll down slowly with the mouse wheel to the acceptance criteria.

🎙 **SAY**
> "They want a back-test. Each customer must be scored by a model that didn't train on them. They also want the drivers in plain language, and a short summary on the team template.
> The acceptance criteria. ROC-AUC of at least 0.78 on a hold-out set. Beat a logistic-regression baseline on PR-AUC. A lift of at least 2.5 in the top twenty percent. And the back-test list must buy at least twice as often as the eligible average."

▶ **DO** Close Firefox (the **X**; on the Mac, **Firefox → Quit Firefox**).

---

### Scene 3 · Data dictionary (2:30–4:00), LibreOffice Calc

▶ **DO** Double-click **input 2 - data dictionary.xlsx**. It opens in **LibreOffice Calc**; if another app opens it, right-click → **Open with → LibreOffice Calc**. Maximise.

🎙 **SAY**
> "The data dictionary lists every column with its source system."

▶ **DO** Move the cursor down the **Source System** column, then stop on the `welcome_pack_sent` row.

🎙 **SAY**
> "Most columns come from core banking, the CRM and the data warehouse. All as of the snapshot date.
> But `welcome_pack_sent` comes from the fulfilment system, and it's updated every day. A welcome pack is sent *after* a customer opens a new product. So this column could leak the answer. I'll test it."

▶ **DO** Hover over `cross_sell_product_type`, then `gender`, then `email_open_rate`.

🎙 **SAY**
> "`cross_sell_product_type` comes from the sales ledger. Also updated every day. Same suspicion.
> `gender` is marked as protected. The brief excludes it.
> And `email_open_rate` is only tracked when emails were sent. So I expect it to be blank for customers who opted out."

▶ **DO** **File → Close** → **Don't Save** if asked.

---

### Scene 4 · Exploring the raw data with pivot tables (4:00–11:00), LibreOffice Calc → artifact 1

▶ **DO** Right-click **input 1 - customers.csv** → **Open with → LibreOffice Calc**. The **Text Import** dialog appears: Character set **Unicode (UTF-8)**, Separated by **Comma** only → **OK**. Maximise.

▶ **DO** Click the **column A header** (the letter A). Then right-click the number in the status bar at the bottom right and tick **CountA**.

✔ **CHECK** The status bar shows **CountA: 20261**.

🎙 **SAY**
> "This is the raw data. I select column A. The status bar counts twenty thousand two hundred and sixty-one cells. That's twenty thousand two hundred and sixty rows plus the header. But the brief says twenty thousand customers. So there are duplicates. The pipeline will handle those. First I want to understand the data with a few pivot tables."

**Pivot 1: products**

▶ **DO** Click cell **A1** → **Insert → Pivot Table…** → **Current selection** → **OK**. The **Pivot Table Layout** dialog opens.

🎙 **SAY**
> "Insert, Pivot Table. Calc has picked up the whole table. In this dialog I drag fields into rows and data."

▶ **DO** In the layout dialog:
1. Drag **num_products** into **Row Fields**
2. Drag **customer_id** into **Data Fields** → double-click it → choose **Count** → **OK**
3. Drag **next_product_purchased_90d** into **Data Fields** → double-click it → choose **Average** → **OK**
4. **OK**. The pivot appears on a new sheet.
5. Select the Average cells → right-click → **Format Cells… → Numbers → Percent**, decimal places **1** → **OK**

✔ **CHECK** 1 → 7.8% · 2 → 15.7% · 3 → 20.1% · 4 → 9.2%

🎙 **SAY** (hover over each row)
> "Customers with one product buy 7.8 percent of the time. Two products: 15.7. Three products: 20.1. But four products drops back to 9.2. So it's not a straight line. Customers who already have everything don't need more. A tree model can learn that. A straight line can't."

▶ **DO** Right-click the sheet tab at the bottom → **Rename Sheet…** → type `Products` → **OK**.

**Pivot 2: data quality**

▶ **DO** Click the **input 1 - customers** sheet tab → cell **A1** → **Insert → Pivot Table… → OK**. Drag **region** into **Row Fields** and **customer_id** into **Data Fields** (double-click → **Count**) → **OK**.

✔ **CHECK** Besides Central / East / North / South / West you see extra items such as **N.**, **W.**, and repeats of East / North / South that differ only by capital letters or a hidden space.

🎙 **SAY**
> "There should be five regions. But I see short forms like 'N.' and 'W.'. And the same region written with different capitals, or with a hidden space before or after the name. The pipeline must clean these labels before modelling."

▶ **DO** Rename the sheet `Data quality`.

**Pivot 3: leakage check**

▶ **DO** Data sheet → **A1** → **Insert → Pivot Table… → OK**. **welcome_pack_sent** into **Row Fields**; **customer_id** into **Data Fields** (Count); **next_product_purchased_90d** into **Data Fields** (Average) → **OK** → format the averages as **Percent**.

✔ **CHECK** 0 → 0.7% · 1 → 85.4%

🎙 **SAY**
> "This confirms what I suspected from the dictionary. With a welcome pack, 85 percent bought. Without one, less than one percent. The welcome pack doesn't predict a purchase. It's a *record* of the purchase. If the model sees this column, it will look brilliant in testing and fail in real use. It must be excluded."

▶ **DO** Rename the sheet `Leakage check`.

**Pivot 4: missing income**

▶ **DO** Data sheet → **A1** → **Insert → Pivot Table… → OK**. **customer_segment** into **Row Fields**; **customer_id** into **Data Fields** (Count); **monthly_income** into **Data Fields** → double-click → **Count** → **OK** → **OK**.

✔ **CHECK** Mass: 14,802 customers vs 13,326 incomes · Affluent 4,538 vs 4,361 · Premier 920 vs 879

🎙 **SAY**
> "Count skips blank cells. So comparing the two columns shows the missing incomes. In the Mass segment, ten percent of incomes are missing. In Affluent and Premier, about four percent. So it's not random. Lower-income customers skip this field more often. So I won't just fill it in. I'll also keep a flag that says the income was missing, because that is useful information too."

▶ **DO** Rename the sheet `Missing income`.

*(Optional if time allows: one more pivot with **complaints_12m** in Row Fields and the average purchase rate: 12.8% → 7.2% → 2.4%. "That supports the brief's rule of excluding customers with two or more complaints.")*

**Save as artifact 1**

▶ **DO** **File → Save As…** → go to `Cnx\Mercor_UC1\UC1_Cross_Sell_vN\Deliverables\3_Intermediate` → **File type: Excel 2007-365 (.xlsx)** → File name: `artifact 1 - exploratory pivot analysis` → **Save** → in the format question click **Use Excel 2007-365!** → **File → Close**.

🎙 **SAY**
> "I'll save this as a workbook in the Intermediate folder, as artifact one. That keeps the pivots as evidence. A CSV would lose them."

---

### Scene 5 · My pipeline (11:00–12:30), VS Code

▶ **DO** Click **VS Code** in the taskbar (Mac: the Dock) to bring it back → maximise. In the Explorer panel on the left, click **Deliverables** to expand it, then **1_Input**, **2_Code**, **3_Intermediate** and **4_Output** in turn.

🎙 **SAY**
> "Back in VS Code. Input has the four files I just looked at. Code has the pipeline I built for this request. Intermediate has my pivot workbook. Output is empty."

▶ **DO** Click **2_Code → pipeline_config.py**. Go down the file one block at a time. Each block starts with a `# ----` line.

#### Top of the file
🎙 "The pipeline is one config file and four notebooks. They run in order: preprocessing, training, testing, then back-test and packaging."

#### `# ---- paths`
🎙 "First the paths. Every file the pipeline reads or writes is named here."

#### `# ---- business rules`
🎙 "Then the business rules from the brief. Contact four thousand customers. Four dollars per contact. A hundred and fifty dollars margin per sale. At most one complaint."

#### `# ---- columns`
🎙 "Then the columns. The target, the ID columns, and gender. Gender is protected, so the model never uses it. And the leaky columns. For now only `cross_sell_product_type` is there. I'll keep an eye on this list, because of what the pivot showed."

#### `# ---- helpers`
🎙 "A small helper to read dates."

#### `# ---- models`
🎙 "And the two models: a logistic regression as the baseline, and gradient boosting. This is the first run on the full snapshot. So let's run it and check every result."

---

### How to run a notebook, cell by cell (Scenes 6–9)

- Code cells are numbered **[1], [2], [3]…** here, from the top. Headings don't count. After **Restart → Run All**, VS Code shows the same number to the left of each cell.
- To run one cell, click the **▶ Run** button on the left of that cell. Wait for the output. Then say the line.
- ✖ means you should see an error in that cell. That's a planted bug: follow the 🔧 **FIX** under it.
- After every fix: **Restart → Run All** (notebook toolbar). Run All runs every cell from the top, so the cells after the fix already have their output. For those, just click the cell, hover over its output and say the line.

---

### Scene 6 · Notebook 01, preprocessing (12:30–17:30): fix P1 and P2

▶ **DO** Click **01_data_preprocessing.ipynb**. Check the top-right corner shows **Python 3.12 (ds-venv)**. If it doesn't: click **Select Kernel → Jupyter Kernel… → Python 3.12 (ds-venv)**.

🎙 **SAY** (scroll through the section headings)
> "Notebook one cleans the raw data. Load, duplicates, dates, labels, impossible values, missing values, and save. I'll run it one cell at a time."

#### [1] `import matplotlib.pyplot as plt` → ▶
✔ No output.
🎙 "The imports and the shared config. The `log` function writes down every cleaning step."

#### [2] Section 1 · `raw = pd.read_csv(cfg.RAW_FILE)` → ▶
✔ `20,260 rows x 26 columns | unique customers: 20,000` · `Target rate: 11.6%`
🎙 "Twenty thousand two hundred and sixty rows. But only twenty thousand unique customers, so some customers appear twice. 11.6 percent bought a new product."

#### [3] `missing = raw.isna()…` → ▶
✔ Bar chart: **Missing values in the raw extract**
🎙 "Missing values. `cross_sell_product_type` is empty for eighty-eight percent. It's only filled for buyers. That's why it's already on my leaky list. Email open rate is missing for twenty-four percent. Days since last contact for sixteen. Income for eight."

#### [4] `raw.describe()…` → ▶
✔ age min **0** max **999** · avg_monthly_balance min **-99999** · tenure_months min **-1**
🎙 "Some values are impossible. Age zero, and age nine hundred and ninety-nine. A balance of minus ninety-nine thousand nine hundred and ninety-nine. A tenure of minus one. These are system defaults, not real values."

#### [5] Section 2 · `df = raw.copy()` → ▶
✔ `exact duplicates 200` · `conflicting customer rows 60` · `20,000 customers`
🎙 "Two hundred rows are exact copies from the CRM merge. Sixty customers have two different rows. There's no update time, so I keep the first one. I do this before the train-test split. Otherwise the same customer could be in both."

#### [6] Section 3 · `df["customer_since"] = pd.to_datetime(…)` → ▶ ✖ **P1**
✔ Red error: `ValueError: time data "30/08/2023" doesn't match format "%Y-%m-%d", at position 13`
🎙 "It stopped. The date thirty, slash, zero eight, slash, twenty twenty-three doesn't match the year-month-day format. That date is day first. So the file mixes two date formats. I won't let pandas guess. A date like five, slash, three could be May or March. My config has a `parse_dates` helper for this. It reads both formats, and fails if anything is left. But in this cell I only used one format. So I'll use the helper."

▶ **DO** Click the **pipeline_config.py** tab → hover over the `parse_dates` function → go back to the notebook.

🔧 **FIX P1** In cell [6], change the **right-hand side** of this one line:
```python
df["customer_since"] = pd.to_datetime(df["customer_since"], format="%Y-%m-%d")
```
to:
```python
df["customer_since"] = cfg.parse_dates(df["customer_since"])
```
*(Select from `pd.to_datetime` to the end of the line with the mouse, then type the replacement.)*

▶ **DO** Click **Restart** → confirm **Restart** if asked → click **Run All**.
🎙 "I restart and run from the top, so nothing is left over from the failed run."

✔ Cell [6] now shows `customer_since: 19,600 ISO dates + 400 day-first dates`. The run stops at cell [8] (next bug).
🎙 "The dates are fixed. Nineteen thousand six hundred normal dates and four hundred day-first dates."

#### [7] `snapshot = pd.Timestamp(…)` (already run: click it, hover)
✔ `negative tenure 40 rows -> recomputed from customer_since`
🎙 "Forty customers had a negative tenure. It's recalculated from the start date."

#### [8] Section 4 · `REGION_FIXES = …` ✖ **P2**
✔ Red error: `AssertionError: unexpected regions: [' South', 'Central', 'East', 'East ', 'North', 'North ', 'South', 'West']`
🎙 "Now the label check fails. It expected five regions and found eight. There's 'North', and 'North' with a space at the end. And 'South' with a space at the front. I saw this in the pivot. The product line removes spaces with `strip`. I forgot it in the region line."

🔧 **FIX P2** In cell [8], change this line:
```python
df["region"] = df["region"].str.lower().replace(REGION_FIXES).str.title()
```
to:
```python
df["region"] = df["region"].str.strip().str.lower().replace(REGION_FIXES).str.title()
```

▶ **DO** **Restart → Run All**.

✔ It runs to the end. Cell [8] shows `region labels 800 rows` · `product labels 600 rows`.
🎙 "Now it runs to the end. Eight hundred region labels and six hundred product labels are cleaned."

**All cells have run now. For each cell below: click it, hover over the output, say the line.**

#### [9] Section 5 · `bad_age = …`
✔ `age outside 18-100 60 rows` · `balance = -99999 60 rows`
🎙 "Sixty impossible ages and sixty fake balances are set to missing."

#### [10] Section 6 · `income_gap = …` (chart)
✔ Bar chart, **Mass** in orange at **10.0%**, others about 4%
🎙 "Income is missing for ten percent of the Mass segment, in orange. The other segments are about four percent. Same pattern as the pivot. So it's not random."

#### [11] `# not missing at random …`
✔ `monthly_income missing 1,677 rows` · cross-table: opted out (0) → **4808** blank, opted in (1) → **0** blank
🎙 "So the pipeline adds an income-missing flag, and fills income with the segment median. This table checks the email open rate. It's blank for exactly the four thousand eight hundred and eight customers who opted out. And for nobody else. Blank means 'not emailed'. So zero is the right value."

#### [12] Section 7 · `df.to_csv(cfg.CLEAN_FILE …)`
✔ `Saved 20,000 rows -> artifact 2 - cleaned customers.csv` · `Saved 10 log entries -> artifact 3 …`
🎙 "The clean data is saved as artifact two. Age, balance and credit score still have some missing values. The model pipelines handle those."

#### [13] `steps = …` (chart)
✔ Bar chart: **Data-quality fixes applied (artifact 3)**
🎙 "This last chart shows every cleaning step, and how many rows it touched."

▶ **DO** In the Explorer panel, click **3_Intermediate → artifact 3 - data quality log.csv**.
🎙 "Every cleaning step is also in a log, artifact three. So anyone can check it."

---

### Scene 7 · Notebook 02, training (17:30–22:30): fix T1 and T2

▶ **DO** Click **2_Code → 02_model_training.ipynb**.

🎙 **SAY**
> "Notebook two splits the data. It compares the two models with five-fold cross-validation, on the training set only. Then it trains and saves them. The test set stays untouched until notebook three. Again, one cell at a time."

#### [1] `import joblib` → ▶
✔ `20,000 customers | 22 features` · `Excluded: [...]`
🎙 "Twenty thousand customers. The Excluded line shows what the model can't use: the IDs, dates, gender, the leaky product type, and the target."

#### [2] Section 1 · `train_df, test_df = train_test_split(…)` → ▶
✔ `train 16,000 (11.6% positive) | test 4,000 (11.6% positive)`
🎙 "The split is stratified. Sixteen thousand customers for training, four thousand for testing. Both have 11.6 percent buyers."

#### [3] Section 2 · `cv = StratifiedKFold(…)` → ▶ ✖ **T1**
✔ Red error: `ValueError: Input X contains NaN. LogisticRegression does not accept missing values encoded as NaN natively.` The traceback mentions `pipeline_config.py`.
🎙 "The baseline fails. Logistic regression can't handle missing values. Age, balance and credit score still have some, on purpose. Gradient boosting handles them by itself, but the baseline needs an imputer. The error points to the baseline in the config file."

▶ **DO** Click **pipeline_config.py** (tab or Explorer panel) → scroll to `build_baseline`.
🎙 "Here's the baseline. A scaler on the numeric columns, but no imputer. I imported `SimpleImputer` at the top, but never used it here. I'd only tried the boosting model, and it doesn't need one. I'll add a median imputer before the scaler, inside the pipeline. That way it only learns from the training folds."

🔧 **FIX T1** In `build_baseline`, change:
```python
        ("num", StandardScaler(), numeric_columns(df)),
```
to:
```python
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns(df)),
```
*(Only this `"num"` line changes. The `make_pipeline(preprocess, LogisticRegression(…))` line at the bottom stays as it is. Watch the brackets: `StandardScaler())` closes the inner `make_pipeline`, then `, numeric_columns(df)),`.)*

▶ **DO** **File → Save**. Click the **02_model_training.ipynb** tab → **Restart → Run All**.

✔ It runs, but cell [3] shows ROC-AUC **≈ 0.98** for both models.
🎙 "It runs now. But look: a ROC-AUC of 0.98 for both models. For a marketing model that's not good news. It's a red flag. Nobody predicts buying that well. This is the welcome pack I saw in the pivot. Let me prove it."

▶ **DO** Hover over the output of cell [3] → click **+ Code** below it → type:
```python
df.groupby("welcome_pack_sent")[cfg.TARGET].mean()
```
→ click this new cell's **▶ Run** button. (It is now cell [4], so the cells after it move down by one.)

✔ `0  0.007` · `1  0.855`
🎙 "Eighty-five percent with a welcome pack. Under one percent without. Same as the pivot. The welcome pack is sent after the purchase. So it goes on the leaky list in my config, next to the product type."

🔧 **FIX T2** In `pipeline_config.py`, change:
```python
LEAKY_COLUMNS = ["cross_sell_product_type"]         # populated only after the purchase
```
to:
```python
LEAKY_COLUMNS = ["cross_sell_product_type", "welcome_pack_sent"]   # populated only after the purchase
```

▶ **DO** **File → Save** → **02_model_training.ipynb** tab → **Restart → Run All**.

**All cells have run now. Scroll back to the top. For each cell: click it, hover over the output, say the line.**

#### [1] `import joblib`
✔ `21 features` · `Excluded:` now has `welcome_pack_sent`
🎙 "The Excluded line now shows both leaky columns, and gender."

#### [3] Section 2 · cross-validation table
✔ baseline_logreg **0.773 / 0.317** · gradient_boosting **0.798 / 0.369**
🎙 "Now the numbers are realistic. The baseline gets a ROC-AUC of 0.77. Gradient boosting gets 0.80. Only 11.6 percent of customers buy. So PR-AUC is the more honest measure. A random model would get 0.116. Boosting gets 0.37, the baseline 0.32. So boosting is worth it."

#### [5] `ax = cv_table…plot.bar(…)` (chart)
✔ Bar chart with a grey dashed line
🎙 "The chart shows the same thing. The dashed line is a random model."

#### [6] Section 3 · `cfg.MODEL_DIR.mkdir(…)`
✔ `saved baseline_logreg.joblib` · `saved gradient_boosting.joblib` · `boosting iterations after early stopping: 164`
🎙 "Early stopping chose a hundred and sixty-four rounds. Both models are saved as artifact five."

---

### Scene 8 · Notebook 03, testing (22:30–27:00): fix E1

▶ **DO** Click **03_model_testing.ipynb**.

🎙 **SAY**
> "Notebook three tests both models on the hold-out set. They have never seen it. Then lift, calibration and the drivers. And the acceptance checks."

#### [1] `import joblib` → ▶
✔ `test set: 4,000 customers, 11.6% positive | models: ['baseline_logreg', 'gradient_boosting']`
🎙 "It loads the four thousand test customers and the two saved models."

#### [2] Section 1 · `scores = {name: model.predict(X_test) …}` → ▶ ✖ **E1** (no error, wrong numbers)
✔ The table shows gradient_boosting ROC-AUC **≈ 0.58**
🎙 "The hold-out ROC-AUC is 0.58. In cross-validation it was 0.80. A drop that big on a random test set means the evaluation is wrong, not the model."

▶ **DO** Hover over `model.predict(X_test)` in cell [2].
🎙 "Here it is. I used `predict`. It returns zero or one, with a fifty percent cut-off. ROC-AUC, PR-AUC and the Brier score need probabilities. The cells below use these same scores. So one fix corrects all of them."

🔧 **FIX E1** In cell [2], change:
```python
scores = {name: model.predict(X_test) for name, model in models.items()}
```
to:
```python
scores = {name: model.predict_proba(X_test)[:, 1] for name, model in models.items()}
```

▶ **DO** **Restart → Run All**.

**All cells have run now. For each cell: click it, hover over the output, say the line.**

#### [2] Section 1 · hold-out table
✔ gradient_boosting **0.810 / 0.421 / 0.084** · baseline **0.774 / 0.367** · random PR-AUC **0.116**
🎙 "Gradient boosting gets a ROC-AUC of 0.81. The target is 0.78. Its PR-AUC is 0.42. The baseline gets 0.37, and random 0.116."

#### [3] Section 2 · lift table
✔ decile 1 lift **3.966** · `Top-20% lift: 2.83x`
🎙 "The top ten percent of customers by score buy at four times the average rate. The bottom groups almost never buy. The top twenty percent give a lift of 2.83. The target is 2.5."

#### [4] Lift chart
🎙 "The bar chart shows the same thing."

#### [5] Section 3 · calibration
✔ Curve close to the diagonal · `mean predicted 0.116 vs actual 0.116`
🎙 "The calibration curve is close to the diagonal. The model predicts 11.6 percent on average, and 11.6 percent really bought. So when the model says thirty percent, about thirty percent really buy. That matters, because Marketing will budget on these numbers."

#### [6] Section 4 · SHAP summary chart
▶ **DO** Hover over each row of the chart as you name it.
🎙 "This SHAP chart shows what drives the predictions.
Email open rate is at the top. Customers who read our emails are the most open to an offer. So email is the right channel for them.
Age: it peaks in the late thirties.
Tenure: one to five years is the sweet spot. Very new customers aren't ready yet.
App logins: digitally active customers buy more.
Number of products: two or three is best, as the pivot showed.
Months since the last product was opened: someone who just bought is less likely to buy again straight away.
And complaints strongly reduce the chance. That supports the complaints rule."

#### [7] SHAP dependence charts (three panels)
▶ **DO** Hover over each panel.
🎙 "These charts show the *shape* of each effect. Above the grey line means more likely to buy.
Tenure: a big jump after the first year, positive up to about five years, then negative.
Number of products: one is negative, two and three are clearly positive, and four drops back. The same as the pivot.
Email open rate: flat up to about twenty-five percent, then rising fast. So Marketing should target customers who read our emails, not just anyone on the list."

#### [8] Section 5 · acceptance table
✔ **True / True / True**
🎙 "All three acceptance checks are True. The comparison table and all the charts are saved as artifacts six and seven."

---

### Scene 9 · Notebook 04, back-test and package (27:00–29:30)

▶ **DO** Click **04_backtest_and_package.ipynb**.

🎙 **SAY**
> "Notebook four answers the real question in the brief. One cell at a time."

#### [1] `import json` → ▶
✔ No output.
🎙 "It loads the clean data and the features."

#### [2] Section 1 · out-of-fold scores → ▶ (takes a few seconds)
✔ `count 20000` · mean **0.113** · max **0.860**
🎙 "Every customer gets an out-of-fold score. The data is split into five parts. Each customer is scored by a model trained on the other four. So no customer is scored by a model that has seen them. The back-test can't flatter us."

#### [3] Section 2 · eligible customers and the list → ▶
✔ `eligible: 14,855 of 20,000 customers | eligible conversion rate 13.64%` · `saved 4,000 customers -> artifact 8 …`
🎙 "Now the compliance rules: opted in, and fewer than two complaints. That leaves fourteen thousand eight hundred and fifty-five customers. They buy at 13.6 percent. The top four thousand by score are saved as artifact eight."

#### [4] Section 3 · back-test result → ▶
✔ expected **1298** · actual **1312** · random **546** · profit **180800** vs **65831** · `passes_backtest_lift True`
🎙 "The result. The model expected about thirteen hundred sales. Thirteen hundred and twelve really happened. That's very close, so the probabilities can be trusted. Random selection would give about five hundred and forty-six.
In money: a hundred and eighty thousand dollars profit, against sixty-six thousand at random. Same budget of sixteen thousand dollars."

#### [5] Back-test chart → ▶
🎙 "The chart shows both side by side."

#### [6] Section 4 · package → ▶
✔ `saved model.joblib and metrics.json`
🎙 "The final model is trained again on all twenty thousand customers, and saved with its metrics."

#### [7] README → ▶
✔ The README is printed.
▶ **DO** Scroll slowly through the printed README.
🎙 "And a README. This is final output three. It's ready to score the thirtieth of September snapshot for Q4."

---

### Scene 10 · Validating the back-test in LibreOffice Calc (29:30–32:30) → final output 1

▶ **DO** File Explorer → `Deliverables\3_Intermediate` → right-click **artifact 8 - backtest scored customers.csv** → **Open with → LibreOffice Calc** → Text Import: **Comma** → **OK** → maximise.

🎙 **SAY**
> "Before this goes to Marketing, I'll check the list myself in a spreadsheet."

▶ **DO** Columns **M** and **N** are empty: you build a small summary table there. Column **M** is text labels you type yourself (they are *not* data columns); column **N** is formulas on the data columns (C = `propensity`, K = `actual_converted`, I = `marketing_opt_in`, J = `complaints_12m`). Every row in this file is one contacted customer, so counting column C counts the customers. Click cell **M1**, type the label, click **N1**, type the formula, and so on down:

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
> "Exactly four thousand customers.
> Each propensity is a probability. So adding them up gives the number of buyers the model expects: about thirteen hundred. The real number was thirteen hundred and twelve. Very close. So the probabilities are well calibrated: when the model says thirty percent, about thirty percent really buy. Marketing can use them to forecast, not just to rank.
> Thirteen hundred and twelve buyers is a 32.8 percent conversion rate. Eligible customers buy at 13.6 percent. So that's 2.4 times. The target was two.
> Random selection would give about five hundred and forty-six.
> Profit is a hundred and eighty thousand eight hundred dollars. Random gives about sixty-six thousand. That's about a hundred and fifteen thousand dollars more, for the same budget.
> And the compliance checks. The minimum opt-in is one, so everyone opted in. The maximum complaints is one, so nobody with two or more complaints is on the list."

▶ **DO** **File → Save As…** → `Deliverables\4_Output` → **File type: Excel 2007-365 (.xlsx)** → name `final output 1 - backtest target list` → **Save** → **Use Excel 2007-365!** → **File → Close**.

---

### Scene 11 · Summary deck (32:30–37:00), LibreOffice Impress → final output 2

▶ **DO** File Explorer → `Deliverables\1_Input` → right-click **input 4 - summary deck template.pptx** → **Open with → LibreOffice Impress**. **Immediately: File → Save As…** → `Deliverables\4_Output` → **File type: PowerPoint 2007-365 (.pptx)** → name `final output 2 - cross-sell summary` → **Save** → **Use PowerPoint 2007-365!**.

🎙 **SAY**
> "This is the team's summary template. First I save my own copy into the Output folder, so the template stays clean. I need to fill in the orange brackets."

▶ **DO** For every orange `[   ]`: double-click into the text → select the **whole** `[   ]`, brackets included → type just the number (units such as %, $k and × are already in the labels) → select the number → in the **Properties** sidebar on the right, **Character → Font Color** arrow → **Automatic** (or **Format → Character… → Font Effects → Font color: Automatic**).

**Slide 2: Problem and approach**
- `[ ]` duplicate rows → **260**

🎙 **SAY** "Two hundred and sixty duplicate rows removed. Dates, labels and fake values fixed. The two leaky columns and gender left out."

**Slide 3: Model results**
- ROC-AUC → **0.81**
- PR-AUC → **0.42** vs **0.37**
- Top-20% lift → **2.83**
- Click the **border of the dashed box** → press **Delete** → **Insert → Image…** → `Deliverables\3_Intermediate\artifact 7 - charts\05_lift_by_decile.png` → **Open** → drag it to fill the right-hand side

🎙 **SAY** "ROC-AUC 0.81. The target was 0.78. PR-AUC 0.42, against 0.37 for the baseline. And 2.83 times lift in the top twenty percent. The chart shows how fast buying drops from the top group down."

**Slide 4: Back-test and Q4 recommendation**
- Conversions → **1,312** vs **546**
- Profit ($k) → **180.8** vs **65.8**
- Conversion rate (%) → **32.8** vs **13.6**
- The three drivers on the right are already written in the template (from the SHAP results): just hover over each one as you mention it

🎙 **SAY**
> "In the back-test, the model's four thousand customers made thirteen hundred and twelve purchases. Random would give five hundred and forty-six. That's a hundred and eighty thousand dollars profit instead of sixty-six thousand.
> The drivers tell Marketing who to target. Customers who read our emails and use the app. Customers with two or three products. And avoid customers who just bought, or who complained.
> My recommendation. Use the packaged model on the September snapshot for Q4. Keep a random ten percent as a control group, to measure the real gain. And check the model again every quarter."

▶ **DO** **File → Save** → **Use PowerPoint 2007-365!** → **File → Close**.

---

### Scene 12 · Wrap-up (37:00–38:30), File Explorer

▶ **DO** In File Explorer, open `Deliverables` and hover over each folder and its files.

🎙 **SAY**
> "To wrap up. Input has the four files I received. Plus my pipeline code as it was before this run, delivered as input five. Code is now the corrected pipeline, delivered as final output four. Intermediate has my pivot analysis, the clean data and quality log, the train-test split, the trained models, the model comparison, the charts and the back-test list. Output has the checked target list with ROI, the summary deck, and the packaged model with its README.
> I fixed five issues along the way. Two data problems in the extract: the date format and the region labels. A missing imputer in the baseline. A column that leaked the answer and pushed accuracy to 0.98. And a test that used labels instead of probabilities.
> Every acceptance criterion is met. The model is ready to score the September snapshot for the Q4 campaign. Thank you."

▶ **DO** Stay silent for **3 seconds**.

---

## PART 5 (Windows practice): Stop and save

▶ **DO**
1. Sharing toolbar → **More (…)** → **Stop recording** → **Stop sharing** → **Leave**
2. A few minutes later: Teams → **Chat** → `UC1 practice` → recording tile → **⋯ → Download** → rename it `UC1_practice_v1.mp4`
3. **Validate and zip the deliverables:**
   ```powershell
   cd C:\Users\ullas.kc\Cnx\LLM_Training_recording      # your project folder
   prep\package_deliverables.cmd UC1
   ```
   ✔ ends with **READY TO UPLOAD** and creates `Cnx\Mercor_UC1\UC1_Cross_Sell_vN\Deliverables.zip` in the newest version folder. It checks every file is labelled input / artifact / final output, all deliverables exist, every fix is in place and no notebook shows an error. It also adds the original code as **input 5** and your corrected code as **final output 4**, and leaves out junk such as `__pycache__`. If it says **NOT READY**, fix what it lists and run it again.
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
| LibreOffice shows a yellow "read-only" or "downloaded from the internet" bar | Click **Edit Document**. Next time re-stage (it removes the flag) |
| The PDF opens in a different app | Right-click → **Open with → Firefox** (Windows: **Choose another app → Firefox**) |
| A pop-up or notification appears | Close it and carry on without comment |
| Running long | Skip the optional complaints pivot and shorten the SHAP talk to the top four drivers |
| Teams freezes or disconnects | Stop, re-stage and restart the practice take |

# Windows Setup: practice and internal-review recordings

Use this on your **org Windows laptop** to set up, rehearse and record a practice version of each use case for internal approval. After approval, do the real recording on the Mac ([README](README.md) sections 1–3). The data, notebooks, narration and run sheet are the same on both machines; only the setup commands and a few app names differ.

| Mac (final) | Windows (practice) |
|---|---|
| Finder | File Explorer |
| Task notes: VS Code Markdown preview | same |
| TaskRecorder | Snipping Tool screen recording, or OBS Studio (section 7) |
| `bash setup_mac.sh` | `setup_windows.cmd` |
| `bash prep/stage_recording.sh UC1` | `prep\stage_recording.cmd UC1` |
| Firefox, LibreOffice Calc, LibreOffice Impress, VS Code | same (Microsoft Office is not used: the Mac doesn't have it) |

---

## 0. Check with IT first (org laptop)

Write the answers in [use_cases/Open_Questions.md](use_cases/Open_Questions.md) (Q7–Q9).

- Can you install **Python 3.12** and **VS Code** for your user? Both offer per-user installers that need no admin rights, but some orgs block them (AppLocker / Intune).
- Can you reach **github.com** and **pypi.org**? If pip must use an internal mirror (Artifactory / Nexus), get its URL.
- Is a **screen recorder** allowed? (Snipping Tool is built into Windows 11.)
- Is **GitHub Copilot** pushed by org policy? It must be **off** during recording, even for practice, so you build the habit.

## 1. Install the prerequisites

Open **PowerShell** (Start → type "PowerShell" → Windows PowerShell).

| Tool | How | Notes |
|---|---|---|
| **Python 3.12 (x64)** | <https://www.python.org/downloads/windows/> → latest **3.12.x** → "Windows installer (64-bit)". In the installer tick **"Add python.exe to PATH"**, then **Install Now** (per-user, no admin) | Or `winget install --id Python.Python.3.12 --scope user`. Even on an ARM (Snapdragon) laptop, use the **64-bit (x64)** installer |
| **Git** (optional) | <https://git-scm.com/download/win>, default options | Or `winget install --id Git.Git --scope user`. Not needed if you use the ZIP download |
| **VS Code** | <https://code.visualstudio.com/> → **User Installer** (x64) | Tick "Add to PATH" |
| **VS Code extensions** | In VS Code: Extensions panel → install **Python** and **Jupyter** (publisher: Microsoft) | Do **not** install Copilot or any AI extension. If Copilot is pre-installed, disable it: Extensions → GitHub Copilot → Disable. Settings → search **"disable AI features"** → tick it |
| **Firefox** and **LibreOffice** | <https://www.mozilla.org/firefox/> and <https://www.libreoffice.org/download/> (includes Calc and Impress). Both free | Practise with the same apps as the Mac. Open each once and dismiss any first-run or "What's new" prompts |

Close and reopen PowerShell, then check:

```powershell
py -3.12 --version      # or: python --version   -> Python 3.12.x
git --version           # only if you installed Git
code --version
```

## 2. Get the project (short path, not OneDrive)

Windows limits paths to 260 characters and some packages have deep folders. **Keep the project path short** and **outside OneDrive** (OneDrive syncing a 3 GB `.venv` will slow everything down).

**Option A: git clone**
```powershell
cd $env:USERPROFILE
git clone https://github.com/UllasKc/LLM_Training_recording.git
cd LLM_Training_recording
```

**Option B: ZIP download** (no Git)
1. Open <https://github.com/UllasKc/LLM_Training_recording> → green **Code** button → **Download ZIP**
2. Then:
```powershell
cd $env:USERPROFILE
Expand-Archive "$env:USERPROFILE\Downloads\LLM_Training_recording-main.zip" -DestinationPath .
Rename-Item LLM_Training_recording-main LLM_Training_recording
cd LLM_Training_recording
```

The project is now at `C:\Users\<you>\LLM_Training_recording`. The setup script refuses to run from a path that is too long and tells you what to do.

## 3. Run the one-time setup

```powershell
.\setup_windows.cmd
```
(Or double-click `setup_windows.cmd` in File Explorer.)

It finds Python 3.12, creates `.venv`, installs the **same locked package versions as the Mac**, registers the Jupyter kernel **`Python 3.12 (ds-venv)`** and runs the readiness check. It should end with **`READY`**. A disk-space warning is fine for practice: Snipping Tool/OBS videos are much smaller than TaskRecorder's. It takes about 3–5 minutes and is safe to re-run.

**Behind a corporate proxy or internal PyPI mirror?** Set these in the same PowerShell window first, then run setup:
```powershell
$env:HTTPS_PROXY   = "http://proxy.yourcompany.com:8080"                      # if IT gave you a proxy
$env:PIP_INDEX_URL = "https://artifactory.yourcompany.com/api/pypi/pypi/simple" # if IT gave you a mirror
$env:PIP_TRUSTED_HOST = "artifactory.yourcompany.com"                          # only if you get SSL errors
.\setup_windows.cmd
```

**If org policy blocks PowerShell scripts** (an error mentioning *execution policy* or *AppLocker*), run the same steps by hand:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-lock.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name ds-venv --display-name "Python 3.12 (ds-venv)"
.\.venv\Scripts\python.exe prep\verify_setup.py
```

**Restart VS Code** (if it was open) so it picks up the new kernel and environment settings.

## 4. Stage a clean workspace (before every take, and to reset after a rehearsal)

```powershell
cd $env:USERPROFILE\LLM_Training_recording
prep\stage_recording.cmd UC1        # or UC2
```

Or **double-click** `prep\stage_recording.cmd` in File Explorer, type `1` (UC1) or `2` (UC2) and press Enter; the window stays open until you press a key.

This copies a fresh workspace to your **Desktop** (`Desktop\UC1_Cross_Sell`); it also works when the Desktop is redirected to OneDrive. The full path is printed at the end. A previous copy, such as a rehearsal, is **moved** to `C:\Users\<you>\Rehearsal_Backups\`, never deleted. The script also:
- removes the "downloaded from the internet" mark, so LibreOffice doesn't show "downloaded from the internet" warnings on camera
- writes hidden VS Code settings: AI features off, the venv interpreter, larger fonts

## 5. First-time VS Code check (off camera, once)

1. VS Code → **File → Open Folder…** → Desktop → `UC1_Cross_Sell` → "Yes, I trust the authors"
2. **File → New File… → Jupyter Notebook**
3. Top right → **Select Kernel** → **Jupyter Kernel…** → **Python 3.12 (ds-venv)**
4. In a cell type `import pandas, sklearn, shap; print("ok")` and click the ▶ Run button → `ok`
5. Close without saving, then re-stage (`prep\stage_recording.cmd UC1`) so the folder is clean again

If **Select Kernel** doesn't list `ds-venv`, see Troubleshooting.

## 6. Pre-take checklist (Windows practice)

- [ ] `prep\stage_recording.cmd UC1` run just now (clean folder)
- [ ] **Teams, Outlook, Slack and any chat apps quit** (not just minimised); org pop-ups on camera are the most common problem
- [ ] **Do not disturb on:** Settings → System → Notifications → Do not disturb
- [ ] Display scale 100–125% (Settings → System → Display); maximise windows
- [ ] Desktop tidy: only the UC folder visible (or right-click Desktop → View → untick "Show desktop icons" and open the folder from File Explorer)
- [ ] Copilot / AI features off in VS Code; no AI assistants in any app (don't click any Copilot button in Office)
- [ ] Headset mic, quiet room
- [ ] `Task Notes.md` open as a **preview in VS Code** before you start recording
- [ ] Vary the look between takes: UC1 Light mode, UC2 Dark mode (Settings → Personalization → Colors)
- [ ] Narration rules are the same as on the Mac: see [use_cases/Recording_Checklist.md](use_cases/Recording_Checklist.md) section C and the run sheet in each use-case document

## 7. Record the practice take

**Option A: Snipping Tool** (built into Windows 11, usually allowed)
1. Open **Snipping Tool** → switch to the **video camera** (Record) mode → **+ New**
2. Drag to select the **whole screen**
3. Turn on the **microphone** toggle in the recording toolbar (Snipping Tool 11.2311+; update it from the Microsoft Store if you don't see it)
4. **Start**, record the full take (15:00–45:59), then **Stop** and **Save as** MP4, e.g. `UC1_practice_v1.mp4`

**Option B: OBS Studio** (if IT allows; better quality and long-take stability)
1. Install from <https://obsproject.com>, then Sources → **+** → **Display Capture**; check **Mic/Aux** in the Audio Mixer
2. Settings → Output → Recording Format **mp4**, Video → Base/Output resolution = your screen
3. **Start Recording** / **Stop Recording**; files go to `Videos\`

Then share the MP4 and the `Deliverables` folder with your manager for internal review.

## 8. After internal approval → move to the Mac

Everything carries over: the same data, briefs, package versions, notebook flow and narration. On the Mac:
1. `git clone` (or `git pull`) into `~/LLM_Training_recording`, as in README section 1
2. `bash setup_mac.sh`, then `bash prep/stage_recording.sh UC1`
3. Work through the full Mac [Recording_Checklist.md](use_cases/Recording_Checklist.md) (TaskRecorder, OTA account, Accessibility Inspector, clock with seconds…)
4. Rehearse once on the Mac: menus sit in the top menu bar, **Finder** replaces File Explorer, and `Ctrl` shortcuts become `Cmd`
5. Apply any reviewer comments from the internal review

> Your notebook from the practice take is **not** reused on the Mac. Each recording is done live from a clean workspace.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Python 3.12 not found` | Install per section 1 (tick "Add python.exe to PATH"), open a **new** PowerShell, re-run |
| `The project folder path is too long` | Clone or move the project to `C:\Users\<you>\LLM_Training_recording` (not inside OneDrive or Documents\…\…) |
| `ARM64 Python detected` | Uninstall it and install the **64-bit (x64)** Python 3.12 installer |
| pip: `SSL: CERTIFICATE_VERIFY_FAILED` / timeouts | Corporate proxy or SSL inspection: set `HTTPS_PROXY` / `PIP_INDEX_URL` / `PIP_TRUSTED_HOST` (section 3) or ask IT for the internal PyPI mirror |
| "running scripts is disabled on this system" | Use `setup_windows.cmd` (it bypasses the policy for that one script) or the manual commands in section 3 |
| Kernel `Python 3.12 (ds-venv)` missing in VS Code | Restart VS Code. Still missing: Select Kernel → **Python Environments…** → choose `.venv\Scripts\python.exe` inside the project |
| VS Code asks to install `ipykernel` | You picked the wrong interpreter; choose the `ds-venv` kernel |
| LibreOffice shows a read-only or "downloaded" warning | Re-run `prep\stage_recording.cmd UC1` (it unblocks the files) |
| Long `UserWarning: Could not find the number of physical cores` in a notebook | Restart VS Code after setup (setup sets `LOKY_MAX_CPU_COUNT` for your user) |
| Calc shows the CSV in one column | In the Text Import dialog tick **Comma** only (character set UTF-8). Delimiter: Comma |

## Cleanup (if you ever need it)

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\LLM_Training_recording\.venv"
Remove-Item -Recurse -Force "$env:APPDATA\jupyter\kernels\ds-venv"
[Environment]::SetEnvironmentVariable("LOKY_MAX_CPU_COUNT", $null, "User")
```

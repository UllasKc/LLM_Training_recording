# Open Questions

Track anything that's undecided. When you get an answer, fill in **Answer**, set **Status** to `Resolved` and add the date, then tell Claude so dependent files can be updated.

Status values: `Open` · `Waiting` (asked someone) · `Resolved`

| ID | Question | Why it matters | Default if no answer | Affects | Status | Answer | Date |
|---|---|---|---|---|---|---|---|
| Q1 | Will the provided Mac have Microsoft Word, Excel and PowerPoint (licensed, no sign-in prompts)? | The app topology, run sheets and Metadata.rtf assume Office. The fallback is Pages / Numbers / Keynote, but Numbers is on Mercor's "use an alternative if possible" list | Office available | Use-case docs §4/§8, both Metadata.rtf, Use_Cases_v2.xlsx | Open | | |
| Q2 | Are the brief numbers and pass criteria OK with your manager? (UC1: 4,000 contacts, $4/contact, $150 margin, AUC ≥ 0.78, top-20% lift ≥ 2.5×. UC2: 25 agents / 37% capacity, day-7 rule, out-of-time AUC ≥ 0.78) | They appear in input 3, Metadata.rtf, Task Notes and the Studio pitch, so they must match the approved story | Keep as written (achievable on the data) | `prep/generate_briefs.py`, both Metadata.rtf, Task Notes, use-case docs, Use_Cases_v2.xlsx | Open | | |
| Q3 | Do you have admin rights on the provided Mac (to install Python 3.12 and VS Code)? | The python.org installer and dragging apps into /Applications need an admin password | Admin rights available | README §2, setup_mac.sh | Open | | |
| Q4 | Does Mercor/Concentrix supply its own Metadata template, or is our Metadata.rtf accepted as is? | The guideline mentions "a template provided by Mercor" | Use our Metadata.rtf; copy sections into the template if one arrives | both Metadata.rtf | Open | | |
| Q5 | Which use case is recorded first? | Decides the UI variation (UC1 light mode / Dock bottom, UC2 dark mode / Dock left) and which one to rehearse first | UC1 first | Recording_Checklist.md §B | Open | | |
| Q7 | Can you install Python 3.12 and VS Code on the org Windows laptop (per-user installers)? | Needed for the Windows practice setup; some orgs block installers via AppLocker/Intune | Per-user install allowed | WINDOWS_SETUP.md §0–1 | Open | | |
| Q8 | Can the org laptop reach github.com and pypi.org, or must pip use an internal mirror / proxy? | setup_windows downloads packages from PyPI | Direct access | WINDOWS_SETUP.md §3 | Open | | |
| Q9 | Which screen recorder is allowed on the org laptop for the internal-review take (Snipping Tool / OBS / other)? | Internal approval needs a practice video | Snipping Tool | WINDOWS_SETUP.md §7 | Open | | |
| Q10 | Does Mercor/partner accept a **pre-written pipeline** (prepared before recording, with planted issues fixed on camera) as a pre-existing asset? | Mercor bans AI tools *during* recording and asks for pre-existing assets to be documented; it says nothing about how those assets were prepared. The internal benchmark used pre-written code | Yes: it's declared as pre-existing code in Metadata and the pitch, as the benchmark did. You must understand every line | UC1 2_Code, Metadata.rtf, pitch | Open | | |

## Resolved

_Move rows here once answered._

| ID | Question | Answer | Date | Files updated |
|---|---|---|---|---|
| Q6 | Public repo or private repo with token? | Public: https://github.com/UllasKc/LLM_Training_recording (clone or ZIP download, no sign-in) | 2026-10-26 | README §1 |

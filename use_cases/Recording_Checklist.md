# Recording Checklist (Project Frost)

Print this or keep it on your phone, **not** on the Mac screen.

## A. One-time Mac setup (dedicated recording user)
- [ ] New macOS user created for recording. **No iCloud, no personal Apple/Google/GitHub accounts, no VPN/proxy**
- [ ] Xcode 26 installed → right-click Xcode → Open Developer Tool → **Accessibility Inspector** → minimise it (icon visible in Dock)
- [ ] TaskRecorder 2.4.3 in Applications; allowed in System Settings → Privacy & Security; **Accessibility, Screen Recording, Microphone all green**; signed in with the **Mercor OTA** Google account ("Select all" on the consent screen)
- [ ] Insightful running
- [ ] Menu-bar clock shows **seconds** (System Settings → Control Center → Clock Options → Display the time with seconds)
- [ ] Python 3.12 from python.org installed → `bash setup_mac.sh` ends with **READY**
- [ ] VS Code installed, with only the **Python** and **Jupyter** extensions (Microsoft). **No GitHub Copilot / Copilot Chat or any AI extension.** Also turn off AI features globally: Settings → search "disable AI features" → tick it
- [ ] Firefox, LibreOffice Calc and LibreOffice Impress open without first-run pop-ups (open each once beforehand and dismiss everything)
- [ ] Built-in display at default scaled resolution (not native 4K/5K)
- [ ] Notifications off (Focus → Do Not Disturb)

## B. Before every take
- [ ] `bash prep/stage_recording.sh UC1` (or UC2) → a fresh, clean folder on the Desktop
- [ ] **≥ 50 GB free disk** (about 35 GB per 20 min)
- [ ] Close every app not in the topology; quit Terminal after staging
- [ ] Desktop clean: only the UC folder visible; Finder window ready
- [ ] Vary the UI compared with the previous recording: UC1 = Light mode, Dock bottom; UC2 = Dark mode, Dock left or auto-hide. Keep the default cursor size and colour
- [ ] Headset mic on, quiet room, water nearby
- [ ] VS Code open on the use-case folder with `Task Notes.md` shown as a preview **before** starting TaskRecorder
- [ ] Off camera, open any notebook once and check that the `Python 3.12 (ds-venv)` kernel appears in the kernel picker, then close the notebook and leave VS Code on the `Task Notes.md` preview
- [ ] No ChatGPT / Claude / Gemini / Copilot / Grammarly anywhere

## C. During the take (15:00–45:59, one continuous take)
- [ ] Task notes visible for a few seconds at the start
- [ ] **Before** each action: name the element and say why. **During:** say what's happening. **After:** confirm the result
- [ ] Never say "this / here / that". Name it ("the blue Run button on cell 4")
- [ ] Hover before clicking; trace text with the cursor; small circles for emphasis (don't overdo it); smooth curved movements
- [ ] Pause about 1 s after each click; one action at a time; wait for cells to finish
- [ ] Mouse and menus, not shortcuts (copy/paste are OK): cell ▶ Run button, not Shift+Enter
- [ ] Windows maximised or side by side; no window on top of another; minimise anything more than 25% covered
- [ ] No trial and error. If something fails, explain the fix calmly as an expert would

## D. After the take
- [ ] Watch the video; check the TaskRecorder screenshot count
- [ ] Every file in `Deliverables/` follows the `input N` / `artifact N` / `final output N` naming
- [ ] Zip the `Deliverables` folder → `Deliverables.zip` (off camera)
- [ ] Upload to Mercor Studio: `video.mp4`, the **unmodified** `recording_TIMESTAMP.zip`, `Deliverables.zip`, `Metadata.rtf`
- [ ] Run **both** AutoQC checks (files/recording and narration); fix or dispute every flag with a reason; complete the checklist; submit
- [ ] Pitch the next idea straight away; apply reviewer comments to the next task

<#
Copy a fresh, clean recording workspace next to the project folder before a take (or after a rehearsal).
Windows counterpart of stage_recording.sh. Every run creates a NEW version; nothing is moved or deleted.

    prep\stage_recording.cmd UC1      -> <parent of project>\Mercor_UC1\UC1_Cross_Sell_v1, _v2, ...
    prep\stage_recording.cmd UC2      -> <parent of project>\Mercor_UC2\UC2_Propensity_To_Pay_v1, _v2, ...

e.g. project C:\Users\you\Cnx\LLM_Training_recording -> C:\Users\you\Cnx\Mercor_UC1\UC1_Cross_Sell_v1
Set STAGE_DESTINATION to use a different parent folder.
#>
param(
    [Parameter(Mandatory = $true)][ValidateSet("UC1", "UC2")][string]$UseCase,
    [string]$Destination = $env:STAGE_DESTINATION
)
$ErrorActionPreference = "Stop"

$RepoDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $Destination) { $Destination = Split-Path $RepoDir -Parent }
$Name = if ($UseCase -eq "UC1") { "UC1_Cross_Sell" } else { "UC2_Propensity_To_Pay" }
$Src = Join-Path $RepoDir "recording_workspace\$Name"
$VenvPy = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPy)) { Write-Host "Run setup_windows.cmd first." -ForegroundColor Red; exit 1 }

$Group = Join-Path $Destination "Mercor_$UseCase"
New-Item -ItemType Directory -Force -Path $Group | Out-Null
# next free version number: v1, v2, ...
$Last = Get-ChildItem -Path $Group -Directory -Filter "$($Name)_v*" |
    ForEach-Object { if ($_.Name -match "_v(\d+)$") { [int]$Matches[1] } } | Measure-Object -Maximum
$Version = if ($Last.Count) { $Last.Maximum + 1 } else { 1 }
$Folder = "$($Name)_v$Version"
$Dest = Join-Path $Group $Folder

Copy-Item -Path $Src -Destination $Dest -Recurse
# empty working folders for the pipeline outputs (git does not keep empty folders)
if (Test-Path (Join-Path $Dest "Deliverables\1_Input")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Dest "Deliverables\3_Intermediate"), (Join-Path $Dest "Deliverables\4_Output") | Out-Null
}
# files from a downloaded ZIP carry Mark-of-the-Web, which makes LibreOffice / Firefox show
# "downloaded from the internet" warnings on camera
Get-ChildItem -Path $Dest -Recurse -File | Unblock-File

# VS Code workspace settings: AI features off, venv interpreter, readable font sizes
$VscodeDir = Join-Path $Dest ".vscode"
New-Item -ItemType Directory -Force -Path $VscodeDir | Out-Null
$Interpreter = ($VenvPy -replace "\\", "/")
$Settings = @"
{
  "chat.disableAIFeatures": true,
  "github.copilot.enable": { "*": false },
  "github.copilot.nextEditSuggestions.enabled": false,
  "editor.inlineSuggest.enabled": false,
  "python.defaultInterpreterPath": "$Interpreter",
  "python.terminal.activateEnvironment": true,
  "editor.fontSize": 15,
  "notebook.markup.fontSize": 15,
  "terminal.integrated.fontSize": 14,
  "workbench.startupEditor": "none",
  "files.exclude": { "**/.vscode": true, "**/.ipynb_checkpoints": true, "**/desktop.ini": true, "**/__pycache__": true, "Metadata.rtf": true },
  "workbench.editorAssociations": { "*.md": "vscode.markdown.preview.editor" },
  "jupyter.notebookFileRoot": "`${fileDirname}",
  "python.envFile": "`${workspaceFolder}/.vscode/kernel.env"
}
"@
[IO.File]::WriteAllText((Join-Path $VscodeDir "settings.json"), $Settings, (New-Object Text.UTF8Encoding $false))
# environment for the notebook kernel: silences joblib's long CPU-count warning on Windows 11
$Loky = [Environment]::GetEnvironmentVariable("LOKY_MAX_CPU_COUNT", "User")
if (-not $Loky) { $Loky = [Math]::Max(1, [int]$env:NUMBER_OF_PROCESSORS - 1) }
[IO.File]::WriteAllText((Join-Path $VscodeDir "kernel.env"), "LOKY_MAX_CPU_COUNT=$Loky`n", (New-Object Text.UTF8Encoding $false))
(Get-Item $VscodeDir).Attributes = (Get-Item $VscodeDir).Attributes -bor [IO.FileAttributes]::Hidden

Write-Host "Staged clean workspace: $Dest"
Get-ChildItem -Path (Join-Path $Dest "Deliverables") -Recurse -Depth 1 -Name | Where-Object { $_ -notmatch "__pycache__" }
Write-Host ""
Write-Host "Open it in VS Code:  File > Open Folder... > $Group > $Folder"
Write-Host "Then follow PART 2 of the recording script (UC1_RECORDING_SCRIPT.md / UC2_RECORDING_SCRIPT.md)"

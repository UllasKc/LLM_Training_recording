<#
Copy a fresh, clean recording workspace to the Desktop before a take (or after a rehearsal).
Windows counterpart of stage_recording.sh.

    prep\stage_recording.cmd UC1      -> Desktop\UC1_Cross_Sell
    prep\stage_recording.cmd UC2      -> Desktop\UC2_Propensity_To_Pay

Anything already on the Desktop with that name (e.g. a rehearsal) is moved to
%USERPROFILE%\Rehearsal_Backups\<name>_<timestamp> - nothing is deleted.
#>
param(
    [Parameter(Mandatory = $true)][ValidateSet("UC1", "UC2")][string]$UseCase,
    # the real Desktop, including when it is redirected to OneDrive
    [string]$Destination = $(if ($env:STAGE_DESTINATION) { $env:STAGE_DESTINATION } else { [Environment]::GetFolderPath("Desktop") })
)
$ErrorActionPreference = "Stop"

$RepoDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Name = if ($UseCase -eq "UC1") { "UC1_Cross_Sell" } else { "UC2_Propensity_To_Pay" }
$Src = Join-Path $RepoDir "recording_workspace\$Name"
$Dest = Join-Path $Destination $Name
$VenvPy = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPy)) { Write-Host "Run setup_windows.cmd first." -ForegroundColor Red; exit 1 }

if (Test-Path $Dest) {
    $BackupRoot = Join-Path $env:USERPROFILE "Rehearsal_Backups"
    New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
    $Backup = Join-Path $BackupRoot ("{0}_{1}" -f $Name, (Get-Date -Format "yyyyMMdd_HHmmss"))
    Move-Item -Path $Dest -Destination $Backup
    Write-Host "Moved previous $Name to $Backup"
}

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
  "jupyter.notebookFileRoot": "`${fileDirname}"
}
"@
[IO.File]::WriteAllText((Join-Path $VscodeDir "settings.json"), $Settings, (New-Object Text.UTF8Encoding $false))
(Get-Item $VscodeDir).Attributes = (Get-Item $VscodeDir).Attributes -bor [IO.FileAttributes]::Hidden

Write-Host "Staged clean workspace: $Dest"
Get-ChildItem -Path (Join-Path $Dest "Deliverables") -Recurse -Depth 1 -Name | Where-Object { $_ -notmatch "__pycache__" }
Write-Host ""
Write-Host "Open it in VS Code:  File > Open Folder... > Desktop > $Name"
Write-Host "Then follow PART 2 of the recording script (UC1_RECORDING_SCRIPT.md / UC2_RECORDING_SCRIPT.md)"

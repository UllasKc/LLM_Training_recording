<#
One-time setup on a Windows laptop (practice / internal-review recordings).

    setup_windows.cmd                      (double-click, or run from a terminal)
    powershell -ExecutionPolicy Bypass -File setup_windows.ps1

Creates .venv with Python 3.12, installs the same locked packages as the Mac
(binary wheels only), registers the Jupyter kernel "Python 3.12 (ds-venv)" for
VS Code, and verifies everything. Safe to re-run.

Behind a corporate proxy / internal PyPI mirror, set these first (pip reads them):
    $env:PIP_INDEX_URL = "https://<your-artifactory>/api/pypi/pypi/simple"
    $env:HTTPS_PROXY   = "http://proxy.company.com:8080"
#>
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$RepoDir = (Get-Location).Path
$KernelName = "ds-venv"
$KernelLabel = "Python 3.12 (ds-venv)"

function Say([string]$Message) { Write-Host ""; Write-Host "==> $Message" -ForegroundColor Cyan }
function Fail([string]$Message) { Write-Host ""; Write-Host "ERROR: $Message" -ForegroundColor Red; exit 1 }
function Invoke-Checked([string]$Exe, [string[]]$Arguments, [string]$What) {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { Fail "$What failed (exit code $LASTEXITCODE)." }
}

Say "Checking machine"
Write-Host "Windows $([Environment]::OSVersion.Version) on $env:PROCESSOR_ARCHITECTURE"

# Some packages contain ~190-character file paths; with the default 260-character Windows
# limit the install fails unless the project folder path is short.
$LongPaths = $false
try {
    $LongPaths = (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -ErrorAction Stop).LongPathsEnabled -eq 1
} catch { }
if (-not $LongPaths -and $RepoDir.Length -gt 50) {
    Fail ("The project folder path is too long for Windows ($($RepoDir.Length) characters, limit 50 here):`n" +
          "  $RepoDir`n" +
          "  Move or clone the project to a short path, e.g.  C:\Users\<you>\LLM_Training_recording  or  C:\LLM_Training_recording`n" +
          "  (or ask IT to enable Windows long-path support), then re-run setup_windows.cmd")
}
Write-Host "Project folder: $RepoDir (long paths enabled: $LongPaths)"

Say "Finding Python 3.12"
$Candidates = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    try {
        $Found = & py -3.12 -c "import sys; print(sys.executable)"
        if ($LASTEXITCODE -eq 0 -and $Found) { $Candidates += $Found.Trim() }
    } catch { }
}
foreach ($Cmd in @(Get-Command python -All -ErrorAction SilentlyContinue)) {
    try {
        $Found = & $Cmd.Source -c "import sys; print(sys.executable if sys.version_info[:2] == (3, 12) else '')"
        if ($LASTEXITCODE -eq 0 -and $Found) { $Candidates += $Found.Trim() }
    } catch { }
}
$Candidates += @(
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "C:\Program Files\Python312\python.exe"
)
$Py = $null
foreach ($c in $Candidates) { if ($c -and (Test-Path $c)) { $Py = $c; break } }
if (-not $Py) {
    Fail ("Python 3.12 not found.`n" +
          "  Install it from https://www.python.org/downloads/windows/ (latest 3.12.x, 'Windows installer (64-bit)').`n" +
          "  In the installer tick 'Add python.exe to PATH'; 'Install Now' installs for your user only (no admin needed).`n" +
          "  Or: winget install --id Python.Python.3.12 --scope user`n" +
          "  Then open a NEW terminal and re-run setup_windows.cmd")
}
$PyInfo = & $Py -c "import platform; print(platform.python_version(), platform.machine())"
Write-Host "Using $Py ($PyInfo)"
if ($PyInfo -notmatch "^3\.12\.") { Fail "Python 3.12 is required; found $PyInfo." }
if ($PyInfo -match "ARM64") {
    Fail ("ARM64 Python detected. Several data-science packages have no Windows-ARM wheels.`n" +
          "  Install the x64 'Windows installer (64-bit)' of Python 3.12 instead (it runs fine on ARM laptops).")
}

Say "Creating virtual environment in .venv"
$VenvPy = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPy)) { Invoke-Checked $Py @("-m", "venv", ".venv") "Creating the virtual environment" }
Invoke-Checked $VenvPy @("-m", "pip", "install", "--quiet", "--upgrade", "pip") "Upgrading pip"

Say "Installing locked packages (binary wheels only - nothing is compiled)"
Invoke-Checked $VenvPy @("-m", "pip", "install", "--quiet", "--only-binary=:all:", "-r", "requirements-lock.txt") "Package install"

Say "Registering Jupyter kernel '$KernelLabel' for VS Code"
Invoke-Checked $VenvPy @("-m", "ipykernel", "install", "--user", "--name", $KernelName, "--display-name", $KernelLabel) "Kernel registration"

# scikit-learn/joblib print a long CPU-count warning on Windows 11 (no wmic) unless
# LOKY_MAX_CPU_COUNT is below the logical core count; set it to the physical core count
$Logical = [int]$env:NUMBER_OF_PROCESSORS
$Physical = (Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum
if (-not $Physical -or $Physical -ge $Logical) { $Physical = [Math]::Max(1, $Logical - 1) }
[Environment]::SetEnvironmentVariable("LOKY_MAX_CPU_COUNT", "$Physical", "User")
$env:LOKY_MAX_CPU_COUNT = "$Physical"

Say "Verifying setup"
Invoke-Checked $VenvPy @("prep\verify_setup.py") "Verification"

Write-Host ""
Write-Host "Setup complete."
Write-Host "  Interpreter : $VenvPy"
Write-Host "  VS Code     : pick kernel `"$KernelLabel`" in the notebook kernel picker"
Write-Host "Next, before each take:"
Write-Host "  prep\stage_recording.cmd UC1     (or UC2)"

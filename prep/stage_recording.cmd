@echo off
rem Usage: prep\stage_recording.cmd UC1   (or UC2)
rem Double-clicking it (no argument) shows a menu and waits at the end.
setlocal
set "UC=%~1"
set "INTERACTIVE="
if not "%UC%"=="" goto run
set "INTERACTIVE=1"
echo.
echo Which use case do you want to stage? (creates a new _vN folder next to the project)
echo    1 = UC1  Cross-Sell model
echo    2 = UC2  Propensity-to-Pay model
echo.
set /p "CHOICE=Type 1 or 2 and press Enter: "
if "%CHOICE%"=="1" set "UC=UC1"
if "%CHOICE%"=="2" set "UC=UC2"
if /i "%CHOICE%"=="UC1" set "UC=UC1"
if /i "%CHOICE%"=="UC2" set "UC=UC2"
if "%UC%"=="" (
  echo Invalid choice "%CHOICE%". Nothing was changed.
  goto done
)
:run
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stage_recording.ps1" -UseCase %UC%
:done
if defined INTERACTIVE (
  echo.
  pause
)

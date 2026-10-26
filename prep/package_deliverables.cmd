@echo off
rem Validate a finished take and build Deliverables.zip (run OFF camera, after recording).
rem Usage: prep\package_deliverables.cmd UC1   (or UC2). Double-click shows a menu.
setlocal
set "UC=%~1"
set "INTERACTIVE="
if not "%UC%"=="" goto run
set "INTERACTIVE=1"
echo.
echo Which use case do you want to package?
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
"%~dp0..\.venv\Scripts\python.exe" "%~dp0package_deliverables.py" %UC% %2 %3
:done
if defined INTERACTIVE (
  echo.
  pause
)

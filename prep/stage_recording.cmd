@echo off
rem Usage: prep\stage_recording.cmd UC1   (or UC2)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stage_recording.ps1" %*

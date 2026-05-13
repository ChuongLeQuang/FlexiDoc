@echo off
chcp 65001 >nul
set PYTHON_CMD=python
if exist ".venv\Scripts\python.exe" set PYTHON_CMD=.venv\Scripts\python.exe
echo 🛡️ Dang chay kiem tra tu dong...
%PYTHON_CMD% auto_checks.py
if %ERRORLEVEL% neq 0 ( echo ❌ Kiem tra that bai! ) else ( echo ✅ Ma nguon an toan! )
pause

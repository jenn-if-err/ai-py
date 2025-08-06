@echo off
REM Gemini CLI App Launcher
REM Usage: gemini.bat "Your prompt here"
REM   or:  echo "Your prompt" | gemini.bat

cd /d "%~dp0"

if "%~1"=="" (
    REM No arguments, read from stdin
    C:/Users/User/alphaus/py-ai/.venv/Scripts/python.exe gemini_cli.py
) else (
    REM Arguments provided, use them as prompt
    echo %* | C:/Users/User/alphaus/py-ai/.venv/Scripts/python.exe gemini_cli.py
)

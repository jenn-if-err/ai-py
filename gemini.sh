#!/bin/bash
# Gemini CLI App Launcher for WSL Ubuntu
# Usage: ./gemini.sh "Your prompt here"
#   or:  echo "Your prompt" | ./gemini.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv-wsl" ]; then
    echo "Error: WSL virtual environment not found."
    echo "Please run the setup commands first:"
    echo "  python3 -m venv .venv-wsl"
    echo "  source .venv-wsl/bin/activate"
    echo "  pip install requests"
    exit 1
fi

# Activate virtual environment
source .venv-wsl/bin/activate

# Check if arguments were provided
if [ $# -eq 0 ]; then
    # No arguments, read from stdin
    python main.py
else
    # Arguments provided, use them as prompt
    echo "$*" | python main.py
fi

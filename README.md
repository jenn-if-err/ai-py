A Python CLI application that sends prompts to the Google Gemini AI API and displays the responses.

## Features

- Reads prompts from stdin
- Sends requests to Gemini AI API via HTTPS
- Displays formatted AI responses

---

## Prerequisites

1. Python 3.6 or higher
2. A Google AI Studio API key for Gemini
3. The `requests` library

## API Information

This app uses the Google Gemini 1.5 Flash model via the REST API endpoint:
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- Method: POST
- Authentication: API key as query parameter
- Content-Type: application/json

---

# WSL Ubuntu / Linux 
## Setup

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:
   ```bash
   # Temporary (current session)
   export GEMINI_API_KEY="your_api_key_here"
   # Permanent
   echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```
3. Install dependencies system-wide (no venv):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-requests
   ```
   Or, if you prefer a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests
   ```
4. (Optional) To use the google-generativeai (genai) package:
   ```bash
   pip install google-generativeai
   ```

---

## Usage

#### Interactive Mode
```bash
python3 main.py
```
Type your prompt and press Ctrl+D to send.

#### Pipe Input
```bash
echo "What is the capital of Philippines?" | python3 main.py
```

#### File Input
```bash
cat prompt.txt | python3 main.py
```

#### Using the Bash Script
```bash
chmod +x gemini.sh
./gemini.sh "What is machine learning?"
```

---

## Examples
```bash
# Simple question
echo "Explain quantum computing in simple terms" | python3 main.py
# Analysis
cat data.txt | python3 main.py
# Multiple lines
cat << EOF | python3 main.py
Write a Python script that:
1. Reads a CSV file
2. Performs basic data analysis
3. Creates visualizations
EOF
# Using bash script
./gemini.sh "What are the latest trends in AI?"
```

---

##  Testing
```bash
# Test environment
chmod +x test_env_wsl.sh
./test_env_wsl.sh
# Test the app
echo "Hello, Gemini!" | python3 main.py
```

---
# Windows
##  Setup

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:
   ```powershell
   # Temporary (current session)
   $env:GEMINI_API_KEY="your_api_key_here"
   # Permanent
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_api_key_here", "User")
   ```
3. Install dependencies system-wide (no venv):
   ```powershell
   pip install requests
   ```
   Or, if you prefer a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install requests
   ```
4. (Optional) To use the google-generativeai (genai) package:
   ```powershell
   pip install google-generativeai
   ```

---

## Usage

#### Interactive Mode
```powershell
python main.py
```
Type your prompt and press Ctrl+Z then Enter to send.

#### Pipe Input
```powershell
echo "What is the capital of Philippines?" | python main.py
```

#### File Input
```powershell
Get-Content prompt.txt | python main.py
```

---

## Examples
```powershell
# Simple question
echo "Explain quantum computing in simple terms" | python main.py
# Analysis
Get-Content data.txt | python main.py
```

---

## Testing
```powershell
# Test environment
python test_env.py
# Test the app
echo "Hello, Gemini!" | python main.py
```

---


### Usage with --use-genai flag:
```sh
python3 main.py --use-genai --prompt "What is the capital of Philippines?"
```

If you do not provide `--prompt`, the script will read from stdin as before.

---


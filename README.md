# ai-py

A Python CLI application that sends prompts to Google Gemini and OpenAI (ChatGPT) APIs and displays the responses.

## Features

- Reads prompts from stdin or --prompt flag
- Sends requests to Gemini AI API or OpenAI ChatGPT API
- Supports both REST and google-generativeai (genai) backends for Gemini
- Displays formatted AI responses

---

## Prerequisites

1. Python 3.6 or higher
2. A Google AI Studio API key for Gemini (for Gemini usage)
3. An OpenAI API key (for ChatGPT usage)
4. The `requests` library

## API Information

### Gemini API
Uses the Google Gemini 1.5 Flash model via the REST API endpoint:
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- Method: POST
- Authentication: API key as query parameter
- Content-Type: application/json

### OpenAI API
Uses the OpenAI ChatGPT API (gpt-3.5-turbo by default):
- Endpoint: `https://api.openai.com/v1/chat/completions`
- Method: POST
- Authentication: Bearer token via `OPENAI_API_KEY` environment variable

---

# WSL Ubuntu / Linux 
## Setup

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variables:
   ```bash
   # Gemini (Google)
   export GEMINI_API_KEY="your_gemini_api_key_here"
   # OpenAI
   export OPENAI_API_KEY="your_openai_api_key_here"
   # To make permanent, add to ~/.bashrc or ~/.zshrc
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
python3 main.py --prompt "What is the capital of Philippines?"
```
Type your prompt and press Ctrl+D to send.

#### Use OpenAI ChatGPT
```bash
python3 main.py --use-chatgpt --prompt "What is the capital of Philippines?"
```

#### Pipe Input
```bash
echo "What is the capital of Philippines?" | python3 main.py
```

#### File Input
```bash
cat prompt.txt | python3 main.py
```

#### Using the Bash Script (Gemini only)
```bash
chmod +x gemini.sh
./gemini.sh "What is machine learning?"
```

---

## Examples
```bash
# Simple question (Gemini)
echo "Explain quantum computing in simple terms" | python3 main.py
# Simple question (OpenAI)
echo "Explain quantum computing in simple terms" | python3 main.py --use-chatgpt
# Analysis
cat data.txt | python3 main.py
# Multiple lines
cat << EOF | python3 main.py
Write a Python script that:
1. Reads a CSV file
2. Performs basic data analysis
3. Creates visualizations
EOF
# Using bash script (Gemini only)
./gemini.sh "What are the latest trends in AI?"
```

---
##  Testing
```bash
# Test environment
chmod +x test_env_wsl.sh
./test_env_wsl.sh
# Test the app
# Gemini
 echo "Hello, Gemini!" | python3 main.py
# OpenAI
 echo "Hello, OpenAI!" | python3 main.py --use-chatgpt
```

---
# Windows
##  Setup

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variables:
   ```powershell
   # Gemini (Google)
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_gemini_api_key_here", "User")
   # OpenAI
   $env:OPENAI_API_KEY="your_openai_api_key_here"
   [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_openai_api_key_here", "User")
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
python main.py --prompt "What is the capital of Philippines?"
```
Type your prompt and press Ctrl+Z then Enter to send.

#### Use OpenAI ChatGPT
```powershell
python main.py --use-chatgpt --prompt "What is the capital of Philippines?"
```

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
# Simple question (Gemini)
echo "Explain quantum computing in simple terms" | python main.py
# Simple question (OpenAI)
echo "Explain quantum computing in simple terms" | python main.py --use-chatgpt
# Analysis
Get-Content data.txt | python main.py
```

---

## Testing
```powershell
# Test environment
python test_env.py
# Test the app
# Gemini
echo "Hello, Gemini!" | python main.py
# OpenAI
echo "Hello, OpenAI!" | python main.py --use-chatgpt
```

---


### Usage with --use-genai flag (Gemini only):
```sh
python3 main.py --use-genai --prompt "What is the capital of Philippines?"
```

### Usage with --use-chatgpt flag (OpenAI):
```sh
python3 main.py --use-chatgpt --prompt "What is the capital of Philippines?"
```

If you do not provide `--prompt`, the script will read from stdin as before.


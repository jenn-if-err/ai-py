# Gemini AI CLI App

A simple Python CLI application that sends prompts to the Google Gemini AI API and displays the responses.

## Features

- Reads prompts from stdin
- Sends requests to Gemini AI API via HTTPS
- Displays formatted AI responses


## Prerequisites

1. Python 3.6 or higher
2. A Google AI Studio API key for Gemini
3. The `requests` library (installed automatically)



1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set the environment variable:
   ```powershell
   # Windows PowerShell - Temporary (current session)
   $env:GEMINI_API_KEY="your_api_key_here"
   
   # Windows PowerShell - Permanent
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_api_key_here", "User")
   ```

3. Install dependencies (if not already installed):
   ```powershell
   .\.venv\Scripts\python.exe -m pip install requests
   ```

### WSL Ubuntu Setup

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set the environment variable:
   ```bash
   # WSL Ubuntu - Temporary (current session)
   export GEMINI_API_KEY="your_api_key_here"
   
   # WSL Ubuntu - Permanent (add to ~/.bashrc or ~/.profile)
   echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Create Python virtual environment and install dependencies:

## Usage

### Windows PowerShell

#### Interactive Mode
Run the script and type your prompt:
```powershell
.\.venv\Scripts\python.exe gemini_cli.py
```
Then type your prompt and press Ctrl+Z followed by Enter to send.

#### Pipe Input
You can pipe text directly to the application:
```powershell
echo "What is the capital of France?" | .\.venv\Scripts\python.exe gemini_cli.py
```

#### File Input
Send the contents of a file as a prompt:
```powershell
Get-Content prompt.txt | .\.venv\Scripts\python.exe gemini_cli.py
```

#### Using the Batch Script (Windows)
For convenience, you can use the included batch script:
```powershell
# Interactive mode
.\gemini.bat

# Direct prompt
.\gemini.bat "What is machine learning?"

# Pipe input
echo "Explain quantum computing" | .\gemini.bat
```

### WSL Ubuntu

#### Interactive Mode
```bash
# Activate virtual environment first
source .venv-wsl/bin/activate

# Run the script
python gemini_cli.py
```
Then type your prompt and press Ctrl+D to send.

#### Pipe Input
```bash
# Activate virtual environment first
source .venv-wsl/bin/activate

# Pipe input
echo "What is the capital of France?" | python gemini_cli.py
```

#### File Input
```bash
# Activate virtual environment first
source .venv-wsl/bin/activate

# File input
cat prompt.txt | python gemini_cli.py
```

#### Using the Bash Script (WSL)
For convenience, you can use the included bash script:
```bash
# Make executable (first time only)
chmod +x gemini.sh

# Interactive mode
./gemini.sh

# Direct prompt
./gemini.sh "What is machine learning?"

# Pipe input
echo "Explain quantum computing" | ./gemini.sh
```


### Windows PowerShell Examples
```powershell
# Simple question
echo "Explain quantum computing in simple terms" | .\.venv\Scripts\python.exe gemini_cli.py

# Code generation
echo "Write a Python function to calculate fibonacci numbers" | .\.venv\Scripts\python.exe gemini_cli.py

# Analysis
Get-Content data.txt | .\.venv\Scripts\python.exe gemini_cli.py

# Using batch script
.\gemini.bat "What are the latest trends in AI?"
```

### WSL Ubuntu Examples
```bash
# Activate environment first
source .venv-wsl/bin/activate

# Simple question
echo "Explain quantum computing in simple terms" | python gemini_cli.py

# Code generation
echo "Write a Python function to calculate fibonacci numbers" | python gemini_cli.py

# Analysis
cat data.txt | python gemini_cli.py

# Multiple lines
cat << EOF | python gemini_cli.py
Write a Python script that:
1. Reads a CSV file
2. Performs basic data analysis
3. Creates visualizations
EOF
```

## Testing Your Setup

### Windows PowerShell
```powershell
# Test environment
C:/Users/User/alphaus/py-ai/.venv/Scripts/python.exe test_env.py

# Test the app
echo "Hello, Gemini!" | C:/Users/User/alphaus/py-ai/.venv/Scripts/python.exe gemini_cli.py
```

### WSL Ubuntu
```bash
# Test environment
chmod +x test_env_wsl.sh
./test_env_wsl.sh

# Test the app
source .venv-wsl/bin/activate
echo "Hello, Gemini!" | python gemini_cli.py


This app uses the Google Gemini 1.5 Flash model via the REST API endpoint:
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- Method: POST
- Authentication: API key as query parameter
- Content-Type: application/json


# ai-py

A Python CLI application for interacting with Google Gemini and OpenAI (ChatGPT) APIs used for testing vortex tracing agent at https://github.com/flowerinthenight/vortex-agent.git

---

## Features
- Flexible CLI: prompt, context, and chatbot modes
- Supports Gemini (REST or google-generativeai) and OpenAI (ChatGPT)
- Easy switching between backends with flags
- Works on Linux, WSL, and Windows

---

# Setup

## Linux / WSL
1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. (Optional) Get your OpenAI API key from [OpenAI](https://platform.openai.com/api-keys)
3. Set environment variables:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export OPENAI_API_KEY="your_openai_api_key_here"  # if using ChatGPT
   # To make permanent, add to ~/.bashrc or ~/.zshrc
   ```
4. Install dependencies:
   - System-wide (no venv):
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-venv python3-requests
     ```
   - Use a virtual environment:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install requests openai 
     pip install -q -U google-genai

     ```

## Windows
1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. (Optional) Get your OpenAI API key from [OpenAI](https://platform.openai.com/api-keys)
3. Set environment variables:
   ```powershell
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_gemini_api_key_here", "User")
   $env:OPENAI_API_KEY="your_openai_api_key_here"
   [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_openai_api_key_here", "User")
   ```
4. Install dependencies:
   - System-wide (no venv):
     ```powershell
     pip install requests openai
     ```
   - Or, using a virtual environment:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install requests openai
     ```
5. (Optional) For Gemini package backend:
   ```powershell
   pip install -q -U google-genai
   ```

---

# Usage

## CLI Flags (main.py)
- `--prompt "<your question>"` : Send a single prompt (default: Gemini)
- `--use-chatgpt` : Use OpenAI ChatGPT instead of Gemini
- `--use-genai` : Use google-generativeai package for Gemini backend
- `--use-context` : Use context.txt and system instruction for advanced summarization (Gemini only)

## Example Commands
- Simple Gemini prompt:
  ```bash
  python3 main.py --prompt "What is the capital of Philippines?"
  ```
- Simple ChatGPT prompt:
  ```bash
  python3 main.py --use-chatgpt --prompt "What is the capital of Philippines?"
  ```
- Pipe input:
  ```bash
  echo "Explain quantum computing" | python3 main.py
  ```
- Use context file (Gemini advanced):
  ```bash
  python3 main.py --use-context
  ```
- Use google-generativeai backend:
  ```bash
  python3 main.py --use-genai --prompt "Summarize this text."
  ```

## Chatbot Mode (chat_cli.py)
- Start Gemini chatbot:
  ```bash
  python3 chat_cli.py
  ```
- Start ChatGPT chatbot:
  ```bash
  python3 chat_cli.py --use-chatgpt
  ```
- Type your message and press Enter. Type `exit` or `quit` to end the session.

## Sample Questions
- "Summarize the following meeting notes."
- "What are the latest trends in AI?"
- "Write a Python script that reads a CSV file and plots a chart."
- "How do I set up a virtual environment in Python?"

---

# Testing
- Linux:
  ```bash
  chmod +x test_env_wsl.sh
  ./test_env_wsl.sh
  echo "Hello, Gemini!" | python3 main.py
  echo "Hello, OpenAI!" | python3 main.py --use-chatgpt
  ```
- Windows:
  ```powershell
  python test_env.py
  echo "Hello, Gemini!" | python main.py
  echo "Hello, OpenAI!" | python main.py --use-chatgpt
  ```

---

# Notes
- If you do not provide `--prompt`, the script will read from stdin.
- For advanced summarization, use `--use-context` (requires context.txt).
- For chatbot mode, use `chat_cli.py` (Gemini by default, ChatGPT with --use-chatgpt).
- All API keys must be set as environment variables.


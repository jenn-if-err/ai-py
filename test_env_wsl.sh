#!/bin/bash
# Test script to verify WSL Ubuntu environment setup

echo "Testing WSL Ubuntu environment setup..."

# Check if API key is set
if [ -n "$GEMINI_API_KEY" ]; then
    echo "GEMINI_API_KEY is set"
    echo "  Key length: ${#GEMINI_API_KEY} characters"
    echo "  Starts with: ${GEMINI_API_KEY:0:10}..."
else
    echo "GEMINI_API_KEY is not set"
    echo "  Please set your Gemini API key:"
    echo "  export GEMINI_API_KEY=\"your_api_key_here\""
    echo "  Or add it to ~/.bashrc for persistence"
    exit 1
fi

# Check if virtual environment exists
if [ -d ".venv-wsl" ]; then
    echo "WSL virtual environment exists"
    
    # Activate virtual environment
    source .venv-wsl/bin/activate
    
    # Check Python version
    python_version=$(python --version 2>&1)
    echo "  Python: $python_version"
    
    # Test imports
    if python -c "import requests" 2>/dev/null; then
        requests_version=$(python -c "import requests; print(requests.__version__)" 2>/dev/null)
        echo "requests library is available"
        echo "  Version: $requests_version"
    else
        echo "requests library is not installed"
        echo "  Please install it: pip install requests"
        exit 1
    fi
    
else
    echo "✗ WSL virtual environment not found"
    echo "  Please create it:"
    echo "  python3 -m venv .venv-wsl"
    echo "  source .venv-wsl/bin/activate"
    echo "  pip install requests"
    exit 1
fi

echo ""
echo "✓ WSL Ubuntu environment is ready!"
echo ""
echo "To test the CLI app, run:"
echo "  source .venv-wsl/bin/activate"
echo "  echo \"What is Python?\" | python main.py"
echo ""
echo "Or use the convenience script:"
echo "  chmod +x gemini.sh"
echo "  ./gemini.sh \"What is Python?\""

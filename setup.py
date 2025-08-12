#!/usr/bin/env python3
"""
Cross-platform setup script for ai-py
Works on Windows PowerShell, WSL Ubuntu, and native Linux/macOS
"""

import os
import sys
import subprocess
import platform


def detect_environment():
    """Detect the current environment"""
    system = platform.system()
    
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        # Check if running in WSL
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return "wsl"
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        return "unknown"


def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("Python 3.6 or higher is required")
        return False
    
    print(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_api_key():
    """Check if API key is set"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("GEMINI_API_KEY is set")
        print(f"   Key length: {len(api_key)} characters")
        return True
    else:
        print("GEMINI_API_KEY is not set")
        return False


def setup_environment(env_type):
    """Set up the environment based on the detected type"""
    print(f"\nSetting up environment for {env_type}...")
    
    if env_type == "windows":
        return setup_windows()
    elif env_type == "wsl":
        return setup_wsl()
    elif env_type in ["linux", "macos"]:
        return setup_unix()
    else:
        print("❌ Unsupported environment")
        return False


def setup_windows():
    """Setup for Windows PowerShell"""
    print("Setting up for Windows PowerShell...")
    
    # Create virtual environment
    if not os.path.exists(".venv"):
        print("Creating virtual environment...")
        result = subprocess.run([sys.executable, "-m", "venv", ".venv"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to create virtual environment: {result.stderr}")
            return False
    
    # Install packages
    pip_path = os.path.join(".venv", "Scripts", "pip.exe")
    if os.path.exists(pip_path):
        print("Installing requests...")
        result = subprocess.run([pip_path, "install", "requests"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to install requests: {result.stderr}")
            return False
    
    print("Windows setup complete!")
    print("\nUsage:")
    print("   .venv\\Scripts\\python.exe main.py")
    return True


def setup_wsl():
    """Setup for WSL Ubuntu"""
    print("Setting up for WSL Ubuntu...")
    
    # Create virtual environment
    if not os.path.exists(".venv-wsl"):
        print("Creating WSL virtual environment...")
        result = subprocess.run(["python3", "-m", "venv", ".venv-wsl"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to create virtual environment: {result.stderr}")
            return False
    
    # Install packages
    pip_path = os.path.join(".venv-wsl", "bin", "pip")
    if os.path.exists(pip_path):
        print("Installing requests...")
        result = subprocess.run([pip_path, "install", "requests"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to install requests: {result.stderr}")
            return False
    
    # Make scripts executable
    scripts = ["gemini.sh", "test_env_wsl.sh"]
    for script in scripts:
        if os.path.exists(script):
            os.chmod(script, 0o755)
    
    print("WSL setup complete!")
    print("\nUsage:")
    print("   source .venv-wsl/bin/activate")
    print("   python gemini_cli.py")
    print("   ./gemini.sh \"Your prompt here\"")
    return True


def setup_unix():
    """Setup for Linux/macOS"""
    print("Setting up for Linux/macOS...")
    
    # Create virtual environment
    if not os.path.exists(".venv-unix"):
        print("Creating virtual environment...")
        result = subprocess.run(["python3", "-m", "venv", ".venv-unix"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to create virtual environment: {result.stderr}")
            return False
    
    # Install packages
    pip_path = os.path.join(".venv-unix", "bin", "pip")
    if os.path.exists(pip_path):
        print("Installing requests...")
        result = subprocess.run([pip_path, "install", "requests"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to install requests: {result.stderr}")
            return False
    
    print("Unix setup complete!")
    print("\nUsage:")
    print("   source .venv-unix/bin/activate")
    print("   python gemini_cli.py")
    return True


def print_api_key_instructions(env_type):
    """Print API key setup instructions"""
    print("\nAPI Key Setup:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Set the environment variable:")
    
    if env_type == "windows":
        print("   # PowerShell (temporary)")
        print("   $env:GEMINI_API_KEY=\"your_api_key_here\"")
        print("   # PowerShell (permanent)")
        print("   [Environment]::SetEnvironmentVariable(\"GEMINI_API_KEY\", \"your_api_key_here\", \"User\")")
    else:
        print("   # Bash (temporary)")
        print("   export GEMINI_API_KEY=\"your_api_key_here\"")
        print("   # Bash (permanent)")
        print("   echo 'export GEMINI_API_KEY=\"your_api_key_here\"' >> ~/.bashrc")
        print("   source ~/.bashrc")


def main():
    """Main setup function"""
    print("ai-py Setup")
    print("=" * 50)
    
    # Detect environment
    env_type = detect_environment()
    print(f"Detected environment: {env_type}")
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Check API key
    api_key_set = check_api_key()
    
    # Setup environment
    if setup_environment(env_type):
        print("\nSetup completed successfully!")
        
        if not api_key_set:
            print_api_key_instructions(env_type)
            print("\nDon't forget to set your API key before using the app!")
        else:
            print("\nYou're ready to use the ai-py app!")
            
        print(f"\nSee README.md for detailed usage instructions")
    else:
        print("\nSetup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Blood Cancer Dashboard - Setup & Launch Script
Installs dependencies and runs the Streamlit dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("\n" + "="*78)
    print("🩸  Blood Cancer Analysis Dashboard - Setup & Launch".center(78))
    print("="*78 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, but you have Python {version.major}.{version.minor}")
        print("Please download Python 3.8+ from https://www.python.org/")
        sys.exit(1)
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} detected")

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required libraries...")
    print("   (This may take 2-3 minutes on first run)\n")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ requirements.txt not found at {requirements_file}")
        sys.exit(1)
    
    try:
        # Upgrade pip
        print("   Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        print("   Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        
        print("\n✅ All libraries installed successfully!\n")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install requirements: {e}")
        print("Please check your internet connection and try again.")
        sys.exit(1)

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching Blood Cancer Analysis Dashboard...")
    print("   Opening in your default browser at http://localhost:8501\n")
    
    dashboard_file = Path(__file__).parent / "dashboard.py"
    
    if not dashboard_file.exists():
        print(f"❌ dashboard.py not found at {dashboard_file}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_file)])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard closed. Goodbye!")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        sys.exit(1)

def main():
    """Main setup and launch function"""
    try:
        print_header()
        check_python_version()
        install_requirements()
        launch_dashboard()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

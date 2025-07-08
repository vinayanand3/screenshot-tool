#!/usr/bin/env python3
"""
Installation script for Advanced Screen Capture Tool
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows)"""
    if os.name == 'nt':  # Windows
        try:
            import winreg
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop_path, "Screenshot Tool.bat")
            
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\ncd /d "{os.getcwd()}"\npython screenshot.py\npause')
            
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            return True
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")
            return False
    else:
        print("ℹ️  Desktop shortcut creation is only available on Windows")
        return True

def main():
    """Main installation function"""
    print("🚀 Advanced Screen Capture Tool - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the tool: python screenshot.py")
    print("2. Or use the desktop shortcut (Windows)")
    print("3. Check the README.md for usage instructions")
    print("\n💡 Tips:")
    print("- Press Ctrl+, to open settings")
    print("- Use Enter to capture, Escape to cancel")
    print("- Try the annotation tools after selecting an area")

if __name__ == "__main__":
    main() 
import PyInstaller.__main__
import os
import shutil
import sys
import re
import platform

def get_version():
    """Get version from VERSION file or git tag"""
    try:
        # First try to read from VERSION file
        with open('VERSION', 'r') as f:
            version = f.read().strip()
            return version
    except:
        # Fallback to git tag
        try:
            with os.popen('git describe --tags --abbrev=0') as stream:
                version = stream.read().strip()
            if not version:
                return '1.0.0'
            version = re.sub('^v', '', version)
            return version
        except:
            return '1.0.0'

# Get current version
version = get_version()
print(f"Building version: {version}")

def check_requirements():
    """Check if all required packages are installed for macOS"""
    try:
        import PyQt5
        import pyautogui
        import AppKit
        import Quartz
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("Please run: pip install -r requirements_mac.txt")
        sys.exit(1)

# Check requirements first
check_requirements()

# Ensure we're running on macOS
if platform.system() != 'Darwin':
    print("Error: This script is intended to be run on macOS only.")
    sys.exit(1)

# Clean previous builds
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Create executable with PyInstaller
print("Building macOS application...")
PyInstaller.__main__.run([
    'spirited_away_mac.py',
    '--name=SpiritedAway',
    '--onefile',
    '--windowed',
    '--icon=./images/XD.png',  # macOS can use PNG directly
    '--add-data=./images/XD.png:images/',  # Note the colon instead of semicolon for macOS
    '--hidden-import=pyautogui',
    '--hidden-import=AppKit',
    '--hidden-import=Quartz',
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=PIL',
    '--distpath=./dist',
    '--workpath=./build'
])

# Verify the executable was created
app_path = os.path.join('dist', 'SpiritedAway.app')
if os.path.exists(app_path):
    print(f"\nBuild successful! Application created at: {app_path}")
    # Get the size of the .app directory
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(app_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    print(f"App size: {total_size / (1024*1024):.2f} MB")
else:
    print("\nError: Application not found in dist folder!")
    sys.exit(1)

# Clean up
if os.path.exists("SpiritedAway.spec"):
    os.remove("SpiritedAway.spec") 
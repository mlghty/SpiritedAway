import PyInstaller.__main__
import os
import shutil
import sys

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import PyQt5
        import win32api
        import pyautogui
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

# Check requirements first
check_requirements()

# Clean previous builds
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Create executable with PyInstaller
PyInstaller.__main__.run([
    'client.py',
    '--name=SpiritedAway',
    '--onefile',
    '--windowed',
    '--icon=./images/XD.ico',
    '--add-data=./images/XD.png;images/',
    '--add-data=./images/XD.ico;images/',
    '--version-file=version.txt',
    # Add hidden imports to ensure all dependencies are included
    '--hidden-import=win32api',
    '--hidden-import=win32con',
    '--hidden-import=pyautogui',
    # Exclude unnecessary packages to reduce size
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=PIL',
    # Add high DPI support
    '--uac-admin',  # Request admin privileges for registry access
    '--win-private-assemblies',
    '--win-no-prefer-redirects',
])

# Clean up
if os.path.exists("SpiritedAway.spec"):
    os.remove("SpiritedAway.spec")

print("\nBuild completed! Executable can be found in the 'dist' folder.") 
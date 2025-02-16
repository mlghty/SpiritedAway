import PyInstaller.__main__
import os
import shutil
import sys
import re

def get_version():
    """Get version from git tag or return default"""
    try:
        with os.popen('git describe --tags --abbrev=0') as stream:
            version = stream.read().strip()
        if not version:
            return '1.0.0'  # Default version
        # Remove 'v' prefix if present
        version = re.sub('^v', '', version)
        return version
    except:
        return '1.0.0'  # Default version

# Update version.txt with current version
version = get_version()
version_parts = version.split('.')
version_tuple = tuple(int(part) for part in version_parts + ['0'] * (4 - len(version_parts)))

version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'SpiritedAway - Window Activity Monitor'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'SpiritedAway'),
        StringStruct(u'LegalCopyright', u''),
        StringStruct(u'OriginalFilename', u'SpiritedAway.exe'),
        StringStruct(u'ProductName', u'SpiritedAway'),
        StringStruct(u'ProductVersion', u'{version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''

# Write version info to file
with open('version.txt', 'w') as f:
    f.write(version_info)

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
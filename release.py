import os
import re
from datetime import datetime

def increment_version(version, increment='patch'):
    """Increment the version number"""
    major, minor, patch = map(int, version.split('.'))
    if increment == 'major':
        return f"{major + 1}.0.0"
    elif increment == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

def create_release():
    # Read current version
    with open('VERSION', 'r') as f:
        current_version = f.read().strip()

    # Ask for version increment type
    print(f"\nCurrent version: {current_version}")
    print("\nSelect version increment type:")
    print("1. Major (x.0.0)")
    print("2. Minor (0.x.0)")
    print("3. Patch (0.0.x)")
    choice = input("\nEnter choice (1-3) [3]: ").strip() or "3"
    
    increment_type = {
        "1": "major",
        "2": "minor",
        "3": "patch"
    }.get(choice, "patch")

    # Calculate new version
    new_version = increment_version(current_version, increment_type)
    
    # Update VERSION file
    with open('VERSION', 'w') as f:
        f.write(new_version)
    
    # Create git tag and push
    os.system('git add VERSION')
    os.system(f'git commit -m "Bump version to {new_version}"')
    os.system(f'git tag -a v{new_version} -m "Release version {new_version}"')
    os.system('git push origin main --tags')

    print(f"\nCreated and pushed version {new_version}")
    print("GitHub Actions will now build and create the release.")

if __name__ == "__main__":
    create_release() 
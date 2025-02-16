# SpiritedAway
Minimizes all windows after certain amount of time has elapsed, restores all windows once user activity is detected. Made because SweptAway was outdated and SpirtedAway was made for OSX.

## Inspiration
+ https://etherealmind.com/osx-spirited-away-productivity-tool/
+ https://lifehacker.com/lifehacker-code-swept-away-windows-255055

## Features
- Automatically minimizes windows after a period of inactivity
- Restores windows when activity is detected
- Customizable inactivity timeout (1-600 seconds or 1-60 minutes)
- System tray integration with status notifications
- Start with Windows option
- Start minimized option
- Auto-start monitoring option
- Activity logging with log rotation (5MB limit)
- Clean and intuitive user interface

## Requirements
- Windows OS
- Python 3.10 or higher
- Required packages:
  - PyQt5 >= 5.15.0
  - pywin32 >= 228
  - pyautogui >= 0.9.53
  - pyinstaller == 5.13.2 (for building)

## Installation
1. Download the latest release from the [Releases](https://github.com/yourusername/SpiritedAway/releases) page
   - Or build from source (see Building section)
2. Run the executable
3. Optional: Enable "Start with Windows" for automatic startup

## Building from Source
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/SpiritedAway.git
   cd SpiritedAway
   ```

2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable
   ```bash
   python build.py
   ```

The executable will be created in the `dist` folder.

## Usage
- Launch the application
- Set your preferred inactivity timeout
- Click "Start Monitoring" to begin
- The application will:
  - Minimize all windows after the set inactivity period
  - Restore windows when mouse/keyboard activity is detected
  - Show notifications in the system tray
  - Log all activities

### Settings
- **Inactivity timeout**: Set the time before windows are minimized (1-600 seconds or 1-60 minutes)
- **Start with Windows**: Automatically start the application on Windows startup
- **Start Minimized**: Start the application minimized to system tray
- **Start monitoring on launch**: Begin monitoring automatically when the application starts

### System Tray
- Left-click: Show menu
- Right-click: Show menu
- Menu options:
  - Show: Display the main window
  - Hide: Minimize to system tray
  - Quit: Close the application

## Release Process
- Versioning follows semantic versioning (X.Y.Z)
- Releases are automated via GitHub Actions
- To create a new release:
  1. Tag the commit with version number: `git tag vX.Y.Z`
  2. Push the tag: `git push origin vX.Y.Z`
  3. GitHub Actions will automatically:
     - Build the executable
     - Create a GitHub release
     - Attach the built executable
     - Generate changelog from commits
     - Publish the release

## Acknowledgments
- Inspired by the original OSX Spirited Away and SweptAway tools
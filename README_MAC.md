# SpiritedAway for macOS

SpiritedAway is a utility that automatically minimizes all windows when you're inactive for a configurable period of time, and restores them when you become active again.

## Features

- Monitors user activity (mouse movement and keyboard input)
- Minimizes all windows when the user is inactive for a configurable period
- Restores windows when activity is detected again
- Runs in the system tray with notifications
- Settings for:
  - Inactivity timeout (in seconds or minutes)
  - Starting with macOS
  - Starting minimized
  - Auto-starting monitoring on launch
- Activity logging

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Install from Source

1. Clone this repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements_mac.txt
```

### Run the Application

```bash
python spirited_away_mac.py
```

### Build a Standalone Application

You can build a standalone application using PyInstaller:

```bash
pyinstaller --windowed --icon=images/XD.png --name="SpiritedAway" spirited_away_mac.py
```

The built application will be in the `dist/SpiritedAway` directory.

## Usage

- **Start/Stop Monitoring**: Toggle the "Start Monitoring" radio button to begin or end monitoring.
- **Inactivity Timeout**: Set how long the system should wait for inactivity before minimizing windows.
- **Start with macOS**: Enable to automatically start the application when you log in.
- **Start Minimized**: Start the application minimized to the system tray.
- **Start monitoring on launch**: Automatically begin monitoring when the application starts.

## Command Line Arguments

- `--start-minimized`: Start the application minimized to the system tray
- `--start-monitoring`: Start monitoring immediately

## Permissions

SpiritedAway requires the following permissions:

- **Accessibility**: To monitor user activity and control windows
- **Automation**: To minimize and restore windows

To grant these permissions:
1. Go to System Preferences > Security & Privacy > Privacy
2. Add SpiritedAway to both the Accessibility and Automation lists

## Troubleshooting

If windows aren't minimizing or restoring properly:

1. Make sure SpiritedAway has the necessary permissions
2. Check the Activity Log in the application for any error messages
3. Try restarting the application

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
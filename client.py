import sys
import time
import win32api
import pyautogui
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu, QAction, 
                            QLabel, QSpinBox, QGridLayout, QRadioButton, QCheckBox, 
                            QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QFrame,
                            QComboBox, QPushButton)
from PyQt5.QtCore import QTime, QDate, QTimer, Qt
from PyQt5.QtGui import QIcon
import threading
import winreg
import json


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # First try the exact path
    full_path = os.path.join(base_path, relative_path)
    if os.path.exists(full_path):
        return full_path

    # If .png doesn't exist, try .ico
    if relative_path.endswith('.png'):
        ico_path = relative_path[:-4] + '.ico'
        ico_full_path = os.path.join(base_path, ico_path)
        if os.path.exists(ico_full_path):
            return ico_full_path

    # If neither exists, try looking in the current directory
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    if os.path.exists(local_path):
        return local_path

    # Return the original path even if it doesn't exist
    return full_path
    

class SpiritedAway(QWidget):
       
    def __init__(self):    
        super().__init__()
        
        self.width = 400
        self.height = 500
        self.image_path = resource_path('./images/XD.png')
        self.settings_file = os.path.join(os.path.expanduser("~"), ".spiritedaway_settings.json")
        self.load_settings()

        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        
        # Check for user inactivity
        self.last_input_time = time.time()
        self.last_cursor_tuple =  win32api.GetCursorPos()
        self.INACTIVITY_TIMEOUT = 500  # Timeout in seconds
        self.MINIMIZED = False
        self.START = False
        self.monitoring_thread = None
        self.app_name = "Spirited Away"
        
        # Load and scale icon to exact 32x32 dimensions
        try:
            if not os.path.exists(self.image_path):
                self.log_message(f"Warning: Icon file not found at {self.image_path}")
                # Set a default icon or use a built-in one
                self.icon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-16.png")
            else:
                original_icon = QIcon(self.image_path)
                if original_icon.isNull():
                    self.log_message("Warning: Failed to load icon")
                    self.icon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-16.png")
                else:
                    pixmap = original_icon.pixmap(32, 32)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                        self.icon = QIcon(scaled_pixmap)
                    else:
                        self.log_message("Warning: Failed to create icon pixmap")
                        self.icon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-16.png")
        except Exception as e:
            self.log_message(f"Error loading icon: {str(e)}")
            self.icon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-16.png")
          
        # Create main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create control panel group
        control_group = QGroupBox("Controls")
        control_layout = QGridLayout()
        control_group.setLayout(control_layout)

        # Start/Stop radio button
        self.radio_button = QRadioButton("Start Monitoring")
        self.radio_button.setChecked(False)
        self.radio_button.toggled.connect(self.on_clicked)
        control_layout.addWidget(self.radio_button, 0, 0, 1, 2)

        # Timeout settings
        timeout_frame = QFrame()
        timeout_layout = QHBoxLayout()
        timeout_frame.setLayout(timeout_layout)

        self.timeout_label = QLabel("Inactivity timeout:")
        
        # Add timeout value input
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 600)
        self.timeout_spinbox.setValue(self.INACTIVITY_TIMEOUT)
        self.timeout_spinbox.valueChanged.connect(self.timeout_changed)
        
        # Add unit selector
        self.timeout_unit_selector = QComboBox()
        self.timeout_unit_selector.addItems(["seconds", "minutes"])
        self.timeout_unit_selector.currentTextChanged.connect(self.unit_changed)
        
        # Add conversion label
        self.conversion_label = QLabel()
        self.update_conversion_label()
        
        timeout_layout.addWidget(self.timeout_label)
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addWidget(self.timeout_unit_selector)
        timeout_layout.addWidget(self.conversion_label)
        timeout_layout.addStretch()
        
        control_layout.addWidget(timeout_frame, 1, 0, 1, 2)

        # Autostart checkbox
        self.autostart_checkbox = QCheckBox("Start with Windows")
        self.autostart_checkbox.setChecked(self.is_autostart_enabled())
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        control_layout.addWidget(self.autostart_checkbox, 2, 0, 1, 2)

        # Add start minimized checkbox under autostart
        self.start_minimized_checkbox = QCheckBox("Start Minimized")
        self.start_minimized_checkbox.setChecked(self.load_start_minimized_setting())
        self.start_minimized_checkbox.stateChanged.connect(self.toggle_start_minimized)
        control_layout.addWidget(self.start_minimized_checkbox, 3, 0, 1, 2)

        # Add autostart monitoring checkbox
        self.autostart_monitoring_checkbox = QCheckBox("Start monitoring on launch")
        self.autostart_monitoring_checkbox.setChecked(self.load_autostart_monitoring_setting())
        self.autostart_monitoring_checkbox.stateChanged.connect(self.toggle_autostart_monitoring)
        control_layout.addWidget(self.autostart_monitoring_checkbox, 4, 0, 1, 2)

        # Add control group to main layout
        main_layout.addWidget(control_group)

        # Create log display group
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        log_layout.setSpacing(0)  # Reduce spacing between elements
        log_layout.setContentsMargins(5, 5, 5, 5)  # Add small padding inside the group

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(200)
        log_layout.addWidget(self.log_display)

        # Add clear logs button
        clear_logs_layout = QHBoxLayout()
        self.clear_logs_button = QPushButton("Clear Logs")
        self.clear_logs_button.clicked.connect(self.clear_logs)
        clear_logs_layout.addStretch()
        clear_logs_layout.addWidget(self.clear_logs_button)
        log_layout.addLayout(clear_logs_layout)

        # Load previous logs if they exist
        self.log_file = os.path.join(os.path.expanduser("~"), ".spiritedaway_log.txt")
        self.load_logs()

        # Add log group to main layout
        main_layout.addWidget(log_group)

        # Status label at the bottom
        self.status_label = QLabel("Status: Monitoring stopped")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.init_ui()
        self.log_message("Application started")
        
    def init_ui(self):
        self.setWindowTitle('SpiritedAway')
        
        # Set window icon
        if not self.icon.isNull():
            self.setWindowIcon(self.icon)
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        if not self.icon.isNull():
            self.tray_icon.setIcon(self.icon)
        self.tray_icon.setVisible(True)

        # Create tray menu
        tray_menu = QMenu()
        show_action = QAction('Show', self)
        hide_action = QAction('Hide', self)
        quit_action = QAction('Quit', self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # Connect left-click to show menu
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_info)
        self.timer.start(1000)

        self.show_info()

    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            # Get the tray icon geometry
            geometry = self.tray_icon.geometry()
            # Show the menu at the tray icon position
            self.tray_icon.contextMenu().popup(geometry.topLeft())

    def show_info(self):
        time_text = "Hi I'm watching for user activity!"
        self.tray_icon.setToolTip(f'{time_text}')
        
    def check_for_user_activity(self):
        while self.START:
            try:
                current_time = time.time()
                if current_time - self.last_input_time > self.INACTIVITY_TIMEOUT:
                    if not self.MINIMIZED:
                        self.MINIMIZED = True
                        pyautogui.hotkey('win', 'm')
                        self.log_message("Windows minimized due to inactivity")
                        self.tray_icon.showMessage(
                            self.app_name,
                            "🪟 Windows Minimized\nNo activity detected for a while!",
                            self.icon,
                            1500
                        )
                else:
                    if self.MINIMIZED:
                        pyautogui.hotkey('win', 'shift', 'm')
                        self.MINIMIZED = False
                        self.log_message("Windows restored due to activity")
                        self.tray_icon.showMessage(
                            self.app_name,
                            "👋 Welcome Back!\nRestoring your windows...",
                            self.icon,
                            1500
                        )
                
                # Check for user input
                if any(win32api.GetAsyncKeyState(key) for key in [0x0001, 0x0002, 0x0004, 0x0100]):
                    self.last_input_time = current_time
                
                current_cursor_pos = win32api.GetCursorPos()
                if current_cursor_pos != self.last_cursor_tuple:
                    self.last_input_time = current_time
                    self.last_cursor_tuple = current_cursor_pos
                
                # Add a small sleep to prevent high CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                error_msg = f"Error monitoring activity: {str(e)}"
                self.log_message(f"Error: {error_msg}")
                self.tray_icon.showMessage(
                    f"{self.app_name} - Error",
                    f"⚠️ Monitoring Error:\n{error_msg}",
                    self.icon,
                    3000
                )
                time.sleep(1)

    def update_conversion_label(self):
        """Update the label showing the time conversion"""
        value = self.timeout_spinbox.value()
        current_unit = self.timeout_unit_selector.currentText()
        
        if current_unit == "seconds":
            minutes = value / 60
            if minutes >= 1:
                self.conversion_label.setText(f"({minutes:.1f} minutes)")
            else:
                self.conversion_label.setText("")
        else:  # minutes
            seconds = value * 60
            self.conversion_label.setText(f"({seconds} seconds)")

    def unit_changed(self, unit):
        """Handle timeout unit changes"""
        current_value = self.timeout_spinbox.value()
        if unit == "minutes":
            # Convert current seconds to minutes
            minutes_value = current_value / 60
            self.timeout_spinbox.setRange(1, 60)  # 1-60 minutes
            self.timeout_spinbox.setValue(round(minutes_value))
        else:  # seconds
            # Convert current minutes to seconds
            seconds_value = current_value * 60
            self.timeout_spinbox.setRange(1, 600)  # 1-600 seconds
            self.timeout_spinbox.setValue(round(seconds_value))
        
        self.update_conversion_label()
        self.timeout_changed()

    def timeout_changed(self):
        """Update timeout value based on unit selection"""
        value = self.timeout_spinbox.value()
        unit = self.timeout_unit_selector.currentText()
        
        # Convert to seconds if in minutes
        if unit == "minutes":
            self.INACTIVITY_TIMEOUT = value * 60
        else:
            self.INACTIVITY_TIMEOUT = value
        
        self.update_conversion_label()    
        self.save_settings()

    def on_clicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.START = True
            try:
                self.monitoring_thread = threading.Thread(target=self.check_for_user_activity, daemon=True)
                self.monitoring_thread.start()
                self.status_label.setText("Status: Monitoring active")
                self.log_message("Monitoring started")
                self.tray_icon.showMessage(
                    self.app_name,
                    "👁️ Monitoring Started\nI'll keep watch over your windows!",
                    self.icon,
                    2000
                )
            except Exception as e:
                error_msg = f"Failed to start monitoring: {str(e)}"
                self.log_message(f"Error: {error_msg}")
                self.tray_icon.showMessage(
                    f"{self.app_name} - Error",
                    f"⚠️ Oops! Something went wrong:\n{error_msg}",
                    self.icon,
                    3000
                )
        else:
            self.START = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=1.0)
            self.status_label.setText("Status: Monitoring stopped")
            self.log_message("Monitoring stopped")
            self.tray_icon.showMessage(
                self.app_name,
                "💤 Monitoring Stopped\nI'm taking a break now!",
                self.icon,
                2000
            )
            
    def hideEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            self.app_name,
            "🔽 Minimized to Tray\nI'll keep running in the background!",
            self.icon,
            1500
        )
        
    def minimize(self):
        self.hide()

    # needs to override QWidgets default close event
    def closeEvent(self, event):
        event.ignore()
        self.tray_icon.showMessage(
            self.app_name,
            "🔽 Minimized to Tray\nI'll keep running in the background!",
            self.icon,
            2000
        )
        self.hide() 
    
    def quit_app(self):
        """Properly cleanup before quitting"""
        self.START = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
        self.tray_icon.hide()
        QApplication.quit()
    
    def toggle_autostart(self, state):
        """Enable or disable autostart with Windows"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SpiritedAway"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if state:
                # Get the path of the current executable
                if getattr(sys, 'frozen', False):
                    # Running as compiled executable
                    app_path = sys.executable
                else:
                    # Running as script
                    app_path = os.path.abspath(sys.argv[0])
                    
                # Add startup parameters
                startup_args = ''
                if self.start_minimized_checkbox.isChecked():
                    startup_args += ' --start-minimized'
                if self.autostart_monitoring_checkbox.isChecked():
                    startup_args += ' --start-monitoring'
                    
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"{startup_args}')
                self.log_message("Autostart enabled - Application will start with Windows")
                self.tray_icon.showMessage(
                    self.app_name,
                    "🚀 Autostart Enabled\nI'll start automatically with Windows!",
                    self.icon,
                    2000
                )
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                    self.log_message("Autostart disabled - Application will not start with Windows")
                    self.tray_icon.showMessage(
                        self.app_name,
                        "⏸️ Autostart Disabled\nYou'll need to start me manually!",
                        self.icon,
                        2000
                    )
                except WindowsError:
                    self.log_message("Warning: Could not disable autostart - Registry key not found")
                    self.tray_icon.showMessage(
                        f"{self.app_name} - Warning",
                        "⚠️ Could not disable autostart\nRegistry key not found",
                        self.icon,
                        2000
                    )
            key.Close()
        except Exception as e:
            error_msg = f"Failed to set autostart: {str(e)}"
            self.log_message(f"Error: {error_msg}")
            self.tray_icon.showMessage(
                f"{self.app_name} - Error",
                f"⚠️ Autostart Error:\n{error_msg}",
                self.icon,
                3000
            )

    def is_autostart_enabled(self):
        """Check if autostart is enabled"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SpiritedAway"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, app_name)
            key.Close()
            return True
        except WindowsError:
            return False

    def load_settings(self):
        """Load saved settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.INACTIVITY_TIMEOUT = settings.get('timeout', 500)
                    saved_unit = settings.get('unit', 'seconds')
                    
                    # Set the correct unit and value in the UI
                    if saved_unit == "minutes":
                        self.timeout_unit_selector.setCurrentText("minutes")
                        self.timeout_spinbox.setValue(self.INACTIVITY_TIMEOUT // 60)
                    else:
                        self.timeout_unit_selector.setCurrentText("seconds")
                        self.timeout_spinbox.setValue(self.INACTIVITY_TIMEOUT)
        except Exception:
            self.INACTIVITY_TIMEOUT = 500

    def save_settings(self):
        """Save current settings"""
        try:
            settings = self.load_settings_file()
            settings.update({
                'timeout': self.INACTIVITY_TIMEOUT,
                'unit': self.timeout_unit_selector.currentText(),
                'start_minimized': self.start_minimized_checkbox.isChecked(),
                'autostart_monitoring': self.autostart_monitoring_checkbox.isChecked()
            })
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            
            # Format timeout message based on unit
            if self.INACTIVITY_TIMEOUT >= 60 and self.INACTIVITY_TIMEOUT % 60 == 0:
                timeout_msg = f"{self.INACTIVITY_TIMEOUT // 60} minutes"
            else:
                timeout_msg = f"{self.INACTIVITY_TIMEOUT} seconds"
                
            self.log_message(f"Settings saved: Timeout set to {timeout_msg}")
        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            self.log_message(f"Error: {error_msg}")
            self.tray_icon.showMessage(
                self.app_name,
                "⚠️ Settings Error\nFailed to save settings",
                self.icon,
                3000
            )

    def load_logs(self):
        """Load previous logs if they exist"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = f.read()
                    if logs:
                        self.log_display.setText(logs)
                        self.log_display.verticalScrollBar().setValue(
                            self.log_display.verticalScrollBar().maximum()
                        )
        except Exception as e:
            self.log_message(f"Error loading previous logs: {str(e)}")

    def log_message(self, message):
        """Add a message to the log display with timestamp and save to file"""
        timestamp = QTime.currentTime().toString("HH:mm:ss")
        log_entry = f"[{timestamp}] {message}"
        self.log_display.append(log_entry)
        
        # Save to file with rotation
        try:
            # Check file size (5MB limit)
            if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 5 * 1024 * 1024:
                # Rename current log file to .old
                backup_log = self.log_file + '.old'
                if os.path.exists(backup_log):
                    os.remove(backup_log)
                os.rename(self.log_file, backup_log)
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"Error saving log: {str(e)}")
            
        # Scroll to the bottom
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )

    def toggle_start_minimized(self, state):
        """Save start minimized preference"""
        try:
            settings = self.load_settings_file()
            settings['start_minimized'] = bool(state)
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            
            self.log_message(f"Start minimized {'enabled' if state else 'disabled'}")
        except Exception as e:
            self.log_message(f"Error saving start minimized setting: {str(e)}")

    def load_start_minimized_setting(self):
        """Load start minimized setting"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    return settings.get('start_minimized', False)
        except Exception:
            pass
        return False

    def load_autostart_monitoring_setting(self):
        """Load autostart monitoring setting"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    return settings.get('autostart_monitoring', False)
        except Exception:
            pass
        return False

    def toggle_autostart_monitoring(self, state):
        """Save autostart monitoring preference"""
        try:
            settings = self.load_settings_file()
            settings['autostart_monitoring'] = bool(state)
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            
            self.log_message(f"Auto-start monitoring {'enabled' if state else 'disabled'}")
        except Exception as e:
            self.log_message(f"Error saving auto-start monitoring setting: {str(e)}")

    def load_settings_file(self):
        """Load all settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def cleanup_app_data(self):
        """Clean up application data files"""
        try:
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            if os.path.exists(self.log_file + '.old'):
                os.remove(self.log_file + '.old')
            self.toggle_autostart(False)  # Remove from startup
        except Exception as e:
            print(f"Error cleaning up app data: {str(e)}")

    def clear_logs(self):
        """Clear the log display and file"""
        try:
            self.log_display.clear()
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            self.log_message("Logs cleared")
        except Exception as e:
            self.log_message(f"Error clearing logs: {str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Parse command line arguments
    start_minimized = '--start-minimized' in sys.argv
    start_monitoring = '--start-monitoring' in sys.argv
    
    # Create the main window
    spirited_away = SpiritedAway()
    
    # Set application icon
    if not spirited_away.icon.isNull():
        app.setWindowIcon(spirited_away.icon)
    
    # Apply startup settings
    if start_minimized or spirited_away.start_minimized_checkbox.isChecked():
        spirited_away.hide()
        if not spirited_away.icon.isNull():
            spirited_away.tray_icon.showMessage(
                spirited_away.app_name,
                "👀 Started Minimized\nI'm watching from the system tray!",
                spirited_away.icon,
                2000
            )
    else:
        spirited_away.show()
    
    # Auto-start monitoring if enabled
    if start_monitoring or spirited_away.autostart_monitoring_checkbox.isChecked():
        spirited_away.radio_button.setChecked(True)
    
    sys.exit(app.exec_())

  
if __name__ == '__main__':
    main()
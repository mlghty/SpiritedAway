import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTime, QDate, QTimer
from PyQt5.QtGui import QIcon

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Clock')
        self.setWindowIcon(QIcon('./images/clock.png'))

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./images/clock.png'))
        self.tray_icon.setVisible(True)

        tray_menu = QMenu()
        show_action = QAction('Show', self)
        hide_action = QAction('Hide', self)
        quit_action = QAction('Quit', self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.showTime()

    def showTime(self):
        time = QTime.currentTime()
        date = QDate.currentDate()
        time_text = time.toString('hh:mm')
        date_text = date.toString('ddd, dd MMM yyyy')
        self.tray_icon.setToolTip(f'{time_text} \n {date_text}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    
    
    
 






# import time
# import win32api
# import pyautogui

# INACTIVITY_TIMEOUT = 60  # Timeout in seconds
# MINIMIZED = False

# # Check for user inactivity
# last_input_time = time.time()
# last_cursor_tuple =  win32api.GetCursorPos()
# while True:
#     if time.time() - last_input_time > INACTIVITY_TIMEOUT:
#         # User is inactive, do something
#         print("User is inactive!")
        
#         if not MINIMIZED:
#             MINIMIZED = True
#             print("minimizing...")
#             pyautogui.hotkey('win', 'm')

#     else:
#         # User is active, do something else
#         print("User is active!")
#         if MINIMIZED:
#             pyautogui.hotkey('win', 'shift', 'm')
#             MINIMIZED = False

#     # Check for user input from the mouse or keyboard
#     if win32api.GetAsyncKeyState(0x0001):  # Left mouse button
#         last_input_time = time.time()
#     if win32api.GetAsyncKeyState(0x0002):  # Right mouse button
#         last_input_time = time.time()
#     if win32api.GetAsyncKeyState(0x0004):  # Middle mouse button (or mouse wheel)
#         last_input_time = time.time()
#     if win32api.GetAsyncKeyState(0x0100):  # Keyboard key
#         last_input_time = time.time()
#     if win32api.GetCursorPos():  # Cursor position
#         temp_cursor_tuple = win32api.GetCursorPos()
#         # print(temp_cursor_tuple)
#         if temp_cursor_tuple != last_cursor_tuple:
#             last_input_time = time.time()
#             last_cursor_tuple = win32api.GetCursorPos()
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       # if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = InactivityTimeoutWidget()
#     widget.show()
#     sys.exit(app.exec_())

    
    
    
    
    # app = SpiritedAway()
    # sys.exit()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSpinBox

class InactivityTimeoutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        width = 550
        height = 600

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.inactivity_timeout = 60  # Initial timeout value in seconds

        # Create a label to display the timeout value
        self.timeout_label = QLabel(self)
        self.timeout_label.setText("Inactivity timeout: %d seconds" % self.inactivity_timeout)

        # Create a spin box to allow the user to enter the timeout value
        self.timeout_spinbox = QSpinBox(self)
        self.timeout_spinbox.setRange(1, 600)  # Allow timeout values between 1 and 600 seconds
        self.timeout_spinbox.setValue(self.inactivity_timeout)
        self.timeout_spinbox.valueChanged.connect(self.timeout_changed)

    def timeout_changed(self):
        # Update the timeout value when the user changes it in the spin box
        self.inactivity_timeout = self.timeout_spinbox.value()
        self.timeout_label.setText("Inactivity timeout: %d seconds" % self.inactivity_timeout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InactivityTimeoutWidget()
    widget.show()
    sys.exit(app.exec_())





# last_cursor_tuple =  win32api.GetCursorPos()


# while True:
#     temp_cursor_tuple = win32api.GetCursorPos()
    
#     if temp_cursor_tuple == last_cursor_tuple:
#         print("The same!")
    
#     if temp_cursor_tuple != last_cursor_tuple:
#         last_cursor_tuple =  win32api.GetCursorPos()
#         print("Not the same!")
        
        
        
#     time.sleep(5)
    
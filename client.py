import sys
import time
import win32api
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction,QLabel,QSpinBox,QGridLayout,QRadioButton
from PyQt5.QtCore import QTime, QDate, QTimer
from PyQt5.QtGui import QIcon
import threading


class SpiritedAway(QWidget):
       
    def __init__(self):    
        super().__init__()
        
        width = 300
        height = 200

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        
        # Check for user inactivity
        self.last_input_time = time.time()
        self.last_cursor_tuple =  win32api.GetCursorPos()
        self.INACTIVITY_TIMEOUT = 500  # Timeout in seconds
        self.MINIMIZED = False
        self.START = False
          
        layout = QGridLayout()
        self.setLayout(layout)

         # Create a spin box to allow the user to enter the timeout value
        self.timeout_spinbox = QSpinBox()

        self.timeout_spinbox.setRange(1, 600)  # Allow timeout values between 1 and 600 seconds
        self.timeout_spinbox.setValue(self.INACTIVITY_TIMEOUT)
        self.timeout_spinbox.valueChanged.connect(self.timeout_changed)
        
        layout.addWidget(self.timeout_spinbox,1,1)

        # timeout_spinbox.setGeometry(10, 30, 50, 30)


        # Create a label to display the timeout value
        self.timeout_label = QLabel()
        self.timeout_label.setText("Inactivity timeout: %d seconds" % self.INACTIVITY_TIMEOUT)
        layout.addWidget(self.timeout_label,1,0)
        
         # self.timeout_label.setText("++++++++Inactivity timeout:")
         
         # x,y width,height
        # self.timeout_label.setGeometry(10, 10, 350, 10)
        
        
        radiobutton = QRadioButton("Start")
        radiobutton.setChecked(False)
        radiobutton.toggled.connect(self.on_clicked)
        layout.addWidget(radiobutton, 0, 0)

        
        self.init_ui()
        # self.check_for_user_activity()
        
    def init_ui(self):
        self.setWindowTitle('SpiritedAway')

        # Grid Layout
        # grid = QGridLayout()
        # self.setLayout(grid)

        self.setWindowIcon(QIcon('./images/XD.png'))

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./images/XD.png'))
        self.tray_icon.setVisible(True)

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_info)
        self.timer.start(1000)

        self.show_info()

    def show_info(self):
        time_text = "Hi I'm watching for user activity!"
        self.tray_icon.setToolTip(f'{time_text}')
        
    def check_for_user_activity(self):
        while self.START:
            if time.time() - self.last_input_time > self.INACTIVITY_TIMEOUT:
                if not self.MINIMIZED:
                    self.MINIMIZED = True
                    pyautogui.hotkey('win', 'm')
            else:
                if self.MINIMIZED:
                    pyautogui.hotkey('win', 'shift', 'm')
                    self.MINIMIZED = False

            # Check for user input from the mouse or keyboard
            if win32api.GetAsyncKeyState(0x0001):  # Left mouse
                self.last_input_time = time.time()
            if win32api.GetAsyncKeyState(0x0002):  # Right mouse 
                self.last_input_time = time.time()
            if win32api.GetAsyncKeyState(0x0004):  
                self.last_input_time = time.time()
            if win32api.GetAsyncKeyState(0x0100):  # Keyboard key
                self.last_input_time = time.time()
            if win32api.GetCursorPos():  # Cursor position
                self.temp_cursor_tuple = win32api.GetCursorPos()
                if self.temp_cursor_tuple != self.last_cursor_tuple:
                    self.last_input_time = time.time()
                    self.last_cursor_tuple = win32api.GetCursorPos()
                    
    def timeout_changed(self):
        # Update the timeout value when the user changes it in the spin box
        self.INACTIVITY_TIMEOUT = self.timeout_spinbox.value()
        self.timeout_label.setText("Inactivity timeout: %d seconds" % self.INACTIVITY_TIMEOUT)
        
    def on_clicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.START = True
            try:
                th = threading.Thread(target=self.check_for_user_activity)
                th.start()
            except:
                print("An exception occurred")
                time.sleep(1600)
            # th = threading.Thread(target=self.check_for_user_activity)
            # th.start()
            
            print("Started to monitor user activity...")
            print(self.START)
        else:
            self.START = False
            print("Stopped monitoring!")
            
    def hideEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            1000
        )
        
    def minimize(self):
        self.hide()

    # needs to override QWidgets default close event
    def closeEvent(self, event):
        event.ignore()
        self.tray_icon.showMessage(
            "Spirited Away",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )
        self.hide() 
    
    def quit_app():
        quit() 

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    clock = SpiritedAway()
    clock.show()
    sys.exit(app.exec_())

  
if __name__ == '__main__':
    main()
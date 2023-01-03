import sys
import itertools
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMenu, QStyle, QSystemTrayIcon
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

#from win10toast import ToastNotifier                                      # win10toast

DURATION_INT = 10
#toaster = ToastNotifier()                                                 # win10toast
TIME_CYCLER = itertools.cycle([10, 5])  

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_timer = 1
        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        #Tray menu
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(app.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # App window
# ?       self.app = QApplication(sys.argv)
# ?       self.win = QMainWindow()
# ?       self.win.setGeometry(200, 200, 200, 200)
# ?       self.win.setWindowTitle("test")
        self.setGeometry(200, 200, 200, 200)                                           # +++
        self.setWindowTitle("test")                                                    # +++

        # Widgets
        self.titleLabel = QtWidgets.QLabel(self) #.win)
        self.titleLabel.setText("Welcome to my app")
        self.titleLabel.move(50,20)

        self.timerLabel = QtWidgets.QLabel(self) #.win)
        self.timerLabel.move(50,50)
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font: 10pt Helvetica")

        self.startButton = QtWidgets.QPushButton(self) #.win)
        self.startButton.setText("Start")
        self.startButton.move(50,100)
        self.startButton.clicked.connect(self.startTimer)

        self.minimizeButton = QtWidgets.QPushButton(self) #.win)
        self.minimizeButton.setText("Minimize")
        self.minimizeButton.move(50,130)
        self.minimizeButton.clicked.connect(self.minimize)

        self.update_gui()

        # Show window
# ?       self.win.show()
# ?       sys.exit(app.exec_())

    def startTimer(self):
        self.time_left_int = next(TIME_CYCLER)
        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(1000)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            if self.current_timer == 1:
#                toaster.show_toast("test1", "test1", duration=3, threaded=True)    # win10toast
                self.current_timer = 2
            elif self.current_timer == 2:
#                toaster.show_toast("test2", "test2", duration=3, threaded=True)    # win10toast
                self.current_timer = 1
            self.time_left_int = next(TIME_CYCLER)

        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.timerLabel.setText(minsec)

    def minimize(self):
# ?       self.win.hide()
        self.hide()                                                                  # +++


    def closeEvent(self, event):
        event.ignore()
# ?       self.win.hide()
        self.hide()                                                                  # +++
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
main_window = App()
main_window.show()
sys.exit(app.exec_())
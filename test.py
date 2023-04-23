import time
import threading
import platform
import datetime

# Import platform-specific modules
if platform.system() == 'Windows':
    import win32gui
    import win32api

def system_event_monitor():
    # Detect sleep and wake events
    if platform.system() == 'Windows':
        # Monitor for system events
        def callback(hwnd, msg, wparam, lparam):
            if msg == win32gui.WM_POWERBROADCAST and wparam == win32api.PBT_APMSUSPEND:
                # PC is going to sleep
                print("PC is going to sleep")
            elif msg == win32gui.WM_POWERBROADCAST and wparam == win32api.PBT_APMRESUMESUSPEND:
                # PC is waking up from sleep
                print("PC is waking up from sleep")
            return True

        win32gui.SetWindowsHookEx(win32gui.WH_CALLWNDPROC, callback, win32api.GetModuleHandle(None), 0)

 
# Start the system event monitor in a separate thread
t = threading.Thread(target=system_event_monitor)
t.daemon = True
t.start()

# Print a number every minute in the main thread
i = 0
last_wake_time = datetime.datetime.now()  # initialize last wake time to current time
while True:
    now = datetime.datetime.now()
    if (now - last_wake_time).total_seconds() >= 60:
        print(i)
        i += 1
        last_wake_time = now
    time.sleep(1)
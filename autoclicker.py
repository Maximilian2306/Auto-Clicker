import pyautogui
import keyboard 
import time

click_delay = 0.1  
start_stop_key = 'f6'  
exit_key = 'esc'  

running = False

print("Auto Clicker gestartet.")
print(f"Drücke {start_stop_key} um Start/Stop, {exit_key} zum Beenden.")

try:
    while True:
        if keyboard.is_pressed(exit_key):
            print("Beendet.")
            break

        if keyboard.is_pressed(start_stop_key):
            running = not running
            print("Auto Clicker:", "AN" if running else "AUS")
            time.sleep(0.5) 

        if running:
            pyautogui.click()
            time.sleep(click_delay)
except KeyboardInterrupt:
    print("Abgebrochen.")

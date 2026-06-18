import os
import pyautogui
import time
from datetime import datetime

os.system("open -a TextEdit")
time.sleep(2)
pyautogui.press("enter")

pyautogui.FAILSAFE = True  # Enable fail-safe feature
pyautogui.PAUSE = 1.0  # Set a pause after each PyAutoGUI call

print("step 1: Open the chrome browser")
time.sleep(2)

pyautogui.hotkey('command', 'space', interval=0.1)  
time.sleep(1)
pyautogui.write("chrome", interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

print("step 2: Open the Website")
pyautogui.hotkey('command', 't', interval=0.1)
time.sleep(2)
pyautogui.write("https://www.accuweather.com/en/in/coimbatore/206673/weather-forecast/206673?type=locality", interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(5)

print("step 3: Copy the full data of the website")
pyautogui.hotkey('command', 'a', interval=0.1)
time.sleep(1)
pyautogui.hotkey('command', 'c', interval=0.1)
time.sleep(1)

print("step 4: open the text editor and paste the data")
time.sleep(1)
pyautogui.press("tab")
pyautogui.press("enter")
pyautogui.hotkey('command', 'space', interval=0.1)
time.sleep(1)
pyautogui.write("TextEdit", interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)
pyautogui.hotkey('command', 'v', interval=0.1)
time.sleep(2)

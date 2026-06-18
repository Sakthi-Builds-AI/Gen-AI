import pyautogui
import time

#Mouse operations

#pyautogui.moveTo(500,500)  # Move mouse to coordinates (500, 500)
#pyautogui.click(500,500)  # Click the mouse
#pyautogui.doubleClick(200,200)  # Double-click the mouse
#pyautogui.rightClick()  # Right-click the mouse
#pyautogui.middleClick()  # Middle-click the mouse

pyautogui.scroll(500)
time.sleep(3)
pyautogui.scroll(-500)  # Scroll down
import pyautogui
import time
import pyscreeze

#pyautogui.write("Hello, World!", interval=0.10)

#hotkeys
#pyautogui.hotkey('cmd', 'a')  # Select all text

# holding down keys
#pyautogui.keyDown('shift')
#pyautogui.typewrite("this is uppercase text")
#pyautogui.keyUp('shift')  #exit
#Release the shift key

screenshot = pyautogui.screenshot()
screenshot.save("Pyautogui_final_demo.png")  # Save the screenshot as a PNG file
"""
Weather Assignment Automation (macOS) - simple version, no functions
Saves the final file as a native Numbers document.

SETUP (run once in Terminal):
    pip3 install pyautogui pillow requests

PERMISSIONS:
    System Settings -> Privacy & Security -> Accessibility -> enable Terminal/your IDE
    System Settings -> Privacy & Security -> Screen Recording -> enable Terminal/your IDE
"""

import subprocess
import time
import os
import pyautogui
import requests
from datetime import datetime

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True  # move mouse to a screen corner to abort

CITY = "New York"  # <-- change to your city
DESKTOP = "/Users/shrisakthiselvaraj/GEN AI COURSE/WEATHER_BOT"  # output folder (kept variable name DESKTOP for simplicity)

today = datetime.now()
date_str = today.strftime("%Y-%m-%d %H:%M")
date_for_filename = today.strftime("%Y-%m-%d")
url = f"https://weather.com/weather/today/l/{CITY.replace(' ', '+')}"

# --- 1. Open Chrome to weather.com ---
print("Opening Chrome to weather.com...")
subprocess.run(["open", "-a", "Google Chrome", url])
time.sleep(4)  # wait for page load

# --- 2. Fetch the temperature from wttr.in (plain-text weather API - reliable, no JS rendering issues) ---
print("Fetching temperature...")
wttr_url = f"https://wttr.in/{CITY.replace(' ', '+')}?format=%t"
resp = requests.get(wttr_url, timeout=10)
temp = resp.text.strip()

print(f"Temperature found: {temp}")
temp = temp.replace("+", "")  # drop the leading "+" e.g. "+21°C" -> "21°C"
comment = f"Logged automatically for {CITY}"

# --- 3, 4, 5. Open Numbers (new blank doc) and set the header + data row ---
# Done via AppleScript instead of simulated keystrokes - typing through pyautogui
# was landing on the table as a selected *object* rather than inside a cell
# (timing/focus dependent), so values weren't actually being entered. Setting
# cell values directly through Numbers' scripting dictionary is immune to that.
print("Opening Numbers and writing data...")
fill_script = f'''
tell application "Numbers"
    activate
    make new document
    delay 1
    tell front document
        tell active sheet
            tell table 1
                set value of cell "A1" to "Date & Time"
                set value of cell "B1" to "Temperature"
                set value of cell "C1" to "Comments"
                set value of cell "A2" to "{date_str}"
                set value of cell "B2" to "{temp}"
                set value of cell "C2" to "{comment}"
            end tell
        end tell
    end tell
end tell
'''
subprocess.run(["osascript", "-e", fill_script])
time.sleep(1)

# --- 6. Save as a native Numbers file ---
# Done entirely via AppleScript - no keyboard shortcuts needed, so it isn't
# affected by any Accessibility/modifier-key issues.
filename_base = f"weather_log_{date_for_filename}"
numbers_path = f"{DESKTOP}/{filename_base}.numbers"

print(f"Saving Numbers file -> {numbers_path}")
os.makedirs(os.path.dirname(numbers_path), exist_ok=True)
save_script = f'''
tell application "Numbers"
    set theDoc to front document
    save theDoc in POSIX file "{numbers_path}"
end tell
'''
subprocess.run(["osascript", "-e", save_script])
time.sleep(2)

# --- 7. Screenshot the final spreadsheet ---
screenshot_path = f"{DESKTOP}/weather_log_{date_for_filename}.png"
print(f"Taking screenshot -> {screenshot_path}")
os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
time.sleep(1)
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)

print("Done.")
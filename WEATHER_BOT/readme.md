Weather Assignment Automation (macOS)

This script automates a small assignment: open a browser to a weather site, grab the current temperature, log it into a spreadsheet, save the file, and take a screenshot of the result.

What it does, step by step


Opens Google Chrome to weather.com for the city you set.
Fetches the actual temperature from wttr.in, a simple text-based weather service. (weather.com's number is loaded by JavaScript, so a plain web request can't read it directly — wttr.in returns the temperature as plain text instead.)
Opens a new Numbers document and fills in a header row (Date & Time, Temperature, Comments) and one data row with today's reading.
Saves the file as a .numbers document with today's date in the filename.
Takes a screenshot of the screen and saves it as a .png, also dated.
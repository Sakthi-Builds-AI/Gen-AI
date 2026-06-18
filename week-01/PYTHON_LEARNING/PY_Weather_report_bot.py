from playwright.sync_api import sync_playwright
from datetime import datetime   
print(" starting the playwright automation script")
print(" script started at : ", datetime.now())

with sync_playwright() as p:
    print(" launching the browser")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print(" navigating to the weather site")
    page.goto("https://www.accuweather.com/en/in/bengaluru/204108/weather-forecast/204108")

    # dismiss the privacy consent popup
    page.locator("button:has-text('Accept')").click()

    page.screenshot(path="weather_report.png")

    # TEMPORARY: dump the HTML so we can find the real class name
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print(" extracting the weather data")
    weather_data = page.locator("div.YOUR_REAL_CLASS_HERE").text_content()
    print(" weather data extracted successfully")

    print(" saving the weather data to a file")
    with open("weather_report.txt", "w") as file:
        file.write(f"Weather Report for Bengaluru on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(weather_data)
    print(" weather data saved to file successfully")

    print(" closing the browser")
    browser.close()
    print(" script completed at : ", datetime.now())
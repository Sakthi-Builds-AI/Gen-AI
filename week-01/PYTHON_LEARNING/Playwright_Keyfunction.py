from playwright.sync_api import Browser, sync_playwright



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()


    page.goto("https://www.accuweather.com/en/us/new-york-ny/10007/weather-forecast/349727")
    page.screenshot(path="accuweather_homepage.png")

    page.click("text =full forecast")
    page.screenshot(path="accuweather_full_forecast.png")

    #typing
    page.fill("input[name='query']", "New York, NY")
    page.press("input[name='query']", "Enter")
    page.screenshot(path="accuweather_search_results.png")

    #waiting
    page.wait_for_selector("text=New York, NY Weather")
    page.screenshot(path="accuweather_search_results_loaded.png")

    #extracting
    title = page.title()
    print(f"Page title: {title}")
    browser.close()
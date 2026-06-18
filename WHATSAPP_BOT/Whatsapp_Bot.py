import os
import json
import random
import time
import urllib.parse
from datetime import datetime
import pandas as pd
from playwright.sync_api import sync_playwright

CONTACT_FILE = "contacts.csv"
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

MSG_BOX = 'div[contenteditable="true"][data-tab="10"], div[aria-label="Type a message"]' 
INVALID_TOAST = 'text="Phone number shared via url is invalid."'
SENT_CHECK = 'span[data-icon="msg-check"], span[data-icon="msg-dblcheck"], span[data-icon="msg-dblcheck-ack"]'
MESSAGE_BUBBLES = "div.message-in, div.message-out"


def delay():
    time.sleep(random.uniform(2, 5))


def load_contacts():
    if not os.path.exists(CONTACT_FILE):
        print(f"{CONTACT_FILE} not found!")
        return []
    df = pd.read_csv(CONTACT_FILE, encoding="latin-1")
    df.columns = df.columns.str.strip()
    return df.fillna("").to_dict("records")


def save_reports(results):
    today = datetime.now().strftime("%Y-%m-%d")
    json_file = f"whatsapp_report_{today}.json"
    excel_file = f"whatsapp_report_{today}.xlsx"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    pd.DataFrame(results).to_excel(excel_file, index=False)
    print("\nReports Generated")
    print(json_file)
    print(excel_file)


def send_whatsapp_message(page, phone, message):
    encoded_msg = urllib.parse.quote(message)
    phone = phone.replace("+", "").strip()
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
    print(f"URL: {url}")
    page.goto(url)

    

    try:
        page.wait_for_selector(MSG_BOX, timeout=40000)
    except:
        raise Exception("Chat did not load — check if WhatsApp is logged in")

    delay()
    page.keyboard.press("Enter")

    # Confirm the message actually went out (check-mark appears on the bubble)
    try:
     page.wait_for_selector(SENT_CHECK, timeout=15000)
    except:
     pass 
    delay()


def get_last_messages(page, count=3):
    bubbles = page.locator(MESSAGE_BUBBLES)
    total = bubbles.count()
    start = max(0, total - count)
    messages = []
    for i in range(start, total):
        text = bubbles.nth(i).locator("span.selectable-text").all_inner_texts()
        messages.append(" ".join(text).strip())
    return messages


def main():
    contacts = load_contacts()
    if not contacts:
        return

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com")
        #input("\nScan QR Code and press ENTER when WhatsApp loads...")
        print("\nScan QR Code now. Bot starts automatically in 20 seconds...")
        time.sleep(50)

        for contact in contacts:
            name = str(contact["Name"])
            phone = str(contact["Phone"])
            message = str(contact.get("Message", "Hi {name}!")).replace("{name}", name)

            row = {
                "Name": name,
                "Phone": phone,
                "Status": "FAILED",
                "Screenshot": "",
                "LastMessages": []
            }

            try:
                print(f"\nSending to {name}")
                send_whatsapp_message(page, phone, message)

                screenshot_file = os.path.join(SCREENSHOT_DIR, f"{name}.png")
                page.screenshot(path=screenshot_file)
                row["Screenshot"] = screenshot_file
                row["LastMessages"] = get_last_messages(page)
                row["Status"] = "SENT"
                print("Success")

            except Exception as e:
                row["Status"] = f"FAILED: {e}"
                print("Failed:", e)

            results.append(row)
            delay()

        save_reports(results)
        browser.close()

    print("\nCompleted Successfully")


if __name__ == "__main__":
    main()
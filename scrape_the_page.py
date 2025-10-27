import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

if os.getenv("GITHUB_ACTIONS") != "true":
    from dotenv import load_dotenv
    load_dotenv()

PRODUCT_URL = os.getenv("PRODUCT_URL")

if not PRODUCT_URL:
    raise ValueError("PRODUCT_URL not set")

def fetch_rendered_html(url: str) -> str:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (StockWatcher/1.0)")
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
        return html


def is_product_available(html: str) -> bool:

    soup = BeautifulSoup(html, "lxml")

    button = soup.find("button", {"name": "add"})

    if not button:
        print("not found 'Add to cart'")
        return False

    if button.has_attr("disabled"):
        return False

    text = button.get_text(strip=True).lower()
    if "sold out" in text or "unavailable" in text:
        return False

    if "add to cart" in text or "add" in text:
        return True

    return False


if __name__ == "__main__":
    html = fetch_rendered_html(PRODUCT_URL)
    available = is_product_available(html)

    if available:
        print("available")
    else:
        print("NOT available")

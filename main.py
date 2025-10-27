import os
from scrape_the_page import fetch_rendered_html, is_product_available
from test_telegram import send_tg

PRODUCT_URL = os.getenv("PRODUCT_URL")

if not PRODUCT_URL:
    raise ValueError("PRODUCT_URL not set")

def main():
    html = fetch_rendered_html(PRODUCT_URL)
    available = is_product_available(html)

    if available:
        print("Product is AVAILABLE!")
        message = f"✅ Product AVAILABLE \n{PRODUCT_URL}"
        send_tg(message)
    else:
        print("Product still sold out.")

if __name__ == "__main__":
    main()

import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PRODUCT_URLS = [
    os.getenv("PRODUCT_URL_1"),
    os.getenv("PRODUCT_URL_2"),
    os.getenv("PRODUCT_URL_3"),
]

CHECK_IT = os.getenv("CHECK_IT", "").strip()


def send_telegram_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        r.raise_for_status()
        print("Message sent")
    except Exception as e:
        print(f"❌error: {e}")


def fetch_product(url: str) -> dict:
    resp = requests.get(
        url,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def find_variant_by_title(product: dict, wanted_title: str):
    wanted = wanted_title.strip().lower()
    for v in product.get("variants", []):
        title = str(v.get("title", "")).strip().lower()
        if title == wanted:
            return v
    return None


def check_url(product_url: str):
    if not product_url:
        return

    try:
        product = fetch_product(product_url)
    except Exception as e:
        print(f"[ERROR]{e}")
        return

    variant = find_variant_by_title(product, CHECK_IT)

    if not variant:
        print(f"[INFO] not found")
        return

    is_avail = bool(variant.get("available", False))
    print(f"[INFO] {is_avail}")

    if is_avail:
        msg = (
            f"✅ <b> Available at: {product_url}"
        )
        send_telegram_message(msg)


def main():
    if not CHECK_IT:
        print("⚠️")
        return

    any_url = False
    for url in PRODUCT_URLS:
        if url:
            any_url = True
            check_url(url)

    if not any_url:
        print("⚠️U")


if __name__ == "__main__":
    main()

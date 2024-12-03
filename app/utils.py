# app/utils.py
import requests

TELEGRAM_BOT_TOKEN = "7982513717:AAFmQKYgf-lNpAXHc_sf4pINn1j3ZeinSI8"
TELEGRAM_CHAT_ID = "769326792"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

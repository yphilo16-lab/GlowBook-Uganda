
import json
import logging
import os
import urllib.request

logger = logging.getLogger(__name__)


def send_telegram_notification(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("Telegram credentials are not configured.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            response.read()

    except Exception:
        logger.exception("Could not send Telegram notification.")

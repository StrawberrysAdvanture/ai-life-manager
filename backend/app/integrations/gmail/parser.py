import base64
from datetime import datetime
from email.utils import getaddresses, parsedate_to_datetime
from typing import Any

from bs4 import BeautifulSoup

from app.integrations.gmail.models import NormalizedGmailMessage


def get_header(
    headers: list[dict[str, Any]],
    name: str,
) -> str | None:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            value = header.get("value")

            if isinstance(value, str):
                return value

    return None


def parse_addresses(value: str | None) -> list[str]:
    if value is None:
        return []

    addresses = getaddresses([value])

    return [address for _, address in addresses if address]


def parse_date(value: str | None) -> datetime | None:
    if value is None:
        return None

    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None


def decode_body(data: str | None) -> str:
    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(data)
        return decoded.decode("utf-8", errors="replace")
    except (ValueError, TypeError):
        return ""


def find_mime_part(
    payload: dict[str, Any],
    target_mime_type: str,
) -> dict[str, Any] | None:
    if payload.get("mimeType") == target_mime_type:
        return payload

    for part in payload.get("parts", []):
        found = find_mime_part(part, target_mime_type)

        if found is not None:
            return found

    return None


def extract_text_body(payload: dict[str, Any]) -> str:
    plain_part = find_mime_part(payload, "text/plain")

    if plain_part is not None:
        body = plain_part.get("body", {})
        return decode_body(body.get("data"))

    html_part = find_mime_part(payload, "text/html")

    if html_part is not None:
        body = html_part.get("body", {})
        html = decode_body(body.get("data"))
        return html_to_text(html)

    return ""


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def normalize_gmail_message(
    message: dict[str, Any],
) -> NormalizedGmailMessage:
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender_addresses = parse_addresses(get_header(headers, "From"))

    recipients = parse_addresses(get_header(headers, "To"))

    sender = sender_addresses[0] if sender_addresses else None

    return NormalizedGmailMessage(
        message_id=message["id"],
        thread_id=message["threadId"],
        sender=sender,
        recipients=recipients,
        subject=get_header(headers, "Subject"),
        sent_at=parse_date(get_header(headers, "Date")),
        labels=message.get("labelIds", []),
        body_text=extract_text_body(payload),
    )

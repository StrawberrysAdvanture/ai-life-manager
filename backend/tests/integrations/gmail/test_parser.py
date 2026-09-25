import pytest

from app.integrations.gmail.parser import (
    decode_body,
    extract_text_body,
    get_header,
    normalize_gmail_message,
    parse_addresses,
    parse_date,
)


def test_get_header() -> None:
    headers = [
        {"name": "From", "value": "Alice <alice@example.com>"},
        {"name": "To", "value": "Bob <bob@example.com>"},
        {"name": "Subject", "value": "Meeting tomorrow"},
    ]

    assert get_header(headers, "Subject") == "Meeting tomorrow"
    assert get_header(headers, "From") == "Alice <alice@example.com>"


def test_get_header_is_case_insensitive() -> None:
    headers = [
        {"name": "Subject", "value": "Meeting tomorrow"},
    ]

    assert get_header(headers, "subject") == "Meeting tomorrow"


def test_get_header_returns_none_when_missing() -> None:
    headers = [
        {"name": "From", "value": "Alice <alice@example.com>"},
    ]

    assert get_header(headers, "Subject") is None


def test_parse_addresses() -> None:
    value = "Alice <alice@example.com>, Bob <bob@example.com>"

    result = parse_addresses(value)

    assert result == [
        "alice@example.com",
        "bob@example.com",
    ]


def test_parse_addresses_returns_empty_list_for_none() -> None:
    assert parse_addresses(None) == []


def test_parse_date() -> None:
    result = parse_date("Wed, 24 Sep 2026 10:30:00 -0700")

    assert result is not None
    assert result.year == 2026
    assert result.month == 9
    assert result.day == 24
    assert result.hour == 10
    assert result.minute == 30


def test_parse_date_returns_none_for_missing_date() -> None:
    assert parse_date(None) is None


def test_parse_date_returns_none_for_invalid_date() -> None:
    assert parse_date("not-a-real-date") is None


def test_decode_body() -> None:
    encoded = "SGVsbG8gSmFja2llIQ=="

    result = decode_body(encoded)

    assert result == "Hello Jackie!"


def test_decode_body_returns_empty_string_for_missing_data() -> None:
    assert decode_body(None) == ""
    assert decode_body("") == ""


def test_extract_text_body_from_plain_message() -> None:
    payload = {
        "mimeType": "text/plain",
        "body": {
            "data": "SGVsbG8gSmFja2llIQ==",
        },
    }

    assert extract_text_body(payload) == "Hello Jackie!"


def test_extract_text_body_prefers_plain_text_part() -> None:
    payload = {
        "mimeType": "multipart/alternative",
        "parts": [
            {
                "mimeType": "text/plain",
                "body": {
                    "data": "SGVsbG8gSmFja2llIQ==",
                },
            },
            {
                "mimeType": "text/html",
                "body": {
                    "data": "PGI-SGVsbG88L2I-",
                },
            },
        ],
    }

    assert extract_text_body(payload) == "Hello Jackie!"


def test_extract_text_body_from_nested_parts() -> None:
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [
            {
                "mimeType": "multipart/alternative",
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {
                            "data": "SGVsbG8gSmFja2llIQ==",
                        },
                    },
                    {
                        "mimeType": "text/html",
                        "body": {
                            "data": "PGI-SGVsbG88L2I-",
                        },
                    },
                ],
            },
        ],
    }

    assert extract_text_body(payload) == "Hello Jackie!"


def test_extract_text_body_falls_back_to_html() -> None:
    payload = {
        "mimeType": "text/html",
        "body": {
            "data": "PHA-SGVsbG8gSmFja2llITwvcD4=",
        },
    }

    assert extract_text_body(payload) == "Hello Jackie!"


def test_normalize_gmail_message() -> None:
    message = {
        "id": "message-1",
        "threadId": "thread-1",
        "labelIds": ["INBOX", "IMPORTANT"],
        "payload": {
            "mimeType": "text/plain",
            "headers": [
                {
                    "name": "From",
                    "value": "Alice <alice@example.com>",
                },
                {
                    "name": "To",
                    "value": "Bob <bob@example.com>",
                },
                {
                    "name": "Subject",
                    "value": "Meeting tomorrow",
                },
                {
                    "name": "Date",
                    "value": "Wed, 24 Sep 2026 10:30:00 -0700",
                },
            ],
            "body": {
                "data": "SGVsbG8gSmFja2llIQ==",
            },
        },
    }

    result = normalize_gmail_message(message)

    assert result.message_id == "message-1"
    assert result.thread_id == "thread-1"
    assert result.sender == "alice@example.com"
    assert result.recipients == ["bob@example.com"]
    assert result.subject == "Meeting tomorrow"
    assert result.sent_at is not None
    assert result.sent_at.year == 2026
    assert result.labels == ["INBOX", "IMPORTANT"]
    assert result.body_text == "Hello Jackie!"


def test_normalize_gmail_message_requires_message_id() -> None:
    message = {
        "threadId": "thread-1",
        "payload": {
            "headers": [],
        },
    }

    with pytest.raises(KeyError):
        normalize_gmail_message(message)

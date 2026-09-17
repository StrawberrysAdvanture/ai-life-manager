from typing import Any, cast

from googleapiclient.discovery import build  # type: ignore[import-untyped]

from app.integrations.gmail.auth import get_gmail_credentials


def get_gmail_profile() -> dict[str, Any]:
    credentials = get_gmail_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    result = service.users().getProfile(userId="me").execute()

    return cast(dict[str, Any], result)

from typing import Any, cast

from googleapiclient.discovery import build  # type: ignore[import-untyped]

from app.integrations.gmail.auth import get_gmail_credentials


class GmailClient:
    def __init__(self, service: Any) -> None:
        self._service = service

    def get_profile(self) -> dict[str, Any]:
        result = self._service.users().getProfile(userId="me").execute()
        return cast(dict[str, Any], result)

    def list_recent_message_ids(
        self,
        *,
        days: int = 7,
        max_results: int = 50,
    ) -> list[str]:
        result = (
            self._service.users()
            .messages()
            .list(
                userId="me",
                q=f"newer_than:{days}d",
                maxResults=max_results,
            )
            .execute()
        )

        messages = result.get("messages", [])

        return [message["id"] for message in messages if "id" in message]

    def get_message(self, message_id: str) -> dict[str, Any]:
        result = (
            self._service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )

        return cast(dict[str, Any], result)

    def get_thread(self, thread_id: str) -> dict[str, Any]:
        result = (
            self._service.users()
            .threads()
            .get(
                userId="me",
                id=thread_id,
                format="full",
            )
            .execute()
        )

        return cast(dict[str, Any], result)


def create_gmail_client() -> GmailClient:
    credentials = get_gmail_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    return GmailClient(service)

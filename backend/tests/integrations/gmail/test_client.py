from unittest.mock import MagicMock

from app.integrations.gmail.client import GmailClient


def test_list_recent_message_ids() -> None:
    service = MagicMock()

    messages = service.users.return_value.messages.return_value
    messages.list.return_value.execute.return_value = {
        "messages": [
            {"id": "message-1", "threadId": "thread_1"},
            {"id": "message-2", "threadId": "thread_2"},
        ]
    }

    client = GmailClient(service)

    result = client.list_recent_message_ids(days=7, max_results=2)

    assert result == ["message-1", "message-2"]

    messages.list.assert_called_once_with(
        userId="me",
        q="newer_than:7d",
        maxResults=2,
    )


def test_get_message() -> None:
    service = MagicMock()

    expected_message = {
        "id": "message-1",
        "threadId": "thread-1",
        "snippet": "Hello from a fake email",
    }

    messages = service.users.return_value.messages.return_value
    messages.get.return_value.execute.return_value = expected_message

    client = GmailClient(service)

    result = client.get_message("message-1")

    assert result == expected_message

    messages.get.assert_called_once_with(
        userId="me",
        id="message-1",
        format="full",
    )


def test_get_thread() -> None:
    service = MagicMock()

    expected_thread = {
        "id": "thread-1",
        "messages": [
            {"id": "message-1"},
            {"id": "message-2"},
        ],
    }

    threads = service.users.return_value.threads.return_value
    threads.get.return_value.execute.return_value = expected_thread

    client = GmailClient(service)

    result = client.get_thread("thread-1")

    assert result == expected_thread

    threads.get.assert_called_once_with(
        userId="me",
        id="thread-1",
        format="full",
    )


def test_list_message_ids_returns_empty_list_when_no_messages() -> None:
    service = MagicMock()

    messages = service.users.return_value.messages.return_value
    messages.list.return_value.execute.return_value = {}

    client = GmailClient(service)

    result = client.list_recent_message_ids(
        days=7,
        max_results=50,
    )

    assert result == []

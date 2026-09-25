from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NormalizedGmailMessage:
    message_id: str
    thread_id: str
    sender: str | None
    recipients: list[str]
    subject: str | None
    sent_at: datetime | None
    labels: list[str]
    body_text: str

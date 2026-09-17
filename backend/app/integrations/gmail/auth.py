from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import-untyped]

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"

GMAIL_SECRETS_DIR = Path(".secrets/gmail")
GMAIL_CLIENT_SECREAT_PATH = GMAIL_SECRETS_DIR / "credentials.json"
GMAIL_TOKEN_PATH = GMAIL_SECRETS_DIR / "token.json"


def get_gmail_credentials() -> Credentials:
    credentials: Credentials | None = None

    if GMAIL_TOKEN_PATH.exists():
        credentials = Credentials.from_authorized_user_file(  # type: ignore[no-untyped-call]
            GMAIL_TOKEN_PATH,
            scopes=[GMAIL_READONLY_SCOPE],
        )

    if credentials and credentials.valid:
        return credentials

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())  # type: ignore[no-untyped-call]
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            GMAIL_CLIENT_SECREAT_PATH,
            scopes=[GMAIL_READONLY_SCOPE],
        )
        credentials = flow.run_local_server(port=0)

    GMAIL_TOKEN_PATH.write_text(credentials.to_json())

    return credentials

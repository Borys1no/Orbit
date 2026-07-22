"""Calendar service — fetches events from Google Calendar API."""

from __future__ import annotations

from datetime import datetime, timezone

from orbit.core.logger import get_logger
from orbit.plugins.calendar.models import EventData

logger = get_logger("calendar")

_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

_API_SERVICE = "calendar"
_API_VERSION = "v3"


class CalendarService:
    """Retrieves upcoming events from Google Calendar."""

    def __init__(
        self,
        credentials_path: str,
        token_path: str,
        calendar_id: str = "primary",
    ) -> None:
        self._credentials_path = credentials_path
        self._token_path = token_path
        self._calendar_id = calendar_id
        self._service = None

    def _get_credentials(self):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from pathlib import Path

        creds = None
        token = Path(self._token_path)

        if token.exists():
            creds = Credentials.from_authorized_user_file(str(token), _SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credentials_path, _SCOPES
                )
                creds = flow.run_local_server(port=0)

            token.write_text(creds.to_json())

        return creds

    def _get_service(self):
        if self._service is None:
            from googleapiclient.discovery import build

            creds = self._get_credentials()
            self._service = build(_API_SERVICE, _API_VERSION, credentials=creds)
        return self._service

    def get_events(self, max_results: int = 10) -> list[EventData]:
        """Fetch upcoming events from the calendar."""
        service = self._get_service()

        now = datetime.now(timezone.utc).isoformat()
        result = (
            service.events()
            .list(
                calendarId=self._calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        items = result.get("items", [])
        events: list[EventData] = []

        for item in items:
            start = item.get("start", {})
            end = item.get("end", {})

            events.append(
                EventData(
                    event_id=item.get("id", ""),
                    summary=item.get("summary", ""),
                    description=item.get("description", ""),
                    start=start.get("dateTime", start.get("date", "")),
                    end=end.get("dateTime", end.get("date", "")),
                    location=item.get("location", ""),
                )
            )

        logger.debug("Fetched %d events", len(events))
        return events

    def is_available(self) -> bool:
        """Check if credentials are configured."""
        from pathlib import Path

        return Path(self._credentials_path).exists()

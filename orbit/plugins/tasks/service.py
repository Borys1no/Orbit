"""Tasks service — fetches tasks from Google Tasks API."""

from __future__ import annotations

from orbit.core.logger import get_logger
from orbit.plugins.tasks.models import TaskData

logger = get_logger("tasks")

_SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]

_API_SERVICE = "tasks"
_API_VERSION = "v1"


class TasksService:
    """Retrieves tasks from Google Tasks."""

    def __init__(
        self,
        credentials_path: str,
        token_path: str,
        task_list: str = "@default",
    ) -> None:
        self._credentials_path = credentials_path
        self._token_path = token_path
        self._task_list = task_list
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

    def get_tasks(self) -> list[TaskData]:
        """Fetch tasks from the specified task list."""
        service = self._get_service()
        result = (
            service.tasks()
            .list(tasklist=self._task_list, maxResults=20, showCompleted=False)
            .execute()
        )

        items = result.get("items", [])
        tasks: list[TaskData] = []

        for item in items:
            tasks.append(
                TaskData(
                    task_id=item.get("id", ""),
                    title=item.get("title", ""),
                    notes=item.get("notes", ""),
                    status=item.get("status", ""),
                    due=item.get("due", ""),
                )
            )

        logger.debug("Fetched %d tasks", len(tasks))
        return tasks

    def is_available(self) -> bool:
        """Check if credentials are configured."""
        from pathlib import Path

        return Path(self._credentials_path).exists()

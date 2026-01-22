import datetime
import logging

logger = logging.getLogger(__name__)


class MockMoodleClient:
    def __init__(self):
        self.token = "mock_token"
        self.user_id = 123

    def authenticate(self) -> bool:
        return True

    def get_upcoming_deadlines(self) -> list[dict]:
        """Return some fake deadlines for testing."""
        now = datetime.datetime.now().timestamp()
        return [
            {
                "id": "assign_mock_1",
                "title": "CS101: Mock Assignment 1",
                "due_date": now + 3600,  # 1 hour from now
                "type": "Assignment",
            },
            {
                "id": "quiz_mock_1",
                "title": "MA202: Mock Quiz 1",
                "due_date": now + 7200,  # 2 hours from now
                "type": "Quiz",
            },
            {
                "id": "assign_mock_old",
                "title": "CS101: Past Assignment",
                "due_date": now - 3600,  # 1 hour ago
                "type": "Assignment",
            },
        ]

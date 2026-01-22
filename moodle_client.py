import requests
import logging
from typing import List, Dict, Optional
from config import MOODLE_URL, MOODLE_USERNAME, MOODLE_PASSWORD

logger = logging.getLogger(__name__)


class MoodleClient:
    def __init__(self):
        self.base_url = MOODLE_URL.rstrip("/")
        self.token = None
        self.user_id = None

    def authenticate(self) -> bool:
        """Get web service token using user credentials."""
        url = f"{self.base_url}/login/token.php"
        params = {
            "username": MOODLE_USERNAME,
            "password": MOODLE_PASSWORD,
            "service": "moodle_mobile_app",
        }
        try:
            response = requests.post(url, data=params, timeout=30)
            data = response.json()
            if "token" in data:
                self.token = data["token"]
                logger.info("Moodle authentication successful")
                return True
            else:
                logger.error(f"Moodle authentication failed: {data.get('error')}")
                return False
        except Exception as e:
            logger.error(f"Moodle authentication error: {e}")
            return False

    def _call_ws(self, function: str, params: Dict = None) -> Optional[Dict]:
        """Call a Moodle web service function."""
        if not self.token:
            if not self.authenticate():
                return None

        url = f"{self.base_url}/webservice/rest/server.php"
        all_params = {
            "wstoken": self.token,
            "wsfunction": function,
            "moodlewsrestformat": "json",
        }
        if params:
            all_params.update(params)

        try:
            response = requests.post(url, data=all_params, timeout=30)
            return response.json()
        except Exception as e:
            logger.error(f"Error calling Moodle WS {function}: {e}")
            return None

    def get_upcoming_deadlines(self) -> List[Dict]:
        """Fetch upcoming assignments and quizzes."""
        deadlines = []

        # 1. Get user's courses
        site_info = self._call_ws("core_webservice_get_site_info")
        if not site_info:
            return []

        self.user_id = site_info.get("userid")

        # 2. Get assignments
        # Note: mod_assign_get_assignments can return all assignments for all courses
        # if courseids is not provided or empty in some versions.
        # But for robustness, we might need to get course IDs first.
        assignments_data = self._call_ws("mod_assign_get_assignments")
        if assignments_data and "courses" in assignments_data:
            for course in assignments_data["courses"]:
                for assign in course.get("assignments", []):
                    # duedate is a Unix timestamp
                    deadlines.append(
                        {
                            "id": f"assign_{assign['id']}",
                            "title": f"{course['shortname']}: {assign['name']}",
                            "due_date": assign["duedate"],
                            "type": "Assignment",
                        }
                    )

        # 3. Get quizzes
        # Quizzes usually need to be fetched per course
        courses = self._call_ws(
            "core_enrol_get_users_courses", {"userid": self.user_id}
        )
        if courses:
            for course in courses:
                quizzes_data = self._call_ws(
                    "mod_quiz_get_quizzes_by_courses", {"courseids[0]": course["id"]}
                )
                if quizzes_data and "quizzes" in quizzes_data:
                    for quiz in quizzes_data["quizzes"]:
                        # timeclose is a Unix timestamp
                        if quiz.get("timeclose"):
                            deadlines.append(
                                {
                                    "id": f"quiz_{quiz['id']}",
                                    "title": f"{course['shortname']}: {quiz['name']}",
                                    "due_date": quiz["timeclose"],
                                    "type": "Quiz",
                                }
                            )

        return deadlines

import unittest
import requests
from models.conferences import ConferenceModel

BASE_URL = "http://localhost:8080/api/conferences/"
conference_id: str = ""


class TestConferenceAPI(unittest.TestCase):

    def setUp(self):
        conference_data = ConferenceModel(
            name="Test Conference",
            articles=[],
            date_of_conference=["2024-12-01"]
        )
        response = requests.post(BASE_URL, json=conference_data.model_dump())
        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.json())
        self.conference_id = response.json()["_id"]

    def test_create_conference(self):
        pass

    def test_get_all_conferences(self):
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        conferences = response.json()
        self.assertIsInstance(conferences, list)

    def test_get_conference(self):
        response = requests.get(f"{BASE_URL}{self.conference_id}")
        self.assertEqual(response.status_code, 200)
        conference = response.json()
        self.assertEqual(conference["name"], "Test Conference")

    def test_update_conference(self):
        updated_data = ConferenceModel(
            name="Updated Test Conference",
            articles=[],
            date_of_conference=["2024-12-01"]
        )
        response = requests.put(
            f"{BASE_URL}{self.conference_id}", json=updated_data.model_dump()
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["date_of_conference"], updated_data.date_of_conference)

    def test_delete_conference(self):
        response = requests.delete(f"{BASE_URL}{self.conference_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

import unittest
import requests


class TestUserAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8080/users"

    def test_retrieve_user_by_name(self):
        response = requests.get(
            f"{self.BASE_URL}/search_by_name?first_name=Kirill&last_name=Sokolsky")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user_by_login(self):
        response = requests.get(
            f"{self.BASE_URL}/search_by_username?username=sunestss")
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        data = {
            "user_name": "new_user",
            "first_name": "Jonny",
            "second_name": "Dep",
            "affiliation": "MAI",
            "password": "new_password"
        }
        response = requests.post(f"{self.BASE_URL}/create_user", json=data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_details(self):
        response = requests.get(f"{self.BASE_URL}/get_user_details?id=1")
        self.assertEqual(response.status_code, 200)

    def test_delete_existing_user(self):
        response = requests.delete(f"{self.BASE_URL}/remove_user?user_id=11")
        self.assertEqual(response.status_code, 200)

    def test_update_existing_user(self):
        data = {
            "affiliation": "IPU"
        }
        response = requests.put(
            f"{self.BASE_URL}/update_user?user_id=12", json=data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

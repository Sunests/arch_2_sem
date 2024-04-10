import unittest
import requests

BASE_URL = "http://localhost:8081/api"
article_id: str = ""


class TestArticleAPI(unittest.TestCase):
    def setUp(self):
        article_data = {
            "title": "Test Article",
            "text": "This is a test article.",
            "UDK": "1234-5678",
            "date_of_load": "2024-04-10",
            "presentation_date": "2024-11-21",
        }
        response = requests.post(f"{BASE_URL}/articles", json=article_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("_id", response.json())
        self.article_id = response.json()["_id"]

    def test_create_article(self):
        pass

    def test_read_article(self):
        response = requests.get(f"{BASE_URL}/articles/{self.article_id}")
        self.assertEqual(response.status_code, 200)
        article = response.json()
        self.assertEqual(article["title"], "Test Article")

    def test_update_article(self):
        updated_data = {
            "title": "Updated Test Article",
            "text": "This is an updated test article.",
            "UDK": "1234-5678",
            "date_of_load": "2024-04-10",
            "presentation_date": "2024-11-21",
        }
        response = requests.put(
            f"{BASE_URL}/articles/{self.article_id}", json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], updated_data["title"])

    def test_delete_article(self):
        response = requests.delete(f"{BASE_URL}/articles/{self.article_id}")
        self.assertEqual(response.status_code, 204)

    def test_get_all_articles(self):
        response = requests.get(f"{BASE_URL}/articles")
        self.assertEqual(response.status_code, 200)
        articles = response.json()
        self.assertIsInstance(articles, list)


if __name__ == '__main__':
    unittest.main()

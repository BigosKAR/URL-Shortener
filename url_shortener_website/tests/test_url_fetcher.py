from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.url_service import URLService
from unittest.mock import patch, MagicMock
from url_shortener_website.utils.url_fetcher_service import UrlFetcherService
from url_shortener_website.utils.user_url_mapping_repository import UserUrlRepository

# Create your tests here.

class TestUrlFetcherUnit(TestCase):
    def setUp(self):
        self.mock_url_repo = MagicMock()
        self.mock_user_url_repo = MagicMock()
        self.url_fetcher = UrlFetcherService(
            url_repo=self.mock_url_repo,
            user_url_repo=self.mock_user_url_repo
        )

    def test_get_latest(self):
        self.mock_url_repo.get_latest.return_value = [
            {"shortcode": "def", "original_url": "https://example2.com"},
            {"shortcode": "abc", "original_url": "https://example1.com"},
        ]

        result = self.url_fetcher.get_latest(2)

        self.assertEqual(result, {
            "http://127.0.0.1:8000/def": "https://example2.com",
            "http://127.0.0.1:8000/abc": "https://example1.com"
        })

    def test_get_user_urls(self):
        self.mock_user_url_repo.get_user_mappings.return_value = [1]
        self.mock_url_repo.get_multiple_by_id.return_value = [
            MagicMock(shortcode="abc", original_url="https://example1.com", clicks=10)
        ]
    
        result = self.url_fetcher.get_user_urls(1)

        self.assertEqual(result, {
            "abc": {
                "shortened_url": "http://127.0.0.1:8000/abc",
                "original_url": "https://example1.com",
                "clicks": 10
            }
        })
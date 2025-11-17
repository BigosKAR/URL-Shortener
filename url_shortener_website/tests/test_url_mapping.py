from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.url_mapping_repository import URLMappingRepository
from ..models import UrlMapping, UserUrlMapping, UserAccount
from unittest.mock import patch, MagicMock


# Create your tests here.

# Integration tests

class TestUrlMappingRepositoryIntegration(TestCase):
    def setUp(self):
        self.url1 = UrlMapping.objects.create(
            shortcode="abc",
            original_url="https://example1.com"
        )
        self.url2 = UrlMapping.objects.create(
            shortcode="def",
            original_url="https://example2.com"
        )
        self.test_user = UserAccount.objects.create(
            email="test_user@gmail.com",
            hashed_password="test"
        )
        UserUrlMapping.objects.create(user_id=self.test_user, url_id=self.url1)
        UserUrlMapping.objects.create(user_id=self.test_user, url_id=self.url2)

    def test_get_mapping_urls(self):
        mappings = UserUrlMapping.objects.filter(user_id=1).values_list("url_id", flat=True)

        results = URLMappingRepository.get_mapping_urls(mappings)

        self.assertEqual(list(results), [self.url1, self.url2])

    def test_get_latests_urls(self):
        expected = [
            {'id': self.url2.id, 'shortcode': 'def', 'original_url': 'https://example2.com', 'clicks': 0},
            {'id': self.url1.id, 'shortcode': 'abc', 'original_url': 'https://example1.com', 'clicks': 0},
        ]

        results = list(URLMappingRepository.get_latest_urls(2))

        self.assertEqual(results, expected)

    def test_increment_click_count_success(self):
        self.assertEqual(self.url1.clicks, 0)

        returned_url = URLMappingRepository.increment_click_count("abc")

        self.url1.refresh_from_db()

        self.assertEqual(self.url1.clicks, 1)
        self.assertEqual(returned_url, "https://example1.com")

    def test_increment_click_count_multiple(self):
        URLMappingRepository.increment_click_count("def")
        URLMappingRepository.increment_click_count("def")

        self.url2.refresh_from_db()
        self.assertEqual(self.url2.clicks, 2)

    def test_increment_click_count_fail(self):

        non_existent_counter = URLMappingRepository.increment_click_count("non-existent")

        self.assertEqual(non_existent_counter, None)





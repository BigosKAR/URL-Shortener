from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.url_repository import UrlRepository
from ..models import UrlMapping, UserUrlMapping, UserAccount
from unittest.mock import patch, MagicMock

# Integration tests

class TestUrlRepositoryIntegration(TestCase):
    def setUp(self):
        self.repo = UrlRepository()
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

    def test_get_multiple_by_id(self):
        mappings = UserUrlMapping.objects.filter(user_id=1).values_list("url_id", flat=True)

        results = self.repo.get_multiple_by_id(mappings)

        self.assertCountEqual(results, [self.url1, self.url2])

    def test_get_latests_urls(self):
        # expected = [
        #     {'id': self.url2.id, 'shortcode': 'def', 'original_url': 'https://example2.com', 'clicks': 0},
        #     {'id': self.url1.id, 'shortcode': 'abc', 'original_url': 'https://example1.com', 'clicks': 0},
        # ]

        results = list(self.repo.get_latest(2))

        self.assertEqual(results[0], self.url2)
        self.assertEqual(results[1], self.url1)

    def test_increment_clicks_success(self):
        self.assertEqual(self.url1.clicks, 0)

        returned_obj = self.repo.increment_clicks("abc")

        self.url1.refresh_from_db()

        self.assertEqual(self.url1.clicks, 1)
        self.assertEqual(returned_obj, self.url1)

    def test_increment_clicks_multiple(self):
        self.repo.increment_clicks("def")
        self.repo.increment_clicks("def")

        self.url2.refresh_from_db()
        self.assertEqual(self.url2.clicks, 2)

    def test_increment_clicks_fail(self):

        non_existent_counter = self.repo.increment_clicks("non-existent")

        self.assertEqual(non_existent_counter, None)

    def test_create_new_url(self):
        url = "https://new.com"
        entry, created = self.repo.get_or_create(url)

        self.assertTrue(created)
        self.assertEqual(entry.original_url, url)
        self.assertTrue(UrlMapping.objects.filter(original_url=url).exists())

    def test_return_existing_url(self):
        entry, created = self.repo.get_or_create("https://example1.com")

        self.assertFalse(created)
        self.assertEqual(entry.id, self.url1.id)
        self.assertEqual(entry.original_url, self.url1.original_url)

    def test_get_by_id_exists(self):
        result = self.repo.get_by_id(self.url1.id)
        self.assertEqual(result, self.url1)

    def test_get_by_id_not_exists(self):
        result = self.repo.get_by_id(9999)
        self.assertFalse(result)
